#!/bin/sh
# mk-spn-cv8-image.sh BUILD-DIR - build s8-spncv8: SPN on the CV8 image.
#
# The engine is engine/spn-cv8.c - the CV8 engine plus SPN - put through
# tools/gen-tos.py and compiled exactly as the byte-header stage s6 is.
# The image is s6's, with the translator (forth/spn-cv8.4) and a saver
# (forth/spn-cv8-save.4) compiled into it by its own CV8 compiler, and
# SPN-BOOT set to run at start-up: every boot translates the dictionary.
# Needs s6-cv8b-s64.img and the fold tables from tools/build-stages.sh.
# x86-64 only.
#
# mk-spn-cv8-image.sh BUILD-DIR --engine SUFFIX "FLAGS" builds only a
# layout variant of the engine, s8-spncv8-64SUFFIX (and s8-full's copy),
# with extra compiler FLAGS - what build-stages.sh's LAYOUTS asks for.
# The images need no variants: SPN reads its stencils, and finds their
# holes, in whichever engine is running.
set -e
O=$(cd "$1" && pwd); ROOT=$(cd "$(dirname "$0")/.." && pwd); W=$O/work
[ -r "$O/s6-cv8b-s64.img" ] || { echo "build s6-cv8b first (tools/build-stages.sh)"; exit 1; }
python3 "$ROOT/tools/gen-tos.py" "$ROOT/engine/spn-cv8.c" > "$O/spn-cv8-tos.c"
engine() {  # engine SUFFIX FLAGS - the one place these flags are written
    cc -O2 $2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=0 -DSPEC=1 -DSHAREDCALL=1 -DDOESFAR=1 \
       -I"$O" -o "$O/s8-spncv8-64$1" "$O/spn-cv8-tos.c" \
       "$ROOT/engine/spn-stencils.c" "$ROOT/engine/spn-markers.c"
    cp "$O/s8-spncv8-64$1" "$O/s8-full-64$1"
}
if [ "${2:-}" = --engine ]; then engine "$3" "$4"; exit 0; fi
engine "" ""
# Two variants, as for s7: s8-spncv8 carries recipes - the translation
# recorded once here and replayed at boot - and s8-full translates in
# full at every boot. Same engine, same native code.
build() {  # build NAME RECORD-WORD
    rm -f "$W/$1-s64.img"
    ( cd "$W" && printf 'S" %s/forth/spn-cv8.4" INCLUDED\nS" %s/forth/spn-cv8-save.4" INCLUDED\n%s\n'"' SPN-BOOT SET-BOOT\nS\" %s-s64.img\" SPN-SAVE\nBYE\n" \
          "$ROOT" "$ROOT" "$2" "$1" | "$O/s8-spncv8-64" "$O/s6-cv8b-s64.img" >/dev/null 2>&1 )
    [ -s "$W/$1-s64.img" ] || { echo "failed to save $1-s64.img"; exit 1; }
    cp "$W/$1-s64.img" "$O/$1-s64.img"
    echo "built  $1 ($(wc -c < "$O/$1-s64.img") bytes)"
}
build s8-spncv8 SPN-RECORD
build s8-full   ""
