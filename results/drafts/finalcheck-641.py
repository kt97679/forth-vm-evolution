#!/usr/bin/env python3
"""results/drafts/finalcheck-641.py [HOURS] - the final check before the freeze (Iteration 641; the owner: "I want to be
absolutely sure we found best designs", 26 hours). Writes results/followup-seed91-final.md and prints the chain's lines.

Every JIT-free design on the pooled front never measured across machines, side by side with the holders and the best
measured before, on all three machines in one chain (the laptop free - no evolution run):
  - first, to pair: the six portable holders (followup-seed91.md's records) and c2ef9488ff;
  - found before, re-measured: every JIT-free design of followup-pick-seed87..91.json's sets, and each earlier follow-up
    chain's three fastest on the laptop alone at each width (9f8811f7f4, e523a45566, a2df4ef183 among them - 640's bridges);
  - the run (why "the check" - followup-roles.py's run() reads it as a candidate, 641): the pool's designs that no chain
    ever measured on a remote line (results/drafts/coverage-641.py: 72 - 66 carried into seeds 89-90 and screened by
    neither, 6 of seed 87's rest), then seed 91's rest (results/screen-seed91.md, 320).
Records as portable-followup.py keeps them. Sizes from seed 91's follow-up's rates: the laptop 38 s a design a session
(four readings, 10 rounds), dream 15 s a width (10 rounds), the Tegra 3 rounds at 631's 22 s a round and 5 s a design."""
import glob, json, math, os, statistics, sys

R = 'results'; OUT = R + '/followup-seed91-final.md'; H = float(sys.argv[1]) if len(sys.argv) > 1 else 26.0
KEEP = ('id', 'genome', 'speed', 'speed32', 'total', 'size', 'bin', 'rss', 'gen', 'status')
recs = lambda f: [json.loads(l) for l in open(f) if l.startswith('{')]
sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']; import evolve as E
jit = lambda r: bool(E.express(E.canon(r['genome'])).get('jit'))
G = {}                                                # id -> a record with its genome, newest list first
for f in [R + '/followup-seed91.md', R + '/screen-seed91.md'] + sorted(glob.glob(R + '/followup-seed8[7-9].md') + glob.glob(R + '/followup-seed90.md'), reverse=True) + [R + '/portable-front-seed90.md']:
    for r in recs(f): G.setdefault(r['id'], r)
rows, seen = [], set()


def add(i, why):
    if i in seen or i not in G or jit(G[i]): return
    rows.append(dict({k: G[i][k] for k in KEEP if k in G[i]}, why=why)); seen.add(i)


f91 = {r['id']: r for r in recs(R + '/followup-seed91.md')}
for i in ('782f3ad7ff', '3eb59b271d', '11a56ff9e4', 'ae99617f06', 'fb0d57c8a2', '64a7345393'):   # results/relf-designs-636.md
    add(i, 'found before - the relf handoff\'s role holder (636)')
add('c2ef9488ff', 'found before - the knee before 636')
nh = len(rows)
for n in (87, 88, 89, 90, 91):
    for r in recs('%s/followup-pick-seed%d.json' % (R, n)):
        if not r.get('jit'): add(r['id'], 'found before - followup-pick-seed%d (%s)' % (n, r.get('why', '')))
gm = lambda v: math.exp(statistics.fmean(math.log(t) for t in v))
for n in (87, 88, 89, 90, 91):                        # each chain's three fastest on the laptop alone, each width
    S = {}
    for f in glob.glob('%s/chain-followup%d/s[0-9]*/loadtest.md' % (R, n)):
        for l in open(f, errors='replace'):
            if l.startswith('{"'):
                x = json.loads(l)
                for k in ('idle', 'idle32'):
                    if x.get(k): S.setdefault(k, {}).setdefault(x['id'], []).append(x[k])
    for k, w in (('idle', '8-byte'), ('idle32', '4-byte')):
        for i in sorted((i for i in S.get(k, {}) if i in G and not jit(G[i])), key=lambda i: gm(S[k][i]))[:3]:
            add(i, 'found before - chain-followup%d\'s fastest on the laptop alone at %s cells' % (n, w))
nf = len(rows) - nh
cov = [l.split()[1] for l in open(R + '/drafts/coverage-641.txt') if l.startswith('- ')]
for i in cov: add(i, 'the check - on the pooled front, never measured across machines (641)')
n72 = len(rows) - nh - nf
for r in recs(R + '/screen-seed91.md'):
    if r['why'].startswith('the run'): add(r['id'], r['why'])
nr = len(rows) - nh - nf - n72
with open(OUT, 'w') as o:
    o.write('# The final check before the freeze (results/drafts/finalcheck-641.py, Iteration 641): every JIT-free design on the\n'
            '# pooled front never measured across machines (%d: results/drafts/coverage-641.txt) and seed 91\'s rest (%d:\n'
            '# results/screen-seed91.md), side by side with the %d holders and the %d best re-measured before, on all three machines.\n\n'
            % (n72, nr, nh, nf))
    for r in rows: o.write(json.dumps(r, sort_keys=True) + '\n')
m = len(rows); lap = m * 38; d = (m + 6) * 15 / 60.0; t = (m + 4) * (3 * 22 + 5) / 60.0
steps = max(1, int((H * 3600 - 900) // lap)) + 1
sd = max(1, int((H * 30 - 5) // d)); st = max(1, round((H * 60 - 5 - 16) / t))
print('%d designs -> %s: holders %d, found before %d, never measured %d, seed 91\'s rest %d' % (m, OUT, nh, nf, n72, nr))
print('a session: the laptop %.1f h, dream %.0f min a width, the Tegra %.0f min at 3 rounds; in %.0f hours: the laptop %d, '
      'dream %d a width, the Tegra %d (%.0f min of %d)' % (lap / 3600.0, d, t, H, steps - 1, sd, st, st * t + 16, H * 60 - 5))
print('NEXT-RUN:  ' + ' then '.join(['experiment loadtest.py --ids %s --rounds 10' % OUT] * steps))
print('REMOTES:   rage.lan     prebuiltarm 4       3       %d     --cell 4 --rejected 4 --sessions %d --also @%s' % (int(H * 60) - 5, st, OUT))
print('           dream.lan    prebuilt32  4       10      %d      --cell 4 --rejected 6 --sessions %d --also @%s' % (int(H * 30) - 5, sd, OUT))
print('           dream.lan    prebuilt64  4       10      %d      --from prebuilt32 --sessions %d' % (int(H * 30) - 5, sd))
