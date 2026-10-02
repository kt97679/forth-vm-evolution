#!/bin/sh
# check-reproducible.sh - build twice and compare every image byte for byte.
#
# Every image is reproducible: two builds, whatever their address layout,
# save the same bytes. Images saved by a running system are where this
# breaks - a variable holding an engine or heap address. The SPN savers
# blank such cells (forth/spn-cv8-save.4, forth/spn-full-scrub.4); this
# check finds the next one. It leaves the second build in build/.
set -e
cd "$(dirname "$0")/.."
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
trap 'exit 130' INT TERM HUP
LAYOUTS=1 bash tools/build-stages.sh > "$T/build1.log" 2>&1 || { echo "FAIL - first build (log: $T/build1.log)"; trap - EXIT; exit 1; }
mkdir "$T/first" && cp build/*.img "$T/first/"
LAYOUTS=1 bash tools/build-stages.sh > "$T/build2.log" 2>&1 || { echo "FAIL - second build (log: $T/build2.log)"; trap - EXIT; exit 1; }
n=0; total=0
for f in "$T"/first/*.img; do
    total=$((total + 1))
    b="build/$(basename "$f")"
    if ! cmp -s "$f" "$b"; then
        n=$((n + 1)); echo "differs: $(basename "$f") ($(cmp -l "$f" "$b" 2>/dev/null | wc -l) bytes)"
    fi
done
[ "$n" -eq 0 ] && { echo "PASS - all $total images identical across two builds"; exit 0; }
echo "FAIL - $n of $total images differ between two builds"; exit 1
