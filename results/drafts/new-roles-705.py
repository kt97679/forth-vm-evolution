#!/usr/bin/env python3
"""results/drafts/new-roles-705.py LIST ARMLIST HOLDERS DB96 RESULTS92 ... RESULTS95 [--k K] [--band B] - the new roles'
candidates, the screen chain's two lists (Iteration 705; the owner: "let's go straight to the new designs" - the plan's
step 6, no confirmation run; the 573 rule's 5 % band, two chains: this screen, then a shortlist). Reads only.

The pool: the series' records - seeds 92-95's results files (each run's front, in-run) and seed 96's database (every alive
design: its own and the strict fronts of seeds 92-95 carried in and measured again in its generation 0); a design in
several, the newest alive record (a death in seed 96 - its stall - never hides an earlier alive reading). By final-set.py's
select() to K and candidates() (the owner's 573: the set by hypervolume, every alive design within B of the fastest at
either width, the 5 smallest, the 5 leanest, every design merged into the set's) and the knee, twice:
  - the whole pool - the x86 roles (the fastest on x86-64 and on x86-32, the best mean, the smallest JIT design);
  - its JIT-free designs (evolve.jit_on false) - the portable roles (the fastest over the three classes, the fastest on
    ARMv7, the knee, small and fast on ARMv7, the least memory, the smallest);
then the JIT-free true front's every design after merging (no in-run reading sees ARMv7: the screen for the ARM roles),
the 5 smallest JIT designs, and the ten holders (HOLDERS: results/drafts/holders-705.py's records - today's measure; the
two the pool holds, the pool's record).
LIST: every candidate (the laptop and dream, both widths). ARMLIST: the JIT-free ones, the whole pool's set (a JIT design
on ARMv7 is its JIT-off build - the best mean's third class) and the holders (the Tegra). One record a line with "why" and
"src" (loadtest.py --ids FILE and xcheck.py --also @FILE read them). stdout: the counts and each role's in-run best."""
import collections, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, '..', '..', 'lab', 'evolve')
A = sys.argv[1:]
k, band = 30, 0.05
if '--k' in A: j = A.index('--k'); k = int(A[j + 1]); del A[j:j + 2]
if '--band' in A: j = A.index('--band'); band = float(A[j + 1]); del A[j:j + 2]
out, armout, holders, db96, files = A[0], A[1], A[2], A[3], A[4:]
sys.argv = ['x']; sys.path.insert(0, LAB)
import evolve as E
import hv, appsize
spec = importlib.util.spec_from_file_location('final_set', os.path.join(LAB, 'final-set.py'))
FS = importlib.util.module_from_spec(spec); spec.loader.exec_module(FS)
b = json.load(open(hv.BOUNDS))

alive = lambda r: r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss') and r.get('speed32')
R, src = {}, {}
for f in files + [db96]:
    for i, r in hv.load(f, E).items():
        if alive(r) or i not in R:
            R[i] = r; src[i] = os.path.basename(f) if f != db96 else 'seed96-db.jsonl'
R = {i: r for i, r in R.items() if alive(r)}
keys = collections.Counter(appsize.size_key(r) for r in R.values())
print('The pool: %d alive designs (%s); sizes by the programs counted: %s' % (
    len(R), ', '.join('%d from %s' % (n, s) for s, n in collections.Counter(src[i] for i in R).most_common()), dict(keys)))
assert set(keys) == {5}, 'two sizes in the pool'
pool = set(R)
jit = {i for i, r in R.items() if E.jit_on(E.canon(E.require(dict(r['genome']))))}

C = {}
add = lambda i, w: C.setdefault(i, []).append(w)
ARM = set()
for name, P in (('all', R), ('JIT-free', {i: r for i, r in R.items() if i not in jit})):
    res = FS.select(P, E, b, k)
    cand = FS.candidates(P, res, band=band)
    print('%s: %d designs, the true front %d (%d after merging), the set %d (%.1f%% of the front\'s hypervolume), '
          'candidates %d, the knee %s' % (name, len(P), res['front'], len(res['kept']), len(res['set']),
                                          100 * res['hv_set'] / res['hv_front'], len(cand), res['knee']))
    for i, ws in cand.items():
        for w in ws: add(i, '%s: %s' % (name, w))
    if res['knee']: add(res['knee'], '%s: the knee' % name)
    if name == 'all':
        ARM |= {i for i, _, _ in res['set']}
    else:
        for i in res['kept']: add(i, 'JIT-free: the true front, merged (the ARM screen)')
