#!/usr/bin/env python3
"""results/drafts/freeze-audit-641.py - the freeze's code paths beyond the gene values (Iteration 641). The retire report
(retire-report-579.py, 639) counts gene values; a code path chosen by several genes at once is not a value. The run-time
overlay a design's build loads (evolve.py _build's fuse: -fuse/-fuse-imm/-lit, -loop/-loopall, -iplus, -empty) counted
over the pooled true front (retire-report-579.py's pool, seeds 77-91), every alive recorded design, the hand-made stages,
and the final check's list with the winners (results/followup-seed91-final.md, results/relf-designs-636.md,
results/final-set-chainsBCD-seed86.md); rtimm_lean (forth/cv8-imm.4 alone) likewise. Run in the main tree."""
import collections, importlib.util, json, sys
sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']; import evolve as E, hv, stopping
_s = importlib.util.spec_from_file_location('confirm', 'lab/evolve/confirm.py'); CF = importlib.util.module_from_spec(_s); _s.loader.exec_module(CF)
method, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < 92]
P = {}
for f in CF.pool_files(runs + CF.confirmations(stopping.LEDGER, 92) + CF.portables(stopping.LEDGER, 92)): P.update(hv.load(f, E))
T = hv.true_front(P, E); alive = [i for i, r in P.items() if r.get('status') == 'ok' and r.get('genome')]
recs = lambda f: [json.loads(l) for l in open(f) if l.startswith('{')]
W = {r['id']: r for f in ('results/followup-seed91-final.md', 'results/relf-designs-636.md', 'results/final-set-chainsBCD-seed86.md') for r in recs(f) if r.get('genome')}
def fuse(g):                                         # evolve.py _build's lines, as at 640
    f = ('-fuse-imm' if g.get('rtimm') and 'imm' in g['spec'] else '-fuse') if E.overlay(g) else ''
    if E.rtimm_lean(g): f = '-lit'
    f += '-loopall' if E.rtloopall_on(g) else '-loop' if E.rtloop_on(g) else ''
    f += '-iplus' if E.rtiplus_on(g) else ''
    f += '-empty' if g.get('tag2') and g.get('rtempty') else ''
    return f or '(none)'
cg = lambda r: E.canon(r['genome'])
cf = collections.Counter(fuse(cg(P[i])) for i in T); ca = collections.Counter(fuse(cg(P[i])) for i in alive)
cw = collections.Counter(fuse(cg(r)) for r in W.values())
print('the pooled true front %d, alive %d, the final check\'s list and the winners %d' % (len(T), len(alive), len(W)))
print('| overlay | front | alive | list + winners |'); print('|---|---|---|---|')
for k in sorted(set(cf) | set(ca) | set(cw)): print('| %s | %d | %d | %d |' % (k, cf.get(k, 0), ca.get(k, 0), cw.get(k, 0)))
print('the hand-made stages: %s' % ', '.join('%s %s' % (n, fuse(E.canon(dict(g)))) for n, g in sorted(E.HUMAN.items()) if g.get('enc') == 'cv8'))
print('-loop users in the list and the winners: %s' % ', '.join(i for i, r in W.items() if fuse(cg(r)).endswith(('-loop', '-loop-empty'))))
print('rtimm_lean (forth/cv8-imm.4 alone): front %d, alive %d, list + winners %d' % (sum(1 for i in T if E.rtimm_lean(cg(P[i]))),
      sum(1 for i in alive if E.rtimm_lean(cg(P[i]))), sum(1 for r in W.values() if E.rtimm_lean(cg(r)))))
