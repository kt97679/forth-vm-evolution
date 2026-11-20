#!/usr/bin/env python3
"""results/drafts/holders-laptop-713.py LIST PACK_MD - the ten holders' records in LIST (results/followup-seed96-roles.md)
replaced by chain A's measure-ids pack's (measure-ids.md: the laptop's memory and speeds; the binary, image and programs'
code the same bytes), the new-roles plan's step 1 (results/drafts/new-roles-plan-705.md) before process-followup.sh.
Each replaced line keeps its place; the pack's "why" is LIST's own. Prints a line per holder: the memory and speed before
and after. Refuses when an id is missing in either, or a size differs (another build)."""
import json, sys

lst, pack = sys.argv[1], sys.argv[2]
new = {}
for l in open(pack):
    if l.startswith('{"'):
        r = json.loads(l); new[r['id']] = r
out, seen = [], set()
for l in open(lst):
    if l.startswith('{"') and '"genome": {' in l:
        r = json.loads(l)
        if r['id'] in new:
            n = new[r['id']]
            for k in ('bin', 'size', 'app', 'total'):
                if r.get(k) != n.get(k): sys.exit('%s: %s %s here, %s in the pack - another build' % (r['id'], k, r.get(k), n.get(k)))
            print('%s  memory %3d -> %3d KB  speed %.4f -> %.4f  at 32 bits %.4f -> %.4f  (%s)' % (r['id'], r['rss'], n['rss'],
                  r['speed'], n['speed'], r['speed32'], n['speed32'], r.get('src')))
            n = dict(n); n['why'] = r.get('why', n.get('why')); n['src'] = 'measure-ids.py (chain A, the laptop)'
            l = json.dumps(n, sort_keys=True) + '\n'; seen.add(r['id'])
    out.append(l)
miss = set(new) - seen
if miss: sys.exit('not in %s: %s' % (lst, ' '.join(sorted(miss))))
open(lst, 'w').write(''.join(out))
print('%d holders replaced in %s' % (len(seen), lst))
