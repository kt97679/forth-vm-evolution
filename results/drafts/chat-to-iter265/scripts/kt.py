import os, sys, subprocess, statistics, resource, shutil
# the kernel workload's CPU time on the fastest JIT design, master's cross.4 against the fast path - alternated
res = {}
for tree in ('/home/claude/forth-vm-evolution', '/tmp/ff'):
    sys.path.insert(0, tree + '/lab/evolve')
import importlib
out = {}
for name, tree in (('before', '/home/claude/forth-vm-evolution'), ('fast', '/tmp/ff')):
    r = subprocess.run(['python3', '-c', '''
import os, sys, shutil
sys.argv = ["x"]; sys.path.insert(0, "%s/lab/evolve"); import evolve as E
E.setup(); E.long_files()
g = E.canon(E.recorded_genome("3bb2087f9d")); d = os.path.join(E.EV, "kt"); shutil.rmtree(d, ignore_errors=True)
eng, img = E.build(g, d); pw = E.private_work(d)
open("/tmp/kt-%s.txt", "w").write(eng + "\\n" + img + "\\n" + pw + "\\n")
open("/tmp/kt-%s.in", "wb").write(E.program("kernel"))
''' % (tree, name, name)], capture_output=True, text=True)
    if r.returncode: print(r.stderr[-400:])
ts = {'before': [], 'fast': []}
cfg = {n: open('/tmp/kt-%s.txt' % n).read().split('\n')[:3] for n in ts}
inp = {n: open('/tmp/kt-%s.in' % n, 'rb').read() for n in ts}
for k in range(15):
    for n in (('before', 'fast') if k % 2 == 0 else ('fast', 'before')):
        eng, img, pw = cfg[n]
        r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
        subprocess.run([eng, img], input=inp[n], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=pw, timeout=120)
        r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
        ts[n].append((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime))
for n in ts: print('%-6s kernel workload on 3bb2087f9d (JIT): median %.1f ms, min %.1f ms' % (n, statistics.median(ts[n]) * 1000, min(ts[n]) * 1000))
print('ratio of medians %.3f' % (statistics.median(ts['fast']) / statistics.median(ts['before'])))
