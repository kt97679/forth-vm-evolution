# results/drafts/simplicity-proposal-408.md, "Approved and built" - run in a scratch clone with the after-seed-62 batch.
# Iteration 409: the freeze rehearsed - every design the search made holds FROZEN's values; outcomes; 32-bit failures.
import json, os, sys
from collections import Counter
os.chdir('/tmp/b64'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
st, w32, enc, bad, hm, n = Counter(), Counter(), Counter(), [], 0, 0
for l in open('/tmp/b64/build/evolve/db.jsonl'):
    try: r = json.loads(l)
    except ValueError: continue
    if 'genome' not in r: continue
    n += 1; g = r['genome']; how = str(r.get('how', r.get('made', '')))
    if n == 1: print('record keys:', sorted(k for k in r if k != 'genome'))
    st[str(r.get('status'))[:45]] += 1; enc[g.get('enc')] += 1
    if r.get('why32'): w32[str(r['why32'])[:60]] += 1
    if how.startswith('hand-made') or g.get('enc') != 'cv8': hm += how.startswith('hand-made'); continue
    off = [k for k, v in E.FROZEN.items() if g.get(k, 0) != v]
    if off: bad.append((r.get('id'), how[:30], off))
print('designs', n, '| hand-made', hm, '| by encoding', dict(enc)); print('status', dict(st)); print('why32', dict(w32) or 'none')
print('designs the search made, off a FROZEN value:', len(bad), bad[:6])
