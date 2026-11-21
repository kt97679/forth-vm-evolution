#!/usr/bin/env python3
"""results/drafts/chainC-list-714.py LISTB CANDC POOLSIZES OUT OUTARM - chain C's list (Iteration 714; the owner: 6 hours,
"our goal is not to lose any potentially good designs"). Every design chain B could not settle, beside the designs it
settled on:
  - results/drafts/chainC-candidates-713.md (CANDC): the 5 JIT-free designs the batch moved onto the front (e51c01ba10 and
    4acee9a48e for small and fast on ARMv7, three small-end trades) and the 4 of the smallest JIT design's middle;
  - chain B's pool-sizes.py finds (POOLSIZES: its pool-sizes.md) - 23 JIT-free designs 3-7 B below 219878ec89, unmeasured;
  - from chain B's list (LISTB), its records: the ten holders (followup-roles.py needs them), each speed role's leader
    and the designs within 2 SE of it (results/drafts/chainB-714.py), the smallest's contenders, the knee's, the least
    memory's trades and the smallest JIT design's nearest trades.
OUT: every design (the laptop and dream); OUTARM: the Tegra's - the JIT-free designs a size or ARMv7 question needs
(the 23, the 5, the smallest's and small-and-fast's anchors, the fastest portable's tie). One record a line, "why" set."""
import json, sys

lb, cc, ps, out, outarm = sys.argv[1:6]
rec = lambda f: [json.loads(l) for l in open(f) if l.startswith('{"') and '"genome": {' in l]
B = {r['id']: r for r in rec(lb)}
L = {}
def add(r, why, arm=False):
    if r['id'] not in L: L[r['id']] = (dict(r, why=why), arm)
    elif arm: L[r['id']] = (L[r['id']][0], True)
for r in rec(cc):
    add(r, 'chain C candidate (713): ' + r.get('why', ''), arm=r['total'] < 30000)
for r in rec(ps):
    add(r, 'chain B\'s pool-sizes.py: %d B at master (%d before the batch), below 219878ec89\'s 21,673 - unmeasured'
        % (r['total'], r['before_batch']['total']), arm=True)
ANCH = [  # (id, why, the Tegra too)
    ('d727605472', 'chain B: the fastest portable\'s leader (-7.46 % against 782f3ad7ff)', True),
    ('5f7e66b12d', 'chain B: the fastest portable - not separated from d727605472 (+0.24 % +/- 0.16 %), 4.2 % smaller', True),
    ('a8d35bdccc', 'chain B: the fastest on ARMv7 (-2.63 % +/- 0.39 % against 3eb59b271d)', False),
    ('48a012411a', 'chain B: the knee by the rule (bytes -1.38 %, x86 +0.76 % / +0.45 %)', False),
    ('9b15ba26f7', 'chain B: the fastest on x86-64 (-10.65 % against c7c35f9c97)', False),
    ('262a51bc6c', 'chain B: the fastest on x86-64 - not separated from 9b15ba26f7', False),
    ('df097ba2e2', 'chain B: best all-round (-7.53 % against 06b188f45b); x86-64 not separated from 9b15ba26f7', False),
    ('ea782c6094', 'chain B: the fastest on x86-32 (-5.49 % against ee34931cd7)', False),
    ('b5c79bff7e', 'chain B: the fastest on x86-32 - not separated from ea782c6094', False),
    ('69cebcaed9', 'chain B: the fastest on x86-32 - not separated from ea782c6094', False),
    ('11f956db93', 'chain B: the fastest on x86-32 - not separated from ea782c6094, 3.8 % smaller, 16 KB less', False),
    ('b525180392', 'chain B: the fastest on x86-32 - not separated from ea782c6094', False),
    ('163935642a', 'chain B: the fastest on x86-32 - not separated from ea782c6094', False),
    ('219878ec89', 'chain B: the smallest (21,673 B)', True),
    ('90273721a1', 'chain B: the smallest\'s contender - 21,679 B, 11.3 % faster on x86-64 than 219878ec89', True),
    ('5cd995716d', 'chain B: the smallest\'s contender - 21,679 B, tied with 90273721a1', False),
    ('cdea6ab042', 'chain B: the smallest\'s contender - 21,679 B, tied with 90273721a1', False),
    ('21768033b7', 'chain B: the smallest\'s contender - 21,679 B, tied with 90273721a1', False),
    ('71005d8a0d', 'chain B: least memory - a trade at the holder\'s 112 KB (x86 -23 %, ARMv7 +7 %)', False),
    ('16560cb51f', 'chain B: least memory - a trade at the holder\'s 112 KB (x86 -23 %, ARMv7 +7.5 %)', False),
    ('2c841d55e3', 'chain B: least memory - a trade at the holder\'s 112 KB, 23,647 B', False),
    ('5ff17f9000', 'chain B: the smallest JIT design - the nearest trade (35,720 B, x86-64 +8.3 %)', False),
    ('4ba25fac6c', 'chain B: the smallest JIT design - a trade (35,830 B, x86-64 +7.2 %)', False),
    ('a6e8c448f0', 'chain B: the smallest JIT design - a trade (35,830 B, x86-64 +7.3 %)', False)]
HOLD = [('782f3ad7ff', 'fastest', False), ('3eb59b271d', 'arm', False), ('11a56ff9e4', 'knee', False),
        ('ae99617f06', 'smallarm', True), ('fb0d57c8a2', 'memory', False), ('d180351903', 'smallest', True),
        ('c7c35f9c97', 'fast64', False), ('ee34931cd7', 'fast32', False), ('06b188f45b', 'allround', False),
        ('c6f1c1331b', 'smalljit', False)]
for i, why, arm in ANCH: add(B[i], why, arm)
for i, role, arm in HOLD: add(B[i], 'a holder: ' + role, arm)
head = ('# Chain C - the designs chain B could not settle (Iteration 714; results/drafts/chainC-list-714.py)\n\n'
        'Chain C\'s candidates (results/drafts/chainC-candidates-713.md), chain B\'s pool-sizes.py finds, and from chain B\'s '
        'list the holders, each role\'s leader and the designs it does not separate from (results/followup-roles-seed96-roles-b.md). '
        'Sizes master\'s (bin and total at 8-byte cells). Read by measure-ids.py --ids, loadtest.py --ids and xcheck.py '
        '--also @FILE - one record a line.\n\n')
for f, ids, what in ((out, list(L), 'every design'), (outarm, [i for i in L if L[i][1]], 'the Tegra\'s: the JIT-free designs a size or ARMv7 question needs')):
    with open(f, 'w') as o:
        o.write(head + '%s - %d designs.\n\n' % (what, len(ids)))
        for i in ids: o.write(json.dumps(L[i][0], sort_keys=True) + '\n')
    print('chainC-list-714: %s - %d' % (f, len(ids)))
