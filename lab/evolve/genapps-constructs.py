#!/usr/bin/env python3
"""lab/evolve/genapps-constructs.py [--cells 8|4] [--systems A,B] [--census NAME] [--out FILE] - what each construct of a program
costs in code bytes, per system (Iteration 674, with genapps.py: where its application-code gap comes from).

Each construct is compiled 16 times into one definition, against the same definition empty; the difference over
16 is the construct's bytes (alignment spread out). The definitions themselves - `:` and `;`, a name's characters,
VARIABLE, CONSTANT, CREATE, a defining word and its child, VALUE - are each one definition, its bytes whole. Calls
three ways: to the kernel (`.`), to a program's word within the first 16 KB of the image (NEAR, defined before the
prelude) and past them (FAR, after 20,000 bytes allotted) - the two-bit tag's calls are 2 bytes in the first 16 KB
and 4 past them, CV8's 2 and 3. NEAR and FAR are nine instructions, too long for relf's inlining (683).

The systems and the preludes are genapps.py's (its work directory, build/genapps/work-CELLS: run it first): the lab's
VALUE and TO are coreext.4's, relf's the prelude's (CREATE , DOES> @ - relf compiles a fetch of one as its VAR@).
Prints a Markdown table (a construct a row) and writes FILE (default build/genapps/constructs-CELLS.json).
--census NAME instead: brainless's definitions by kind on system NAME (a lab system) - its load with `:`, :NONAME,
CONSTANT, VARIABLE, VALUE and CREATE each counting itself (a definition through its old self), after the prelude."""
import argparse, json, os, re, shutil, subprocess, sys
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
DESIGNS = ['smallest', 'least-memory', 'portable-small', 'portable-knee', 'portable-arm', 'portable-fastest',
           'best-all-round', 'small-jit', 'fastest-x86-64', 'fastest-x86-32']
ap = argparse.ArgumentParser(usage=__doc__.split('\n')[0])
ap.add_argument('--cells', type=int, default=8, choices=(8, 4)); ap.add_argument('--systems', default='')
ap.add_argument('--out', default=''); ap.add_argument('--census', default='')
a = ap.parse_args()
B = os.path.join(ROOT, 'build'); W = os.path.join(B, 'genapps', 'work-%d' % a.cells); rtree = os.path.join(W, 'relf-tree')
if not os.path.isdir(rtree): sys.exit('genapps-constructs: run genapps.py --cells %d first (no %s)' % (a.cells, rtree))
SYS = {}
if a.cells == 8:
    SYS['s6'] = ('lab', [os.path.join(B, 's6-cv8b-64'), os.path.join(B, 's6-cv8b-s64.img')])
    for d in DESIGNS: SYS[d] = ('lab', [os.path.join(ROOT, 'designs', d, 'forth'), os.path.join(ROOT, 'designs', d, 'image.img')])
    SYS['relf64'] = ('relf', [os.path.join(rtree, 'relf64'), os.path.join(rtree, 'forth', 'kernel64.img')])
    SYS['relfasm64'] = ('relf', [os.path.join(rtree, 'relfasm64'), os.path.join(rtree, 'forth', 'kernel64.img')])
    if shutil.which('gforth-fast'): SYS['gforth-fast'] = ('gforth', [shutil.which('gforth-fast')])
else:
    SYS['s6'] = ('lab', [os.path.join(B, 's6-cv8b-32'), os.path.join(B, 's6-cv8b-s32.img')])
    for d in DESIGNS: SYS[d] = ('lab', [os.path.join(ROOT, 'designs', d, 'forth32'), os.path.join(ROOT, 'designs', d, 'image32.img')])
    SYS['relf32'] = ('relf', [os.path.join(rtree, 'relf32'), os.path.join(rtree, 'forth', 'kernel32.img')])
if a.systems: SYS = {k: v for k, v in SYS.items() if k in a.systems.split(',')}
# (label, the construct - compiled 16 times into a definition) and (label, a whole definition)
N = 16
INNER = [('a primitive (DUP)', 'DUP'), ('a call: the kernel (.)', '.'), ('a call: NEAR', 'NEAR'), ('a call: FAR', 'FAR'),
         ('literal 5', '5'), ('literal 1000', '1000'), ('literal 100000', '100000'), ('literal 1000000000', '1000000000'),
         ('a variable', 'KV'), ('a variable @', 'KV @'), ('a variable !', 'KV !'), ('a constant', 'KC'),
         ('a VALUE', 'KW'), ('TO a VALUE', 'TO KW'), ('5 +', '5 +'), ("['] DUP", "['] DUP"),
         ('IF THEN', 'IF THEN'), ('IF ELSE THEN', 'IF ELSE THEN'), ('BEGIN UNTIL', 'BEGIN UNTIL'),
         ('BEGIN WHILE REPEAT', 'BEGIN WHILE REPEAT'), ('DO LOOP', 'DO LOOP'), ('S" ABCDEFGH"', 'S" ABCDEFGH"'),
         ('." ABCDEFGH"', '." ABCDEFGH"')]
