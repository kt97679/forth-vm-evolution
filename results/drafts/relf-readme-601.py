"""results/drafts/relf-readme-601.py ROWS.jsonl PACKDIR - the README of the designs packed for relf (Iteration 601):
ROWS.jsonl from results/drafts/relf-handoff-601.py --json (the 21, each across machines), PACKDIR from
lab/evolve/pack-designs.py (each design's check.txt and sizes at both widths). Writes PACKDIR/README.md; the same text
is results/handoff-relf-601.md. The roles, the notes for relf: this file's text; the numbers: the rows and the pack."""
import json, os, re, sys
rows = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[1])}; P = sys.argv[2]
ROLES = [('c7c35f9c97', 'fastest on x86-64'), ('4ef851fd8e', 'fastest on x86-32'), ('06b188f45b', 'best all-round (the best mean of the three classes)'),
         ('bac37f35a2', 'smallest of the JIT designs'), ('690981ca5b', 'fastest portable; fastest on ARMv7'),
         ('c2ef9488ff', 'the knee: fastest portable on x86, small'), ('22420b3b61', 'small, fast on ARMv7'),
         ('fb0d57c8a2', 'least memory'), ('cea114f47e', 'smallest')]
G = open('lab/evolve/GENES.md').read().split('\n')
GLOSS = {   # the genes GENES.md has no row for, from what the repository states elsewhere (601)
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
}
def doc(g):
    if g in GLOSS: return GLOSS[g]
    for l in G:
        if re.search(r'\(`%s`[:;)]' % re.escape(g), l) and l.startswith('|'):
            c = l.strip('|').split('|')[0].strip(); return c if len(c) <= 260 else c[:257].rsplit(' ', 1)[0] + ' ...'
    return None
def val(v):
    if v is None: return '-'
    return '%d ops' % len(v) if isinstance(v, list) and len(v) > 3 else ','.join('+'.join(x) if isinstance(x, list) else str(x) for x in v) if isinstance(v, list) else str(v)
def size(i, c):
    d = os.path.join(P, i, 'cell%d' % c); return os.path.getsize(os.path.join(d, 'engine')) + os.path.getsize(os.path.join(d, 'image.img'))
def ok(i, c): t = open(os.path.join(P, i, 'cell%d' % c, 'check.txt')).read(); return '%d/9' % t.count(' right')
L = ['# Forth designs for relf - the winners of forth-vm-evolution\'s search (Iteration 601)', '',
     'Nine designs from the lab\'s final set (21 designs, results/final-set-chainsBCD-seed86.md), chosen so that every',
     'criterion\'s winner is here: no design is best at everything - none comes within 25% of the best on all three machine',
     'classes, and the fast designs are large while the small ones are slow. Every one is the CV8 byte-coded family, built',
     'at both cell widths and checked against the lab\'s hand-made s6-cv8b on the nine workloads it measures.', '',
     '## The designs', '',
     'Speed: CPU time against the hand-made s6-cv8b, the geometric mean over the selection workloads (kernel, fib, corpus,',
     'loop, bubble, ackermann, apps) - lower is faster, 0.185 is 5.4 times s6\'s speed. Each class the geometric mean of its',
     'machines, every session pooled: x86-64 - the laptop (AMD Ryzen 7 PRO 8840HS, 31 sessions) and dream (Intel i7-6700,',
     '42 sessions) at 8-byte cells; x86-32 - the same at 4-byte cells; ARMv7 - rage (an NVIDIA Tegra, 6 sessions), where a',
     'JIT design runs without its JIT (*). Size: the stripped engine plus the image, exact. Memory: peak resident, the',
     'laptop at 8-byte cells.', '',
     '| role | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | bytes, 4-byte | memory KB | JIT | checks (8 / 4) |',
     '|---|---|---|---|---|---|---|---|---|---|']
for i, role in ROLES:
    r = rows[i]
    L.append('| %s | %s | %.3f | %.3f | %.3f%s | %s | %s | %d | %s | %s / %s |' % (role, i, r['x86_64'], r['x86_32'], r['armv7'], '*' if r['jit'] else '',
             format(size(i, 8), ','), format(size(i, 4), ','), r['rss'], 'x86-64 and x86-32' if r['jit'] else 'no - portable', ok(i, 8), ok(i, 4)))
