import json, os, shutil, sys
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup(); print('cell width %d bytes, dumps %s' % (E.cellw(), E.KW()), flush=True)
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md') if l.startswith('{"') and '09de03f091' in l)
SRC = (': T2 3 BEGIN + DUP 30 < WHILE 3 REPEAT ;\n10 T2 .\n: T3 DUP 7 + ;\n5 T3 . .\n: T4 SWAP 9 + ;\n1 2 T4 . .\n'
       ': T5 0 SWAP BEGIN SWAP 2 + SWAP 1- DUP 0= UNTIL DROP ;\n6 T5 .\n: T6 IF 4 ELSE 6 THEN 1 + ;\n-1 T6 . 0 T6 .\n'
       ': L1 0 10 0 DO I + LOOP ;\nL1 .\n: L2 0 4 0 DO 3 0 DO I J * + LOOP LOOP ;\nL2 .\n: L3 0 100 0 DO I 7 = IF I UNLOOP EXIT THEN LOOP ;\nL3 .\n'
       ': L4 0 SWAP 0 ?DO 1+ LOOP ;\n5 L4 . 0 L4 .\n: L5 0 20 0 DO I 9 > IF LEAVE THEN 1+ LOOP ;\nL5 .\n: L6 0 30 0 DO I + 5 +LOOP ;\nL6 .\nBYE\n')
for name, g in [('as it is', {}), ('rtimm=2', {'rtimm': 2}), ('rtloop=1', {'rtloop': 1}), ('rtloop=2', {'rtloop': 2}), ('rtimm=2 rtloop=2', {'rtimm': 2, 'rtloop': 2})]:
    g = E.canon(dict(r['genome'], **g)); d = os.path.join(E.EV, 'rmw'); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw)
        out = getattr(E.sh([eng, img], cwd=pw, inp=SRC.encode(), timeout=60, cpu=20), 'stdout', b'')
        print('%-17s lean %-5s %d bytes, corpus ok | %s' % (name, E.rtimm_lean(g), os.path.getsize(eng) + os.path.getsize(img), ' '.join(x for x in out.decode('latin-1').split() if x.lstrip('-').isdigit())), flush=True)
    except Exception as x: print('%s: %s' % (name, str(x)[:200]), flush=True)
