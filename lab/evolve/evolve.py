#!/usr/bin/env python3
"""evolve.py - evolve VM designs: the faster and the smaller survive.

    lab/evolve/evolve.py --validate            the hand-made stages, rebuilt
                                               from their genomes, must give
                                               the build's images exactly
    lab/evolve/evolve.py [--pop N] [--gens G] [--rounds R] [--seed S] [--jobs N] [--until EPOCH]
    lab/evolve/evolve.py --report              report.md from what is known
    lab/evolve/evolve.py --remeasure N         the front measured again, N rounds
    lab/evolve/evolve.py --knockout [ID,...]   each gene set back to s6's value
    lab/evolve/evolve.py --sample N [--seed S] designs drawn uniformly, not bred
    --db FILE reads another database; -h or --help prints this. Any other
    option is refused: unrecognised, it would have started a run.

Needs a finished tools/build-stages.sh: its dumps, engine sources, cputime
and corpus. It keeps everything in build/evolve/: db.jsonl, one line per
design ever evaluated - genome, parents, how it was made, how it lived or
died, size, timings - and report.md. A design already in the database is
never measured twice, and a run resumes where the last one stopped.

GENOME - phase 1: the CV8 family, 8-byte cells
  tos        0/1   engine with the top of stack in a register (gen-tos)
  scale      0-3   call targets in units of 2^scale (engine SCALE, image --cpt)
  bytehdr    0/1   byte-granular headers (image --bytehdr, from the k64-b dump)
  spec       set   specialisation families of loc var tiny small imm
  sharedcall 0/1   one call path shared by every call opcode
  doesfar    0/1   DOES> children that reach anywhere (DOESFAR)
  varcall    0/1   opcodes that call through a variable (VARCALL)
  varslot    0/1   opcodes for variable slots (VARSLOT)
  d256       0/1   the 256-entry dispatch table (DISPATCH256)
  guard      0/1   guard pages below the stacks (GUARD)
  folds      list  primitives given a folded prim;EXIT opcode, at most 23, in
                   opcode order (gen-fold.py, and layout.py --fold-set)

LIFE. The engine must compile, the image convert, the corpus give the cell
engine's output byte for byte, and the kernel workload reproduce the
reference kernel byte for byte. Anything else dies, and the cause is kept.

FITNESS, both minimised and kept as a Pareto front, so nothing is traded:
  speed  geometric mean of the end-to-end time - cycles where the hardware
         counters can be read, CPU time otherwise - over the selection
         workloads, WORK_SEL: kernel, fib, corpus, loop, bubble, ackermann
         (since Iteration 127; until 41 kernel, fib, parse, corpus; from 41
         with loop), every program loaded from a FILE (standard input would
         measure read() calls, not engines)
  size   bytes of the engine plus the self-hosting image ('total': since
         Iteration 75; before it, the image alone) - with speed, memory
         (rss) and, under --widths 8,4, speed at 4-byte cells: the
         objectives of dominates(). The aim behind them: GOALS.md.
WORK_HELD is HELD OUT: never selected on, reported for the survivors, so a
design tuned to the selection does not pass unnoticed - sieve and parse
since Iteration 127 (loop until 41, sieve from 41).

OPERATORS
  mutation   a gene flipped or nudged; a fold added, removed or swapped
  crossover  two parents mixed gene by gene; folds drawn from both
  borrowing  a whole block - the call path, the header format, the dispatch,
             the folds - transplanted from an unrelated design
  selection  NSGA-II: rank by Pareto front, then by crowding, so designs
             that are different survive beside designs that are better
"""
import bisect, collections, hashlib, json, math, os, random, re, shutil, statistics, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
O = os.path.join(ROOT, 'build'); W = os.path.join(O, 'work')
EV = os.path.join(O, 'evolve'); DB = os.path.join(EV, 'db.jsonl'); CORPUS = os.path.join(EV, 'corpus.fth')
CPUT = os.path.join(O, 'cputime')
HOT = '+,=,!,@,LSHIFT,RSHIFT,C@,C!,AND,OR,XOR,LIT,<,U<,OVER,DROP,DUP,SWAP,ROT,>R,R>,R@,NEGATE'.split(',')
SPECS = ['loc', 'var', 'tiny', 'small', 'imm']
FOLDMAX = 23
# Primitives a fold may never take: control flow and the system's own.
NOFOLD = set('NOOP EXIT BRANCH ?BRANCH EXECUTE BYE SP@ SP! RP@ RP! WRITE READ (SYSTEM) SYSCALL (EXECVE) (WAITPID) (PIPE) (DUP2) (GETENV) (SETENV) (UNSETENV) (CHDIR) (GETCWD) (GETPID) ALLOCATE FREE RESIZE (GETPWHOME) (GETFSIZE) (SETFSIZE) (SYS-EXIT) (SYS-ARGC) (SYS-ARG)'.split()) | {n for n in []}
PRIMS = [l.split()[1] for l in open(os.path.join(ROOT, 'forth', 'kernel.4')) if l.startswith('PRIMITIVE')]
POOL = [p for p in PRIMS if p not in NOFOLD and 'FILE' not in p and 'LINE' not in p] or HOT
for h in HOT:
    if h not in POOL: POOL.append(h)

# Compiler genes, from gforth's and CPython's builds: a computed-goto
# interpreter loses its point if the compiler merges every dispatch into one
# shared indirect jump (-fno-gcse, -fno-crossjumping); gforth also keeps
# blocks in order and code compact. -fcf-protection=none drops endbr64.
CFLAGS = {'nogcse': '-fno-gcse', 'nocrossjump': '-fno-crossjumping', 'nocet': '-fcf-protection=none',
          'align1': '-falign-labels=1 -falign-jumps=1', 'noreorder': '-fno-reorder-blocks',
          # Iteration 7: what -fprofile-use switches on that helped s6 without
          # a profile - fib 6-7% better, beyond the layout-only band; on the
          # selection mean at the band's edge (lab/evolve/GENES.md).
          'peel': '-fpeel-loops', 'ipaclone': '-fipa-cp-clone', 'tracer': '-ftracer',
          # Iteration 113: for the binary - a function's alignment, and no
          # inlining of small functions (-O2 engines: ~1.1 and ~1.3 KB)
          'alignfn': '-falign-functions=1 -falign-loops=1', 'noinls': '-fno-inline-small-functions'}
CC0 = dict(opt='O2', nogcse=0, nocrossjump=0, nocet=0, align1=0, noreorder=0, peel=0, ipaclone=0, tracer=0)
# Genes added after runs were recorded: left out of a design's identity when
# off, so every design recorded before them keeps its id (databases resume,
# knockouts and reports still find their designs by id).
# Iteration 136: sysc likewise (results/syscall-pricing.md) - with NAME>BUF, after seed 39. Iteration 137: jitinl too.
# Iteration 129: jitloop is built and tested but DORMANT - in LATE, not yet in EXPRESSED, so no
# mutation turns it on: seeds 38 and 39 run the same genes (the owner); EXPRESSED takes it after 39.
LATE = ('threads', 'fsys', 'regpin', 'dskew', 'peel', 'ipaclone', 'tracer', 'hotcalls', 'rtimm', 'lean', 'rtloop', 'rtloopall', 'bss', 'kfast', 'tfind', 'kinput', 'klookup', 'thinhdr', 'rtiplus', 'swapi', 'tag2', 't2hot', 'jit', 'hotinl', 'opbody', 't2wide', 'rtempty', 'jitx', 'alignfn', 'noinls', 'fbuf', 'kstack', 'abortif', 'opcall', 'jitloop', 'sysc', 'jitinl', 'jitos', 'jittail', 'jitk', 'lto', 'gotodup', 'compiler')
HOTINLN = (0, 10, 20, 40)      # Iteration 92: inlined at the hottest call sites (lab/evolve/hotsites-v1.json)
FBUFV = (4096, 1024, 512)      # Iteration 115: a file's read-ahead buffer (results/deep-dive-2.md: memory)
HOTSITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotsites-v1.json')
HOTWORDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotwords-v1.json')   # Iteration 267: the gene factor's cold words (hotwords.py)
FACTORV = (0, 1e-3, 1e-2, 2.0)  # Iteration 267: factor - a word below this share of the reference dispatches is factored (2.0: every word)
OPBODY = ('(FIND)', '(>NUMBER)', 'THREAD-FIND', '+!', '?DUP', '2@', '2!', '>', '0=')   # Iteration 92: their bodies [opcode EXIT], the gene opbody; 290: 2@ 2!
HOTN = (0, 8, 16, 32)          # one-byte calls (Iteration 14): how many of the image's own words
CV8 = dict(tos=1, scale=3, bytehdr=0, spec=SPECS, sharedcall=1, doesfar=0, varcall=1, varslot=1,
           d256=0, guard=0, folds=HOT, skippad=0, fold=1, supers=[], rtfuse=0, ops10=[], escape=0, tail=0, msc=0)
def human(enc, **kw):
    g = dict(CV8, **CC0); g.update(enc=enc, **kw); return g
HUMAN = {   # the hand-made stages, as genomes; genes a family does not use lie dormant
    's0-cell':    human('cell'),
    's1-sod16':   human('sod16', scale=1, skippad=1, fold=0),
    's2-cpt16':   human('cpt16', scale=1, skippad=1, fold=0),
    's3-cpt16f':  human('cpt16', scale=3, skippad=0, fold=1),
    's4-cv8':     human('cv8', tos=0, spec=[], sharedcall=0, varcall=0, varslot=0),
    's5-cv8spec': human('cv8', lean=1),     # Iteration 166: the compiler's copies and the dump tool left out
    's6-cv8b':    human('cv8', scale=0, bytehdr=1, doesfar=1, lean=1),
}
FAMILIES = ['cell', 'sod16', 'cpt16', 'cv8']
# Which genes each family expresses; the rest are carried, not built.
EXPRESSED = {'cell': [], 'sod16': ['skippad'], 'cpt16': ['scale', 'skippad', 'fold', 'folds'],
             'cv8': ['tos', 'scale', 'bytehdr', 'spec', 'sharedcall', 'doesfar', 'varcall',
                     'varslot', 'd256', 'guard', 'folds', 'supers', 'rtfuse', 'ops10', 'escape', 'tail', 'msc', 'hotcalls', 'rtimm', 'lean', 'rtloop', 'rtloopall', 'bss', 'kfast', 'tfind', 'kinput', 'klookup', 'thinhdr', 'rtiplus', 'swapi', 'tag2', 't2hot', 'jit', 'hotinl', 'opbody', 't2wide', 'rtempty', 'jitx', 'alignfn', 'noinls', 'fbuf', 'kstack', 'abortif', 'opcall']}
# ---- the gene table (Iteration 276, prompts/17-variants-as-data) -----------
# A gene is one row: gene(name, values, show, family, late, needs, convert).
#   values  - what it can be, off first (a late gene's off is 0); none: 0/1;
#   show    - how a mutation names a value (default 'name=value');
#   family  - the encoding that expresses it (EXPRESSED); late - added after runs
#             were recorded, so out of a design's identity while off (LATE);
#   needs   - (g, e) -> true when it is expressed (applied last in express());
#   convert - g -> the converter's options (build()); it decides itself when -
#             factor's when expressed, the older flags by the genome, as before.
# mutate() and random_genome() read every gene's values from GENE_VALUES. The
# genes older than the table keep their rules in express() and their build code,
# with only their values here (GENE_VALUES.update, before mutate()); a gene that
# changes the engine still needs its build code. lab/evolve/gene-table-test.py
# adds a fictional gene and requires it to work with no code change.
GENE_VALUES, GENE_RULES, GENE_CONVERT = {}, [], []
def gene(name, values=None, show=None, family='cv8', late=True, needs=None, convert=None):
    global LATE
    listed = bool(family) and name in EXPRESSED[family]      # a gene older than its row keeps its place, and its late-ness (Iteration 278)
    if listed: assert (name in LATE) == bool(late), 'gene %s: listed already, %s LATE - say late=%s' % (name, 'in' if name in LATE else 'not in', name in LATE)
    elif late and name not in LATE: LATE = LATE + (name,)
    if family and not listed: EXPRESSED[family].append(name)
    if values is not None:
        values = tuple(values)
        assert not late or values[0] == 0, 'gene %s: a late gene is off at 0' % name
        GENE_VALUES[name] = (values, show or (lambda v, n=name: '%s=%s' % (n, v)))
    if needs: GENE_RULES.append((name, needs))
    if convert: GENE_CONVERT.append((name, convert))
# The older genes as rows (Iteration 278): their rules in registration order - tag2
# before the rules that read it; the dispatch cluster (varcall, sharedcall, doesfar,
# msc, tail, d256), the compiler's, the list genes', two value rewrites and the
# dormant sysc stay in express() as code. Genes listed above keep their place.
gene('rtfuse', late=False, needs=lambda g, e: e.get('supers') or rt_tests(g))  # nothing to fuse at run time otherwise; older than LATE
gene('rtimm', values=range(3), needs=lambda g, e: overlay(g) and 'imm' in g['spec'])   # Iteration 37: n + at run time needs both
gene('rtloop', values=range(3), needs=lambda g, e: rtloop_on(g))               # Iteration 41: a loop opcode to use
gene('rtloopall', needs=lambda g, e: rtloopall_on(g))                          # Iteration 43: all eight of them
gene('kfast', needs=lambda g, e: kfast_on(g))                                  # Iteration 49: byte headers
gene('tfind', needs=lambda g, e: tfind_on(g))                                  # Iteration 52: with kfast
gene('kinput', needs=lambda g, e: kinput_on(g))                                # Iteration 54: with kfast
gene('klookup', needs=lambda g, e: klookup_on(g))                              # Iteration 57: with kinput
gene('jit', needs=lambda g, e: jit_on(g))                                      # Iteration 80: phase 1's conditions
gene('rtiplus', needs=lambda g, e: rtiplus_on(g))                              # Iteration 60: with rtloopall
gene('swapi', needs=lambda g, e: swapi_on(g))                                  # Iteration 61: with 'imm'
gene('tag2', needs=lambda g, e: g['enc'] == 'cv8' and g['bytehdr'])            # Iteration 66: CV8, byte headers - before the rules that read it
gene('hotcalls', values=HOTN, needs=lambda g, e: e.get('varcall') and not e.get('tag2'))   # far-call prefixes; none under the tag
gene('t2hot', needs=lambda g, e: e.get('tag2'))                                # Iteration 71: with the tag (values: GENE_VALUES below)
gene('hotinl', values=HOTINLN, needs=lambda g, e: e.get('tag2'))               # Iteration 92: designs in the tag
gene('t2wide', needs=lambda g, e: t2wide_on(g))                                # Iteration 95: the tag, not multi-state
gene('rtempty', needs=lambda g, e: e.get('tag2'))                              # Iteration 101: the tag's run-time compiler
gene('kstack', needs=lambda g, e: e.get('tag2') and not kinput_on(g))          # Iteration 116: the tag's dumps; kinput has it already
gene('jitx', needs=lambda g, e: jit_on(g))                                     # Iteration 108: on the JIT
gene('opbody', needs=lambda g, e: any(w in OPBODY for w, _ in ops10_in(g)),    # Iteration 92: an opcode to point at
     convert=lambda g: ['--op-bodies'] if g.get('opbody') else [])
gene('bss', convert=lambda g: ['--bss'] if g.get('bss') else [])               # Iteration 44: scratch buffers out of the file
gene('thinhdr', convert=lambda g: ['--thin-header'] if g.get('thinhdr') else [])   # Iteration 58: one thread head, not 32
gene('abortif', convert=lambda g: ['--guard-abort'] if g.get('abortif') else [])   # Iteration 117: ABORT" behind IF ... THEN
gene('lean', convert=lambda g: ['--drop-x8', '--drop-dumptool'] if g.get('lean') else [])   # Iterations 38-39: build artifacts left out
gene('jitloop', needs=lambda g, e: jit_on(g))                                  # Iteration 129: on the JIT
gene('jitinl', needs=lambda g, e: jit_on(g) and g.get('jitx'))                # Iteration 137: in jitx's translator
gene('jitmul', needs=lambda g, e: jit_on(g))                                   # Iteration 472: UM* and UM/MOD, COUNT (results/drafts/jitapps-471.md)
gene('jitdoes', needs=lambda g, e: jit_on(g) and g.get('jitx'))              # Iteration 473: DOES> children native (jit.c)
gene('jitexec', needs=lambda g, e: jit_on(g) and g.get('jitx'))              # Iteration 476: EXECUTE through a helper (jit.c)
gene('jitcfa', needs=lambda g, e: jit_on(g) and g.get('jitx'))               # Iteration 482: the return-stack check along the paths
gene('jitrp', needs=lambda g, e: jit_on(g) and g.get('jitx') and not e.get('compiler') and cellw() == 8 and not g.get('lto'))   # 494; 516: not with lto - 'global register variable follows a function definition' (seed 71, 6 died)
gene('jitfuse', needs=lambda g, e: jit_on(g) and g.get('jitx'))              # Iteration 507: pairs as one stencil (jit-pairs-506.md)
gene('jitos', needs=lambda g, e: jit_on(g) and g['opt'] != 'Os')             # Iteration 239: the JIT's translator compiled for size; an -Os engine is so already
gene('jittail', needs=lambda g, e: jit_on(g))                                  # Iteration 246: the JIT's tail calls as jumps (results/price-jit-calls.md)
# Iteration 292: the [opcode EXIT] words among the primitives, so PRIMITIVE? lets the run-time
# compiler copy their opcode in place of a call (tools/layout.py --op-inline). It matters only
# where a design has such a word: an expressed format-10 opcode of layout.py's base list, or,
# opbody on, of OPBODY. Keep OPB_BASE as layout.py's _OPB before --op-bodies.
OPB_BASE = ('FILL', 'CMOVE', 'SCAN', 'SKIP', '(PARSE)', 'HASH', 'PLACE')
gene('opinline', needs=lambda g, e: any(w in OPB_BASE or (e.get('opbody') and w in OPBODY) for w in (e.get('ops10') or [])),
     convert=lambda g: ['--op-inline'] if express(g).get('opinline') else [])
# Iteration 293: clang 19+'s preserve_none and musttail in the tail-call engine (tools/gen-tail.py
# --preserve-none) - CPython 3.14's tail-call interpreter. Built with clang_pn(), the newest clang
# that takes them; expressed only on a clang tail engine, and only where such a clang is here.
gene('tailpn', needs=lambda g, e: e.get('tail') and e.get('compiler') and bool(clang_pn()))
# Iteration 295: NUMBER? as one opcode (forth/cv8b-knumber.4, after klookup's overlay) - on seed 49's
# fastest designs its own Forth was 10-13% of the corpus's dispatches. Expressed only with klookup.
gene('knumber', needs=lambda g, e: klookup_on(g))
# Iteration 298: the laptop's counters - the evolved interpreted designs stall in the front end half their
# cycles on compute work (results/counters-amd-ryzen-7-pro-8840hs.md); align1 only takes alignment away.
# GCC's -falign-jumps/-labels/-functions at 32 or 64 bytes: Zen 4's fetch window and op-cache line.
ALIGNV = (None, '32:11', '32', '64')   # 32:11 - aligned where it costs at most 10 bytes (GCC's n:m)
gene('alignhot', values=range(len(ALIGNV)), show=lambda v: 'alignhot=%s' % ALIGNV[v],
     needs=lambda g, e: not e.get('compiler') and not e.get('align1') and not e.get('alignfn'))
gene('jitret', needs=lambda g, e: jit_on(g))   # Iteration 404: EXIT as pop and jmp, not ret - the return predictor's depth (jit.c)
gene('jitvar', needs=lambda g, e: jit_on(g))   # Iteration 342: vf and vs (getstatic, putstatic) given the JIT
gene('jitimg', values=(0, 1), needs=lambda g, e: jit_on(g))   # Iteration 341: the image's words JIT candidates - 1 the outer interpreter (2, every plain code word, kills on the corpus: not offered)
gene('bfind', needs=lambda g, e: any(w in (e.get('ops10') or []) for w in ('THREAD-FIND', '(FIND)')))   # Iteration 316: the walk branch-light
gene('factor', values=range(len(FACTORV)),       # Iteration 267: repeated cold code in headerless shared bodies (results/drafts/factor-plan.md)
     needs=lambda g, e: e.get('tag2'),            # the tag's 2-byte calls and byte headers
     convert=lambda g: ['--factor', '--factor-hot', HOTWORDS, '--factor-share', repr(FACTORV[g['factor']])] if express(g).get('factor') else [])   # no table, no design: a missing file kills it loudly
EXPRESSED['cv8'] += ['jitk']      # Iteration 259: the top K cells in registers in the JIT's code (tools/gen-jitk.py)
EXPRESSED['cv8'] += ['lto', 'gotodup']   # Iteration 260: link-time optimisation; GCC's goto unfactoring (results/missed-options-2026-10.md)
# Iteration 262: the compiler - 0 GCC (cc), 1 clang. Offered only where clang is installed: elsewhere
# a design with it could not be built. Flags and genes one compiler lacks are not expressed under it.
HAVE_CLANG = bool(shutil.which('clang'))
_CLANG_PN = None
def clang_pn():
    """The newest clang here that takes preserve_none and musttail (19 and later), or ''
    - asked once, by compiling a line (Iteration 293, the gene tailpn)."""
    global _CLANG_PN
    if _CLANG_PN is None:
        _CLANG_PN = ''
        src = 'typedef void (__attribute__((preserve_none)) *f)(long);\n__attribute__((preserve_none)) void g(long a) { extern f h; __attribute__((musttail)) return h(a); }\n'
        for c in ('clang-22', 'clang-21', 'clang-20', 'clang-19', 'clang'):
            if shutil.which(c) and subprocess.run([c, '-x', 'c', '-c', '-o', os.devnull, '-'], input=src.encode(), capture_output=True).returncode == 0:
                _CLANG_PN = c; break
    return _CLANG_PN
if HAVE_CLANG: EXPRESSED['cv8'] += ['compiler']
GCC_ONLY = ('nogcse', 'nocrossjump', 'align1', 'noreorder', 'peel', 'ipaclone', 'tracer', 'noinls', 'gotodup', 'jitos', 'regpin', 'lto', 'alignhot')
JITKV = (0, 2, 3)                 # Iteration 259: the stack cache's size, cells - 0 off
gene('jitk', values=JITKV, needs=lambda g, e: jit_on(g) and e['jitk'])   # Iteration 259: on the JIT; 0 is off
EXPRESSED['cv8'] += ['threads']   # Iteration 204: the dictionary in 16, 32, 64 or 128 chains (results/loop-audit.md)
EXPRESSED['cv8'] += ['fsys']   # Iteration 202: file words and RESIZE in Forth, their handlers out
EXPRESSED['cv8'] += ['regpin']   # Iteration 197: the VM registers pinned, 0-3 (results/forth-implementations-survey.md)
EXPRESSED['cv8'] += ['dskew']   # Iteration 183 (the owner: the stacks' place): the data stack 2 KB lower - its top cells off the return stack's page offsets   # sysc retired with Iteration 147: every engine is SYSC   # the after-seed-39 batch: the dormant genes switched on
BLOCKS = [('sharedcall', 'd256'), ('scale', 'bytehdr', 'doesfar'), ('varcall', 'varslot'),
          ('spec',), ('folds',), ('tos', 'guard'), tuple(CC0), ('skippad', 'fold'), ('supers',), ('folds', 'supers'), ('ops10',), ('ops10', 'supers'), ('escape', 'ops10', 'supers'), ('tail',), ('tail', 'tos'), ('msc',), ('msc', 'tail'), ('hotcalls',), ('rtimm',), ('rtfuse', 'rtimm'), ('lean',), ('rtloop',), ('rtloopall',), ('rtloop', 'rtloopall', 'rtiplus', 'swapi'), ('bss', 'thinhdr'), ('kfast', 'tfind', 'kinput', 'klookup'), ('tag2', 't2hot', 't2wide'), ('hotinl',), ('opbody',), ('rtempty',), ('jitx',), ('alignfn',), ('noinls',), ('fbuf',), ('kstack',), ('abortif',), ('opcall',)]
