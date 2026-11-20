#!/usr/bin/env python3
# results/drafts/outliers-chainA-713.py REPO - chain A's readings off their design's median by more than 10 % after each session's shift (Iteration 713: 80 of 35,295, the worst 1.20)
import glob, json, math, os, statistics, sys
ROOT = sys.argv[1]; os.chdir(ROOT)
sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']
import evolve as E
C = {r['id']: r for r in (json.loads(l) for l in open('results/followup-seed96-roles.md') if l.startswith('{"'))}
SL = {json.loads(l)['id'] for l in open('results/followup-seed96-roles-b.md') if l.startswith('{"')}
jit = {i: bool(E.express(E.canon(C[i]['genome'])).get('jit')) for i in C}
HOST = {'dream64': 'dream.lan-prebuilt64.out.json', 'dream32': 'dream.lan-prebuilt32.out.json', 'rage': 'rage.lan-prebuiltarm.out.json'}
src = {k: {} for k in ('lap64', 'lap32', 'lapL64', 'lapL32', 'dream64', 'dream32', 'rage')}
for d in sorted(glob.glob('results/chain-followup96-roles/s[0-9]*'), key=lambda d: int(d.rsplit('s', 1)[1])):
    s = int(d.rsplit('s', 1)[1]); p = os.path.join(d, 'loadtest.md')
    if os.path.exists(p):
        for r in (json.loads(l) for l in open(p) if l.startswith('{"')):
            for k, f in (('lap64', 'idle'), ('lap32', 'idle32'), ('lapL64', 'loaded'), ('lapL32', 'loaded32')):
                if r.get(f): src[k].setdefault(r['id'], {})[s] = r[f]
    for k, f in HOST.items():
        p = os.path.join(d, f)
        if os.path.exists(p):
            for x in json.load(open(p))['designs']:
                if x.get('id') in C and x.get('speed_here'): src[k].setdefault(x['id'], {})[s] = x['speed_here']
# each session's common shift (the median over designs of reading / the design's median), then a design's reading
# against its own median after the shift
out = []
for k, D in src.items():
    sess = sorted({s for v in D.values() for s in v})
    med = {i: statistics.median(v.values()) for i, v in D.items() if len(v) >= 3}
    shift = {s: statistics.median(v[s] / med[i] for i, v in D.items() if i in med and s in v) for s in sess}
    for i, v in D.items():
        if i not in med: continue
        for s, x in v.items():
            r = x / shift[s] / med[i]
            if r > 1.10 or r < 0.90: out.append((r, k, i, s))
out.sort(reverse=True)
print('readings off their design\'s median (after the session\'s shift) by more than 10 %%: %d of %d' % (
    len(out), sum(len(v) for D in src.values() for v in D.values())))
by = {}
for r, k, i, s in out: by.setdefault(k, []).append((r, i, s))
for k, v in by.items():
    print('  %-7s %3d  worst: %s' % (k, len(v), ', '.join('%s s%d %.2f%s' % (i, s, r, '' if i in SL else ' (off the shortlist)') for r, i, s in v[:6])))
json.dump([dict(r=r, line=k, id=i, s=s) for r, k, i, s in out], open('/tmp/outliers-chainA.json', 'w'))
