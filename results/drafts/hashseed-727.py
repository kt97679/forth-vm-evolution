#!/usr/bin/env python3
"""results/drafts/hashseed-727.py [ID] - a hash seed searched per image, priced (Iteration 727; from the demoscene survey,
results/drafts/demoscene-ioccc-727.md: crinkler finds its imports by hash and brute-forces its parameters per program).
The kernel's chain hash is v = len ^ b0<<1 ^ b1<<2 masked to the chain count (tools/layout.py's _wl_hash); an XOR seed
would only permute the chains, so the tunable form is multiplicative - h = ((v * K) & 0xFFFF) >> (16 - log2 T), K odd,
one constant the converter would choose for the image's own names (the image header or a -D; a multiply and a shift in
HASH and the Forth walkers). K is chosen on the held-out programs' lookups only (wordfreq, minif, brainless - the
project's rule), every odd K below 65536, by the static walk (each image name's position in its chain, newest first or
by use; a miss walks its chain); then every choice is priced on the workloads' token streams - corpus, parse and the
five selection programs' sources - by results/drafts/chain-order-707.py's simulation (definitions go in front as they
come). Rows: today's hash, chainorder (707: by use), the searched K, and both. Reads only; python3 -B, as the build user."""
import collections, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
DID = sys.argv[1] if len(sys.argv) > 1 else '219878ec89'
src = open(os.path.join(HERE, 'lookup-cache-model.py')).read()
pre = src[:src.index("d = os.path.join(E.EV, 'lcache')")]
ns = {'__file__': os.path.join(HERE, 'lookup-cache-model.py'), '__name__': 'x'}
sys.argv = ['x', DID]; exec(pre, ns); E = ns['E']
body = src[src.index('def h(n, T):'):src.index('works = {}')]
exec(body, ns); lookups, strip = ns['lookups'], ns['strip_line_comments']
rec = None
for f in ('relf-designs-718.md', 'followup-seed96-roles.md'):
    for l in open(os.path.join(ROOT, 'results', f)):
        if l.startswith('{"') and '"%s"' % DID in l: rec = json.loads(l)
    if rec: break
d = os.path.join(E.EV, 'hseed'); sm = d + '.sym'; os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
try: E.build(E.canon(rec['genome'] if rec else E.recorded_genome(DID)), d)
finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
image = []
for l in open(sm):
    n = l.split(None, 2)[2].strip()
    if n and not n.startswith('('): image.append(n)
image = list(dict.fromkeys(image)); IMG = set(image); rank = {n: i for i, n in enumerate(image)}
APPS = os.path.join(ROOT, 'lab', 'evolve', 'apps')
def text_of(names):
    t = ''
    for a in names:
        p = os.path.join(APPS, a + '.fth')
        t += open(p, errors='replace').read() if os.path.exists(p) else ''.join(open(f, errors='replace').read() for f in sorted(glob.glob(os.path.join(APPS, a, '*.f*'))))
    return strip(t)
def v_of(n):
    b = n.encode('latin-1', 'replace'); return len(b) ^ (b[0] << 1) ^ ((b[1] << 2) if len(b) > 1 else 0)
def hfun(T, K):
    s = 16 - (T.bit_length() - 1)
    return (lambda n: v_of(n) & (T - 1)) if K is None else (lambda n: ((v_of(n) * K) & 0xFFFF) >> s)
tst = lookups(text_of(['wordfreq', 'minif', 'brainless']))
train = collections.Counter(n for k, n in tst if k == 'find' and n in IMG)
tmiss = collections.Counter(n for k, n in tst if k == 'find' and n not in IMG)
VI = [(v_of(n), train[n], rank[n]) for n in image]
VM = collections.Counter()
for n, c in tmiss.items(): VM[v_of(n)] += c

def static_cost(T, K, byuse):
    """the held-out lookups' visits under chain function (T, K), definitions ignored: K's search objective"""
    s = 16 - (T.bit_length() - 1); ch = collections.defaultdict(list)
    for v, c, r in VI: ch[(v & (T - 1)) if K is None else (((v * K) & 0xFFFF) >> s)].append((c, r))
    cost = 0
    for k, L in ch.items():
        L.sort(key=(lambda x: (-x[0], -x[1])) if byuse else (lambda x: -x[1]))
        cost += sum(c * (i + 1) for i, (c, r) in enumerate(L))
    for v, c in VM.items():
        cost += c * len(ch.get((v & (T - 1)) if K is None else (((v * K) & 0xFFFF) >> s), ()))
    return cost

def price(stream, T, K, byuse):
    hh = hfun(T, K); chains = collections.defaultdict(list)
    for n in image: chains[hh(n)].insert(0, n)
    if byuse:
        for k in chains: chains[k].sort(key=lambda n: (-train[n], -rank[n]))
    v = f = 0
    for kind, name in stream:
        c = chains[hh(name)]
        try: p = c.index(name) + 1
        except ValueError: p = 0
        f += 1; v += p if p else len(c)
        if kind == 'def': c.insert(0, name)
    return v / f, f

works = {'corpus': strip(open(E.CORPUS).read()) * E.LONG['corpus']}
pf = (E.LONGF or {}).get('parse') or os.path.join(E.ROOT, 'bench', 'parse.fth')
works['parse'] = strip(open(pf).read()) * E.LONG['parse']
works['the five programs'] = text_of(['sim16', 'gc16', 'scan', 'evo', 'shellmix'])
streams = {w: lookups(t) for w, t in works.items()}
genes = rec['genome'] if rec else {}
print('%s (threads gene %s): %d names in the image; the held-out three: %d lookups of image names (%d distinct), %d misses\n'
      % (DID, genes.get('threads'), len(image), sum(train.values()), len(train), sum(tmiss.values())))
print('| chains | K (searched on the held-out three) | workload | visits a lookup today | chainorder | K | K + chainorder |')
print('|---:|---|---|---:|---:|---:|---:|')
for T in (16, 32, 64, 128):
    best = {}
    for byuse in (False, True):
        best[byuse] = min(range(1, 65536, 2), key=lambda K: static_cost(T, K, byuse))
    for w, st in streams.items():
        a, n = price(st, T, None, False); b, _ = price(st, T, None, True)
        c, _ = price(st, T, best[False], False); e, _ = price(st, T, best[True], True)
        print('| %d | %d / %d | %s | %.2f | %.2f (%+.0f%%) | %.2f (%+.0f%%) | %.2f (%+.0f%%) |' % (T, best[False], best[True], w, a,
              b, 100 * (b / a - 1), c, 100 * (c / a - 1), e, 100 * (e / a - 1)))
