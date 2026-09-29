#!/bin/sh
# tools/mk-spn-image.sh BUILD-DIR - the SPN stage image, s7-spn-s64.img.
#
# Builds two images from the same source, differing only in recipes:
#   s7-spn-s64.img   the boot translation run once at build time and its
#                    decisions recorded in the image; boot replays them.
#   s7-full-s64.img  no recipes; boot translates the dictionary in full.
# They produce byte-identical native code; only start-up and size differ.
# SPN_RECIPES=0 makes s7-spn itself the recipe-less one.
#
# The kernel image, plus the SPN translator, saved with SPN-BOOT as its
# boot word: every start translates the dictionary, then falls through
# to the ordinary banner and interpreter. pool.4 and save-system.4 are
# only there to save it; locals.4 is left out because it redefines ;
# as SPN does, and save-system.4 needs only its one variable.
set -e
O=$(cd "$1" && pwd); ROOT=$(cd "$(dirname "$0")/.." && pwd); W=$O/work
# --engine SUFFIX "FLAGS": only a layout variant of the engine, as for s8.
if [ "${2:-}" = --engine ]; then
    cc -O2 -Wall $4 -o "$O/s7-spn-64$3" "$ROOT/engine/spn.c" \
       "$ROOT/engine/spn-stencils.c" "$ROOT/engine/spn-markers.c"
    cp "$O/s7-spn-64$3" "$O/s7-full-64$3"; exit 0
fi
cc -O2 -Wall -o "$O/spn-64" "$ROOT/engine/spn.c" "$ROOT/engine/spn-stencils.c" \
   "$ROOT/engine/spn-markers.c"
cp "$W/kernel.img" "$W/.spn-kernel-save.img"
rm -f "$W/s7-spn-s64.img"
REC=$([ "${SPN_RECIPES:-1}" = 1 ] && echo SPN-RECORD || echo "")
( cd "$W" && printf 'S" pool.4" INCLUDED\nVARIABLE LSAVE-SP\nS" save-system.4" INCLUDED\nS" %s/forth/spn-full.4" INCLUDED\n%s\n'"' SPN-BOOT SET-BOOT\nS\" s7-spn-s64.img\" SAVE-SYSTEM\nBYE\n" "$ROOT" "$REC" \
    | "$O/spn-64" kernel.img >/dev/null 2>&1 )
cp "$W/.spn-kernel-save.img" "$W/kernel.img"
[ -s "$W/s7-spn-s64.img" ] || { echo "failed to save s7-spn-s64.img"; exit 1; }
cp "$W/s7-spn-s64.img" "$O/s7-spn-s64.img"
cp "$O/spn-64" "$O/s7-spn-64"
echo "built  s7-spn ($(wc -c < "$O/s7-spn-s64.img") bytes)"
if [ "${SPN_RECIPES:-1}" = 1 ] && [ -z "${SPN_NESTED:-}" ]; then
    cp "$O/s7-spn-s64.img" "$O/.s7-rcp.img"
    SPN_RECIPES=0 SPN_NESTED=1 "$0" "$O" >/dev/null
    cp "$O/s7-spn-s64.img" "$O/s7-full-s64.img"; cp "$O/spn-64" "$O/s7-full-64"
    cp "$O/.s7-rcp.img" "$O/s7-spn-s64.img"; rm -f "$O/.s7-rcp.img"
    echo "built  s7-full, no recipes ($(wc -c < "$O/s7-full-s64.img") bytes)"
fi
