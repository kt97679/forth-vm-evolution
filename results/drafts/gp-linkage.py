import json, re, math, collections, statistics as st, sys, importlib.util
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('E', '/tmp/fe/r/lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
# noise: recorded vs re-measured, the same designs, session 35
L = open('/tmp/s40/cmp/pack/compare-fronts.md').read().split('\n'); hi = next(i for i, l in enumerate(L) if l.startswith('| run |'))
hdr = [x.strip() for x in L[hi].split('|')]; a, b = hdr.index('speed now'), hdr.index('recorded'); q = []
for l in L[hi + 2:]:
    c = [x.strip() for x in l.split('|')]
    try: q.append(float(c[a]) / float(c[b]))
    except (ValueError, IndexError, ZeroDivisionError): pass
q.sort(); print('speed re-measured / recorded, %d designs: median %.3f, 10-90%% %.3f-%.3f, 5-95%% %.3f-%.3f' % (len(q), q[len(q)//2], q[len(q)//10], q[9*len(q)//10], q[len(q)//20], q[19*len(q)//20]))
# linkage: mutual information of expressed gene values over the final front
R = {}
for l in open('/tmp/s40/run/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
ok = {i: r for i, r in R.items() if r['status'] == 'ok' and r.get('rss')}
obj = lambda r: (r['speed'], r.get('total', r['size']), r['rss'])
def dom(x, y): return all(u <= v for u, v in zip(x, y)) and x != y
pts = sorted((obj(r), i) for i, r in ok.items()); front, best = [], []
for o, i in pts:
    if not any(dom(p, o) for p in best): front.append(i); best = [p for p in best if not dom(o, p)] + [o]
ex = [E.express(ok[i]['genome']) for i in front]
genes = sorted(set(k for e in ex for k in e if not isinstance(e.get(k), (list, tuple)) or k in ('spec',)))
val = {g: [json.dumps(e.get(g), sort_keys=True) for e in ex] for g in genes}
def H(xs): c = collections.Counter(xs); n = len(xs); return -sum(v / n * math.log(v / n) for v in c.values())
def MI(x, y): return H(x) + H(y) - H(list(zip(x, y)))
var = [g for g in genes if H(val[g]) > 0.05]
pairs = sorted(((MI(val[g], val[h]) / (min(H(val[g]), H(val[h])) or 1), g, h) for i, g in enumerate(var) for h in var[i + 1:]), reverse=True)
blocks = [set(b) for b in E.BLOCKS]
print('\nlinkage on the final front (%d designs, %d varying genes): normalised MI, top 14; * = already in one of the hand-made BLOCKS' % (len(front), len(var)))
for m, g, h in pairs[:14]: print('  %.2f  %-10s %-10s %s' % (m, g, h, '*' if any(g in b and h in b for b in blocks) else ''))
print('  hand-made BLOCKS: %d groups, %d of them with 2+ varying genes' % (len(blocks), sum(len(b & set(var)) > 1 for b in blocks)))
print('  genes never varying on the front: %s' % ', '.join(g for g in genes if H(val[g]) <= 0.05))
