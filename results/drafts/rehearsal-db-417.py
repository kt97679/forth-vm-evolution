import json, os, sys
from collections import Counter
os.chdir('/tmp/b70'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
st, w32, enc, bad, n = Counter(), Counter(), Counter(), 0, 0
for l in open('/tmp/b70/build/evolve/db.jsonl'):
    try: r = json.loads(l)
    except ValueError: continue
    if 'genome' not in r: continue
    n += 1; g = r['genome']; st[str(r.get('status'))[:45]] += 1; e = E.express(E.canon(g))
    enc['tag2' if e.get('tag2') else g.get('enc')] += 1
    if r.get('why32'): w32[str(r['why32'])[:60]] += 1
    if not str(r.get('how', '')).startswith('hand-made') and g.get('enc') == 'cv8' and any(g.get(k, 0) != v for k, v in E.FROZEN.items()): bad += 1
print('designs %d | by encoding %s | status %s | 32-bit failures %s | off a frozen value %d' % (n, dict(enc), dict(st), dict(w32) or 'none', bad))