# Superinstruction candidates: primitive pairs ranked by how often the CV8
# interpreter (s6, -DPROFILE=1, VMPROF) dispatched them over kernel, fib,
# parse and corpus, control flow, literals, EXIT and system calls excluded.
SUPER_POOL = [["DUP", ">R"], ["C!", "R>"], [">R", "C!"], ["ROT", "DUP"], ["R@", "ROT"], ["DUP", "C@"], [">R", "OVER"], ["OVER", "C@"], ["C@", "="], ["C@", "DUP"], ["SWAP", "R>"], ["LSHIFT", "OVER"], ["OVER", "R>"], ["ROT", "ROT"], ["C@", "SWAP"], ["C@", "OR"], ["SWAP", "DUP"], ["R>", "SWAP"], ["OVER", "R@"], ["C@", ">R"], ["DUP", "@"], ["+", "R>"], ["R>", "="], ["C@", "OVER"]]
SUPER_FREE = [126, 127]       # free in every CV8 engine; more when folds or SPEC give theirs up
def super_slots(g):
    """The opcodes superinstructions may take: 126 and 127, the fold band
    past the folds in use, and the specialisation band when SPEC is off -
    so folds, specialisations and pairs compete for the same slots."""
    return (SUPER_FREE + list(range(73 + len(g['folds']), 96)) + ([] if g['spec'] else list(range(96, 124)))
            + (list(range(27 if g.get('escape') == 2 else 36, 68)) if g.get('escape') else []))   # ESCAPE: primitives 36-67 behind a byte; level 2 from 27
LOOP10 = ('(DO)', '(LOOP)', '(+LOOP)', '(?DO)', '(LEAVE)', 'I', 'J', 'UNLOOP')
# Iteration 190: forth/cv8-fuse-loop.4's words reached only by its own code
# (and the converter, which fills the three tables by their names in the
# dump): rtloop=2 builds them headerless (tools/layout.py --headerless).
RTLOOP_INTERNAL = ('X10-OP', 'W@', 'CHAIN16?', 'RESOLVE-LEAVE16', 'RESOLVE-LEAVES', 'LOOP-OPS', 'X10-XTS', 'X10-OPS')
# Iteration 202, the gene fsys (results/drafts/fsys/README.md): six file words
# and RESIZE in Forth over SYSCALL (forth/file-sysc.4, loaded last in a -fsys
# dump), their handlers out of the engine: 27 of 68 primitives never ran in
# the eight workloads. A design without it builds from the dumps it always did.
FSYS_INTERNAL = ('FS-BLK', 'FS0', 'FS1', 'FS2', 'FS3', 'FS4', 'FS-DROP', 'FS-WRITE', 'FS-NL', 'FS-MMAP')   # called by file-sysc.4's words only
THREADS_N = {1: 64, 2: 128, 3: 16}   # Iteration 204, the gene threads: 0 as built (32 chains)
# Iteration 212 (the owner): a library that does not load whole must stop the
# run, not fall back. file-sysc5.4 once failed at a remark outside a comment;
# the definitions before it stood, fsys 3's READ-LINE stood in for fsys 5's
# under the same name, and every gate passed. So each dump is checked as it is
# made: (1) its load messages hold no error the kernel prints while loading;
# (2) every name each loaded file defines is among the dump's words - an error
# part-way through a file leaves its later names out.
DUMP_ERRORS = ('Undefined word', 'dictionary full', 'name too long', 'Incomplete control structure',
               'compile only', 'Not found', 'Error reading file')
DEFINERS = (':', 'CREATE', 'VARIABLE', 'CONSTANT', '2VARIABLE', '2CONSTANT', 'VALUE', 'DEFER')
_DEFS = {}
BASE_NAMES = collections.Counter()                  # the kernel image's own words, by count
def source_names(path):
    """The names a Forth source file defines, its comments and strings skipped."""
    if path not in _DEFS:
        toks, out = open(path, errors='replace').read().split('\n'), []
        words = []
        for line in toks:
            t = line.split()
            i = 0
            while i < len(t):
                w = t[i]
                if w == '\\': break                                # to the end of the line
                if w == '(' or w == '.(':                          # to the closing )
                    while i < len(t) and not t[i].endswith(')'): i += 1
                    i += 1; continue
                if w.upper() in ('S"', '."', 'ABORT"', 'C"'):    # to the closing "
                    i += 1
                    while i < len(t) and not t[i].endswith('"'): i += 1
                    i += 1; continue
                words.append(w); i += 1
        inside, k = False, 0                                # in a colon definition a definer is compiled, not run
        while k < len(words):
            w = words[k].upper()
            if inside:
                if w == ';': inside = False
            elif w == ':NONAME': inside = True
            elif w == ':' and k + 1 < len(words): out.append(words[k + 1].upper()); inside = True; k += 1
            elif w in DEFINERS and k + 1 < len(words): out.append(words[k + 1].upper()); k += 1
            k += 1
        _DEFS[path] = out
    return _DEFS[path]
def dump_guard(name, boot, out):
    text = out.replace(b'\r', b'').decode('latin-1')
    m = re.search(r'^S \d+ \d+', text, re.M)
    pre, body = (text[:m.start()], text[m.start():]) if m else (text, '')
    bad = [l.strip() for l in pre.split('\n') if any(e in l for e in DUMP_ERRORS)]
    have = collections.Counter(n.strip().upper() for n in re.findall(r'^N -?\d+ -?\d+ (.*)$', body, re.M))
    missing, want = {}, collections.Counter()
    for f in re.findall(r'S" (\S+)" INCLUDED', boot):
        src = os.path.join(ROOT, 'forth', f)
        if os.path.exists(src) and f != 'dict-dump-addr.4':     # the base dump has that one too
            lost = [n for n in source_names(src) if n not in have]
            if lost: missing[f] = lost
            want.update(source_names(src))
    # A redefinition that failed is invisible by name - the older definition
    # stands. By count it is not: loaded whole, a dump holds each name as often
    # as the kernel image (BASE_NAMES) and the loaded files define it.
    short = ['%s %d of %d' % (n, have[n], BASE_NAMES.get(n, 0) + k) for n, k in want.items() if have[n] < BASE_NAMES.get(n, 0) + k]
    if short: missing['(definitions by count)'] = short
    if bad or missing or not body:
        sys.exit('dump %s did not load whole - the run stops here, not on a fallback:%s%s%s' % (
            name, ''.join('\n  load message: %s' % b for b in bad[:5]),
            ''.join(('\n  by count - definitions missing (in the dump, of kernel + files): %s' % ', '.join(v[:8])) if f.startswith('(')
                    else '\n  forth/%s: %d of its names missing: %s' % (f, len(v), ' '.join(v[:8])) for f, v in missing.items()),
            '' if body else '\n  no dump records at all'))

def fsys_on(g):
    return bool(g.get('fsys')) and g['enc'] == 'cv8'
def fsys_level(g):                     # Iteration 205: 0 native, 1 seven words in Forth, 2 the single-SYSCALL family
    return g.get('fsys', 0) if fsys_on(g) else 0
FSYS2_INTERNAL = ('FS-OFL', 'FS-END', 'FS-SAVED')
FSYS2_REBIND = ('OPEN-FILE', 'CLOSE-FILE', 'WRITE-FILE', 'ALLOCATE', 'FREE')
FSYS3_INTERNAL = ('FS-P', 'FS-EDIT?', 'FS-SEEKS?', 'FS-BACK', 'FS-UPTO-EDIT', 'FS-ANY', 'FS-LF', 'FS-CR',
                  'FS-SK', 'FS-BIT', 'FS-FORGET')   # Iteration 206; the last three 208
FSYS3_REBIND = ('WRITE', 'READ', 'READ-LINE', 'BYE')
FSYS4_INTERNAL = ('FS-OB', 'FS-OMODE', 'FS-OSIZE', 'FS-OINIT')   # Iteration 207
FSYS5_INTERNAL = ('FS-RT', 'FS-RSIZE', 'FS-RE', 'FS-RESET', 'FS-GIVEBACK', 'FS-E', 'FS-LIM', 'FS-FILL', 'FS-TAKE')   # Iteration 211; 214: FS-LIM for FS-CNT, FS-MAX, FS-ERR

def rtloop_on(g):
    """Iteration 41: does this design compile loops at run time with its loop
    opcodes (forth/cv8-fuse-loop.4)? The gene, and any of them - each word
    uses its own where the design has it."""
    return g['enc'] == 'cv8' and bool(g.get('rtloop')) and any(n in g.get('ops10', []) for n in LOOP10)
def rtloopall_on(g):
    """Iteration 43: the compact run-time loop compiler (forth/cv8-fuse-loopall.4)
    in rtloop's place - for a design with all eight loop opcodes."""
    if not (rtloop_on(g) and bool(g.get('rtloopall')) and all(n in g.get('ops10', []) for n in LOOP10)): return False
    # Iteration 77: all eight must GET a slot. kinput's and klookup's words
    # claim theirs first; a loop opcode pushed out by them left the loop
    # compiler without it - the converter's LOOPTAB assertion, 8 deaths in
    # seed 18. I+ assumed to claim its slot whenever rtiplus is asked for.
    got = [w for w, _ in zip(ops10_order(g, bool(g.get('rtiplus'))), super_slots(g))]
    return all(n in got for n in LOOP10)
LOOP_REPAIR = float(os.environ.get('EVOLVE_LOOP_REPAIR', 0.25))
def rtloopall_repair(g):
    """Iteration 440 (results/audit-genes-designs-439.md): rtloopall's prerequisite met - the loop words missing from
    the format-10 list put first, where they get slots, and the run-time loop compiler on. In seed 62 only 92 of 5,819
    genomes setting rtloopall could express it (J, UNLOOP and (LEAVE) missing): eight entries at once, three of them
    worth little alone; and a tag-2 design without escape has 2-4 format-10 slots, too few for eight - escape on
    then (rtloopall and escape are linked already, LINKS). The search still weighs it: the words take slots from others."""
    fixed = []
    missing = [n for n in LOOP10 if n not in g.get('ops10', [])]
    if missing: g['ops10'] = missing + [w for w in g.get('ops10', []) if w not in missing]; fixed.append('+ops ' + ' '.join(missing))
    elif not rtloopall_on(g): g['ops10'] = list(LOOP10) + [w for w in g['ops10'] if w not in LOOP10]; fixed.append('loop ops first')
    if not g.get('rtloop'): g['rtloop'] = 1; fixed.append('rtloop=1')
    if not rtloopall_on(g) and not g.get('escape'): g['escape'] = 1; fixed.append('escape=1')   # the slots: 2-4 without it on the tag
    return fixed
def kfast_on(g):
    """Iteration 49: kernel words made faster for the byte-header system
    (forth/cv8b-kfast.4) - a byte-header CV8 design with the gene. (A
    cell-header version hung at the first lookup: an open item.)"""
    return g['enc'] == 'cv8' and bool(g.get('bytehdr')) and bool(g.get('kfast'))
def tfind_on(g):
    """Iteration 52: THREAD-FIND, kfast's thread walk, as the FIRST format-10
    opcode - sure of a slot. Seed 11 found it in the pool 7 times in 1,425
    designs, once with kfast: the biggest saving there, never taken up."""
    return kfast_on(g) and bool(g.get('tfind'))
KINPUT = ['SCAN', 'SKIP', 'FILL', '(PARSE)', 'HASH', 'PLACE']   # TABS>BL gone with Iteration 148: no tab is made a space
def kinput_on(g):
    """Iteration 54: the input side - forth/cv8b-kinput.4 (REFILL's tab loop
    was factored out as TABS>BL, gone with Iteration 148) and SCAN, SKIP and FILL first among the
    format-10 names: one switch, as tfind - a design with kfast."""
    return kfast_on(g) and bool(g.get('kinput'))
KLOOKUP = ['(FIND)', '(>NUMBER)']
def knumber_on(g):
    """Iteration 295: NUMBER? as one opcode - forth/cv8b-knumber.4, after klookup's overlay."""
    return bool(klookup_on(g) and g.get('knumber'))

def klookup_on(g):
    """Iteration 57: the whole lookup - forth/cv8b-klookup.4 ((FIND), FIND8)
    and (FIND) first among the format-10 names: a design with kinput."""
    return kinput_on(g) and bool(g.get('klookup'))
def swapi_on(g):
    """Iteration 61: SWAP+I (SWAP n +, Iteration 34) first among the
    format-10 names - in the pool since, and on none of seed 13's front: fib's
    SWAP -2 + took two dispatches. A design with the 'imm' specialisation."""
    return g['enc'] == 'cv8' and 'imm' in g['spec'] and bool(g.get('swapi'))
def rtiplus_on(g):
    """Iteration 60: I then + as I+ in code compiled at run time
    (forth/cv8-fuse-iplus.4) - a design with rtloopall, whose LOOPTAB knows I."""
    return rtloopall_on(g) and bool(g.get('rtiplus'))
def overlay(g):
    """Does this CV8 design need forth/cv8-fuse.4, the compiler that fuses
    pairs at run time? Only if it has pairs and the rtfuse gene. (Its fold
    list needs no overlay: the converter writes it into cv8.4's FOLD-OPS.)
    Everything else keeps the build's dumps, so the hand-made stages still
    come out byte-identical."""
    # Iteration 447: and rtiplus - I+ is found by the fuser's lookup, in its table; without the fuser it was expressed
    # and inert (seed 64: a plain design's loop -20.0% with the fuser, +0.0% without; 37 of the front's 55 without it)
    return g['enc'] == 'cv8' and (bool(g.get('rtfuse') and (supers_in(g) or rt_tests(g))) or rtimm2(g) or rtiplus_on(g))
def rtimm2(g):
    """Iteration 175: rtimm=2 - run-time immediates without pairs: the overlay
    for ADDI and SWAP+I alone (forth/cv8t-fuse.4's lookup over no pairs, then
    cv8t-fuse-imm.4). Seed 40's small designs carried rtimm=1 unexpressed: it
    waited on pairs and rtfuse, three mutations away (results/price-hybrid.md)."""
    return g['enc'] == 'cv8' and g.get('rtimm') == 2 and 'imm' in g['spec']
RTIMM_LEAN_INTERNAL = ('IMM-OPS', 'LIT-PREV', 'SMALL-LIT?', 'IMM+')
def rtimm_lean(g):
    """Iteration 422 (results/wip-regmachine/README.md): rtimm=2 in a plain-CV8 design with nothing else
    for the run-time fuser to do - no pairs, no fused tests - builds forth/cv8-imm.4 alone, not
    cv8-fuse.4 under cv8-fuse-imm.4 (rtimm=2 passes --rtfuse: built pairs and tests fuse, rtfuse or not)."""
    return rtimm2(g) and not (supers_in(g) or rt_tests(g)) and not express(g).get('tag2') and not rtiplus_on(g)   # 447: I+ needs the fuser
RT_TESTS = ('?NBRANCH', '<?BRANCH', '=?BRANCH', 'U<?BRANCH', '<>?BRANCH', '>?BRANCH', '0<?BRANCH')     # the long fused tests: what the overlay can fuse at run time
def rt_tests(g):
    """The fused tests this design has opcodes for - with rtfuse, its
    compiler fuses them in code compiled at run time (Iteration 9)."""
    return [w for w, _ in ops10_in(g) if w in RT_TESTS]
# relf's format-10 opcodes: kernel colon words given opcodes, where the
# converter finds their compiled body exactly as the engine implements it.
OPS10_POOL = ['EXECUTE', 'I', '(DO)', '+!', '?DUP', 'UNLOOP', 'J', '(LOOP)', '(?DO)', '(+LOOP)', '(LEAVE)',
              '?BRANCH8', 'BRANCH8',   # the short branches: not words, opcodes the converter uses where they fit
              '?NBRANCH', '?NBRANCH8',  # 0= ?BRANCH fused, long and short (Iteration 8); the short needs the long
              '<?BRANCH', '<?BRANCH8',  # < ?BRANCH fused (Iteration 9); at run time too, with rtfuse
              '=?BRANCH', '=?BRANCH8', 'U<?BRANCH', 'U<?BRANCH8',
              '<>?BRANCH', '<>?BRANCH8', '>?BRANCH', '>?BRANCH8', '0<?BRANCH', '0<?BRANCH8', '=I?BRANCH', '=I?BRANCH8',   # Iteration 12
              'DUP?BRANCH', 'DUP?BRANCH8', 'OVER?BRANCH', 'OVER?BRANCH8',   # Iteration 33: tests that keep their value
              'DUP?NBRANCH', 'DUP?NBRANCH8', 'SWAP+I', 'DUP+I', 'DUP<I',   # Iteration 34: DUP 0= ?BRANCH kept; SWAP n +
              'FILL', 'CMOVE',                           # Iteration 50: the kernel's byte loops
              'THREAD-FIND',                             # Iteration 51: the byte-header thread walk (kfast's)
              'SCAN', 'SKIP',                            # Iteration 54: the input side (TABS>BL went, Iteration 148; kinput's)
              '(PARSE)', 'HASH', 'PLACE',                # Iteration 54: ((PARSE): kinput's)
              '(FIND)', '(>NUMBER)',                     # Iteration 57: the lookup, numbers (klookup's)
              'I+',
              '2@', '2!',   # Iteration 290: bubble's and the corpus's double-cell words (results/source-audit-2.md)
              '>', '0=']   # Iteration 299: bubble's compare, ackermann's test (results/source-audit-3.md)                                      # Iteration 60: I then + in run-time code (rtiplus's)
OPS10_LABEL = {'2@': 'L_x_2fetch', '2!': 'L_x_2store', '>': 'L_x_gt', '0=': 'L_x_zeq',   # Iteration 290
               '+!': 'L_x_plusstore', '?DUP': 'L_x_qdup', 'EXECUTE': 'L_x_execute', 'I': 'L_x_i',
               'J': 'L_x_j', 'UNLOOP': 'L_x_unloop', '(DO)': 'L_x_do', '(LOOP)': 'L_x_loop',
               '(?DO)': 'L_x_qdo', '(+LOOP)': 'L_x_ploop', '(LEAVE)': 'L_x_leave',
               '?BRANCH8': 'L_x_qbr8', 'BRANCH8': 'L_x_br8', '?NBRANCH': 'L_x_nqbr', '?NBRANCH8': 'L_x_nqbr8',
               '<?BRANCH': 'L_x_ltbr', '<?BRANCH8': 'L_x_ltbr8', '=?BRANCH': 'L_x_eqbr', '=?BRANCH8': 'L_x_eqbr8',
               'U<?BRANCH': 'L_x_ultbr', 'U<?BRANCH8': 'L_x_ultbr8',
               '<>?BRANCH': 'L_x_nebr', '<>?BRANCH8': 'L_x_nebr8', '>?BRANCH': 'L_x_sgtbr', '>?BRANCH8': 'L_x_sgtbr8',
               '0<?BRANCH': 'L_x_zltbr', '0<?BRANCH8': 'L_x_zltbr8', '=I?BRANCH': 'L_x_eqibr', '=I?BRANCH8': 'L_x_eqibr8',
               'DUP?BRANCH': 'L_x_dupbr', 'DUP?BRANCH8': 'L_x_dupbr8', 'OVER?BRANCH': 'L_x_overbr', 'OVER?BRANCH8': 'L_x_overbr8',
               'DUP?NBRANCH': 'L_x_dupnbr', 'DUP?NBRANCH8': 'L_x_dupnbr8', 'SWAP+I': 'L_x_swapaddi', 'DUP+I': 'L_x_dupaddi', 'DUP<I': 'L_x_duplti',
               'FILL': 'L_x_fill', 'CMOVE': 'L_x_cmove', 'THREAD-FIND': 'L_x_threadfind',
               'SCAN': 'L_x_scan', 'SKIP': 'L_x_skip', '(PARSE)': 'L_x_parse', 'HASH': 'L_x_hash', 'PLACE': 'L_x_place', '(NUMBER?)': 'L_x_numberq', '(FIND)': 'L_x_find', '(>NUMBER)': 'L_x_tonumber', 'I+': 'L_x_iplus'}
# Iteration 12's handlers are compiled only where a design has them (engine/vm-lab.c)
X_MACRO = {'<>?BRANCH': 'X_NEBR', '<>?BRANCH8': 'X_NEBR', '>?BRANCH': 'X_SGTBR', '>?BRANCH8': 'X_SGTBR',
           '0<?BRANCH': 'X_ZLTBR', '0<?BRANCH8': 'X_ZLTBR', '=I?BRANCH': 'X_EQIBR', '=I?BRANCH8': 'X_EQIBR',
           'DUP?BRANCH': 'X_DUPBR', 'DUP?BRANCH8': 'X_DUPBR', 'OVER?BRANCH': 'X_OVERBR', 'OVER?BRANCH8': 'X_OVERBR',
           'DUP?NBRANCH': 'X_DUPNBR', 'DUP?NBRANCH8': 'X_DUPNBR', 'SWAP+I': 'X_SWAPADDI', 'DUP+I': 'X_DUPADDI', 'DUP<I': 'X_DUPLTI',
           'FILL': 'X_FILL', 'CMOVE': 'X_CMOVE', 'THREAD-FIND': 'X_THREADFIND',
           'SCAN': 'X_SCAN', 'SKIP': 'X_SKIP', '(PARSE)': 'X_PARSE', 'HASH': 'X_HASH', 'PLACE': 'X_PLACE', '(NUMBER?)': 'X_NUMBERQ', '(FIND)': 'X_FIND', '(>NUMBER)': 'X_TONUMBER', 'I+': 'X_IPLUS'}
def newest_front():
    """(path, records) of the newest run's results file - its front's designs, genomes and
    measures (Iteration 278: c-baseline.py and counters.py choose their designs from it)."""
    import glob                                   # not among the module's imports
    fs = sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed*.md')), key=lambda f: int(re.search(r'seed(\d+)\.md$', f).group(1)) if re.search(r'seed(\d+)\.md$', f) else -1)
    recs = [json.loads(l) for l in open(fs[-1], errors='replace') if l.startswith('{"bin"')]
    return fs[-1], recs
def recorded_genome(i):
    """A recorded design's genome, from results/evolve-*.md - None if absent (Iteration 155)."""
    import glob
    key = '"id": "%s"' % i
    for p in sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md'))):
        for l in open(p, errors='replace'):
            if l.startswith('{"bin"') and key in l:
                try: return json.loads(l)['genome']
                except ValueError: pass
    return None

def jit_on(g):
    """Iteration 80 (JIT.md): the lazy JIT - colon words compiled at run time
    translated to native code on their first call (engine/jit.c, SPN's
    stencils). Phase 1: the two-bit tag, byte headers, the cached top of
    stack, one state, no tail calls; x86-64."""
    return (g['enc'] == 'cv8' and bool(g.get('jit')) and bool(g.get('tag2')) and bool(g['bytehdr'])
            and bool(g['tos']) and not g.get('msc') and not g.get('tail') and os.uname().machine == 'x86_64')
