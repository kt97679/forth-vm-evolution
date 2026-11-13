"""results/drafts/relf-handoff-657.py - the relf handoff made final (Iteration 657): one document for
results/handoff-relf-611.md and its four updates (628, 631, 636, 649), on stdout - results/handoff-relf-657.md.
Each role's row is the newest of those documents that states it - their figures, each from the chain that decided the
role - checked against the records (results/relf-designs-649.md: the ten, their bytes and memory) and designs/README.md's
table; the genes are each design's expression off s6-cv8b's by today's evolver, with the glossary, as
results/drafts/relf-readme-611.py made them (611's lines for the designs kept since compared, on stderr). It asserts what
611 claimed and must still hold: none within 25% of the best in all three classes; the tag on the JIT designs alone.
As the build user (it imports the evolver):
    runuser -u claude -- python3 results/drafts/relf-handoff-657.py > results/handoff-relf-657.md"""
import glob, json, os, re, sys, textwrap
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E

R = 'results/'
DOCS = [611, 628, 631, 636, 649]
SRC = {628: ("seed 89's follow-up", ['followup-roles-seed89.md']),        # where a document's figures were measured,
       631: ("seed 89's follow-up", ['xcheck-seed90.md', 'followup-roles-seed89.md']),   # and its roles' evidence
       636: ("seed 90's follow-up", ['followup-roles-seed90.md']),
       649: ('the final check', ['followup-roles-seed91-final.md'])}
SRC611 = {True: ("seed 86's chains B-D", ['final-pick-chainCD-seed86.md']), False: ("seed 87's follow-up", ['followup-roles-seed87.md'])}
for _, f in list(SRC.values()) + list(SRC611.values()):
    for x in f: assert os.path.exists(R + x), x
cells = lambda l: [c.strip() for c in l.strip().strip('|').split('|')]

rows, order, hist = {}, [], []
for n in DOCS:
    for l in open(R + 'handoff-relf-%d.md' % n):
        c = cells(l) if l.startswith('| ') else None
        if not c or len(c) != 10 or c[0] == 'role': continue
        i, w, jit = c[1].split()[0], re.search(r'\(was (\w+)\)', c[1]), c[8] != 'no - portable'
        assert n == 611 or (c[0] in rows and w and rows[c[0]]['id'] == w.group(1)), (n, c[0])   # an update replaces a holder
        if n == 611: order.append(c[0])
        else: hist.append((n, c[0], i, w.group(1)))
        rows[c[0]] = dict(role=c[0], id=i, doc=n, x64=float(c[2]), x32=float(c[3]), arm=float(c[4].rstrip('*')),
                          b8=int(c[5].replace(',', '')), b4=int(c[6].replace(',', '')), mem=int(c[7]), jit=jit, checks=c[9],
                          src=SRC[n] if n in SRC else SRC611[jit])
assert len(order) == 10 and len(hist) == 6
ROWS = [rows[k] for k in order]

REC = {json.loads(l)['id']: json.loads(l) for l in open(R + 'relf-designs-649.md') if l.startswith('{')}
assert sorted(REC) == sorted(r['id'] for r in ROWS)
T = {c[1]: c for c in (cells(l) for l in open('designs/README.md') if l.startswith('| `')) if len(c) == 9}
for r in ROWS:
    x, c = REC[r['id']], T[r['id']]
    assert (x['total'], x['rss'], r['checks']) == (r['b8'], r['mem'], '9/9 / 9/9'), r['id']
    assert (float(c[3]), float(c[4]), float(c[5].rstrip('*')), int(c[6].replace(',', '')), int(c[7].split()[0]),
            c[8] == 'yes') == (r['x64'], r['x32'], r['arm'], r['b8'], r['mem'], r['jit']), r['id']
    r['target'] = c[0].strip('`')
K = ('x64', 'x32', 'arm'); best = [min(r[k] for r in ROWS) for k in K]
assert not [r for r in ROWS if all(r[k] <= 1.25 * b for k, b in zip(K, best))]

def val(v):
    if v is None: return '-'
    return '%d ops' % len(v) if isinstance(v, list) and len(v) > 3 else ','.join('+'.join(x) if isinstance(x, list) else str(x) for x in v) if isinstance(v, list) else str(v)