for i in sorted(jit, key=lambda i: (R[i]['total'], R[i]['speed'], i))[:5]:
    add(i, 'the 5 smallest JIT designs')
H = [json.loads(l) for l in open(holders) if l.startswith('{')]
for h in H:
    role = h['why'].split(': ', 1)[1].split(' (')[0]
    if h['id'] in pool: add(h['id'], 'a holder: %s (results/relf-designs-649.md; the pool\'s record)' % role)
    else:
        R[h['id']] = h; src[h['id']] = 'holders-705.py'
        add(h['id'], 'a holder: %s (results/relf-designs-649.md; measured here - holders-705.py)' % role)
    ARM.add(h['id'])
ARM |= {i for i in C if i in pool and i not in jit}
ARM |= {i for i in C if i not in pool and not E.jit_on(E.canon(E.require(dict(R[i]['genome']))))}

head = ('# The new roles\' screen (Iteration 705; results/drafts/new-roles-705.py) - %d designs, %s\n\n'
        'The series\' pool (seeds 92-96): the whole and its JIT-free designs, each by final-set.py\'s select() to %d and '
        'candidates() (every alive design within %d%% of the fastest at either width, the 5 smallest, the 5 leanest, the '
        'merged) and the knee; the JIT-free true front after merging (the ARM roles\' screen), the 5 smallest JIT designs, '
        'and the ten roles\' holders (today\'s measure). %s Read by loadtest.py --ids FILE and xcheck.py --also @FILE.\n\n')
with open(out, 'w') as o:
    o.write(head % (len(C), 'the laptop and dream', k, round(100 * band), 'Every candidate.'))
    for i, w in C.items(): o.write(json.dumps(dict(R[i], why='; '.join(w), src=src[i]), sort_keys=True) + '\n')
with open(armout, 'w') as o:
    o.write(head % (len(ARM), 'the Tegra', k, round(100 * band), 'The JIT-free ones, the whole pool\'s set (on ARMv7 a JIT '
                    'design is its JIT-off build) and the holders.'))
    for i, w in C.items():
        if i in ARM: o.write(json.dumps(dict(R[i], why='; '.join(w), src=src[i]), sort_keys=True) + '\n')

isjit = lambda i: i in jit or (i not in pool and E.jit_on(E.canon(E.require(dict(R[i]['genome'])))))
cnt = collections.Counter()
for ws in C.values():
    for w in set(x.split(' (')[0].split(' into ')[0].split(': a holder')[0] for x in ws):
        cnt[w if not w.startswith('a holder') else 'a holder'] += 1
print('\nThe list: %d designs (JIT %d, JIT-free %d); the ARM list %d (JIT %d)' % (
    len(C), sum(1 for i in C if isjit(i)), sum(1 for i in C if not isjit(i)), len(ARM), sum(1 for i in ARM if isjit(i))))
for w, n in sorted(cnt.items()): print('  %4d  %s' % (n, w))
P = [i for i in C if i in pool]
fr = [i for i in P if i not in jit]
best = lambda key, S: min(S, key=lambda i: (R[i][key], i))
for nm, S in (('all', P), ('JIT-free', fr), ('JIT', [i for i in P if i in jit])):
    print('In-run, %s: fastest %s %.4f, at 32 bits %s %.4f, smallest %s %s B, least memory %s %d KB' % (
        nm, best('speed', S), R[best('speed', S)]['speed'], best('speed32', S), R[best('speed32', S)]['speed32'],
        best('total', S), format(R[best('total', S)]['total'], ','), best('rss', S), R[best('rss', S)]['rss']))
