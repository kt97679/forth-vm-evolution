#!/usr/bin/env python3
"""results/drafts/dream32-variants-612.py - the designs of the dream 32-bit experiment (Iteration 612; the owner: "let's
try it"). The follow-up chain (results/followup-roles-seed87.md): a lineage of GCC designs runs about twice the laptop's
time on dream (the i7-6700) at 4-byte cells against 1.24 for the 45, normal at 8-byte cells - the same binaries, so the
CPU. The genes that separate it are confounded (regpin, rtimm 2, nogcse, alignhot 3, lto, GCC, ...): each is reverted
alone here on two of the lineage - 9f8811f7f4 (the laptop's fastest at 32 bits, 2.09) and 690981ca5b (relf's ARMv7
design, 1.81) - beside them and 782f3ad7ff (clang, 1.07) as the control. A variant whose change express() drops has
its base's id (gid hashes the expression) and is left out. Writes results/candidates-dream32-612.md (xcheck.py finds
genomes in results/candidates-*.md; loadtest.py --ids reads them) and prints each variant's change as expressed. As the
build user (it imports the evolver)."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
R = {json.loads(l)['id']: json.loads(l) for l in open(os.path.join(ROOT, 'results/followup-seed87.md')) if l.startswith('{')}
BASES, CONTROL = ('9f8811f7f4', '690981ca5b'), '782f3ad7ff'
REVERT = (('regpin', 0), ('rtimm', 0), ('nogcse', 0), ('alignhot', 0), ('align1', 1), ('noreorder', 0), ('gotodup', 0),
          ('lto', 0), ('noinls', 0), ('compiler', 1))
short = lambda v: '%d ops' % len(v) if isinstance(v, list) and len(v) > 3 else v
out = []
for i in BASES + (CONTROL,):
    r = dict(R[i]); r['why'] = 'dream32 experiment (612): %s' % ('the control' if i == CONTROL else 'a base')
    out.append(r)
for b in BASES:
    g = E.canon(R[b]['genome']); e = E.express(g)
    for k, v in REVERT:
        g2 = E.canon(dict(g, **{k: v})); e2 = E.express(g2); i2 = E.gid(g2)
        if i2 == R[b]['id']:
            print('%s %s=%s: not expressed or no change - left out' % (b, k, v)); continue
        d = {x: (short(e.get(x)), short(e2.get(x))) for x in sorted(set(e) | set(e2)) if e.get(x) != e2.get(x)}
        print('%s %s=%s -> %s: %s' % (b, k, v, i2, ', '.join('%s %s->%s' % (x, a, c) for x, (a, c) in d.items())))
        out.append({'id': i2, 'genome': g2, 'status': 'ok', 'base': b, 'reverted': '%s=%s' % (k, v),
                    'why': 'dream32 experiment (612): %s with %s=%s' % (b, k, v)})
assert len({r['id'] for r in out}) == len(out)
with open(os.path.join(ROOT, 'results/candidates-dream32-612.md'), 'w') as f:
    f.write('# The dream 32-bit experiment\'s designs (Iteration 612; results/drafts/dream32-variants-612.py): two of the slow\n'
            '# lineage, each with one gene reverted at a time, and the control - measured on the laptop, dream at both widths and\n'
            '# the Tegra in seed 88\'s chain. One record a line.\n\n')
    for r in out: f.write(json.dumps(r, sort_keys=True) + '\n')
print('%d designs: %d bases, the control, %d variants' % (len(out), len(BASES), len(out) - len(BASES) - 1))
