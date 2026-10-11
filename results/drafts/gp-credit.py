import json, re, math, collections, statistics as st, sys
R = {}
for l in open('/tmp/s40/run/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
ok = {i: r for i, r in R.items() if r['status'] == 'ok' and r.get('rss')}
obj = lambda r: (r['speed'], r.get('total', r['size']), r['rss'])
def dom(a, b): return all(x <= y for x, y in zip(a, b)) and a != b
# the final front (exact, by sorting on speed)
pts = sorted((obj(r), i) for i, r in ok.items()); front = set(); best = []
for o, i in pts:
    if not any(dom(p, o) for p in best): front.add(i); best = [p for p in best if not dom(o, p)] + [o]
print('designs %d, alive %d, final front %d' % (len(R), len(ok), len(front)))
# 1. operator credit: per operator kind and per mutated gene
kinds = collections.defaultdict(lambda: [0, 0, 0, 0])   # made, alive, not dominated by a parent, on the final front
def tally(key, r, i):
    t = kinds[key]; t[0] += 1
    if r['status'] != 'ok': return
    t[1] += 1
    ps = [ok[p] for p in r.get('parents', []) if p in ok]
    if ps and r.get('rss') and not any(dom(obj(p), obj(r)) for p in ps): t[2] += 1
    if i in front: t[3] += 1
for i, r in R.items():
    if not r.get('gen'): continue
    h = r['how']
    ops = (['crossover'] if 'crossover' in h else []) + (['borrow'] if 'borrowed' in h else [])
    m = re.search(r'mutation: ([^;]*)', h)
    genes = [g.split('=')[0].split(' ')[0].strip() for g in m.group(1).split(',')] if m else []
    tally('op: ' + ('+'.join(ops) or 'mutation only') + (' + mutation' if ops and genes else ''), r, i)
    for g in set(genes): tally('gene: ' + g, r, i)
print('\n| variation | made | alive | not dominated by a parent | on the final front |\n|---|---|---|---|---|')
for k, (n, a, nd, f) in sorted(kinds.items(), key=lambda kv: -kv[1][0]):
    if k.startswith('op:'): print('| %s | %d | %.1f%% | %.1f%% | %d |' % (k[4:], n, 100.0 * a / n, 100.0 * nd / n, f))
G = sorted(((k[6:], v) for k, v in kinds.items() if k.startswith('gene:') and v[0] >= 150), key=lambda kv: -kv[1][2] / kv[1][0])
print('\nmutated gene: made, not dominated by a parent, on the final front - the 8 most and 8 least productive (of %d with 150+)' % len(G))
for g, (n, a, nd, f) in G[:8] + [('...', (1, 0, 0, 0))] + G[-8:]: print('  %-10s %6d  %5.1f%%  %3d' % (g, n, 100.0 * nd / n, f))
# 2. evaluation cost
secs = [r['secs'] for r in R.values() if r.get('secs')]
print('\nevaluation secs: median %.1f, 90%% %.1f, total %.1f h; died ones %.1f h' % (st.median(secs), sorted(secs)[int(.9 * len(secs))], sum(secs) / 3600, sum(r.get('secs') or 0 for r in R.values() if r['status'] != 'ok') / 3600))
# 3. workload correlations (log speed ratios over the alive designs)
W = sorted(next(iter(ok.values()))['t']); X = {w: [math.log(r['t'][w]) for r in ok.values() if all(r['t'].get(v) for v in W)] for w in W}
def corr(a, b):
    ma, mb = st.mean(a), st.mean(b); sa, sb = st.pstdev(a), st.pstdev(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (len(a) * sa * sb)
print('\nworkload correlations (log time ratios, %d alive designs):' % len(X[W[0]]))
print('          ' + ' '.join('%8s' % w[:8] for w in W))
for w in W: print('%-9s ' % w[:9] + ' '.join('%8.2f' % corr(X[w], X[v]) for v in W))
