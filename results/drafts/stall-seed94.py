#!/usr/bin/env python3
"""results/drafts/stall-seed94.py DB.jsonl - seed 94's stall at generations 43-44 (Iteration 700), from its database:
the deaths by generation, the 32-bit extreme 2806f89619 against its parent workload by workload, the least-memory
designs, and whether any design the stall killed would have been on the front. The kernel timed here:
results/drafts/ktime-seed94.py. Run with python3 -I."""
import json, math, sys
from collections import defaultdict

db = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
by = defaultdict(list)
for r in db: by[r['id']].append(r)
env = lambda s: 'timed out' in s or 'CPU time' in s
dg = defaultdict(lambda: defaultdict(int))
for r in db:
    if env(r['status']): dg[r.get('gen')]['timed out' if 'timed out' in r['status'] else 'cc CPU limit'] += 1
print('the timed-out and cc-CPU-limit deaths by generation:', {g: dict(v) for g, v in sorted(dg.items())})
w32 = [r for r in db if r.get('why32')]
print('the 32-bit failures:', ', '.join('%s gen %s (%s...)' % (r['id'], r.get('gen'), r['why32'][:40]) for r in w32))

W = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps']
x = by['2806f89619'][0]; p = by[x['parents'][0]][0]
for n, r in (('2806f89619', x), ('parent ' + p['id'], p)):
    print('%-18s gen %s speed32 %.4f  ' % (n, r['gen'], r['speed32']) + ' '.join('%s %.3f' % (w, r['t32'][w]) for w in W))
t = dict(x['t32']); t['kernel'] = p['t32']['kernel']
print('2806f89619 with its parent\'s 32-bit kernel: speed32 %.4f' % math.prod(t.values()) ** (1 / len(t)))
ok = sorted((r for r in db if r['status'] == 'ok' and r.get('speed32')), key=lambda r: r['speed32'])
k = sorted(r['t32']['kernel'] for r in ok[:50])
print('the 32-bit kernel over the 50 fastest at 32 bits: lowest %.3f, next %.3f, median %.3f' % (k[0], k[1], k[25]))
print('the fastest at 32 bits without it:', ', '.join('%s %.4f' % (r['id'], r['speed32']) for r in ok if r['id'] != '2806f89619')[:60])

alive = [r for r in db if r['status'] == 'ok' and r.get('rss')]
low = sorted(alive, key=lambda r: r['rss'])[:2]
print('the least memory:', ', '.join('%s %d KB gen %s (%s)' % (r['id'], r['rss'], r.get('gen'), (r.get('how') or '')[:50]) for r in low))

K = lambda r: (r['speed'], r['total'], r['rss'], r['speed32'])
pool = [r for r in ok if r['id'] != '2806f89619' and r.get('speed')]
dom = lambda v: any(all(a <= b for a, b in zip(K(q), v)) and any(a < b for a, b in zip(K(q), v)) for q in pool)
dead = [r for r in db if env(r['status'])]
meas = [r for r in dead if r.get('speed') and r.get('speed32')]
print('killed by the stall: %d, %d measured before (all four objectives) - %d of them undominated; %d never measured'
      % (len(dead), len(meas), sum(1 for r in meas if not dom(K(r))), len(dead) - len(meas)))
print('2806f89619 with the corrected speed32:', 'dominated' if dom((x['speed'], x['total'], x['rss'], 0.1672)) else 'undominated')
