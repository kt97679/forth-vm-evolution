#!/bin/bash
# corpus-run.sh [BUILDDIR] [REPS] - the cross-family benchmark.
#
# WHY THIS EXISTS. kernel-compile.sh cannot include SOD32. SOD32 does
# cross-compile itself, in about 39 ms, but it compiles ITS OWN kernel -
# kernel.4th, a different word set from kernel.4 - so the two numbers
# measure different amounts of work and putting them in one column would
# be dishonest.
#
# The shared ANS CORE corpus is the one workload both families perform
# identically: the same 616 cases, the same source text, byte for byte.
# It compiles several hundred definitions at run time and then executes
# them, so it exercises the compiler and the inner interpreter together.
# That makes it the right place to put SOD32 beside its descendants.
#
# It is a weaker VM benchmark than kernel compilation in one respect:
# the corpus is dominated by short definitions and stack arithmetic
# rather than by dictionary work, so it flatters encodings with cheap
# dispatch and says less about compile-heavy workloads. Both numbers
# belong in the article, and neither on its own.
#
# CORRECTNESS GATE. A stage is timed only if the run reaches the
# end-of-corpus sentinel with zero failures, so a stage cannot place
# well by giving up early.
set -u

# Every engine this script runs is a measured subject, so it runs in a
# predictable environment rather than in whatever the caller happens to
# have exported.
#
# LD_PRELOAD is the one that actually bites. A desktop session that
# preloads a library into everything will have it loaded into every
# engine here too, which is unwanted work inside the thing being timed;
# and when the engine is a 32-bit binary and the library is 64-bit,
# ld.so cannot load it and writes a line of complaint per process. That
# was reported from a real machine: six copies of "object
# 'libgtk3-nocsd.so.0' from LD_PRELOAD cannot be preloaded" during the
# dictionary dumps. Harmless there, because a dump captures stdout and
# ld.so writes to stderr - but not something to leave in a benchmark.
unset LD_PRELOAD

cd "$(dirname "$0")/.."
ROOT=$PWD
O=${1:-$ROOT/build}
O=$(cd "$O" && pwd)
W=$O/work
REPS=${2:-10}
WIDTH=${WIDTH:-32}

CORPUS=$ROOT/tests/corpus/core.fth
SENTINEL=CORPUS-REACHED-END
IN=$O/.bench-corpus.fth
{ cat "$CORPUS"; printf '\nS" %s" TYPE CR\nBYE\n' "$SENTINEL"; } > "$IN"
printf 'BYE\n' > "$O/.nul.fth"
ERRS='INCORRECT RESULT: \{|WRONG NUMBER OF RESULTS: \{|Undefined word'

STAGES="s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec"

# name -> "engine image workdir"
declare -A E I D
for s in $STAGES; do
    E[$s]=$O/$s-$WIDTH; I[$s]=$O/$s-s$WIDTH.img; D[$s]=$W
done
ORDER="$STAGES"
if [ "$WIDTH" = 32 ] && [ -x "$O/sod32/sod32" ]; then
    E[sod32]=$O/sod32/sod32; I[sod32]=$O/sod32/forth.img; D[sod32]=$O/sod32
    ORDER="sod32 $STAGES"
fi

# ---- correctness gate ------------------------------------------------
echo "verifying every engine completes the corpus..."
ok=""
for s in $ORDER; do
    if [ ! -x "${E[$s]}" ] || [ ! -r "${I[$s]}" ]; then
        printf '  %-12s SKIP (not built)\n' "$s"; continue
    fi
    ( cd "${D[$s]}" && timeout 120 "${E[$s]}" "${I[$s]}" < "$IN" > "$O/.b.out" 2>&1 )
    st=$?
    out=$(tr -d '\r' < "$O/.b.out")
    bad=$(printf '%s' "$out" | grep -acE "$ERRS")
    if [ $st -ne 0 ]; then
        printf '  %-12s EXCLUDED: exited %s\n' "$s" "$st"
    elif ! printf '%s' "$out" | grep -q "$SENTINEL"; then
        printf '  %-12s EXCLUDED: did not reach the end of the corpus\n' "$s"
    elif [ "$bad" -ne 0 ]; then
        printf '  %-12s EXCLUDED: %s failing cases\n' "$s" "$bad"
    else
        printf '  %-12s ok\n' "$s"; ok="$ok $s"
    fi
done
echo

# ---- fixed overhead --------------------------------------------------
declare -A OVER
for s in $ok; do
    t0=$(date +%s%N)
    for _ in $(seq 20); do
        ( cd "${D[$s]}" && "${E[$s]}" "${I[$s]}" < "$O/.nul.fth" >/dev/null 2>&1 )
    done
    t1=$(date +%s%N)
    OVER[$s]=$(( (t1 - t0) / 20 ))
done

# ---- interleaved timing ----------------------------------------------
declare -A BEST
for s in $ok; do BEST[$s]=0; done
echo "timing, $REPS interleaved repetitions..."
for _ in $(seq "$REPS"); do
    for s in $ok; do
        t0=$(date +%s%N)
        ( cd "${D[$s]}" && "${E[$s]}" "${I[$s]}" < "$IN" >/dev/null 2>&1 )
        t1=$(date +%s%N)
        d=$(( t1 - t0 ))
        if [ "${BEST[$s]}" -eq 0 ] || [ "$d" -lt "${BEST[$s]}" ]; then BEST[$s]=$d; fi
    done
done
echo

# ---- report ----------------------------------------------------------
# Minimum, not mean: noise on a shared machine only ever adds time.
base=""
printf '%-12s %10s %10s %9s\n' stage "ms" "net ms" "vs first"
for s in $ok; do
    net=$(( BEST[$s] - OVER[$s] ))
    [ -z "$base" ] && base=$net
    printf '%-12s %10.2f %10.2f %9.3f\n' "$s" \
        "$(echo "${BEST[$s]}/1000000" | bc -l)" \
        "$(echo "$net/1000000" | bc -l)" \
        "$(echo "$net/$base" | bc -l)"
done
echo
echo "cell width $WIDTH, $REPS reps, minimum of run; startup subtracted"
echo "every row above ran the identical 616-case corpus with zero failures"
