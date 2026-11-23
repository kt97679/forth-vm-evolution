#!/usr/bin/env python3
"""results/drafts/roles-screen-741.py LIST ARMLIST DB RESULTS ... (--designs DIR --records FILE | --holders FILE)
[--also FILE ...] [--k K] [--band B] [--iter N] [--series LABEL] [--db-label L] [--holders-src L] - the roles' screen, the
first follow-up chain's two lists, for any series (Iteration 741; results/drafts/new-roles-705.py made general - the
endgame's step 3, results/drafts/endgame-740.md). Reads only.

The pool: the series' records - RESULTS (each run's results file: its front, in-run) and DB (the last run's database:
every alive design, the earlier fronts carried in and measured again); a design in several, the newest alive record.
By final-set.py's select() to K (30) and candidates() (every alive design within B (0.05) of the fastest at either
width, the 5 smallest, the 5 leanest, every design merged into the set's) and the knee, twice: the whole pool (the x86
roles) and its JIT-free designs (the portable roles); then the JIT-free true front after merging (the ARM roles'
screen), the 5 smallest JIT designs, and the holders:
  --designs DIR --records FILE: today's roles - each DIR/NAME/record.json's id, its record from FILE
      (results/relf-designs-NNN.md: master's sizes, the laptop's memory), the role its NAME;
  --holders FILE: 705's form - records whose why reads "a holder: ROLE (SOURCE) ..." (results/roles-holders-705.md).
A holder in the pool keeps the pool's record. --also FILE (any number): records added to the list as they are - their
genome is what the chain measures (results/candidates-guard-740.md: the guard challengers); JIT-free ones go on the ARM
list too. LIST: every candidate (the laptop and dream, both widths); ARMLIST: the JIT-free ones, the whole pool's set (a
JIT design on ARMv7 is its JIT-off build) and the holders (the Tegra). One record a line with "why" and "src" (loadtest.py
--ids FILE, measure-ids.py --ids FILE and xcheck.py --also @FILE read them; the remote lines find genomes by id in
results/evolve-*-seed*.md, results/candidates-*.md and results/relf-designs-*.md - keep an --also file under one of
those names). stdout: the counts and each role's in-run best.
Test (741): with 705's arguments (--holders, --db-label seed96-db.jsonl, --holders-src holders-705.py) it writes 705's
script's record lines on the same inputs, byte for byte - results/drafts/roles-screen-741.sh."""
import collections, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, '..', '..', 'lab', 'evolve')
A = sys.argv[1:]
def opt(name, default=None, many=False):
    vals = []
    while name in A:
        j = A.index(name); vals.append(A[j + 1]); del A[j:j + 2]
    return vals if many else (vals[-1] if vals else default)
k, band = int(opt('--k', '30')), float(opt('--band', '0.05'))
ITER, SERIES = opt('--iter', '?'), opt('--series')
DESIGNS, RECORDS, HOLDERS = opt('--designs'), opt('--records'), opt('--holders')
ALSO = opt('--also', many=True)
DBL, HSRC = opt('--db-label'), opt('--holders-src')
if len(A) < 4 or not (HOLDERS or (DESIGNS and RECORDS)): sys.exit(__doc__)
out, armout, db, files = A[0], A[1], A[2], A[3:]
DBL = DBL or os.path.basename(db)
HSRC = HSRC or os.path.basename(HOLDERS or RECORDS)
sys.argv = ['x']; sys.path.insert(0, LAB)
import evolve as E
import hv, appsize
spec = importlib.util.spec_from_file_location('final_set', os.path.join(LAB, 'final-set.py'))
FS = importlib.util.module_from_spec(spec); spec.loader.exec_module(FS)
b = json.load(open(hv.BOUNDS))

alive = lambda r: r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss') and r.get('speed32')
R, src = {}, {}
for f in files + [db]:
    for i, r in hv.load(f, E).items():
        if alive(r) or i not in R:
            R[i] = r; src[i] = os.path.basename(f) if f != db else DBL
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
if HOLDERS:                                              # 705's form: the role and its source in the record's why
    H = []
    for l in open(HOLDERS):
        if not l.startswith('{'): continue
        h = json.loads(l); w = h['why'].split(': ', 1)[1]
        H.append((w.split(' (')[0], w.split(' (', 1)[1].split(')')[0], h))
    MEAS = 'measured here - ' + HSRC
else:                                                    # today's roles: designs/NAME/record.json, the record from RECORDS
    RR = {json.loads(l)['id']: json.loads(l) for l in open(RECORDS) if l.startswith('{')}
    H = []
    for n in sorted(x for x in os.listdir(DESIGNS) if os.path.exists(os.path.join(DESIGNS, x, 'record.json'))):
        i = json.load(open(os.path.join(DESIGNS, n, 'record.json')))['id']
        assert i in RR, 'the holder %s (%s) not in %s' % (i, n, RECORDS)
        H.append((n, RECORDS, RR[i]))
    MEAS = 'its record - the chain measures it'
for role, hs, h in H:
    if h['id'] in pool: add(h['id'], 'a holder: %s (%s; the pool\'s record)' % (role, hs))
    else:
        R[h['id']] = h; src[h['id']] = HSRC
        add(h['id'], 'a holder: %s (%s; %s)' % (role, hs, MEAS))
    ARM.add(h['id'])
for f in ALSO:                                           # 741: designs asked for as they are (the guard challengers)
    for l in open(f):
        if not l.startswith('{'): continue
        r = json.loads(l)
        if r['id'] not in R: R[r['id']] = r; src[r['id']] = os.path.basename(f)
        add(r['id'], 'also (%s): %s' % (os.path.basename(f), r.get('why', '')))
ARM |= {i for i in C if i in pool and i not in jit}
ARM |= {i for i in C if i not in pool and not E.jit_on(E.canon(E.require(dict(R[i]['genome']))))}

head = ('# The roles\' screen (Iteration %s; results/drafts/roles-screen-741.py) - %d designs, %s\n\n'
        'The series\' pool (%s): the whole and its JIT-free designs, each by final-set.py\'s select() to %d and '
        'candidates() (every alive design within %d%% of the fastest at either width, the 5 smallest, the 5 leanest, the '
        'merged) and the knee; the JIT-free true front after merging (the ARM roles\' screen), the 5 smallest JIT designs, '
        'the roles\' holders%s. %s Read by loadtest.py --ids FILE and xcheck.py --also @FILE.\n\n')
ser = SERIES or ', '.join([os.path.basename(f) for f in files] + [DBL])
alsot = (' and ' + ', '.join(os.path.basename(f) for f in ALSO)) if ALSO else ''
with open(out, 'w') as o:
    o.write(head % (ITER, len(C), 'the laptop and dream', ser, k, round(100 * band), alsot, 'Every candidate.'))
    for i, w in C.items(): o.write(json.dumps(dict(R[i], why='; '.join(w), src=src[i]), sort_keys=True) + '\n')
with open(armout, 'w') as o:
    o.write(head % (ITER, len(ARM), 'the Tegra', ser, k, round(100 * band), alsot, 'The JIT-free ones, the whole pool\'s set '
                    '(on ARMv7 a JIT design is its JIT-off build) and the holders.'))
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
