#!/usr/bin/env python3
"""evolve.py - evolve VM designs: the faster and the smaller survive.

    lab/evolve/evolve.py --validate            the hand-made stages, rebuilt
                                               from their genomes, must give
                                               the build's images exactly
    lab/evolve/evolve.py [--pop N] [--gens G] [--rounds R] [--seed S]
    lab/evolve/evolve.py --report              report.md from what is known

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
         counters can be read, CPU time otherwise - over kernel, fib, parse
         and corpus, every program loaded from a FILE (standard input would
         measure read() calls, not engines)
  size   bytes of the self-hosting image
loop is HELD OUT: never selected on, reported for the survivors, so a
design tuned to the four does not pass unnoticed.

OPERATORS
  mutation   a gene flipped or nudged; a fold added, removed or swapped
  crossover  two parents mixed gene by gene; folds drawn from both
  borrowing  a whole block - the call path, the header format, the dispatch,
             the folds - transplanted from an unrelated design
  selection  NSGA-II: rank by Pareto front, then by crowding, so designs
             that are different survive beside designs that are better
"""
import collections, hashlib, json, math, os, random, re, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
O = os.path.join(ROOT, 'build'); W = os.path.join(O, 'work')
EV = os.path.join(O, 'evolve'); DB = os.path.join(EV, 'db.jsonl'); CORPUS = os.path.join(EV, 'corpus.fth')
CPUT = os.path.join(O, 'cputime')
HOT = '+,=,!,@,LSHIFT,RSHIFT,C@,C!,AND,OR,XOR,LIT,<,U<,OVER,DROP,DUP,SWAP,ROT,>R,R>,R@,NEGATE'.split(',')
SPECS = ['loc', 'var', 'tiny', 'small', 'imm']
FOLDMAX = 23
# Primitives a fold may never take: control flow and the system's own.
NOFOLD = set('NOOP EXIT BRANCH ?BRANCH EXECUTE BYE SP@ SP! RP@ RP! WRITE READ SYSTEM FORK EXECVE '
             'WAITPID PIPE DUP2 GETENV SETENV UNSETENV CHDIR GETCWD GETPID ALLOCATE FREE RESIZE '
             'GETPWHOME GETFSIZE SETFSIZE SYS-EXIT SYSARGC SYSARG'.split()) | {n for n in []}
PRIMS = [l.split()[1] for l in open(os.path.join(ROOT, 'forth', 'kernel.4')) if l.startswith('PRIMITIVE')]
POOL = [p for p in PRIMS if p not in NOFOLD and 'FILE' not in p and 'LINE' not in p] or HOT
for h in HOT:
    if h not in POOL: POOL.append(h)

# Compiler genes, from gforth's and CPython's builds: a computed-goto
# interpreter loses its point if the compiler merges every dispatch into one
# shared indirect jump (-fno-gcse, -fno-crossjumping); gforth also keeps
# blocks in order and code compact. -fcf-protection=none drops endbr64.
CFLAGS = {'nogcse': '-fno-gcse', 'nocrossjump': '-fno-crossjumping', 'nocet': '-fcf-protection=none',
          'align1': '-falign-labels=1 -falign-jumps=1', 'noreorder': '-fno-reorder-blocks'}
CC0 = dict(opt='O2', nogcse=0, nocrossjump=0, nocet=0, align1=0, noreorder=0)
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
    's5-cv8spec': human('cv8'),
    's6-cv8b':    human('cv8', scale=0, bytehdr=1, doesfar=1),
}
FAMILIES = ['cell', 'sod16', 'cpt16', 'cv8']
# Which genes each family expresses; the rest are carried, not built.
EXPRESSED = {'cell': [], 'sod16': ['skippad'], 'cpt16': ['scale', 'skippad', 'fold', 'folds'],
             'cv8': ['tos', 'scale', 'bytehdr', 'spec', 'sharedcall', 'doesfar', 'varcall',
                     'varslot', 'd256', 'guard', 'folds', 'supers', 'rtfuse', 'ops10', 'escape', 'tail', 'msc']}
BLOCKS = [('sharedcall', 'd256'), ('scale', 'bytehdr', 'doesfar'), ('varcall', 'varslot'),
          ('spec',), ('folds',), ('tos', 'guard'), tuple(CC0), ('skippad', 'fold'), ('supers',), ('folds', 'supers'), ('ops10',), ('ops10', 'supers'), ('escape', 'ops10', 'supers'), ('tail',), ('tail', 'tos'), ('msc',), ('msc', 'tail')]
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
            + (list(range(36, 68)) if g.get('escape') else []))   # ESCAPE moves primitives 36-67 behind a byte
