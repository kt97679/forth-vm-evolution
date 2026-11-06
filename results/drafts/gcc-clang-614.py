#!/usr/bin/env python3
"""results/drafts/gcc-clang-614.py - the dream/laptop ratio of GCC and clang builds at both widths, the median over each
chain's designs (Iteration 614): seed 87's follow-up (results/chain-followup87, its 45) and seed 88's chain
(results/chain-seed88, the experiment's 20) - each speed the geometric mean of its sessions, read by
results/drafts/dream32-experiment-613.py's read(). Run from the repository's root."""
import importlib.util, json, math, statistics as st, sys
s = importlib.util.spec_from_file_location('x', 'results/drafts/dream32-experiment-613.py'); X = importlib.util.module_from_spec(s); s.loader.exec_module(X)
def ratios(d, cand):
    C = [json.loads(l) for l in open(cand) if l.startswith('{')]
    ids = [c['id'] for c in C]; G = {c['id']: c['genome'] for c in C}
    S, kind = X.read(d, ids)
    if isinstance(S.get('laptop32', {}).get(ids[0]), dict):
        S = {k: {i: [v for v in d2.values()] for i, d2 in v.items()} for k, v in S.items()}
    g = lambda src, i: X.gm([t for t in S[src][i] if t]) if any(S[src][i]) else None
    out = []
    for i in ids:
        a, b, c, e = g('dream.lan-prebuilt32', i), g('laptop32', i), g('dream.lan-prebuilt64', i), g('laptop64', i)
        if a and b: out.append((i, G[i].get('compiler'), a / b, c / e if c and e else None))
    return out
for name, d, cand in (('follow-up 87', 'results/chain-followup87', 'results/followup-seed87.md'), ('seed 88 chain', 'results/chain-seed88', 'results/candidates-dream32-612.md')):
    R = ratios(d, cand)
    for comp, lab in ((0, 'GCC'), (1, 'clang')):
        v = [r[2] for r in R if r[1] == comp]; w = [r[3] for r in R if r[1] == comp and r[3]]
        if v: print('%s %s: %d designs, dream/laptop at 4 bytes %.2f-%.2f (median %.2f); at 8 bytes median %.2f' % (name, lab, len(v), min(v), max(v), st.median(v), st.median(w)))