s6 = E.express(E.canon(E.HUMAN['s6-cv8b']))
for r in ROWS:
    e = E.express(E.canon(REC[r['id']]['genome']))
    assert bool(e.get('jit')) == r['jit'], r['id']
    r['differs'] = {k: e.get(k) for k in sorted(set(e) | set(s6)) if e.get(k) != s6.get(k)}
    assert (r['differs'].get('tag2') == 1) == r['jit'], r['id']
    r['genes'] = ', '.join('%s=%s' % (k, val(v)) for k, v in sorted(r['differs'].items()))
old = {m.group(1): m.group(2) for m in (re.match(r'- \*\*(\w+)\*\* \(.*?\): (.*)\.$', l.strip()) for l in open(R + 'handoff-relf-611.md')) if m}
for r in ROWS:
    if r['id'] in old:
        a, b = set(old[r['id']].split(', ')), set(r['genes'].split(', '))
        print('611 -> 657 %s: %s' % (r['id'], 'the same' if a == b else 'out %s; in %s' % (sorted(a - b), sorted(b - a))), file=sys.stderr)

G = open('lab/evolve/GENES.md').read().split('\n')
GLOSS = {   # the genes GENES.md has no row for, from what the repository states elsewhere (601, 611)
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
    # 657: the four 611 left to evolve.py, from GENES.md's table, evolve.py's flags, PROGRESS.md (Iteration 71) and engine/vm-lab.c
    'folds': 'which of the 23 foldable primitives get prim;EXIT opcodes, in what order (GENES.md\'s table)',
    'noreorder': '-fno-reorder-blocks, GCC only (build.txt)',
    't2hot': 'the two-bit tag\'s ranking: its hot threshold - 0.02 by default, 0, 0.05 or static (Iteration 71; with the tag)',
    'varslot': 'slot operands (VAR@ and VAR!, the locals opcodes) of variable length - a 15-bit payload in two bytes, 23 bits in three; at 0 a fixed 16 bits (engine/vm-lab.c, VARSLOT)',
}
def doc(g):
    if g in GLOSS: return GLOSS[g]
    for l in G:
        if re.search(r'\(`%s`[:;)]' % re.escape(g), l) and l.startswith('|'):
            c = l.strip('|').split('|')[0].strip(); return c if len(c) <= 260 else c[:257].rsplit(' ', 1)[0] + ' ...'
    return None
def newest(i):   # the newest records file that holds design i
    f = sorted((p for p in glob.glob(R + 'relf-designs-*.md') if any(l.startswith('{"') and json.loads(l)['id'] == i for l in open(p))),
               key=lambda p: int(re.search(r'-(\d+)\.md$', p).group(1)))
    return f[-1] if f else '-'

