import json, collections, random, sys, re, os, time
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
E.design_pairs = lambda g, n=24: list(E.SUPER_POOL)      # no profiling builds in the simulation below
R = {}
for l in open('/tmp/s46/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
def kind(h):
    h = h or ''
    for k in ('crossover', 'borrowed', 'mutation', 'carried'):
        if h.startswith(k): return k
    return (h.split(':')[0][:24] or '(none)')
gens = [r['gen'] for r in R.values()]
print('records', len(R), 'generations', min(gens), '-', max(gens))
print('status', collections.Counter(r['status'] for r in R.values()).most_common())
kids = [r for r in R.values() if r['gen'] >= 1]
kc = collections.Counter(kind(r['how']) for r in kids)
print('children (gen >= 1): %d; by the try that made them: %s' % (len(kids), ', '.join('%s %d (%.1f%%)' % (k, n, 100 * n / len(kids)) for k, n in kc.most_common())))
late = [r for r in kids if r['gen'] >= 0.8 * max(gens)]
print('  the last fifth of generations: crossover %.1f%% of %d' % (100 * sum(kind(r['how']) == 'crossover' for r in late) / len(late), len(late)))
print('via the attic: %d children' % sum('via the attic' in (r['how'] or '') for r in kids))
pg = collections.Counter(r['gen'] for r in kids)
print('new designs a generation: median %d, min %d (N 256)' % (sorted(pg.values())[len(pg) // 2], min(pg.values())))
sc = [r for r in kids if r['gen'] >= 5]
print('screened from generation 5: %d of %d (%.1f%%)' % (sum(r['status'] == 'screened' for r in sc), len(sc), 100 * sum(r['status'] == 'screened' for r in sc) / len(sc)))
print('audited mentions:', sum('audit' in json.dumps(r.get('how', '')) for r in R.values()), sum(1 for r in R.values() if r['status'] == 'ok' and 'pred' in r))
# the run's final front, from its report
front = []
for l in open('/tmp/s46/pack/report.md'):
    if l.startswith('## ') and front: break
    m = re.match(r'^\| ([0-9a-f]{10}) \|', l)
    if m: front.append(m.group(1))
print('\nthe front: %d designs' % len(front))
fk = collections.Counter(kind(R[i]['how']) for i in front if i in R)
print('  by the try that made them:', dict(fk), '; via the attic:', sum('via the attic' in (R[i]['how'] or '') for i in front if i in R),
      '; not in this db:', sum(i not in R for i in front))
fr = sorted((R[i] for i in front if i in R and R[i].get('total')), key=lambda r: r['total'])
third = max(1, len(fr) // 3)
for name, part in (('the small third', fr[:third]), ('the middle', fr[third:-third]), ('the fast third (largest)', fr[-third:])):
    g = [p['genome'] for p in part]
    print('  %s (%d, %s-%s bytes, speed %.3f-%.3f): threads %s; fsys %s; klookup %s' % (name, len(part), format(part[0]['total'], ','), format(part[-1]['total'], ','),
          min(p['speed'] for p in part), max(p['speed'] for p in part),
          dict(collections.Counter(x.get('threads', 0) for x in g)), dict(collections.Counter(x.get('fsys', 0) for x in g)), dict(collections.Counter(x.get('klookup', 0) for x in g))))
nk = [R[i]['genome'] for i in front if i in R and not R[i]['genome'].get('klookup')]
print('  without klookup: %d; their threads: %s' % (len(nk), dict(collections.Counter(x.get('threads', 0) for x in nk))))
print('  fsys on the whole front:', dict(collections.Counter(R[i]['genome'].get('fsys', 0) for i in front if i in R)),
      '; threads:', dict(collections.Counter(R[i]['genome'].get('threads', 0) for i in front if i in R)))
# the crossover share: one try of each kind from the front's designs, against everything the run made
seen = set(R); rnd = random.Random(46); par = [i for i in front if i in R]
rep = {'mutation-only': [0, 0], 'crossover': [0, 0]}
t0 = time.time()
for t in range(3000):
    for k in rep:
        p1, p2 = rnd.sample(par, 2)
        g = E.crossover(R[p1]['genome'], R[p2]['genome'], rnd) if k == 'crossover' else E.canon(R[p1]['genome'])
        if rnd.random() < 0.15:
            g, _ = E.borrow(g, R[rnd.choice(par)]['genome'], rnd)
        if rnd.random() < 0.9 or E.gid(g) in seen: g, _ = E.mutate(g, rnd)
        rep[k][0] += E.gid(g) in seen; rep[k][1] += 1
    if time.time() - t0 > 90: break
rm, rx = rep['mutation-only'][0] / rep['mutation-only'][1], rep['crossover'][0] / rep['crossover'][1]
print('\na try from the front against the run\'s %d designs (%d tries each): mutation-only repeats %.1f%%, crossover %.1f%%' % (len(seen), rep['crossover'][1], 100 * rm, 100 * rx))
print('  so at XOVER 0.25 the children kept would be %.1f%% crossover' % (100 * 0.25 * (1 - rx) / (0.25 * (1 - rx) + 0.75 * (1 - rm))))
# deaths by cause, corpus deaths; the new genes on the front
dead = [r for r in R.values() if r['status'] not in ('ok', 'screened')]
print('\nnot alive: %d; by status: %s' % (len(dead), collections.Counter(r['status'] for r in dead).most_common(8)))
why = collections.Counter((r.get('why') or r.get('error') or '')[:60] for r in dead)
print('  by cause (first 60 chars):', why.most_common(8))
print('  corpus deaths:', sum('corpus' in json.dumps(r.get('why', '')) for r in dead))
fg = [R[i]['genome'] for i in front if i in R]
for gname in ('jitos', 'jit', 'jitx', 'jitloop', 'jitinl', 'fbuf', 'tag2', 'tos', 'tail', 'bytehdr'):
    print('  %s on the front: %s' % (gname, dict(collections.Counter(E.express(E.canon(x)).get(gname, 0) for x in fg))))
