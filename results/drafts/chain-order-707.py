#!/usr/bin/env python3
"""results/drafts/chain-order-707.py [ID] - the image's names ordered in their chains by use, priced (Iteration 707; the
morphological box's empty cell "dictionary order": the image's chains are in definition order today, every lookup's
walk starting at the newest). Zero bytes: the converter would only link each chain's image names most-used first - user
definitions still go in front, as now. The use: learned from the held-out programs (wordfreq, minif, brainless - never
the selection's, the project's rule: nothing selected by the workloads), counted as lookup-cache-model.py counts a token
stream; priced on the workloads' streams - corpus, parse and the five selection programs' sources (the apps workload
compiles them) - in entries visited per lookup, now and so ordered, at 1-128 chains (the kernel's hash of the length
and two characters). Names not found walk their whole chain either way. Reads only; python3 -I -B, as the build user."""
import collections, glob, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
DID = sys.argv[1] if len(sys.argv) > 1 else '21768033b7'
src = open(os.path.join(HERE, 'lookup-cache-model.py')).read()
pre = src[:src.index("d = os.path.join(E.EV, 'lcache')")]      # its imports and E.setup(), not its run
ns = {'__file__': os.path.join(HERE, 'lookup-cache-model.py'), '__name__': 'x'}
sys.argv = ['x', DID]; exec(pre, ns); E = ns['E']
body = src[src.index('def h(n, T):'):src.index('works = {}')]
exec(body, ns); h, lookups, strip = ns['h'], ns['lookups'], ns['strip_line_comments']
d = os.path.join(E.EV, 'chorder'); sm = d + '.sym'; os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
rec = None
for f in [os.path.join(ROOT, 'results', 'followup-seed96-roles.md')]:
    for l in open(f):
        if l.startswith('{"') and '"%s"' % DID in l: rec = __import__('json').loads(l)
try: E.build(E.canon(rec['genome'] if rec else E.recorded_genome(DID)), d)
finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
image = []
for l in open(sm):
    n = l.split(None, 2)[2].strip()
    if n and not n.startswith('('): image.append(n)
image = list(dict.fromkeys(image))
APPS = os.path.join(ROOT, 'lab', 'evolve', 'apps')
def text_of(names):
    t = ''
    for a in names:
        p = os.path.join(APPS, a + '.fth')
        t += open(p, errors='replace').read() if os.path.exists(p) else ''.join(open(f, errors='replace').read() for f in sorted(glob.glob(os.path.join(APPS, a, '*.f*'))))
    return strip(t)
train = collections.Counter(n for k, n in lookups(text_of(['wordfreq', 'minif', 'brainless'])) if k == 'find')
works = {'corpus': strip(open(E.CORPUS).read()) * E.LONG['corpus']}
pf = (E.LONGF or {}).get('parse') or os.path.join(E.ROOT, 'bench', 'parse.fth')
works['parse'] = strip(open(pf).read()) * E.LONG['parse']
works['the five programs'] = text_of(['sim16', 'gc16', 'scan', 'evo', 'shellmix'])

def price(stream, T, byuse):
    chains = collections.defaultdict(list)
    for n in image: chains[h(n, T)].insert(0, n)          # newest first, as linked
    if byuse:
        rank = {n: i for i, n in enumerate(image)}
        for k in chains: chains[k].sort(key=lambda n: (-train[n], -rank[n]))
    v = f = miss = 0
    for kind, name in stream:
        c = chains[h(name, T)]
        try: p = c.index(name) + 1
        except ValueError: p = 0
        f += 1; v += p if p else len(c); miss += 0 if p else len(c)
        if kind == 'def': c.insert(0, name)
    return v / f, miss / max(v, 1), f

print('%s: %d names in the image; learned from the held-out three: %d lookups of %d distinct image names\n'
      % (DID, len(image), sum(train[n] for n in image), sum(1 for n in image if train[n])))
print('| workload | lookups | chains | visits a lookup now | by use | the walk saved | of it now, names not found |\n|---|---:|---:|---:|---:|---:|---:|')
for w, text in works.items():
    st = lookups(text)
    for T in (1, 16, 32, 64, 128):
        a, ma, n = price(st, T, False); b, _, _ = price(st, T, True)
        print('| %s | %s | %d | %.1f | %.1f | %.0f%% | %.0f%% |' % (w, format(n, ','), T, a, b, 100 * (1 - b / a), 100 * ma))
