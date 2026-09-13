#!/bin/bash
# kernel-compile.sh [BUILDDIR] [REPS] - the headline benchmark.
#
# WHAT IT MEASURES. Each stage runs the cross-compiler over kernel.4 and
# writes a new kernel image. This is the system's own self-hosting work:
# it exercises the interpreter, the compiler, the dictionary and the
# string code rather than one arithmetic idiom, and it cannot be accused
# of being tuned to any encoding, because the encoding it EMITS is the
# cell format in every case. Only the VM running the compiler differs.
#
# WHY IT IS ALSO A CORRECTNESS CHECK. Every stage must produce a kernel
# image byte-identical to the reference. Same input, same output,
# different virtual machine - so a stage that is fast because it is
# quietly wrong is caught by the same run that times it. A timing for a
# stage whose output differs is not reported at all.
#
# METHOD. One process per repetition, so startup and image load are
# included; measured separately below and subtracted in the report,
# because at ~1.2 ms against ~50 ms they would otherwise compress every
# ratio by a couple of percent. Repetitions are interleaved rather than
# run back to back per stage, so a drifting machine perturbs all stages
# alike instead of penalising whichever went last.
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
REPS=${2:-15}

STAGES="s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec s6-cv8b"
WIDTH=${WIDTH:-64}

# The cross-compiler's TARGET cell width is a source constant in cross.4,
# not a runtime option - see the README, and cross.4's own comment for
# why a top-level IF/THEN there corrupted the dictionary. So a 32-bit
# run needs a retargeted copy. Either way the engine WRITES kernel.img,
# so both committed images are saved and restored around the run.
if [ "$WIDTH" = 32 ]; then
    sed '22s/^8 TARGET-CELL-BYTES !/4 TARGET-CELL-BYTES !/' \
        "$ROOT/forth/cross.4" > "$W/cross32.4"
    XCSRC=cross32.4
    REFSRC=$W/kernel32.img
else
    XCSRC=cross.4
    REFSRC=$W/kernel.img
fi
REF=$O/.kernel-ref.img
cp "$REFSRC" "$REF"
SAVE64=$O/.save-kernel64.img
cp "$W/kernel.img" "$SAVE64"
restore() { cp "$SAVE64" "$W/kernel.img"; }
trap restore EXIT INT TERM
printf 'S" extend.4" INCLUDED\nS" %s" INCLUDED\n' "$XCSRC" > "$O/.xc.fth"
printf 'BYE\n' > "$O/.nul.fth"

eng() { echo "$O/$1-$WIDTH"; }
img() { echo "$O/$1-s$WIDTH.img"; }

# ---- correctness gate ------------------------------------------------
echo "verifying every stage reproduces the reference kernel..."
ok=""
for s in $STAGES; do
    e=$(eng "$s"); i=$(img "$s")
    if [ ! -x "$e" ] || [ ! -r "$i" ]; then
        printf '  %-12s SKIP (not built)\n' "$s"; continue
    fi
    ( cd "$W" && timeout 120 "$e" "$i" < "$O/.xc.fth" >/dev/null 2>&1 )
    st=$?
    if [ $st -ne 0 ]; then
        printf '  %-12s EXCLUDED: cross-compile exited %s\n' "$s" "$st"
    elif cmp -s "$W/kernel.img" "$REF"; then
        printf '  %-12s ok\n' "$s"; ok="$ok $s"
    else
        printf '  %-12s EXCLUDED: kernel image differs from reference\n' "$s"
    fi
    cp "$SAVE64" "$W/kernel.img"
done
echo

# ---- fixed overhead --------------------------------------------------
# A run that loads the image and exits, so the compile figures can be
# reported net of process startup.
declare -A OVER
for s in $ok; do
    e=$(eng "$s"); i=$(img "$s")
    t0=$(date +%s%N)
    for _ in $(seq 20); do ( cd "$W" && "$e" "$i" < "$O/.nul.fth" >/dev/null 2>&1 ); done
    t1=$(date +%s%N)
    OVER[$s]=$(( (t1 - t0) / 20 ))
done

# ---- interleaved timing ----------------------------------------------
declare -A BEST
for s in $ok; do BEST[$s]=0; done
echo "timing, $REPS interleaved repetitions..."
for r in $(seq "$REPS"); do
    for s in $ok; do
        e=$(eng "$s"); i=$(img "$s")
        t0=$(date +%s%N)
        ( cd "$W" && "$e" "$i" < "$O/.xc.fth" >/dev/null 2>&1 )
        t1=$(date +%s%N)
        cp "$SAVE64" "$W/kernel.img"
        d=$(( t1 - t0 ))
        if [ "${BEST[$s]}" -eq 0 ] || [ "$d" -lt "${BEST[$s]}" ]; then BEST[$s]=$d; fi
    done
done
echo

# ---- report ----------------------------------------------------------
# The minimum, not the mean: every source of noise on a shared machine
# adds time, so the fastest run is the one least contaminated. The mean
# would mostly measure the neighbours.
base=""
printf '%-12s %10s %10s %8s\n' stage "ms" "net ms" "vs cell"
for s in $ok; do
    net=$(( BEST[$s] - OVER[$s] ))
    [ -z "$base" ] && base=$net
    printf '%-12s %10.2f %10.2f %8.3f\n' "$s" \
        "$(echo "${BEST[$s]}/1000000" | bc -l)" \
        "$(echo "$net/1000000" | bc -l)" \
        "$(echo "$net/$base" | bc -l)"
done
echo
echo "cell width $WIDTH, $REPS reps, minimum of run; overhead subtracted"
