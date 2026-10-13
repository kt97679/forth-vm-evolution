#!/usr/bin/env python3
"""seed-facts.py DB RESULTS - step 3 of processing a returned seed (Iteration 256).

DB: the run pack's db.jsonl; RESULTS: its results file (or the pack's
report.md) - the front's records. Prints what the results file's facts list
carries: designs by status; deaths by cause, and for each cause the gene values
nearly all its designs share and the living rarely do (seed 46: every "engine
did not compile" had tail=1, no living design had it - found late, by hand);
the screen; children by the try that made them, the last fifth's crossover,
the attic; the front by how made, its thirds by size (fsys, threads, klookup),
and the main genes on it; and a try from the front against everything the run
made (how often mutation alone and crossover repeat a design).

    python3 lab/evolve/seed-facts.py /tmp/s46/pack/db.jsonl results/evolve-amd-ryzen-7-pro-8840hs-seed46.md

Until Iteration 256 this lived in /tmp, rewritten each time.
"""
import collections, json, os, random, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) != 3: sys.exit(__doc__)
db, results = sys.argv[1], sys.argv[2]
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E

E.design_pairs = lambda g, n=24: list(E.SUPER_POOL)      # no profiling builds in the simulation below
R = {}
for l in open(db):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
EX = {}
def ex(r):
    if r['id'] not in EX: EX[r['id']] = E.express(E.canon(r['genome']))
    return EX[r['id']]
def val(e, k):
    v = e.get(k)
    return json.dumps(v, sort_keys=True) if isinstance(v, (list, dict)) else str(v if v is not None else 0)
def kind(h):
    h = h or ''
    for k in ('crossover', 'borrowed', 'mutation', 'carried'):
        if h.startswith(k): return k
    return h.split(':')[0][:24] or '(none)'

gens = [r['gen'] for r in R.values()]
st = collections.Counter(r['status'] for r in R.values())
print('records %d, generations %d-%d' % (len(R), min(gens), max(gens)))
print('by status:', ', '.join('%s %d' % kv for kv in st.most_common()))

# deaths by cause, and what each cause's designs share
alive = [r for r in R.values() if r['status'] == 'ok']
for cause, n in st.most_common():
    if cause in ('ok', 'screened') or n < 20: continue
    dead = [r for r in R.values() if r['status'] == cause]
    genes = set(k for r in dead[:200] for k in ex(r))
    shared = []
    for k in genes:
        c = collections.Counter(val(ex(r), k) for r in dead)
        v, m = c.most_common(1)[0]
        if m < 0.95 * len(dead) or v in ('0', 'None', '[]', 'False'): continue
        a = sum(val(ex(r), k) == v for r in alive)
        if a < 0.5 * len(alive): shared.append('%s=%s (%d of %d; alive with it: %d of %d)' % (k, v[:30], m, len(dead), a, len(alive)))
    print('  %s - %d%s' % (cause, n, (': shared, and rare among the living: ' + '; '.join(sorted(shared)[:6])) if shared else ''))

kids = [r for r in R.values() if r['gen'] >= 1]
sc = [r for r in kids if r['gen'] >= 5]
print('screened from generation 5: %d of %d (%.1f%%)' % (sum(r['status'] == 'screened' for r in sc), len(sc), 100 * sum(r['status'] == 'screened' for r in sc) / max(1, len(sc))))
kc = collections.Counter(kind(r['how']) for r in kids)
print('children %d by the try that made them: %s' % (len(kids), ', '.join('%s %d (%.1f%%)' % (k, n, 100 * n / len(kids)) for k, n in kc.most_common())))
late = [r for r in kids if r['gen'] >= 0.8 * max(gens)]
print('  the last fifth: crossover %.1f%% of %d' % (100 * sum(kind(r['how']) == 'crossover' for r in late) / max(1, len(late)), len(late)))
print('  via the attic: %d children' % sum('via the attic' in (r['how'] or '') for r in kids))

front = [json.loads(l)['id'] for l in open(results) if l.startswith('{"bin"')]
fr = [R[i] for i in front if i in R]
print('\nthe front: %d designs (%d not in the db); by how made: %s; via the attic %d' % (
    len(front), len(front) - len(fr), dict(collections.Counter(kind(r['how']) for r in fr)), sum('via the attic' in (r['how'] or '') for r in fr)))
fs = sorted((r for r in fr if r.get('total')), key=lambda r: r['total'])
third = max(1, len(fs) // 3)
for name, part in (('the small third', fs[:third]), ('the middle', fs[third:-third]), ('the fast third', fs[-third:])):
    if not part: continue
    e = [ex(p) for p in part]
    print('  %s (%d, %s-%s bytes, speed %.3f-%.3f): fsys %s; threads %s; klookup %s' % (
        name, len(part), format(part[0]['total'], ','), format(part[-1]['total'], ','), min(p['speed'] for p in part), max(p['speed'] for p in part),
        dict(collections.Counter(x.get('fsys', 0) for x in e)), dict(collections.Counter(x.get('threads', 0) for x in e)),
        dict(collections.Counter(int(bool(x.get('klookup'))) for x in e))))
for k in ('jit', 'jitx', 'jitloop', 'jitinl', 'jittail', 'jitos', 'tail', 'msc', 'tos', 'tag2', 'guard', 'rtloop', 'fbuf'):
    c = collections.Counter(val(ex(r), k) for r in fr)
    print('  %-8s on the front: %s' % (k, ', '.join('%s %d' % kv for kv in sorted(c.items()))))

seen = set(R); rnd = random.Random(len(R)); par = [r['id'] for r in fr]
rep = {'mutation-only': [0, 0], 'crossover': [0, 0]}; t0 = time.time()
while len(par) >= 2 and time.time() - t0 < 60:
    for k in rep:
        p1, p2 = rnd.sample(par, 2)
        g = E.crossover(R[p1]['genome'], R[p2]['genome'], rnd) if k == 'crossover' else E.canon(R[p1]['genome'])
        if rnd.random() < 0.15: g, _ = E.borrow(g, R[rnd.choice(par)]['genome'], rnd)
        if rnd.random() < 0.9 or E.gid(g) in seen: g, _ = E.mutate(g, rnd)
        rep[k][0] += E.gid(g) in seen; rep[k][1] += 1
if rep['crossover'][1]:
    print('\na try from the front against the run\'s %d designs (%d tries each): mutation alone repeats %.1f%%, crossover %.1f%%' % (
        len(seen), rep['crossover'][1], 100 * rep['mutation-only'][0] / rep['mutation-only'][1], 100 * rep['crossover'][0] / rep['crossover'][1]))