J = [rows[i] for i, _ in ROLES if rows[i]['jit']]; N = [rows[i] for i in ('690981ca5b', 'c2ef9488ff', '22420b3b61')]
x = lambda v: '%.1f-%.1f' % (1 / max(v), 1 / min(v))
L += ['', 'The trade in two sentences: the JIT designs are %s times s6\'s speed on x86-64 (%s at 32 bits) in %s-%s KB and %d-%d KB of' % (
      x([r['x86_64'] for r in J]), x([r['x86_32'] for r in J]), min(r['total'] for r in J) // 1000, max(r['total'] for r in J) // 1000 + 1,
      min(r['rss'] for r in J), max(r['rss'] for r in J)),
      'memory; without the JIT the three fastest portable designs are %s times s6\'s speed on ARMv7 and %s on x86-64 in %s-%s KB,' % (
      x([r['armv7'] for r in N]), x([r['x86_64'] for r in N]), min(r['total'] for r in N) // 1000, max(r['total'] for r in N) // 1000 + 1),
      'and the smallest and the leanest give up speed for 14 KB of engine and image, or 104 KB of memory.', '',
      '## What each is built from', '',
      'The genes where a design\'s expression differs from s6-cv8b\'s (lab/evolve/evolve.py; long lists as their length; GENE=-',
      'one s6 has and the design does not). tag2: relf\'s two-bit tag format; compiler 1: clang, else GCC; opt: the',
      'optimisation level, -O2 if absent.', '']
used = set()
for i, role in ROLES:
    r = rows[i]; d = r['differs']; used |= set(d)
    L.append('- **%s** (%s): %s.' % (i, role, ', '.join('%s=%s' % (k, val(v)) for k, v in sorted(d.items()))))
L += ['', '### The genes, as lab/evolve/GENES.md describes them', '']
for g in sorted(used):
    t = doc(g); L.append('- `%s` - %s' % (g, t if t else 'see lab/evolve/evolve.py, `grep -n "gene(\'%s\'" lab/evolve/evolve.py`' % g))
L += ['', '## For relf (RELF.md\'s adoption criteria)', '',
      '- **The JIT is x86 only** (x86-64 and x86-32); relf\'s CV8 stays portable, so the four JIT designs show what x86 reaches',
      '  and the five without it are relf\'s candidates as they stand. The JIT designs\' ARMv7 figures are their JIT-off builds.',
      '- **The images come from the lab\'s converter** (tools/layout.py), not relf\'s cross.4: what relf can take is mechanisms -',
      '  opcodes, fused and specialised forms, the dictionary\'s chains, engine flags - each rebuilt in relf and measured on',
      '  relf\'s own workloads with its tools (tools/relf-ab.sh, relf\'s bench-vm.py), as RELF.md requires. At Iteration 364 the',
      '  C-engine-only flags (clang, -Os, pinned registers) did not transfer to relf\'s cv8.c; the instruction level is the offer.',
      '- **The two-bit tag**: the JIT designs use it (tag2=1), the portable ones do not - their format is CV8 without the tag.',
      '- **Not measured here**: relf\'s shell workloads, AArch64 and RISC-V. The lab\'s selection is generic Forth by design (RELF.md,',
      '  the order of the work: phase 2 is seeing how these fit relf).', '',
      '## The files', '',
      'For each design, `ID/record.json` (its genome and the lab\'s record) and, at each width, `ID/cell8/` and `ID/cell4/`:',
      '`engine` and `image.img` (statically linked; run `./engine image.img < program.fth` - names are upper case, `BYE`',
      'ends it), `src/` (the engine\'s C source as compiled: vm.c and every file generated beside it), `build.txt` (each command',
      'the lab\'s build ran, in order - the compiler line gives every -D), `check.txt` (the nine workloads against s6-cv8b at the',
      'same width). `SHA256SUMS` covers every engine and image.', '',
      'Rebuilt byte for byte from the repository at the commit named in the bundle: `python3 lab/evolve/pack-designs.py OUT',
      'results/final-set-chainsBCD-seed86.md ' + ','.join(i for i, _ in ROLES) + '` (in a built tree). The other 12 of the final set,',
      'and every reading behind these numbers: results/final-pick-chainCD-seed86.md.', '']
open(os.path.join(P, 'README.md'), 'w').write('\n'.join(L))
print('\n'.join(L))
