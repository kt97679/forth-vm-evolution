"""results/drafts/relf-handoff-726.py - the relf handoff for the new roles (Iteration 726), on stdout -
results/handoff-relf-726.md: results/drafts/handoff-relf-draft-721.md made final once chain D (725) and the rage check's
second run with portable-fastest's gate (726) had decided its marks. The table is designs/README.md's (chains B and C,
results/drafts/designs-table-718.py), each row checked against the records (results/relf-designs-718.md: the id, the
bytes, the memory, the JIT) and designs/TRANSLATOR-BUILT (which images are the converter's); the genes are each
design's expression off s6-cv8b's by today's evolver, as results/drafts/relf-handoff-657.py made them, with the
glossary (GENES.md, then the lines below for the genes it has no row for). It asserts what 657 claimed and must still
hold: none measured in all three classes within 25 % of the best in each (the Tegra measured one JIT design, without
its JIT). 657's other claim, the two-bit tag on the JIT designs alone, no longer holds: the tag's users are listed. As the build user (it imports
the evolver):
    runuser -u claude -- python3 results/drafts/relf-handoff-726.py > results/handoff-relf-726.md"""
import json, re, sys, textwrap
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E

R = 'results/'
PKG = 'forth-vm-evolution-designs-iter726.tar.gz'
cells = lambda l: [c.strip() for c in l.strip().strip('|').split('|')]
ROWS = []
for l in open('designs/README.md'):
    c = cells(l) if l.startswith('| `') else None
    if not c or len(c) != 9 or c[1] == 'design': continue
    f = lambda s: None if s == '-' else float(s.rstrip('*'))
    ROWS.append(dict(target=c[0].strip('`'), id=c[1], wins=c[2], x64=f(c[3]), x32=f(c[4]), arm=f(c[5]), arms=c[5],
                     b8=int(c[6].replace(',', '')), mem=int(c[7].split()[0]), jit=c[8] == 'yes'))
assert len(ROWS) == 10, len(ROWS)
REC = {json.loads(l)['id']: json.loads(l) for l in open(R + 'relf-designs-718.md') if l.startswith('{')}
assert sorted(REC) == sorted(r['id'] for r in ROWS)
TB = {l.split()[0]: l.split(' ', 1)[1].strip() for l in open('designs/TRANSLATOR-BUILT') if l.strip() and not l.startswith('#')}
assert sorted(TB) == ['fastest-x86-32', 'fastest-x86-64', 'small-jit'], TB
for r in ROWS:
    x = REC[r['id']]
    assert (x['total'], x['rss']) == (r['b8'], r['mem']), (r['id'], x['total'], x['rss'])
    r['image'] = 'translator-built' if r['target'] in TB else 'self-built'
K = ('x64', 'x32', 'arm'); best = {k: min(r[k] for r in ROWS if r[k] is not None) for k in K}
assert not [r for r in ROWS if None not in [r[k] for k in K] and all(r[k] <= 1.25 * best[k] for k in K)]

OLD = {}                                                 # 657's ten by make target, for the history
for l in open(R + 'handoff-relf-657.md'):
    m = re.match(r'\| .*\(`([\w-]+)`\) \| (\w{10}) \|', l)
    if m: OLD[m.group(1)] = m.group(2)
assert sorted(OLD) == sorted(r['target'] for r in ROWS), OLD
changed = [r for r in ROWS if OLD[r['target']] != r['id']]

def val(v):
    if v is None: return '-'
    return '%d ops' % len(v) if isinstance(v, list) and len(v) > 3 else ','.join('+'.join(x) if isinstance(x, list) else str(x) for x in v) if isinstance(v, list) else str(v)
s6 = E.express(E.canon(E.HUMAN['s6-cv8b']))
for r in ROWS:
    e = E.express(E.canon(REC[r['id']]['genome']))
    assert bool(e.get('jit')) == r['jit'], r['id']
    r['differs'] = {k: e.get(k) for k in sorted(set(e) | set(s6)) if e.get(k) != s6.get(k)}
    r['tag2'] = bool(e.get('tag2'))
    r['genes'] = ', '.join('%s=%s' % (k, val(v)) for k, v in sorted(r['differs'].items()))
