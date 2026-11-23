#!/bin/sh
# results/drafts/roles-screen-741.sh [OUT] - results/drafts/roles-screen-741.py tested (Iteration 741). Seed 96's database
# (705's pool) is not in the repository, so the test is equivalence on what is: seeds 92-95's results files and seed 96's
# standing in for the database, results/roles-holders-705.md the holders -
#   1. 705's script (new-roles-705.py) and the general one with 705's arguments: stdout and every record line of both
#      lists the same, byte for byte (the headers' prose differs, by design);
#   2. the general one as the endgame runs it - the holders from designs/ and results/relf-designs-718.md, the guard
#      challengers --also, the thumb variants --also-arm (742): all ten holders in both lists (a holder is on the Tegra's
#      list as on 705's), the three challengers on the laptop's and dream's list, not the Tegra's (JIT designs), the six
#      thumb variants on the Tegra's alone.
# PASS or FAIL. As the build user, from the repository's top; a few minutes.
set -u
O=${1:-/tmp/roles-screen-741}; rm -rf "$O"; mkdir -p "$O"
T=results/candidates-thumb-742.md; [ -f $T ] || T=results/queued-thumb/candidates-thumb-742.md   # 742: the thumb variants, --also-arm
S=results/evolve-amd-ryzen-7-pro-8840hs-seed
F="${S}92.md ${S}93.md ${S}94.md ${S}95.md"; DB=${S}96.md
python3 -B results/drafts/new-roles-705.py "$O/old.md" "$O/old-arm.md" results/roles-holders-705.md $DB $F > "$O/old.out" 2>&1 || { echo "roles-screen: FAIL - 705's script"; exit 1; }
python3 -B results/drafts/roles-screen-741.py "$O/new.md" "$O/new-arm.md" $DB $F --holders results/roles-holders-705.md \
    --db-label seed96-db.jsonl --holders-src holders-705.py --iter 705 --series 'seeds 92-96' > "$O/new.out" 2>&1 || { echo "roles-screen: FAIL - the general one"; exit 1; }
f=
cmp -s "$O/old.out" "$O/new.out" || f="$f stdout"
for x in "" -arm; do
    grep '^{' "$O/old$x.md" > "$O/old$x.recs"; grep '^{' "$O/new$x.md" > "$O/new$x.recs"
    cmp -s "$O/old$x.recs" "$O/new$x.recs" || f="$f list$x"
done
python3 -B results/drafts/roles-screen-741.py "$O/end.md" "$O/end-arm.md" $DB $F --designs designs --records results/relf-designs-718.md \
    --also results/candidates-guard-740.md --also-arm "$T" --iter 741 --series 'seeds 92-96 (the stand-in)' > "$O/end.out" 2>&1 || f="$f endgame-mode"
python3 - "$O/end.md" "$O/end-arm.md" > "$O/end.check" <<'PY' || f="$f endgame-lists"
import json, os, sys
L = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[1]) if l.startswith('{')}
M = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[2]) if l.startswith('{')}
H = {json.load(open(os.path.join('designs', n, 'record.json')))['id'] for n in os.listdir('designs') if os.path.exists(os.path.join('designs', n, 'record.json'))}
G = {json.loads(l)['id'] for l in open('results/candidates-guard-740.md') if l.startswith('{')}
TF = 'results/candidates-thumb-742.md' if os.path.exists('results/candidates-thumb-742.md') else 'results/queued-thumb/candidates-thumb-742.md'
TV = {json.loads(l)['id'] for l in open(TF) if l.startswith('{')}
bad = [('holder not listed', i) for i in H if i not in L or i not in M] + [('challenger', i) for i in G if i not in L or i in M]
bad += [('holder why', i) for i in H if i in L and 'a holder: ' not in L[i]['why']]
bad += [('thumb variant', i) for i in TV if i in L or i not in M]
print('list %d, ARM list %d; holders %d of %d on both; challengers %d of %d on the list, %d on the ARM list; thumb variants %d of %d on the ARM list, %d on the list' % (
    len(L), len(M), sum(i in L and i in M for i in H), len(H), sum(i in L for i in G), len(G), sum(i in M for i in G), sum(i in M for i in TV), len(TV), sum(i in L for i in TV)))
for b in bad: print('BAD', *b)
sys.exit(1 if bad else 0)
PY
cat "$O/end.check"
echo "roles-screen: ${f:+FAIL -$f}${f:-PASS}"
