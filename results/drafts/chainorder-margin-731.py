#!/usr/bin/env python3
"""results/drafts/chainorder-margin-731.py - what chainorder would add to hashk as built (Iteration 731). The ten roles
(results/drafts/hashk-table-728.py's model and streams, each role's image names and chain count): entries visited a
lookup on corpus, parse and the five programs with hashk's one K (newest first in each chain, as today), and with the
same chains in use order - each chain's names by their lookups in the held-out three (wordfreq, minif, brainless), the
rest newest first; definitions in front as they come. The margin is chainorder's, before its signed links' bytes
(+19-73 B, 710). Reads only; python3 -B, as the build user, in a built tree; minutes (it builds each role once)."""
import collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'hashk-table-728.py')).read()
src = src[:src.index('TS = (16, 32, 64, 128)')]                  # the roles built, the model's functions
g = {'__file__': os.path.join(HERE, 'hashk-table-728.py'), '__name__': 'x'}; exec(src, g)
D, streams, chain, v_of, tst = g['D'], g['streams'], g['chain'], g['v_of'], g['tst']
K = 18835
def price(dd, stream, T, byuse):
    train = collections.Counter(n for k, n in tst if k == 'find' and n in dd['rank'])
    chains = collections.defaultdict(list)
    for n in dd['image']: chains[chain(v_of(n), T, K, 'one')].insert(0, n)
    if byuse:
        for c in chains.values(): c.sort(key=lambda n: (-train[n], -dd['rank'][n]))
    v = f = 0
    for kind, name in stream:
        c = chains[chain(v_of(name), T, K, 'one')]
        try: p = c.index(name) + 1
        except ValueError: p = 0
        f += 1; v += p if p else len(c)
        if kind == 'def': c.insert(0, name)
    return v / f
print('chainorder on top of hashk (K %d): entries visited a lookup, hashk alone -> hashk and use order\n' % K)
print('| role | chains | corpus | parse | the five programs |'); print('|---|---:|---|---|---|')
for dd in D:
    T = dd['T']; cells = []
    for w in ('corpus', 'parse', 'the five programs'):
        a, b = price(dd, streams[w], T, False), price(dd, streams[w], T, True)
        cells.append('%.2f -> %.2f (%+.0f%%)' % (a, b, 100 * (b / a - 1)))
    print('| %s | %d | %s |' % (dd['name'], T, ' | '.join(cells)), flush=True)
