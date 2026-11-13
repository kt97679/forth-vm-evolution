#!/usr/bin/env python3
"""results/drafts/freeze-ids-656.py [--compare BEFORE.jsonl AFTER.jsonl] - the freeze's byte check (Iteration 656): 641's
test of results/queued-freeze's batch (results/drafts/freeze-retire-641.md) again, on master at the freeze, with 649's
smallest (d180351903) among the winners.
Without arguments, run on the tree BEFORE the batch (it reads evolve.py's -loop and rtimm_lean tests, which the batch
removes): one comma-separated id list on stdout for results/drafts/build-hash-641.py --only, the counts on stderr - every
winner (the final set, results/final-set-chainsBCD-seed86.md; the relf handoff's roles at 636 and at 649,
results/relf-designs-636.md and -649.md) and, drawn with random.Random(656) from the pooled true front of seeds 77-91
(freeze-audit-641.py's pool) among the designs build-hash-641.py reads, 30 whose build loads -loopall (the overlay the
rtloop patch keeps beside the path it retires), 10 loading -fuse-imm without it (rtimm, the rtimmlean patch's gene) and 10
with neither. A design using what the batch retires (-loop, rtimm_lean) is not drawn; a winner using it is named (641: none).
--compare: build-hash-641.py's two outputs at one width - PASS when every id has the same engine and image bytes before
and after, or died in both; exit 1 otherwise."""
import importlib.util, json, random, re, sys

if sys.argv[1:2] == ['--compare']:
    rd = lambda f: {r['id']: r for r in (json.loads(l) for l in open(f) if l.strip())}
    b, a = rd(sys.argv[2]), rd(sys.argv[3])
    key = lambda r: 'died' if 'died' in r else (r['engine'], r['image'])
    same = [i for i in b if i in a and 'died' not in b[i] and key(b[i]) == key(a[i])]
    died = [i for i in b if i in a and 'died' in b[i] and 'died' in a[i]]
    bad = sorted((set(b) | set(a)) - set(same) - set(died))
    cell = next(iter(b.values()))['cell'] if b else '?'
    print('cell %s: %d of %d the same engine and image bytes, %d died in both - %s' % (
        cell, len(same), len(set(b) | set(a)), len(died), 'PASS' if not bad and b else 'FAIL: ' + ', '.join(bad[:20])))
    sys.exit(0 if not bad and b else 1)

sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']
import evolve as E, hv, stopping
_s = importlib.util.spec_from_file_location('confirm', 'lab/evolve/confirm.py')
CF = importlib.util.module_from_spec(_s); _s.loader.exec_module(CF)
method, runs = stopping.series(stopping.LEDGER)
recs = lambda f: [json.loads(l) for l in open(f) if l.startswith('{')]

# What build-hash-641.py can reach with --only (its own lines: the series' pool before seed 87 and the confirmations, its
# true front; the final pick's candidates; the stages; the portable runs' pools; the final check's list and two records)
P = {}
for f in CF.pool_files([r for r in runs if r['seed'] < 87] + CF.confirmations(stopping.LEDGER, 87)): P.update(hv.load(f, E))
G = set(hv.true_front(P, E)) | {r['id'] for r in recs('results/candidates-final-seed86.md')} | set(E.HUMAN)
for f in CF.pool_files(CF.portables(stopping.LEDGER, 92)):
    G |= {i for i, r in hv.load(f, E).items() if r.get('genome')}
for f in ('results/followup-seed91-final.md', 'results/relf-designs-636.md', 'results/final-set-chainsBCD-seed86.md'):
    G |= {r['id'] for r in recs(f)}

# The pooled true front of seeds 77-91, as freeze-audit-641.py reads it
A = {}
for f in CF.pool_files([r for r in runs if r['seed'] < 92] + CF.confirmations(stopping.LEDGER, 92)
                       + CF.portables(stopping.LEDGER, 92)): A.update(hv.load(f, E))
T = hv.true_front(A, E)

def fuse(g):                                         # freeze-audit-641.py's reading of evolve.py _build's overlay
    f = ('-fuse-imm' if g.get('rtimm') and 'imm' in g['spec'] else '-fuse') if E.overlay(g) else ''
    if E.rtimm_lean(g): f = '-lit'
    f += '-loopall' if E.rtloopall_on(g) else '-loop' if E.rtloop_on(g) else ''
    f += '-iplus' if E.rtiplus_on(g) else ''
    f += '-empty' if g.get('tag2') and g.get('rtempty') else ''
    return f or '(none)'
retired = lambda g: E.rtimm_lean(g) or re.search(r'-loop(?!all)', fuse(g)) is not None

W = {}
for f in ('results/final-set-chainsBCD-seed86.md', 'results/relf-designs-636.md', 'results/relf-designs-649.md'):
    for r in recs(f):
        if r.get('genome'): W.setdefault(r['id'], r)
wr = sorted(i for i, r in W.items() if retired(E.canon(r['genome'])))
wm = sorted(i for i in W if i not in G)

cand = sorted(i for i in T if i in G and i not in W and A[i].get('genome'))
fz = {i: fuse(E.canon(A[i]['genome'])) for i in cand}
ok = [i for i in cand if not retired(E.canon(A[i]['genome']))]
la = [i for i in ok if '-loopall' in fz[i]]
im = [i for i in ok if '-fuse-imm' in fz[i] and '-loopall' not in fz[i]]
ne = [i for i in ok if '-fuse-imm' not in fz[i] and '-loopall' not in fz[i]]
rng = random.Random(656)
picks = rng.sample(la, min(30, len(la))) + rng.sample(im, min(10, len(im))) + rng.sample(ne, min(10, len(ne)))
print(','.join(sorted(W) + picks))
sys.stderr.write('winners %d (using a retired path: %s; not reachable by build-hash: %s); the pooled true front %d, '
                 'reachable and not a winner %d, %d of them using a retired path; drawn %d -loopall of %d, %d -fuse-imm '
                 'of %d, %d neither of %d\n' % (len(W), ', '.join(wr) or 'none', ', '.join(wm) or 'none', len(T),
                 len(cand), len(cand) - len(ok), min(30, len(la)), len(la), min(10, len(im)), len(im),
                 min(10, len(ne)), len(ne)))
