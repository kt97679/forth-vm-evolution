"""results/drafts/chainCD-agreement-598.py [CHAIN_D_DIR] - each host's sessions against each other on the shortlist's 40
(Iteration 598; results/final-pick-chainCD-seed86.md): chain B against chain C on each line (chain C's predictions 3 and
4), chain D's sessions within the night - the median pairwise Spearman and its range (chain D's prediction 5) - and the
laptop's lines the same way (idle at 64 and 32 bits). Then each line's chain-D spread: the fastest design's share of
sessions it is fastest in, and per design the coefficient of variation over the sessions (the median over the 40).
From results/chainB-seed86/, results/chainC-seed86/ and chain D's sessions laid out by lab/evolve/chain-sessions.py
(default results/chainD-seed86/, DIR/sK)."""
import glob, json, math, os, re, statistics, sys
D = sys.argv[1] if len(sys.argv) > 1 else 'results/chainD-seed86'
IDS = [json.loads(l)['id'] for l in open('results/shortlist-seed86.md') if l.startswith('{')]
LINES = ('dream.lan-prebuilt64', 'dream.lan-prebuilt32', 'rage.lan-prebuiltarm')


def host(f):
    return {x['id']: x['speed_here'] for x in json.load(open(f))['designs'] if x.get('speed_here')}


def lap(f, k):
    return {j['id']: j[k] for j in (json.loads(l) for l in open(f) if l.startswith('{"id"')) if j.get(k)}


def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def sp(a, b):
    ids = [i for i in IDS if i in a and i in b]
    ra, rb = rank([a[i] for i in ids]), rank([b[i] for i in ids]); n = len(ids); ma = sum(ra) / n; mb = sum(rb) / n
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5


sd = sorted(glob.glob(os.path.join(D, 's*')), key=lambda p: int(re.search(r's(\d+)$', p).group(1)))
src = {}
for ln in LINES:
    src[ln] = (host('results/chainB-seed86/%s.out.json' % ln), host('results/chainC-seed86/%s.out.json' % ln),
               [host(os.path.join(d, ln + '.out.json')) for d in sd if os.path.exists(os.path.join(d, ln + '.out.json'))])
for k, nm in (('idle', 'the laptop alone, 64 bits'), ('idle32', 'the laptop alone, 32 bits')):
    src[nm] = (lap('results/chainB-seed86/loadtest.md', k), lap('results/chainC-seed86/loadtest.md', k),
               [lap(os.path.join(d, 'loadtest.md'), k) for d in sd if os.path.exists(os.path.join(d, 'loadtest.md'))])
print('| line | B against C | D: sessions | D: median pairwise (range) | D against B | D against C | D\'s fastest (sessions it leads) | median CV a design |')
print('|---|---|---|---|---|---|---|---|')
for ln, (b, c, ds) in src.items():
    pw = [sp(ds[i], ds[j]) for i in range(len(ds)) for j in range(i + 1, len(ds))]
    gm = {i: math.exp(statistics.mean(math.log(s[i]) for s in ds if i in s)) for i in IDS if any(i in s for s in ds)}
    lead = [min((s[i], i) for i in IDS if i in s)[1] for s in ds]; top = min(gm, key=gm.get)
    cv = statistics.median(statistics.pstdev([s[i] for s in ds if i in s]) / statistics.mean([s[i] for s in ds if i in s]) for i in gm)
    print('| %s | %.3f | %d | %s | %.3f | %.3f | %s (%d of %d) | %.2f%% |' % (ln, sp(b, c), len(ds),
          '%.3f (%.3f-%.3f)' % (statistics.median(pw), min(pw), max(pw)) if pw else '-', sp(gm, b), sp(gm, c), top,
          lead.count(top), len(ds), cv * 100))
