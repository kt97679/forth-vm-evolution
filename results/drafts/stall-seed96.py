#!/usr/bin/env python3
"""results/drafts/stall-seed96.py PACK CHAINLOG RESULTS95 (Iteration 704) - seed 96's stall in generation 0, read by the
ticker (701's machine line, its first run) and from the database: the ticks with a load over 10 or a late tick, the carried
designs that died of a time limit (timed out, cc past its CPU limit, a compiler crash), each looked up among seed 95's
front records (RESULTS95's JSON lines), and seed 96's true front measured again with those found restored as seed 95 read
them - so a design lost to the stall is shown to change the verdict or not. Reads only. Run with python3 -I -B."""
import json, os, re, sys

pack, chainlog, res95 = sys.argv[1:4]
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E
import hv

print('the ticks - a load over 10 or a late tick:')
for l in open(chainlog, errors='replace'):
    if l.startswith('next-run: progress'):
        m = re.search(r'load ([0-9.]+)', l)
        if (m and float(m.group(1)) > 10) or 'late' in l:
            print('  ' + re.sub(r'no generation yet, 0 designs in the database, |the evolution stops in ', '', l[19:].strip()))

TIME = ('timed out', 'CPU time limit', 'Program arguments')
db = pack + '/db.jsonl'
dead = []
for l in open(db, errors='replace'):
    if '"died' in l and any(t in l for t in TIME):
        r = json.loads(l)
        dead.append((r['id'], r.get('gen'), r['status'][:60], str(r.get('how', ''))[:40]))
print('\nthe deaths of a time limit: %d, generations %s' % (len(dead), sorted({d[1] for d in dead})))

old = {}
for l in open(res95, errors='replace'):
    if l.startswith('{'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id') in {d[0] for d in dead}:
            old[r['id']] = r
for d in dead:
    r = old.get(d[0])
    print('  %s gen %s %-45s %s' % (d[0], d[1], d[2], 'on seed 95\'s front: speed %.4f, 32-bit %.4f, %d B, %d KB'
          % (r['speed'], r['speed32'], r['total'], r['rss']) if r else 'not among seed 95\'s front records'))

R = hv.load(db, E)
b = json.load(open(hv.BOUNDS))
m0 = hv.measure(db, E, b, R=dict(R))
for i, r in old.items():
    r = dict(r, status='ok', gen=0)
    r['total'] = E.ov(r, 'total')
    R[i] = r
m1 = hv.measure(db, E, b, R=R)
for name, m in (('as run', m0), ('%d restored' % len(old), m1)):
    print('%s: true front %d, hypervolume %.5f; alive extremes: fastest %.4f, smallest %d, memory %d KB, 32-bit %.4f'
          % (name, m['front'], m['hv'], m['alive']['fastest'], m['alive']['smallest'], m['alive']['memory'],
             m['alive']['fastest32']))
