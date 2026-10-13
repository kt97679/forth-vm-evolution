import os, sys, shutil, subprocess, statistics, resource
sys.argv = ['x']; sys.path.insert(0, '/tmp/mo/lab/evolve'); import evolve as E
E.setup(); E.long_files()
res = {}
for did in ('3456ac1e5e', '3bb2087f9d'):
    for lto in (0, 1):
        g = E.canon(dict(E.recorded_genome(did), lto=lto)); d = os.path.join(E.EV, 'lt-%s-%d' % (did, lto)); shutil.rmtree(d, ignore_errors=True)
        eng, img = E.build(g, d); E.alive(eng, img, E.private_work(d)); res[(did, lto)] = (eng, img, os.path.join(d, 'work'))
    print(did, 'engine: lto=0 %d, lto=1 %d' % (os.path.getsize(res[(did, 0)][0]), os.path.getsize(res[(did, 1)][0])), flush=True)
for w in ('fib', 'loop'):
    prog = E.program(w); ts = {0: [], 1: []}
    for r in range(7):
        for lto in ((0, 1) if r % 2 == 0 else (1, 0)):
            eng, img, pw = res[('3bb2087f9d', lto)]
            r0 = resource.getrusage(resource.RUSAGE_CHILDREN); subprocess.run([eng, img], input=prog, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=pw, timeout=60); r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
            ts[lto].append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
    print('3bb2087f9d (JIT) %s: lto=0 %.1f ms, lto=1 %.1f ms' % (w, statistics.median(ts[0]) * 1000, statistics.median(ts[1]) * 1000), flush=True)
