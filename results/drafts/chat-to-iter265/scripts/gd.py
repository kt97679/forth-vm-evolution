import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
for did in ('3456ac1e5e', 'fe3c9c3940', '3bb2087f9d'):
    out = []
    for gv in (0, 1):
        g = E.canon(dict(E.recorded_genome(did), guard=gv)); d = os.path.join(E.EV, 'gd%d' % gv); shutil.rmtree(d, ignore_errors=True)
        eng, img = E.build(g, d)
        r = subprocess.run([eng, img], input=b'S" before the fault" TYPE CR 0 @ . S" after" TYPE CR\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30, cwd=d)
        out.append('guard %d: engine %d, `0 @` exit %d, output %r' % (gv, os.path.getsize(eng), r.returncode, r.stdout.replace(b'\r', b'')[-60:]))
    print(did, ' | '.join(out), flush=True)
