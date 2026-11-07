#!/usr/bin/env python3
"""results/drafts/retire-report-579.py [N] - consolidation's retirement, read before it starts (Iteration 579; the rule
the owner set at 578: a gene value or code path is retired only when no design on the pooled true front uses it).

The pool: confirm.py's - the series' results files (stopping-series.md's newest method, seeds before N, default 87) and
every confirmation run's - their designs' union, its true front (hv.true_front: both widths). For each gene with values
(evolve.py's GENE_VALUES) and each value: how many designs on the pooled true front express it (evolve.express - a
dormant gene's value counts for none), and how many of all the pool's alive designs. A value no front design expresses is
a retire candidate under 578's rule; a value fewer than 5 front designs express is named as thin - kept, but the
re-measures decide whether those designs stay. Nothing is changed; the report is markdown on stdout. Iteration 623 (the freeze's preview): the portable runs' fronts in the
pool too (confirm.py's portables - none before seed 88, so N 87's report as it was); --winners: each candidate's users among
the final set's 21 and the relf handoff's ten, whose bytes the freeze keeps (599) - such a value stays. The code a retired
value would remove: results/drafts/retire-candidates-573.md for the nine re-enabled genes - not recomputed here."""
import collections, importlib.util, json, os, sys

HERE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lab', 'evolve')
sys.path.insert(0, HERE)
WIN = '--winners' in sys.argv; sys.argv = [x for x in sys.argv if x != '--winners']
N = int(sys.argv[1]) if len(sys.argv) > 1 else 87
sys.argv = ['x']; import evolve as E
import hv, stopping
_s = importlib.util.spec_from_file_location('confirm', os.path.join(HERE, 'confirm.py')); CF = importlib.util.module_from_spec(_s); _s.loader.exec_module(CF)

method, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < N]
pool = CF.pool_files(runs + CF.confirmations(stopping.LEDGER, N) + CF.portables(stopping.LEDGER, N))
P = {}
for f in pool: P.update(hv.load(f, E))
T = hv.true_front(P, E)
alive = [i for i, r in P.items() if r.get('status') == 'ok' and r.get('genome')]
def expressed(genome):
    """express() with a gene's 0 put back where the gene is live: express() drops a late gene at 0 (LATE) and compiler
    at 0, the same as a dormant one - live here when setting it on would express it."""
    g = E.canon(genome); e = E.express(g)
    for k in E.EXPRESSED[g['enc']]:
        if k in e or isinstance(g.get(k), (list, dict)): continue
        on = next((v for v in E.GENE_VALUES[k][0] if v), None) if k in E.GENE_VALUES else 1
        if on is not None and k in E.express(dict(g, **{k: on})): e[k] = 0
    return e
ex = {i: expressed(P[i]['genome']) for i in set(alive) | set(T)}
print('# Consolidation\'s retirement, read before it starts - the rule of 578 (retire-report-579.py)\n')
print('The pool: %d results files (%s); %d alive designs recorded in them (each run\'s front and its named designs, not its whole population), %d on its true front. A value is counted where a design '
      'expresses it (a dormant gene counts for none).\n' % (len(pool), ', '.join(os.path.basename(f).split('-')[-1].replace('.md', '') for f in pool),
      len(alive), len(T)))
print('| gene | value | front designs | in the results files | verdict |'); print('|---|---|---|---|---|')
cand, thin = [], []
for g in sorted(set().union(*E.EXPRESSED.values()) | set(E.GENE_VALUES)):
    if g in getattr(E, 'FROZEN', {}): continue
    seen = [ex[i][g] for i in alive if g in ex[i]] + [ex[i][g] for i in T if g in ex[i]]
    if any(isinstance(v, (list, dict)) for v in seen): continue          # word lists (supers, ops10, folds): no code path
    if g in E.GENE_VALUES: vals = E.GENE_VALUES[g][0]
    elif all(v in (0, 1) for v in seen): vals = (0, 1)                    # a switch (bytehdr, varcall, msc, ...)
    else: vals = tuple(sorted(set(seen), key=str))                       # the values the pool shows (opt, ...)
    cf = collections.Counter(ex[i].get(g) for i in T); ca = collections.Counter(ex[i].get(g) for i in alive)
    if not any(cf.get(v) for v in vals) and not any(ca.get(v) for v in vals): continue   # never expressed - a dormant gene everywhere
    for v in vals:
        nf, na = cf.get(v, 0), ca.get(v, 0)
        live = sum(cf.get(u, 0) for u in vals)
        verdict = 'RETIRE CANDIDATE - no front design (the gene live on %d)' % live if nf == 0 else 'thin - kept' if nf < 5 else 'kept'
        if nf == 0: cand.append((g, v, na))
        elif nf < 5: thin.append((g, v, nf))
        print('| %s | %s | %d | %d | %s |' % (g, v, nf, na, verdict))
print('\n**Retire candidates under 578** (%d values): %s.' % (len(cand), '; '.join('%s=%s (%d recorded designs off the front)' % c for c in cand) or 'none'))
if WIN:
    root = os.path.dirname(os.path.dirname(HERE))
    W = {}
    for f in ('results/final-set-chainsBCD-seed86.md', 'results/relf-designs-611.md'):
        W.update({r['id']: r for r in (json.loads(l) for l in open(os.path.join(root, f)) if l.startswith('{')) if r.get('genome')})
    xw = {i: expressed(W[i]['genome']) for i in W}
    print('\n**The winners** (%d: the final set\'s 21 and the relf handoff\'s ten, results/final-set-chainsBCD-seed86.md and '
          'results/relf-designs-611.md) - each candidate\'s users among them, whose bytes the freeze keeps (599):' % len(W))
    for g, v, na in cand:
        u = sorted(i for i in W if xw[i].get(g) == v)
        print('- %s=%s: %s' % (g, v, ('%d - %s: stays' % (len(u), ' '.join(u))) if u else 'none - retirable'))
print('**Thin** (fewer than 5 front designs - their designs\' re-measures decide): %s.' % ('; '.join('%s=%s (%d)' % t for t in thin) or 'none'))
print('\nWhat a candidate means: a late gene\'s 0 unused (jit=0, jitos=0, jitinl=0 where they are live) fixes the gene on '
      'and removes no code - the search space only; another value unused removes that value\'s code (alignhot=1, fsys 1, 4 '
      'and 5, jitdoes=1, msc=1); the older genes\' values (bytehdr, varcall, doesfar, scale, lean) build the hand-made '
      'stages s2-s5 - results/drafts/retire-candidates-573.md: kept while the stages are built. Against 573 (seeds 77-83, '
      'the nine): thinhdr and bss are off that list now - a design on the pooled front uses each - and sharedcall is '
      'dormant wherever varcall is on.')
print('Retired genes (FROZEN: %s) are not listed - their code is gone already.' % ', '.join(sorted(getattr(E, 'FROZEN', {}))))
