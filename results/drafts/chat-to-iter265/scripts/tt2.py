import os, sys, shutil, subprocess, time, statistics, resource
sys.argv = ['x']; sys.path.insert(0, '/tmp/b46b/lab/evolve'); import evolve as E
E.setup()
base = E.canon(E.recorded_genome('28677d13b1'))
progs = {'ack x600': b'S" ackermann.fth" INCLUDED\n: B 600 0 DO NUM 3 -ack DROP LOOP ; B\nBYE\n',
         'fib x12': b'S" fib.fth" INCLUDED\n: B 12 0 DO 27 FIB DROP LOOP ; B\nBYE\n',
         'startup': b'BYE\n'}
for tail in (0, 1):
    g = E.canon(dict(base, jittail=tail)); d = os.path.join(E.EV, 'tt%d' % tail); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    for f in ('ackermann.fth', 'fib.fth'): shutil.copy('/tmp/b46b/bench/' + f, os.path.join(d, f))
    out = {}
    for name, prog in progs.items():
        ts = []
        for k in range(9):
            r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
            r = subprocess.run([eng, img], input=prog, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, cwd=d)
            r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
            ts.append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
        out[name] = round(statistics.median(ts) * 1000, 1)
    print('jittail=%d engine %d bytes, cpu ms (median of 9):' % (tail, os.path.getsize(eng)), out, flush=True)
