#!/bin/sh
# tools/relf-ab.sh [-r ROUNDS] [-s SCALE] [-w "WORKLOADS"] [PATCH ...] - a candidate for relf, measured on
# relf's own terms (Iteration 357; RELF.md). A: vendor/relf/tree as vendored; B: the same with the
# PATCHes applied (patch -p1, against the tree). A patch touching engine/opcodes.tab, forth/kernel.4 or
# forth/cross.4 rebuilds B's kernel images first (relf's make does not: make images IMAGES_FORCE=1).
# B must pass relf's `make test` and a shell's `echo ok` before it is measured. Then relf's
# tools/bench-vm.py - paired, interleaved CPU time, medians with bootstrap intervals - on its shell
# workloads (default loop fn str arith realistic start), A first: each ratio is B's time over A's.
# No PATCH: B is A again - the noise floor.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
ROUNDS=20; SCALE=2; WL="loop fn str arith realistic start"
while [ $# -gt 0 ]; do case $1 in -r) ROUNDS=$2; shift 2 ;; -s) SCALE=$2; shift 2 ;; -w) WL=$2; shift 2 ;; *) break ;; esac; done
T=${RELF_AB_DIR:-$(mktemp -d /tmp/relf-ab.XXXXXX)}
mkdir -p "$T"; rm -rf "$T/A" "$T/B"; cp -r "$ROOT/vendor/relf/tree" "$T/A"; cp -r "$ROOT/vendor/relf/tree" "$T/B"
images=
for p in "$@"; do
    p=$(cd "$(dirname "$p")" && pwd)/$(basename "$p")
    (cd "$T/B" && patch -s -p1 < "$p") || { echo "relf-ab: $p does not apply to vendor/relf/tree"; exit 1; }
    grep -q '^+++ .*\(engine/opcodes.tab\|forth/kernel.4\|forth/cross.4\)' "$p" && images=1
done
echo "relf-ab: A vendor/relf/tree ($(sed -n 's/^commit  \(.......\).*/\1/p' "$ROOT/vendor/relf/UPSTREAM")); B with ${*:-nothing - the noise floor}"
(cd "$T/A" && make -s relfsh64 > "$T/A.make" 2>&1) || { echo "relf-ab: A does not build"; tail -5 "$T/A.make"; exit 1; }
if [ -n "$images" ]; then (cd "$T/B" && make -s images IMAGES_FORCE=1 > "$T/B.images" 2>&1) || { echo "relf-ab: B's images do not build"; tail -5 "$T/B.images"; exit 1; }; fi
(cd "$T/B" && make -s relfsh64 > "$T/B.make" 2>&1) || { echo "relf-ab: B does not build"; tail -5 "$T/B.make"; exit 1; }
# The gate is regression, not perfection: B may fail only what A fails (relf's suite has network and
# terminal tests a host may not allow). A's failures recorded once for the vendored commit.
AF=$ROOT/build/relf-ab-$(sed -n 's/^commit  \(.......\).*/\1/p' "$ROOT/vendor/relf/UPSTREAM").fails
if [ ! -f "$AF" ]; then
    (cd "$T/A" && make -s test > "$T/A.test" 2>&1) || true
    grep '^FAIL' "$T/A.test" | sort -u > "$AF"
    echo "relf-ab: A's own make test here: $(wc -l < "$AF") failing check(s), recorded in $AF"
fi
(cd "$T/B" && make -s test > "$T/B.test" 2>&1) || true
grep '^FAIL' "$T/B.test" | sort -u > "$T/B.fails"
NEW=$(comm -13 "$AF" "$T/B.fails")
[ -z "$NEW" ] || { echo "relf-ab: B fails what A passes:"; echo "$NEW" | head -10; exit 1; }
[ "$(cd "$T/B" && ./relfsh64 -c 'echo ok')" = ok ] || { echo "relf-ab: B's shell fails echo ok"; exit 1; }
echo "relf-ab: B fails nothing A passes ($(wc -l < "$T/B.fails") as A) and the shell echoes; $ROUNDS rounds at SCALE=$SCALE: $WL"
printf 'relf|%s|./relfsh64 {w}\ncandidate|%s|./relfsh64 {w}\n' "$T/A" "$T/B" > "$T/cfg"
cd "$T/A" && WL="$WL" SCALE="$SCALE" python3 tools/bench-vm.py "$ROUNDS" "$T/cfg"
