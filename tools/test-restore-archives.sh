#!/bin/sh
# test-restore-archives.sh - lab/evolve/restore-archives.sh on a made-up runs directory (Iteration 572). tools/run-tests.sh
# runs it. The rules checked: a seed with no archive comes back from its pack, top-level or in a chain's packs/, as
# archived-<the pack's time> holding the pack's db.jsonl; a seed already archived, a seed under FROM and a pack that is no
# seed pack stay out; a seed packed twice comes back once, from the newest; a pack without a database leaves nothing; a
# second run restores nothing. Exit 1 on any failure.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
R=$T/runs; mkdir -p "$R"; cd "$T" || exit 1
pack() {   # pack DIR NAME [CONTENT] - a seed pack holding pack/db.jsonl (none without CONTENT)
    rm -rf pack; mkdir pack; echo x > pack/next-run.log; [ -z "${3:-}" ] || echo "$3" > pack/db.jsonl
    mkdir -p "$R/$1"; tar -czf "$R/$1/$2" pack; rm -rf pack
}
mkdir -p "$R/archived-20261029-040143/build/evolve"; echo seed79 > "$R/archived-20261029-040143/build/evolve/db.jsonl"
echo "seed 79 noevolved nocarry at abc, pop 256" > "$R/archived-20261029-040143/build/evolve/next-run.state"
pack chain-A/packs forth-vm-evolution-seed78-aaa-fury-20261028-130255.tar.gz db78
pack chain-B/packs forth-vm-evolution-seed79-bbb-fury-20261029-023923.tar.gz db79
pack . forth-vm-evolution-seed77-ccc-fury-20261028-023821.tar.gz db77
pack chain-C/packs forth-vm-evolution-seed70-ddd-fury-20261024-154345.tar.gz db70
pack chain-D/packs forth-vm-evolution-seed76-eee-fury-20261026-120000.tar.gz db76old
pack chain-E/packs forth-vm-evolution-seed76-fff-fury-20261027-133126.tar.gz db76new
pack chain-F/packs forth-vm-evolution-seed75-ggg-fury-20261027-014140.tar.gz
pack . forth-vm-evolution-appbench-hhh-fury-20261031-002321.tar.gz db-appbench
F=0; no() { echo "FAIL: $*"; F=1; }
out=$(RUNS=$R sh "$HERE/../lab/evolve/restore-archives.sh")
has() { [ "$(cat "$R/archived-$1/build/evolve/db.jsonl" 2>/dev/null)" = "$2" ] || no "archived-$1 should hold $2"; }
has 20261028-130255 db78; has 20261028-023821 db77; has 20261027-133126 db76new; has 20261029-040143 seed79
grep -q '^seed 78 restored from chain-A/packs/' "$R/archived-20261028-130255/build/evolve/next-run.state" || no "seed 78's state"
for t in 20261029-023923 20261024-154345 20261026-120000 20261027-014140 20261031-002321; do
    [ ! -e "$R/archived-$t" ] || no "archived-$t should not be there"; done
[ "$(ls -d "$R"/archived-* | wc -l)" = 4 ] || no "four archives expected: $(ls "$R" | tr '\n' ' ')"
[ -z "$(ls -A "$R" | grep '^\.restore')" ] || no "a .restore- directory left behind"
echo "$out" | grep -q 'seed 75 - no database' || no "seed 75's empty pack not said"
echo "$out" | tail -1 | grep -q '^restore-archives: 3 restored, seeds 71 on$' || no "the count: $(echo "$out" | tail -1)"
out2=$(RUNS=$R sh "$HERE/../lab/evolve/restore-archives.sh" | tail -1)
[ "$out2" = "restore-archives: 0 restored, seeds 71 on" ] || no "a second run: $out2"
[ $F = 0 ] || exit 1
echo "PASS - 3 restored (77, 78, 76 from its newer pack), 79 archived, 70 under FROM, 75 empty, appbench no seed; again 0"
