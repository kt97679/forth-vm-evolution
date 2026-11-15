#!/usr/bin/env python3
"""lab/evolve/string-price.py [--cells 8|4] [--out FILE] - the price of inline strings without cell alignment (Iteration
680: item 6 of results/drafts/search-reopen-plan-677.md, before it is built) on genapps.py's seven programs.

S" and ." are redefined before the program, each with its own run-time word: once laying the string as kernel.4's
STRING, does - count, characters, ALIGN - and (S")'s `ALIGNED` (A), once without either (B). HERE's advance over the
program's load, A less B, is the padding the change takes out of that program's code on that system: exact for this
layout (a call to a colon word where a design's kernel may lay an opcode, so its padding can differ by a byte or two
from the built change's). Both versions end their definitions at the same 256-byte boundary, so the program starts at
the same address. Not the kernel's own strings - the image's - which move with the change itself. ABORT" is not in
the seven. Needs build/genapps/work-CELLS (genapps.py makes it; this runs genapps.py --sizes on s6 for it).
On s6 and the ten designs of designs/. Writes FILE (default build/genapps/string-price-CELLS.json); prints a table."""
import json, os, re, subprocess, sys
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
a = sys.argv[1:]; CELLS = int(a[a.index('--cells') + 1]) if '--cells' in a else 8
OUT = a[a.index('--out') + 1] if '--out' in a else os.path.join(ROOT, 'build', 'genapps', 'string-price-%d.json' % CELLS)
W = os.path.join(ROOT, 'build', 'genapps', 'work-%d' % CELLS)
subprocess.run([sys.executable, os.path.join(HERE_, 'genapps.py'), '--sizes', '--cells', str(CELLS), '--systems', 's6', '--apps', 'sim16'],
               check=True, stdout=subprocess.DEVNULL)
APPS = [('sim16', 'S" sim16.fth" INCLUDED'), ('gc16', 'S" gc16.fth" INCLUDED'), ('scan', 'S" scan.fth" INCLUDED'), ('evo', 'S" evo.fth" INCLUDED'),
        ('wordfreq', 'S" wordfreq.fth" INCLUDED'), ('minif', 'S" minif.fth" INCLUDED'), ('brainless', 'INCLUDE benchmark.fs')]
DESIGNS = re.findall(r"'([\w-]+)'", re.search(r'DESIGNS = \[([^\]]*)\]', open(os.path.join(HERE_, 'genapps.py')).read()).group(1))
B = os.path.join(ROOT, 'build')
SYS = {'s6': [os.path.join(B, 's6-cv8b-%d' % (64 if CELLS == 8 else 32)), os.path.join(B, 's6-cv8b-s%d.img' % (64 if CELLS == 8 else 32))]}
for d in DESIGNS:
    SYS[d] = [os.path.join(ROOT, 'designs', d, 'forth' if CELLS == 8 else 'forth32'), os.path.join(ROOT, 'designs', d, 'image.img' if CELLS == 8 else 'image32.img')]
def redef(aligned):
    al, an = (' ALIGNED', ' ALIGN') if aligned else ('', '')
    return (': (S2") R> COUNT 2DUP +%s >R ;\n: (.2") R> COUNT 2DUP TYPE +%s >R ;\n'
            ': STRING2, DUP C, HERE OVER ALLOT SWAP MOVE%s ;\n'
            ': S" STATE @ IF POSTPONE (S2") 34 PARSE STRING2, ELSE POSTPONE S" THEN ; IMMEDIATE\n'
            ': ." POSTPONE (.2") 34 PARSE STRING2, ; IMMEDIATE\n'
            'HERE 255 + -256 AND HERE - ALLOT\n' % (al, al, an))
def size(s, app, inc, aligned):
    t = ('S" lab-prelude.fth" INCLUDED\n' if app == 'brainless' else '') + redef(aligned)
    t += 'VARIABLE H0  HERE H0 !\n' + inc + '\n777001 . HERE H0 @ - . 777002 . CR\nBYE\n'
    name = 'sp-%s-%s.fs' % (app, 'a' if aligned else 'b'); open(os.path.join(W, name), 'w').write(t)
    p = subprocess.run(SYS[s], cwd=W, input=('S" %s" INCLUDED\n' % name).encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    m = re.search(r'777001 (-?\d+) +777002', p.stdout.decode('latin-1'))
    return int(m.group(1)) if m else None
R = {}
for s in SYS:
    R[s] = {}
    for app, inc in APPS:
        x, y = size(s, app, inc, True), size(s, app, inc, False)
        R[s][app] = {'aligned': x, 'unaligned': y, 'saved': (x - y) if x is not None and y is not None else None}
    print('string-price %d: %-16s %s' % (CELLS, s, ' '.join('%s %s' % (k, v['saved']) for k, v in R[s].items())), flush=True)
json.dump(R, open(OUT, 'w'), indent=1); print('string-price: wrote %s' % OUT)