WHOLE = [(': X ; (a 3-character name)', ': X%02d ;'), ('a name\'s character, each (8 more)', ': X%02dABCDEFGH ;'),
         ('VARIABLE', 'VARIABLE X%02d'), ('CONSTANT', '5 CONSTANT X%02d'), ('CREATE', 'CREATE X%02d'),
         ('a defining word (CREATE , DOES> @)', ': X%02d CREATE , DOES> @ ;'), ('its child', '5 XDEF X%02d'),
         ('VALUE', '0 VALUE X%02d')]
def driver(kind):
    pre = {'lab': 'S" lab-prelude.fth" INCLUDED\n', 'relf': 'S" relf-prelude.fth" INCLUDED\n', 'gforth': ''}[kind]
    body = ' 1 2 3 4 5 2DROP 2DROP DROP ;\n'
    t = ': NEAR' + body + pre + '20000 ALLOT\n: FAR' + body + 'VARIABLE KV  5 CONSTANT KC  0 VALUE KW\n'
    t += ': XDEF CREATE , DOES> @ ;\nVARIABLE H0  : M0 HERE H0 ! ;  : M1 ( n --- ) HERE H0 @ - SWAP . . CR ;\n'
    for i, (_, c) in enumerate(INNER):
        t += 'M0 : Y%02d ; %d M1\n' % (i, 1000 + i)
        t += 'M0 : Z%02d %s ; %d M1\n' % (i, ' '.join([c] * N), 2000 + i)
    for i, (_, c) in enumerate(WHOLE):
        t += ('M0 ' + c + ' %d M1\n') % (i, 3000 + i)
    return t + 'BYE\n'
def run(s):
    kind, cmd = SYS[s]
    name = 'constructs-%s.fs' % kind
    if kind == 'gforth':
        open(os.path.join(W, 'gf', name), 'w').write(driver(kind))
        p = subprocess.run(cmd + [name], cwd=os.path.join(W, 'gf'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    else:
        open(os.path.join(W, name), 'w').write(driver(kind))
        p = subprocess.run(cmd, cwd=W, input=('S" %s" INCLUDED\n' % name).encode(), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=120)
    out = p.stdout.decode('latin-1'); got = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r'(\d{4}) (-?\d+) *\r?\n', out)}
    r = {}
    for i, (lab, _) in enumerate(INNER):
        if 1000 + i in got and 2000 + i in got: r[lab] = (got[2000 + i] - got[1000 + i]) / N
    for i, (lab, _) in enumerate(WHOLE):
        if 3000 + i in got: r[lab] = got[3000 + i]
    if WHOLE[1][0] in r and WHOLE[0][0] in r: r[WHOLE[1][0]] = (r[WHOLE[1][0]] - r[WHOLE[0][0]]) / 8
    missing = [l for l, _ in INNER + WHOLE if l not in r]
    if missing: print('genapps-constructs: %s: none for %s\n%s' % (s, ', '.join(missing), out[-400:]), file=sys.stderr)
    return r
if a.census:
    kind, cmd = SYS[a.census]
    if kind != 'lab': sys.exit('genapps-constructs: --census takes a lab system')
    KINDS = [':', ':NONAME', 'CONSTANT', 'VARIABLE', 'VALUE', 'CREATE']
    t = 'S" lab-prelude.fth" INCLUDED\n'
    for i, k in enumerate(KINDS): t += 'VARIABLE #K%d  0 #K%d !  : %s 1 #K%d +! %s ;\n' % (i, i, k, i, k)
    t += 'INCLUDE benchmark.fs\n777001 . ' + ' '.join('#K%d @ .' % i for i in range(len(KINDS))) + ' 777002 . CR BYE\n'
    open(os.path.join(W, 'census-lab.fs'), 'w').write(t)
    p = subprocess.run(cmd, cwd=W, input=b'S" census-lab.fs" INCLUDED\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    m = re.search(r'777001 ([\d ]+?) 777002', p.stdout.decode('latin-1'))
    if not m: sys.exit('genapps-constructs: no census\n' + p.stdout.decode('latin-1')[-400:])
    print('brainless on %s: ' % a.census + ', '.join('%s %s' % (n, k) for k, n in zip(KINDS, m.group(1).split())))
    sys.exit(0)
R = {s: run(s) for s in SYS}
names = list(SYS)
print('| construct | ' + ' | '.join(names) + ' |'); print('|---|' + '---:|' * len(names))
fmt = lambda v: '-' if v is None else ('%d' % v if v == int(v) else '%.1f' % v)
for lab, _ in INNER + WHOLE:
    print('| %s | ' % lab.replace('|', '\\|') + ' | '.join(fmt(R[s].get(lab)) for s in names) + ' |')
json.dump({'cells': a.cells, 'systems': R}, open(a.out or os.path.join(B, 'genapps', 'constructs-%d.json' % a.cells), 'w'), indent=1)
