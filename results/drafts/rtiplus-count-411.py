# Iteration 411: does rtiplus change the loop's dispatches on 4ac602c8bd? The profiler's count, with and without it.
import collections, json, os, shutil, sys
os.chdir('/home/claude/forth-vm-evolution'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed60.md') if l.startswith('{"') and '4ac602c8bd' in l)
for v in (0, 1):
    g = E.canon(dict(r['genome'], rtiplus=v)); d = '/tmp/rl/p%d' % v; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False
    pw = E.private_work(d); out = []
    for w in ('loop', 'bubble'):
        pf = os.path.join(d, 'prof-' + w); E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
        by = collections.Counter()
        for line in open(pf):
            f = line.split()
            if f and f[0].isdigit() and not (int(f[0]) == 0x7D or 128 <= int(f[1]) <= 255): by[int(f[1])] += int(f[2])
        out.append('%s %d dispatches (op 17, I: %d)' % (w, sum(by.values()), by[17]))
    print('rtiplus=%d: %s; supers %s' % (v, '; '.join(out), [s for s in E.supers_in(g) if 'I' in s[:2]][:4]), flush=True)
