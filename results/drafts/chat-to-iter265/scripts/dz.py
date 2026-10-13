import os, sys, shutil
root = sys.argv[1]
sys.argv = ['x']; sys.path.insert(0, root + '/lab/evolve'); import evolve as E
E.setup()
out = []
for did in ('add5ec8937', 'cc6d168e0a', '28677d13b1', 'f20de05a64'):
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'dz'); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    out.append('%s %d' % (did, os.path.getsize(eng)))
print(root, ' | '.join(out))
