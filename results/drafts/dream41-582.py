#!/usr/bin/env python3
"""results/drafts/dream41-582.py REMOTE - dream's reading of the fast-end file's 41 (Iteration 582): seed 84's best bred
design against the best of the rest, at each width, the split results/drafts/fastend-judge-575.py made on the laptop's
re-measure (bred by results/fastend-remeasure-575.md's "why"). REMOTE: the seed 86 chain archive's remote/ directory
(dream.lan-prebuilt64/out.json and dream.lan-prebuilt32/out.json; each design's speed_here is dream's, against s6
measured there; speed is the laptop's in-run number, carried along). Run from the repository root.
Seed 86's chain: the bred lead -0.6% at 64 bits, +0.2% at 32 - against 5.9% idle on the laptop's re-measure (576)."""
import json, statistics, sys
R = sys.argv[1]
I = {}
for l in open('results/fastend-remeasure-575.md'):
    if l.startswith('{'):
        r = json.loads(l); I[r['id']] = r
isbred = lambda i: I[i]['why'].startswith('seed 84 bred')
for w in ('64', '32'):
    D = json.load(open(R + '/dream.lan-prebuilt%s/out.json' % w))['designs']
    sp = {x['id']: x['speed_here'] for x in D if x.get('id') in I and x.get('speed_here')}
    b = sorted((s, i) for i, s in sp.items() if isbred(i)); o = sorted((s, i) for i, s in sp.items() if not isbred(i))
    print('%s bits: %d of %d with a speed here; bred %d, the rest %d' % (w, len(sp), len(I), len(b), len(o)))
    print('  the best bred %s %.4f, the best of the rest %s %.4f (%s) - bred ahead %+.1f%% (the bar 2%%)'
          % (b[0][1], b[0][0], o[0][1], o[0][0], I[o[0][1]]['why'], 100 * (o[0][0] / b[0][0] - 1)))
    for k, g in (('bred', b), ('rest', o)):
        print('  %s: median %.4f; the best 3 %s' % (k, statistics.median(s for s, _ in g), ', '.join('%s %.4f' % (i, s) for s, i in g[:3])))
