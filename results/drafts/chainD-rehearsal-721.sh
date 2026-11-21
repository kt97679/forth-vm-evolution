#!/bin/sh
# results/drafts/chainD-rehearsal-721.sh [CHAIN_C_TGZ] - chain D's processing rehearsed before its archive comes (Iteration
# 721, while chain D runs): a stand-in archive made from chain C's - its Tegra line taken out (chain D has none) and its
# pool-sizes pack given a --write list (717): the static list's 28 and three of the pack's own finds, never measured -
# then process-followup.sh 96-jitband in a scratch clone (/tmp/chainD-rehearsal) with the tree's tools as they are. The
# checks: written-list.py appended the three to the list; the processing DONE; the smallest JIT design's line in the
# summary, 15eda54ebd the holder. PASS or FAIL. As the build user, from the repository's top.
set -u
B=${1:-$(ls -t /mnt/user-data/uploads/*forth-vm-evolution-chain-71fc8dd42-*[_.]tar.gz 2>/dev/null | head -n 1)}
[ -f "$B" ] || { echo "chainD-rehearsal: no chain C archive"; exit 1; }
R=/tmp/chainD-rehearsal; rm -rf "$R"; mkdir -p "$R/work" "$R/x"
git clone -q . "$R/tree" && ln -s "$PWD/build" "$R/tree/build" || exit 1
cp lab/evolve/process-followup.sh lab/evolve/written-list.py lab/evolve/followup-roles.py "$R/tree/lab/evolve/"   # as they are
cp results/followup-seed96-jitband.md "$R/tree/results/"
tar xzf "$B" -C "$R/work" || exit 1; H=$(ls -d "$R"/work/chain-*); rm -rf "$H/remote/rage.lan-prebuiltarm"
P=$(ls "$H"/packs/*-pool-sizes-*.tar.gz); tar xzf "$P" -C "$R/x" || exit 1
IDS=$(grep '^{"' results/followup-seed96-jitband.md | python3 -c 'import json,sys; print(",".join(json.loads(l)["id"] for l in sys.stdin))')
NEW=$(grep '^{"' "$R/x/pack/pool-sizes.md" | head -n 3 | python3 -c 'import json,sys; print(",".join(json.loads(l)["id"] for l in sys.stdin))')
printf '\nwritten build/evolve/jitband-list.md: 28 anchors, 3 found\nwritten ids: %s,%s\n' "$IDS" "$NEW" >> "$R/x/pack/pool-sizes.md"
(cd "$R/x" && tar czf "$P" pack) || exit 1
# chain D's measure-ids reads the written list - so the stand-in's pack (chain C's 66) keeps only the written ids
M=$(ls "$H"/packs/*-measure-ids-*.tar.gz); mkdir -p "$R/m" && tar xzf "$M" -C "$R/m" || exit 1
python3 - "$R/m/pack/measure-ids.md" "$IDS,$NEW" <<'PY'
import json, sys
f, keep = sys.argv[1], set(sys.argv[2].split(','))
L = [l for l in open(f) if not l.startswith('{"') or json.loads(l).get('id') in keep]
open(f, 'w').writelines(L)
PY
(cd "$R/m" && tar czf "$M" pack) || exit 1
(cd "$R/work" && tar czf "$R/forth-vm-evolution-chain-rehearseD_tar.gz" "$(basename "$H")") || exit 1
(cd "$R/tree" && OUT=$R/out HANDOFF=results/handoff-relf-657.md PRED=717 sh lab/evolve/process-followup.sh 96-jitband 721 smalljit=15eda54ebd \
    "$R/forth-vm-evolution-chain-rehearseD_tar.gz") > "$R/process.log" 2>&1
rc=$?; f=
[ $rc = 0 ] && grep -q 'process-followup: DONE' "$R/process.log" || f="$f processing (exit $rc: $(tail -n 1 "$R/process.log" | cut -c1-100))"
grep -q 'written-list.py: 3 appended' "$R/out/summary.md" 2>/dev/null || f="$f written-list"
for i in $(echo "$NEW" | tr ',' ' '); do grep -q "\"id\": \"$i\"" "$R/tree/results/followup-seed96-jitband.md" || f="$f record-$i"; done
grep -q 'the smallest JIT design - 15eda54ebd' "$R/out/summary.md" 2>/dev/null || f="$f smalljit-line"
echo "chainD-rehearsal: ${f:+FAIL -$f}${f:-PASS}"
