import os, sys, shutil, subprocess, statistics, resource
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup(); E.long_files()
orig_rt = E.rt
built = {}
for mode in ('as is', 'lto'):
    E.rt = (lambda: orig_rt() + ['-flto']) if mode == 'lto' else orig_rt
    for did in ('3bb2087f9d', '3456ac1e5e'):
        g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'lto-%s-%s' % (did, mode.replace(' ', '')))
        shutil.rmtree(d, ignore_errors=True); eng, img = E.build(g, d); built[(did, mode)] = (eng, img, E.private_work(d))
E.rt = orig_rt
for did, works in (('3bb2087f9d', ('fib', 'loop', 'ackermann', 'corpus')), ('3456ac1e5e', ('corpus', 'fib'))):
    for w in works:
        prog = E.program(w); ts = {'as is': [], 'lto': []}
        for k in range(9):
            for m in (('as is', 'lto') if k % 2 == 0 else ('lto', 'as is')):
                eng, img, pw = built[(did, m)]
                r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
                subprocess.run([eng, img], input=prog, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=pw, timeout=120)
                r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
                ts[m].append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
        a, b = statistics.median(ts['as is']), statistics.median(ts['lto'])
        print('%s %-9s as is %6.1f ms  lto %6.1f ms  ratio %.3f' % (did, w, a * 1000, b * 1000, b / a), flush=True)
