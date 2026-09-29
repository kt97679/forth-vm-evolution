#!/bin/sh
# tools/mk-spn-image.sh BUILD-DIR - the SPN stage image, s7-spn-s64.img.
#
# The kernel image, plus the SPN translator, saved with SPN-BOOT as its
# boot word: every start translates the dictionary, then falls through
# to the ordinary banner and interpreter. pool.4 and save-system.4 are
# only there to save it; locals.4 is left out because it redefines ;
# as SPN does, and save-system.4 needs only its one variable.
set -e
O=$1; ROOT=$(cd "$(dirname "$0")/.." && pwd); W=$O/work
cc -O2 -Wall -o "$O/spn-64" "$ROOT/engine/spn.c" "$ROOT/engine/spn-stencils.c" \
   "$ROOT/engine/spn-markers.c"
cp "$W/kernel.img" "$W/.spn-kernel-save.img"
rm -f "$W/s7-spn-s64.img"
( cd "$W" && printf 'S" pool.4" INCLUDED\nVARIABLE LSAVE-SP\nS" save-system.4" INCLUDED\nS" %s/forth/spn-full.4" INCLUDED\n'"' SPN-BOOT SET-BOOT\nS\" s7-spn-s64.img\" SAVE-SYSTEM\nBYE\n" "$ROOT" \
    | "$O/spn-64" kernel.img >/dev/null 2>&1 )
cp "$W/.spn-kernel-save.img" "$W/kernel.img"
[ -s "$W/s7-spn-s64.img" ] || { echo "failed to save s7-spn-s64.img"; exit 1; }
cp "$W/s7-spn-s64.img" "$O/s7-spn-s64.img"
cp "$O/spn-64" "$O/s7-spn-64"
echo "built  s7-spn ($(wc -c < "$O/s7-spn-s64.img") bytes)"
