import os, sys, subprocess, statistics, resource
sys.argv = ['x']; sys.path.insert(0, '/tmp/mo/lab/evolve'); import evolve as E
E.setup(); E.long_files()
d = {k: os.path.join(E.EV, 'jk%d' % k) for k in (0, 2, 3)}
pw = {k: os.path.join(d[k], 'work') for k in d}
for w in ('fib', 'loop', 'bubble', 'ackermann', 'corpus'):
    prog = E.program(w); ts = {k: [] for k in d}
    for r in range(11):
        order = [(0, 2, 3), (2, 3, 0), (3, 0, 2)][r % 3]
        for k in order:
            r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
            subprocess.run([d[k] + '/engine', d[k] + '/image.img'], input=prog, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=pw[k], timeout=120)
            r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
            ts[k].append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
    m = {k: statistics.median(ts[k]) for k in d}
    print('%-9s jitk=0 %6.1f ms | jitk=2 %6.1f (%.3f) | jitk=3 %6.1f (%.3f)' % (w, m[0] * 1000, m[2] * 1000, m[2] / m[0], m[3] * 1000, m[3] / m[0]), flush=True)
