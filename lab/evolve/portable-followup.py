#!/usr/bin/env python3
"""lab/evolve/portable-followup.py DB PICK.json OUT [--k 30] [--hours H] [--before FILE] [--holders FILE] [--jit --seed N] - the portable
run's follow-up chain written
(Iteration 604; results/drafts/portable-plan-602.md, "Then"): one session a machine re-measuring, side by side, the
run's best and the best of the portable designs found before it.

DB: the portable run's db.jsonl (seed 87's pack). PICK.json: final-pick.py --json on results/portable-front-seed86.md
with the chain's readings (process-seed.sh's portablepick.json) - the set of the 282 re-measured on three machines, by
role. OUT: the list, one record a line (loadtest.py --ids and xcheck.py --also @OUT read it):
  - from the run: its designs on the union's true front (the run and the portable designs found before, in-run - as
    lab/evolve/portable.py names them), narrowed by final-set.py's select() to --k: the four extremes, then the designs
    adding the most hypervolume in the fixed box;
  - the pick's set: each design kept with its role.
--before FILE (Iteration 614, seed 88's follow-up): the portable designs found before the run, one record a line, as
portable.py --front wrote them (results/portable-front-seed87.md: the 348 before seed 88, seed 87's run among them) -
in place of the pool of the seeds before 87 and the final set (the default, seed 87's). --holders FILE: the relf
handoff's designs (results/relf-designs-611.md), each JIT-free one not listed yet added, so a role is re-measured beside
its holder (610 added 690981ca5b and c2ef9488ff by hand).
--also FILE (Iteration 617): records added as they are, each not listed yet, its own why - the screen's flagged
(followup-roles.py --screen --flagged). --rest OUT2 (Iteration 617; results/drafts/portable-plan-602.md, "After the follow-up"): the run's other designs on the
union's front - those select() left out - and the holders, one record a line: the screen the next portable run's remote
lines measure; its REMOTES lines printed, sized to --hours from seed 88's chain's rates (dream 11 s a design a session at
4-byte cells and 10 at 8-byte, 10 rounds; the Tegra 17 s a round and 5 s a design, at 3 rounds).
Prints the chain's lines - NEXT-RUN's `experiment loadtest.py --ids OUT --rounds 10` and REMOTES' two hosts - sized from
the measured rates (chain D: the laptop about 34 s a design for its four readings at 10 rounds; dream about 10 s a design
a session at 10 rounds; the Tegra about 18 s a round and 5 s a design, its stages 16 minutes), to fit --hours (default
the laptop's line). As the build user (it imports the evolver).
--jit (Iteration 622; results/drafts/jit-run-plan-620.md, "The follow-up"): the JIT run's - its JIT designs kept and, of
its designs, only what it bred (confirm.py's CARRIED: a carried design is the pool's); found before, without --before,
the pool before --seed N (confirm.py's: the series, the confirmations, the portable runs) and the final set; the holders
and --also kept with their JIT; each record its "jit" (followup-roles.py's portable roles skip JIT designs). PICK - for
none: the x86 and portable holders come by --holders."""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
a = sys.argv[1:]
if len(a) < 3: sys.exit(__doc__)
db, pick, out = a[:3]; k = int(a[a.index('--k') + 1]) if '--k' in a else 30
hours = float(a[a.index('--hours') + 1]) if '--hours' in a else None
opt = lambda n: a[a.index(n) + 1] if n in a else None
before, holders, rest, also = opt('--before'), opt('--holders'), opt('--rest'), opt('--also')
JIT, seedN = '--jit' in a, (int(opt('--seed')) if opt('--seed') else None)
if JIT and not before and seedN is None: sys.exit('portable-followup: --jit needs --seed N (the pool before it) or --before FILE')
recs = lambda f: [json.loads(l) for l in open(f) if l.strip().startswith('{')]
sys.argv = ['x']; import evolve as E
import hv, stopping
_s = importlib.util.spec_from_file_location('final_set', os.path.join(HERE, 'final-set.py')); FS = importlib.util.module_from_spec(_s); _s.loader.exec_module(FS)
_c = importlib.util.spec_from_file_location('confirm', os.path.join(HERE, 'confirm.py')); CF = importlib.util.module_from_spec(_c); _c.loader.exec_module(CF)
jit = lambda r: bool(E.express(E.canon(r['genome'])).get('jit'))
drop = (lambda r: False) if JIT else jit           # 622: --jit keeps the JIT designs
R = {i: r for i, r in hv.load(db, E).items() if r.get('genome') and not drop(r)
     and not (JIT and str(r.get('how', '')).startswith(CF.CARRIED))}   # 622: only what the JIT run bred
Q = {}
if before:
    for x in recs(before):
        if not drop(x): Q.setdefault(x['id'], dict(x, speed=x.get('inrun') or x['speed'], speed32=x.get('inrun32') or x['speed32']))
else:
    n0 = seedN if JIT else 87
    method, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < n0]
    for f in CF.pool_files(runs + CF.confirmations(stopping.LEDGER, n0) + (CF.portables(stopping.LEDGER, n0) if JIT else [])):
        Q.update({i: r for i, r in hv.load(f, E).items() if r.get('genome') and not drop(r)})
    for l in open(os.path.join(HERE, '..', '..', 'results', 'final-set-chainsBCD-seed86.md')):
        if l.startswith('{'):
            x = json.loads(l)
            if not drop(x): Q.setdefault(x['id'], dict(x, speed=x.get('inrun') or x['speed'], speed32=x.get('inrun32') or x['speed32']))
