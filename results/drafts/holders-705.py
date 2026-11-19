#!/usr/bin/env python3
"""results/drafts/holders-705.py OUT [ROUNDS] - the ten roles' holders (results/relf-designs-649.md) measured here under
today's measure (Iteration 705): the size since 678/686 counts the five selection programs' code, so 649's records (binary +
image only) cannot pool with the series' (appsize.one_size, final-pick.py refuse it). Each holder's genome built by
evolve.evaluate at both widths: the binary, the image, the programs' code and the memory exact - as the laptop's build
makes them; the speeds this sandbox's, ROUNDS rounds (default 1) - the chain re-measures them beside the new candidates.
OUT: one record a line, its "why" the role. As the build user."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
out, rounds = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1
sys.argv = ['x']; sys.path.insert(0, os.path.join(HERE, '..', '..', 'lab', 'evolve'))
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
ROLE = {'c7c35f9c97': 'fastest-x86-64', 'ee34931cd7': 'fastest-x86-32', '06b188f45b': 'best-all-round',
        'c6f1c1331b': 'small-jit', '782f3ad7ff': 'portable-fastest', '3eb59b271d': 'portable-arm',
        '11a56ff9e4': 'portable-knee', 'ae99617f06': 'portable-small', 'fb0d57c8a2': 'least-memory',
        'd180351903': 'smallest'}
with open(out, 'w') as o:
    for l in open(os.path.join(HERE, '..', 'relf-designs-649.md')):
        if not l.startswith('{'): continue
        r = json.loads(l)
        g = E.canon(E.require(dict(r['genome'])))
        rec = E.evaluate(g, rounds)
        rec.update(id=E.gid(g), genome=g, gen=0, how='the %s holder (results/relf-designs-649.md), measured here' % ROLE[r['id']],
                   why='a holder: %s (results/relf-designs-649.md) - sizes and memory exact here, speeds this sandbox\'s'
                   % ROLE[r['id']])
        print('%s %-16s %s total %s (bin %s, image %s, app %s) rss %s speed %s speed32 %s' % (
            rec['id'], ROLE[r['id']], rec['status'], rec.get('total'), rec.get('bin'), rec.get('size'), rec.get('app'),
            rec.get('rss'), rec.get('speed') and round(rec['speed'], 4), rec.get('speed32') and round(rec['speed32'], 4)),
            flush=True)
        o.write(json.dumps(rec, sort_keys=True) + '\n')
