import os, sys
ids = sys.argv[1:]; sys.argv = ['x']; sys.path.insert(0, '/tmp/batch43/lab/evolve'); import evolve as E
E.setup()
bad = 0
for did in ids:
    d = os.path.join(E.EV, 'gate5')
    eng, img = E.build(E.canon(dict(E.recorded_genome(did), fsys=5)), d)
    try: E.alive(eng, img, E.private_work(d)); print('%s fsys 5: alive (corpus as the cell engine, kernel.img identical, far)' % did, flush=True)
    except Exception as e: bad += 1; print('%s fsys 5: DIED %s' % (did, e), flush=True)
sys.exit(1 if bad else 0)
