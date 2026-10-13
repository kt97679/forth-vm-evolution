#!/usr/bin/env python3
"""gene-table-test.py - a new gene is one row: a fictional gene works with no code change (Iteration 276).

prompts/17-variants-as-data, step 3. The gene `zzfict` exists only here -
values 0, 5, 7; expressed only under the two-bit tag; a converter option when
expressed - registered with evolve.gene() and nothing else. Required of it,
with every check counted:

  1. every recorded design keeps its id (a late gene off is out of the identity);
  2. expressed on a tag design at 5, dropped from a design without the tag;
  3. mutate() reaches it and sets 5 or 7, never the value it had;
  4. random_genome() draws all three values;
  5. the converter's options for an expressing design are the row's.

And a control (prompts/15): the same row without its rule must make check 2
fail - else check 2 could not tell a working rule from none.

    python3 lab/evolve/gene-table-test.py        PASS, or FAIL and what broke
"""
import copy, glob, json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E

E.design_pairs = lambda g: [list(p) for p in E.SUPER_POOL]     # no profiling builds in a unit test
E.opcall_avail = lambda g: list(E.OPCALL_POOL)
recs = []
for f in sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md'))):
    for l in open(f, errors='replace'):
        if l.startswith('{"bin"'):
            try: recs.append(json.loads(l))
            except ValueError: pass
before = [E.gid(copy.deepcopy(r['genome'])) for r in recs]
fails, n = [], {}
def check(name, ok, why=''):
    n[name] = n.get(name, 0) + 1
    if not ok: fails.append('%s: %s' % (name, why))

E.gene('zzfict', values=(0, 5, 7), needs=lambda g, e: e.get('tag2'), convert=lambda g: ['--zzfict', str(g['zzfict'])])
after = [E.gid(copy.deepcopy(r['genome'])) for r in recs]
for r, a, b in zip(recs, before, after): check('1 ids kept', a == b, r.get('id'))
tag = next(E.canon(r['genome']) for r in recs if E.express(r['genome']).get('tag2'))
plain = E.canon(dict(E.HUMAN['s6-cv8b']))
check('2 expressed under the tag', E.express(dict(tag, zzfict=5)).get('zzfict') == 5)
check('2 dropped without it', 'zzfict' not in E.express(dict(plain, zzfict=5)))
got = set()
for t in range(4000):
    g0 = dict(tag, zzfict=[0, 5, 7][t % 3])
    g1, how = E.mutate(copy.deepcopy(g0), random.Random(t))
    if g1['zzfict'] != g0['zzfict']:
        got.add(g1['zzfict']); check('3 mutated to another value', g1['zzfict'] in (0, 5, 7) and g1['zzfict'] != g0['zzfict'], how)
        check('3 named in the record', 'zzfict=%d' % g1['zzfict'] in how, how)
check('3 reached', bool(got), 'mutate() never touched the gene in 4000 tries')
drawn = {E.random_genome(random.Random(t)).get('zzfict') for t in range(600)}
check('4 all values drawn', drawn >= {0, 5, 7}, sorted(drawn))
g5 = dict(tag, zzfict=5)
opts = [o for k, conv in E.GENE_CONVERT if E.express(g5).get(k) for o in conv(g5)]
check('5 converter options', opts[-2:] == ['--zzfict', '5'], opts)

E.gene('zzctl', values=(0, 5, 7))                             # the control: no rule
control = 'zzctl' not in E.express(dict(plain, zzctl=5))
if control: fails.append('control: a row without a rule was dropped without the tag too - check 2 cannot tell')
print('gene-table-test: %s - %s; control %s' % ('FAIL' if fails else 'PASS', ', '.join('%s %d' % kv for kv in n.items()), 'caught' if not control else 'NOT caught'))
for f in fails[:10]: print('  ' + f)
sys.exit(1 if fails else 0)
