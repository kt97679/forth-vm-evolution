#!/bin/bash
# layout-noise.sh [BUILDDIR] [REPS] - how much does an engine's speed
# move when NOTHING about it changes except where the code lands?
#
# WHY THIS MATTERS MORE THAN IT SOUNDS. Several differences in
# RESULTS.md are small - a few percent between neighbouring stages. The
# parent project recorded that code layout alone moved an engine by
# 4-5%, and that one engine got 8% faster by containing handlers it
# never executed. If that holds here, those differences are noise
# wearing a number, and the article must not read meaning into them.
#
# METHOD. Build the SAME engine source several times, varying only flags
# that change where code lands and nothing about what it does, then run
# the identical workload on each, interleaved. Every variant is the same
# program: same semantics, same image, same input. Whatever spread shows
# up is the floor below which no comparison in this repository means
# anything.
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
# 40, not the handful the other harnesses use. At 6 reps two runs of this
# script reported 5.3% and 11.2% and disagreed about WHICH build was
# fastest - the measurement was reading machine variance rather than
# layout. At 40 it settles to about 5% and stays there.
REPS=${2:-40}
L=$O/layout-noise
mkdir -p "$L"

HOT='+,=,!,@,LSHIFT,RSHIFT,C@,C!,AND,OR,XOR,LIT,<,U<,OVER,DROP,DUP,SWAP,ROT,>R,R>,R@,NEGATE'
python3 tools/gen-tos.py "$O/vm-lab.c" > "$L/vm-lab-tos.c"
python3 tools/gen-fold.py "$L/vm-lab-tos.c" "$HOT" v8 > /dev/null
# Which cell width exists here is not a constant: a 32-bit host has no
# 8-byte column at all. Pick the image that was actually built and the
# call scale that goes with it.
if [ -r "$O/s5-cv8spec-s64.img" ]; then
    IMG=$O/s5-cv8spec-s64.img; SCALE=3; M=
elif [ -r "$O/s5-cv8spec-s32.img" ]; then
    IMG=$O/s5-cv8spec-s32.img; SCALE=2; M=$( [ "$(printf '%s' "$(getconf LONG_BIT 2>/dev/null)")" = 64 ] && echo "-m32 -fno-pie -no-pie" )
else
    echo "no s5-cv8spec self-hosting image in $O - run tools/build-stages.sh"; exit 1
fi
BASE="$M -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=$SCALE -DSPEC=1 -DSHAREDCALL=1"

# Semantically neutral, layout-changing. Nothing here alters what the
# engine computes; -falign-* only moves code, and the dead function is
# never called.
cat > "$L/dead.h" <<'EOF'
/* Never called. Present only to move everything after it. */
static int layout_padding_never_called(int x) { return x * 3 + 1; }
EOF

variants() {
    echo "v-align16 -falign-functions=16 -falign-loops=16"
    echo "v-align32 -falign-functions=32 -falign-loops=32"
    echo "v-align64 -falign-functions=64 -falign-loops=64"
    echo "v-plain "
    echo "v-jumps -fno-align-jumps"
}

echo "building variants of one engine, identical semantics ..."
names=""
while read -r nm flags; do
    cc $BASE $flags -I"$L" -o "$L/$nm" "$L/vm-lab-tos.c" 2>/dev/null || {
        echo "  $nm FAILED to build"; continue; }
    names="$names $nm"
    printf '  %-10s %8s bytes of text\n' "$nm" \
        "$(size "$L/$nm" 2>/dev/null | awk 'NR==2{print $1}')"
done < <(variants)

# The cross-compiler's TARGET cell width is a source constant, so a
# 4-byte run needs a retargeted copy and a different reference image -
# the same dance kernel-compile.sh does. Either way the engine WRITES
# kernel.img, so the committed one is saved and restored around the run.
if [ "$SCALE" = 2 ]; then
    sed '22s/^8 TARGET-CELL-BYTES !/4 TARGET-CELL-BYTES !/' \
        "$ROOT/forth/cross.4" > "$W/cross32.4"
    XCSRC=cross32.4; REFSRC=$W/kernel32.img
else
    XCSRC=cross.4;   REFSRC=$W/kernel.img
fi
REF=$L/ref.img
cp "$REFSRC" "$REF"
SAVEK=$L/save-kernel.img
cp "$W/kernel.img" "$SAVEK"
trap 'cp "$SAVEK" "$W/kernel.img"' EXIT INT TERM
printf 'S" extend.4" INCLUDED\nS" %s" INCLUDED\n' "$XCSRC" > "$L/xc.fth"

# Correctness first, exactly as the real harnesses do: every variant must
# produce the reference kernel byte for byte.
ok=""
for n in $names; do
    # The exit status matters as much as the comparison. An engine that
    # dies on startup leaves kernel.img untouched, so it is byte-identical
    # to the reference and the comparison PASSES - which is how a broken
    # 32-bit configuration once reported a tidy 1.9% spread over five
    # builds that had each run for two milliseconds and done nothing.
    ( cd "$W" && timeout 120 "$L/$n" "$IMG" < "$L/xc.fth" >/dev/null 2>&1 )
    st=$?
    if [ $st -ne 0 ]; then echo "  $n EXCLUDED: exited $st"
    elif cmp -s "$W/kernel.img" "$REF"; then ok="$ok $n"
    else echo "  $n EXCLUDED: output differs"; fi
    cp "$SAVEK" "$W/kernel.img"
done

declare -A BEST
for n in $ok; do BEST[$n]=0; done
echo "timing, $REPS interleaved repetitions ..."
for _ in $(seq "$REPS"); do
    for n in $ok; do
        t0=$(date +%s%N)
        ( cd "$W" && "$L/$n" "$IMG" < "$L/xc.fth" >/dev/null 2>&1 )
        t1=$(date +%s%N)
        cp "$SAVEK" "$W/kernel.img"
        d=$(( t1 - t0 ))
        if [ "${BEST[$n]}" -eq 0 ] || [ "$d" -lt "${BEST[$n]}" ]; then BEST[$n]=$d; fi
    done
done

echo
lo=0; hi=0
for n in $ok; do
    v=${BEST[$n]}
    [ $lo -eq 0 ] || [ $v -lt $lo ] && lo=$v
    [ $v -gt $hi ] && hi=$v
done
printf '%-12s %10s %8s\n' variant ms "vs best"
for n in $ok; do
    printf '%-12s %10.2f %8.3f\n' "$n" \
        "$(echo "${BEST[$n]}/1000000" | bc -l)" \
        "$(echo "${BEST[$n]}/$lo" | bc -l)"
done
echo
echo "spread across builds of the SAME engine: $(echo "($hi-$lo)*100/$lo" | bc -l | cut -c1-5)%"
echo "no comparison in RESULTS.md smaller than this means anything."
echo
echo "Which variant wins is NOT stable between runs of this script; the"
echo "spread is a band, not a ranking. Do not read it as -falign-functions"
echo "having an effect worth choosing."