G = open('lab/evolve/GENES.md').read().split('\n')
GLOSS = {   # 657's, and (726) the genes since that GENES.md has no row for, from evolve.py's gene lines and their results files
    'tos': 'the top of the data stack in a register (GENES.md\'s CV8 table; engine/vm-lab-tos.c)',
    'spec': 'specialised opcode families - var, tiny, small, imm, loc: variables, small literals and immediates as their own opcodes (GENES.md\'s CV8 table, "specialisation families")',
    'supers': 'superinstructions - the pairs listed, each one opcode (tools/gen-super.py)',
    'tag2': 'the two-bit tag image format, relf\'s (FORMAT-TAG2.md)',
    'threads': 'the dictionary in 16, 32, 64 or 128 chains (evolve.py, Iteration 204)',
    'fsys': 'the file words over single system calls, by level (results/drafts/fsys/single-syscall.md; levels 4-5 retired at 599)',
    'guard': 'guard pages around the stacks (GENES.md\'s CV8 table)',
    'd256': 'a 256-entry dispatch table (GENES.md\'s CV8 table)',
    'regpin': 'the VM\'s registers pinned to machine registers (RELF.md, Iteration 364)',
    'opt': 'the optimisation level: O2 (absent), O3 or Os (clang: -Oz)',
    'jit': 'the JIT: hot words translated to x86 machine code from compiled stencils (engine/jit.c, engine/spn-stencils.c; x86 only)',
    'jitimg': 'the image\'s own words JIT candidates (evolve.py, Iteration 341)',
    'jitvar': 'variable fetch and store given JIT stencils (evolve.py, Iteration 342)',
    'rtfuse': 'run-time fusion: the compiler the image carries fuses pairs as the converter does',
    'nogcse': '-fno-gcse, GCC only (the compile line in build.txt)', 'nocrossjump': '-fno-crossjumping, GCC only (build.txt)',
    'nocet': '-fcf-protection=none (build.txt)', 'align1': 'the -falign-*=1 flags, GCC only (build.txt)',
    'folds': 'which of the 23 foldable primitives get prim;EXIT opcodes, in what order (GENES.md\'s table)',
    'noreorder': '-fno-reorder-blocks, GCC only (build.txt)',
    't2hot': 'the two-bit tag\'s ranking: its hot threshold - 0.02 by default, 0, 0.05 or static (Iteration 71; with the tag)',
    'varslot': 'slot operands (VAR@ and VAR!, the locals opcodes) of variable length - a 15-bit payload in two bytes, 23 bits in three; at 0 a fixed 16 bits (engine/vm-lab.c, VARSLOT)',
    'peel': '-fpeel-loops, GCC only (build.txt)', 'tracer': '-ftracer, GCC only (build.txt)', 'ipaclone': '-fipa-cp-clone, GCC only (build.txt)',
    'rtvar': 'a data word\'s @ and ! compiled as one operation (vf, vs) at run time - relf\'s VAR@ and VAR!, DOES> @ among them (forth/cv8-fuse-var.4; results/rtvar-688.md, does-at-695.md)',
    'rtconst': 'a constant compiled as its value at run time - relf\'s rule and test (forth/cv8-fuse-const.4; results/rtconst-691.md)',
    'rtinline': 'a body of at most 3 instructions in 6 bytes copied for its call at run time - relf\'s inlining rule (forth/cv8-fuse-inline.4; results/rtinline-694.md)',
}
def doc(g):
    if g in GLOSS: return GLOSS[g]
    for l in G:
        if re.search(r'\(`%s`[:;)]' % re.escape(g), l) and l.startswith('|'):
            c = l.strip('|').split('|')[0].strip(); return c if len(c) <= 260 else c[:257].rsplit(' ', 1)[0] + ' ...'
    m = re.search(r"^gene\('%s'.*?#\s*(.*)$" % re.escape(g), open('lab/evolve/evolve.py').read(), re.M)
    return (m.group(1) if len(m.group(1)) <= 260 else m.group(1)[:257].rsplit(' ', 1)[0] + ' ...') + ' (evolve.py\'s gene line)' if m else None

