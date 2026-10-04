#!/usr/bin/env python3
"""image-ab.py ID [ID ...] --env VAR=VALUE [--set GENE=VALUE] [--db FILE] [--rounds N] - a
change to the image alone, measured on one engine.

Iteration 8's lesson: two builds of a design differ in the engine's layout
by several per cent, so a change to the IMAGE is measured as two images on
ONE engine. For each design: its engine built once (as the evolver builds
it); its image converted twice - with VAR=VALUE in the converter's
environment (A), and as the converter stands (B); both through the gate,
the corpus and the kernel workload; their sizes; their dispatches counted
on a profiling engine of the same design (layout-free); and their CPU
time on the design's own engine, A and B run back to back, alternating
which goes first, best of the rounds. Ratios are B / A.

Iteration 13: SOD16_OLD_BODYCHECK=1 - the format-10 and tiny words' body
check as it was, reading bodies after the pairs, short branches and fused
tests had rewritten them - against the fix. Iteration 14: --set hotcalls=32
--env SOD16_NO_HOTCALLS=1 - one-byte calls, image against image; and with
no --set, both images are the same: the noise of the machine itself.
"""
import json, math, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; db = os.path.join(HERE, '..', '..', 'build', 'evolve', 'db.jsonl'); rounds = 10; env = None
sets = {}
for opt in ('--db', '--rounds', '--env', '--set'):
    while opt in args:
        i = args.index(opt); v = args[i + 1]; del args[i:i + 2]
        if opt == '--set': k, x = v.split('=', 1); sets[k] = int(x) if x.lstrip('-').isdigit() else x; continue
        if opt == '--db': db = v
        elif opt == '--rounds': rounds = int(v)
        else: env = v.split('=', 1)
if not args or env is None or any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
recs = {}
for l in open(db):
    try: r = json.loads(l); recs[r['id']] = r
    except ValueError: pass
WORKS = E.WORK_SEL + E.WORK_HELD

def both(g, d, profile=False):
    """(engine, image A, image B): one engine, the image converted both ways."""
    E.PROFILING[0] = profile
    try:
        os.environ[env[0]] = env[1]
        try: eng, a = E.build(g, d)
        finally: del os.environ[env[0]]
        shutil.copy(a, a + '.A'); a += '.A'
        eng2, b = E.build(g, d + '-b')
    finally: E.PROFILING[0] = False
    return eng, a, b

def count(eng, img, pw, w, d):
    pf = os.path.join(d, 'prof'); 
    if os.path.exists(pf): os.remove(pf)          # the profiler appends
    E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
    return sum(int(l.split()[2]) for l in open(pf) if l.startswith('I '))

print('| design | size A | size B | B - A | dispatches B / A: %s | time B / A: %s | selection |'
      % (', '.join(WORKS), ', '.join(WORKS)))
print('|---|---|---|---|---|---|---|')
for did in args:
    if did not in recs: sys.exit('no design %s in %s' % (did, db))
    g = E.canon(dict(recs[did]['genome'], **sets))    # --set GENE=VALUE: the design with that gene changed
    d = os.path.join(E.EV, 'ab')
    eng, a, b = both(g, d)
    pw = E.private_work(d)
    for img in (a, b):
        E.alive(eng, img, pw)                       # raises 'died: ...' if either fails the gate
    sa, sb = os.path.getsize(a), os.path.getsize(b)
    peng, pa, pb = both(dict(g, tail=0, msc=0), d + '-p', profile=True)
    ppw = E.private_work(d + '-p')
    cr = [count(peng, pb, ppw, w, d) / count(peng, pa, ppw, w, d) for w in WORKS]
    best = {}
    for r_ in range(rounds):
        for w in WORKS:
            pair = [(a, 'A'), (b, 'B')]
            for img, k in (pair if r_ % 2 == 0 else pair[::-1]):
                best[(k, w)] = min(best.get((k, w), 1 << 62), E.run_metric(eng, img, pw, w))
    tr = [best[('B', w)] / best[('A', w)] for w in WORKS]
    sel = math.exp(sum(math.log(x) for x, w in zip(tr, WORKS) if w in E.WORK_SEL) / len(E.WORK_SEL))
    print('| %s | %d | %d | %+d | %s | %s | %.3f |' % (did, sa, sb, sb - sa, ', '.join('%.3f' % x for x in cr),
          ', '.join('%.3f' % x for x in tr), sel), flush=True)
    for x in (d, d + '-b', d + '-p', d + '-p-b'): shutil.rmtree(x, ignore_errors=True)
