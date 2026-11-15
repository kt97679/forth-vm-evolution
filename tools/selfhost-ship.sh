#!/bin/sh
# tools/selfhost-ship.sh [DIR [NAME...]] - the designs ship their self-built images (Iteration 675;
# results/drafts/selfhost-plan-666.md, phase 5). DIR: a designs directory (default designs/; an export of
# lab/evolve/export-designs.py), NAME: its designs (default every one with a record.json). For each: the genes as Forth
# (lab/evolve/export-genes.py, DESIGNS=DIR), then tools/selfhost-check.sh at 8- and 4-byte cells with SHIP=1 - once
# the check passes (A = B, the gate), A replaces image.img (image32.img) and a JIT design's src/vm-jit-ops.h (src32/)
# takes A's layout lines - then the design's own `make selfhost selfhost32`. DIR gets the images' source - DIR/forth/:
# kernel.4, extend.4, cross-cv8.4 and the overlays any of its genes files names - and selfhost.sh, and each Makefile its
# `make selfhost` rules. Last in a build-out (results/drafts/freeze-build-645.sh): after export-designs.py and
# export-arm.py, which checks that image32.img is the lab's translator-built image. Idempotent: a shipped image is its
# own fixed point, and a second run changes nothing. As the build user, from the repository's top, in a built tree.
# About 30-60 s a design and width: run it detached. SOURCES=1: DIR/forth/ made again, nothing else (a build-out puts
# an export's designs in designs/, which then needs every design's overlays).
set -u
cd "$(dirname "$0")/.."
DS=$(cd "${1:-designs}" && pwd) || exit 1; [ $# -gt 0 ] && shift
NAMES=${*:-$(cd "$DS" && for d in */; do [ -f "$d/record.json" ] && echo "${d%/}"; done)}
die() { echo "selfhost-ship: $*"; exit 1; }
TAB=$(printf '\t')
[ -n "${SOURCES:-}" ] || DESIGNS=$DS python3 lab/evolve/export-genes.py $NAMES > /tmp/selfhost-ship-genes.log 2>&1 || die "export-genes.py (/tmp/selfhost-ship-genes.log)"
mkdir -p "$DS/forth" && rm -f "$DS/forth"/*.4
for f in kernel.4 extend.4 cross-cv8.4 $(grep -h '^S" .*" G+$' "$DS"/*/genes.4 "$DS"/*/genes32.4 | grep -o '[A-Za-z0-9_-]*\.4' | sort -u); do
    cp "forth/$f" "$DS/forth/" || die "no forth/$f"; done
[ "$DS" = "$(pwd)/designs" ] || cp designs/selfhost.sh "$DS/"
[ -n "${SOURCES:-}" ] && { echo "selfhost-ship: $DS/forth/ - $(ls "$DS/forth" | wc -l) files"; exit 0; }
for n in $NAMES; do
    M=$DS/$n/Makefile; [ -f "$M" ] || die "no $M"
    grep -q '^selfhost:' "$M" || printf '%s\n' '' \
        '# `make selfhost` (`selfhost32`): the image rebuilt from its source - ../forth/ and genes.4 (genes32.4) - must be' \
        '# image.img (image32.img) byte for byte; written by tools/selfhost-ship.sh.' \
        'selfhost: forth' "${TAB}sh ../selfhost.sh forth image.img genes.4 src" '' \
        'selfhost32: forth32' "${TAB}sh ../selfhost.sh forth32 image32.img genes32.4 src32" '' '.PHONY: selfhost selfhost32' >> "$M"
    SHIP=1 DESIGNS=$DS sh tools/selfhost-check.sh "$n" || die "$n: the check failed - nothing shipped at 8-byte cells"
    SHIP=1 DESIGNS=$DS sh tools/selfhost-check.sh --32 "$n" || die "$n: the check failed at 4-byte cells (8-byte shipped)"
    make -s -C "$DS/$n" selfhost selfhost32 || die "$n: make selfhost failed after shipping"
done
echo "selfhost-ship: $(echo $NAMES | wc -w) design(s) shipped in $DS"