ids = ','.join(r['id'] for r in ROWS); named = ','.join('%s=%s' % (r['target'], r['id']) for r in ROWS)
L = ['# Forth designs for relf - the new roles (Iteration 726)', '',
     '(forth-vm-evolution, Iteration 726: results/drafts/handoff-relf-draft-721.md made final - chain D decided the smallest JIT',
     'design and the self-hosting gate (725, results/followup-roles-seed96-jitband.md), the rage check\'s second run and',
     'portable-fastest\'s gate the rest (726, results/rage-designs-726.md). It replaces results/handoff-relf-657.md, which stays',
     'as the history. Written by results/drafts/relf-handoff-726.py from designs/, the records and those documents.)', '',
     '## What changed since the 657 handoff', '',
     '- **The measure** (676-686): the size is the engine, the image and the code the five selection programs lay (sim16, gc16,',
     '  scan, evo, shellmix - relf\'s shellmix.fth the fifth, 686), at 8-byte cells - so the bytes below are not comparable',
     '  with 657\'s (which were the engine and the image only).',
     '- **The search reopened** (677-704): seeds 92-96 with the run-time genes rtvar (a data word\'s @ and ! as one operation,',
     '  relf\'s VAR@ and VAR!), rtconst (a constant compiled as its value - relf\'s rule), rtinline (a body of at most 3',
     '  instructions in 6 bytes copied for its call - relf\'s inlining rule), DOES> @ in rtvar; the unaligned strings and VALUE',
     '  without its kind cell taken for everyone (680-681). The series stopped at seed 96 by its rule.',
     '- **The roles chosen again** (705-725): chains A-D on the laptop, dream and the Tegra - A a screen of 944, B a shortlist',
     '  of 99, C the 66 it could not settle, D the smallest JIT design\'s band (results/followup-roles-seed96-roles.md, -b.md,',
     '  -c.md, followup-roles-seed96-jitband.md); the ten by the rule - 1 % smaller, no machine class 2 % slower, memory within',
     '  8 KB; a speed role\'s challenger 2 % faster at 2 SE - results/new-roles-718.md, with every near design kept on record',
     '  there. %d of the ten changed: %s; %s kept.' % (len(changed), ', '.join('`%s` %s (was %s)' % (r['target'], r['id'], OLD[r['target']]) for r in changed),
                                                  ' and '.join('`%s` %s' % (r['target'], r['id']) for r in ROWS if r not in changed)),
     '- **The images are self-built** (666-726, relf\'s way): forth/cross-cv8.4, a CV8 cross compiler in Forth run by each',
     '  design\'s own engine, writes the design\'s image from source - designs/forth/ (kernel.4, extend.4, cross-cv8.4 and the',
     '  overlays its genes name) and designs/NAME/genes.4; `make selfhost` in a design rebuilds its image byte for byte. Every',
     '  role self-hosts at both widths (722). The gate\'s speed half (lab/evolve/selfhost-speed.py on the laptop: 5',
     '  alternations of 10 rounds, both widths; a self-built image more than 2 %% slower than the translator\'s ships the',
     '  translator\'s): %d self-built; %s translator-built - their self-built images 2.1-4.6 %% slower at one width' % (
         sum(r['image'] == 'self-built' for r in ROWS), ', '.join('`%s`' % t for t in sorted(TB))),
     '  (designs/TRANSLATOR-BUILT gives each), the instructions the same (721): code placement. portable-fastest, self-built',
     '  since 722, passed at 726 (0.997 at 8-byte cells, 0.987 at 4).', '',
     '## The designs', '',
     '| `make` target | design | what it wins | x86-64 | x86-32 | ARMv7 | bytes | memory | JIT | image |',
     '|---|---|---|---|---|---|---|---|---|---|']
for r in ROWS:
    L.append('| `%s` | %s | %s | %s | %s | %s | %s | %d KB | %s | %s |' % (r['target'], r['id'], r['wins'], '%.3f' % r['x64'],
             '%.3f' % r['x32'], r['arms'], format(r['b8'], ','), r['mem'], 'yes' if r['jit'] else 'no', r['image']))
L += ['', 'Speed: CPU time against the hand-made s6-cv8b, the geometric mean over the selection workloads - lower is faster;',
      'each class the geometric mean of its machines over a chain\'s sessions (chain B\'s, or chain C\'s where B lacks a class -',
      'results/drafts/designs-table-718.py): x86-64 the laptop (AMD Ryzen 7 PRO 8840HS) and dream (Intel i7-6700) at 8-byte',
      'cells, x86-32 the same at 4-byte cells, ARMv7 rage (an NVIDIA Tegra). \\* best-all-round on ARMv7 without its JIT; - not',
      'measured there. Bytes: the engine, the image and the five programs\' code, 8-byte cells (the records, results/relf-',
      'designs-718.md). Memory: peak resident, the laptop. Image: what designs/ ships at both widths. The same table:',
      'designs/README.md. Of the seven measured in all three classes, none comes within 25 % of the best in each.', '',
      '## What each is built from', '',
      'The genes where a design\'s expression differs from s6-cv8b\'s, by today\'s evolver (lab/evolve/evolve.py; long lists as',
      'their length; GENE=- one s6 has and the design does not). tag2: relf\'s two-bit tag format; compiler 1: clang, else GCC;',
      'opt: the optimisation level, -O2 if absent. designs/NAME/genes.4 has the same as Forth (lab/evolve/export-genes.py).', '']
