#!/usr/bin/env python3
"""results/drafts/numfirst-probe-733.py NAME ... - the gene numfirst's semantics (Iteration 733): each role (designs/NAME/record.json) built
by the lab with numfirst off and on (evolve.build), three programs run on each - numbers of both signs and bases, a name of
digits defined (it turns the fast path off: : 123 456 ; 123 . prints 456), a negative one, a token of digits not a number
in the base. Prints each output; off and on must agree. HK_W4=1: 4-byte cells. From the top of a built tree, python3 -B."""
ROOT = os.getcwd(); sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve'))
names = sys.argv[1:]; sys.argv = ['x']
import evolve as E
if os.environ.get('HK_W4'): os.environ.update(E.W4_ENV)
E.setup()
PROG = (b'77 . -5 . 0 . -0 . HEX 10 . 1A . DECIMAL 2 BASE ! 101 . DECIMAL 3 1+ . CR\n'
        b': 123 456 ; 123 . -7 . 8 . CR\n')
PROG2 = b': -9 1 ; -9 . 9 . CR\n'
PROG3 = b'2 BASE ! 12 . CR\n'
for n in names:
    g = json.load(open(os.path.join(ROOT, 'designs', n, 'record.json')))['genome']
    for v in (0, 1):
        d = os.path.join(E.EV, 'nfprobe-%s-%d' % (n, v)); et, it = E.build(E.canon(dict(g, numfirst=v)), d); pw = E.private_work(d)
        for p in (PROG, PROG2, PROG3):
            o = subprocess.run([et, it], input=p, capture_output=True, timeout=60, cwd=pw)
            print(n, v, repr((o.stdout + o.stderr)[-90:]))
