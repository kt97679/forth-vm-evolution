# Iteration 401 (results/fail32-400.md): a database's 32-bit "engine did not compile" deaths split by what the 32-bit
# genome expresses - tail or not, clang or GCC, preserve_none (tailpn) or not. python3 THIS DB, from the repository.
import json, sys
from collections import Counter
db = sys.argv[1]; sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
c = Counter()
for l in open(db):
    if 'engine did not compile' not in l: continue
    r = json.loads(l)
    if r.get('why32') != 'died: engine did not compile': continue
    g = dict(r['genome'], jit=0)
    if (g.get('scale') or 0) > 2: g['scale'] = 2
    ex = E.express(E.canon(g))
    c[('tail' if ex.get('tail') else 'NOT tail', 'clang' if ex.get('compiler') else 'gcc', 'tailpn' if ex.get('tailpn') else '-')] += 1
print(sum(c.values()), dict(c))
