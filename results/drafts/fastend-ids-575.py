#!/usr/bin/env python3
"""results/drafts/fastend-ids-575.py DB --seed N [--out FILE] - the fast-end re-measure's designs (Iteration 575).

Seed 84 (the confirmation run) was NOT CONFIRMED by its fastest (0.1325, the bar 0.1350) and by the stricter test (the
bred designs +1.19% to the pool, the bar 1%) - both at the fast end, by about the session spread (results/
evolve-amd-ryzen-7-pro-8840hs-seed84.md, "Judged"). The owner (575): re-measure both sides in one session before
another confirmation run - loadtest.py --ids FILE on fury, alone and under load at both widths. FILE, one record a line
as final-set.py --candidates writes them (the in-run numbers, the genome), holds:
  - the run's bred designs as fast as its best re-timed founder or faster (speed), and its 4 fastest bred at 32 bits;
  - the run's 4 fastest re-timed founders (generation 0), at 64 bits;
  - the pool's (confirm.py's: the method's results files) 8 fastest and 4 fastest at 32 bits, their own runs' records.
A design in both the pool and the run keeps the pool's record - its in-run number from its own run.
Run from the repository root."""
import json, sys
sys.path.insert(0, 'lab/evolve')
import hv, stopping, confirm

a = sys.argv[1:]; db = a[0]; N = int(a[a.index('--seed') + 1])
out = a[a.index('--out') + 1] if '--out' in a else 'results/fastend-remeasure-575.md'
sys.argv = ['x']; import evolve as E
_, runs = stopping.series(stopping.LEDGER)
runs = [r for r in runs if r['seed'] < N] + confirm.confirmations(stopping.LEDGER, N)
P = {}
for f in confirm.pool_files(runs):
    for i, r in hv.load(f, E).items(): P[i] = dict(r, _from=f.split('-seed')[-1].split('.')[0])
R = hv.load(db, E)
ok = lambda r: r.get('status') == 'ok' and r.get('speed') and r.get('speed32') and r.get('genome')
alive = [r for r in R.values() if ok(r)]
bred = [r for r in alive if (r.get('gen') or 0) >= 1 and not str(r.get('how', '')).startswith(confirm.CARRIED)]
found = sorted((r for r in alive if (r.get('gen') or 0) == 0), key=lambda r: r['speed'])
pool = [r for r in P.values() if ok(r)]
pick = {}
def take(rs, why, k=None):
    for r in rs[:k]:
        if r['id'] not in pick: pick[r['id']] = (P.get(r['id']) or r, why)
take(sorted((r for r in bred if r['speed'] <= found[0]['speed']), key=lambda r: r['speed']), 'seed %d bred, as fast as its best founder' % N)
take(sorted(bred, key=lambda r: r['speed32']), 'seed %d bred, fastest at 32 bits' % N, 4)
take(found, 'seed %d founder re-timed' % N, 4)
take(sorted(pool, key=lambda r: r['speed']), 'the pool, fastest', 8)
take(sorted(pool, key=lambda r: r['speed32']), 'the pool, fastest at 32 bits', 4)
with open(out, 'w') as o:
    for i, (r, why) in sorted(pick.items(), key=lambda kv: kv[1][0]['speed']):
        o.write(json.dumps(dict({k: v for k, v in r.items() if not k.startswith('_')}, why=why, run=r.get('_from', 'seed%d' % N))) + '\n')
for i, (r, why) in sorted(pick.items(), key=lambda kv: kv[1][0]['speed']):
    print('%s  %.4f  %.4f  %-8s %s' % (i, r['speed'], r['speed32'], r.get('_from', 'seed%d' % N), why))
print('%d designs -> %s' % (len(pick), out))
