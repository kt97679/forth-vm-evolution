#!/usr/bin/env python3
"""supers-knockout.py RESULTS.md [--every K] [--all-encodings] - do superinstruction pairs buy anything?
(Iteration 385; HANDOFF item 1, results/drafts/supers-tag2.md: "if a knockout shows superinstructions buy
nothing, the supers gene comes out of tag-2 designs").

Every tag-2 design of the front in RESULTS.md that builds pairs (express() keeps only the pairs that got a
slot), sorted by binary + image, every K-th of them and both extremes (default K 4) - and one design that
builds none, as a control (its knockout must change nothing). Each built twice: as it is, and with the
supers gene emptied. For each: binary + image (the size objective; as it is, checked against the record),
and the dispatches over the selection workloads from the profiler (-DPROFILE, VMPROF) - deterministic, so
noise-free on any machine; the time they stand for is the laptop's to measure. The design is built as it
is in every other respect: with the JIT on, what is counted is what the JIT leaves to the interpreter.
"""
import collections, glob, json, math, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
argv = sys.argv[1:]
if not argv or argv[0].startswith('--'): sys.exit(__doc__)
every = int(argv[argv.index('--every') + 1]) if '--every' in argv else 4
any_enc = '--all-encodings' in argv
recs = []
for l in open(argv[0], errors='replace'):
    try: r = json.loads(l)
    except ValueError: continue
    if isinstance(r, dict) and 'genome' in r and 'id' in r: recs.append(r)
if not recs: sys.exit('supers-knockout: no design records in %s' % argv[0])
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()

def size(g, d):
    E.PROFILING[0] = False
    eng, img = E.build(g, d)
    n = os.path.getsize(eng) + os.path.getsize(img); shutil.rmtree(d, ignore_errors=True); return n

def dispatches(g, d):
    """-> {workload: dispatches} over the selection workloads, the profiler's count"""
    E.PROFILING[0] = True
    try: eng, img = E.build(g, d)
    finally: E.PROFILING[0] = False
    pw = E.private_work(d); out = {}
    for wl in E.WORK_SEL:
        pf = os.path.join(d, 'p-' + wl)
        E.sh([eng, img], cwd=pw, inp=E.program(wl), timeout=240, cpu=60, env=dict(os.environ, VMPROF=pf))
        out[wl] = sum(int(f[2]) for f in (l.split() for l in open(pf)) if f and f[0] == 'I')
    shutil.rmtree(d, ignore_errors=True); return out

cands, control = [], None
for r in recs:
    g = E.canon(r['genome']); e = E.express(g)
    if not (any_enc or e.get('tag2')): continue
    if e.get('supers'): cands.append((r.get('bin', 0) + r.get('size', 0), r, g, e))
    elif control is None: control = (r.get('bin', 0) + r.get('size', 0), r, g, e)
cands.sort(key=lambda c: c[0])
pick = sorted({0, len(cands) - 1} | set(range(0, len(cands), every)))
todo = [cands[i] for i in pick] + ([control] if control else [])
print('# Superinstruction pairs knocked out - %s\n' % os.path.basename(argv[0]))
print('%d %sdesigns of the front build pairs; %d measured (every %d-th by size, the extremes)%s. '
      'Dispatches summed over %s; a ratio below 1 is pairs saving dispatches.\n'
      % (len(cands), '' if any_enc else 'tag-2 ', len(todo) - (1 if control else 0), every,
         ', and %s, building none, as the control' % control[1]['id'] if control else '', ', '.join(E.WORK_SEL)))
print('| design | pairs built | binary + image | without pairs | bytes the pairs cost | dispatches | without pairs | ratio, geometric mean over workloads | largest saving |')
print('|---|---|---|---|---|---|---|---|---|')
ratios, costs, bad = [], [], []
for tot, r, g, e in todo:
    g0 = E.canon(dict(g, supers=[]))
    d = os.path.join(E.EV, 'supko')
    s1, s0 = size(g, d), size(g0, d)
    if tot and s1 != tot: bad.append('%s: built %d, recorded %d' % (r['id'], s1, tot))
    c1, c0 = dispatches(g, d), dispatches(g0, d)
    rw = {w: c1[w] / max(1, c0[w]) for w in E.WORK_SEL}
    gm = math.exp(sum(math.log(v) for v in rw.values()) / len(rw))
    best = min(rw, key=rw.get)
    is_control = control and r is control[1]
    if not is_control: ratios.append(gm); costs.append(s1 - s0)
    print('| %s%s | %s | %s | %s | %+d | %s | %s | %.4f | %s %.4f |' % (
        r['id'], ' (control)' if is_control else '', '; '.join(' '.join(p) for p in e.get('supers', [])) or 'none',
        format(s1, ','), format(s0, ','), s1 - s0, format(sum(c1.values()), ','), format(sum(c0.values()), ','),
        gm, best, rw[best]))
    sys.stdout.flush()
if ratios:
    rs = sorted(ratios); cs = sorted(costs)
    print('\nOver the %d designs that build pairs: dispatch ratio median %.4f, range %.4f-%.4f; bytes the pairs cost '
          'median %+d, range %+d to %+d.' % (len(rs), rs[len(rs) // 2], rs[0], rs[-1], cs[len(cs) // 2], cs[0], cs[-1]))
if bad: print('\n**Size check failed** - the method is not the record\'s: ' + '; '.join(bad))
else: print('\nSize check: every design as it is built to the bytes its record holds.')
