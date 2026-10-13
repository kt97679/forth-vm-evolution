import os, sys, shutil
root = sys.argv[1]
sys.argv = ['x']; sys.path.insert(0, root + '/lab/evolve'); import evolve as E
E.setup()
out = []
for did in ('add5ec8937', 'dde890d478', 'cc6d168e0a', 'c1cc8e127c', 'f20de05a64', '0af26c8e89'):
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'sz2'); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    out.append('%s %d+%d' % (did, os.path.getsize(eng), os.path.getsize(img)))
print(root, ' | '.join(out))
