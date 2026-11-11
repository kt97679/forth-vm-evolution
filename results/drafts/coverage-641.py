#!/usr/bin/env python3
"""results/drafts/coverage-641.py - which designs on the pooled portable front were never measured across machines
(Iteration 641). Every reading the repository holds: each chain's remote out.json (dream at both widths, the Tegra) and
each laptop loadtest.md under results/chain*/. The pool before seed 91 (results/portable-front-seed90.md, 528) and seed
91's own (results/screen-seed91.md, results/followup-seed91.md). Writes results/drafts/coverage-641.txt: the counts, then
"- ID origin" for each pool design on no remote line (the final check's list reads them, finalcheck-641.py)."""
import collections, glob, json, os, sys
R = 'results'; recs = lambda f: [json.loads(l) for l in open(f) if l.startswith('{')]
remote = collections.defaultdict(set); lap = set()
for f in glob.glob(R + '/chain*/**/*.out.json', recursive=True):
    h = os.path.basename(f); m = 'rage' if 'arm' in h else 'dream32' if '32' in h else 'dream64'
    try: o = json.load(open(f))
    except Exception: continue
    for x in o.get('designs', []):
        if x.get('speed_here'): remote[x['id']].add(m)
for f in glob.glob(R + '/chain*/**/loadtest.md', recursive=True):
    for l in open(f, errors='replace'):
        if l.startswith('{"'):
            r = json.loads(l)
            if r.get('idle'): lap.add(r['id'])
pool = {r['id']: r for r in recs(R + '/portable-front-seed90.md')}
s91 = {r['id']: r for r in recs(R + '/screen-seed91.md') + recs(R + '/followup-seed91.md') if r['id'] not in pool}
lists = {os.path.basename(f): {r['id'] for r in recs(f)} for f in glob.glob(R + '/screen-seed*.md') + glob.glob(R + '/followup-seed*.md')
         + glob.glob(R + '/portable-front-seed8*.md')}
out = []
cls = lambda i: ('all three' if {'rage', 'dream32', 'dream64'} <= remote.get(i, set()) else 'some' if remote.get(i) else 'none')
for name, P in (('the pool before seed 91', pool), ('seed 91\'s own', s91)):
    c = collections.Counter((cls(i), i in lap) for i in P)
    out.append('%s: %d - %s' % (name, len(P), ', '.join('remote %s%s %d' % (a, ', the laptop' if b else '', n) for (a, b), n in sorted(c.items()))))
miss = sorted((i for i in pool if cls(i) == 'none'), key=lambda i: pool[i]['speed'])
inl = lambda i: [k for k, v in lists.items() if i in v]
out.append('the pool\'s designs on no remote line: %d - in no follow-up or screen list %d' % (len(miss), sum(1 for i in miss if not inl(i))))
for i in miss:
    r = pool[i]
    out.append('- %s speed %.4f, 32-bit %.4f, %d B, %d KB; %s%s' % (i, r['speed'], r['speed32'], r['total'], r['rss'], str(r.get('how', ''))[:60],
                                                                   ('; in ' + ', '.join(inl(i))) if inl(i) else ''))
open(R + '/drafts/coverage-641.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:3]))
