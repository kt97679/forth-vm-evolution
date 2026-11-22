#!/usr/bin/env python3
"""results/drafts/chainorder-est-727.py ID CHAINS K_ALONE K_WITH OUT - chainorder priced in instructions from hashk's prototype
(Iteration 728). hashk-727.py measured, on a real build, the instructions K alone saves on corpus and parse (OUT: its
output); hashseed-727.py's model gives the entries visited a lookup there, today and with K (the same token streams). Their
ratio is the instructions one visited entry costs in that design's lookup (a Forth walk or klookup's C one). chainorder's
visits - alone, and with K (its own searched K, K_WITH) - priced at that cost: the instructions it would save, as a share of
the workload's, with no build of the signed links it needs (results/drafts/demoscene-ioccc-727.md; 707, 710). The
assumption, said: a visit costs the same in either chain order - the walk's loop is the same; only how many entries it
visits changes. Reads only; python3 -B, as the build user, in a built tree."""
import os, re, sys
DID, T, KA, KW, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'hashseed-727.py')).read()
src = src[:src.index("print('| chains |")]                         # the model: builds the design, reads the streams
sys.argv = ['x', DID]; g = {'__file__': os.path.join(HERE, 'hashseed-727.py'), '__name__': 'x'}; exec(src, g)
price, streams = g['price'], g['streams']
ir = {}
for l in open(OUT):
    m = re.match(r'\s+(\w+)\s+dispatches\s+[\d,]+ ->\s+[\d,]+\s+[\d.]+\s+instructions\s+([\d,]+) ->\s+([\d,]+)', l)
    if m: ir[m.group(1)] = (int(m.group(2).replace(',', '')), int(m.group(3).replace(',', '')))
print('%s, %d chains (K %d alone, %d with chainorder): instructions a visited entry, from hashk\'s prototype (%s)\n' % (DID, T, KA, KW, os.path.basename(OUT)))
print('| workload | lookups | visits a lookup: today / K / chainorder / both | instructions saved by K (measured) | a visit | chainorder alone (est.) | both (est.) |')
print('|---|---:|---|---:|---:|---:|---:|')
for w, key in (('corpus', 'corpus'), ('parse', 'parse')):
    a, n = price(streams[w], T, None, False); c, _ = price(streams[w], T, KA, False)
    b, _ = price(streams[w], T, None, True); e, _ = price(streams[w], T, KW, True)
    base, prot = ir[key]; ipv = (base - prot) / ((a - c) * n)
    print('| %s | %d | %.2f / %.2f / %.2f / %.2f | %.1f %% | %.1f | %.1f %% | %.1f %% |' % (w, n, a, c, b, e,
          100 * (base - prot) / base, ipv, 100 * (a - b) * n * ipv / base, 100 * (a - e) * n * ipv / base))
