import os, sys
ids = sys.argv[1:]; sys.argv = ['x']; sys.path.insert(0, '/tmp/batch43/lab/evolve'); import evolve as E
E.setup()
for did in ids:
    g0 = E.recorded_genome(did)
    for lev in (4, 5):
        d = os.path.join(E.EV, 'sizes')
        eng, img = E.build(E.canon(dict(g0, fsys=lev)), d)
        print('%s fsys %d: image %d, engine file %d' % (did, lev, os.path.getsize(img), os.path.getsize(eng)), flush=True)
