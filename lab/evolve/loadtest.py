#!/usr/bin/env python3
"""loadtest.py DB [DB ...] [--fastest K] [--slowest K] [--rounds R] [--load N] - the measuring load (Iteration 455)

The owner: test the load. The fast end's optimism - the front's fastest re-measured after the run about 10% slower
than in it, seeds 58-66 - did not fall when the fast gate's second reading moved to the next generation
(results/drafts/fastgate-review-445.md, Iteration 454). In the run JOBS workers measure at once, each on its own core;
the re-measure after it, one design at a time. Is it the load? The newest database's front - its K fastest and K
slowest - each measured against s6 (evolve.py's measure(), on the core setup() pins) idle, and with N other cores each
running s6 on the kernel workload over and over: idle, loaded, idle, loaded. Per design the ratio idle and loaded, and
loaded / idle; then each group's median. The load explains the optimism if the fast group runs faster against s6
under it - loaded / idle near 0.90 - and the slow group does not.

--ids FILE (Iteration 573 - GOALS.md step 3, the final set re-measured alone and under load; the owner's decision: the
extremes chosen only after it): instead of the front's fastest and slowest, every design in FILE (final-set.py
--candidates: one record a line), each also at 32 bits (evolve.py's eval32), idle and loaded; after the table one JSON
line a design - {"id", "inrun", "inrun32", "idle", "loaded", "idle32", "loaded32"} - for the processing to read.
"""
import argparse, json, math, os, statistics, subprocess, sys, tempfile, time
ap = argparse.ArgumentParser(usage=__doc__.split('\n')[0])
ap.add_argument('dbs', nargs='*')
ap.add_argument('--ids')
ap.add_argument('--fastest', type=int, default=8)
ap.add_argument('--slowest', type=int, default=4)
ap.add_argument('--rounds', type=int, default=3)
ap.add_argument('--load', type=int, default=3)
a = ap.parse_args()
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
if a.ids: E.TWO_WIDTHS[0] = True; E.setup_widths()         # 573: the 4-byte cells' references too, for eval32
else: E.setup()
if not a.ids and not a.dbs: ap.error('a database, or --ids FILE')
if a.ids and not os.path.exists(a.ids):                      # 573: a chain's experiment names it from the repository
    a.ids = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), a.ids)
db = a.ids or max(a.dbs, key=os.path.getmtime)
R = {}
for l in open(db):
    try: r = json.loads(l); R[r['id']] = r
    except (ValueError, KeyError, TypeError): pass
rmf = os.path.join(os.path.dirname(db), os.path.basename(db).replace('db', 'remeasure', 1).replace('.jsonl', '.json'))
if a.ids:                                                      # 573: the final set's candidates, every one
    R = {i: r for i, r in R.items() if r.get('genome')}; sp = {i: R[i].get('speed') or 0.0 for i in R}; how = 'the candidates'
elif os.path.basename(db).startswith('db') and os.path.exists(rmf):
    rm = json.load(open(rmf)); sp = {i: (rm[i]['speed'] if isinstance(rm[i], dict) else rm[i]) for i in rm if i in R}; how = 're-measured front'
else:
    ids = E.fronts([i for i, r in R.items() if r.get('status') == 'ok'], R)[0]; sp = {i: R[i]['speed'] for i in ids}; how = 'selection front'
order = sorted(sp, key=sp.get)
groups = [('fast', i) for i in order[:a.fastest]] + ([('slow', i) for i in order[-a.slowest:]] if a.slowest else [])
if a.ids: groups = [('asked', i) for i in R]
core = int(E.PIN[-1]) if E.PIN else 0
def siblings(c):
    try:
        out = set()
        for part in open('/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list' % c).read().strip().split(','):
            lo, _, hi = part.partition('-'); out |= set(range(int(lo), int(hi or lo) + 1))
        return out
    except OSError: return {c}
