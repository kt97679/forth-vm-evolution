#!/bin/sh
# tools/arm-qemu-check.sh - the 32-bit ARM path, checked without ARM hardware
# (Iteration 29): the cell engine cross-compiled for ARMv7 (ARM mode, static)
# runs the 32-bit kernel under qemu's user-mode emulator. Correctness only -
# timing belongs on the Tegra.
#
# Needs (Ubuntu): gcc-arm-linux-gnueabihf libc6-dev-armhf-cross qemu-user
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd); T=${TMPDIR:-/tmp}/arm-qemu-check; mkdir -p "$T"
command -v arm-linux-gnueabihf-gcc >/dev/null && command -v qemu-arm >/dev/null || {
    echo "needs arm-linux-gnueabihf-gcc and qemu-arm (apt: gcc-arm-linux-gnueabihf libc6-dev-armhf-cross qemu-user)" >&2; exit 1; }
arm-linux-gnueabihf-gcc -O2 -marm -static -Wall -o "$T/cell-arm" "$ROOT/engine/relf.c"
out=$(printf '2 3 + . CR : SQ DUP * ; 12 SQ . CR BYE\n' | qemu-arm "$T/cell-arm" "$ROOT/forth/kernel32-seed.img" 2>&1)
echo "$out" | tr -d '\r' | grep -q '^5 *$' && echo "$out" | tr -d '\r' | grep -q '^144 *$' \
    && echo "PASS - the cell engine on ARMv7 (qemu) runs the 32-bit kernel" \
    || { echo "FAIL:"; echo "$out"; exit 1; }
