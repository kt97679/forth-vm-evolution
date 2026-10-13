import os, sys, shutil, subprocess, time, statistics
sys.argv = ['x']; sys.path.insert(0, '/tmp/b46b/lab/evolve'); import evolve as E
E.setup()
base = E.canon(E.recorded_genome('28677d13b1'))
res = {}
for tail in (0, 1):
    g = E.canon(dict(base, jittail=tail)); d = os.path.join(E.EV, 'tt%d' % tail); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    for f in ('ackermann.fth', 'fib.fth'): shutil.copy('/tmp/b46b/bench/' + f, os.path.join(d, f))
    out = {}
    for f in ('ackermann.fth', 'fib.fth'):
        ts = []
        for k in range(7):
            t0 = time.perf_counter()
            r = subprocess.run([eng, img], input=('S" %s" INCLUDED\nBENCH\nBYE\n' % f).encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd=d)
            ts.append(time.perf_counter() - t0)
        out[f] = (r.stdout.replace(b'\r', b'').decode(errors='replace').split('\n')[-3:-1], round(statistics.median(ts) * 1000, 1))
    r = subprocess.run([eng, img], input=b': CNT DUP IF 1- RECURSE THEN ;  3000000 CNT . CR\n: T2 DUP 0= IF EXIT THEN 1- RECURSE ;  3000000 T2 . CR\nBYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd=d)
    out['deep'] = (r.returncode, r.stdout.replace(b'\r', b'').decode(errors='replace').strip().split('\n')[-3:])
    print('jittail=%d engine %d bytes:' % (tail, os.path.getsize(eng)), out, flush=True)
