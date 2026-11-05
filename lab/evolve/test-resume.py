#!/usr/bin/env python3
"""lab/evolve/test-resume.py - a resumed run replays what the first attempt did, then goes on (Iteration 610).

Seed 87's laptop crashed at generation 136; the restart forked at generation 3 and ran 262 generations from there - the
replay saw each gated design's second reading (written a generation after its first, Iteration 446) from the start and
ranked on it early (results/drafts/resume-610.md). Here a run of 12 designs for 9 generations with a stand-in for the
measurement (a speed from the id and a noise term - nothing built or run), its database cut at generation 6 as a crash
would leave it, and the run started again on it: generations 1-6 (each generation's line, the operators, the attic) as
the first attempt's - and, the control, not so with the replay off (EVOLVE_REPLAY=0), or the test proves nothing.
tools/run-tests.sh runs it, a few seconds; exit 1 on a failure.
"""
import contextlib, io, json, os, shutil, subprocess, sys, tempfile
AMP, FG, CUT, GENS = float(os.environ.get('RT_AMP', 0.6)), os.environ.get('RT_FG', '2'), int(os.environ.get('RT_CUT', 6)), int(os.environ.get('RT_GENS_ALL', 9))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if len(sys.argv) > 1 and sys.argv[1] == 'child':
    sys.argv = ['x']; sys.path.insert(0, ROOT + '/lab/evolve'); import evolve as E
    db, gens = os.environ['RT_DB'], os.environ['RT_GENS']
    E.design_pairs = lambda g, n=24: list(E.SUPER_POOL)[:n]
    E.report = lambda R: None; E.setup_widths = lambda *a, **k: None; E.setup = lambda *a, **k: None
    cnt = [0]
    def fake_job(a):
        g, gate, again = a[0], a[3], a[4]
        i = E.gid(E.canon(g)); h = int(i, 16); cnt[0] += 1
        s = (0.3 + (h % 997) / 997.0) * (1 + AMP * (((cnt[0] * 7919) % 101) / 100.0 - 0.5))
        rec = {'status': 'ok', 'speed': s, 't': {w: s for w in E.WORK_SEL}, 'raw': {w: 1000.0 for w in E.WORK_SEL}, 'size': 8000 + h % 3001,
               'bin': 4000, 'total': 12000 + h % 3001, 'rss': 100 + h % 41, 'mem': {}, 'unit': 1.0, 'etext': None, 'secs': 0}
        if gate and s < gate and not again: rec['gated'] = 1
        return rec
    E._job = fake_job
    E.main(['--db', db, '--pop', '12', '--gens', gens, '--seed', '5', '--fastgate', FG])
    sys.exit(0)
def run(db, gens, env=None):
    e = dict(os.environ, RT_DB=db, RT_GENS=str(gens), **(env or {}))
    p = subprocess.run([sys.executable, __file__, 'child'], env=e, capture_output=True, text=True)
    if p.returncode: print(p.stderr[-2000:]); sys.exit(1)
    return [l for l in p.stdout.split('\n') if l.startswith(('  generation ', '  the attic', '  operators'))], p.stdout
d = tempfile.mkdtemp(prefix='test-resume-')
la, outa = run(d + '/a.jsonl', GENS)
L = open(d + '/a.jsonl').readlines(); recs = [json.loads(l) for l in L]
cut = next(k for k, r in enumerate(recs) if (r.get('gen') or 0) >= CUT and 'speed1' not in r)
while 'speed1' in recs[cut - 1]: cut -= 1
gated_early = sum(1 for r in recs[:cut] if 'speed1' in r)
for f in ('b.jsonl', 'c.jsonl'): open(d + '/' + f, 'w').writelines(L[:cut])
lb, outb = run(d + '/b.jsonl', GENS)
lc, outc = run(d + '/c.jsonl', GENS, {'EVOLVE_REPLAY': '0'})
# up to generation 5's breeding: its attic follows the children measured after the cut - another moment's readings
upto = lambda ls: ls[:next((k for k, l in enumerate(ls) if l.startswith('  the attic') and any(x.startswith('  generation %d:' % CUT) for x in ls[:k])), len(ls))]
ok, ctl = upto(la) == upto(lb), upto(la) != upto(lc)
shutil.rmtree(d, ignore_errors=True)
first = next(('%s | %s' % (x.strip(), y.strip()) for x, y in zip(upto(la), upto(lc)) if x != y), 'none')
if not gated_early: print('test-resume: FAIL - no second reading before the cut: the test proves nothing'); sys.exit(1)
if not ok: print('test-resume: FAIL - the resumed run forked inside its replay'); sys.exit(1)
if not ctl: print('test-resume: FAIL - the control: with the replay off it did not fork either'); sys.exit(1)
print('test-resume: ok - cut at generation %d after %d second readings: the replay as the first attempt; off, it forks (%s)' % (CUT, gated_early, first))
