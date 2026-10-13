#!/usr/bin/env python3
"""gene-equiv.py [REV] - the evolver's genes behave as they did at an earlier commit (Iteration 276).

Moving genes into the gene table (prompts/17, GENES.md "Adding a gene") must not
change what any design is. This imports lab/evolve/evolve.py as it is and as it
was at REV (default HEAD~1 - give the commit before the change), and requires,
over every genome recorded in results/*.md: the same id and the same expression;
and, seeded alike, the same 3,000 mutations, 1,000 random genomes and 1,000
crossovers. Two helpers that read build data (design_pairs, opcall_avail) are
stubbed alike in both. A control (prompts/15) then reorders one gene's values in
the new copy: the mutations must come out different, or the comparison is blind.

Iteration 276's table: 2,876 genomes - every id, expression, mutation, draw and
crossover the same; the control caught.

    python3 lab/evolve/gene-equiv.py HEAD~1     PASS, or FAIL and how many differ
"""
import copy, glob, json, os, random, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
rev = sys.argv[1] if len(sys.argv) > 1 else 'HEAD~1'
old = subprocess.run(['git', '-c', 'safe.directory=*', 'show', '%s:lab/evolve/evolve.py' % rev], cwd=ROOT, capture_output=True, text=True)
if old.returncode: sys.exit('gene-equiv: no lab/evolve/evolve.py at %s' % rev)
tmp = os.path.join(HERE, '_evolve_at_rev.py')
open(tmp, 'w').write(old.stdout)
try:
    sys.argv = ['x']; sys.path.insert(0, HERE)
    import _evolve_at_rev as B, evolve as A
finally:
    os.remove(tmp)
for M in (A, B):
    M.design_pairs = lambda g, M=M: [list(p) for p in M.SUPER_POOL]
    M.opcall_avail = lambda g, M=M: list(M.OPCALL_POOL)
gs = []
for f in sorted(glob.glob(os.path.join(ROOT, 'results', '*.md'))):
    for l in open(f, errors='replace'):
        if l.startswith('{"bin"'):
            try: gs.append(json.loads(l)['genome'])
            except (ValueError, KeyError): pass
J = lambda x: json.dumps(x, sort_keys=True)
def compare(n_mut=3000, n_rand=1000, n_cross=1000):
    bad = {'id': 0, 'expression': 0, 'mutation': 0, 'random genome': 0, 'crossover': 0}
    for g in gs:
        if A.gid(copy.deepcopy(g)) != B.gid(copy.deepcopy(g)): bad['id'] += 1
        if J(A.express(copy.deepcopy(g))) != J(B.express(copy.deepcopy(g))): bad['expression'] += 1
    for t in range(n_mut):
        g = gs[(t * 7919) % len(gs)]
        if J(A.mutate(copy.deepcopy(g), random.Random(t))) != J(B.mutate(copy.deepcopy(g), random.Random(t))): bad['mutation'] += 1
    for t in range(n_rand):
        if J(A.random_genome(random.Random(t))) != J(B.random_genome(random.Random(t))): bad['random genome'] += 1
    for t in range(n_cross):
        x, y = gs[(t * 31) % len(gs)], gs[(t * 97 + 13) % len(gs)]
        if J(A.crossover(A.canon(copy.deepcopy(x)), A.canon(copy.deepcopy(y)), random.Random(t))) != \
           J(B.crossover(B.canon(copy.deepcopy(x)), B.canon(copy.deepcopy(y)), random.Random(t))): bad['crossover'] += 1
    return bad
bad = compare()
ok = not any(bad.values())
vals, show = A.GENE_VALUES['fsys']                     # the control: one gene's values reordered
A.GENE_VALUES['fsys'] = (tuple(reversed(vals)), show)
caught = compare(n_mut=1500, n_rand=0, n_cross=0)['mutation'] > 0
A.GENE_VALUES['fsys'] = (vals, show)
print('gene-equiv against %s: %s - %d recorded genomes, 3,000 mutations, 1,000 random genomes, 1,000 crossovers; differing: %s; control %s'
      % (rev, 'PASS' if ok and caught else 'FAIL', len(gs), ', '.join('%s %d' % kv for kv in bad.items()), 'caught' if caught else 'NOT caught - the comparison is blind'))
sys.exit(0 if ok and caught else 1)
