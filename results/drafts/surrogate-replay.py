import json, bisect, pickle, collections
d = pickle.load(open('/tmp/fe/sur2.pkl', 'rb')); P, final = d['pred'], d['final']
R = []
for l in open('/tmp/s40/run/pack/db.jsonl'):
    try: R.append(json.loads(l))
    except ValueError: pass
ok = [r for r in R if r['status'] == 'ok' and r.get('total') and r.get('speed')]
by_gen = collections.defaultdict(list)
for r in ok: by_gen[r.get('gen', 0)].append(r)
CUT = 68
def run(ms, mt):
    sp, tt = [], []          # the staircase: speeds ascending, totals descending
    def add(s, t):
        k = bisect.bisect_right(sp, s)
        if k and tt[k - 1] <= t: return
        j = k
        while j < len(sp) and tt[j] >= t: j += 1
        sp[k:j] = [s]; tt[k:j] = [t]
    def beaten(s, t):
        k = bisect.bisect_right(sp, s * (1 - ms))
        return k > 0 and tt[k - 1] <= t * (1 - mt)
    for g in range(0, CUT + 1):
        for r in by_gen[g]: add(r['speed'], r['total'])
    skipped = lost = n = fin = 0
    for g in range(CUT + 1, 137):
        for r in by_gen[g]:
            n += 1; fin += r['id'] in final
            if beaten(P['speed'][r['id']], P['total'][r['id']]): skipped += 1; lost += r['id'] in final
        for r in by_gen[g]: add(r['speed'], r['total'])
    return n, skipped, lost, fin
for ms, mt in ((0.05, 0.0), (0.10, 0.0), (0.10, 0.02), (0.20, 0.02), (0.30, 0.05)):
    n, s, l, f = run(ms, mt)
    print('skip if predicted %2d%% slower and %d%% bigger than the front: %5d of %d children skipped (%2.0f%%); final-front designs lost %d of %d (random skipping at that rate: %.0f)'
          % (100 * ms, 100 * mt, s, n, 100.0 * s / n, l, f, f * s / n))