avoid = siblings(core) | {core}
others = [c for c in range(os.cpu_count() or 1) if c not in avoid and not (siblings(c) & avoid)]
others = [c for k, c in enumerate(others) if not any(c in siblings(o) for o in others[:k])][:a.load]   # one a physical core
if os.environ.get('LOADTEST_CORES'): others = [int(c) for c in os.environ['LOADTEST_CORES'].split(',')]   # a test's override
reng, rimg, rpw = E.REF[0], E.REF[1], E.REF[2]
prog = tempfile.NamedTemporaryFile('wb', suffix='.fth', delete=False); prog.write(E.program('kernel')); prog.close()
def start_load():
    return [subprocess.Popen(['sh', '-c', 'while :; do taskset -c %d %s %s < %s > /dev/null 2>&1; done' % (c, reng, rimg, prog.name)],
                             cwd=rpw, start_new_session=True) for c in others]
def stop_load(ps):
    for p in ps:
        try: os.killpg(p.pid, 9)
        except OSError: pass
def speed(eng, img, pw):
    t, _ = E.measure(eng, img, pw, E.WORK_SEL, a.rounds)
    return math.exp(sum(math.log(t[w]) for w in E.WORK_SEL) / len(E.WORK_SEL))
print('# The measuring load (lab/evolve/loadtest.py, Iteration 455)\n')
print('Front: %s, %s (%d designs); the %d fastest and %d slowest. Measured on core %d (setup()\'s), the load on %s: s6 on the'
      ' kernel workload over and over. %d rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.\n'
      % (db, how, len(order), a.fastest, a.slowest, core, ', '.join(map(str, others)) or 'none - no other physical core', a.rounds))
if not others: print('**No other core to load: nothing to test here.**'); sys.exit(0)
print('| design | group | in-run | re-measured | idle | loaded | loaded / idle |%s\n|---|---|---|---|---|---|---|%s' % (
    ' in-run 32 | idle 32 | loaded 32 |' if a.ids else '', '---|---|---|' if a.ids else ''), flush=True)
res = {'fast': [], 'slow': [], 'asked': []}; js = []
for grp, i in groups:
    d = os.path.join(E.EV, 'loadtest'); import shutil; shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(E.canon(R[i]['genome']), d); pw = E.private_work(d)
        idle, loaded = [], []
        for _ in range(2):
            idle.append(speed(eng, img, pw))
            ps = start_load(); time.sleep(1)
            try: loaded.append(speed(eng, img, pw))
            finally: stop_load(ps)
        gi = math.sqrt(idle[0] * idle[1]); gl = math.sqrt(loaded[0] * loaded[1]); res[grp].append(gl / gi)
        x32 = ''
        if a.ids:                                                  # 573: and at 32 bits, idle then loaded
            i32 = E.eval32(E.canon(R[i]['genome']), a.rounds).get('speed32')
            ps = start_load(); time.sleep(1)
            try: l32 = E.eval32(E.canon(R[i]['genome']), a.rounds).get('speed32')
            finally: stop_load(ps)
            f3 = lambda v: '%.3f' % v if v else '-'
            x32 = ' %s | %s | %s |' % (f3(R[i].get('speed32')), f3(i32), f3(l32))
            js.append(dict(id=i, inrun=R[i].get('speed'), inrun32=R[i].get('speed32'), idle=gi, loaded=gl, idle32=i32, loaded32=l32))
        print('| %s | %s | %.3f | %.3f | %.3f | %.3f | %.3f |%s' % (i, grp, R[i].get('speed', 0), sp[i], gi, gl, gl / gi, x32), flush=True)
    except Exception as x: print('| %s | %s | - | - | - | - | failed: %s |' % (i, grp, str(x)[:60]), flush=True)
os.unlink(prog.name)
print()
for x in js: print(json.dumps(x, sort_keys=True))
for g in ('fast', 'slow', 'asked'):
    if res[g]: print('- the %s group: loaded / idle, median %.3f over %d (range %.3f-%.3f)' % (g, statistics.median(res[g]), len(res[g]), min(res[g]), max(res[g])))
print('\nThe load explains the fast end\'s optimism if the fast group\'s median is near 0.90 and the slow group\'s near 1.00.')
