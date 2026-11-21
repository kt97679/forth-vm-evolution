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
# Iteration 714: a design that fails the check keeps the converter's images - the pre-mortem's gate
# (results/drafts/premortem-roles-707.md): a role that fails it ships its translator-built image, named, rather than
# holding the others back. It gets no `make selfhost` rules (a stale pair removed), both widths stay the converter's (an
# 8-byte image shipped before a 4-byte failure is put back), and DIR/TRANSLATOR-BUILT names it with the check's reason -
# the top Makefile's `make selfhost` and run-tests skip what it names. STRICT=1: stop at the first failure, as before.
# Iteration 721: TRANSLATOR='NAME:REASON|NAME:REASON' - the gate's speed half (lab/evolve/selfhost-speed.py): a design
# whose self-built image runs slower than its translator's ships translator-built, named with REASON, its check not run
# (on a fresh export, whose images are the translator's - a build-out's order).
forced() { echo "${TRANSLATOR:-}" | tr '|' '\n' | sed -n "s/^$1://p" | head -n 1; }
TB=$DS/TRANSLATOR-BUILT; KEPT=; SHIPPED=0
[ -f "$TB" ] && grep -v -E "^($(echo $NAMES | tr ' ' '|')) " "$TB" > "$TB.new"; mv -f "$TB.new" "$TB" 2> /dev/null
why() {     # the check's output: its reason - the cross compiler's own words where its log has them ("cross: not yet: ...")
    L=$(tail -n 1 "$1" | sed -n 's/.*(\(.*\.log\))$/\1/p')
    r=; [ -n "$L" ] && [ -f "$L" ] && r=$(grep -h 'cross: not yet:' "$L" | head -n 1 | tr -s ' '); [ -n "$L" ] && [ -f "$L" ] && [ -z "$r" ] && r=$(grep -h '^cross: ' "$L" | tail -n 1)
    echo "${r:-$(tail -n 1 "$1")}" | cut -c1-200
}
keep() {    # NAME REASON: the converter's images stay
    [ -n "${STRICT:-}" ] && die "$1: $2"
    sed -i '/^# `make selfhost` (`selfhost32`)/,/^\.PHONY: selfhost selfhost32/d' "$DS/$1/Makefile"
    [ -s "$TB" ] || printf '%s\n' '# Designs whose image.img and image32.img are the converter'"'"'s (tools/layout.py), not self-built: the' \
        '# self-hosting check (tools/selfhost-check.sh) failed - the cross compiler cannot yet build them - or the gate'"'"'s' \
        '# speed half found the self-built image slower (TRANSLATOR=, Iteration 721); written by' \
        '# tools/selfhost-ship.sh. NAME, then the check'"'"'s reason. `make selfhost` and the tests skip these.' > "$TB"
    echo "$1 $2" >> "$TB"; KEPT="$KEPT $1"
    echo "selfhost-ship: $1 keeps its translator-built images - $2"
}
for n in $NAMES; do
    M=$DS/$n/Makefile; [ -f "$M" ] || die "no $M"
    f=$(forced "$n"); if [ -n "$f" ]; then keep "$n" "$f"; continue; fi     # 721: by the gate's speed half
    BK=$(mktemp -d) || die "mktemp"
    cp -p "$DS/$n/image.img" "$DS/$n/image32.img" "$BK/" && for s in src src32; do
        [ -f "$DS/$n/$s/vm-jit-ops.h" ] && { mkdir -p "$BK/$s"; cp -p "$DS/$n/$s/vm-jit-ops.h" "$BK/$s/"; }; done
    SHIP=1 DESIGNS=$DS sh tools/selfhost-check.sh "$n" > "$BK/c8" 2>&1; c=$?; cat "$BK/c8"
    if [ $c != 0 ]; then keep "$n" "$(why "$BK/c8")"; rm -rf "$BK"; continue; fi
    SHIP=1 DESIGNS=$DS sh tools/selfhost-check.sh --32 "$n" > "$BK/c4" 2>&1; c=$?; cat "$BK/c4"
    if [ $c != 0 ]; then
        cp -p "$BK/image.img" "$BK/image32.img" "$DS/$n/"; for s in src src32; do
            [ -f "$BK/$s/vm-jit-ops.h" ] && cp -p "$BK/$s/vm-jit-ops.h" "$DS/$n/$s/"; done
        keep "$n" "4-byte cells: $(why "$BK/c4")"; rm -rf "$BK"; continue
    fi
    rm -rf "$BK"
    grep -q '^selfhost:' "$M" || printf '%s\n' '' \
        '# `make selfhost` (`selfhost32`): the image rebuilt from its source - ../forth/ and genes.4 (genes32.4) - must be' \
        '# image.img (image32.img) byte for byte; written by tools/selfhost-ship.sh.' \
        'selfhost: forth' "${TAB}sh ../selfhost.sh forth image.img genes.4 src" '' \
        'selfhost32: forth32' "${TAB}sh ../selfhost.sh forth32 image32.img genes32.4 src32" '' '.PHONY: selfhost selfhost32' >> "$M"
    make -s -C "$DS/$n" selfhost selfhost32 || die "$n: make selfhost failed after shipping"
    SHIPPED=$((SHIPPED + 1))
done
grep -q -v '^#' "$TB" 2> /dev/null || rm -f "$TB"      # none named: no file
echo "selfhost-ship: $SHIPPED design(s) shipped self-built in $DS${KEPT:+; translator-built (TRANSLATOR-BUILT):$KEPT}"

