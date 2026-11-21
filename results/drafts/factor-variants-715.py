# results/drafts/factor-variants-715.py SRC OUT - Iteration 715's test designs for the gene factor in the cross
# compiler: d727605472 and 5f7e66b12d (the fastest portable's pair, chain B) without the fused =I?BRANCH /
# =I?BRANCH8 / DUP?NBRANCH / DUP?NBRANCH8 the cross compiler does not do yet (fac0000001, fac0000002), and
# fac0000001 at factor=3 (--factor-share 2.0: every word, fac0000003). SRC: results/followup-seed96-roles-c.md.
import json, sys
src, out = sys.argv[1], sys.argv[2]
rows = {json.loads(l)['id']: json.loads(l) for l in open(src) if l.startswith('{')}
fb = {'=I?BRANCH', '=I?BRANCH8', 'DUP?NBRANCH', 'DUP?NBRANCH8'}
with open(out, 'w') as f:
    for i, nid, fac in (('d727605472', 'fac0000001', None), ('5f7e66b12d', 'fac0000002', None), ('d727605472', 'fac0000003', 3)):
        r = dict(rows[i]); g = dict(r['genome'])
        g['ops10'] = [o for o in g['ops10'] if o not in fb]
        if fac: g['factor'] = fac
        r['genome'] = g; r['id'] = nid; r['why'] = '715 test variant: %s without the fused branches%s' % (i, ', factor=%d' % fac if fac else '')
        f.write(json.dumps(r) + '\n')
