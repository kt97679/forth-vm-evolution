#!/bin/bash
# parse-bench.sh - 4000 lines of interpreted arithmetic: almost pure outer interpreter
#
# A thin harness: everything about HOW a number is produced lives in
# bench/lib.sh, so the five workloads cannot drift apart in method.
cd "$(dirname "$0")/.."
. bench/lib.sh
bench_init "${1:-}" "${2:-}"

BENCH_NAME=parse
BENCH_STAGES="s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec s6-cv8b"
BENCH_CHECK=marker
BENCH_SOD32=1

bench_prepare() {
    MARK=PARSE-DONE
    cp "$ROOT/bench/parse.fth" "$INPUT"
}

bench_run
