import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/tmp/mo/lab/evolve'); import evolve as E
E.setup()
base = E.recorded_genome('3bb2087f9d')
for k in (0, 2, 3):
    g = E.canon(dict(base, jitk=k)); d = os.path.join(E.EV, 'jk%d' % k); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(g, d)
        E.alive(eng, img, E.private_work(d))
        r = subprocess.run([eng, img], input=b': T1 0 10 0 DO I + LOOP . ; T1 CR : T2 3 4 OVER OVER + * . ; T2 CR : T3 1 2 3 ROT ROT + + . ; T3 CR : T4 5 DUP 0= IF 1 ELSE 2 THEN + . ; T4 CR\nBYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30, cwd=d)
        print('jitk=%d: engine %d bytes, corpus alive; tests: %s' % (k, os.path.getsize(eng), r.stdout.replace(b'\r', b'').decode().split()[-9:]), flush=True)
    except Exception as e:
        print('jitk=%d: DIED %s' % (k, str(e)[:300]), flush=True)
