# results/rehearsal-405.md - the after-seed-62 batch's rehearsal (Iteration 405); run in a scratch clone with the batch applied.
# Iteration 405: the rehearsal's database - outcomes, 32-bit failures, and the batch's genes among the designs evaluated.
import json, os, re, sys
from collections import Counter
db = sys.argv[1]; os.chdir('/tmp/b62'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
st, w32, n = Counter(), Counter(), 0
G = {k: Counter() for k in ('jithelp', 'jitre', 'jitret', 'tail (gcc)', 'tail (clang)', 'tailpn', 'bfind, tos', 'bfind, no tos')}
for l in open(db):
    try: r = json.loads(l)
    except ValueError: continue
    if 'genome' not in r: continue
    n += 1; s = str(r.get('status')); st[re.sub(r'\d+', 'N', s)[:70]] += 1
    if r.get('why32'): w32[re.sub(r'0x[0-9a-f]+|\d+', 'N', str(r['why32']))[:110]] += 1
    e = E.express(E.canon(r['genome']))
    out = s[:24] if s != 'ok' else ('dead at 32' if r.get('why32') else 'ok' if 'speed32' in r else 'ok, 64 only')
    for k in ('jithelp', 'jitre', 'jitret', 'tailpn'):
        if e.get(k): G[k][out] += 1
    if e.get('tail'): G['tail (clang)' if e.get('compiler') else 'tail (gcc)'][out] += 1
    if e.get('bfind'): G['bfind, tos' if e.get('tos') else 'bfind, no tos'][out] += 1
print('designs', n, '| status', dict(st)); print('why32', dict(w32) or 'none')
for k, c in G.items(): print('  %-14s %s' % (k, dict(c) or '-'))
