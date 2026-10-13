import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/tmp/b46b/lab/evolve'); import evolve as E
E.setup()
base = E.recorded_genome('28677d13b1')
for name, g in (('nojitx', dict(base, jitx=0, jitinl=0, jittail=1)), ('nojitx-off', dict(base, jitx=0, jitinl=0, jittail=0))):
    g = E.canon(g); d = os.path.join(E.EV, 'tt6'); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    shutil.copy('/tmp/b46b/bench/ackermann.fth', d)
    r = subprocess.run([eng, img], input=b'S" ackermann.fth" INCLUDED\nBENCH\n: CNT DUP IF 1- RECURSE THEN ;  3000000 CNT . CR\nBYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd=d)
    print(name, 'expressed jittail', E.express(g).get('jittail'), 'engine', os.path.getsize(eng), r.returncode, r.stdout.replace(b'\r', b'').decode(errors='replace').split()[-9:])