by = {r['role']: r for r in ROWS}
J = [r for r in ROWS if r['jit']]
N = [by[k] for k in ('fastest portable; fastest portable on x86', 'fastest on ARMv7', 'the knee: fast portable on x86, small')]
x = lambda v: '%.1f-%.1f' % (1 / max(v), 1 / min(v))
kb = lambda v: '%d-%d' % (min(v) // 1000, max(v) // 1000 + 1)
ids = ','.join(r['id'] for r in ROWS); named = ','.join('%s=%s' % (r['target'], r['id']) for r in ROWS)
sm, lm = by['smallest'], by['least memory']
L = ['# Forth designs for relf - the final handoff (Iteration 657)', '',
     '(forth-vm-evolution, Iteration 657: one document for results/handoff-relf-611.md and its four updates - 628, 631, 636',
     'and 649, each changing a role or three - which stay as the history, below. The search is over: the improvement phase',
     'ended by its stopping rule (seed 83), the portable search at Iteration 640, and the final check (641-649) found no',
     'further gain; the code is frozen (656: the last retirements applied - no engine or image byte of these ten changed at',
     'either width). Written by results/drafts/relf-handoff-657.py from those documents, the records and designs/.)', '',
     'Ten designs - the lab\'s final set\'s (21 designs, results/final-set-chainsBCD-seed86.md) and the later runs\' (seeds',
     '87-91, each re-measured on the three machines in a follow-up chain) - chosen so that every criterion\'s winner is here:',
     'no design is best at everything - none comes within 25% of the best on all three machine classes, and the fast designs',
     'are large while the small ones are slow. Every one is the CV8 byte-coded family, built at both cell widths and checked',
     'against the lab\'s hand-made s6-cv8b on the nine workloads it measures.', '',
     '## The designs', '',
     'Speed: CPU time against the hand-made s6-cv8b, the geometric mean over the selection workloads (kernel, fib, corpus,',
     'loop, bubble, ackermann, apps) - lower is faster, 0.185 is 5.4 times s6\'s speed. Each class the geometric mean of its',
     'machines, every session pooled: x86-64 - the laptop (AMD Ryzen 7 PRO 8840HS) and dream (Intel i7-6700) at 8-byte',
     'cells; x86-32 - the same at 4-byte cells; ARMv7 - rage (an NVIDIA Tegra), where a JIT design runs without its JIT (*).',
     'Each row as measured in the chain that decided its role ("measured"; its evidence in the history, below): every role',
     'was taken against its holder in the same sessions, and rows from different chains compare to a few percent. Size: the',
     'stripped engine plus the image, exact. Memory: peak resident, the laptop at 8-byte cells. The `make` target is the',
     'design\'s directory in designs/.', '',
     '| role (`make` target) | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | bytes, 4-byte | memory KB | JIT | checks (8 / 4) | measured |',
     '|---|---|---|---|---|---|---|---|---|---|---|']
for r in ROWS:
    L.append('| %s (`%s`) | %s | %.3f | %.3f | %.3f%s | %s | %s | %d | %s | %s | %s |' % (r['role'], r['target'], r['id'], r['x64'], r['x32'],
             r['arm'], '*' if r['jit'] else '', format(r['b8'], ','), format(r['b4'], ','), r['mem'],
             'x86-64 and x86-32' if r['jit'] else 'no - portable', r['checks'], r['src'][0]))
L += ['', 'The trade in two sentences: the JIT designs are %s times s6\'s speed on x86-64 (%s at 32 bits) in %s KB and %d-%d KB of' % (
      x([r['x64'] for r in J]), x([r['x32'] for r in J]), kb([r['b8'] for r in J]), min(r['mem'] for r in J), max(r['mem'] for r in J)),
      'memory; without the JIT the three fastest portable designs are %s times s6\'s speed on ARMv7 and %s on x86-64 in %s KB,' % (
      x([r['arm'] for r in N]), x([r['x64'] for r in N]), kb([r['b8'] for r in N])),
      'and the smallest and the leanest give up speed for %d KB of engine and image, or %d KB of memory.' % (round(sm['b8'] / 1000), lm['mem']), '',
      'Read the ARMv7 column as a band (649; results/followup-roles-seed91-final.md, "The Tegra between chains"): on the Tegra,',
      'two designs within a few percent of each other do not keep their order from one measuring chain to the next - a pair',
      'swung 4-5% (its kernel moved from 7.3.1 to 7.3.3 between chains). The ARMv7 roles were decided over every session',
      'pooled (629\'s rule): `portable-small` (ae99617f06) and a627b954c6 are interchangeable there, and so are `portable-arm`',
      '(3eb59b271d) and 7fb40ff7ba (-0.94% in the final check).', '',
      '## What each is built from', '',
      'The genes where a design\'s expression differs from s6-cv8b\'s, by the frozen code (lab/evolve/evolve.py; long lists as',
      'their length; GENE=- one s6 has and the design does not). tag2: relf\'s two-bit tag format; compiler 1: clang, else GCC;',
      'opt: the optimisation level, -O2 if absent.', '']
used = set()
for r in ROWS:
    used |= set(r['differs']); L.append('- **%s** (%s, `%s`): %s.' % (r['id'], r['role'], r['target'], r['genes']))
L += ['', '### The genes, as lab/evolve/GENES.md describes them', '']
for g in sorted(used):
    t = doc(g); L.append('- `%s` - %s' % (g, t if t else 'see lab/evolve/evolve.py, `grep -n "gene(\'%s\'" lab/evolve/evolve.py`' % g))
a2, a3 = newest('c2ef9488ff'), newest('64a7345393')
L += ['', '## For relf (RELF.md\'s adoption criteria)', '',
      '- **The JIT is x86 only** (x86-64 and x86-32); relf\'s CV8 stays portable, so the four JIT designs show what x86 reaches',
      '  and the six without it are relf\'s candidates as they stand. The JIT designs\' ARMv7 figures are their JIT-off builds.',
      '- **The images come from the lab\'s converter** (tools/layout.py), not relf\'s cross.4: what relf can take is mechanisms -',
      '  opcodes, fused and specialised forms, the dictionary\'s chains, engine flags - each rebuilt in relf and measured on',
      '  relf\'s own workloads with its tools (tools/relf-ab.sh, relf\'s bench-vm.py), as RELF.md requires. At Iteration 364 the',
      '  C-engine-only flags (clang, -Os, pinned registers) did not transfer to relf\'s cv8.c; the instruction level is the offer.',
      '- **The two-bit tag**: the JIT designs use it (tag2=1), the portable ones do not - their format is CV8 without the tag.',
      '- **Without the C library, and on ARMv7**: each design\'s measured build carries its own small runtime, static; the six',
      '  without the JIT also build with the C library (`make libc`, for any other host) and for ARMv7 without it (`make arm`,',
      '  the build the Tegra measured) - the clang three (portable-fastest, portable-knee, smallest) cross-built, the lab\'s',
      '  bytes, running under qemu-arm (646, 649); the GCC three (portable-arm, portable-small, least-memory) built on the Tegra',
      '  by its own GCC, the lab\'s bytes and running (654: results/rage-designs-654.md).',
      '- **Two former holders, for 8-byte cells on a Zen-class CPU**: there the two x86 machines split - on the owner\'s laptop',
      '  (Ryzen 7 PRO 8840HS) 11a56ff9e4 is 4.4% slower than c2ef9488ff, the knee it replaced (636), and d180351903 3.4% slower',
      '  than 64a7345393, the smallest it replaced (649); both kept for that case, their records in %s' % a2,
      '  and %s.' % a3,
      '- **Not measured here**: relf\'s shell workloads, AArch64 and RISC-V. The lab\'s selection is generic Forth by design (RELF.md,',
      '  the order of the work: phase 2 is seeing how these fit relf).', '',
      '## The files', '',
      '- **designs/** - each design as its engine\'s own C source and a Makefile, with its images (designs/README.md): `make`',
      '  from the repository\'s top builds all ten (8-byte cells, x86-64 Linux, without the C library - the build measured),',
      '  `make test` runs each, `make 32` builds them at 4-byte cells, `make libc` and `make arm` the six without the JIT.',
      '  lab/evolve/export-designs.py, then export-arm.py, write designs/ and check each engine is the lab\'s bytes.',
      '- **The package** forth-vm-evolution-designs-iter649.tar.gz (lab/evolve/pack-designs.py): for each design',
      '  `ID/record.json` (its genome and the lab\'s record) and, at each width, `ID/cell8/` and `ID/cell4/`: `engine` and',
      '  `image.img` (statically linked; run `./engine image.img < program.fth` - names are upper case, `BYE` ends it), `src/`',
      '  (the engine\'s C source as compiled: vm.c and every file generated beside it), `build.txt` (each command the lab\'s',
      '  build ran, in order - the compiler line gives every -D), `check.txt` (the nine workloads against s6-cv8b at the same',
      '  width); `SHA256SUMS` covers every engine and image. Rebuilt byte for byte from the repository, in a built tree:',
      '  `python3 lab/evolve/pack-designs.py OUT results/relf-designs-649.md %s` - its 40 engines and' % ids,
      '  images the checksums of results/drafts/designs-sha256-649.txt, before the freeze and after it (650, 656).',
      '- **The whole build-out**, one command (the freeze\'s; a role changed later goes the same way, with its records):',
      '  `sh results/drafts/freeze-build-645.sh . results/relf-designs-649.md %s` -' % named,
      '  validate, the export against designs/, make test, make 32, make libc, the package (the script\'s header).', '',
      '## The history', '',
      'Each document stays as it was written; this one replaces them. Every role change was the owner\'s decision, on the',
      'evidence named.', '',
      '- 601 - results/handoff-relf-601.md: the first handoff, nine winners of the lab\'s final set (seed 86\'s chains B-D).',
      '- 611 - results/handoff-relf-611.md: ten, with the portable run\'s (seed 87; results/followup-roles-seed87.md) - 782f3ad7ff',
      '  the fastest portable design, a627b954c6 for 22420b3b61 as small and fast on ARMv7, 64a7345393 for cea114f47e as the',
      '  smallest (612).']
for n in DOCS[1:]:
    ch = [h for h in hist if h[0] == n]
    L.append(textwrap.fill('- %d - results/handoff-relf-%d.md: %s (%s; the records results/relf-designs-%d.md).' % (n, n, '; '.join(
             '`%s` to %s (was %s)' % (by[role]['target'], i, w) for _, role, i, w in ch), ', '.join(R + f for f in SRC[n][1]), n),
             120, subsequent_indent='  ', break_on_hyphens=False))
L += ['- 656 - the freeze: the last batch applied on master (results/applied-after-seed91/ORDER.md) - the ten\'s engine and',
      '  image bytes the same at both widths, the build-out the same as designs/ and the package (PROGRESS.md, Iteration 656).',
      '- 657 - this document.', '']
print('\n'.join(L))
