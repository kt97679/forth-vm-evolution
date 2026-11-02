"""results/drafts/chainB-agreement-587.py [LOADTEST.md] [CHAIN_DIR] - the machines' agreement on chain B's 40 (Iteration
587; results/final-pick-chainB-seed86.md): the laptop's sessions, rage against the laptop by the JIT, chain A against
chain B where chain A's tables keep both readings, and the across-machines top over all 232 rage measured (a proxy:
the in-run x86 speeds). From the repository and chain B's readings kept in results/chainB-seed86/."""
import glob, json, math, re, sys, importlib.util
P = sys.argv[1] if len(sys.argv) > 1 else 'results/chainB-seed86/loadtest.md'      # 587: chain B's readings, kept
R = sys.argv[2] if len(sys.argv) > 2 else 'results/chainB-seed86/'                 # each host's out.json as HOST.out.json
lap = {j['id']: j for j in (json.loads(l) for l in open(P) if l.startswith('{"id"'))}
rec = {r['id']: r for r in (json.loads(l) for l in open('results/candidates-final-seed86.md') if l.startswith('{'))}
host = {h: {x['id']: x['speed_here'] for x in json.load(open(R + h + '.out.json'))['designs'] if x.get('speed_here')}
        for h in ('dream.lan-prebuilt64', 'dream.lan-prebuilt32', 'rage.lan-prebuiltarm')}
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
S = lambda f, g, ids: sp([f(i) for i in ids], [g(i) for i in ids])
spec = importlib.util.spec_from_file_location('E', 'lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
jit = lambda i: bool(E.express(E.canon(rec[i]['genome'])).get('jit'))
A = sorted(lap); J = [i for i in A if jit(i)]; N = [i for i in A if not jit(i)]
print('the laptop, the 40: alone against in-run %.3f (64) %.3f (32); alone against loaded %.3f (64) %.3f (32)' % (
    S(lambda i: lap[i]['idle'], lambda i: lap[i]['inrun'], A), S(lambda i: lap[i]['idle32'], lambda i: lap[i]['inrun32'], A),
    S(lambda i: lap[i]['idle'], lambda i: lap[i]['loaded'], A), S(lambda i: lap[i]['idle32'], lambda i: lap[i]['loaded32'], A)))
F = [i for i in A if lap[i]['idle'] < 0.25]
print('the fast band (under 0.25 alone at 64 bits): %d, %d with the JIT; dream 64 against the laptop %.3f, dream 32 %.3f' % (
    len(F), sum(map(jit, F)), S(lambda i: host['dream.lan-prebuilt64'][i], lambda i: lap[i]['idle'], F),
    S(lambda i: host['dream.lan-prebuilt32'][i], lambda i: lap[i]['idle32'], F)))
ra = host['rage.lan-prebuiltarm']
for name, ids in (('all 40', A), ('the %d with the JIT (JIT off there)' % len(J), J), ('the %d without' % len(N), N)):
    print('rage against the laptop at 32 bits, %s: %.3f; against dream 32 %.3f' % (name, S(lambda i: ra[i], lambda i: lap[i]['idle32'], ids),
          S(lambda i: ra[i], lambda i: host['dream.lan-prebuilt32'][i], ids)))
print('  rage: the JIT designs %.3f-%.3f, the others %.3f-%.3f' % (min(ra[i] for i in J), max(ra[i] for i in J), min(ra[i] for i in N), max(ra[i] for i in N)))
# chain A's tables keep the laptop alone (the set's 10) and the classes' x86 means (21): dream = mean^2 / laptop
T = open('results/final-pick-chainA-seed86.md').read()
a64 = {m[0]: (float(m[1]), float(m[2])) for m in re.findall(r'^\| \d+ \| ([0-9a-f]{10}) \| [^|]+\| ([0-9.]+) \([0-9.]+\) \| [0-9,]+ \| \d+ \| ([0-9.]+) \(', T, re.M)}
cl = {m[0]: (float(m[1]), float(m[2])) for m in re.findall(r'^\| \d+ \| ([0-9a-f]{10}) \| ([0-9.]+) \| ([0-9.]+) \| [0-9.]+ \|', T, re.M)}
B = [i for i in a64 if i in cl and i in lap]
dA = {i: (cl[i][0] ** 2 / a64[i][0], cl[i][1] ** 2 / a64[i][1]) for i in B}
print('chain A against chain B, the %d both tables keep: the laptop alone %.3f (64) %.3f (32); dream %.3f (64) %.3f (32)' % (len(B),
      S(lambda i: a64[i][0], lambda i: lap[i]['idle'], B), S(lambda i: a64[i][1], lambda i: lap[i]['idle32'], B),
      S(lambda i: dA[i][0], lambda i: host['dream.lan-prebuilt64'][i], B), S(lambda i: dA[i][1], lambda i: host['dream.lan-prebuilt32'][i], B)))
print('  dream, B / A by design: 64 bits %s; 32 bits %s' % (' '.join('%.3f' % (host['dream.lan-prebuilt64'][i] / dA[i][0]) for i in B),
      ' '.join('%.3f' % (host['dream.lan-prebuilt32'][i] / dA[i][1]) for i in B)))
for x, y in (('c7c35f9c97', '2af9192e1d'), ('cea114f47e', 'bee0b97bb5')):
    print('  %s / %s alone: chain B %.4f / %.4f (64), %.4f / %.4f (32); chain A %s / %s' % (x, y, lap[x]['idle'], lap[y]['idle'],
          lap[x]['idle32'], lap[y]['idle32'], a64.get(x, ('-',))[0], a64.get(y, ('-',))[0]))
# the across-machines top over every design rage measured, the x86 classes by the in-run speeds (no re-measure outside the 40)
gm = lambda v: math.exp(sum(map(math.log, v)) / len(v))
px = sorted((gm([rec[i]['speed'], rec[i]['speed32'], ra[i]]), i) for i in rec if i in ra and rec[i].get('speed') and rec[i].get('speed32'))
top = px[0][0]
print('the three classes by the in-run x86 speeds, %d designs: the best %s %.4f (%s); within 2%%: %d (%d of them outside the 40); the 40\'s best %s' % (
      len(px), px[0][1], top, 'in the 40' if px[0][1] in lap else 'outside', sum(m <= top * 1.02 for m, _ in px),
      sum(m <= top * 1.02 and i not in lap for m, i in px), next(i for _, i in px if i in lap)))
print('  rage\'s fastest of all %d: %s %.3f (%s)' % (len(ra), min(ra, key=ra.get), min(ra.values()), 'in the 40' if min(ra, key=ra.get) in lap else 'outside'))
