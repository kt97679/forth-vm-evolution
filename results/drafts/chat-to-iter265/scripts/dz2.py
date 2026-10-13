import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/tmp/mo/lab/evolve'); import evolve as E
E.setup()
out = []
for did in ('3456ac1e5e', 'fe3c9c3940', '3bb2087f9d', '697f12fecc'):
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'dz2'); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    r = subprocess.run([eng, img], input=b': T 7 0 / ; : U [\'] T CATCH . ; U CR 7 2 / . CR\nBYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30, cwd=d)
    out.append('%s %d %s' % (did, os.path.getsize(eng), r.stdout.replace(b'\r', b'').decode().split()[-4:]))
print(' | '.join(out))
