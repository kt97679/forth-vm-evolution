#!/bin/sh
# test-clean-runs.sh - tools/clean-runs.sh on a made-up runs directory (Iteration 541). tools/run-tests.sh runs it.
# The rules checked: the copies sent to the remotes (repo.bundle, bins.tar.gz) go from finished chains only, never
# from a running one; chain tarballs past the newest KEEP_CHAINS go; other packs past the newest KEEP_PACKS go; a run
# directory goes once its pack is here or in a chain's packs/; archived-* past the newest KEEP go - and no seed pack is
# ever removed, nor a directory holding one, wherever the rules would have listed it. The dry run removes nothing.
# Exit 1 on any failure.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
R=$T/runs; mkdir -p "$R"; cd "$R"
f() { mkdir -p "$(dirname "$1")"; head -c "${2:-1000}" /dev/zero > "$1"; }
for c in A:done B:running C:stopped; do
    n=chain-2026102${c%%:*}; mkdir -p "$n/remote/h1" "$n/packs"; echo "${c#*:}" > "$n/status"
    f "$n/remote/repo.bundle" 9000; f "$n/remote/h1/bins.tar.gz" 3000; f "$n/remote/h1/out.json" 100
done
f chain-2026102A/packs/forth-vm-evolution-seed60-abc1234-host-20261020-010101.tar.gz 5000
f chain-2026102B/packs/forth-vm-evolution-seed61-bcd2345-host-20261021-010101.tar.gz 5000
for d in 21 22 23 24; do f forth-vm-evolution-chain-abc$d-host-202610$d-010101.tar.gz 7000; done
f forth-vm-evolution-chain-dead-host-20261019-010101-failed.tar.gz 50
for d in 10 11 12 13 14 15 16 17 18 19; do
    f forth-vm-evolution-seed$d-0123abc-host-202610$d-020202.tar.gz 4000
    f forth-vm-evolution-footprint-0123abc-host-202610$d-030303.tar.gz 400
done
for a in 1 2 3 4 5 6; do mkdir archived-2026102$a; f archived-2026102$a/db.jsonl 2000; done
f archived-20261021/forth-vm-evolution-seed09-0123abc-host-20261009-020202.tar.gz 10   # a seed pack where none belongs
mkdir seed60-abc1234 footprint-def5678; f seed60-abc1234/build.log 10; f footprint-def5678/build.log 10
mkdir seed61-bcd2345; f seed61-bcd2345/tests.log 10        # Iteration 549: its pack in a running chain's packs/
FAIL=0
ok() { if eval "$2"; then echo "ok    $1"; else echo "FAIL  $1"; FAIL=1; fi; }
gone() { [ ! -e "$1" ]; }
here() { [ -e "$1" ]; }
before=$(find . ! -name .lock | sort | md5sum)    # the lock is made by every call
out=$(RUNS=$R sh "$HERE/clean-runs.sh" --dry-run 2>&1)
ok "the dry run removes nothing" '[ "$(find . ! -name .lock | sort | md5sum)" = "$before" ]'
ok "the dry run gives each size and the total" 'printf "%s" "$out" | grep -q "KB in all" && printf "%s" "$out" | grep -q "KB  chain-2026102A/remote/repo.bundle"'
err=$(RUNS=$R sh "$HERE/clean-runs.sh" 2>&1 >/dev/null)
ok "a finished chain loses its repo.bundle and bins.tar.gz" 'gone chain-2026102A/remote/repo.bundle && gone chain-2026102A/remote/h1/bins.tar.gz'
ok "a stopped chain loses its repo.bundle" 'gone chain-2026102C/remote/repo.bundle'
ok "a finished chain keeps its results" 'here chain-2026102A/remote/h1/out.json && here chain-2026102A/status'
ok "a running chain's first step keeps its directory (549)" 'here seed61-bcd2345/tests.log'
ok "a running chain keeps everything" 'here chain-2026102B/remote/repo.bundle && here chain-2026102B/remote/h1/bins.tar.gz'
ok "chain tarballs: the newest 2 kept" 'gone forth-vm-evolution-chain-abc21-host-20261021-010101.tar.gz && gone forth-vm-evolution-chain-abc22-host-20261022-010101.tar.gz && here forth-vm-evolution-chain-abc23-host-20261023-010101.tar.gz && here forth-vm-evolution-chain-abc24-host-20261024-010101.tar.gz'
ok "every seed pack kept - ten at the top, two in chains" '[ $(ls forth-vm-evolution-seed*.tar.gz | wc -l) = 10 ] && [ $(ls chain-*/packs/forth-vm-evolution-seed*.tar.gz | wc -l) = 2 ]'
ok "other packs: the newest 8 kept" '[ $(ls forth-vm-evolution-footprint-*.tar.gz | wc -l) = 8 ] && gone forth-vm-evolution-footprint-0123abc-host-20261010-030303.tar.gz'
ok "a run directory whose pack is in a chain goes; one without a pack stays" 'gone seed60-abc1234 && here footprint-def5678'
ok "archives past the newest 4 go - but not one holding a seed pack, reported as a bug" 'gone archived-20261022 && here archived-20261021 && here archived-20261023 && printf "%s" "$err" | grep -q "BUG - archived-20261021 holds a seed pack"'
ok "a failed chain tarball (no time at the end of its name) stays" 'here forth-vm-evolution-chain-dead-host-20261019-010101-failed.tar.gz'
[ $FAIL = 0 ] && echo "test-clean-runs: 13 checks, all pass" || echo "test-clean-runs: FAIL"
exit $FAIL
