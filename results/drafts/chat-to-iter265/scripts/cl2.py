import os, sys, shutil, subprocess, statistics, resource
os.environ['PATH'] = '/tmp/clangbin:' + os.environ['PATH']
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup(); E.long_files()
GCC_ONLY = ('-fipa-cp-clone', '-ftracer', '-fpeel-loops', '-fno-gcse', '-fno-crossjumping', '-falign-labels=1', '-falign-jumps=1', '-fno-reorder-blocks', '-falign-loops=1')
orig = E.ccflags
for opt in ('as is', '-Oz'):
    def cf(g, opt=opt):
        f = [x for x in orig(g) if x not in GCC_ONLY]
        return ['-Oz' if x in ('-Os', '-O2', '-O3') else x for x in f] if opt == '-Oz' else f
    E.ccflags = cf
    for did in ('3456ac1e5e', 'fe3c9c3940', '3bb2087f9d'):
        g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'cl2-%s' % did); shutil.rmtree(d, ignore_errors=True)
        try:
            eng, img = E.build(g, d); E.alive(eng, img, E.private_work(d))
            ts = []
            for k in range(5):
                r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
                subprocess.run([eng, img], input=E.program('fib'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60, cwd=os.path.join(d, 'work'))
                r1 = resource.getrusage(resource.RUSAGE_CHILDREN); ts.append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
            print('clang %-6s %s: engine %6d bytes, corpus alive, fib %.1f ms' % (opt, did, os.path.getsize(eng), statistics.median(ts) * 1000), flush=True)
        except Exception as e:
            print('clang %-6s %s: DIED %s' % (opt, did, str(e)[:160].replace('\n', ' ')), flush=True)
