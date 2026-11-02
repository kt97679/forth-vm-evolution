"""results/drafts/chainA-agreement-585.py [LOADTEST.md] [CHAIN_DIR] - the machines' agreement on chain A's 232 candidates
(Iteration 585; results/final-pick-chainA-seed86.md): dream against the laptop at each width, the slower candidates, and
within the fast band (under 0.25 on the laptop at 64 bits) every pair of the readings; the JIT count. From the repository."""
import json, re, sys, importlib.util
P = sys.argv[1] if len(sys.argv) > 1 else '/tmp/process/forth-vm-evolution-loadtest-d804d66d9-fury-20261102-064323/pack/loadtest.md'
R = (sys.argv[2] if len(sys.argv) > 2 else '/tmp/process/chain-20261102-053635') + '/remote/'
lap = {}
for l in open(P):
    c = [x.strip() for x in l.split('|')]
    if len(c) > 11 and re.fullmatch(r'[0-9a-f]{10}', c[1]):
        try: lap[c[1]] = dict(inrun=float(c[3]), idle=float(c[5]), loaded=float(c[6]), inrun32=float(c[8]), idle32=float(c[9]), loaded32=float(c[10]))
        except ValueError: pass
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r
def sp(a, b):
    ra, rb = rank(a), rank(b); n = len(a); ma = sum(ra) / n; mb = sum(rb) / n
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
d = {w: {x['id']: x['speed_here'] for x in json.load(open(R + 'dream.lan-prebuilt%s/out.json' % w))['designs'] if x.get('speed_here')} for w in ('64', '32')}
rd = {'laptop 64 in-run': lambda i: lap[i]['inrun'], 'laptop 64': lambda i: lap[i]['idle'], 'laptop 64 loaded': lambda i: lap[i]['loaded'],
      'laptop 32 in-run': lambda i: lap[i]['inrun32'], 'laptop 32': lambda i: lap[i]['idle32'], 'laptop 32 loaded': lambda i: lap[i]['loaded32'],
      'dream 64': lambda i: d['64'][i], 'dream 32': lambda i: d['32'][i]}
A = [i for i in lap if i in d['64'] and i in d['32']]
S = lambda a, b, ids: sp([rd[a](i) for i in ids], [rd[b](i) for i in ids])
for w in ('64', '32'):
    slow = [i for i in A if rd['laptop ' + w](i) >= 0.25]
    print('all %d: dream %s against the laptop %.3f; the %d slower (0.25 and up) %.3f' % (len(A), w, S('dream ' + w, 'laptop ' + w, A), len(slow), S('dream ' + w, 'laptop ' + w, slow)))
F = [i for i in A if lap[i]['idle'] < 0.25]
print('the fast band (laptop 64 under 0.25): %d' % len(F))
for a, b in (('laptop 64 in-run', 'laptop 64'), ('laptop 64', 'laptop 64 loaded'), ('laptop 32 in-run', 'laptop 32'), ('laptop 32', 'laptop 32 loaded'),
             ('laptop 64', 'laptop 32'), ('dream 64', 'dream 32'), ('laptop 64', 'dream 64'), ('laptop 64', 'dream 32'), ('laptop 32', 'dream 32'), ('laptop 32', 'dream 64')):
    print('  %-17s ~ %-17s %.3f' % (a, b, S(a, b, F)))
spec = importlib.util.spec_from_file_location('E', 'lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
G = {x['id']: x['genome'] for x in json.load(open(R + 'dream.lan-prebuilt64/designs.json'))}
print('  JIT designs in the fast band: %d of %d' % (sum(bool(E.express(E.canon(G[i])).get('jit')) for i in F), len(F)))
