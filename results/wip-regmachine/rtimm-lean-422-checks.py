import json, os, shutil, sys
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md') if l.startswith('{"') and '09de03f091' in l)
SRC = (': T2 ( n -- n2 ) 3 BEGIN + DUP 30 < WHILE 3 REPEAT ;\n10 T2 .\n'
       ': T3 ( n -- n n2 ) DUP 7 + ;\n5 T3 . .\n'
       ': T4 ( a b -- a2 b ) SWAP 9 + ;\n1 2 T4 . .\n'
       ': T5 ( n -- n2 ) 0 SWAP BEGIN SWAP 2 + SWAP 1- DUP 0= UNTIL DROP ;\n6 T5 .\n'
       ': T6 ( f -- n ) IF 4 ELSE 6 THEN 1 + ;\n-1 T6 . 0 T6 .\nBYE\n')
for cell in (8, 4):
    for name, g in [('as it is', dict(r['genome'])), ('rtimm=2 lean', dict(r['genome'], rtimm=2))]:
        g = E.canon(dict(g, cell=cell)) if 'cell' in E.canon(r['genome']) else E.canon(g)
        d = os.path.join(E.EV, 'rmt'); shutil.rmtree(d, ignore_errors=True)
        try:
            eng, img = E.build(g, d); pw = E.private_work(d); a = E.alive(eng, img, pw)
            out = E.sh([eng, img], cwd=pw, inp=SRC.encode(), timeout=60, cpu=20)
            out = getattr(out, "stdout", out)
            out = (out.decode('latin-1') if isinstance(out, bytes) else str(out)).split()
            print('cell %d %-13s lean %s alive %r -> %s' % (cell, name, E.rtimm_lean(g), a, ' '.join(x for x in out if x.lstrip('-').isdigit())), flush=True)
        except Exception as x: print('cell %d %s: %s' % (cell, name, str(x)[:200]), flush=True)
