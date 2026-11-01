#!/bin/sh
# lab/evolve/restore-archives.sh [FROM] - the archived databases tools/clean-runs.sh removed, back from the seed packs,
# for "carryall" (Iteration 572). clean-runs.sh keeps the newest four archived-* - their databases travel in the seed
# packs, which it never removes - while carryall (562) reads every archived-*: seed 83's chain (carry-check.py --all)
# found seeds 79-83 only, none of carry-named.txt's five. For each seed pack forth-vm-evolution-seedN-*.tar.gz in RUNS
# or a chain's packs/, N at least FROM (default 71: the seven workloads with apps - results/drafts/confirmation-pool-559.md),
# whose seed no archived-*/build/evolve/next-run.state names: its pack/db.jsonl into RUNS/archived-<the pack's
# time>/build/evolve/, with a next-run.state naming the seed and the pack. A seed packed twice: the newest pack. Idempotent;
# clean-runs.sh prunes them again before a later run, the packs stay. next-run.sh runs it for carryall, before the carry;
# tools/test-restore-archives.sh tests it.
set -u
RUNS=${RUNS:-$(cd "$(dirname "$0")/../.." && pwd)/runs}; FROM=${1:-71}; n=0
cd "$RUNS" || exit 1
for p in $(ls forth-vm-evolution-seed[0-9]*-*.tar.gz chain-*/packs/forth-vm-evolution-seed[0-9]*-*.tar.gz 2>/dev/null \
        | sed -n 's/^\(.*-\([0-9]\{8\}-[0-9]\{6\}\)\.tar\.gz\)$/\2 \1/p' | sort -r | cut -d' ' -f2-); do
    s=$(basename "$p" | sed -n 's/^forth-vm-evolution-seed\([0-9]*\)-.*/\1/p')
    [ -n "$s" ] && [ "$s" -ge "$FROM" ] || continue
    grep -qs "^seed $s " archived-*/build/evolve/next-run.state && continue
    t=$(echo "$p" | sed 's/.*-\([0-9]\{8\}-[0-9]\{6\}\)\.tar\.gz$/\1/')
    [ ! -e "archived-$t" ] || { echo "restore-archives: seed $s - archived-$t there already, not its: $p left"; continue; }
    k=.restore-$t; rm -rf "$k"; mkdir -p "$k/build/evolve"
    if tar -xzOf "$p" pack/db.jsonl > "$k/build/evolve/db.jsonl" 2> /dev/null && [ -s "$k/build/evolve/db.jsonl" ]; then
        w=$(tar -xzOf "$p" pack/machine.txt 2> /dev/null | grep -m 1 '^seed ')   # 576: the run's WANT - next-run.sh's carry reads "random" in it
        echo "seed $s restored from $p${w:+ - $w}" > "$k/build/evolve/next-run.state"
        mv "$k" "archived-$t" && n=$((n + 1)) && echo "restore-archives: seed $s - archived-$t from $p"
    else rm -rf "$k"; echo "restore-archives: seed $s - no database in $p"; fi
done
echo "restore-archives: $n restored, seeds $FROM on"
