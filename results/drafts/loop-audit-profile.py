import os, re, sys, json, shutil, collections, importlib.util
sys.argv = ['evolve.py']
spec = importlib.util.spec_from_file_location('E', '/tmp/fe/b/lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
E.setup()
g = E.canon(E.recorded_genome('0ceb043115'))
d = os.path.join(E.EV, 'loopaudit'); shutil.rmtree(d, ignore_errors=True)
sm, cm = d + '.sym', d + '.map'
os.environ['SYMMAP'] = sm; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
try: eng, img = E.build(dict(g, tail=0, msc=0), d)
finally: E.PROFILING[0] = False; del os.environ['SYMMAP']; del os.environ['CALLMAP']
ranges = []
for l in open(sm):
    a, b, n = l.split(None, 2); ranges.append((int(a), int(b), n.strip()))
ranges.sort()
n_img = int(open(cm).readline().split()[2])
pw = E.private_work(d)
if not E.LONGF: E.long_files()
res = {}
import bisect
starts = [r[0] for r in ranges]
for w in E.WORK_SEL + E.WORK_HELD:
    pf = os.path.join(d, 'prof-' + w)
    E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=60, env=dict(os.environ, VMPROF=pf))
    per, total, runtime = collections.Counter(), 0, 0
    for line in open(pf):
        f = line.split()
        if f[0] != 'I': continue
        a, k = int(f[1]), int(f[2]); total += k
        if a >= n_img: runtime += k; continue
        i = bisect.bisect_right(starts, a) - 1
        if i >= 0 and ranges[i][0] <= a < ranges[i][1]: per[ranges[i][2]] += k
    res[w] = {'total': total, 'runtime': runtime, 'per': dict(per)}
json.dump(res, open('/tmp/fe/loopaudit.json', 'w'))
for w, r in res.items(): print('%-9s %6.1fM dispatches, %4.1f%% in run-time compiled code, top words: %s' % (w, r['total'] / 1e6, 100.0 * r['runtime'] / r['total'],
      ', '.join('%s %.1f%%' % (n, 100.0 * k / r['total']) for n, k in sorted(r['per'].items(), key=lambda kv: -kv[1])[:4])))
