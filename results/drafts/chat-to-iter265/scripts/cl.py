import os, sys, shutil, subprocess, time
mode = sys.argv[1]
if mode == 'clang': os.environ['PATH'] = '/tmp/clangbin:' + os.environ['PATH']
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
for did in ('3456ac1e5e', '697f12fecc', 'c05f76468e', 'fe3c9c3940', '3bb2087f9d'):
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'cl-%s-%s' % (mode, did)); shutil.rmtree(d, ignore_errors=True)
    t0 = time.time()
    try:
        eng, img = E.build(g, d); E.alive(eng, img, E.private_work(d))
        r = subprocess.run([eng, img], input=E.program('fib', single=True), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60, cwd=os.path.join(d, 'work'))
        t = time.time() - t0
        print('%-5s %s: engine %6d bytes, corpus alive, jit %s, opt %s, tail %s' % (mode, did, os.path.getsize(eng), E.jit_on(g), g.get('opt'), E.express(g).get('tail')), flush=True)
    except Exception as e:
        print('%-5s %s: DIED %s' % (mode, did, str(e)[:200].replace('\n', ' ')), flush=True)
