#!/bin/bash
# loop-bench.sh [BUILDDIR] [REPS] - the narrow benchmark.
#
# bench/parse.fth is nested counted loops over stack arithmetic, written
# in the intersection of what SOD32's kernel.4th and this project's
# kernel.4 both provide, so every engine runs the same source text.
#
# It exists to separate two questions that corpus-run.sh measures
# together: how fast the VM dispatches, and how fast the rest of the
# Forth system is. Almost all of the time here is the inner interpreter,
# so a difference is attributable to the encoding and the dispatch in a
# way that a whole-system workload never is.
#
# It is a NARROW benchmark and the article should say so. It has no
# dictionary lookups, no parsing, no string handling and no calls except
# one per outer iteration, which is exactly the profile that flatters a
# cheap dispatch loop. It is not evidence about anything else.
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
REPS=${2:-7}
WIDTH=${WIDTH:-32}

IN=$ROOT/bench/parse.fth
printf 'BYE\n' > "$O/.nul.fth"
STAGES="s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec"

declare -A E I D
for s in $STAGES; do E[$s]=$O/$s-$WIDTH; I[$s]=$O/$s-s$WIDTH.img; D[$s]=$W; done
ORDER="$STAGES"
if [ "$WIDTH" = 32 ] && [ -x "$O/sod32/sod32" ]; then
    E[sod32]=$O/sod32/sod32; I[sod32]=$O/sod32/forth.img; D[sod32]=$O/sod32
    ORDER="sod32 $STAGES"
fi

echo "verifying every engine completes the parse run..."
ok=""
for s in $ORDER; do
    [ -x "${E[$s]}" ] && [ -r "${I[$s]}" ] || { printf '  %-12s SKIP\n' "$s"; continue; }
    ( cd "${D[$s]}" && timeout 180 "${E[$s]}" "${I[$s]}" < "$IN" > "$O/.b.out" 2>&1 )
    st=$?
    if [ $st -ne 0 ]; then
        printf '  %-12s EXCLUDED: exited %s\n' "$s" "$st"
    elif ! grep -aq PARSE-DONE "$O/.b.out"; then
        printf '  %-12s EXCLUDED: did not finish\n' "$s"
    else
        printf '  %-12s ok\n' "$s"; ok="$ok $s"
    fi
done
echo

declare -A OVER BEST
for s in $ok; do
    t0=$(date +%s%N)
    for _ in $(seq 10); do
        ( cd "${D[$s]}" && "${E[$s]}" "${I[$s]}" < "$O/.nul.fth" >/dev/null 2>&1 )
    done
    t1=$(date +%s%N)
    OVER[$s]=$(( (t1 - t0) / 10 )); BEST[$s]=0
done

echo "timing, $REPS interleaved repetitions..."
for _ in $(seq "$REPS"); do
    for s in $ok; do
        t0=$(date +%s%N)
        ( cd "${D[$s]}" && "${E[$s]}" "${I[$s]}" < "$IN" >/dev/null 2>&1 )
        t1=$(date +%s%N)
        d=$(( t1 - t0 ))
        [ "${BEST[$s]}" -eq 0 ] || [ "$d" -lt "${BEST[$s]}" ] && BEST[$s]=$d
    done
done
echo

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
