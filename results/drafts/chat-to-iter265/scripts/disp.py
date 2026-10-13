import os, sys, shutil, collections, bisect
TREE = sys.argv[1]; ids = sys.argv[2].split(',')
sys.argv = ['x']; sys.path.insert(0, TREE + '/lab/evolve'); import evolve as E
E.setup()
for did in ids:
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'disp'); shutil.rmtree(d, ignore_errors=True); sm = d + '.sym'
    os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
    syms = sorted((int(a), int(b), n.strip()) for a, b, n in (l.split(' ', 2) for l in open(sm))); starts = [s[0] for s in syms]
    pw = E.private_work(d); out = []
    for w in ('corpus', 'kernel', 'parse', 'fib'):
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=30, env=dict(os.environ, VMPROF=pf))
        by, total = collections.Counter(), 0
        for line in open(pf):
            f = line.split()
            if f and f[0] == 'I':
                a, k = int(f[1]), int(f[2]); total += k; i = bisect.bisect_right(starts, a) - 1
                by[syms[i][2] if i >= 0 and a < syms[i][1] else '?'] += k
        out.append('%s %d (NEXT-NFA8 %d)' % (w, total, by['NEXT-NFA8']))
    print('%s %s: %s' % (TREE, did, ' | '.join(out)), flush=True)
