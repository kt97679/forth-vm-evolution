#!/usr/bin/env python3
"""factor-price.py ID [--shares 1e-3,1e-2,2] [--db FILE ...] - what the gene
factor saves and costs on one recorded design (Iteration 270: the tool behind
Iteration 267's numbers, which were measured with a script in /tmp).

Builds the design with the gene off and once for each share (the converter's
--factor-share: a word below that share of the reference dispatches, from
lab/evolve/hotwords-v1.json, is factored; 2 means every word), with the
profiler on, runs the selection workloads, and prints the image bytes and each
workload's dispatches against the gene off. Dispatch counts are exact, so the
price is measured here, not on the laptop's clock.

Iteration 267 on 3456ac1e5e: 1e-4 -17 bytes +0.001%; 1e-3 -41 +0.007%; 3e-3 -65
+0.028%; 1e-2 -95 +0.167%; every word -127 +1.979% (the geometric mean of the
six workloads' dispatch ratios). The gene's levels, FACTORV, came from this.

It also splits the image's change (Iteration 276): the converter reports the
changed words' code and the bodies, each encoded exactly, before placement;
what the image changed beyond that is placement - word starts realigned, links
resized. --raw prints every workload's dispatch counts, to compare runs exactly.
"""
import glob, json, math, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]; dbs, shares = [], ['1e-3', '1e-2', '2']
while '--db' in args: i = args.index('--db'); dbs.append(args[i + 1]); del args[i:i + 2]
if '--shares' in args: i = args.index('--shares'); shares = args[i + 1].split(','); del args[i:i + 2]
raw = '--raw' in args
if raw: args.remove('--raw')
if len(args) != 1: sys.exit(__doc__)
recs = {}
for db in dbs or sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md'))):
    for l in open(db, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if isinstance(r, dict) and 'genome' in r and 'id' in r: recs[r['id']] = r
if args[0] not in recs: sys.exit('factor-price: no recorded design %s' % args[0])
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
conv = {}                                   # the converter's own factor lines, per build
_sh = E.sh
def _sh2(cmd, *a, **k):
    r = _sh(cmd, *a, **k)
    if any('layout.py' in str(x) for x in cmd):
        o = r.stdout.decode(errors='replace') if isinstance(r.stdout, bytes) else (r.stdout or '')
        conv['last'] = [l for l in o.splitlines() if l.startswith('factor')]
    return r
E.sh = _sh2
g = E.canon(recs[args[0]]['genome'])
if not E.express(dict(g, factor=1)).get('factor'): sys.exit('factor-price: %s cannot take the gene (not in the tag)' % args[0])
tot, size = {}, {}
for sh in [None] + shares:
    d = os.path.join(E.EV, 'factor-price'); shutil.rmtree(d, ignore_errors=True)
    if sh is not None: E.FACTORV = (0, float(sh))      # level 1 is this share, for this build
    E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, factor=0 if sh is None else 1), d)
    finally: E.PROFILING[0] = False
    size[sh] = os.path.getsize(img); pw = E.private_work(d); conv[sh] = conv.pop('last', [])
    for wl in E.WORK_SEL:
        pf = os.path.join(d, 'p-' + wl)
        E.sh([eng, img], cwd=pw, inp=E.program(wl), timeout=240, cpu=20, env=dict(os.environ, VMPROF=pf))
        tot[(sh, wl)] = sum(int(f[2]) for f in (l.split() for l in open(pf)) if f[0] == 'I')
        assert tot[(sh, wl)], 'factor-price: %s ran nothing' % wl
    shutil.rmtree(d, ignore_errors=True)
print('%s: image %d bytes with the gene off' % (args[0], size[None]))
for sh in shares:
    r = [tot[(sh, w)] / tot[(None, w)] for w in E.WORK_SEL]
    print('  share < %-6s image %+5d bytes  dispatches %+.3f%% (geometric mean)  %s' % (sh, size[sh] - size[None],
          100.0 * (math.exp(sum(map(math.log, r)) / len(r)) - 1), '  '.join('%s %+.2f%%' % (w, 100.0 * (x - 1)) for w, x in zip(E.WORK_SEL, r))))
    m = [re.search(r': (-?\d+) bytes before placement', l) for l in conv[sh]]
    m = [x for x in m if x]
    if m:
        net = int(m[0].group(1)); d_ = size[sh] - size[None]
        print('    the converter: %s' % [l for l in conv[sh] if 'before placement' in l][0][len('factor: '):])
        print('    so: %d bytes before placement, %+d by placement (word starts realigned, links resized) = %+d in the image' % (-net, d_ + net, d_))
if raw:
    for wl in E.WORK_SEL: print('  raw %-10s off %d  %s' % (wl, tot[(None, wl)], '  '.join('%s %d' % (sh, tot[(sh, wl)]) for sh in shares)))
