#!/bin/bash
# kernel-compile.sh - cross-compile the kernel and check the image byte for byte
#
# A thin harness: everything about HOW a number is produced lives in
# bench/lib.sh, so the five workloads cannot drift apart in method.
cd "$(dirname "$0")/.."
. bench/lib.sh
bench_init "${1:-}" "${2:-}"

BENCH_NAME=kernel
BENCH_STAGES="s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec s6-cv8b"
BENCH_CHECK=image
BENCH_SOD32=0
# SOD32 is absent on purpose: it cross-compiles its OWN kernel.4th, a
# different word set, so the two numbers would measure different work.

bench_prepare() {
    # The cross-compiler's TARGET cell width is a source constant, so a
    # 4-byte run needs a retargeted copy. Either way the engine WRITES
    # kernel.img, so the committed image is saved and restored.
    if [ "$WIDTH" = 32 ]; then
        sed '22s/^8 TARGET-CELL-BYTES !/4 TARGET-CELL-BYTES !/' \
            "$ROOT/forth/cross.4" > "$W/cross32.4"
        XCSRC=cross32.4; REFSRC=$W/kernel32.img
    else
        XCSRC=cross.4;   REFSRC=$W/kernel.img
    fi
    REF=$O/.kernel-ref.img
    cp "$REFSRC" "$REF"
    SAVE=$O/.save-kernel.img
    cp "$W/kernel.img" "$SAVE"
    trap 'cp "$SAVE" "$W/kernel.img"' EXIT INT TERM
    printf 'S" extend.4" INCLUDED\nS" %s" INCLUDED\n' "$XCSRC" > "$INPUT"
}

bench_run
