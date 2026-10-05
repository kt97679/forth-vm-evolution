#!/bin/sh
# tools/arm-qemu-check.sh - the 32-bit ARM path, checked (Iterations 29-30).
#
# 1. The cell engine, built for ARMv7 (ARM state, static), runs the 32-bit
#    kernel.
# 2. SPN on ARM: its engine and stencils built the same way; forth/spn.4
#    translates fib and sumto (bench/spn) to ARM machine code, and each
#    must give the interpreter's answer - 1346269 and 500500.
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