def overlay(g):
    """Does this CV8 design need forth/cv8-fuse.4, the compiler that fuses
    pairs at run time? Only if it has pairs and the rtfuse gene. (Its fold
    list needs no overlay: the converter writes it into cv8.4's FOLD-OPS.)
    Everything else keeps the build's dumps, so the hand-made stages still
    come out byte-identical."""
    return g['enc'] == 'cv8' and bool(supers_in(g) and g.get('rtfuse'))
# relf's format-10 opcodes: kernel colon words given opcodes, where the
# converter finds their compiled body exactly as the engine implements it.
OPS10_POOL = ['EXECUTE', 'I', '(DO)', '+!', '?DUP', 'UNLOOP', 'J', '(LOOP)', '(?DO)', '(+LOOP)', '(LEAVE)',
              '?BRANCH8', 'BRANCH8']   # the short branches: not words, opcodes the converter uses where they fit
OPS10_LABEL = {'+!': 'L_x_plusstore', '?DUP': 'L_x_qdup', 'EXECUTE': 'L_x_execute', 'I': 'L_x_i',
               'J': 'L_x_j', 'UNLOOP': 'L_x_unloop', '(DO)': 'L_x_do', '(LOOP)': 'L_x_loop',
               '(?DO)': 'L_x_qdo', '(+LOOP)': 'L_x_ploop', '(LEAVE)': 'L_x_leave',
               '?BRANCH8': 'L_x_qbr8', 'BRANCH8': 'L_x_br8'}
def ops10_in(g):
    """[[word, opcode], ...]: they take the free slots first, the pairs the rest."""
    return [[w, op] for w, op in zip(g.get('ops10', []), super_slots(g))]
def supers_in(g):
    """[[first, second, opcode], ...] for the pairs that get a slot."""
    return [[a, b, op] for (a, b), op in zip(g['supers'], super_slots(g)[len(ops10_in(g)):])]
WORK_SEL = ['kernel', 'fib', 'parse', 'corpus']; WORK_HELD = ['loop']


def canon(g):
    g = dict(g); g['spec'] = [s for s in SPECS if s in g['spec']]; g['folds'] = list(g['folds'])
    g['supers'] = [list(x) for x in g.get('supers', [])]
    g['ops10'] = list(g.get('ops10', []))
    if g['bytehdr']: g['scale'] = 0   # byte headers never convert with scaled targets: lethal, so not tried
    return g
def express(g):
    """The genes that make the design - its identity. Two genomes that differ
    only in dormant genes build the same design, and are measured once."""
    g = canon(g); e = {k: g[k] for k in ['enc'] + list(CC0) + EXPRESSED[g['enc']]}
    if g['enc'] == 'cpt16' and not g['fold']: e.pop('folds')
    if 'supers' in e: e['supers'] = [x[:2] for x in supers_in(g)]   # only the pairs that got a slot
    if 'ops10' in e: e['ops10'] = [x[0] for x in ops10_in(g)]
    if 'rtfuse' in e and not e.get('supers'): e.pop('rtfuse')        # nothing to fuse at run time
    if e.get('varcall'): e.pop('sharedcall', None)                     # forced on: see build()
    elif 'varcall' in e: e.pop('doesfar', None)                        # forced off: see build()
    if 'msc' in e and not g['tos']: e.pop('msc')                       # made from the cached engine only
    if e.get('msc'):                                                   # its own tables; tail calls excluded
        e.pop('d256', None); e.pop('sharedcall', None); e.pop('tail', None)
    if 'tail' in e and not g['tos']: e.pop('tail')                     # made from the cached engine only
    if e.get('tail'):                                                  # one call function, 256-entry table
        e.pop('d256', None); e.pop('sharedcall', None)
    return e
def gid(g):
    return hashlib.sha1(json.dumps(express(g), sort_keys=True).encode()).hexdigest()[:10]


# ---- building and testing one design ------------------------------------
def _contain(cpu):
    """In the child: a CPU-time limit - SIGXCPU at cpu seconds."""
    import resource
    def f(): resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 2))
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
    p = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.PIPE if inp is not None else subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, preexec_fn=_contain(cpu), env=env)
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

def ccflags(g):
    return ['-' + g['opt']] + [w for k, f in CFLAGS.items() if g[k] for w in f.split()]