def t2wide_on(g):
    """Iteration 95: the tag without its 3-byte call - 0x80-0xBF 64 more one-byte
    codes (127), calls of 2 bytes (16 KB) and 4 (1 GB). Not yet for multi-state
    caching: tools/gen-msc.py builds its tables with three call widths."""
    return (g['enc'] == 'cv8' and bool(g.get('t2wide')) and bool(g.get('tag2')) and bool(g['bytehdr'])
            and not (g.get('msc') and g['tos']))
def ops10_order(g, iplus):
    """The format-10 words in the order they claim slots; iplus: whether I+
    claims one (rtiplus) - a parameter, so rtloopall_on can ask without
    recursing through rtiplus_on (Iteration 77)."""
    ws = [w for w in g.get('ops10', []) if w != 'THREAD-FIND' or kfast_on(g)]   # Iteration 51: a kfast word
    if tfind_on(g): ws = ['THREAD-FIND'] + [w for w in ws if w != 'THREAD-FIND']  # Iteration 52: first, sure of a slot
    ws = [w for w in ws if w != 'TABS>BL']                                         # Iteration 148: gone - a genome naming it frees the slot
    ws = [w for w in ws if w != '(PARSE)' or kinput_on(g)]                         # Iteration 54: kinput's words
    if kinput_on(g):                                                               # Iteration 54: next, sure of slots
        ws = ws[:1 if tfind_on(g) else 0] + KINPUT + [w for w in ws[1 if tfind_on(g) else 0:] if w not in KINPUT]
    ws = [w for w in ws if w not in KLOOKUP or klookup_on(g)]                      # Iteration 57: klookup's words
    if klookup_on(g): ws = KLOOKUP + [w for w in ws if w not in KLOOKUP]           # Iteration 57: first of all
    ws = [w for w in ws if w != '(NUMBER?)']                                       # Iteration 295: knumber's, after them
    if knumber_on(g): ws = ['(NUMBER?)'] + ws                                      # first: the gene is the opcode
    ws = [w for w in ws if w != 'I+' or iplus]                                     # Iteration 60: rtiplus's
    if iplus: ws = ['I+'] + [w for w in ws if w != 'I+']                           # Iteration 60: sure of a slot
    if swapi_on(g): ws = ['SWAP+I'] + [w for w in ws if w != 'SWAP+I']             # Iteration 61: sure of a slot
    return ws
def ops10_in(g):
    """[[word, opcode], ...]: they take the free slots first, the pairs the rest."""
    return [[w, op] for w, op in zip(ops10_order(g, rtiplus_on(g)), super_slots(g))]
def supers_in(g):
    """[[first, second, opcode], ...] for the pairs that get a slot."""
    return [[a, b, op] for (a, b), op in zip(g['supers'], super_slots(g)[len(ops10_in(g)):])]
# Iteration 121, the gene opcall (results/docs-reuse.md - Koopman's op+CALL,
# priced at 2.7-6.6% of dispatches): an operation and the call after it as one
# opcode - the operation, then straight into the call's code, no table
# dispatch. The pool: operations without an operand that come before calls
# most (the fastest and the smallest designs' profiles), each with its handler
# in the engine; 0= and 1+ are the tiny specialisation's, (PARSE) and PLACE
# format-10 words - offered only where the design has them.
OPCALL_POOL = {'DROP': 'L_drop', 'AND': 'L_and', '@': 'L_fetch', '>R': 'L_tor', 'C@': 'L_cfetch', 'SWAP': 'L_swap',
               'DUP': 'L_dup', 'ROT': 'L_rot', 'OVER': 'L_over', 'R>': 'L_fromr', '+': 'L_plus', 'OR': 'L_or',
               '0=': 'L_zeq', '1+': 'L_onep', '(PARSE)': 'L_x_parse', 'PLACE': 'L_x_place'}
def opcall_on(g):
    """The tag's computed-goto engines: the tail-call and multi-state
    generators rewrite handlers their own way."""
    return (g['enc'] == 'cv8' and bool(g.get('tag2')) and bool(g['bytehdr'])   # Iteration 385: the tag as the build
            and not g.get('tail') and not g.get('msc'))                         # has it - tag2 without byte headers is no tag
def opcall_avail(g):
    o10 = {w for w, _ in ops10_in(g)}
    return [n for n in OPCALL_POOL if (n not in ('0=', '1+') or 'tiny' in g['spec']) and (n not in ('(PARSE)', 'PLACE') or n in o10)]
def opcall_in(g):
    """[[name, logical opcode, handler], ...]: codes of their own under the tag,
    0xFE00 + k, no slot in the 128-entry table (as the JIT's) - the designs that
    could use them most had no slot left after format-10 words and pairs."""
    if not opcall_on(g): return []
    av = set(opcall_avail(g)); names = [n for n in dict.fromkeys(g.get('opcall') or []) if n in av]
    return [[n, 0xFE00 + k, OPCALL_POOL[n]] for k, n in enumerate(names)]
WORK_SEL = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps']; WORK_HELD = ['sieve', 'parse']   # 495 (the owner): apps
WORK_FAR = ['far']   # Iteration 159: the timed fib behind a 1 MB gap - three-byte calls; compare-fronts only
# Iteration 41: loop selected (the owner), sieve held out. Iteration 127 (the owner): parse held out - it
# timed the interpreter twice over, with the corpus - and two execution-heavy workloads in, the owner's
# RelF/bench programs (his collection; Iteration 128): bubble and ackermann (deep recursion).


def canon(g):
    g = dict(g); g['spec'] = [s for s in SPECS if s in g['spec']]; g['folds'] = list(g['folds'])
    g['supers'] = [list(x) for x in g.get('supers', [])]
    g['ops10'] = list(g.get('ops10', []))
    for k in LATE: g.setdefault(k, 0)          # genomes recorded before them: off
    g['opcall'] = list(g['opcall'] or [])      # Iteration 121: a list gene, [] when off
    if g['bytehdr']: g['scale'] = 0   # byte headers never convert with scaled targets: lethal, so not tried
    return g
def express(g):
    """The genes that make the design - its identity. Two genomes that differ
    only in dormant genes build the same design, and are measured once."""
    g = canon(g); e = {k: g[k] for k in ['enc'] + list(CC0) + EXPRESSED[g['enc']]}
    if g['enc'] == 'cpt16' and not g['fold']: e.pop('folds')
    if 'supers' in e: e['supers'] = [x[:2] for x in supers_in(g)]   # only the pairs that got a slot
    if 'ops10' in e: e['ops10'] = [x[0] for x in ops10_in(g)]
    if 'opcall' in e:                           # Iteration 121: only those with a slot; none, out of the identity
        e['opcall'] = [x[0] for x in opcall_in(g)]
        if not e['opcall']: e.pop('opcall')
    if e.get('rtimm') == 2 and g.get('rtfuse') and (supers_in(g) or rt_tests(g)): e['rtimm'] = 1   # Iteration 175: the same build - one id
    if e.get('rtloop') == 2 and rtloopall_on(g): e['rtloop'] = 1                   # Iteration 190: loopall's own words - the same build
    if 'sysc' in e and g['enc'] != 'cv8': e.pop('sysc')                            # Iteration 136: SYSC is vm-lab.c's, build()'s
    if e.get('compiler'):                                                           # Iteration 262: clang - GCC's own genes do nothing
        for k in GCC_ONLY: e.pop(k, None)
    elif 'compiler' in e: e.pop('compiler')
    if e.get('varcall'): e.pop('sharedcall', None)                     # forced on: see build()
    elif 'varcall' in e: e.pop('doesfar', None)                        # forced off: see build()
    if 'msc' in e and not g['tos']: e.pop('msc')                       # made from the cached engine only
    if e.get('msc'):                                                   # its own tables; tail calls excluded
        e.pop('d256', None); e.pop('sharedcall', None); e.pop('tail', None)
    if 'tail' in e and not g['tos']: e.pop('tail')                     # made from the cached engine only
    if e.get('tail'):                                                  # one call function, 256-entry table
        e.pop('d256', None); e.pop('sharedcall', None)
    for k, needs in GENE_RULES:                                        # Iteration 276: the table's rows (gene())
        if k in e and not needs(g, e): e.pop(k)
    for k in LATE:
        if not e.get(k): e.pop(k, None)                                # see LATE
    return e
def gid(g):
    return hashlib.sha1(json.dumps(express(g), sort_keys=True).encode()).hexdigest()[:10]


# ---- building and testing one design ------------------------------------
BUILD_TOOLS = ('cc', 'gcc', 'clang', 'make', 'sh', 'bash', 'git', 'objcopy', 'objdump', 'size', 'strip', 'ld', 'as', 'cpp', 'nm')
def _kind(cmd):
    """'engine', 'cputime' (about to run one) or None (a build tool, which
    forks: the compiler, the converter). Anything not known to be a tool
    counts as an engine - a new tool fails loudly rather than escaping."""
    i = 3 if cmd and os.path.basename(str(cmd[0])) == 'taskset' else 0    # taskset -c N
    if len(cmd) > i + 3 and os.path.basename(str(cmd[i])) == 'setarch': i += 3   # setarch ARCH -R (Iteration 24)
    exe = os.path.basename(str(cmd[i])) if len(cmd) > i else ''
    if exe == os.path.basename(CPUT): return 'cputime'
    # clang-19 and the like - the gene tailpn's compiler (Iteration 293) - a build tool too: jailed as an
    # engine, no new process, its driver could not start the linker
    # Iteration 325: and EVOLVE_CC's compiler (arm-linux-gnueabihf-gcc for the Tegra) - jailed, its driver could not start cc1
    return None if exe in BUILD_TOOLS or exe.startswith(('python', 'clang-')) or exe == os.path.basename(cc()[0]) else 'engine'
def _contain(cpu, kind=None):
    """In the child: a CPU-time limit - SIGXCPU at cpu seconds - and for an
    engine, the jail: no new processes (RLIMIT_NPROC 0), at most 1 GB of
    address space, 64 MB files, 64 open files, no core dumps. Iteration 10:
    a broken design forked without bound and froze the owner's laptop -
    the CPU limit and the group kill came too late, since a fork bomb fills
    the machine in milliseconds. No workload forks. Under cputime, which
    must fork once, cputime jails its child (CPUTIME_JAIL)."""
    import resource
    def f():
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 2))
        if kind:
            for r, v in ((resource.RLIMIT_CORE, 0), (resource.RLIMIT_AS, 1 << 30),
                         (resource.RLIMIT_FSIZE, 64 << 20), (resource.RLIMIT_NOFILE, 64)):
                resource.setrlimit(r, (v, v))
        if kind == 'engine':
            resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
    return f
def sh(cmd, cwd=None, inp=None, timeout=300, env=None, cpu=60):
    """Run cmd in a process group of its own and kill the WHOLE group on
    timeout. A broken design executes arbitrary code, and the engine's
    primitives include fork and execve: a wild jump can leave processes
    behind that hold the pipes open - one such run hung the lab and once
    took the machine down with it.

    A run's limit is in CPU time (cpu): a design that loops burns CPU and
    is stopped however busy the machine is, while a correct design merely
    waiting its turn on a loaded laptop is not. timeout, wall-clock, is
    only the backstop for one that blocks. SIGXCPU counts as a timeout."""
    kind = _kind(cmd)
    if kind == 'cputime': env = dict(env if env is not None else os.environ, CPUTIME_JAIL='1')
    p = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.PIPE if inp is not None else subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, preexec_fn=_contain(cpu, kind), env=env)
    try:
        out, err = p.communicate(inp, timeout=timeout)
    except subprocess.TimeoutExpired:
        import signal
        try: os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError: pass
        p.communicate()
        raise
    finally:
        try: os.killpg(p.pid, 9)        # anything the run left behind
        except (ProcessLookupError, PermissionError): pass
    import signal
    if p.returncode == -signal.SIGXCPU: raise subprocess.TimeoutExpired(cmd, cpu)
    return subprocess.CompletedProcess(cmd, p.returncode, out, err)

def cellw():
    """Iteration 326 (the owner: 8-byte cells on a 64-bit host, 4 on a 32-bit one): the cell width
    of what this run builds - the host's own (8 on the laptop and dream, 4 on the Tegra), or
    EVOLVE_CELL (4: 32-bit x86 built here, with EVOLVE_CC='gcc -m32'). Everything width-dependent
    follows it: the kernel dumps (k64-/k32-), the engine and kernel image that make them, the
    converter's width, the references."""
    import struct
    v = os.environ.get('EVOLVE_CELL')
    return int(v) if v in ('4', '8') else (4 if struct.calcsize('P') == 4 else 8)
def KW(): return 'k%d' % (8 * cellw())                      # the dumps' prefix: k64 or k32
def S0(): return os.path.join(O, 's0-cell-%d' % (8 * cellw()))   # the cell engine that makes them
def KIMG(): return 'kernel.img' if cellw() == 8 else 'kernel32.img'

W4_ENV = {'EVOLVE_CELL': '4', 'EVOLVE_CC': 'gcc -m32 -fno-pie -no-pie'}   # Iteration 363: as relf builds its 32-bit engine - no PIC base register
KERNEL_IN64 = None

class at_width:
    """Iteration 336: evaluate at 4-byte cells - the build's environment and setup's four width-
    dependent globals swapped in (build, alive and measure read them at call time), then put back."""
    def __init__(self, ctx): self.ctx = ctx
    def __enter__(self):
        g = globals(); self.saved = {k: g[k] for k in ('REF', 'KREF', 'REF_CORPUS', 'KERNEL_IN')}
        self.env = {k: os.environ.get(k) for k in W4_ENV}
        os.environ.update(W4_ENV); g.update(self.ctx)
    def __exit__(self, *_):
        globals().update(self.saved)
        for k, v in self.env.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v

def setup_widths():
    """Iteration 336: setup at 4-byte cells first (its own reference, kernel reference and k32
    variants), kept in WIDTH4; then setup as always - the run's own width, 8."""
    global KERNEL_IN64
    if TWO_WIDTHS[0]:
        KERNEL_IN64 = KERNEL_IN
        env = {k: os.environ.get(k) for k in W4_ENV}; os.environ.update(W4_ENV)
        try:
            setup(); WIDTH4.update(REF=REF, KREF=KREF, REF_CORPUS=REF_CORPUS, KERNEL_IN=KERNEL_IN)
        finally:
            for k, v in env.items():
                if v is None: os.environ.pop(k, None)
                else: os.environ[k] = v
            globals()['KERNEL_IN'] = KERNEL_IN64
    setup()

def eval32(g, rounds):
    """Iteration 336: speed32 - the design as a 32-bit x86 engine at 4-byte cells, over the selection's
    workloads, a round fewer; none (and why) if it does not build or live so. Iteration 461: with its
    JIT, which builds at 32 bits now (results/drafts/jit-i386-460.md) - jitk aside, x86-64's registers."""
    # Iteration 337: and its call scale at most 2 - at 4-byte cells nothing is 8-aligned, scale 3's
    # unit: run-time definitions align to the cell, and a scaled call missed them (the corpus died).
    # A 32-bit build of the design takes cell-aligned calls. (Until Iteration 461 it took no JIT either.)
    g32 = dict(g)
    if (g32.get('scale') or 0) > 2: g32['scale'] = 2
    g32 = canon(g32); d32 = os.path.join(EV, 'ind32-' + gid(g)); out = {}
    try:
        with at_width(WIDTH4):
            eng, img = build(g32, d32); pw = private_work(d32)
            alive(eng, img, pw, far=not hand_made(g32))
            t, raw = measure(eng, img, pw, WORK_SEL, max(1, rounds - 1))
        out['speed32'] = math.exp(sum(math.log(t[w]) for w in WORK_SEL) / len(WORK_SEL)); out['t32'] = t
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        out['speed32'] = None; out['why32'] = str(e)[:200]
    shutil.rmtree(d32, ignore_errors=True)
    return out

def w32():
    """Iteration 461: building for 32-bit x86 here (EVOLVE_CC with -m32)."""
    return '-m32' in os.environ.get('EVOLVE_CC', '').split()

def CCV(g):
    """Iteration 324: the design's compiler as a command - EVOLVE_CC in place of GCC's (clang
    designs keep clang: the Tegra has none, and its sample is GCC's)."""
    c = CC(g)
    if os.environ.get('EVOLVE_CC') and c in ('cc', 'gcc'): return os.environ['EVOLVE_CC'].split()
    return [c] + (['-m32', '-fno-pie', '-no-pie'] if '-m32' in os.environ.get('EVOLVE_CC', '').split() else [])   # Iteration 336: clang at 32 bits too; 363: not PIE, as relf's

def cc():
    """Iteration 324: the C compiler - EVOLVE_CC to build for another host (gcc -m32: a 32-bit
    host tested here; arm-linux-gnueabihf-gcc: the Tegra's). Unset, cc - as always."""
    return os.environ.get('EVOLVE_CC', 'cc').split()

RTC = os.path.join(ROOT, 'engine', 'rt-linux-x86_64.c')
def rt():
    """Iteration 75 (the owner): every engine WITHOUT the C library - its
    system calls from engine/rt-linux-x86_64.c, linked statically - so the
    binary is all there is: its size and its memory are the design's own,
    and logic moved into the engine shows. Without unwind tables, which
    nothing reads. Not for profiling builds, off x86-64 Linux, or with
    EVOLVE_LIBC=1: there, the C library as before."""
    fl = ['-fno-asynchronous-unwind-tables']
    u = os.uname()
    if PROFILING[0] or os.environ.get('EVOLVE_LIBC') == '1' or (u.sysname, u.machine) != ('Linux', 'x86_64'): return fl
    # Iteration 331: building 32-bit x86 here (EVOLVE_CC with -m32) - the i386 runtime, static
    # as the x86-64 one: a 32-bit check's binaries run where no 32-bit C library is (dream.lan)
    rtc = os.path.join(ROOT, 'engine', 'rt-linux-i386.c') if '-m32' in os.environ.get('EVOLVE_CC', '').split() else RTC
    # Iteration 82: and without page alignment (-n), RELRO or a build-id - a
    # static engine has no dynamic relocations, and their padding made the
    # binary move in 4 KB steps (s6: 29,456 bytes, 22,200 without)
    return fl + ['-static', '-no-pie', '-nostdlib', '-fno-stack-protector', '-U_FORTIFY_SOURCE', '-D_FORTIFY_SOURCE=0',
                 '-Wl,-N', '-Wl,-z,norelro', '-Wl,--build-id=none', '-DRTLIB=1', rtc, '-lgcc',
                 '-ffunction-sections', '-fdata-sections', '-Wl,--gc-sections']
    # --gc-sections (Iteration 113): the runtime is one object file, so code
    # nothing calls came along - vsnprintf, snprintf, execvp, syscall,
    # getrusage, memmove: 1.9-2.7 KB of every engine, dead. Dropped.
    # -N, not -n (Iteration 110): -n kept the default script's page alignment
    # of the data sections - .data.rel.ro started on a page boundary, so an
    # engine's file grew in 4 KB steps whenever its code's end crossed one,
    # luck for any design and any change (a 430-byte saving showed as -4,296
    # bytes and as -72). -N lays them end to end: the file is its sections
    # and ~800 bytes of headers. The segment was readable, writable and
    # executable under -n already.

def bin_size(eng):
    """Iteration 75: the engine as it would ship. Since Iteration 149 build()
    returns it so - tools/elf_tight.py: no section headers, symbols or
    .comment, 620 bytes a design - and keeps the full file beside it as
    engine.full, for tail_offenders and anyone with nm or gdb."""
    return os.path.getsize(eng)

GOTODUPV = (None, 32, 128)        # Iteration 260: GCC's max-goto-duplication-insns - None its default, 8
def CC(g):
    """Iteration 262: the compiler the gene names - GCC as cc, or clang."""
    return 'clang' if express(g).get('compiler') else 'cc'
ARM32 = os.uname().machine.startswith('arm')   # Iteration 407: a 32-bit ARM host - the Tegra (armv7l)
def ccflags(g):
    if express(g).get('compiler'):          # Iteration 262: clang - its -Oz for -Os, and only the flags it knows
        return ['-Oz' if g['opt'] == 'Os' else '-' + g['opt']] + [w for k, f in CFLAGS.items() if g.get(k) and k not in GCC_ONLY for w in f.split()] + _EXTRA_CFLAGS
    f = ['-' + g['opt']] + [w for k, f in CFLAGS.items() if g.get(k) for w in f.split()]   # a flag gene a genome lacks is off
    if g.get('gotodup'): f += ['--param', 'max-goto-duplication-insns=%d' % GOTODUPV[g['gotodup']]]   # Iteration 260
    # Iteration 407 (open item 0d): not on 32-bit ARM - there GCC places the engine's literal pools without the padding
    # these alignments add, and a load lands past its 4 KB reach: the assembler's 'bad immediate value for offset', all
    # 14 of seeds 58-60's Tegra failures alignhot 32 or 64, all 28 that built 0 or 1. Left out of that build, as the JIT
    # of a 32-bit one; the laptop's and dream's builds as before.
    if g.get('alignhot') and not ARM32: f += ['-falign-jumps=%s' % ALIGNV[g['alignhot']], '-falign-labels=%s' % ALIGNV[g['alignhot']],
                                '-falign-functions=%s' % ALIGNV[g['alignhot']]]   # Iteration 298: a handler's entry - a computed goto's
                                # target, or a tail engine's function - on a fetch window's start
    return f + _EXTRA_CFLAGS
_EXTRA_CFLAGS = os.environ.get('EVOLVE_CFLAGS', '').split()   # Iteration 294: a measurement's -g (missmap.py) - never the evolution's

# Iteration 456 (the owner; results/gene-votes.md): tail-call threading removed - tail_offenders(), build_tail() and
# tools/gen-tail.py. tail and tailpn stay in the genome, frozen off (FROZEN, Iteration 450), so every design keeps its
# identity; seed 66 showed no loss with them off.

