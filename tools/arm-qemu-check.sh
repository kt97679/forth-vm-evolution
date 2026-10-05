#!/bin/sh
# tools/arm-qemu-check.sh - the 32-bit ARM path, checked (Iterations 29-30).
#
# 1. The cell engine, built for ARMv7 (ARM state, static), runs the 32-bit
#    kernel.
# 2. SPN on ARM: its engine and stencils built the same way; forth/spn.4
#    translates fib and sumto (bench/spn) to ARM machine code, and each
#    must give the interpreter's answer - 1346269 and 500500.
# 3. s8, the current SPN (Iteration 31): engine/spn-cv8.c built for ARM;
#    s8-full, s8-spncv8 (recipes) and s8-lazy made from the 32-bit s6
#    image as tools/mk-spn-cv8-image.sh makes them; each must pass the ANS
#    corpus as tools/run-tests.sh judges it - the good corpus to its end
#    with no error, the deliberately wrong one with at least one.
#    Needs build/s6-cv8b-s32.img, from tools/build-stages.sh with 4-byte
#    cells - native on an ARM host; on Ubuntu x86-64 from gcc-multilib,
#    which conflicts with gcc-arm-linux-gnueabihf: build first, or keep the
#    cross-compiler and link /usr/include/asm -> x86_64-linux-gnu/asm, the
#    one file multilib provided that the 4-byte build needs.
#
# On an x86-64 host it cross-compiles and runs everything under qemu's
# user-mode emulator - correctness only, which is all qemu can say: it also
# hides a missing instruction-cache flush, since it watches pages it has
# translated. On an ARMv7 host (the Tegra) it builds with cc and runs
# natively. Needs, on Ubuntu x86-64: gcc-arm-linux-gnueabihf
# libc6-dev-armhf-cross qemu-user.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd); T=${TMPDIR:-/tmp}/arm-qemu-check; mkdir -p "$T"
case "$(uname -m)" in
    armv7*|armv8l) CC=cc; RUN= ;;
    *) CC=arm-linux-gnueabihf-gcc; RUN=qemu-arm
       command -v $CC >/dev/null && command -v $RUN >/dev/null || {
           echo "needs $CC and $RUN (apt: gcc-arm-linux-gnueabihf libc6-dev-armhf-cross qemu-user)" >&2; exit 1; } ;;
esac
FLAGS="-O2 -marm -static -Wall"
$CC $FLAGS -o "$T/cell-arm" "$ROOT/engine/relf.c" 2>/dev/null
out=$(printf '2 3 + . CR : SQ DUP * ; 12 SQ . CR BYE\n' | $RUN "$T/cell-arm" "$ROOT/forth/kernel32-seed.img" 2>&1 | tr -d '\r')
echo "$out" | grep -q '^5 *$' && echo "$out" | grep -q '^144 *$' \
    && echo "PASS - the cell engine on ARMv7${RUN:+ (qemu)} runs the 32-bit kernel" \
    || { echo "FAIL - the cell engine:"; echo "$out"; exit 1; }
$CC $FLAGS -o "$T/spn-arm" "$ROOT/engine/spn.c" "$ROOT/engine/spn-stencils.c" "$ROOT/engine/spn-markers.c" 2>/dev/null
for p in fib:1346269 sumto:500500; do
    name=${p%%:*}; want=${p#*:}
    got=$(cd "$ROOT/bench" && { cat "spn/$name.fth"; echo BYE; } | $RUN "$T/spn-arm" ../forth/kernel32-seed.img 2>&1 | tr -d '\r' | grep -E '^-?[0-9]+ -?[0-9]+ *$' | tail -1)
    [ "$got" = "$want $want " ] || [ "$got" = "$want $want" ] \
        && echo "PASS - SPN on ARMv7${RUN:+ (qemu)}: $name interpreted and native, both $want" \
        || { echo "FAIL - SPN $name: got '$got', want '$want $want'"; exit 1; }
done
O=$ROOT/build; W=$O/work
if [ ! -r "$O/s6-cv8b-s32.img" ] || [ ! -r "$O/.corpus-good.fth" ]; then
    echo "SKIP - s8 on ARMv7: needs build/s6-cv8b-s32.img (a 4-byte-cell build) and the corpus (tools/run-tests.sh)"
    exit 0
fi
python3 "$ROOT/tools/gen-tos.py" "$ROOT/engine/spn-cv8.c" > "$T/spn-cv8-tos.c"
$CC $FLAGS -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=0 -DSPEC=1 -DSHAREDCALL=1 -DDOESFAR=1 -DSPN_FUSED_BR=1 -DSPN_IO=1 \
    -I"$O" -I"$ROOT/engine" -o "$T/s8-arm" "$T/spn-cv8-tos.c" \
    "$ROOT/engine/spn-stencils.c" "$ROOT/engine/spn-markers.c" 2>/dev/null
ERRS='INCORRECT RESULT: \{|WRONG NUMBER OF RESULTS: \{|Undefined word'
for v in s8-full: s8-spncv8:SPN-RECORD s8-lazy:SPN-RECORD-LAZY; do
    name=${v%%:*}; rec=${v#*:}; img="$T/$name-s32.img"; rm -f "$img"
    ( cd "$W" && printf 'S" %s/forth/spn-cv8.4" INCLUDED\nS" %s/forth/spn-cv8-build.4" INCLUDED\nS" %s/forth/spn-cv8-save.4" INCLUDED\n%s\n'"' SPN-BOOT SET-BOOT\nS\" %s\" SPN-SAVE\nBYE\n" \
          "$ROOT" "$ROOT" "$ROOT" "$rec" "$img" | $RUN "$T/s8-arm" "$O/s6-cv8b-s32.img" >/dev/null 2>&1 )
    [ -s "$img" ] || { echo "FAIL - $name: the image was not saved"; exit 1; }
    nat=$(printf '#NATIVE @ . CR BYE\n' | $RUN "$T/s8-arm" "$img" 2>&1 | tr -d '\r' | grep -E '^[0-9]+ *$' | tail -1)
    nat=$(echo $nat)
    for c in good bad; do
        ( cd "$W" && $RUN "$T/s8-arm" "$img" < "$O/.corpus-$c.fth" > "$T/$name-$c.out" 2>&1 ) || true
        grep -q CORPUS-REACHED-END "$T/$name-$c.out" || { echo "FAIL - $name: the $c corpus stopped before its end"; exit 1; }
        n=$(tr -d '\r' < "$T/$name-$c.out" | grep -cE "$ERRS" || true)
        if [ $c = good ] && [ "$n" -ne 0 ]; then echo "FAIL - $name: $n bad cases"; exit 1; fi
        if [ $c = bad ] && [ "$n" -lt 1 ]; then echo "FAIL - $name: the deliberately wrong case was not detected"; exit 1; fi
    done
    echo "PASS - s8 on ARMv7${RUN:+ (qemu)}: $name, ${nat:-?} words native, the corpus passes and its wrong case is caught"
done
