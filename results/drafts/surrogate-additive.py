import json, math, bisect, random, pickle, collections, sys, importlib.util, time
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('E', '/tmp/fe/a/lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
R = [json.loads(l) for l in open('/tmp/s40/run/pack/db.jsonl') if l.strip()]
ok = [r for r in R if r['status'] == 'ok' and r.get('total') and r.get('speed')]
final = pickle.load(open('/tmp/fe/sur2.pkl', 'rb'))['final']
def feats(g):
    f = []
    for k, v in E.express(g).items():
        if isinstance(v, (list, tuple)): f += ['%s:%s' % (k, json.dumps(x)) for x in v]
        else: f.append('%s=%s' % (k, json.dumps(v)))
    return f
CUT = 68; t0 = time.time()
F = {r['id']: feats(r['genome']) for r in ok}
tr = [r for r in ok if r.get('gen', 0) <= CUT]; te = [r for r in ok if r.get('gen', 0) > CUT]
def fit(k, epochs=25, lr=0.02, lam=1e-5):
    w = collections.defaultdict(float); b = sum(math.log(r[k]) for r in tr) / len(tr); rnd = random.Random(1); idx = list(range(len(tr)))
    for ep in range(epochs):
        rnd.shuffle(idx); a = lr / (1 + ep * 0.2)
        for i in idx:
            r = tr[i]; fs = F[r['id']]; e = b + sum(w[f] for f in fs) - math.log(r[k])
            for f in fs: w[f] -= a * (e + lam * w[f])
            b -= a * e * 0.1
    return lambda r: math.exp(b + sum(w.get(f, 0.0) for f in F[r['id']]))
M = {k: fit(k) for k in ('speed', 'total')}
print('fitted in %.0f s (pure Python)' % (time.time() - t0))
for k in ('speed', 'total'):
    e = sorted(abs(M[k](r) / r[k] - 1) for r in te); n = len(e)
    print('additive %-5s: median error %.2f%%, 90%% within %.1f%%' % (k, 100 * e[n // 2], 100 * e[9 * n // 10]))
pred = {r['id']: (M['speed'](r), M['total'](r)) for r in te}
by_gen = collections.defaultdict(list)
for r in ok: by_gen[r.get('gen', 0)].append(r)
def run(ms, mt):
    sp, tt = [], []
    def add(s, t):
        k = bisect.bisect_right(sp, s)
        if k and tt[k - 1] <= t: return
        j = k
        while j < len(sp) and tt[j] >= t: j += 1
        sp[k:j] = [s]; tt[k:j] = [t]
    def beaten(s, t):
        k = bisect.bisect_right(sp, s * (1 - ms)); return k > 0 and tt[k - 1] <= t * (1 - mt)
    for g in range(0, CUT + 1):
        for r in by_gen[g]: add(r['speed'], r['total'])
    skipped = lost = n = fin = 0
    for g in range(CUT + 1, 137):
        for r in by_gen[g]:
            n += 1; fin += r['id'] in final; ps, pt = pred[r['id']]
            if beaten(ps, pt): skipped += 1; lost += r['id'] in final
        for r in by_gen[g]: add(r['speed'], r['total'])
    return n, skipped, lost, fin
for ms, mt in ((0.30, 0.05), (0.20, 0.02), (0.10, 0.02)):
    n, s, l, f = run(ms, mt)
    print('  additive screen %d%%/%d%%: %2.0f%% skipped, final-front lost %d of %d (random: %.0f)' % (100 * ms, 100 * mt, 100.0 * s / n, l, f, f * s / n))
