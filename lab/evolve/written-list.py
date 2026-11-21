#!/usr/bin/env python3
"""lab/evolve/written-list.py LIST POOLSIZES.md ... - a chain's pool-sizes.py --write list merged into the chain's list
before its processing (Iteration 721; chain D, 717: the laptop measured LIST's records and the finds pool-sizes.py wrote to
build/evolve/jitband-list.md, which stayed on the laptop). Each pool-sizes.md names what it wrote ("written ids: ...")
and carries every find's record (one JSON line each): the written ids not in LIST are appended to it, their records as
the pack has them (master's sizes; the measure-ids packs, read after this by ids-records.py, give the laptop's memory).
LIST rewritten in place; prints one line - how many appended, and any written id the pack has no record of (an error:
exit 1). lab/evolve/process-followup.sh runs it on the chain's pool-sizes packs."""
import json, sys
if len(sys.argv) < 3: sys.exit(__doc__)
lst, packs = sys.argv[1], sys.argv[2:]
have = {json.loads(l)['id'] for l in open(lst) if l.startswith('{"')}
add, missing = [], []
for p in packs:
    recs, ids = {}, []
    for l in open(p):
        if l.startswith('{"'):
            r = json.loads(l); recs[r['id']] = r
        elif l.startswith('written ids: '): ids = l.split(':', 1)[1].strip().split(',')
    for i in ids:
        if i in have or any(r['id'] == i for r in add): continue
        if i in recs: add.append(dict(recs[i], why='written by pool-sizes.py --write (%s)' % recs[i].get('why', '')))
        else: missing.append(i)
if add:
    with open(lst, 'a') as f:
        for r in add: f.write(json.dumps(r, sort_keys=True) + '\n')
print('written-list.py: %d appended to %s from %d pack(s)%s' % (len(add), lst, len(packs),
      '; NO RECORD for ' + ','.join(missing) if missing else ''))
sys.exit(1 if missing else 0)