def tail_offenders(eng):
    """Handlers whose machine code CALLS through an indexed table - a
    dispatch the compiler did not make a jump, which would grow the C
    stack by a frame each time it runs."""
    out = sh(['objdump', '-d', '--no-show-raw-insn', eng]).stdout.decode(errors='replace')
    fn, bad = None, set()
    for line in out.splitlines():
        m = re.match(r'^[0-9a-f]+ <([^>]+)>:', line)
        if m: fn = m.group(1); continue
        if fn and re.match(r'[HI]_', fn) and re.search(r'call +\*\(%\w+,%\w+,8\)', line):
            bad.add(re.sub(r'^[HI]_', '', fn).split('.')[0])
    return bad

def build_tail(g, d, src, flags, eng):
    """Tail-call threading (tools/gen-tail.py): preprocess this design's
    engine with the 256-entry dispatch, make every handler a function, and
    wrap the ones whose dispatch the compiler would not make a jump - read
    from the machine code, then checked again: none may be left."""
    pp, tc = os.path.join(d, 'pp.c'), os.path.join(d, 'tail.c')
    fl = [f for f in flags if not f.startswith(('-DDISPATCH256', '-DSHAREDCALL'))] + ['-DDISPATCH256=1', '-DSHAREDCALL=1']
    if sh(['cc', '-E', '-P'] + fl + ['-o', pp, src]).returncode: raise RuntimeError('died: engine did not compile')
    wrap = []
    for attempt in range(2):
        r = sh(['python3', os.path.join(ROOT, 'tools', 'gen-tail.py'), pp, tc] + (['--wrap', ','.join(sorted(wrap))] if wrap else []))
        if r.returncode: raise RuntimeError('died: tail-call generation')
        if sh(['cc'] + ccflags(g) + ['-w', '-o', eng, tc]).returncode: raise RuntimeError('died: engine did not compile')
        bad = tail_offenders(eng)
        if not bad: return
        wrap = sorted(set(wrap) | bad)
    raise RuntimeError('died: tail calls not jumps (%s)' % ','.join(sorted(bad)))

