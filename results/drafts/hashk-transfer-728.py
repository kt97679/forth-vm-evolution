#!/usr/bin/env python3
"""results/drafts/hashk-transfer-728.py ID - does one K per chain count serve every design? (Iteration 728). For the design ID:
entries visited a lookup on corpus, parse and the five programs (hashseed-727.py's model and streams) with today's hash,
with its own searched K, and with each other K that hashseed-727.txt records for that chain count (the smallest's and
portable-fastest's, alone) - the cost of fixing K per chain count instead of searching it per image. Reads only."""
import os, re, sys
DID = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'hashseed-727.py')).read()
src = src[:src.index("print('| chains |")]
sys.argv = ['x', DID]; g = {'__file__': os.path.join(HERE, 'hashseed-727.py'), '__name__': 'x'}; exec(src, g)
price, streams, static_cost = g['price'], g['streams'], g['static_cost']
KS = {}
for l in open(os.path.join(HERE, 'hashseed-727.txt')):
    m = re.match(r'\| (\d+) \| (\d+) / (\d+) \| corpus', l)
    if m: KS.setdefault(int(m.group(1)), []).append(int(m.group(2)))
print('%s: entries visited a lookup - today, its own K, the recorded Ks (hashseed-727.txt, K alone)\n' % DID)
print('| chains | K | corpus | parse | the five programs |'); print('|---:|---|---:|---:|---:|')
for T in (16, 32, 64, 128):
    own = min(range(1, 65536, 2), key=lambda K: static_cost(T, K, False))
    for lab, K in [('today', None), ('own %d' % own, own)] + [('recorded %d' % k, k) for k in KS.get(T, []) if k != own]:
        print('| %d | %s | %s |' % (T, lab, ' | '.join('%.2f' % price(streams[w], T, K, False)[0] for w in ('corpus', 'parse', 'the five programs'))))
