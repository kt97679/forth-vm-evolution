import os, sys, subprocess, statistics, resource
sys.argv = ['x']; sys.path.insert(0, '/tmp/b46b/lab/evolve'); import evolve as E
E.setup(); E.long_files()
d = {0: '/tmp/b46b/build/evolve/tt0', 1: '/tmp/b46b/build/evolve/tt1'}
for w in ('fib', 'corpus'):
    prog = E.program(w)
    ts = {0: [], 1: []}
    for k in range(25):
        for t in ((0, 1) if k % 2 == 0 else (1, 0)):
            r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
            subprocess.run([d[t] + '/engine', d[t] + '/image.img'], input=prog, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120, cwd=E.EV)
            r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
            ts[t].append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
    m0, m1 = statistics.median(ts[0]), statistics.median(ts[1])
    print('%-7s jittail=0 median %5.1f min %5.1f | jittail=1 median %5.1f min %5.1f | ratio of medians %.3f, of minima %.3f' % (
        w, m0 * 1000, min(ts[0]) * 1000, m1 * 1000, min(ts[1]) * 1000, m1 / m0, min(ts[1]) / min(ts[0])), flush=True)