PROFILING = [False]      # set while design_pairs builds a profiling engine
CONVERT_EXTRA = []       # more converter options, set by a pricing tool (callsites.py); empty in a run
PAIRS_CACHE = {}
PAIRS_BAD = {'NOOP', 'EXIT', 'LIT', 'BRANCH', '?BRANCH', 'EXECUTE', 'BYE', 'SP@', 'SP!', 'RP@', 'RP!', 'WRITE', 'READ'}
def design_pairs(g, n=24):
    """This design's own hottest primitive pairs: build it with the
    engine's profiler (VMPROF) and run the selection workloads - the
    pool a mutation adding a pair draws from. The fixed SUPER_POOL came
    from one profile of s6; a design that already fuses some pairs, or
    has folds, specialisations or format-10 words, leaves others hot.
    Cached per design; SUPER_POOL if profiling fails or g is no CV8."""
    if g['enc'] != 'cv8': return list(SUPER_POOL)
    key = gid(g)
    cache = os.path.join(EV, 'pairs.json')         # kept on disk: a resumed run replays its mutations
    if not PAIRS_CACHE and os.path.exists(cache):
        try: PAIRS_CACHE.update(json.load(open(cache)))
        except ValueError: pass
    if key in PAIRS_CACHE: return PAIRS_CACHE[key]
    pool = list(SUPER_POOL)
    prims = [l.split()[1] for l in open(os.path.join(ROOT, 'forth', 'kernel.4')) if l.startswith('PRIMITIVE')]
    def prim(op):                       # this design's one-byte primitive opcodes
        if g.get('escape') == 2: i = op if op < 27 else None
        elif g.get('escape'): i = op if op < 32 else op + 1 if op < 36 else None
        else: i = op if op < 68 else None
        return prims[i] if i is not None and i < 33 and prims[i] not in PAIRS_BAD else None
    d = os.path.join(EV, 'profile'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    PROFILING[0] = True
    try:
        eng, img = build(dict(g, tail=0, msc=0), d)     # the stream, not the dispatch, decides the pairs
        # Iteration 366: a tag-2 design profiles its own one-byte codes, which t2hot orders hot first -
        # named through its table (vm-tag2-one.h), not as plain opcodes: until now every tag-2 design's
        # pool was its codes misread (OR DROP for DUP and a specialisation), and wide codes 128-191 lost.
        hp = os.path.join(d, 'vm-tag2-one.h')
        one = [int(x) for x in re.findall(r'-?\d+', open(hp).read())] if g.get('tag2') and os.path.exists(hp) else None
        def op_of(code):
            if one is None: return code if code < 128 else None
            i = code if code < 64 else code - 64 if 128 <= code < 192 else None
            return one[i] if i is not None and i < len(one) else None
        pw = private_work(d); share = collections.Counter()
        for w in WORK_SEL:
            pf = os.path.join(d, 'prof-' + w)
            sh([eng, img], cwd=pw, inp=program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
            c, total = collections.Counter(), 0
            for line in open(pf):
                m = re.match(r'^(\d+) (\d+) (\d+)$', line)
                if m:
                    a, b, k = map(int, m.groups()); total += k
                    oa, ob = op_of(a), op_of(b)
                    if oa is not None and ob is not None and prim(oa) and prim(ob): c[(prim(oa), prim(ob))] += k
            for pr, k in c.items(): share[pr] += k / max(total, 1)
        if share: pool = [list(pr) for pr, _ in share.most_common(n)]
    except Exception:
        pass
    finally:
        PROFILING[0] = False
        shutil.rmtree(d, ignore_errors=True)
    PAIRS_CACHE[key] = pool
    tmp = cache + '.tmp'
    json.dump(PAIRS_CACHE, open(tmp, 'w')); os.replace(tmp, cache)
    return pool

WHY_GENERIC = ('collect2: error: ld returned', 'lto-wrapper: fatal error', 'compilation terminated')
def why(r):
    """A failed tool's own words, for the record. Iteration 385 (open item 0d b): the first error, not
    the last - a link failure's last line is always ld's generic 'returned 1 exit status', which hid
    the Tegra's three; where only the generic lines say error, the line before them, the linker's own;
    paths cut to their file names, so the words fit. A Python traceback keeps its exception line."""
    lines = [l for l in (r.stderr or b'').decode(errors='replace').splitlines() + (r.stdout or b'').decode(errors='replace').splitlines() if l.strip()]
    err = [l for l in lines if ('rror' in l or 'ssert' in l) and not any(x in l for x in WHY_GENERIC)]
    exc = [l for l in lines if re.match(r'[A-Za-z_][\w.]*(Error|Exception)\b', l)]
    if exc and any(l.startswith('Traceback') for l in lines): err = [exc[-1]]   # Python: its exception, last
    if not err:
        gen = [i for i, l in enumerate(lines) if any(x in l for x in WHY_GENERIC)]
        err = [lines[gen[0] - 1]] if gen and gen[0] > 0 else lines
    if not err: return ' (exit %d)' % r.returncode
    return ' (%s)' % re.sub(r'(?:/[^\s:/()]+)+/([^\s:/()]+)', r'\1', err[0].strip())[:160]

T2RANK = os.path.join(ROOT, 'lab', 'evolve', 'tag2-rank-v1.json')   # the reference ranking (Iteration 66)
# Iteration 71: t2hot - the tag's one-byte codes, hot first above this weight,
# the rest by static use (layout.py --tag2-hot): 0 the middle way (the
# default), then speed first, then size first by degrees
T2HOT = [0.02, 0.0, 0.05, 100.0]
# Iteration 71: --require tag2 - every design of the run, the hand-made
# references excepted, in the two-bit tag (with byte headers)
REQUIRE = []
# Iteration 409 (the owner: the simplicity review, results/drafts/simplicity-proposal-408.md): genes the search no longer
# varies. On in every front design of seeds 53-60 (1,431 - bss and lean in all but one and two), so frozen on: bytehdr,
# doesfar, thinhdr, varcall, bss, lean; on in none, with no fault behind it, so removed: msc and scale, held at 0. Every
# design the search makes carries these values (require, at get()); a hand-made design keeps its own, so s6 and the
# stages are unchanged. With varcall and doesfar on, no design dies at the reach limit any more (reach_lethal). Not
# tail - a fault hid it until the after-seed-62 batch; judged after seed 63.
# Iteration 450 (the owner; results/seed63-rules.md's gene votes): sharedcall, tail, kstack and tailpn frozen off - 12 of
# 12 removal votes over seeds 63-65, on no front design, so the dependence test had nothing to rebuild. Reversible: the
# code stays; removed only if the run after shows no loss (its comparison small or better).
FROZEN = {'bytehdr': 1, 'doesfar': 1, 'thinhdr': 1, 'varcall': 1, 'bss': 1, 'lean': 1, 'msc': 0, 'scale': 0,
          'sharedcall': 0, 'tail': 0, 'kstack': 0, 'tailpn': 0,
          'alignhot': 0, 'jitos': 0}   # 475: jitdoes enabled (the owner); 477: jitexec; 483: jitcfa; 495 (the owner): jitrp enabled, jitos frozen; 504: jithelp and jitre retired; 508 (the owner): jitfuse enabled; 501: nocase retired (the owner)
def require(g):
    if g.get('enc') == 'cv8': g = dict(g, **FROZEN)                   # Iteration 409
    if 'tag2' in REQUIRE and g.get('enc') == 'cv8': g = dict(g, tag2=1, bytehdr=1)
    return g

def _build(g, d):
    """-> (engine, image) or raises RuntimeError('died: ...')"""
    if os.path.exists(d): shutil.rmtree(d)
    os.makedirs(d)
    if g['enc'] != 'cv8': return build_other(g, d)
    src = os.path.join(d, 'vm.c')
    shutil.copy(os.path.join(O, 'vm-lab-tos.c' if g['tos'] else 'vm-lab.c'), src)
    folds = ','.join(g['folds'])
    r = sh(['python3', os.path.join(ROOT, 'tools', 'gen-fold.py'), src, folds, 'v8'])
    if r.returncode: raise RuntimeError('died: fold generation')
    flags = ['-DENC=3', '-DREG=1', '-DFOLD=1', '-DSCALE=%d' % g['scale'],
             '-DVARCALL=%d' % g['varcall'], '-DVARSLOT=%d' % g['varslot']]
    # Variable-length calls are decoded only on the shared call path
    # (engine/vm-lab.c, do_call), so with varcall the engine always has it.
    # And DODOES reads the three-byte (far) form only under VARCALL, so far
    # DOES> calls need variable-length calls.
    eff = dict(g, sharedcall=g['sharedcall'] or g['varcall'], doesfar=g['doesfar'] and g['varcall'])
    for k, f in (('sharedcall', '-DSHAREDCALL=1'), ('doesfar', '-DDOESFAR=1'),
                 ('d256', '-DDISPATCH256=1'), ('guard', '-DGUARD=1'), ('dskew', '-DDSKEW=2048')):
        if eff.get(k): flags.append(f)          # .get: a hand-made genome need not carry a late gene (dskew)
    if fsys_on(g): flags.append('-DFSYS=%d' % fsys_level(g))   # Iteration 202: seven handlers out (1); twelve, rebound (2: Iteration 205)
    if g.get('regpin'): flags.append('-DREGPIN=%d' % g['regpin'])   # Iteration 197: the VM registers pinned
    if g['spec']: flags.append('-DSPEC=1')
    t2 = bool(g.get('tag2')) and bool(g['bytehdr'])   # Iteration 66: the two-bit tag (FORMAT-TAG2.md); byte headers
    if g.get('hotcalls') and g['varcall'] and not t2: flags.append('-DHOTCALLS=1')   # one-byte calls: see express()
    if t2: flags.append('-DTAG2=1')
    if t2wide_on(g): flags.append('-DT2WIDE=1')         # Iteration 95: no 3-byte call, 127 one-byte codes
    if jit_on(g): flags.append('-DX_JIT=1')
    if jit_on(g) and express(g).get('jitrp'):        # Iteration 494, the gene jitrp: the return-stack pointer in a register
        flags += ['-DJITRP=1', '-DJITRP_REG="%s"' % {2: 'rbx', 3: 'r13'}.get(g.get('regpin') or 0, 'r15')]   # clear of regpin's
    if jit_on(g) and express(g).get('jitvar'): flags.append('-DJITVAR=1')   # Iteration 342: the slot operand's decoding
    if jit_on(g) and os.environ.get('EVOLVE_JITLOG'): flags.append('-DJITLOG=1')   # Iteration 340: jitleft.py --why's build only
    if express(g).get('bfind'): flags.append('-DBFIND=1')   # Iteration 316: THREAD-FIND's and (FIND)'s walk branch-light
    if jit_on(g) and g.get('jitx'): flags.append('-DJITX=1')   # Iteration 108: the translator reaches further
    if jit_on(g) and express(g).get('jitloop'): flags.append('-DJITLOOP=1')   # Iteration 129: the scan reads further (expressed: dormant, nothing)
    # sysc's -DSYSC=1: every engine source is SYSC by default since Iteration 147   # Iteration 136: one SYSCALL for the shell's seventeen (forth/shell-sysc.4)
    if jit_on(g) and express(g).get('jitinl'): flags.append('-DJITINL=1')   # Iteration 137: one-operation words inline; D+'s stencil
    if jit_on(g) and express(g).get('jitmul'): flags.append('-DJITMUL=1')   # Iteration 472: UM* and UM/MOD's stencils
    if jit_on(g) and express(g).get('jitdoes'): flags.append('-DJITDOES=1') # Iteration 473: DOES> children native
    if jit_on(g) and express(g).get('jitexec'): flags.append('-DJITEXEC=1') # Iteration 476: EXECUTE's helper
    if jit_on(g) and express(g).get('jitcfa'): flags.append('-DJITCFA=1')   # Iteration 482: the check along the paths
    if jit_on(g) and express(g).get('jitfuse'): flags.append('-DJITFUSE=1') # Iteration 507: pairs as one stencil
    if jit_on(g) and express(g).get('jitos'): flags.append('-DJITOS=1')     # Iteration 239: the translator -Os
    if jit_on(g) and express(g).get('jittail'): flags.append('-DJITTAIL=1')  # Iteration 246: tail calls as jumps
    if jit_on(g) and express(g).get('jitret'): flags.append('-DJITRET=1')    # Iteration 404: EXIT as pop and jmp
    if jit_on(g) and express(g).get('jitk') and not w32(): flags.append('-DJITK=%d' % express(g)['jitk'])   # Iteration 259: gen-jitk.py's stencils; 461: not at 32 bits
    if g.get('fbuf'): flags.append('-DFBUFSZ=%d' % FBUFV[g['fbuf']])   # Iteration 115: memory, against reads
    if PROFILING[0]: flags.append('-DPROFILE=%d' % (2 if PROFILING[0] == 2 else 1))   # 2: the tracer (Iteration 162)
    if PROFILING[0] and os.environ.get('JIT_PRICE') == '1': flags.append('-DJIT_PRICE=1')   # Iteration 218: lab/evolve/jitstack.py
    if g.get('escape'): flags.append('-DESCAPE=%d' % g['escape'])
    o10 = ops10_in(g)
    if o10:
        json.dump(o10, open(os.path.join(d, 'ops10.json'), 'w'))
        open(os.path.join(os.path.dirname(src), 'vm-ops10-table.h'), 'w').write(
            ''.join('[%d] = DSP(%s),\n' % (op, OPS10_LABEL[w]) for w, op in o10 if not 27 <= op < 68))
        open(os.path.join(os.path.dirname(src), 'vm-ops10-esc.h'), 'w').write(     # the band ESCAPE frees
            ''.join('cv8_tab[%d] = &&%s;\n' % (op, OPS10_LABEL[w]) for w, op in o10 if 27 <= op < 68))
        flags.append('-DOPS10=1')
        flags += sorted({'-D%s=1' % X_MACRO[w] for w, _ in o10 if w in X_MACRO})
    sup = supers_in(g)
    if sup:
        json.dump(sup, open(os.path.join(d, 'supers.json'), 'w'))
        if sh(['python3', os.path.join(ROOT, 'tools', 'gen-super.py'), src, os.path.join(d, 'supers.json')]).returncode:
            raise RuntimeError('died: superinstruction generation')
        flags.append('-DSUPER=1')
    oc = opcall_in(g)
    if oc:                                    # Iteration 121: the op;CALL handlers
        json.dump(oc, open(os.path.join(d, 'opcall.json'), 'w'))
        r = sh(['python3', os.path.join(ROOT, 'tools', 'gen-opcall.py'), src, os.path.join(d, 'opcall.json')])
        if r.returncode: raise RuntimeError('died: op;CALL generation' + why(r))
        flags.append('-DOPCALL=1')
    if g.get('msc') and g['tos']:           # multi-state stack caching (tools/gen-msc.py); the tag too (Iteration 70)
        r = sh(['python3', os.path.join(ROOT, 'tools', 'gen-msc.py'), src])
        if r.returncode: raise RuntimeError('died: multi-state generation' + why(r))
        flags = [f for f in flags if not f.startswith(('-DDISPATCH256', '-DSHAREDCALL'))] + ['-DDISPATCH256=1', '-DSHAREDCALL=1']
    eng = os.path.join(d, 'engine')
    def compile_engine():
        jit = ['-I', os.path.dirname(src), '-I', os.path.join(ROOT, 'engine'), os.path.join(ROOT, 'engine', 'spn-stencils.c'),
               os.path.join(ROOT, 'engine', 'spn-markers.c')] if jit_on(g) else []   # Iteration 80: the stencils
        if jit_on(g) and express(g).get('jitk') and not w32():   # Iteration 259: the stack cache's stencils, beside vm.c (461: x86-64's registers)
            if sh(['python3', os.path.join(ROOT, 'tools', 'gen-jitk.py'), str(express(g)['jitk']), os.path.dirname(src)]).returncode:
                raise RuntimeError('died: stack-cache generation')
        lto = ['-flto'] if express(g).get('lto') else []    # Iteration 260: the engine and its runtime as one
        if lto and jit:                                      # the stencils outside it: the JIT reads their code as compiled
            objs = []
            for c in ('spn-stencils.c', 'spn-markers.c'):
                o = os.path.join(d, c[:-2] + '.o'); objs.append(o)
                r = sh(CCV(g) + ccflags(g) + flags + [x for x in rt() if x.startswith(('-f', '-D', '-U'))] + jit[:4] + ['-c', '-o', o, os.path.join(ROOT, 'engine', c)])
                if r.returncode: raise RuntimeError('died: engine did not compile' + why(r))
            jit = jit[:4] + objs
        r = sh(CCV(g) + ccflags(g) + flags + lto + ['-o', eng, src] + jit + rt())
        if r.returncode: raise RuntimeError('died: engine did not compile' + why(r))
    if not t2: compile_engine()      # under the tag, after the converter: its ranking is the engine's map
    opts = ['--v8', '--cpt', str(g['scale']), '--dataprims', '--fold', '--fold-set', folds, '--cv8-compiler']
    if g['bytehdr']: opts.append('--bytehdr')
    if g.get('escape'): opts.append('--escape')
    if g.get('escape') == 2: opts.append('--escape2')
    opts.append('--set-compiler-vars')       # the image's compiler follows THIS design's scale and DOES> form
    if g['doesfar'] and g['varcall']: opts.append('--does-far')   # see build(): far DOES> needs VARCALL
    if g['spec']: opts += ['--spec', ','.join(canon(g)['spec'])]
    if not g['varcall']: opts.append('--no-varcall')
    if not g['varslot']: opts.append('--no-varslot')
    if sup: opts += ['--supers-file', os.path.join(d, 'supers.json')]
    if oc: opts += ['--opcall-file', os.path.join(d, 'opcall.json')]
    if o10: opts += ['--ops10-file', os.path.join(d, 'ops10.json')]
    if (g['rtfuse'] and (sup or rt_tests(g))) or rtimm2(g) or rtiplus_on(g): opts.append('--rtfuse')   # 447: I+'s entry   # rtimm=2: IMM-OPS filled
    if g.get('hotcalls') and g['varcall'] and not t2: opts += ['--hotcalls', str(g['hotcalls'])]
    if t2: opts += ['--tag2'] + (['--tag2-rank', T2RANK] if os.path.exists(T2RANK) else []) + ['--tag2-hot', str(T2HOT[g.get('t2hot', 0)])]
    if t2wide_on(g): opts.append('--tag2-wide')
    if g.get('hotinl') and t2: opts += ['--hot-inline', HOTSITES, str(g['hotinl'])]   # Iteration 92: the hottest call sites inlined
    for k, conv in GENE_CONVERT: opts += conv(g)                  # Iteration 276-278: the rows' own options (gene())
    if jit_on(g): opts.append('--jit')                             # Iteration 80: vm-jit-ops.h beside the image
    if jit_on(g) and g.get('jitx'): opts.append('--jitx')         # Iteration 108: >R, R>, R@ given stencils
    if jit_on(g) and express(g).get('jitloop'): opts.append('--jitloop')   # Iteration 129: (+LOOP) and (?DO) given stencils
    if jit_on(g) and express(g).get('jitinl'): opts.append('--jitinl')     # Iteration 137: D+'s stencil
    if jit_on(g) and express(g).get('jitmul'): opts.append('--jitmul')     # Iteration 472: UM*, UM/MOD, COUNT
    if jit_on(g) and express(g).get('jitexec'): opts.append('--jitexec')   # Iteration 476: EXECUTE's row
    if jit_on(g) and express(g).get('jitimg'): opts += ['--jitimg', str(express(g)['jitimg'])]   # Iteration 341: the image's words JIT candidates
    if jit_on(g) and express(g).get('jitvar'): opts.append('--jitvar')   # Iteration 342: vf and vs given the JIT
    hl = []                                                     # words kept, their headers dropped (tools/layout.py --headerless)
    if rtloop_on(g) and not rtloopall_on(g) and express(g).get('rtloop') == 2: hl += RTLOOP_INTERNAL   # Iteration 190: cv8-fuse-loop.4's internal words
    if rtimm_lean(g): hl += RTIMM_LEAN_INTERNAL                 # Iteration 422: cv8-imm.4's internal words
    if fsys_on(g): hl += FSYS_INTERNAL                          # Iteration 202: file-sysc.4's helpers
    if fsys_level(g) >= 2:                                      # Iteration 205: file-sysc2.4's, and the kernel's uses rebound
        hl += FSYS2_INTERNAL + (FSYS3_INTERNAL if fsys_level(g) >= 3 else ()) + (FSYS4_INTERNAL if fsys_level(g) >= 4 else ()) + (FSYS5_INTERNAL if fsys_level(g) == 5 else ())
        opts += ['--rebind', ','.join(FSYS2_REBIND + (FSYS3_REBIND if fsys_level(g) >= 3 else ()))]
    if hl: opts += ['--headerless', ','.join(hl)]
    if g.get('threads'): opts += ['--threads', str(THREADS_N[g['threads']])]   # Iteration 204: the dictionary's chains
    opts += CONVERT_EXTRA
    img = os.path.join(d, 'image.img')
    fuse = ('-fuse-imm' if g.get('rtimm') and 'imm' in g['spec'] else '-fuse') if overlay(g) else ''   # rtimm: Iteration 37
    if rtimm_lean(g): fuse = '-lit'                                                                   # Iteration 422: no pair lookup
    fuse += '-loopall' if rtloopall_on(g) else '-loop' if rtloop_on(g) else ''                        # rtloop: 41; rtloopall: 43
    fuse += '-iplus' if rtiplus_on(g) else ''                                                          # rtiplus: 60
    fuse += '-empty' if t2 and g.get('rtempty') else ''                                                # rtempty: 101
    dump = os.path.join(O, (KW() + ('-bt%s.txt' if t2 else '-b%s.txt' if g['bytehdr'] else '-self%s.txt')) % (('-kfast' if kfast_on(g) else '') + ('-kinput' if kinput_on(g) else '') + ('-klookup' if klookup_on(g) else '') + ('-knumber' if knumber_on(g) else '') + fuse + ('-jit' if jit_on(g) else '') + ({1: '-fsys', 2: '-fsys2', 3: '-fsys3', 4: '-fsys4', 5: '-fsys5'}.get(fsys_level(g), ''))))
    # Iteration 199: a short branch the tag-2 encoding finds out of range is
    # written to long-branches.json and the conversion fails; converted again
    # with it kept long - the set only grows, so it ends.
    lb = os.path.join(d, 'long-branches.json')
    if os.path.exists(lb): os.remove(lb)
    for _try in range(4):
        r = sh(['python3', os.path.join(ROOT, 'tools', 'layout.py'), dump, str(cellw())] + opts + ['--long-branches', lb, '--emit-image', img], cwd=W)
        if r.returncode != 4: break
    if r.returncode or not os.path.exists(img):
        raise RuntimeError('died: image did not convert' + (why(r) if r.returncode else ' (exit 0, no image written)'))
    # Iteration 13: a format-10 or tiny word whose body the converter could not
    # match was dropped with a printed line, and the design lived without it -
    # 1,032 of seed 3's 1,145 living CV8 designs (lab/evolve/scan-bodycheck.py).
    # Fixed in tools/sod16.py; a design the check fails now dies, loudly.
    m = re.search(rb'(?:ops10|tiny): no exact body match for [^\n]*', r.stdout)
    if m: raise RuntimeError('died: ' + m.group(0).decode(errors='replace'))
    if t2: compile_engine()          # the converter wrote vm-tag2-one.h and vm-tag2-esc.h beside vm.c
    return eng, img

sys.path.insert(0, os.path.join(ROOT, 'tools'))
import elf_tight                                    # Iteration 149
import farcheck                                     # Iteration 158: code far from the image base
def build(g, d):
    """-> (engine, image) or raises RuntimeError('died: ...'). The engine as
    it ships (Iteration 149): the ELF header, the program headers and the
    bytes they load - what runs is the same bytes, and the gate, the timings
    and the size are all of this file; the full one stays as engine.full."""
    eng, img = _build(g, d)
    data = open(eng, 'rb').read(); t = elf_tight.tighten(data)
    if t is not None and len(t) < len(data):
        os.replace(eng, eng + '.full'); open(eng, 'wb').write(t); os.chmod(eng, 0o755)
    return eng, img

def build_other(g, d):
    """The cell engine (relf.c, its image as built), SOD16 and CPT16."""
    eng = os.path.join(d, 'engine'); img = os.path.join(d, 'image.img')
    if g['enc'] == 'cell':
        if sh(cc() + ccflags(g) + ['-Wall', '-o', eng, os.path.join(ROOT, 'engine', 'relf.c')] + rt()).returncode:
            raise RuntimeError('died: engine did not compile')
        shutil.copy(os.path.join(O, 's0-cell-s%d.img' % (8 * cellw())), img); return eng, img   # Iteration 338: the image of its width
    src = os.path.join(d, 'vm.c'); shutil.copy(os.path.join(O, 'vm-lab.c'), src)
    if g['enc'] == 'sod16':
        flags = ['-DENC=1', '-DREG=1', '-DSCALE=1'] + (['-DSKIPPAD=1'] if g['skippad'] else [])
        dump, opts = KW() + '-s16.txt', (['--skip-pad'] if g['skippad'] else []) + ['--compiler-overlay', '16']
    else:
        sc = max(1, g['scale'])
        flags = ['-DENC=2', '-DREG=1', '-DSCALE=%d' % sc] + (['-DSKIPPAD=1'] if g['skippad'] else [])
        dump, opts = KW() + '-cpt.txt', ['--cpt', str(sc)] + (['--skip-pad'] if g['skippad'] else [])
        if g['fold']:
            folds = ','.join(g['folds'])
            if sh(['python3', os.path.join(ROOT, 'tools', 'gen-fold.py'), src, folds]).returncode:
                raise RuntimeError('died: fold generation')
            flags.append('-DFOLD=1'); opts += ['--dataprims', '--fold', '--fold-set', folds]
        opts += ['--compiler-overlay', '16']
    if sh(cc() + ccflags(g) + flags + ['-o', eng, src] + rt()).returncode:
        raise RuntimeError('died: engine did not compile')
    r = sh(['python3', os.path.join(ROOT, 'tools', 'layout.py'), os.path.join(O, dump), str(cellw())] + opts + ['--emit-image', img], cwd=W)
    if r.returncode or not os.path.exists(img):
        raise RuntimeError('died: image did not convert' + (why(r) if r.returncode else ' (exit 0, no image written)'))
    return eng, img

def private_work(d):
    """A work directory of its own: the kernel workload writes kernel.img."""
    pw = os.path.join(d, 'work'); os.makedirs(pw, exist_ok=True)
    for f in os.listdir(W):
        if f != 'kernel.img': os.symlink(os.path.join(W, f), os.path.join(pw, f))
    shutil.copy(KREF, os.path.join(pw, 'kernel.img'))
    return pw

KERNEL_IN = b'S" extend.4" INCLUDED\nS" cross.4" INCLUDED\n'
# Iteration 100 (the owner): longer workloads. The fast designs had made them
# short - on the fastest, loop 0.55 ms and the corpus 1.45 ms, a bare start
# 18% and 7% of them, and two slow rounds of three moved a median. A timed
# run now repeats its workload's work: the BENCH line K times (fib, loop, the
# sieve), or the file included K times without its BYE (parse, the corpus) -
# 8-17 ms each on the fastest design (VM), a start ~1%. Loop 10 times, not
# more: s6's loop, which every design is paired with, would cost 236 ms at 30. The kernel workload stays
# single: cross.4 included twice in one process does nothing the second time.
# Memory keeps its meaning: repeated, the corpus redefines its words, so its
# memory is one run of the single corpus (measure); the others allocate
# nothing when repeated. bench/ is untouched: the long files are made here.
LONG = {'fib': 2, 'loop': 10, 'sieve': 3, 'parse': 3, 'corpus': 5, 'bubble': 12, 'ackermann': 23}   # 128: ~11 ms each on the fastest (VM)
LONGF = {}
def long_files():
    for w, k in LONG.items():
        lines = open(CORPUS if w == 'corpus' else os.path.join(ROOT, 'bench', w + '.fth')).read().split('\n')
        if w not in ('parse', 'corpus'):          # a bench/ file with one BENCH line
            assert lines.count('BENCH') == 1, 'bench/%s.fth: one BENCH line to repeat' % w
            text = '\n'.join('\n'.join(['BENCH'] * k) if l == 'BENCH' else l for l in lines)
        else:
            while lines and lines[-1].strip() in ('', 'BYE'): lines.pop()
            text = '\n'.join(lines) + '\n'
        LONGF[w] = os.path.join(EV, 'long-%s.fth' % w); open(LONGF[w], 'w').write(text)
def program(w, single=False):
    """The workload's input: the long one (Iteration 100), or single - as before."""
    if w == 'kernel': return KERNEL_IN
    if w == 'apps': return APPS_IN       # 495: the four applications of lab/evolve/apps/, a short pass each
    if w == 'far':         # Iteration 159: fib's words past 1 MB - long calls under the tag, within s6's reach
        return ('1048576 ALLOT\n' + program('fib', single).decode()).encode()
    path = os.path.join(ROOT, 'bench', w + '.fth') if w != 'corpus' else CORPUS
    if single or w not in LONGF: return ('S" %s" INCLUDED\nBYE\n' % path).encode()
    if w == 'corpus':      # an empty line after each pass, for its ACCEPT test to read (it took the next pass's line)
        return (('S" %s" INCLUDED\n\n' % LONGF[w]) * LONG[w] + 'BYE\n').encode()
    if w == 'parse': return (('S" %s" INCLUDED\n' % LONGF[w]) * LONG[w] + 'BYE\n').encode()
    return ('S" %s" INCLUDED\nBYE\n' % LONGF[w]).encode()

# Iteration 495 (the owner: add the applications): the seventh selection workload - our own four applications (a CPU
# simulated, a collector, a scanner generator, a genetic algorithm), each one short pass checking itself, their source
# inline so the program needs no file wherever it runs; sized as the six, ~11 ms on the fastest. Appbench's programs
# stay held out (appbench.py). results/drafts/apps-selection-491.md priced it.
APPS_IN = b''.join(open(os.path.join(ROOT, 'lab', 'evolve', 'apps', f), 'rb').read() + b'\n' + call + b'\n' for f, call in (
    ('sim16.fth', b'700 ORG 15 LIT, FIB CALL, HALT,  0 STEPS !  700 RUN DPOP . STEPS @ . CR'),   # fib(15) on the simulated CPU
    ('gc16.fth', b'200 BENCH'), ('scan.fth', b'3 BENCH'), ('evo.fth', b'12 BENCH'))) + b'BYE\n'
FAR_IN = open(os.path.join(ROOT, 'tests', 'core', 'far.fth'), 'rb').read()
FULL_IN = open(os.path.join(ROOT, 'tests', 'core', 'full.fth'), 'rb').read()
HAND_MADE = []
def hand_made(g):
    """Whether g is one of the hand-made stages (Iteration 158: not gated far)."""
    if not HAND_MADE: HAND_MADE.extend(canon(v) for v in HUMAN.values())
    return canon(g) in HAND_MADE

def alive(eng, img, pw, far=True):
    """The corpus must match the cell engine's output; the kernel must match."""
    with open(CORPUS, 'rb') as f:
        r = sh([eng, img], cwd=pw, inp=f.read(), timeout=120, cpu=5)
    if r.stdout != REF_CORPUS: raise RuntimeError('died: corpus')
    # The work directory starts with a copy of the reference kernel, so
    # the workload must WRITE it: remove it first. Until this, a design
    # that died quietly before saving passed - the copy matched.
    k = os.path.join(pw, 'kernel.img')
    if os.path.exists(k): os.remove(k)
    sh([eng, img], cwd=pw, inp=KERNEL_IN, timeout=240, cpu=10)
    if not os.path.exists(k) or open(k, 'rb').read() != open(KREF, 'rb').read():
        raise RuntimeError('died: kernel workload')
    # Iteration 158 (the owner): code and data far from the image base - past
    # 64 KB, then past 8 MB more (tests/core/far.fth). Every answer right, or
    # refused out loud: a design that computes something else, crashes or
    # hangs there dies. The hand-made stages are run-tests.sh's to judge.
    if far:
        try:
            r = sh([eng, img], cwd=pw, inp=FAR_IN, timeout=60, cpu=5); out, code = r.stdout.decode(errors='replace'), r.returncode
        except Exception as e: out, code = '', 'raised: %s' % str(e)[:60]
        v = farcheck.verdict(out, code)
        if v != 'all' and not v.startswith('refused'): raise RuntimeError('died: far (%s)' % v)
        # Iteration 161: an ALLOT past the dictionary's room - refused, HERE
        # unmoved, the system going on (tests/core/full.fth).
        try: r = sh([eng, img], cwd=pw, inp=FULL_IN, timeout=60, cpu=5); out = r.stdout.decode(errors='replace')
        except Exception: out = ''
        if 'dictionary full' not in out or [l for l in out.replace('\r', '').split('\n') if re.fullmatch(r'[0-9]+ ', l)] != ['1 ', '42 ']:
            raise RuntimeError('died: dictionary full not refused')

METRIC = rb'^CYCLES (\d+)' if os.environ.get('EVOLVE_METRIC') == 'cycles' else rb'^CPUNS (\d+)'
PIN, REF = [], None            # set by setup(): the core, the reference (eng, img, work dir)
def run_metric(eng, img, pw, w, single=False):
    """One timed run: the process's own CPU time (user + system, from
    getrusage of the child - tools/cputime.c), not wall time, so other
    processes on the machine do not count against it."""
    r = sh(PIN + [CPUT, eng, img], cwd=pw, inp=program(w, single), timeout=240, cpu=30)
    m = re.search(METRIC, r.stderr, re.M) or re.search(rb'^CPUNS (\d+)', r.stderr, re.M)
    # The run's memory, KB (Iteration 75): the pages it touched - cputime's
    # MINFLT, faults counted one by one - times the page size. MAXRSS only
    # from an older cputime: on Linux 6.x it reads 0 for a small static run.
    mf = re.search(rb'^MINFLT (\d+)', r.stderr, re.M)
    mr = re.search(rb'^MAXRSS (\d+)', r.stderr, re.M)
    RSS_LAST[0] = int(mf.group(1)) * PAGE_KB if mf else (int(mr.group(1)) if mr else 0)
    OUT_LAST[0] = hashlib.sha1(re.sub(rb'(?m)^Redefining:[^\n]*\n', b'', r.stdout.replace(b'\r', b''))).hexdigest()
    # Iteration 516: what it printed - measure() compares it with s6's; a family's kernel differs in its words, so
    # 'Redefining: X' differs with it (cell designs have no LIT, or CALL, for sim16 to redefine) - not the output
    return int(m.group(1))
RSS_LAST, LAST_RSS = [0], {}     # the last run's memory (KB); the last measure()'s design, per workload: the median
OUT_LAST = ['']                  # Iteration 516: the last run's output, hashed
PAGE_KB = os.sysconf('SC_PAGE_SIZE') // 1024

def text_size(path):
    """Iteration 73: the engine's machine code - its ELF .text section, in
    bytes - what a design adds to the engine (handlers, pairs, the cached
    states' copies, a JIT's stencils), which the image's size does not see."""
    import struct
    b = open(path, 'rb').read()
    if b[:4] != b'\x7fELF': return None
    c64, le = b[4] == 2, '<' if b[5] == 1 else '>'
    if c64: shoff = struct.unpack_from(le + 'Q', b, 0x28)[0]; shent, shnum, shstr = struct.unpack_from(le + 'HHH', b, 0x3A)
    else: shoff = struct.unpack_from(le + 'I', b, 0x20)[0]; shent, shnum, shstr = struct.unpack_from(le + 'HHH', b, 0x2E)
    def sec(k):
        return struct.unpack_from(le + ('IIQQQQ' if c64 else 'IIIIII'), b, shoff + k * shent)
    stroff = sec(shstr)[4]
    for k in range(shnum):
        s = sec(k)
        if b[stroff + s[0]:b.index(b'\0', stroff + s[0])] == b'.text': return s[5]
    return None
def measure(eng, img, pw, works, rounds):
    """The MEDIAN CPU time per workload over the rounds, the design and the
    reference - hand-made s6 - run back to back in every round, alternating
    which goes first. Returns design / reference per workload, and the
    design's own medians: a ratio of runs seconds apart, so drift in
    background load or clock speed over a run of hours cancels.

    The median, not the best (Iteration 25). On the laptop a rare fib run
    is 20-38% faster - 0.4-2.3% of runs for some designs, with address
    randomisation on or off, at no stack offset in particular (Iteration
    27) - and the best of the rounds reported that luck: a different draw
    each session, so two sessions ranked the same designs up to 28% apart. The median of the same runs
    agreed within 3.6% between halves of a session and 2.1% between CPUs
    (results/run-spread-amd-ryzen-7-pro-8840hs.md)."""
    runs, ref = {}, {}
    LAST_RSS.clear(); mem = {}; outs = {}
    for r_ in range(rounds):
        for w in works:
            pair = [(eng, img, pw, runs), REF + (ref,)]
            for e, i, p, store in (pair if r_ % 2 == 0 else pair[::-1]):
                store.setdefault(w, []).append(run_metric(e, i, p, w))
                if store is runs: mem.setdefault(w, []).append(RSS_LAST[0])   # the design's, not s6's
                outs.setdefault((store is runs, w), set()).add(OUT_LAST[0])
    # Iteration 516: a workload's output must be s6's - the run, not only its time. Unchecked, the applications
    # workload (seed 71) rewarded failing it: 791 cpt16 designs stopped early in apps on undefined words and timed
    # 0.13 of s6 there, against ~1.07 elsewhere - one reached the front. Both ran the same program in the same rounds.
    for w in works:
        if outs.get((True, w)) != outs.get((False, w)): raise RuntimeError('wrong output: ' + w)
    if 'corpus' in mem and 'corpus' in LONGF:    # Iteration 100: the corpus's memory from one single run
        run_metric(eng, img, pw, 'corpus', single=True); mem['corpus'] = [RSS_LAST[0]]
    LAST_RSS.update({w: statistics.median(v) for w, v in mem.items()})     # a page or two of noise
    med = {w: statistics.median(runs[w]) for w in works}
    return {w: med[w] / statistics.median(ref[w]) for w in works}, med

def reach_lethal(g):
    """Scale 0 with a two-byte-only call or DOES> form: 2^14 bytes of reach,
    and the kernel workload's dictionary is larger (SCAN.md) - 345 of 345
    such designs died, none lived (seed 2 on the Ryzen, the VM rehearsal).
    So they are not run at all: run, they execute whatever lies past their
    reach, and one of them, 8cfd49f24c, looped through FORK 8,181 times -
    the third run's fork bomb (Iteration 10). At scale 1 (2^15) 13 of 18
    lived: those still run - jailed."""
    return g['enc'] == 'cv8' and g.get('scale', 0) == 0 and not (g.get('varcall') and g.get('doesfar'))
FASTGATE = [20, 1.05]   # Iteration 391 (the owner): the fast end measured twice - fast_gate(), evaluate(); --fastgate N
ISLANDS = [int(os.environ.get('EVOLVE_ISLANDS', 1))]   # Iteration 436 (results/drafts/escape-mechanism-435.md): --islands K
MIGRATE = [int(os.environ.get('EVOLVE_MIGRATE', 10))]  # generations between migrations, a ring
def fast_gate(R):
    """The speed under which a child is measured twice: 5% above the FASTGATE[0]-th fastest design alive so
    far - the fast end, and the noise band around it. The fast end's in-run speeds were ~10% optimistic
    (results/review-methodology-386.md, 2a): designs admitted on lucky draws, a 3% noise the best of
    thousands. None while fewer are alive, or with --fastgate 0."""
    n = FASTGATE[0]
    if not n: return None
    sp = sorted(r['speed'] for r in R.values() if r.get('status') == 'ok' and r.get('speed'))
    return sp[n - 1] * FASTGATE[1] if len(sp) >= n else None

def evaluate(g, rounds, keep=False, gate=None, again=False):
    # Build what the identity names: canon(g), as express() and gid() see it.
    # Built raw, a mutation that turned on byte headers in a design with
    # scaled calls was refused by the converter (--bytehdr wants --cpt 0) -
    # and the death recorded under the identity of the byte-granular design,
    # which converts. 34 such deaths on the Ryzen, 31 in the VM rehearsal.
    g = canon(g)
    d = os.path.join(EV, 'ind-' + gid(g)); rec = {'status': 'ok'}
    if reach_lethal(g):
        rec['status'] = 'died: reach limit at scale 0 - not run'
        return rec
    try:
        eng, img = build(g, d)
        rec['size'] = os.path.getsize(img)
        rec['bin'] = bin_size(eng); rec['total'] = rec['bin'] + rec['size']     # Iteration 75: an objective
        pw = private_work(d)
        alive(eng, img, pw, far=not hand_made(g))
        t, raw = measure(eng, img, pw, WORK_SEL + WORK_HELD, rounds)
        rec['t'] = t; rec['raw'] = raw
        rec['speed'] = math.exp(sum(math.log(t[w]) for w in WORK_SEL) / len(WORK_SEL))
        rec['etext'] = text_size(eng)                              # Iteration 73: tracked, not scored
        # Iteration 520: not the applications' - their data (gc16's 320 KB of cells) set every design's memory from seed 71
        # (460-500 KB, the six's 108-136): the objective measured the programs, not the machine. The rest as before.
        rec['rss'] = max([v for w_, v in LAST_RSS.items() if w_ != 'apps'] or list(LAST_RSS.values())) if LAST_RSS else None   # KB: an objective
        rec['mem'] = dict(LAST_RSS)
        rec['unit'] = UNIT
        if gate and rec['speed'] < gate:   # Iteration 391: under the fast gate, measured again; Iteration 446
            rec['gated'] = 1               # (results/drafts/fastgate-review-445.md): not at once - back to back the two
                                           # readings shared their moment's luck - but in the next generation's batch
        if TWO_WIDTHS[0] and not again: rec.update(eval32(g, rounds))       # Iteration 336: the 32-bit measurement, after the 64-bit one
    except RuntimeError as e:
        rec['status'] = str(e)
    except subprocess.TimeoutExpired:
        rec['status'] = 'died: timed out'
    if not keep: shutil.rmtree(d, ignore_errors=True)
    return rec


# ---- variation -------------------------------------------------------------
GENE_VALUES.update({    # Iteration 276: the older genes' values, once - mutate() and random_genome() both read them
    'opt': (('O2', 'O3', 'Os'), lambda v: '-' + v),
    'scale': ((0, 1, 2, 3), lambda v: 'scale=%d' % v),
    't2hot': (tuple(range(len(T2HOT))), lambda v: 't2hot=%s' % T2HOT[v]),       # Iteration 71: the tag's ranking, size against speed
    'gotodup': (tuple(range(len(GOTODUPV))), lambda v: 'gotodup=%s' % GOTODUPV[v]),   # Iteration 260: GCC's goto unfactoring
    'fbuf': (tuple(range(len(FBUFV))), lambda v: 'fbuf=%d' % FBUFV[v]),          # Iteration 115: a file's read-ahead, 4096, 1024, 512
    'fsys': (tuple(range(6)), lambda v: 'fsys=%d' % v),                         # Iterations 202-211: native, then Forth over SYSCALL, levels 1-5
    'threads': (tuple(range(4)), lambda v: 'threads=%d' % v),                   # Iteration 204: as built (32), 64, 128, 16 chains
    'regpin': (tuple(range(4)), lambda v: 'regpin=%d' % v),                     # Iteration 197: GCC's choice, three assignments
    'escape': (tuple(range(3)), lambda v: 'escape=%d' % v),                     # Iteration 11: nine more primitives behind it
})

def mutate(g, rnd):
    g = canon(g); what = []
    for _ in range(rnd.choice([1, 1, 2])):
        pool = [x for x in EXPRESSED[g['enc']] + list(CC0) if x not in FROZEN] + ['enc'] * (1 if rnd.random() < 0.2 else 0)   # 409: not FROZEN's
        k = rnd.choice(pool)
        if k in SLOW_GENES and rnd.random() < 0.9: k = rnd.choice([x for x in pool if x not in SLOW_GENES])   # Iteration 197
        if k == 'enc':
            g['enc'] = rnd.choice([f for f in FAMILIES if f != g['enc']]); what.append('family %s' % g['enc'])
        elif k in GENE_VALUES and len(GENE_VALUES[k][0]) > 2:      # Iteration 276: a value from the gene table (binary genes flip below)
            vals, show = GENE_VALUES[k]
            g[k] = rnd.choice([v for v in vals if v != g.get(k, vals[0])]); what.append(show(g[k]))
        elif k == 'spec':
            s = rnd.choice(SPECS)
            g['spec'] = [x for x in g['spec'] if x != s] if s in g['spec'] else g['spec'] + [s]
            what.append(('-' if s not in g['spec'] else '+') + 'spec ' + s)
        elif k == 'ops10':
            f = g['ops10']; out = [p for p in OPS10_POOL if p not in f]
            op = rnd.choice(['add', 'add', 'remove', 'swap'])
            if op == 'add' and out:
                p = rnd.choice(out); f.insert(rnd.randrange(len(f) + 1), p); what.append('+op %s' % p)
            elif op == 'remove' and f:
                what.append('-op %s' % f.pop(rnd.randrange(len(f))))
            elif f and out:
                i = rnd.randrange(len(f)); q = rnd.choice(out); what.append('op %s->%s' % (f[i], q)); f[i] = q
        elif k == 'opcall':           # Iteration 121: one more, one fewer, or one swapped
            f = g['opcall']; out = [n for n in opcall_avail(g) if n not in f]
            op = rnd.choice(['add', 'add', 'remove', 'swap'])
            if op == 'add' and out:
                n = rnd.choice(out); f.insert(rnd.randrange(len(f) + 1), n); what.append('+opcall %s' % n)
            elif op == 'remove' and f:
                n = f.pop(rnd.randrange(len(f))); what.append('-opcall %s' % n)
            elif f and out:
                i = rnd.randrange(len(f)); n = rnd.choice(out); what.append('opcall %s -> %s' % (f[i], n)); f[i] = n
        elif k == 'supers':
            f = g['supers']; out = [p for p in design_pairs(g) if p not in f]
            op = rnd.choice(['add', 'add', 'remove', 'swap'])
            if op == 'add' and out:
                p = rnd.choice(out); f.insert(rnd.randrange(len(f) + 1), p); what.append('+super %s %s' % tuple(p))
            elif op == 'remove' and f:
                p = f.pop(rnd.randrange(len(f))); what.append('-super %s %s' % tuple(p))
            elif f and out:
                i = rnd.randrange(len(f)); p, q = f[i], rnd.choice(out); f[i] = q
                what.append('super %s %s->%s %s' % (p[0], p[1], q[0], q[1]))
        elif k == 'folds':
            f = g['folds']; out = [p for p in POOL if p not in f]
            op = rnd.choice(['add', 'remove', 'swap'])
            if op == 'add' and len(f) < FOLDMAX and out:
                p = rnd.choice(out); f.insert(rnd.randrange(len(f) + 1), p); what.append('+fold ' + p)
            elif op == 'remove' and f:
                p = f.pop(rnd.randrange(len(f))); what.append('-fold ' + p)
            elif f and out:
                i = rnd.randrange(len(f)); p, q = f[i], rnd.choice(out); f[i] = q
                what.append('fold %s->%s' % (p, q))
        else:
            g[k] ^= 1; what.append('%s=%d' % (k, g[k]))
    # Iteration 440: rtloopall turned on, or carried blocked (one child in four), gets its prerequisite
    if g['enc'] == 'cv8' and g.get('rtloopall') and not rtloopall_on(g) and ('rtloopall=1' in what or rnd.random() < LOOP_REPAIR):
        fixed = rtloopall_repair(g)
        if fixed: what.append('rtloopall repaired (%s)' % ', '.join(fixed))
    return g, 'mutation: ' + ', '.join(what or ['(none)'])

def crossover(a, b, rnd):
    c = {}
    whole = {}                       # Iteration 197: each linked group from one parent
    for grp in LINKS:
        src = a if rnd.random() < 0.5 else b
        for k in grp: whole[k] = src
    for k in a:
        if k == 'ops10':
            pool = list(dict.fromkeys(a.get('ops10', []) + b.get('ops10', [])))
            n = rnd.randint(min(len(a.get('ops10', [])), len(b.get('ops10', []))), max(len(a.get('ops10', [])), len(b.get('ops10', []))))
            keep = set(rnd.sample(pool, min(n, len(pool))))
            c['ops10'] = [x for x in pool if x in keep]
        elif k == 'supers':
            pool = [list(x) for x in dict.fromkeys(tuple(x) for x in a['supers'] + b['supers'])]
            n = rnd.randint(min(len(a['supers']), len(b['supers'])), max(len(a['supers']), len(b['supers'])))
            keep = set(map(tuple, rnd.sample(pool, min(n, len(pool)))))
            c['supers'] = [x for x in pool if tuple(x) in keep]
        elif k == 'folds':
            pool = list(dict.fromkeys(a['folds'] + b['folds']))
            n = min(FOLDMAX, rnd.randint(min(len(a['folds']), len(b['folds'])), max(len(a['folds']), len(b['folds']))))
            keep = set(rnd.sample(pool, min(n, len(pool))))
            c['folds'] = [p for p in pool if p in keep]
        elif k == 'spec':
            c['spec'] = [s for s in SPECS if (s in (a['spec'] if rnd.random() < 0.5 else b['spec']))]
        elif k in whole and k in whole[k]:
            c[k] = whole[k][k]
        else:
            c[k] = a[k] if rnd.random() < 0.5 else b[k]
    return canon(c)

def borrow(g, donor, rnd):
    blk = rnd.choice(BLOCKS); g = canon(g)
    for k in blk: g[k] = canon(donor)[k]
    return g, 'borrowed %s' % '+'.join(blk)


# ---- selection: NSGA-II on (speed, size) -------------------------------------
# Iteration 75 (the owner): three objectives, equal - CPU time, binary +
# image, peak memory. A record from before (no binary, no memory measured)
# falls back to its image size and no memory: its own run's two.
OBJECTIVES = ('speed', 'total', 'rss')
# Iteration 336 (the owner, results/drafts/two-width-selection.md): --widths 8,4 - each design also
# measured as a 32-bit x86 engine at 4-byte cells, here (gcc -m32: the laptop runs it), its JIT off -
# a JIT design is judged at 32 bits by the interpreter under its JIT - and speed32 a fourth objective
# on the front, not folded into speed: a weakness at one width does not hide behind the other.
TWO_WIDTHS = [False]
WIDTH4 = {}                 # REF, KREF, REF_CORPUS, KERNEL_IN at 4-byte cells (setup_widths)
# Iteration 77: memory within MEM_TOL KB counts as a tie. Seed 18's
# session: 18 of the front's 39 were there by memory alone, every one a
# page or less (2-4 KB) from a design faster and smaller - the noise of the
# count, or an image a few bytes over a page boundary. With one page of
# tolerance none was. Speed and binary + image stay exact, so the relation
# has no cycles and the fronts below still sort.
MEM_TOL = float(os.environ.get('EVOLVE_MEM_TOL', 8))
# Iteration 197: speed within SPEED_TOL (a fraction) a tie, as memory within
# MEM_TOL is - seed 40's front measured again in another session moved
# +-2.6% (5-95%), so a smaller difference decided dominance by noise. In the
# generation's ranking (fronts, rank); first_front - the reports' and the
# carry's, over whole databases - stays exact (compare-fronts measures again).
SPEED_TOL = float(os.environ.get('EVOLVE_SPEED_TOL', 0.02))
# Iteration 200 (the owner: pure Python, conservative): the surrogate
# screen (results/drafts/surrogate-offline.md). A child whose predicted speed
# and binary + image are both beaten - by SCREEN_MS and SCREEN_MT - by what was
# measured before its generation is not measured: recorded "screened". The
# model is additive - one weight per gene value, log speed and log size, fitted
# by stochastic gradient descent on the earlier generations' living designs
# every SCREEN_EVERY generations (seed 40 offline: speed within 8.2%, size 1.2%;
# at 30%/5% a third of the children skipped, 1 of 163 final-front designs
# lost). One screened child in SCREEN_AUDIT is measured anyway ("screened,
# audited" in how it was made) - the screen's own check. Deterministic: the
# fit has its own seed and sees only earlier generations, the audit is chosen
# by id - a resumed run's replay decides the same. EVOLVE_SCREEN=0: off.
SCREEN = os.environ.get('EVOLVE_SCREEN', '1') != '0'
SCREEN_MS, SCREEN_MT = (float(x) for x in os.environ.get('EVOLVE_SCREEN_MARGINS', '0.30,0.05').split(','))
SCREEN_AUDIT = int(os.environ.get('EVOLVE_SCREEN_AUDIT', 10))
SCREEN_FROM = int(os.environ.get('EVOLVE_SCREEN_FROM', 5))
SCREEN_EVERY = int(os.environ.get('EVOLVE_SCREEN_EVERY', 10))
SCREEN_MIN = int(os.environ.get('EVOLVE_SCREEN_MIN', 1000))

def screen_feats(g):
    f = []
    for k, v in express(g).items():
        if isinstance(v, (list, tuple)): f += ['%s:%s' % (k, json.dumps(x, sort_keys=True)) for x in v]
        else: f.append('%s=%s' % (k, json.dumps(v, sort_keys=True)))
    return f

def screen_fit(recs, epochs=12):
    """The additive model: [(weights, bias) for log speed, for log binary + image]."""
    data = [(screen_feats(r['genome']), math.log(r['speed']), math.log(ov(r, 'total'))) for r in recs]
    model = []
    for t in (1, 2):
        w = collections.defaultdict(float); b = sum(d[t] for d in data) / len(data)
        rnd = random.Random(1); idx = list(range(len(data)))
        for ep in range(epochs):
            rnd.shuffle(idx); a = 0.02 / (1 + ep * 0.2)
            for i in idx:
                fs, y = data[i][0], data[i][t]
                e = b + sum(w[f] for f in fs) - y
                for f in fs: w[f] -= a * (e + 1e-5 * w[f])
                b -= a * e * 0.1
        model.append((dict(w), b))
    return model

def screen_predict(model, g):
    fs = screen_feats(g)
    return tuple(math.exp(b + sum(w.get(f, 0.0) for f in fs)) for w, b in model)

def screen_stair(recs):
    """What was measured, as a staircase: speeds ascending, the least size up to each."""
    sp, tt = [], []
    for s_, t_ in sorted((r['speed'], ov(r, 'total')) for r in recs):
        if tt and tt[-1] <= t_: continue
        sp.append(s_); tt.append(t_)
    return sp, tt

def screen_beaten(stair, s_, t_):
    sp, tt = stair; k = bisect.bisect_right(sp, s_ * (1 - SCREEN_MS))
    return k > 0 and tt[k - 1] <= t_ * (1 - SCREEN_MT)

def dominates(a, b):
    """Design a dominates design b: no worse in all three, better in one -
    memory by more than MEM_TOL, speed by more than SPEED_TOL. With --widths 8,4,
    speed32 a fourth, with speed's tolerance."""
    s, t, m = (ov(a, k) for k in OBJECTIVES); s2, t2, m2 = (ov(b, k) for k in OBJECTIVES)
    if not TWO_WIDTHS[0]:
        return (s <= s2 * (1 + SPEED_TOL) and t <= t2 and m <= m2 + MEM_TOL
                and (s < s2 * (1 - SPEED_TOL) or t < t2 or m < m2 - MEM_TOL))
    w, w2 = ov(a, 'speed32'), ov(b, 'speed32')
    return (s <= s2 * (1 + SPEED_TOL) and t <= t2 and m <= m2 + MEM_TOL and w <= w2 * (1 + SPEED_TOL)
            and (s < s2 * (1 - SPEED_TOL) or t < t2 or m < m2 - MEM_TOL or w < w2 * (1 - SPEED_TOL)))
def ov(r, k):
    if k == 'speed32':                  # Iteration 336: none (no 32-bit build, or not alive there) - the worst
        v = r.get('speed32'); return v if v is not None else 1e9
    if k == 'total': return r.get('total', r['size'])
    if k == 'rss': return r.get('rss') or 0
    return r[k]

def fronts(ids, R):
    # Lists, not sets: a set of ids iterates in an order that changes with
    # each process's string hashing, the fronts would come out in another
    # order, and a resumed run would pick different parents and fork.
    dom = {i: [] for i in ids}; n = {i: 0 for i in ids}
    def better(x, y):
        return dominates(R[x], R[y])
    for x in ids:
        for y in ids:
            if x != y and better(x, y): dom[x].append(y)
            elif x != y and better(y, x): n[x] += 1
    F = [[i for i in ids if n[i] == 0]]
    while F[-1]:
        nxt = []
        for x in F[-1]:
            for y in dom[x]:
                n[y] -= 1
                if n[y] == 0: nxt.append(y)
        F.append(nxt)
    F = F[:-1]
    # Iteration 197: with tolerances the relation need not be transitive - a
    # cycle would leave its designs in no front and drop them unseen; last.
    placed = set(x for f in F for x in f)
    left = [i for i in ids if i not in placed]
    return F + [left] if left else F

def first_front(ids, R):
    """fronts(ids, R)[0] - the same designs, in the same order - without
    comparing every pair (Iteration 99: a 12-hour run makes ~90,000 designs,
    and fronts() over all of them would take hours). Sorted by speed, a
    design is dominated by one strictly faster with no more total and memory
    within MEM_TOL - so, per memory value, the least total seen among the
    faster ones decides it - or by one as fast, no worse in both and better
    in one: checked within its speed. Linear in the designs, times the few
    memory values (pages: ~10)."""
    pts = sorted(((ov(R[i], 'speed'), ov(R[i], 'total'), ov(R[i], 'rss'), i) for i in ids), key=lambda p: p[0])
    mems = sorted(set(p[2] for p in pts)); least = {m: math.inf for m in mems}; out = set(); k = 0
    while k < len(pts):
        j = k
        while j < len(pts) and pts[j][0] == pts[k][0]: j += 1
        grp = pts[k:j]
        for s, t, m, i in grp:
            dom = any(least[mv] <= t for mv in mems if mv <= m + MEM_TOL)
            dom = dom or any(i2 != i and t2 <= t and m2 <= m + MEM_TOL and (t2 < t or m2 < m - MEM_TOL) for s2, t2, m2, i2 in grp)
            if not dom: out.add(i)
        for s, t, m, i in grp: least[m] = min(least[m], t)
        k = j
    return [i for i in ids if i in out]

def crowding(front, R):
    cd = {i: 0.0 for i in front}
    for k in OBJECTIVES + (('speed32',) if TWO_WIDTHS[0] else ()):
        s = sorted(front, key=lambda i: ov(R[i], k)); lo, hi = ov(R[s[0]], k), ov(R[s[-1]], k)
        cd[s[0]] = cd[s[-1]] = float('inf')
        for j in range(1, len(s) - 1):
            cd[s[j]] += (ov(R[s[j + 1]], k) - ov(R[s[j - 1]], k)) / ((hi - lo) or 1)
    return cd

# Iteration 188 (the owner): demote, don't delete - and keep what has
# potential. Survival keeps the best N of parents and children; what falls
# out is no longer simply gone: a demoted design carrying a gene value no
# survivor has goes to the attic (ATTIC of them, the rarest genes first), and
# leaves it once the population has that value again. One parent in ATTIC_P
# comes from the attic, and a borrowed gene may come from there: a stepping
# stone (a gene costly alone, good with a partner not yet found) keeps its
# chance to pass on, at no measuring cost - the attic is measured already.
# And the Q_KEEP best by Q - binary + image x run time x memory, the owner's
# compound quality: the front's knee - always survive, as the extremes
# (crowding) and each family's best already do.
# Iteration 197 (results/gp-deep-dive.md, seed 40's database): mutation-only
# children made 73% of the final front from a quarter of the children;
# crossover, then 60% of variation, was twelve times less productive per
# child - so less of it (EVOLVE_XOVER). Its uniform choice gene by gene split
# genes linked on the front (mutual information 0.67-1.00): LINKS are
# inherited whole, from one parent. varcall's and doesfar's mutants were not
# dominated by their parent 0.5% and 0.2% of the time - 3.5% of a run's
# evaluations: drawn one time in ten (SLOW_GENES).
XOVER = float(os.environ.get('EVOLVE_XOVER', 0.25))
LINKS = [('jit', 'jitx', 'jitloop', 'jitinl', 'jitos', 'jittail', 'jitk'), ('tos', 'tail', 'msc'), ('escape', 'rtloopall'), ('rtfuse', 'rtimm')]
SLOW_GENES = ('varcall', 'doesfar')
ATTIC = int(os.environ.get('EVOLVE_ATTIC', 128))
ATTIC_P = float(os.environ.get('EVOLVE_ATTIC_P', 0.1))
Q_KEEP = int(os.environ.get('EVOLVE_Q_KEEP', 8))

def qual(r):
    """Q, lower better; a record with no memory measured has none."""
    return ov(r, 'speed') * ov(r, 'total') * r['rss'] if r.get('rss') else math.inf

def genes_of(r):
    """The design's gene values as strings: one per scalar gene, one per
    element of a list gene (a fold, a pair, a slot) - the units a design can
    lose or carry alone."""
    out = []
    for k, v in sorted(express(r['genome']).items()):
        if isinstance(v, (list, tuple)): out += ['%s:%s' % (k, json.dumps(x, sort_keys=True)) for x in v]
        else: out.append('%s=%s' % (k, json.dumps(v, sort_keys=True)))
    return out

def attic_of(order, pop, attic, R):
    """The new attic: from the designs out of the population (this
    generation's demoted, then the attic before), those carrying a gene value
    no survivor has - most such values first, then by rank; deterministic, so
    a resumed run's replay rebuilds it."""
    have = set(g for i in pop for g in genes_of(R[i])); inpop = set(pop)
    cand = list(dict.fromkeys([i for i in order if i not in inpop] + [i for i in attic if i not in inpop and R[i]['status'] == 'ok']))
    nov = [(-sum(g not in have for g in genes_of(R[i])), k, i) for k, i in enumerate(cand)]
    return [i for n, k, i in sorted(nov) if n < 0][:ATTIC]

def rank(ids, R):
    order, rk, cdist = [], {}, {}
    for r, f in enumerate(fronts(ids, R)):
        c = crowding(f, R)
        for i in f: rk[i] = r; cdist[i] = c[i]
        order += sorted(f, key=lambda i: -c[i])
    return order, rk, cdist


# ---- the database ----------------------------------------------------------
LOADED = {'lines': 0, 'bad': 0, 'first_bad': None}
def load():
    """The designs evaluated so far. A run killed while writing leaves a
    truncated last line: skipped, and that design is evaluated again.
    What was skipped is counted (LOADED), so a database that cannot be
    read at all does not pass for an empty one."""
    R = {}
    LOADED.update(lines=0, bad=0, first_bad=None)
    if os.path.exists(DB):
        for l in open(DB, encoding='utf-8-sig', errors='replace'):   # a byte-order mark is not JSON
            if not l.strip(): continue
            LOADED['lines'] += 1
            try: r = json.loads(l); R[r['id']] = r
            except (ValueError, KeyError, TypeError):
                LOADED['bad'] += 1
                if LOADED['first_bad'] is None: LOADED['first_bad'] = l[:70]
    return R
def save(r):
    with open(DB, 'a') as f: f.write(json.dumps(r) + '\n')

def foldable():
    """Which primitives a fold can take, tested once and kept: a primitive
    gen-fold.py or the compiler cannot fold is a lethal gene, not a choice."""
    path = os.path.join(EV, 'foldable.json')
    if os.path.exists(path): return json.load(open(path))
    good = list(HOT)
    for p in POOL:
        if p in HOT: continue
        g = canon(HUMAN['s5-cv8spec']); g['folds'] = HOT[:-1] + [p]
        try: build(g, os.path.join(EV, 'probe')); good.append(p)
        except RuntimeError: pass
    shutil.rmtree(os.path.join(EV, 'probe'), ignore_errors=True)
    json.dump(good, open(path, 'w')); return good

def quiet_cpu():
    """taskset arguments for the core to pin every timed run to: BENCH_CPU
    if set; else the core that, with its hyperthread sibling, was least
    busy over one second - not core 0 by default, which takes interrupts
    and much background work. [] (no pinning) if taskset is missing."""
    if not shutil.which('taskset'): return []
    if os.environ.get('BENCH_CPU'): return ['taskset', '-c', os.environ['BENCH_CPU']]
    def busy():
        b = {}
        for l in open('/proc/stat'):
            f = l.split()
            if re.match(r'cpu\d+$', f[0]):
                v = list(map(int, f[1:])); b[int(f[0][3:])] = (sum(v) - v[3] - v[4], sum(v))
        return b
    try:
        a = busy(); time.sleep(1); b = busy()
        load = {c: (b[c][0] - a[c][0]) / max(b[c][1] - a[c][1], 1) for c in b}
        def sib(c):
            try:
                txt = open('/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list' % c).read().strip()
                out = set()
                for part in txt.split(','):
                    lo, _, hi = part.partition('-'); out |= set(range(int(lo), int(hi or lo) + 1))
                return out
            except OSError: return {c}
        score = {c: sum(load.get(x, 0) for x in sib(c)) for c in load}
        cand = [c for c in score if c != 0] or list(score)
        c = min(cand, key=lambda c: (score[c], c))
        print('pinned to cpu %d (it and its sibling %.0f%% busy; BENCH_CPU=N to choose)' % (c, 100 * score[c]), flush=True)
        return ['taskset', '-c', str(c)]
    except Exception:
        return []

def free_cores(n):
    """Iteration 99 (the owner: four cores): n logical CPUs on n different
    physical cores - each the least busy over a second, its hyperthread
    sibling counted with it, core 0 last (interrupts) - for n workers, each
    timing on its own core. BENCH_CPUS=2,4,6,10 to choose. Fewer if the
    machine has fewer cores (a VM: the workers share them)."""
    if os.environ.get('BENCH_CPUS'): return [int(c) for c in os.environ['BENCH_CPUS'].split(',')][:n]
    def busy():
        b = {}
        for l in open('/proc/stat'):
            f = l.split()
            if re.match(r'cpu\d+$', f[0]):
                v = list(map(int, f[1:])); b[int(f[0][3:])] = (sum(v) - v[3] - v[4], sum(v))
        return b
    def sib(c):
        try:
            out = set()
            for part in open('/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list' % c).read().strip().split(','):
                lo, _, hi = part.partition('-'); out |= set(range(int(lo), int(hi or lo) + 1))
            return frozenset(out)
        except OSError: return frozenset([c])
    try: allowed = sorted(os.sched_getaffinity(0))
    except AttributeError: allowed = list(range(os.cpu_count() or 1))
    a = busy(); time.sleep(1); b = busy()
    load = {c: (b[c][0] - a[c][0]) / max(b[c][1] - a[c][1], 1) for c in b if c in allowed}
    cores = {}
    for c in load: cores.setdefault(sib(c), []).append(c)
    ranked = sorted(cores, key=lambda k: (0 in k, sum(load.get(x, 0) for x in k), min(k)))
    return [min(c for c in k if c in load) for k in ranked][:n]

WORKERS = [None]
def _worker(q):
    """A worker of --jobs N: its own core for everything it runs - builds and
    timed runs alike - and its own copy of the reference's work directory
    (the kernel workload writes kernel.img there)."""
    global REF
    cpu = q.get()
    if cpu is not None:
        try: os.sched_setaffinity(0, {cpu})
        except (AttributeError, OSError): pass
        PIN[:] = ['taskset', '-c', str(cpu)] if shutil.which('taskset') else []
    d = os.path.join(EV, 'ref-w%d' % os.getpid()); shutil.rmtree(d, ignore_errors=True)
    REF = (REF[0], REF[1], private_work(d))
def _job(a):
    t0 = time.time(); rec = evaluate(*a); rec['secs'] = round(time.time() - t0, 1); return rec
def start_pool(n):
    """n workers on n cores (free_cores); the evaluation order is the run's
    order either way, so a resumed or a serial run asks for the same designs."""
    import multiprocessing as mp
    cpus = free_cores(n); ctx = mp.get_context('fork'); q = ctx.SimpleQueue()
    for k in range(n): q.put(cpus[k % len(cpus)] if cpus else None)
    WORKERS[0] = ctx.Pool(n, initializer=_worker, initargs=(q,))
    print('%d workers, on cpus %s%s' % (n, ', '.join(map(str, cpus)), ' (shared: fewer cores than workers)' if len(cpus) < n else ''), flush=True)

def stale_build():
    """The sources build/ is made from, newer than build/ itself - after
    a git pull without a rebuild. The evolver builds every design from the
    engine source the build generated (vm-lab-tos.c) and from its dumps:
    stale, the newer genes die for reasons that are not theirs."""
    made = [os.path.join(O, f) for f in ('vm-lab-tos.c', KW() + '-self.txt', KW() + '-b.txt')]
    if not all(os.path.exists(f) for f in made): return ['(build/ is incomplete)']
    when = min(os.path.getmtime(f) for f in made)
    srcs = [os.path.join(ROOT, 'engine', 'vm-lab.c'), os.path.join(ROOT, 'tools', 'gen-tos.py'),
            os.path.join(ROOT, 'tools', 'build-stages.sh')]
    srcs += [os.path.join(ROOT, 'forth', f) for f in os.listdir(os.path.join(ROOT, 'forth'))
             if f.endswith('.4') or f.endswith('-seed.img')]
    return sorted(os.path.relpath(f, ROOT) for f in srcs if os.path.exists(f) and os.path.getmtime(f) > when + 1)

def setup():
    if os.geteuid() == 0 and not os.environ.get('EVOLVE_ALLOW_ROOT'):
        sys.exit('evolve.py: will not run as root. Engines are denied fork by RLIMIT_NPROC, '
                 'which does not bind root, and a broken design can fork without bound '
                 '(Iteration 10). EVOLVE_ALLOW_ROOT=1 only where a fork bomb cannot hurt.')
    global REF_CORPUS, KREF, UNIT, POOL
    newer = stale_build()
    if newer:
        sys.exit('build/ is older than its sources (%s%s) - after a git pull, build again:\n'
                 '    LAYOUTS=1 bash tools/build-stages.sh && bash tools/run-tests.sh && python3 lab/evolve/evolve.py --validate'
                 % (', '.join(newer[:4]), ', ...' if len(newer) > 4 else ''))
    for need in (CPUT, os.path.join(O, KW() + '-self.txt'), os.path.join(O, 'vm-lab-tos.c')):
        if not os.path.exists(need): sys.exit('%s missing: run tools/build-stages.sh first' % need)
    # The CV8 compiler with table-driven folds and run-time fusion
    # (forth/cv8-fuse.4), dumped the way tools/build-stages.sh dumps cv8.4.
    import shutil
    W = os.path.join(O, 'work')
    for f4 in ('cv8-fuse.4', 'cv8-fuse-imm.4', 'cv8-imm.4', 'cv8-fuse-loop.4', 'cv8-fuse-loopall.4', 'cv8b-kfast.4', 'cv8b-kinput.4', 'cv8b-klookup.4', 'cv8b-knumber.4', 'cv8-fuse-iplus.4',
               'cv8t.4', 'cv8bt.4', 'cv8t-fuse.4', 'cv8t-fuse-imm.4', 'cv8t-jit.4', 'cv8t-empty.4', 'file-sysc.4', 'file-sysc2.4', 'file-sysc3.4', 'file-sysc4.4', 'file-sysc5.4'):    # Iteration 67: the two-bit tag's     # rtimm (37), rtloop (41), rtloopall (43), kfast (49)
        src4, dst4 = os.path.join(ROOT, 'forth', f4), os.path.join(W, f4)
        if not (os.path.exists(dst4) and os.path.samefile(src4, dst4)): shutil.copy(src4, dst4)   # a fresh build links it
    base = subprocess.run([S0(), KIMG()], input=b'S" dict-dump-addr.4" INCLUDED\nBYE\n', cwd=W, capture_output=True).stdout
    BASE_NAMES.clear(); BASE_NAMES.update(n.strip().upper() for n in re.findall(r'^N -?\d+ -?\d+ (.*)$', base.replace(b'\r', b'').decode('latin-1'), re.M))   # Iteration 212
    for name, files in [(b + k + f + l + t + e + q + j + y + '.txt', fs) for b, fs in ((KW() + '-self', ['cv8.4']), (KW() + '-b', ['cv8.4', 'cv8b.4']),
                                                                    (KW() + '-bt', ['cv8t.4', 'cv8bt.4']))   # tag 2: Iteration 67
                        for k in (('', '-kfast', '-kfast-kinput', '-kfast-kinput-klookup', '-kfast-kinput-klookup-knumber') if b != KW() + '-self' else ('',))   # 501: -nocase retired
                        for f in (('', '-fuse', '-fuse-imm', '-lit') if b != KW() + '-bt' else ('', '-fuse', '-fuse-imm')) for l in ('', '-loop', '-loopall')   # -lit: Iteration 422
                        for t in (('', '-iplus') if l == '-loopall' else ('',))
                        for e in (('', '-empty') if b == KW() + '-bt' else ('',))     # Iteration 101
                        for q in ('',)    # Iteration 456: kstack's dumps gone (kstack frozen off since 450)
                        for j in (('', '-jit') if b == KW() + '-bt' else ('',))
                        for y in ('', '-fsys', '-fsys2', '-fsys3', '-fsys4', '-fsys5') if k or f or l or t or e or q or j or y or b == KW() + '-bt']:   # -fsys: Iteration 202; -fsys2: 205   # -jit: Iteration 80   # the plain two: build-stages'
        boot = ''.join('S" %s" INCLUDED\n' % f for f in files + (['cv8b-kfast.4'] if '-kfast' in name else []) + (['cv8b-kinput.4'] if '-kinput' in name else []) + (['cv8b-klookup.4'] if '-klookup' in name else []) + (['cv8b-knumber.4'] if '-knumber' in name else [])
                       + ([('cv8t-fuse.4' if name.startswith(KW() + '-bt') else 'cv8-fuse.4')] if '-fuse' in name else [])
                       + ([('cv8t-fuse-imm.4' if name.startswith(KW() + '-bt') else 'cv8-fuse-imm.4')] if '-imm' in name else [])
                       + (['cv8-imm.4'] if '-lit' in name else [])     # Iteration 422: the immediates alone
                       + (['cv8-fuse-loopall.4'] if '-loopall' in name
                       else ['cv8-fuse-loop.4'] if '-loop' in name else [])
                       + (['cv8-fuse-iplus.4'] if '-iplus' in name else [])
                       + (['cv8t-empty.4'] if '-empty' in name else [])     # Iteration 101: after the fusers, before the JIT
                       + (['cv8t-jit.4'] if '-jit' in name else [])          # Iteration 80: last - its ;8 wraps the others'
                       + (['file-sysc.4'] if '-fsys' in name else [])        # Iteration 202: after every kernel word - none refers to it
                       + (['file-sysc2.4'] if any(k in name for k in ('-fsys2', '-fsys3', '-fsys4', '-fsys5')) else [])   # Iteration 205: the rest of the file words (fsys 2)
                       + (['file-sysc3.4'] if any(k in name for k in ('-fsys3', '-fsys4', '-fsys5')) else [])   # Iteration 206: WRITE, READ, READ-LINE, BYE (fsys 3)
                       + (['file-sysc4.4'] if '-fsys4' in name or '-fsys5' in name else [])   # Iteration 207: the output buffered off a terminal (fsys 4)
                       + (['file-sysc5.4'] if '-fsys5' in name else [])      # Iteration 211: READ-LINE reading ahead where a file can seek (fsys 5)
                       + ['dict-dump-addr.4']) + 'BYE\n'
        out = subprocess.run([S0(), KIMG()], input=boot.encode(), cwd=W, capture_output=True).stdout
        dump_guard(name, boot, out)                          # Iteration 212: every file loaded, whole
        open(os.path.join(O, name), 'wb').write(out.replace(b'\r', b''))
    os.makedirs(EV, exist_ok=True)
    # The corpus as tools/run-tests.sh feeds it, written here so a fresh
    # build is enough: the CORE tests, then a sentinel that proves the end.
    with open(CORPUS, 'wb') as f:
        f.write(open(os.path.join(ROOT, 'tests', 'corpus', 'core.fth'), 'rb').read())
        f.write(b'\nS" CORPUS-REACHED-END" TYPE CR\nBYE\n')
    if cellw() == 4:
        # Iteration 326: at 4-byte cells the kernel workload builds the 4-byte kernel - as
        # tools/reseed.sh makes kernel32-seed.img: cross.4 with its one width line retargeted. A
        # 4-byte host cannot build the 8-byte kernel (cross.4 leaves a narrow host's high bytes
        # zero), and the reference is the kernel of the design's own width.
        global KERNEL_IN
        c4 = open(os.path.join(ROOT, 'forth', 'cross.4')).read()
        c32 = re.sub(r'(?m)^8 TARGET-CELL-BYTES !', '4 TARGET-CELL-BYTES !', c4)
        if c32 == c4: sys.exit('cannot retarget cross.4 to 4-byte cells (tools/reseed.sh has the same check)')
        open(os.path.join(W, 'cross32.4'), 'w').write(c32)
        KERNEL_IN = b'S" extend.4" INCLUDED\nS" cross32.4" INCLUDED\n'
    KREF = os.path.join(EV, 'kernel-ref%s.img' % ('32' if cellw() == 4 else '')); shutil.copy(os.path.join(W, KIMG()), KREF)   # 336: one a width
    with open(CORPUS, 'rb') as f:
        REF_CORPUS = sh([S0(), os.path.join(O, 's0-cell-s%d.img' % (8 * cellw()))], cwd=W, inp=f.read()).stdout
    UNIT = 'median ' + ('cycles' if os.environ.get('EVOLVE_METRIC') == 'cycles' else 'cpu time') + ' / hand-made s6'   # median: Iteration 25
    UNIT += ', long workloads (Iteration 100)'
    long_files()
    PIN[:] = quiet_cpu()
    # the reference every measurement is paired with: hand-made s6
    global REF
    rd = os.path.join(EV, 'reference' + ('32' if cellw() == 4 else '')); shutil.rmtree(rd, ignore_errors=True); os.makedirs(rd)   # 336: one a width
    # Iteration 331: a check's host may be handed its reference built (EVOLVE_PREBUILT_REF, a
    # directory with engine and image - xcheck's prebuilt s6), when it cannot build one itself:
    # dream.lan has no 32-bit C compiler, and its 32-bit check measures the laptop's binaries
    pre_ref = os.environ.get('EVOLVE_PREBUILT_REF')
    if pre_ref: os.makedirs(rd, exist_ok=True); re_, ri = os.path.join(pre_ref, 'engine'), os.path.join(pre_ref, 'image')
    else: re_, ri = build(canon(HUMAN['s6-cv8b']), rd)
    rp = private_work(rd)
    REF = (re_, ri, rp)
    POOL = foldable()


def random_genome(rnd):
    """Uniform over the genome's space (prompts/02, step 5): a family drawn
    uniformly, then every gene it expresses and every compiler gene drawn
    uniformly from its domain. Lists are uniform random subsets in random
    order - each member in or out with even odds - folds cut to FOLDMAX,
    pairs from the founders' fixed pool (no profiling per draw)."""
    g = dict(HUMAN['s6-cv8b']); g['enc'] = rnd.choice(FAMILIES)
    for k in list(EXPRESSED[g['enc']]) + list(CC0):
        v = g.get(k, CC0.get(k))
        if k in GENE_VALUES and len(GENE_VALUES[k][0]) > 2: g[k] = rnd.choice(GENE_VALUES[k][0])   # Iteration 276: the gene table
        elif k == 'spec': g[k] = [x for x in SPECS if rnd.random() < 0.5]
        elif k == 'opcall': g[k] = [n for n in OPCALL_POOL if rnd.random() < 0.5]
        elif k in ('ops10', 'supers', 'folds'):
            f = [x for x in {'ops10': OPS10_POOL, 'supers': SUPER_POOL, 'folds': POOL}[k] if rnd.random() < 0.5]
            rnd.shuffle(f); g[k] = f[:FOLDMAX] if k == 'folds' else f
        elif isinstance(v, int) or v is None: g[k] = rnd.randrange(2)
        else: sys.exit('sample: no domain known for gene %s (%r)' % (k, v))
    return canon(g)


def sample(argv):
    """--sample N [--seed S] [--rounds R]: N designs drawn uniformly, each
    built, checked and timed as the run does them - before trusting any
    optimum (prompts/02, step 5): how many live, the spread of speed and
    size, and where s6 and the run's best fall in it. Records go to
    build/evolve/sample-seedS.jsonl, one per design, never the run's
    database; run again, it resumes where it stopped."""
    val = lambda k, d: argv[argv.index(k) + 1] if k in argv else d
    n, seed, rounds = int(val('--sample', 0)), int(val('--seed', 1)), int(val('--rounds', 2))
    rnd = random.Random(seed); draws = [random_genome(rnd) for _ in range(n)]
    # The draws depend on the gene pool: a new gene changes every draw after
    # the first that meets it. So the file is named after the pool, and a
    # sample drawn from another pool is never mixed in.
    pool = hashlib.sha1(json.dumps([FAMILIES, CC0, EXPRESSED, SPECS, OPS10_POOL, SUPER_POOL, POOL, FOLDMAX], sort_keys=True).encode()).hexdigest()[:6]
    path = os.path.join(EV, 'sample-seed%d-%s.jsonl' % (seed, pool)); done = {}
    if os.path.exists(path):
        for line in open(path):
            try: r = json.loads(line); done[r['id']] = r
            except ValueError: pass
    setup()
    with open(path, 'a') as out:
        for i, g in enumerate(draws):
            if gid(g) in done: continue
            r = evaluate(g, rounds); r.update(id=gid(g), enc=g['enc'], genome=g)
            out.write(json.dumps(r) + '\n'); out.flush(); done[r['id']] = r
            print('  %d/%d %s %-5s %s' % (i + 1, n, gid(g), g['enc'], '%.3f %d B' % (r['speed'], r['size']) if r['status'] == 'ok' else r['status'][:60]), file=sys.stderr, flush=True)
    R = [done[gid(g)] for g in draws]; ok = sorted((r for r in R if r['status'] == 'ok'), key=lambda r: r['speed'])
    q = lambda xs, f: xs[min(len(xs) - 1, int(f * len(xs)))]
    model = next((l.split(':', 1)[1].strip() for l in open('/proc/cpuinfo') if l.startswith('model name')), '?')
    L = ['# A uniform sample of the design space', '',
         'machine: %s; commit %s; %d designs, seed %d, %d rounds; every figure MEASURED, as the run measures (CPU time over s6\'s, paired).'
         % (model, sh(['git', '-C', ROOT, 'rev-parse', '--short', 'HEAD']).stdout.decode().strip(), n, seed, rounds),
         'Drawn: the family uniformly, then each gene uniformly over its domain (lists: each member in or out with even odds, random order; folds cut to %d; pairs from the founders\' pool).' % FOLDMAX, '',
         'alive: %d of %d' % (len(ok), n)]
    deaths = collections.Counter(re.sub(r'[0-9a-f]{10}|\d+', '#', r['status'])[:70] for r in R if r['status'] != 'ok')
    L += ['', '| died of | designs |', '|---|---|'] + ['| %s | %d |' % (c, k) for c, k in deaths.most_common()] if deaths else []
    if ok:
        sp = [r['speed'] for r in ok]; sz = sorted(r['size'] for r in ok)
        L += ['', 'speed against s6: fastest %.3f, quartile %.3f, median %.3f, quartile %.3f, slowest %.3f; faster than s6: %d of %d'
              % (sp[0], q(sp, .25), q(sp, .5), q(sp, .75), sp[-1], sum(x < 1 for x in sp), len(sp)),
              'size: smallest %d, median %d, largest %d bytes' % (sz[0], q(sz, .5), sz[-1])]
        R0 = load() if os.path.exists(DB) else {}
        best = min((r['speed'] for r in R0.values() if r.get('status') == 'ok'), default=None)
        if best: L.append("the run's database's fastest, %.3f, is faster than %d of the %d sampled designs alive" % (best, sum(x > best for x in sp), len(sp)))
        L += ['', '| family | drawn | alive | fastest | median |', '|---|---|---|---|---|']
        for f in FAMILIES:
            fs = [r['speed'] for r in ok if r['enc'] == f]
            L.append('| %s | %d | %d | %s | %s |' % (f, sum(r['enc'] == f for r in R), len(fs), '%.3f' % fs[0] if fs else '-', '%.3f' % q(fs, .5) if fs else '-'))
    print('\n'.join(L))


def knockout(argv):
    """--knockout [ID,...] [--rounds N]: for each design (default: the
    front, measured again where --remeasure has been run), undo one gene
    at a time - set it to hand-made s6's value - and measure again: what
    each gene is worth IN that design, interactions included. Reported
    for pasting back from another machine (prompts/11): machine, commit,
    settings, and for every variant its name, the expected and the actual
    value. Calibrated against known answers (prompts/03): s6 against
    itself must come out 1.000 and its image exactly s6's size; the design
    itself is measured again in the same session."""
    R = load(); ok = [i for i in R if R[i]['status'] == 'ok']
    if not ok: nothing_alive(R); sys.exit(1)
    i_ = argv.index('--knockout')
    ids = argv[i_ + 1].split(',') if i_ + 1 < len(argv) and not argv[i_ + 1].startswith('--') else None
    rounds = int(argv[argv.index('--rounds') + 1]) if '--rounds' in argv else 6
    if ids is None:                                   # the front, by re-measured speed where there is one
        rm = os.path.join(EV, 'remeasure.json'); rm = json.load(open(rm)) if os.path.exists(rm) else {}
        F = first_front(ok, R)          # Iteration 107: not fronts() - every pair of a long run's ~40,000 designs
        sp = {i: rm[i]['speed'] if i in rm else R[i]['speed'] for i in F}
        ids = [i for i in F if not any(sp[j] <= sp[i] and R[j]['size'] <= R[i]['size'] and (sp[j], R[j]['size']) != (sp[i], R[i]['size']) for j in F)]
        ids.sort(key=lambda i: sp[i])
    bad = [i for i in ids if i not in R or R[i]['status'] != 'ok']
    if bad: sys.exit('not alive in %s: %s' % (DB, ', '.join(bad)))
    s6 = canon(HUMAN['s6-cv8b'])
    model = next((l.split(':', 1)[1].strip() for l in open('/proc/cpuinfo') if l.startswith('model name')), '?')
    head = ['# Knockouts', '',
            'machine: %s; commit %s; %s UTC; %s; %d rounds; every figure MEASURED (none modelled): CPU time over'
            % (model, sh(['git', '-C', ROOT, 'rev-parse', '--short', 'HEAD']).stdout.decode().strip(),
               time.strftime('%Y-%m-%d %H:%M', time.gmtime()), ' '.join(PIN) or 'not pinned', rounds),
            "hand-made s6's, paired run by run, geometric mean over %s; size of the self-hosting image." % ', '.join(WORK_SEL), '',
            'How these can mislead (prompts/03): each knockout measures a gene IN this design - interactions included, so the',
            'changes do not add up to the total; "also changed" names what moved with it (the escape takes its slots, and',
            'with them pairs and words; a dormant gene can wake: undoing multi-state caching turns on tail calls the genome',
            'carries); a difference smaller than the calibration\'s distance from 1.000 is noise.', '']
    log = lambda m: print(m, file=sys.stderr, flush=True)      # progress; the report goes to stdout once, at the end
    cal = evaluate(s6, rounds)                         # prompts/03: a case whose answer is known
    calline = ('calibration, s6 against itself: speed expected 1.000, measured %.3f; size expected %d, measured %d - %s'
               % (cal.get('speed', float('nan')), R[next(i for i in R if R[i]['how'] == 'hand-made s6-cv8b')]['size'] if any(R[i]['how'] == 'hand-made s6-cv8b' for i in R) else 10065,
                  cal.get('size', -1), cal['status']))
    log(calline)
    out = head + [calline, '']
    for did in ids:
        g = canon(R[did]['genome']); eg = express(g)
        me = evaluate(g, rounds)
        line = ('## %s\n\ncalibration, the design itself: speed in the run %.3f, measured now %.3f; size recorded %d, measured %d - %s'
                % (did, R[did]['speed'], me.get('speed', float('nan')), R[did]['size'], me.get('size', -1), me['status']))
        log(line); out += [line, '']
        if me['status'] != 'ok': continue
        rows = []
        for k in list(eg):
            if k == 'enc' or g.get(k) == s6.get(k): continue
            v = canon(dict(g, **{k: s6[k]})); ev = express(v)
            if ev == eg: continue                      # dormant here: nothing to undo
            # what else moved, by EFFECTIVE value: a gene gone dormant counts as s6's value
            also = sorted(x for x in set(ev) | set(eg) if x != k and ev.get(x, s6.get(x)) != eg.get(x, s6.get(x)))
            r = evaluate(v, rounds)
            show = lambda x: (('%d items' % len(x)) if isinstance(x, list) else str(x))
            if r['status'] == 'ok':
                rows.append((r['speed'] / me['speed'] - 1, '| %s | %s -> %s | %s | %.3f | %+.1f%% | %d | %+d | %s |' % (
                    k, show(g[k]), show(s6[k]), ', '.join(also) or '-', r['speed'], 100 * (r['speed'] / me['speed'] - 1),
                    r['size'], r['size'] - me['size'], ' '.join('%s %.3f' % (w, r['t'][w]) for w in WORK_SEL + WORK_HELD if w in r['t']))))
            else:
                rows.append((float('inf'), '| %s | %s -> %s | %s | %s | - | - | - | - |' % (k, show(g[k]), show(s6[k]), ', '.join(also) or '-', r['status'])))
            log('  %s: %s' % (k, rows[-1][1]))
        tab = ['| gene | design -> s6 | also changed | speed without it | change | size | change | per workload |',
               '|---|---|---|---|---|---|---|---|'] + [x for _, x in sorted(rows, key=lambda t: -t[0])]
        out += tab + ['']
    path = os.path.join(EV, 'knockout.md')
    open(path, 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))
    log('written: %s' % path)

def main(argv):
    if '-h' in argv or '--help' in argv:
        print(__doc__); return
    known = {'--validate', '--report', '--pop', '--gens', '--rounds', '--seed', '--db', '--knockout', '--remeasure', '--sample', '--carry', '--require',
             '--jobs', '--until', '--fromzero', '--noevolved', '--widths', '--fastgate', '--islands'}
    if '--islands' in argv: ISLANDS[0] = int(argv[argv.index('--islands') + 1])   # Iteration 436
    if '--require' in argv: REQUIRE[:] = [x for x in argv[argv.index('--require') + 1].split(',') if x]
    if '--widths' in argv:                     # Iteration 336: 8,4 - selecting at both widths
        if argv[argv.index('--widths') + 1] != '8,4': sys.exit('--widths: 8,4 only')
        TWO_WIDTHS[0] = True
    bad = [a for a in argv if a.startswith('-') and a not in known]
    if bad:
        # Iteration 4: `--help`, unrecognised, started a full run that wrote
        # 86 records into the VM rehearsal's database.
        sys.exit('evolve.py: unknown option %s (see --help)' % ', '.join(bad))
    global DB
    if '--db' in argv:                 # read another database: an earlier run kept aside
        DB = os.path.abspath(argv[argv.index('--db') + 1])
    def opt(name, default):
        return type(default)(argv[argv.index(name) + 1]) if name in argv else default
    setup_widths()                         # Iteration 336: setup() itself, unless --widths 8,4
    if '--validate' in argv:
        ok = True
        for name, g in HUMAN.items():
            d = os.path.join(EV, 'validate-' + name)
            try:
                eng, img = build(g, d)
                same = open(img, 'rb').read() == open(os.path.join(O, name + '-s%d.img' % (8 * cellw())), 'rb').read()   # Iteration 338
                pw = private_work(d); alive(eng, img, pw, far=False)   # Iteration 158: run-tests.sh judges them far
                print('  %-11s image %s the build\'s, corpus and kernel workload correct' % (name, 'IDENTICAL to' if same else 'DIFFERENT from'))
                ok &= same
            except RuntimeError as e:
                print('  %-11s %s' % (name, e)); ok = False
            shutil.rmtree(d, ignore_errors=True)
        sys.exit(0 if ok else 1)
    if '--report' in argv:
        report(load()); return
    if '--knockout' in argv:
        knockout(argv); return
    if '--sample' in argv:
        sample(argv); return
    if '--remeasure' in argv:
        # The front, measured again with more rounds: chosen as the best of
        # many noisy measurements, its designs were partly chosen for luck.
        # In the VM rehearsal they came out 3-6% slower when re-measured.
        R = load(); ok = [i for i in R if R[i]['status'] == 'ok']
        if not ok: nothing_alive(R); sys.exit(1)
        F = first_front(ok, R); n = opt('--remeasure', 6); out = {}
        path = os.path.join(EV, 'remeasure.json')
        if os.path.exists(path): out = json.load(open(path))
        for i in sorted(F, key=lambda i: R[i]['speed']):
            r = evaluate(canon(R[i]['genome']), n)
            if r['status'] == 'ok': out[i] = {'speed': r['speed'], 't': r['t'], 'rounds': n}
            print('  %s: in the run %.3f, re-measured %s' % (i, R[i]['speed'], ('%.3f' % r['speed']) if r['status'] == 'ok' else r['status']), flush=True)
            json.dump(out, open(path, 'w'))
        report(R); return
    N, G, ROUNDS, rnd = opt('--pop', 16), opt('--gens', 10), opt('--rounds', 3), random.Random(opt('--seed', 1))
    FASTGATE[0] = opt('--fastgate', FASTGATE[0])          # Iteration 391: 0, off
    JOBS, UNTIL = opt('--jobs', 1), opt('--until', 0)        # Iteration 99: workers on their own cores; a deadline
    R = load()
    if JOBS > 1: start_pool(JOBS)
    # The designs THIS run has asked for so far. Its decisions must not look
    # at the whole database: resumed, it replays from there, and the
    # database already holds what the first attempt made later - the
    # replay would make different children and fork instead of resuming.
    seen, pending = set(), {}
    SCR = {'model': None, 'fit': -1}          # Iteration 200: the screen's model and when it was fitted
    def get(g, parents, how, gen):
        """The design's id; asked for, it is evaluated at the next flush()."""
        if not how.startswith('hand-made'): g = canon(require(g))   # Iteration 71; 409: FROZEN, always
        i = gid(g); seen.add(i)
        if i not in R and i not in pending: pending[i] = (g, parents, how, gen)
        return i
    def flush():
        """Iteration 99: what get() asked for, evaluated - by the workers when
        --jobs N - and recorded in the order asked: a generation's children are
        all made before any is needed, so the run decides as it did serially."""
        items = list(pending.items()); pending.clear()
        gen_now = max((it[1][3] for it in items), default=0)
        if SCREEN and items and gen_now >= SCREEN_FROM:          # Iteration 200: the screen
            if SCR['model'] is None or gen_now - SCR['fit'] >= SCREEN_EVERY:
                recs = [r for r in R.values() if r['status'] == 'ok' and r.get('speed') and ov(r, 'total') and r.get('gen', 0) < gen_now]
                if len(recs) >= SCREEN_MIN:
                    SCR['model'], SCR['fit'] = screen_fit(recs), gen_now
                    print('  the screen: fitted on %d designs at generation %d' % (len(recs), gen_now), flush=True)
            if SCR['model'] is not None:
                stair = screen_stair([r for r in R.values() if r['status'] == 'ok' and r.get('speed') and ov(r, 'total') and r.get('gen', 0) < gen_now])
                keep, n_scr, n_aud = [], 0, 0
                for i, (g, parents, how, gen) in items:
                    ps, pt = screen_predict(SCR['model'], canon(g))
                    if gen >= SCREEN_FROM and screen_beaten(stair, ps, pt):
                        if int(i, 16) % SCREEN_AUDIT == 0:
                            n_aud += 1; keep.append((i, (g, parents, how + '; screened, audited', gen))); continue
                        n_scr += 1
                        rec = {'status': 'screened', 'pred': [round(ps, 4), round(pt)], 'secs': 0,
                               'id': i, 'genome': canon(g), 'parents': parents, 'how': how, 'gen': gen}
                        R[i] = rec; save(rec)
                    else: keep.append((i, (g, parents, how, gen)))
                if n_scr or n_aud: print('  the screen: %d of %d children not measured, %d audited' % (n_scr, len(items), n_aud), flush=True)
                items = keep
        gate = fast_gate(R)                                   # Iteration 391
        args = [(canon(g), ROUNDS, False, gate) for i, (g, parents, how, gen) in items]
        # Iteration 446: the gated children of the generation before, measured again in this batch - among other
        # co-runners, at another moment - their speed the geometric mean of the two readings then
        again = [i for i, r in R.items() if r.get('gated') == 1 and r.get('status') == 'ok'] if items else []
        args += [(R[i]['genome'], ROUNDS, False, None, True) for i in again]
        results = list(WORKERS[0].imap(_job, args) if WORKERS[0] else map(_job, args))
        for i, rec2 in zip(again, results[len(items):]):
            r = R[i]
            if rec2.get('status') == 'ok' and rec2.get('t'):
                t1, raw1 = r['t'], r.get('raw', {})
                r['speed1'], r['speed2'] = r['speed'], rec2['speed']
                r['t'] = t = {w: math.sqrt(t1[w] * rec2['t'][w]) for w in t1 if w in rec2['t']}
                r['raw'] = {w: math.sqrt(raw1[w] * rec2['raw'][w]) for w in raw1 if w in rec2.get('raw', {})}
                r['speed'] = math.exp(sum(math.log(t[w]) for w in WORK_SEL) / len(WORK_SEL))
            r['gated'] = 2; save(r)
            print('    %s measured again: %.4g, then %s - %s' % (i, r.get('speed1', r['speed']), ('%.4g' % r['speed2']) if 'speed2' in r else rec2.get('status'), ('speed %.4g' % r['speed'])), flush=True)
        for (i, (g, parents, how, gen)), rec in zip(items, results[:len(items)]):
            rec.update(id=i, genome=canon(g), parents=parents, how=how, gen=gen)
            R[i] = rec; save(rec)
            print('    %s %-24s %s' % (i, rec['status'] if rec['status'] != 'ok' else
                  'speed %.4g size %d%s' % (rec['speed'], rec['size'], ' twice %.4g/%.4g' % (rec['speed1'], rec['speed2']) if 'speed1' in rec else ''), how[:70]), flush=True)
    # Iteration 115 (the owner: "sod32 from nothing"): --fromzero - the first
    # generation all random genomes, uniform over the whole space: no hand-made
    # design, no founder, nothing carried, no mutant of a hand-made one (the
    # seeded fill). Hand-made s6 stays the yardstick, outside the population.
    FROMZERO = '--fromzero' in argv
    NOEVOLVED = '--noevolved' in argv   # Iteration 387: no founder drawn from an earlier run's record (results/review-methodology-386.md, 1)
    if FROMZERO:
        pop = []
        while len(pop) < N:
            g = random_genome(rnd); g = require(g)
            pop.append(get(g, [], 'random', 0))
        print('  from zero: %d random genomes' % len(pop), flush=True)
    pop = pop if FROMZERO else [get(g, [], 'hand-made ' + n, 0) for n, g in HUMAN.items()]
    # Founders carrying superinstructions, so the gene enters with a population
    # behind it rather than waiting on one mutation in seventeen.
    if not FROMZERO: pop += [get(dict(HUMAN['s4-cv8'], supers=SUPER_POOL[:24], rtfuse=1), [], 'founder: s4-cv8 + 24 pairs, run-time fusion', 0),
            get(dict(HUMAN['s6-cv8b'], supers=SUPER_POOL[:2]), [], 'founder: s6-cv8b + 2 pairs', 0),
            get(dict(HUMAN['s6-cv8b'], supers=SUPER_POOL[:2], rtfuse=1), [], 'founder: s6-cv8b + 2 pairs, run-time fusion', 0),
            get(dict(HUMAN['s4-cv8'], ops10=list(OPS10_POOL), supers=SUPER_POOL[:20]), [], 'founder: s4-cv8 + format-10 opcodes + 20 pairs', 0),
            get(dict(HUMAN['s6-cv8b'], ops10=OPS10_POOL[:2]), [], 'founder: s6-cv8b + EXECUTE, I as opcodes', 0),
            get(dict(HUMAN['s6-cv8b'], escape=1, ops10=list(OPS10_POOL), supers=list(SUPER_POOL)), [], 'founder: s6-cv8b + escape, 7 words, 24 pairs', 0),
            get(dict(HUMAN['s6-cv8b'], escape=1, ops10=list(OPS10_POOL), supers=list(SUPER_POOL), rtfuse=1), [], 'founder: s6-cv8b + escape, all format-10 opcodes, pairs, tests fused at run time', 0)]
    # Iteration 155 (the owner): founders carrying the JIT's new genes, so jitloop and
    # jitinl enter with designs behind them - through seed 38 they were dormant, no
    # genome has them, and jitinl is two mutations (jitx too) from most JIT designs.
    # One competitive - seed 37's fastest, its record from results/ - and one any
    # tree can make, from hand-made s6; crossover lends their genes on.
    if not FROMZERO:
        pop += [get(dict(HUMAN['s6-cv8b'], tag2=1, jit=1, jitx=1, jitloop=1, jitinl=1), [], 'founder: s6-cv8b + the tag, the JIT, jitx, jitloop, jitinl', 0)]   # 441: the JIT needs the tag
        f37 = None if NOEVOLVED else recorded_genome('38446e6c09')
        if f37: pop += [get(dict(f37, jitloop=1, jitinl=1), [], "founder: seed 37's fastest (38446e6c09) + jitloop, jitinl", 0)]
        else: print("  founder: seed 37's fastest %s - left out" % ('evolved, and --noevolved' if NOEVOLVED else 'not in results/'), flush=True)
    # Iteration 178: the hybrid's first forms - run-time immediates without pairs
    # (rtimm=2) and the keeping forms (DUP+I, DUP<I) - three mutations from seed
    # 40's smallest, whose fib they take -36% (results/price-hybrid.md): a founder
    # starts there, its record from results/.
    if not FROMZERO:
        # Iteration 188 (the owner: weigh, do not lock out): from the small
        # end's knee, not its extreme - d99e3d9ed9, 1.3% larger than the
        # smallest and 28% faster, the best Q there (the smallest's the worst);
        # the forms push out only HASH and SKIP, compile-time words, where on
        # 903b231e0d (Q 0.63) they would push out (LOOP).
        f40 = None if NOEVOLVED else recorded_genome('d99e3d9ed9')
        if f40: pop += [get(dict(f40, rtimm=2, ops10=['DUP+I', 'DUP<I'] + [w for w in f40.get('ops10', []) if w not in ('DUP+I', 'DUP<I')]), [],
                            "founder: seed 40's small-end knee (d99e3d9ed9) + rtimm=2, DUP+I, DUP<I", 0)]
        else: print("  founder: seed 40's small-end knee %s - left out" % ('evolved, and --noevolved' if NOEVOLVED else 'not in results/'), flush=True)
    # Iteration 46 (the owner): the earlier runs' fronts carried into this one,
    # so what one run found the next starts from - seed 9 lost the fast end
    # seed 8 had (Iteration 45). --carry DB,DB,...: each database's own front,
    # chosen by its own records - speeds of other sessions, some over four
    # workloads, so only to choose; here every one is timed again like any
    # design of the run. Sorted, so a resumed run makes the same first
    # generation; no random draw is spent, so the seed's draws are as before.
    if '--carry' in argv and not FROMZERO:
        carried, have = [], set(pop)
        for path in sorted(p for p in argv[argv.index('--carry') + 1].split(',') if p):
            C = {}
            for l in open(path):
                try: r = json.loads(l)
                except ValueError: continue
                if r.get('status') == 'ok' and r.get('speed') and r.get('size'): C[r['id']] = r
            label = '/'.join(path.split('/')[-4:-3] + path.split('/')[-1:])
            for i in first_front(list(C), C):
                g = canon(require(C[i]['genome']))
                if gid(g) in have: continue
                # re-encoded (--require), it is a new design: this run's, not its origin's
                have.add(gid(g)); carried.append((g, ('tag 2 of %s: %s' if gid(g) != i else 'carried from %s: %s') % (label, i)))
        print('  carried in: %d designs, the fronts of %d databases' % (len(carried), len(argv[argv.index('--carry') + 1].split(','))), flush=True)
        pop += [get(g, [], how, 0) for g, how in carried]
    while len(pop) < N:                 # (from zero, already full)
        g, how = mutate(HUMAN[rnd.choice(list(HUMAN))], rnd)
        pop.append(get(g, [], 'seeded ' + how, 0))
    flush()
    attic = []   # Iteration 188: demoted designs with genes the population lost
    def breed(live, rk, cd, count, gen):   # Iteration 436: one island's children (all of them with one island)
        kids = []
        def pick():
            if attic and rnd.random() < ATTIC_P: return rnd.choice(attic)   # Iteration 188
            a, b = rnd.sample(live, 2) if len(live) > 1 else (live[0], live[0])
            return a if (rk[a], -cd[a]) <= (rk[b], -cd[b]) else b
        for _ in range(count):
            p1, p2 = pick(), pick()
            same = [i for i in live if i != p1 and R[i]['genome']['enc'] == R[p1]['genome']['enc']]
            if same and rnd.random() < 0.8: p2 = rnd.choice(same)   # mostly within the species
            for _try in range(10):
                if rnd.random() < XOVER and p1 != p2:   # Iteration 197: 0.6 before
                    g = crossover(R[p1]['genome'], R[p2]['genome'], rnd); how = 'crossover'; parents = [p1, p2]
                else:
                    g = canon(R[p1]['genome']); how = ''; parents = [p1]
                if rnd.random() < 0.15 and len(live) > 2:
                    donor = rnd.choice([i for i in live + attic if i not in parents])   # the attic's lost genes too
                    g, h = borrow(g, R[donor]['genome'], rnd); how = (how + '; ' if how else '') + h + ' from ' + donor
                    parents = parents + [donor]
                if rnd.random() < 0.9 or gid(g) in seen:
                    g, h = mutate(g, rnd); how = (how + '; ' if how else '') + h
                if gid(g) not in seen: break
            kids.append(get(g, parents, how + ('; via the attic' if set(parents) & set(attic) else ''), gen))
        return kids
    def survive(members, kids, n, qkeep):   # Iteration 436: survival within one island (the population, with one)
        live = [i for i in dict.fromkeys(members + kids) if R[i]['status'] == 'ok']
        order = rank(live, R)[0]
        best_of = [next(i for i in order if R[i]['genome']['enc'] == f) for f in FAMILIES
                   if any(R[i]['genome']['enc'] == f for i in order)]   # no family dies out by crowding
        qbest = sorted((i for i in order if R[i].get('rss')), key=lambda i: qual(R[i]))[:qkeep]   # the knee survives
        return list(dict.fromkeys(best_of + qbest + order))[:max(n, len(best_of) + len(qbest))], order
    def migrants(members):   # Iteration 436: an island's two fastest and its best by Q
        al = [i for i in members if R[i]['status'] == 'ok']
        fast = sorted(al, key=lambda i: R[i].get('speed') or 9e9)[:2]
        return list(dict.fromkeys(fast + sorted((i for i in al if R[i].get('rss')), key=lambda i: qual(R[i]))[:1]))
    isl = []
    for gen in range(1, G + 1):
        if UNTIL and time.time() >= UNTIL:
            print('  the deadline (--until): no generation %d' % gen, flush=True); break
        if ISLANDS[0] <= 1:
            live = [i for i in dict.fromkeys(pop) if R[i]['status'] == 'ok']
            order, rk, cd = rank(live, R)
            print('  generation %d: %d alive, front %d' % (gen, len(live), sum(1 for i in live if rk[i] == 0)), flush=True)
            kids = breed(live, rk, cd, N, gen)
            flush()
            pop, order = survive(pop, kids, N, Q_KEEP)
        else:   # Iteration 436 (results/drafts/escape-mechanism-435.md): islands, each ranked and bred alone
            k = ISLANDS[0]; n = max(2, N // k)
            if not isl: isl = [list(dict.fromkeys(pop))[j::k] for j in range(k)]
            made = []
            for j in range(k):
                live = [i for i in dict.fromkeys(isl[j]) if R[i]['status'] == 'ok'] or [i for i in dict.fromkeys(pop) if R[i]['status'] == 'ok'][:2]
                order, rk, cd = rank(live, R)
                print('  generation %d, island %d: %d alive, front %d' % (gen, j, len(live), sum(1 for i in live if rk[i] == 0)), flush=True)
                made.append(breed(live, rk, cd, n, gen))
            flush()
            pool = list(dict.fromkeys([i for members in isl for i in members] + [i for kids in made for i in kids]))   # for the attic
            for j in range(k): isl[j] = survive(isl[j], made[j], n, max(1, Q_KEEP // k))[0]
            if gen % MIGRATE[0] == 0:   # a ring: each island's migrants join the next, which keeps its best n
                moving = [migrants(isl[j]) for j in range(k)]
                for j in range(k):
                    t = (j + 1) % k
                    isl[t] = survive(isl[t], [i for i in moving[j] if i not in isl[t]], n, max(1, Q_KEEP // k))[0]
                print('  generation %d: migrants %s' % (gen, ' '.join('%d>%d %d' % (j, (j + 1) % k, len(moving[j])) for j in range(k))), flush=True)
            pop = list(dict.fromkeys(i for members in isl for i in members))
            order = rank([i for i in pool if R[i]['status'] == 'ok'], R)[0]   # every candidate, as with one: the demoted reach the attic
        attic = attic_of(order, pop, attic, R) if ATTIC else []
        print('  the attic: %d designs, %d gene values no survivor has' % (len(attic),
              len(set(g for i in attic for g in genes_of(R[i])) - set(g for i in pop for g in genes_of(R[i])))), flush=True)
    if WORKERS[0]: WORKERS[0].close(); WORKERS[0].join()
    report(R)


def nothing_alive(R):
    """What the database holds when no design in it is alive."""
    if not R:
        if not os.path.exists(DB):
            print('%s does not exist: run the evolution first (lab/evolve/RUNNING.md)' % DB)
        elif not LOADED['lines']:
            print('%s is empty (%d bytes): run the evolution first (lab/evolve/RUNNING.md)' % (DB, os.path.getsize(DB)))
        else:
            print('%s has %d lines, and none could be read as a design. The first begins:' % (DB, LOADED['lines']))
            print('  %r' % LOADED['first_bad'])
            print('Each line should be one JSON object, beginning {"id": ... - was the file changed on the way?')
        return
    why = collections.Counter(R[i]['status'] for i in R)
    print('%s holds %d designs, none alive. Causes of death:' % (DB, len(R)))
    for st, k in why.most_common(6): print('  %5d  %s' % (k, st))
    print('If that is not the reach limit or a converter refusal (RUNNING.md), please send the database.')

# Iteration 87 (the owner: a new chat should need no pack): the reports kept
# in results/ carry their front's genomes. The databases stay on the laptop.
GENOMES_NOTE = ('Each design above, and any other the front was measured again with, as one JSON line: its record '
                'without the raw timings. A tool that takes a database (--db) reads this report as one - the lines '
                'that are not JSON are skipped - so results/ is all a new chat needs to rebuild a front design.')
def front_records(R, ids):
    return ['```jsonl'] + [json.dumps({k: v for k, v in R[i].items() if k != 'raw'}, sort_keys=True) for i in ids] + ['```']

def qbest_line(F, R, ref):
    """Iteration 188: the knee named beside the extremes - the design of the
    best Q (binary + image x run time x memory; information, the owner's)."""
    qs = [i for i in F if R[i].get('rss')]
    if not qs: return 'The Q-best design: none (no memory measured).'
    i = min(qs, key=lambda i: qual(R[i])); x = R[i]
    rel = ' - Q %.3f of s6-cv8b\'s' % (qual(x) / qual(ref)) if ref and ref.get('rss') else ''
    return ('The Q-best design (binary + image x run time x memory - the knee; information): %s, speed %.3f, '
            'binary + image %s, memory %d KB%s.' % (i, x['speed'] / (ref['speed'] if ref else 1), format(ov(x, 'total'), ','), x['rss'], rel))

def report(R):
    if any('speed32' in r for r in R.values()): TWO_WIDTHS[0] = True     # Iteration 338: a two-width run's front, four objectives
    ok = [i for i in R if R[i]['status'] == 'ok']
    if not ok: nothing_alive(R); return
    F = first_front(ok, R)
    hum = {R[i]['how'][10:]: i for i in ok if R[i]['how'].startswith('hand-made')}
    ref = R[hum['s6-cv8b']] if 's6-cv8b' in hum else None
    L = ['# Evolved VM designs', '',
         '%d designs evaluated, %d alive%s. Speed is the geometric mean of %s over %s,' %
         (sum(1 for x in R.values() if x['status'] != 'screened'), len(ok),
          ', %d screened - not measured (Iteration 200)' % sum(1 for x in R.values() if x['status'] == 'screened') if any(x['status'] == 'screened' for x in R.values()) else '',
          R[ok[0]].get('unit', ''), ', '.join(WORK_SEL)),
         'relative to s6-cv8b; size is the self-hosting image, binary the stripped engine. %s is held out.' % ', '.join(WORK_HELD),
         'The front is over three objectives, equal (Iteration 75): speed, binary + image, peak memory - memory within %g KB a tie (Iteration 77).' % MEM_TOL, '',
         '', qbest_line(F, R, ref), '',
         '## The Pareto front', '',
         '| design | speed | re-measured | image | binary | binary + image | memory KB | %s (held out) | genes, where they differ from s6-cv8b | how it was made |' % WORK_HELD[0],
         '|---|---|---|---|---|---|---|---|---|---|']
    tw = TWO_WIDTHS[0]                         # Iteration 338: the 32-bit speed beside the speed, when the run has it
    if tw: L[-2] = L[-2].replace('| speed | re-measured |', '| speed | 32-bit speed | re-measured |'); L[-1] += '---|'
    def diff(g):
        if not ref: return ''
        g, r = express(g), express(ref['genome']); out = []
        if g['enc'] != r['enc']: return 'family %s: %s' % (g['enc'], ', '.join('%s=%s' % (k, v) for k, v in g.items()
                                   if k not in ('enc', 'folds', 'spec') and CC0.get(k) != v) or 'as hand-made')
        for k in g:
            if k == 'folds':
                a, b = set(g['folds']) - set(r['folds']), set(r['folds']) - set(g['folds'])
                if a or b: out.append(' '.join(['+' + x for x in sorted(a)] + ['-' + x for x in sorted(b)]))
            elif k == 'supers' and g[k] != r.get(k): out.append('%d pairs: %s' % (len(g[k]), ', '.join(' '.join(x) for x in g[k][:4]) + (', ...' if len(g[k]) > 4 else '')))
            elif g[k] != r.get(k): out.append('%s=%s' % (k, ','.join(g[k]) if isinstance(g[k], list) else g[k]))
        return '; '.join(out) or '(s6-cv8b itself)'
    rm = os.path.join(EV, 'remeasure.json'); rm = json.load(open(rm)) if os.path.exists(rm) else {}
    for i in sorted(F, key=lambda i: R[i]['speed']):
        x = R[i]; rs = x['speed'] / ref['speed'] if ref else 1
        h = WORK_HELD[0]; rl = x['t'][h] / ref['t'][h] if ref and h in x['t'] and h in ref['t'] else float('nan')
        # already a ratio to s6, measured in the same session - possibly on
        # another machine than the run, so not divided by the run's s6
        again = ('%.3f' % rm[i]['speed']) if i in rm else '-'
        bn = format(x['bin'], ',') if x.get('bin') else '-'
        tt = format(x['total'], ',') if x.get('total') else '-'
        rm_ = format(x['rss'], ',') if x.get('rss') else '-'
        L.append(('| %s | %.3f |' + (' %s |' if tw else '') + ' %s | %s | %s | %s | %s | %.3f | %s | %s |') % ((i, rs) + ((('%.3f' % x['speed32']) if x.get('speed32') is not None else '-',) if tw else ()) + (again, format(x['size'], ','), bn, tt, rm_, rl, diff(x['genome']), x['how'][:60])))
    L += ['', '## How the front came about', '']
    for i in sorted(F, key=lambda i: R[i]['speed']):
        chain, j = [], i
        while j in R and R[j]['parents'] and len(chain) < 8:
            chain.append(R[j]['how'][:70]); j = R[j]['parents'][0]
        root = R[j]['how'] if j in R else '?'
        L.append('- `%s`: from %s, then %s' % (i, root, ' / '.join(reversed(chain)) or '(itself)'))
    L += ['', '## The hand-made stages', '', '| stage | speed | size | on the front |', '|---|---|---|---|']
    for n, i in sorted(hum.items()):
        L.append('| %s | %.3f | %d | %s |' % (n, R[i]['speed'] / ref['speed'] if ref else 1, R[i]['size'], 'yes' if i in F else 'no'))
    deaths = {}
    for i in R:
        if R[i]['status'] not in ('ok', 'screened'): deaths[R[i]['status']] = deaths.get(R[i]['status'], 0) + 1
    L += ['', '## Deaths', ''] + ['- %s: %d' % kv for kv in sorted(deaths.items(), key=lambda kv: -kv[1])] + ['']
    scr = [i for i in R if R[i]['status'] == 'screened']; aud = [i for i in ok if 'screened, audited' in R[i].get('how', '')]
    if scr or aud:                                      # Iteration 200
        L += ['## The screen', '', '- not measured, predicted beaten by %d%% in speed and %d%% in binary + image: %d' % (100 * SCREEN_MS, 100 * SCREEN_MT, len(scr)),
              '- audited (one in %d, measured anyway): %d, of them on the front: %d' % (SCREEN_AUDIT, len(aud), sum(1 for i in aud if i in set(F))), '']
    L += ["## The front's genomes", '', GENOMES_NOTE, ''] + front_records(R, sorted(set(F) | {i for i in rm if i in R}, key=lambda i: R[i]['speed'])) + ['']
    open(os.path.join(EV, 'report.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L[6:6 + 3 + len(F)] + L[6 + 3 + len(F):6 + 6 + 2 * len(F)]))
    print('report: %s' % os.path.join(EV, 'report.md'))


if __name__ == '__main__':
    main(sys.argv[1:])
