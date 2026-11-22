#!/usr/bin/env python3
"""results/drafts/hashk-table-728.py - one K for every design and chain count (Iteration 728). hashk-transfer-728.py found
the K searched per image no better on the workloads than another design's (the held-out three are a noisy objective), so
the gene can be one constant: h = ((v * K) >> 8) & (chains - 1), v kernel.4's (len ^ b0<<1 ^ b1<<2) - the same
expression at every chain count, so the Forth HASH, the engine's and the converter's carry K alone. K is searched over every
odd value below 65,536 on the held-out programs' lookups only (wordfreq, minif, brainless), the objective the sum over
the ten roles (designs/*/record.json) and 16, 32, 64, 128 chains of each one's static walk as a share of today's (each
design and chain count counting alike). Then each role at its own chain count on corpus, parse and the five programs:
today, the one K, and the K hashseed-727.py would search for that image (the multiplicative form) - the price of one
constant. Builds each role once (a profiling build, its symbol map); minutes. Reads only; python3 -B, as the build user."""
import collections, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(HERE, 'hashseed-727.py')).read()
head = src[:src.index("rec = None")]                              # the evolver, the model's lookups
sys.argv = ['x', 'none']; g = {'__file__': os.path.join(HERE, 'hashseed-727.py'), '__name__': 'x'}; exec(head, g)
E, lookups, strip = g['E'], g['lookups'], g['strip']
APPS = os.path.join(ROOT, 'lab', 'evolve', 'apps')
def text_of(names):
    t = ''
    for a in names:
        p = os.path.join(APPS, a + '.fth')
        t += open(p, errors='replace').read() if os.path.exists(p) else ''.join(open(f, errors='replace').read() for f in sorted(glob.glob(os.path.join(APPS, a, '*.f*'))))
    return strip(t)
def v_of(n):
    b = n.encode('latin-1', 'replace'); return len(b) ^ (b[0] << 1) ^ ((b[1] << 2) if len(b) > 1 else 0)
tst = lookups(text_of(['wordfreq', 'minif', 'brainless']))
works = {'corpus': strip(open(E.CORPUS).read()) * E.LONG['corpus']}
pf = (E.LONGF or {}).get('parse') or os.path.join(E.ROOT, 'bench', 'parse.fth')
works['parse'] = strip(open(pf).read()) * E.LONG['parse']
works['the five programs'] = text_of(['sim16', 'gc16', 'scan', 'evo', 'shellmix'])
streams = {w: lookups(t) for w, t in works.items()}
TN = E.THREADS_N
D = []
for rf in sorted(glob.glob(os.path.join(ROOT, 'designs', '*', 'record.json'))):
    rec = json.load(open(rf)); name = os.path.basename(os.path.dirname(rf))
    d = os.path.join(E.EV, 'hktab-' + name); sm = d + '.sym'; os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
    try: E.build(E.canon(rec['genome']), d)
    finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
    image = []
    for l in open(sm):
        n = l.split(None, 2)[2].strip()
        if n and not n.startswith('('): image.append(n)
    image = list(dict.fromkeys(image)); IMG = set(image); rank = {n: i for i, n in enumerate(image)}
    train = collections.Counter(n for k, n in tst if k == 'find' and n in IMG)
    VM = collections.Counter(v_of(n) for k, n in tst if k == 'find' and n not in IMG)
    D.append(dict(name=name, id=rec['id'], T=TN.get(rec['genome'].get('threads', 0), 32), image=image, rank=rank,
                  VI=[(v_of(n), train[n], rank[n]) for n in image], VM=VM))
def chain(v, T, K, form):
    if K is None: return v & (T - 1)
    return ((v * K) >> 8) & (T - 1) if form == 'one' else ((v * K) & 0xFFFF) >> (16 - (T.bit_length() - 1))
def static(dd, T, K, form):
    ch = collections.defaultdict(list)
    for v, c, r in dd['VI']: ch[chain(v, T, K, form)].append((c, r))
    cost = 0
    for L in ch.values():
        L.sort(key=lambda x: -x[1]); cost += sum(c * (i + 1) for i, (c, r) in enumerate(L))
    for v, c in dd['VM'].items(): cost += c * len(ch.get(chain(v, T, K, form), ()))
    return cost
def price(dd, stream, T, K, form):
    chains = collections.defaultdict(list)
    for n in dd['image']: chains[chain(v_of(n), T, K, form)].insert(0, n)
    v = f = 0
    for kind, name in stream:
        c = chains[chain(v_of(name), T, K, form)]
        try: p = c.index(name) + 1
        except ValueError: p = 0
        f += 1; v += p if p else len(c)
        if kind == 'def': c.insert(0, name)
    return v / f
TS = (16, 32, 64, 128)
today = {(dd['name'], T): static(dd, T, None, 'one') for dd in D for T in TS}
best = min(range(1, 65536, 2), key=lambda K: sum(static(dd, T, K, 'one') / today[(dd['name'], T)] for dd in D for T in TS))
print('One K for the ten roles and every chain count: K = %d (h = ((v * K) >> 8) & (chains - 1)); the held-out objective %.3f of today\'s\n'
      % (best, sum(static(dd, T, best, 'one') / today[(dd['name'], T)] for dd in D for T in TS) / (len(D) * len(TS))))
print('| role | id | chains | workload | today | the one K | its own K (727\'s form) |'); print('|---|---|---:|---|---:|---:|---:|')
for dd in D:
    T = dd['T']; own = min(range(1, 65536, 2), key=lambda K: static(dd, T, K, 'mul'))
    for w, st in streams.items():
        a, b, c = price(dd, st, T, None, 'one'), price(dd, st, T, best, 'one'), price(dd, st, T, own, 'mul')
        print('| %s | %s | %d | %s | %.2f | %.2f (%+.0f%%) | %.2f (%+.0f%%) |' % (dd['name'], dd['id'], T, w, a, b, 100 * (b / a - 1), c, 100 * (c / a - 1)), flush=True)
