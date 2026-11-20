#!/usr/bin/env python3
"""lab/evolve/ids-records.py LIST PACK_MD [PACK_MD ...] - a list's records replaced by a chain's measure-ids packs'
(measure-ids.md: the laptop's memory and speeds; the binary, image and programs' code the same bytes), before
process-followup.sh. Chain A (713): the ten holders in results/followup-seed96-roles.md, one pack. Chain B: every design of
results/followup-seed96-roles-b.md, its first pack the whole list's and four more the lean end's
(results/followup-seed96-roles-b-lean.md) - a design read in several packs gets the MEDIAN of its reads as its memory,
rss and each workload's mem (the 8 KB close call at the lean end: five reads, the medians - the plan's step 1, the owner
at 708), the rest from its first pack (the packs in the order given: name them oldest first); "rss_reads" keeps the reads.
Each replaced line keeps its place; the list's "why" kept. Prints a line per design - the memory and speed before and
after. Refuses when a pack's design is missing from LIST, or a size differs (another build). LIST is rewritten."""
import json, statistics, sys

lst, packs = sys.argv[1], sys.argv[2:]
if not packs: sys.exit(__doc__)
new, reads = {}, {}
for p in packs:
    for l in open(p):
        if l.startswith('{"'):
            r = json.loads(l)
            if r.get('status') != 'ok': continue
            new.setdefault(r['id'], r); reads.setdefault(r['id'], []).append(r)
out, seen = [], set()
for l in open(lst):
    if l.startswith('{"') and '"genome": {' in l:
        r = json.loads(l)
        if r['id'] in new:
            n = dict(new[r['id']]); rs = reads[r['id']]
            for k in ('bin', 'size', 'app', 'total'):
                for x in rs:
                    if r.get(k) != x.get(k): sys.exit('%s: %s %s here, %s in a pack - another build' % (r['id'], k, r.get(k), x.get(k)))
            if len(rs) > 1:
                n['rss'] = statistics.median(x['rss'] for x in rs); n['rss_reads'] = [x['rss'] for x in rs]
                n['mem'] = {w: statistics.median(x['mem'][w] for x in rs if w in x.get('mem', {})) for w in n.get('mem', {})}
            print('%s  memory %3d -> %5.1f KB%s  speed %.4f -> %.4f  at 32 bits %.4f -> %.4f  (%s)' % (r['id'], r['rss'], n['rss'],
                  ' (%d reads: %s)' % (len(rs), ' '.join(str(x['rss']) for x in rs)) if len(rs) > 1 else '',
                  r['speed'], n['speed'], r['speed32'], n['speed32'], r.get('src')))
            n['why'] = r.get('why', n.get('why')); n['src'] = 'measure-ids.py (the laptop, %d read%s)' % (len(rs), 's' if len(rs) > 1 else '')
            l = json.dumps(n, sort_keys=True) + '\n'; seen.add(r['id'])
    out.append(l)
miss = set(new) - seen
if miss: sys.exit('not in %s: %s' % (lst, ' '.join(sorted(miss))))
open(lst, 'w').write(''.join(out))
print('%d records replaced in %s (%d read more than once)' % (len(seen), lst, sum(len(reads[i]) > 1 for i in seen)))
