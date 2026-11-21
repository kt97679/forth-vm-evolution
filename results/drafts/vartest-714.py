#!/usr/bin/env python3
"""results/drafts/vartest-714.py LIST OUT - the designs results/selfhost-fusions-714.md checks, one record a line for
results/drafts/selfhost-ids-714.sh: from LIST (results/followup-seed96-roles-b.md) 48a012411a, 11f956db93, ea782c6094,
a8d35bdccc, 219878ec89 and 90273721a1 as they are, and two made for VAR-OPS - no rtvar design in chains B and C
self-hosts yet (--factor, =I?BRANCH or --guard-abort) - 48a012411a and 11f956db93 with rtvar=1 and varslot=1 (rtvar needs
varslot: express() drops it without), ids v48a012411 and v11f956db9. Then:
  sh results/drafts/selfhost-ids-714.sh OUT knee=48a012411a x32=ea782c6094 x32b=11f956db93 kneevar=v48a012411 \\
     x32bvar=v11f956db9 arm=a8d35bdccc small=219878ec89 small2=90273721a1"""
import json, os, sys
lst, out = sys.argv[1:3]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
C = {r['id']: r for r in (json.loads(l) for l in open(lst) if l.startswith('{"'))}
R = [C[i] for i in ('48a012411a', '11f956db93', 'ea782c6094', 'a8d35bdccc', '219878ec89', '90273721a1')]
for i, nid in (('48a012411a', 'v48a012411'), ('11f956db93', 'v11f956db9')):
    r = dict(C[i]); g = dict(r['genome']); g['rtvar'] = 1; g['varslot'] = 1
    assert E.express(E.canon(g)).get('rtvar'), i
    r.update(genome=g, id=nid, why='a VAR-OPS test: %s with rtvar=1 varslot=1 (Iteration 714)' % i); R.append(r)
with open(out, 'w') as o:
    for r in R: o.write(json.dumps(r, sort_keys=True) + '\n')
print('vartest-714: %s - %d records' % (out, len(R)))
