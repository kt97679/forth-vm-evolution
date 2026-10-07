#!/usr/bin/env python3
"""hotsites.py ID [--db FILE ...] [--write FILE] - the image's hottest call
sites, for the gene hotinl (Iteration 92; lab/evolve/GENES.md, "Ranked
(Iteration 91)", 1): inlining at the hottest sites, whatever the callee.

Builds the design with the call map and the profiler (as callsites.py does),
runs the selection workloads, and ranks every call site in the image's code
by the mean share of each workload's dispatches its calls and returns take.
A site is named by its caller, its callee and which call to that callee it
is in the caller - names, so the list carries over to other designs built
from the same sources. --write keeps the list (lab/evolve/hotsites-v1.json):
the converter (layout.py --hot-inline FILE K) inlines the first K that are
safe in the design at hand.
"""
import collections, glob, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]; dbs, out = [], None
while '--db' in args: i = args.index('--db'); dbs.append(args[i + 1]); del args[i:i + 2]
if '--write' in args: i = args.index('--write'); out = args[i + 1]; del args[i:i + 2]
if len(args) != 1: sys.exit(__doc__)
recs = {}
for db in dbs or sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md'))):
    for l in open(db, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if isinstance(r, dict) and 'genome' in r and 'id' in r: recs[r['id']] = r
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
g = E.canon(recs[args[0]]['genome']); d = os.path.join(E.EV, 'hotsites'); shutil.rmtree(d, ignore_errors=True)
g2 = dict(g, tail=0, msc=0, hotinl=0)
if not E.jit_on(g): g2['jit'] = 0
cm = d + '.map'; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
try: eng, img = E.build(g2, d)
finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
M = [l.rstrip('\n').split(' ') for l in open(cm)]
n = int(M[0][2])
C = sorted((int(f[1]), int(f[2]), int(f[3]), f[6], ' '.join(f[7:])) for f in M if f[0] == 'C')
O = {int(f[1]): ' '.join(f[4:]) for f in M if f[0] == 'O'}
W = {int(f[1]): int(f[2]) for f in M if f[0] == 'W'}
seen, site = collections.Counter(), {}
for a, ln, t, caller, callee in C:
    if caller == '(prologue)': continue
    seen[(caller, callee)] += 1; site[a + ln] = (caller, callee, seen[(caller, callee)], t)
pw = E.private_work(d); share = collections.Counter()
for w in E.WORK_SEL:
    pf = os.path.join(d, 'p-' + w); E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=20, env=dict(os.environ, VMPROF=pf))
    runs, tot = {}, 0
    for f in (l.split() for l in open(pf)):
        if f[0] == 'I': tot += int(f[2])
        elif f[0] == 'R' and int(f[1]) in site: runs[int(f[1])] = int(f[3])
    for r, k in runs.items(): share[site[r][:3]] += 2.0 * k / tot / len(E.WORK_SEL)
body = {s[:3]: ' '.join(O.get(x, 'call') for x in sorted(O) if s[3] <= x < W.get(s[3], s[3])) for s in site.values()}
top = [k for k, v in share.most_common() if v > 0]
for i, k in enumerate(top[:30]): print('%2d %5.2f%%  %s -> %s (#%d): %s' % (i + 1, 100 * share[k], k[0], k[1], k[2], body.get(k, '?')[:70]))
if out:
    json.dump([[c, t, o, round(share[(c, t, o)], 6)] for c, t, o in top[:100]], open(out, 'w'), indent=0)
    print('wrote %s: %d sites' % (out, min(100, len(top))))
shutil.rmtree(d, ignore_errors=True)
