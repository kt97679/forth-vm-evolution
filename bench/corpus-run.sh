#!/bin/bash
# corpus-run.sh - the shared 616-case ANS CORE corpus, the one workload SOD32 also runs
#
# A thin harness: everything about HOW a number is produced lives in
# bench/lib.sh, so the five workloads cannot drift apart in method.
cd "$(dirname "$0")/.."
. bench/lib.sh
bench_init "${1:-}" "${2:-}"

BENCH_NAME=corpus
BENCH_STAGES="s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec s6-cv8b"
BENCH_CHECK=marker
BENCH_SOD32=1
# The only workload SOD32 and the ladder perform from identical source,
# so it carries the cross-family comparison.
BENCH_ERRS='INCORRECT RESULT: \{|WRONG NUMBER OF RESULTS: \{|Undefined word'

bench_prepare() {
    MARK=CORPUS-REACHED-END
    { cat "$ROOT/tests/corpus/core.fth"
      printf '\nS" %s" TYPE CR\nBYE\n' "$MARK"; } > "$INPUT"
}

bench_run
