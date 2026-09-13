#!/bin/bash
# bench/lib.sh - the measurement machinery every harness shares.
#
# A harness sets a few variables and calls bench_run. Everything about
# HOW a number is produced lives here, so the five workloads cannot
# drift apart in methodology, which they had begun to do.
#
# ---------------------------------------------------------------------
# WHAT THIS CORRECTS
#
# The variability in these measurements was never mostly run-to-run
# noise. Three consecutive runs of the SAME binaries agree to 1-2%; but
# rebuild the tree and a stage moves by five or ten percent. Where the
# compiler happens to place code is worth several percent, and it is
# FIXED for a given binary - so taking the minimum over more repetitions
# measures that bias more precisely instead of removing it. The old
# harnesses reported a figure that repeated to 1% and could be wrong by
# 12%.
#
# So two mechanisms, for two different problems:
#
#   Run noise only ever ADDS time. Take the minimum of several rounds,
#   interleaved across binaries so drift hits everything alike.
#
#   Build bias needs more builds. With the tree built at LAYOUTS=N,
#   every engine exists N times over, each compiled with flags that move
#   code and change nothing it computes. All N are timed and the MEAN is
#   reported, with one standard error.
#
# The mean rather than the median: layout effects are roughly symmetric,
# so the mean of n has standard error sd/sqrt(n), while a median of five
# is much less efficient - measured, a median moved 6-9% between runs
# where the mean moves 2-3%.
#
# The resulting error bar is dominated by build bias, not by the
# machine, and two consecutive runs now agree inside it.
# ---------------------------------------------------------------------
#
# A harness provides:
#   BENCH_NAME    what to call the workload
#   BENCH_STAGES  stage names, in report order
#   bench_prepare writes $INPUT; may set REF (image mode) or MARK
#   BENCH_CHECK   "image" (produced kernel.img must equal $REF)
#                 or "marker" (output must contain $MARK)
#   BENCH_ERRS    optional egrep pattern; any match fails the gate
#   BENCH_SOD32   1 to include the vendored SOD32 as an extra runner
set -u

# Every engine is a measured subject, so it runs in a predictable
# environment rather than in whatever the caller exported. LD_PRELOAD is
# the one that bites: a preloaded library is work inside the thing being
# timed, and a 64-bit one cannot load into a 32-bit engine at all.
unset LD_PRELOAD

bench_init() {
    ROOT=$PWD
    O=${1:-$ROOT/build}
    O=$(cd "$O" && pwd)
    W=$O/work
    REPS=${2:-6}
    WIDTH=${WIDTH:-64}
    # Pin to one CPU where possible: a migration costs a cold cache and
    # shows up as a slow round.
    PIN=""
    command -v taskset >/dev/null 2>&1 && PIN="taskset -c 0"
    INPUT=$O/.bench-in.fth
    OUTF=$O/.bench-out
    NULF=$O/.bench-nul.fth
    printf 'BYE\n' > "$NULF"
    REF=""; MARK=""; BENCH_ERRS=${BENCH_ERRS:-}
}

# runner record: stage<TAB>engine<TAB>image<TAB>workdir
bench_runners() {
    local s e
    for s in $BENCH_STAGES; do
        [ -r "$O/$s-s$WIDTH.img" ] || continue
        for e in "$O/$s-$WIDTH" "$O/$s-$WIDTH"-v*; do
            [ -x "$e" ] || continue
            printf '%s\t%s\t%s\t%s\n' "$s" "$e" "$O/$s-s$WIDTH.img" "$W"
        done
    done
    if [ "${BENCH_SOD32:-0}" = 1 ] && [ "$WIDTH" = 32 ] \
       && [ -x "$O/sod32/sod32" ]; then
        printf '%s\t%s\t%s\t%s\n' sod32 "$O/sod32/sod32" \
               "$O/sod32/forth.img" "$O/sod32"
    fi
}

bench_one() {   # bench_one ENGINE IMAGE WORKDIR -> exit status, output in $OUTF
    ( cd "$3" && timeout 180 $PIN "$1" "$2" < "$INPUT" > "$OUTF" 2>&1 )
}

bench_run() {
    local rec s e i d st shown
    bench_prepare

    echo "verifying every runner..."
    : > "$O/.bench.ok"
    shown=" "
    while IFS=$'\t' read -r s e i d; do
        [ -n "$s" ] || continue
        bench_one "$e" "$i" "$d"; st=$?
        if [ $st -ne 0 ]; then
            printf '  %-12s %-26s EXCLUDED: exited %s\n' "$s" "$(basename "$e")" "$st"
        elif [ "$BENCH_CHECK" = image ] && ! cmp -s "$W/kernel.img" "$REF"; then
            printf '  %-12s %-26s EXCLUDED: image differs\n' "$s" "$(basename "$e")"
        elif [ "$BENCH_CHECK" = marker ] && ! grep -aq "$MARK" "$OUTF"; then
            printf '  %-12s %-26s EXCLUDED: did not finish\n' "$s" "$(basename "$e")"
        elif [ -n "$BENCH_ERRS" ] && grep -aqE "$BENCH_ERRS" "$OUTF"; then
            printf '  %-12s %-26s EXCLUDED: failing cases\n' "$s" "$(basename "$e")"
        else
            printf '%s\t%s\t%s\t%s\n' "$s" "$e" "$i" "$d" >> "$O/.bench.ok"
            case "$shown" in *" $s "*) ;; *) printf '  %-12s ok\n' "$s"
                shown="$shown$s ";; esac
        fi
        [ "$BENCH_CHECK" = image ] && cp "$SAVE" "$W/kernel.img"
    done < <(bench_runners)
    echo

    # Fixed cost per binary: load the image and exit. Subtracted, because
    # at ~1.5 ms against 20-300 ms of work it would otherwise compress
    # every ratio towards 1.
    local n=0
    : > "$O/.bench.over"
    while IFS=$'\t' read -r s e i d; do
        local t0 t1
        t0=$(date +%s%N)
        for _ in 1 2 3 4 5 6 7 8 9 10; do
            ( cd "$d" && $PIN "$e" "$i" < "$NULF" >/dev/null 2>&1 )
        done
        t1=$(date +%s%N)
        echo "$(( (t1 - t0) / 10 ))" >> "$O/.bench.over"
        n=$((n + 1))
    done < "$O/.bench.ok"

    echo "timing $BENCH_NAME: $REPS rounds over $n binaries ..."
    : > "$O/.bench.dat"
    local r
    for r in $(seq "$REPS"); do
        local k=0
        while IFS=$'\t' read -r s e i d; do
            k=$((k + 1))
            local ov t0 t1
            ov=$(sed -n "${k}p" "$O/.bench.over")
            t0=$(date +%s%N)
            ( cd "$d" && $PIN "$e" "$i" < "$INPUT" >/dev/null 2>&1 )
            t1=$(date +%s%N)
            [ "$BENCH_CHECK" = image ] && cp "$SAVE" "$W/kernel.img"
            echo "$s $e $(( t1 - t0 - ov ))" >> "$O/.bench.dat"
        done < "$O/.bench.ok"
    done
    echo

    # sod32 is reported first when it took part: it is the ancestor, and
    # a reader should see it before the ladder that came out of it.
    local ORDER=$BENCH_STAGES
    [ "${BENCH_SOD32:-0}" = 1 ] && [ "$WIDTH" = 32 ] && ORDER="sod32 $ORDER"
    BASE_STAGE=${BASE_STAGE:-s0-cell} \
    python3 "$ROOT/bench/report.py" "$O/.bench.dat" "$WIDTH" "$REPS" \
            "$BENCH_NAME" $ORDER
}
