import json, math, bisect, re, pickle, collections, statistics as st
R = {}
for l in open('/tmp/s40/run/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
ok = {i: r for i, r in R.items() if r['status'] == 'ok' and r.get('total') and r.get('speed')}
final = pickle.load(open('/tmp/fe/sur2.pkl', 'rb'))['final']
CUT = 68
def changes(h):
    m = re.search(r'mutation: ([^;]*)', h)
    return [x.strip() for x in m.group(1).split(',')] if m else []
def pmean(r, k):
    ps = [ok[p][k] for p in r.get('parents', []) if p in ok]
    return math.exp(sum(math.log(v) for v in ps) / len(ps)) if ps else None
# learn: the mean log effect of each change token, from training children with measured parents
eff = {k: collections.defaultdict(list) for k in ('speed', 'total')}
for r in ok.values():
    if r.get('gen', 0) > CUT or not r.get('gen'): continue
    ch = changes(r['how'])
    for k in ('speed', 'total'):
        pm = pmean(r, k)
        if pm and len(ch) == 1 and 'crossover' not in r['how']: eff[k][ch[0]].append(math.log(r[k] / pm))
E = {k: {c: st.mean(v) for c, v in d.items() if len(v) >= 3} for k, d in eff.items()}
test = [r for r in ok.values() if r.get('gen', 0) > CUT]
def predict(r, k, model):
    pm = pmean(r, k)
    if pm is None: return None
    if model == 'parents': return pm
    return pm * math.exp(sum(E[k].get(c, 0.0) for c in changes(r['how'])))
P = {}
for model in ('parents', 'parents+deltas'):
    for k in ('speed', 'total'):
        errs = [abs(predict(r, k, model) / r[k] - 1) for r in test if predict(r, k, model)]
        errs.sort(); n = len(errs)
        print('%-15s %-5s: %d predicted (of %d), median error %.2f%%, 90%% within %.1f%%' % (model, k, n, len(test), 100 * errs[n // 2], 100 * errs[9 * n // 10]))
    P[model] = {r['id']: (predict(r, 'speed', model), predict(r, 'total', model)) for r in test}
by_gen = collections.defaultdict(list)
for r in ok.values(): by_gen[r.get('gen', 0)].append(r)
def run(pred, ms, mt):
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
            n += 1; fin += r['id'] in final; ps, pt = pred.get(r['id'], (None, None))
            if ps and pt and beaten(ps, pt): skipped += 1; lost += r['id'] in final
        for r in by_gen[g]: add(r['speed'], r['total'])
    return n, skipped, lost, fin
for model in P:
    for ms, mt in ((0.30, 0.05), (0.20, 0.02), (0.10, 0.02)):
        n, s, l, f = run(P[model], ms, mt)
        print('  %-15s screen %d%%/%d%%: %2.0f%% skipped, final-front lost %d of %d (random: %.0f)' % (model, 100 * ms, 100 * mt, 100.0 * s / n, l, f, f * s / n))
