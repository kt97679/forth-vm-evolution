import os, sys, subprocess, statistics, resource
d0, d1 = '/tmp/b46b/build/evolve/tt0', '/tmp/b46b/build/evolve/tt1'
prog = b'S" ackermann.fth" INCLUDED\n: B 2000 0 DO NUM 3 -ack DROP LOOP ; B\nBYE\n'
ts = {0: [], 1: []}
for k in range(15):
    for t, d in ((0, d0), (1, d1)) if k % 2 == 0 else ((1, d1), (0, d0)):
        r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
        subprocess.run([d + '/engine', d + '/image.img'], input=prog, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120, cwd=d)
        r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
        ts[t].append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
for t in (0, 1):
    print('jittail=%d: ackermann x2000 median %.1f ms, min %.1f ms' % (t, statistics.median(ts[t]) * 1000, min(ts[t]) * 1000))
print('ratio of medians %.3f, of minima %.3f' % (statistics.median(ts[1]) / statistics.median(ts[0]), min(ts[1]) / min(ts[0])))