U = dict(Q); U.update(R)
on = {i: R[i] for i in hv.true_front(U, E) if i in R and i not in Q}
b = json.load(open(hv.BOUNDS))
chosen = [(i, 'the run - ' + w) for i, w, _ in FS.select(on, E, b, k)['set']] if on else []
P = [] if pick == '-' else [json.loads(l) for l in open(pick) if l.strip().startswith('{')]
keep = ('id', 'genome', 'speed', 'speed32', 'total', 'size', 'bin', 'rss', 'gen', 'status')
rows, seen = [], set()
for i, w in chosen:
    rows.append(dict({x: on[i][x] for x in keep if x in on[i]}, why=w)); seen.add(i)
for r in P:
    if r['id'] not in seen: rows.append(dict({x: r[x] for x in keep if x in r}, why='found before - ' + str(r.get('why', 'the pick')))); seen.add(r['id'])
for r in (recs(holders) if holders else []):
    if r['id'] not in seen and not drop(r): rows.append(dict({x: r[x] for x in keep if x in r}, why='found before - the relf handoff\'s role holder')); seen.add(r['id'])
for r in (recs(also) if also else []):
    if r['id'] not in seen and not drop(r): rows.append(dict({x: r[x] for x in keep if x in r}, why=r.get('why', 'found before - added'))); seen.add(r['id'])
if JIT: rows = [dict(r, jit=bool(jit(r))) for r in rows]
with open(out, 'w') as o:
    o.write(('# The JIT run\'s follow-up (lab/evolve/portable-followup.py --jit)' if JIT else '# The portable run\'s follow-up (lab/evolve/portable-followup.py)')
            + ': the run\'s best (%d of its %d designs on the union\'s\n'
            '# true front, by final-set.py\'s select()) and the best of the portable designs found before (%d: final-pick.py\'s set\n'
            '# in %s%s), re-measured side by side - one session a machine. In-run numbers for the run\'s, re-measured for the rest.\n\n'
            % (len(chosen), len(on), len(rows) - len(chosen), os.path.basename(pick), ', the relf handoff\'s role holders' if holders else ''))
    for r in rows: o.write(json.dumps(r, sort_keys=True) + '\n')
n = len(rows); lap_h = n * 34 / 3600.0; dream_m = n * 10 / 60.0; rage_m = 16 + n * (10 * 18 + 5) / 60.0
H = hours or max(lap_h, rage_m / 60.0)
print('%d designs -> %s: the run %d (of %d on the union\'s front), found before %d' % (n, out, len(chosen), len(on), n - len(chosen)))
print('the laptop: about %.1f hours at 10 rounds (four readings); dream about %.0f minutes a session a width; the Tegra about %.0f minutes a session at 10 rounds' % (lap_h, dream_m, rage_m))
s_d = min(40, max(1, int(H * 60 / 2 // dream_m))); s_r = min(5, max(1, int((H * 60 - 16) // (rage_m - 16))))   # chain D: dream's cap 40
print('NEXT-RUN:  experiment loadtest.py --ids %s --rounds 10' % out)
print('REMOTES:   rage.lan     prebuiltarm 4       10      %d      --cell 4 --rejected 4 --sessions %d --also @%s' % (int(H * 60) - 5, s_r, out))
print('           dream.lan    prebuilt32  4       10      %d      --cell 4 --rejected 6 --sessions %d --also @%s' % (int(H * 30) - 5, s_d, out))
print('           dream.lan    prebuilt64  4       10      %d      --from prebuilt32 --sessions %d' % (int(H * 30) - 5, s_d))
if rest:                                              # 617: the screen - the union's front less the chosen, with the holders
    rr = [dict({x: on[i][x] for x in keep if x in on[i]}, why='the run - the screen (the rest of the union\'s front)')
          for i in sorted(on, key=lambda i: (on[i]['speed'], i)) if i not in seen]
    hold = [dict({x: r[x] for x in keep if x in r}, why='found before - the relf handoff\'s role holder')
            for r in (recs(holders) if holders else []) if not drop(r)]
    with open(rest, 'w') as o:
        o.write('# The screen (lab/evolve/portable-followup.py --rest, Iteration 617): the run\'s %d other designs on the union\'s true\n'
                '# front - those its follow-up does not re-measure - and the relf handoff\'s %d portable role holders to pair them with,\n'
                '# measured on the remote lines during the next portable run (results/drafts/portable-plan-602.md, "After the follow-up").\n\n'
                % (len(rr), len(hold)))
        for r in rr + hold: o.write(json.dumps(r, sort_keys=True) + '\n')
    m = len(rr) + len(hold); H2 = hours or 21.0
    d32, d64, tg = m * 11 / 60.0, m * 10 / 60.0, m * (3 * 17 + 5) / 60.0
    print('the screen: %d designs -> %s (the run %d, the holders %d); a session: dream %.0f and %.0f minutes (4- and 8-byte), the '
          'Tegra %.0f at 3 rounds' % (m, rest, len(rr), len(hold), d32, d64, tg))
    sd = max(1, min(int((H2 * 30 - 5) // d32), int((H2 * 30 - 5) // d64))); st = max(1, int((H2 * 60 - 5 - 16) // tg))
    print('REMOTES:   rage.lan     prebuiltarm 4       3       %d     --cell 4 --rejected 4 --sessions %d --also @%s' % (int(H2 * 60) - 5, st, rest))
    print('           dream.lan    prebuilt32  4       10      %d      --cell 4 --rejected 6 --sessions %d --also @%s' % (int(H2 * 30) - 5, sd, rest))
    print('           dream.lan    prebuilt64  4       10      %d      --from prebuilt32 --sessions %d' % (int(H2 * 30) - 5, sd))