PROFILING = [False]      # set while design_pairs builds a profiling engine
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
        if g.get('escape'): i = op if op < 32 else op + 1 if op < 36 else None
        else: i = op if op < 68 else None
        return prims[i] if i is not None and i < 33 and prims[i] not in PAIRS_BAD else None
    d = os.path.join(EV, 'profile'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    PROFILING[0] = True
    try:
        eng, img = build(dict(g, tail=0, msc=0), d)     # the stream, not the dispatch, decides the pairs
        pw = private_work(d); share = collections.Counter()
        for w in WORK_SEL:
            pf = os.path.join(d, 'prof-' + w)
            sh([eng, img], cwd=pw, inp=program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
            c, total = collections.Counter(), 0
            for line in open(pf):
                m = re.match(r'^(\d+) (\d+) (\d+)$', line)
                if m:
                    a, b, k = map(int, m.groups()); total += k
                    if a < 128 and b < 128 and prim(a) and prim(b): c[(prim(a), prim(b))] += k
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

def why(r):
    """The last line a failed tool printed, for the record."""
    lines = [l for l in (r.stderr or b'').decode(errors='replace').splitlines() + (r.stdout or b'').decode(errors='replace').splitlines() if l.strip()]
    err = [l for l in lines if 'rror' in l or 'ssert' in l] or lines
    return (' (%s)' % err[-1].strip()[:120]) if err else ' (exit %d)' % r.returncode

def retried(cmd, **kw):
    """A build step, tried a second time before it kills the design: the
    VM rehearsal lost 31 designs to conversions that failed once and
    succeeded when repeated, cause unrecorded."""
    r = sh(cmd, **kw)
    return sh(cmd, **kw) if r.returncode else r

def build(g, d):
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
                 ('d256', '-DDISPATCH256=1'), ('guard', '-DGUARD=1')):
        if eff[k]: flags.append(f)
    if g['spec']: flags.append('-DSPEC=1')
    if PROFILING[0]: flags.append('-DPROFILE=1')
    if g.get('escape'): flags.append('-DESCAPE=1')
    o10 = ops10_in(g)
    if o10:
        json.dump(o10, open(os.path.join(d, 'ops10.json'), 'w'))
        open(os.path.join(os.path.dirname(src), 'vm-ops10-table.h'), 'w').write(
            ''.join('[%d] = &&%s,\n' % (op, OPS10_LABEL[w]) for w, op in o10 if not 36 <= op < 68))
        open(os.path.join(os.path.dirname(src), 'vm-ops10-esc.h'), 'w').write(     # the band ESCAPE frees
            ''.join('cv8_tab[%d] = &&%s;\n' % (op, OPS10_LABEL[w]) for w, op in o10 if 36 <= op < 68))
        flags.append('-DOPS10=1')
    sup = supers_in(g)
    if sup:
        json.dump(sup, open(os.path.join(d, 'supers.json'), 'w'))
        if sh(['python3', os.path.join(ROOT, 'tools', 'gen-super.py'), src, os.path.join(d, 'supers.json')]).returncode:
            raise RuntimeError('died: superinstruction generation')
        flags.append('-DSUPER=1')
    if g.get('msc') and g['tos']:           # multi-state stack caching (tools/gen-msc.py)
        if sh(['python3', os.path.join(ROOT, 'tools', 'gen-msc.py'), src]).returncode:
            raise RuntimeError('died: multi-state generation')
        flags = [f for f in flags if not f.startswith(('-DDISPATCH256', '-DSHAREDCALL'))] + ['-DDISPATCH256=1', '-DSHAREDCALL=1']
    eng = os.path.join(d, 'engine')
    if g.get('tail') and g['tos'] and not g.get('msc'): build_tail(g, d, src, flags, eng)
    else:
        r = retried(['cc'] + ccflags(g) + flags + ['-o', eng, src])
        if r.returncode: raise RuntimeError('died: engine did not compile' + why(r))
    opts = ['--v8', '--cpt', str(g['scale']), '--dataprims', '--fold', '--fold-set', folds, '--cv8-compiler']
    if g['bytehdr']: opts.append('--bytehdr')
    if g.get('escape'): opts.append('--escape')
    opts.append('--set-compiler-vars')       # the image's compiler follows THIS design's scale and DOES> form
    if g['doesfar'] and g['varcall']: opts.append('--does-far')   # see build(): far DOES> needs VARCALL
    if g['spec']: opts += ['--spec', ','.join(canon(g)['spec'])]
    if not g['varcall']: opts.append('--no-varcall')
    if not g['varslot']: opts.append('--no-varslot')
    if sup: opts += ['--supers-file', os.path.join(d, 'supers.json')]
    if o10: opts += ['--ops10-file', os.path.join(d, 'ops10.json')]
    if sup and g['rtfuse']: opts.append('--rtfuse')
    img = os.path.join(d, 'image.img')
    fuse = '-fuse' if overlay(g) else ''
    dump = os.path.join(O, ('k64-b%s.txt' if g['bytehdr'] else 'k64-self%s.txt') % fuse)
    r = retried(['python3', os.path.join(ROOT, 'tools', 'layout.py'), dump, '8'] + opts + ['--emit-image', img], cwd=W)
    if r.returncode or not os.path.exists(img):
        raise RuntimeError('died: image did not convert' + (why(r) if r.returncode else ' (exit 0, no image written)'))
    return eng, img

def build_other(g, d):
    """The cell engine (relf.c, its image as built), SOD16 and CPT16."""
    eng = os.path.join(d, 'engine'); img = os.path.join(d, 'image.img')
    if g['enc'] == 'cell':
        if sh(['cc'] + ccflags(g) + ['-Wall', '-o', eng, os.path.join(ROOT, 'engine', 'relf.c')]).returncode:
            raise RuntimeError('died: engine did not compile')
        shutil.copy(os.path.join(O, 's0-cell-s64.img'), img); return eng, img
    src = os.path.join(d, 'vm.c'); shutil.copy(os.path.join(O, 'vm-lab.c'), src)
    if g['enc'] == 'sod16':
        flags = ['-DENC=1', '-DREG=1', '-DSCALE=1'] + (['-DSKIPPAD=1'] if g['skippad'] else [])
        dump, opts = 'k64-s16.txt', (['--skip-pad'] if g['skippad'] else []) + ['--compiler-overlay', '16']
    else:
        sc = max(1, g['scale'])
        flags = ['-DENC=2', '-DREG=1', '-DSCALE=%d' % sc] + (['-DSKIPPAD=1'] if g['skippad'] else [])
        dump, opts = 'k64-cpt.txt', ['--cpt', str(sc)] + (['--skip-pad'] if g['skippad'] else [])
        if g['fold']:
            folds = ','.join(g['folds'])
            if sh(['python3', os.path.join(ROOT, 'tools', 'gen-fold.py'), src, folds]).returncode:
                raise RuntimeError('died: fold generation')
            flags.append('-DFOLD=1'); opts += ['--dataprims', '--fold', '--fold-set', folds]
        opts += ['--compiler-overlay', '16']
    if sh(['cc'] + ccflags(g) + flags + ['-o', eng, src]).returncode:
        raise RuntimeError('died: engine did not compile')
    r = retried(['python3', os.path.join(ROOT, 'tools', 'layout.py'), os.path.join(O, dump), '8'] + opts + ['--emit-image', img], cwd=W)
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
def program(w):
    if w == 'kernel': return KERNEL_IN
    path = os.path.join(ROOT, 'bench', w + '.fth') if w != 'corpus' else CORPUS
    return ('S" %s" INCLUDED\nBYE\n' % path).encode()

def alive(eng, img, pw):
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

METRIC = rb'^CYCLES (\d+)' if os.environ.get('EVOLVE_METRIC') == 'cycles' else rb'^CPUNS (\d+)'
PIN, REF = [], None            # set by setup(): the core, the reference (eng, img, work dir)
def run_metric(eng, img, pw, w):
    """One timed run: the process's own CPU time (user + system, from
    getrusage of the child - tools/cputime.c), not wall time, so other
    processes on the machine do not count against it."""
    r = sh(PIN + [CPUT, eng, img], cwd=pw, inp=program(w), timeout=240, cpu=10)
    m = re.search(METRIC, r.stderr, re.M) or re.search(rb'^CPUNS (\d+)', r.stderr, re.M)
    return int(m.group(1))
def measure(eng, img, pw, works, rounds):
    """Best (minimum) CPU time per workload over the rounds, the design and
    the reference - hand-made s6 - run back to back in every round,
    alternating which goes first. Returns design / reference per workload,
    and the design's own times: a ratio of two runs minutes apart, so
    drift in background load or clock speed over a run of hours cancels."""
    best, ref = {}, {}
    for r_ in range(rounds):
        for w in works:
            pair = [(eng, img, pw, best), REF + (ref,)]
            for e, i, p, store in (pair if r_ % 2 == 0 else pair[::-1]):
                store[w] = min(store.get(w, 1 << 62), run_metric(e, i, p, w))
    return {w: best[w] / ref[w] for w in works}, best

def evaluate(g, rounds, keep=False):
    d = os.path.join(EV, 'ind-' + gid(g)); rec = {'status': 'ok'}
    try:
        eng, img = build(g, d)
        rec['size'] = os.path.getsize(img)
        pw = private_work(d)
        alive(eng, img, pw)
        t, raw = measure(eng, img, pw, WORK_SEL + WORK_HELD, rounds)
        rec['t'] = t; rec['raw'] = raw
        rec['speed'] = math.exp(sum(math.log(t[w]) for w in WORK_SEL) / len(WORK_SEL))
        rec['unit'] = UNIT
    except RuntimeError as e:
        rec['status'] = str(e)
    except subprocess.TimeoutExpired:
        rec['status'] = 'died: timed out'
    if not keep: shutil.rmtree(d, ignore_errors=True)
    return rec


# ---- variation -------------------------------------------------------------
def mutate(g, rnd):
    g = canon(g); what = []
    for _ in range(rnd.choice([1, 1, 2])):
        k = rnd.choice(EXPRESSED[g['enc']] + list(CC0) + ['enc'] * (1 if rnd.random() < 0.2 else 0))
        if k == 'enc':
            g['enc'] = rnd.choice([f for f in FAMILIES if f != g['enc']]); what.append('family %s' % g['enc'])
        elif k == 'opt':
            g['opt'] = rnd.choice([o for o in ('O2', 'O3', 'Os') if o != g['opt']]); what.append('-' + g['opt'])
        elif k == 'scale':
            g['scale'] = rnd.choice([s for s in range(4) if s != g['scale']]); what.append('scale=%d' % g['scale'])
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
    return g, 'mutation: ' + ', '.join(what or ['(none)'])

def crossover(a, b, rnd):
    c = {}
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
        else:
            c[k] = a[k] if rnd.random() < 0.5 else b[k]
    return canon(c)

def borrow(g, donor, rnd):
    blk = rnd.choice(BLOCKS); g = canon(g)
    for k in blk: g[k] = canon(donor)[k]
    return g, 'borrowed %s' % '+'.join(blk)


# ---- selection: NSGA-II on (speed, size) -------------------------------------
def fronts(ids, R):
    # Lists, not sets: a set of ids iterates in an order that changes with
    # each process's string hashing, the fronts would come out in another
    # order, and a resumed run would pick different parents and fork.
    dom = {i: [] for i in ids}; n = {i: 0 for i in ids}
    def better(x, y):
        a, b = R[x], R[y]
        return a['speed'] <= b['speed'] and a['size'] <= b['size'] and (a['speed'] < b['speed'] or a['size'] < b['size'])
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
    return F[:-1]

def crowding(front, R):
    cd = {i: 0.0 for i in front}
    for k in ('speed', 'size'):
        s = sorted(front, key=lambda i: R[i][k]); lo, hi = R[s[0]][k], R[s[-1]][k]
        cd[s[0]] = cd[s[-1]] = float('inf')
        for j in range(1, len(s) - 1):
            cd[s[j]] += (R[s[j + 1]][k] - R[s[j - 1]][k]) / ((hi - lo) or 1)
    return cd

def rank(ids, R):
    order, rk, cdist = [], {}, {}
    for r, f in enumerate(fronts(ids, R)):
        c = crowding(f, R)
        for i in f: rk[i] = r; cdist[i] = c[i]
        order += sorted(f, key=lambda i: -c[i])
    return order, rk, cdist


# ---- the database ----------------------------------------------------------
def load():
    """The designs evaluated so far. A run killed while writing leaves a
    truncated last line: skipped, and that design is evaluated again."""
    R = {}
    if os.path.exists(DB):
        for l in open(DB):
            try: r = json.loads(l)
            except ValueError: continue
            R[r['id']] = r
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

def setup():
    global REF_CORPUS, KREF, UNIT, POOL
    for need in (CPUT, os.path.join(O, 'k64-self.txt'), os.path.join(O, 'vm-lab-tos.c')):
        if not os.path.exists(need): sys.exit('%s missing: run tools/build-stages.sh first' % need)
    # The CV8 compiler with table-driven folds and run-time fusion
    # (forth/cv8-fuse.4), dumped the way tools/build-stages.sh dumps cv8.4.
    import shutil
    W = os.path.join(O, 'work'); src4, dst4 = os.path.join(ROOT, 'forth', 'cv8-fuse.4'), os.path.join(W, 'cv8-fuse.4')
    if not (os.path.exists(dst4) and os.path.samefile(src4, dst4)): shutil.copy(src4, dst4)   # a fresh build links it
    for name, files in (('k64-self-fuse.txt', ['cv8.4']), ('k64-b-fuse.txt', ['cv8.4', 'cv8b.4'])):
        boot = ''.join('S" %s" INCLUDED\n' % f for f in files + ['cv8-fuse.4', 'dict-dump-addr.4']) + 'BYE\n'
        out = subprocess.run([os.path.join(O, 's0-cell-64'), 'kernel.img'], input=boot.encode(), cwd=W, capture_output=True).stdout
        open(os.path.join(O, name), 'wb').write(out.replace(b'\r', b''))
    os.makedirs(EV, exist_ok=True)
    # The corpus as tools/run-tests.sh feeds it, written here so a fresh
    # build is enough: the CORE tests, then a sentinel that proves the end.
    with open(CORPUS, 'wb') as f:
        f.write(open(os.path.join(ROOT, 'tests', 'corpus', 'core.fth'), 'rb').read())
        f.write(b'\nS" CORPUS-REACHED-END" TYPE CR\nBYE\n')
    KREF = os.path.join(EV, 'kernel-ref.img'); shutil.copy(os.path.join(W, 'kernel.img'), KREF)
    with open(CORPUS, 'rb') as f:
        REF_CORPUS = sh([os.path.join(O, 's0-cell-64'), os.path.join(O, 's0-cell-s64.img')], cwd=W, inp=f.read()).stdout
    UNIT = ('cycles' if os.environ.get('EVOLVE_METRIC') == 'cycles' else 'cpu time') + ' / hand-made s6'
    PIN[:] = quiet_cpu()
    # the reference every measurement is paired with: hand-made s6
    global REF
    rd = os.path.join(EV, 'reference'); shutil.rmtree(rd, ignore_errors=True); os.makedirs(rd)
    re_, ri = build(canon(HUMAN['s6-cv8b']), rd); rp = private_work(rd)
    REF = (re_, ri, rp)
    POOL = foldable()


def main(argv):
    def opt(name, default):
        return type(default)(argv[argv.index(name) + 1]) if name in argv else default
    setup()
    if '--validate' in argv:
        ok = True
        for name, g in HUMAN.items():
            d = os.path.join(EV, 'validate-' + name)
            try:
                eng, img = build(g, d)
                same = open(img, 'rb').read() == open(os.path.join(O, name + '-s64.img'), 'rb').read()
                pw = private_work(d); alive(eng, img, pw)
                print('  %-11s image %s the build\'s, corpus and kernel workload correct' % (name, 'IDENTICAL to' if same else 'DIFFERENT from'))
                ok &= same
            except RuntimeError as e:
                print('  %-11s %s' % (name, e)); ok = False
            shutil.rmtree(d, ignore_errors=True)
        sys.exit(0 if ok else 1)
    if '--report' in argv:
        report(load()); return
    if '--remeasure' in argv:
        # The front, measured again with more rounds: chosen as the best of
        # many noisy measurements, its designs were partly chosen for luck.
        # In the VM rehearsal they came out 3-6% slower when re-measured.
        R = load(); ok = [i for i in R if R[i]['status'] == 'ok']
        if not ok: nothing_alive(R); sys.exit(1)
        F = fronts(ok, R)[0]; n = opt('--remeasure', 6); out = {}
        path = os.path.join(EV, 'remeasure.json')
        if os.path.exists(path): out = json.load(open(path))
        for i in sorted(F, key=lambda i: R[i]['speed']):
            r = evaluate(canon(R[i]['genome']), n)
            if r['status'] == 'ok': out[i] = {'speed': r['speed'], 't': r['t'], 'rounds': n}
            print('  %s: in the run %.3f, re-measured %s' % (i, R[i]['speed'], ('%.3f' % r['speed']) if r['status'] == 'ok' else r['status']), flush=True)
            json.dump(out, open(path, 'w'))
        report(R); return
    N, G, ROUNDS, rnd = opt('--pop', 16), opt('--gens', 10), opt('--rounds', 3), random.Random(opt('--seed', 1))
    R = load()
    # The designs THIS run has asked for so far. Its decisions must not look
    # at the whole database: resumed, it replays from there, and the
    # database already holds what the first attempt made later - the
    # replay would make different children and fork instead of resuming.
    seen = set()
    def get(g, parents, how, gen):
        i = gid(g); seen.add(i)
        if i not in R:
            t0 = time.time(); rec = evaluate(g, ROUNDS)
            rec.update(id=i, genome=canon(g), parents=parents, how=how, gen=gen, secs=round(time.time() - t0, 1))
            R[i] = rec; save(rec)
            print('    %s %-24s %s' % (i, rec['status'] if rec['status'] != 'ok' else
                  'speed %.4g size %d' % (rec['speed'], rec['size']), how[:70]), flush=True)
        return i
    pop = [get(g, [], 'hand-made ' + n, 0) for n, g in HUMAN.items()]
    # Founders carrying superinstructions, so the gene enters with a population
    # behind it rather than waiting on one mutation in seventeen.
    pop += [get(dict(HUMAN['s4-cv8'], supers=SUPER_POOL[:24], rtfuse=1), [], 'founder: s4-cv8 + 24 pairs, run-time fusion', 0),
            get(dict(HUMAN['s6-cv8b'], supers=SUPER_POOL[:2]), [], 'founder: s6-cv8b + 2 pairs', 0),
            get(dict(HUMAN['s6-cv8b'], supers=SUPER_POOL[:2], rtfuse=1), [], 'founder: s6-cv8b + 2 pairs, run-time fusion', 0),
            get(dict(HUMAN['s4-cv8'], ops10=list(OPS10_POOL), supers=SUPER_POOL[:20]), [], 'founder: s4-cv8 + format-10 opcodes + 20 pairs', 0),
            get(dict(HUMAN['s6-cv8b'], ops10=OPS10_POOL[:2]), [], 'founder: s6-cv8b + EXECUTE, I as opcodes', 0),
            get(dict(HUMAN['s6-cv8b'], escape=1, ops10=list(OPS10_POOL), supers=list(SUPER_POOL)), [], 'founder: s6-cv8b + escape, 7 words, 24 pairs', 0)]
    while len(pop) < N:
        g, how = mutate(HUMAN[rnd.choice(list(HUMAN))], rnd)
        pop.append(get(g, [], 'seeded ' + how, 0))
    for gen in range(1, G + 1):
        live = [i for i in dict.fromkeys(pop) if R[i]['status'] == 'ok']
        order, rk, cd = rank(live, R)
        def pick():
            a, b = rnd.sample(live, 2) if len(live) > 1 else (live[0], live[0])
            return a if (rk[a], -cd[a]) <= (rk[b], -cd[b]) else b
        kids = []
        print('  generation %d: %d alive, front %d' % (gen, len(live), sum(1 for i in live if rk[i] == 0)), flush=True)
        for _ in range(N):
            p1, p2 = pick(), pick()
            same = [i for i in live if i != p1 and R[i]['genome']['enc'] == R[p1]['genome']['enc']]
            if same and rnd.random() < 0.8: p2 = rnd.choice(same)   # mostly within the species
            for _try in range(10):
                if rnd.random() < 0.6 and p1 != p2:
                    g = crossover(R[p1]['genome'], R[p2]['genome'], rnd); how = 'crossover'; parents = [p1, p2]
                else:
                    g = canon(R[p1]['genome']); how = ''; parents = [p1]
                if rnd.random() < 0.15 and len(live) > 2:
                    donor = rnd.choice([i for i in live if i not in parents])
                    g, h = borrow(g, R[donor]['genome'], rnd); how = (how + '; ' if how else '') + h + ' from ' + donor
                    parents = parents + [donor]
                if rnd.random() < 0.9 or gid(g) in seen:
                    g, h = mutate(g, rnd); how = (how + '; ' if how else '') + h
                if gid(g) not in seen: break
            kids.append(get(g, parents, how, gen))
        live = [i for i in dict.fromkeys(pop + kids) if R[i]['status'] == 'ok']
        order = rank(live, R)[0]
        best_of = [next(i for i in order if R[i]['genome']['enc'] == f) for f in FAMILIES
                   if any(R[i]['genome']['enc'] == f for i in order)]   # no family dies out by crowding
        pop = list(dict.fromkeys(best_of + order))[:max(N, len(best_of))]
    report(R)


def nothing_alive(R):
    """What the database holds when no design in it is alive."""
    if not R:
        print('%s holds no designs: run the evolution first (lab/evolve/RUNNING.md)' % DB)
        return
    why = collections.Counter(R[i]['status'] for i in R)
    print('%s holds %d designs, none alive. Causes of death:' % (DB, len(R)))
    for st, k in why.most_common(6): print('  %5d  %s' % (k, st))
    print('If that is not the reach limit or a converter refusal (RUNNING.md), please send the database.')

def report(R):
    ok = [i for i in R if R[i]['status'] == 'ok']
    if not ok: nothing_alive(R); return
    F = fronts(ok, R)[0]
    hum = {R[i]['how'][10:]: i for i in ok if R[i]['how'].startswith('hand-made')}
    ref = R[hum['s6-cv8b']] if 's6-cv8b' in hum else None
    L = ['# Evolved VM designs', '',
         '%d designs evaluated, %d alive. Speed is the geometric mean of %s over %s,' %
         (len(R), len(ok), R[ok[0]].get('unit', ''), ', '.join(WORK_SEL)),
         'relative to s6-cv8b; size is the self-hosting image. loop is held out.', '',
         '## The Pareto front', '',
         '| design | speed | re-measured | size | loop (held out) | genes, where they differ from s6-cv8b | how it was made |',
         '|---|---|---|---|---|---|---|']
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
        x = R[i]; rs = x['speed'] / ref['speed'] if ref else 1; rl = x['t']['loop'] / ref['t']['loop'] if ref else 1
        again = ('%.3f' % (rm[i]['speed'] / ref['speed'] if ref else rm[i]['speed'])) if i in rm else '-'
        L.append('| %s | %.3f | %s | %d | %.3f | %s | %s |' % (i, rs, again, x['size'], rl, diff(x['genome']), x['how'][:60]))
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
        if R[i]['status'] != 'ok': deaths[R[i]['status']] = deaths.get(R[i]['status'], 0) + 1
    L += ['', '## Deaths', ''] + ['- %s: %d' % kv for kv in sorted(deaths.items(), key=lambda kv: -kv[1])] + ['']
    open(os.path.join(EV, 'report.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L[6:6 + 3 + len(F)] + L[6 + 3 + len(F):6 + 6 + 2 * len(F)]))
    print('report: %s' % os.path.join(EV, 'report.md'))


if __name__ == '__main__':
    main(sys.argv[1:])