used = set()
for r in ROWS:
    used |= set(r['differs']); L.append('- **%s** (`%s`): %s.' % (r['id'], r['target'], r['genes']))
L += ['', '### The genes', '']
for g in sorted(used):
    t = doc(g); L.append('- `%s` - %s' % (g, t if t else 'see lab/evolve/evolve.py, `grep -n "gene(\'%s\'" lab/evolve/evolve.py`' % g))
L += ['', '## For relf (RELF.md\'s adoption criteria) - what still holds from 657, and what is new', '',
      '- **The JIT is x86 only**, as before; the six without it are relf\'s candidates as they stand.',
      '- **New: the images are built relf\'s way** - by a cross compiler in Forth, from source, on the design\'s own engine - so',
      '  what relf takes can now be the source as well as the mechanisms: designs/forth/ and a design\'s genes.4 rebuild its',
      '  image (`make selfhost`); the genes as Forth name each translator rewrite the design uses.',
      '- **New: relf\'s own mechanisms measured in the lab** - rtvar, rtconst and rtinline (relf\'s VAR@/VAR!, constant rule and',
      '  inlining rule; results/mech-prices-684.md, relf-reply-685.md): which of the ten carry them is in their genes above;',
      '  shellmix.fth (relf\'s) is in the size and the speed.',
      '- **The two-bit tag** (relf\'s format, tag2=1): %s; the rest CV8 without the tag.' % ', '.join('`%s`' % r['target'] for r in ROWS if r['tag2']),
      '- **Without the C library and on ARMv7**, as before: `make libc`, `make arm` for the six without the JIT; the clang three',
      '  (portable-fastest, portable-knee, smallest) cross-built, the lab\'s bytes, under qemu-arm (725); the GCC three',
      '  (portable-arm, portable-small, least-memory) built on the Tegra by its own GCC, the lab\'s bytes and running on their',
      '  self-built images (726: results/rage-designs-726.md - engines of 16,782, 13,014 and 11,158 B).',
      '- **Not measured here**, as before: relf\'s shell workloads beyond shellmix, AArch64, RISC-V.', '',
      '## The files and how to fetch them', '',
      '- **designs/** in the repository (the bundle the owner hands over) - what to build from: each design\'s engine source,',
      '  its Makefile, its images (the "image" column) and their source; `make`, `make test`, `make selfhost`, `make 32`, `make',
      '  libc`, `make arm` from the top.',
      '- **The package** %s (lab/evolve/pack-designs.py, as 657\'s; the owner\'s copy, not the repository): for' % PKG,
      '  each design `ID/record.json` and, at each width, `ID/cell8/`, `ID/cell4/` - `engine`, `image.img` (`./engine image.img',
      '  < program.fth`; names upper case, `BYE` ends it), `src/`, `build.txt` (each command the lab\'s build ran), `check.txt`',
      '  (the nine workloads against s6-cv8b at the same width); `SHA256SUMS`. It is the lab\'s measured build: its images are',
      '  the converter\'s (tools/layout.py), so for the seven self-built roles designs/\' images differ from it (smaller; the',
      '  same speed by the gate). Rebuilt byte for byte from the repository, in a built tree:',
      '  `python3 lab/evolve/pack-designs.py OUT results/relf-designs-718.md %s` -' % ids,
      '  its 40 engines and images the checksums of results/drafts/designs-sha256-718.txt (718, and again at 726).',
      '- **The build-out**: `sh results/drafts/roles-build-718.sh 1 . results/relf-designs-718.md NAMES`, the cross GCC\'s',
      '  export-arm.py --gcc, then `... 2 . results/relf-designs-718.md NAMES` (the script\'s header; NAMES',
      '  `%s`); a gate FAIL ships' % named,
      '  translator-built by `TRANSLATOR=\'NAME:REASON\'` in phase 2 (725). A role changed later goes the same way, alone.', '',
      '## The history', '',
      'Each document stays as it was written. 601-657: results/handoff-relf-657.md, "The history". 718: the new roles chosen',
      '(results/new-roles-718.md; the records results/relf-designs-718.md). 721: this document drafted. 725: small-jit',
      'confirmed (chain D) and the gate\'s three shipped translator-built. 726: the rage check passed on the self-built images,',
      'portable-fastest passed the gate - this document.', '']
W = lambda l: l if l.startswith('|') or len(l) <= 120 else textwrap.fill(l, 120, subsequent_indent='  ', break_on_hyphens=False, break_long_words=False)
print('\n'.join(W(l) for l in L))
