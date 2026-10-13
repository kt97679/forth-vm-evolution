import os, sys, subprocess, statistics, resource
sys.argv = ['x']; sys.path.insert(0, '/tmp/b46b/lab/evolve'); import evolve as E
E.setup(); E.long_files()
d = {0: '/tmp/b46b/build/evolve/tt0', 1: '/tmp/b46b/build/evolve/tt1'}
for w in ('kernel', 'corpus', 'fib', 'loop', 'bubble', 'ackermann'):
    prog = E.program(w)
    ts = {0: [], 1: []}
    for k in range(9):
        for t in ((0, 1) if k % 2 == 0 else (1, 0)):
            r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
            subprocess.run([d[t] + '/engine', d[t] + '/image.img'], input=prog, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120, cwd=E.EV)
            r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
            ts[t].append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
    m0, m1 = statistics.median(ts[0]), statistics.median(ts[1])
    print('%-9s jittail=0 %6.1f ms  jittail=1 %6.1f ms  ratio %.3f' % (w, m0 * 1000, m1 * 1000, m1 / m0), flush=True)
