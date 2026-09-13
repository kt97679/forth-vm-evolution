#!/bin/bash
# kernel-compile.sh [BUILDDIR] [REPS] - the headline benchmark.
#
# WHAT IT MEASURES. Each stage cross-compiles kernel.4 and writes a new
# kernel image: the system's own self-hosting work. It exercises the
# interpreter, the compiler, the dictionary and the string code rather
# than one idiom, and it cannot be accused of favouring an encoding,
# because the encoding it EMITS is the cell format in every case.
#
# WHY IT IS ALSO A CORRECTNESS CHECK. Every stage must produce an image
# byte-identical to the reference before it is timed at all. Same input,
# same output, different VM - so a stage that is fast because it is
# quietly wrong is caught by the run that measures it.
#
# HOW IT HANDLES VARIABILITY. Two different problems, two mechanisms.
#
#   Run-to-run noise only ever ADDS time, so the minimum of several
#   repetitions is the least contaminated sample, and repetitions are
#   interleaved across binaries so drift hits everything alike.
#
#   Per-BUILD bias is the larger effect and repetitions cannot touch it.
#   Where the compiler places code is worth several percent and is FIXED
#   for a given binary, so measuring harder just measures the bias more
#   precisely. Three runs of the same binaries agree to about 1%; but
#   rebuild the tree and a stage moves by five or ten, and
#   tools/layout-noise.sh puts the spread between five semantically
#   identical builds at 2.5% to 17% depending on the workload.
#
#   So when the tree was built with LAYOUTS>1, every layout variant of
#   every stage is timed and the MEDIAN across variants is reported, with
#   the spread beside it. That turns a hidden constant into a measured
#   distribution - the argument of Mytkowicz et al., "Producing Wrong
#   Data Without Doing Anything Obviously Wrong!" (ASPLOS 2009).
set -u

# Every engine here is a measured subject, so it runs in a predictable
# environment rather than in whatever the caller exported.
unset LD_PRELOAD

cd "$(dirname "$0")/.."
ROOT=$PWD
O=${1:-$ROOT/build}
O=$(cd "$O" && pwd)
W=$O/work
REPS=${2:-6}
WIDTH=${WIDTH:-64}

STAGES="s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec s6-cv8b"

# Pin to one CPU where possible: a migration costs a cold cache and
# shows up as a slow repetition.
PIN=""
command -v taskset >/dev/null 2>&1 && PIN="taskset -c 0"

# The cross-compiler's TARGET cell width is a source constant, so a
# 32-bit run needs a retargeted copy. Either way the engine WRITES
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
printf 'S" extend.4" INCLUDED\nS" %s" INCLUDED\n' "$XCSRC" > "$O/.xc.fth"
printf 'BYE\n' > "$O/.nul.fth"

# ---- which binaries exist --------------------------------------------
RUNNERS=""
for s in $STAGES; do
    for e in "$O/$s-$WIDTH" "$O/$s-$WIDTH"-v*; do
        [ -x "$e" ] && [ -r "$O/$s-s$WIDTH.img" ] || continue
        RUNNERS="$RUNNERS $s:$e"
    done
done

echo "verifying every stage reproduces the reference kernel..."
ok=""
for r in $RUNNERS; do
    s=${r%%:*}; e=${r#*:}
    ( cd "$W" && timeout 120 $PIN "$e" "$O/$s-s$WIDTH.img" < "$O/.xc.fth" \
        >/dev/null 2>&1 )
    st=$?
    if [ $st -ne 0 ]; then
        printf '  %-12s %-24s EXCLUDED: exited %s\n' "$s" "$(basename "$e")" "$st"
    elif cmp -s "$W/kernel.img" "$REF"; then
        ok="$ok $r"
        [ "$e" = "$O/$s-$WIDTH" ] && printf '  %-12s ok\n' "$s"
    else
        printf '  %-12s %-24s EXCLUDED: image differs\n' "$s" "$(basename "$e")"
    fi
    cp "$SAVE" "$W/kernel.img"
done
echo

# ---- fixed overhead, per binary --------------------------------------
declare -A OVER BEST
for r in $ok; do
    s=${r%%:*}; e=${r#*:}
    t0=$(date +%s%N)
    for _ in $(seq 10); do
        ( cd "$W" && $PIN "$e" "$O/$s-s$WIDTH.img" < "$O/.nul.fth" >/dev/null 2>&1 )
    done
    t1=$(date +%s%N)
    OVER[$r]=$(( (t1 - t0) / 10 ))
    BEST[$r]=0
done

# ---- timing ----------------------------------------------------------
nvar=$(echo $ok | wc -w)
echo "timing, $REPS rounds over $nvar binaries ..."
for _ in $(seq "$REPS"); do
    for r in $ok; do
        s=${r%%:*}; e=${r#*:}
        t0=$(date +%s%N)
        ( cd "$W" && $PIN "$e" "$O/$s-s$WIDTH.img" < "$O/.xc.fth" >/dev/null 2>&1 )
        t1=$(date +%s%N)
        cp "$SAVE" "$W/kernel.img"
        d=$(( t1 - t0 - OVER[$r] ))
        if [ "${BEST[$r]}" -eq 0 ] || [ "$d" -lt "${BEST[$r]}" ]; then BEST[$r]=$d; fi
    done
done
echo

# ---- report ----------------------------------------------------------
{ for r in $ok; do echo "${r%%:*} ${BEST[$r]}"; done; } > "$O/.kc.dat"
python3 - "$O/.kc.dat" "$WIDTH" "$REPS" <<'PY'
import sys, collections
rows = collections.defaultdict(list)
for line in open(sys.argv[1]):
    st, ns = line.split()
    rows[st].append(int(ns))
order = ["s0-cell", "p4-pack4", "p8-pack8", "s1-sod16", "s2-cpt16",
         "s3-cpt16f", "s4-cv8", "s5-cv8spec", "s6-cv8b"]


def stats(v):
    """Mean across layout variants, and the standard error of that mean.

    The MEAN, not the median: layout effects are roughly symmetric and
    the mean of n has standard error sd/sqrt(n), where the median of a
    small n is noticeably less efficient. Measured here, a median of
    five moved 6-9% between runs where the mean moves 2-3%.

    The standard error is the number that matters. A single build gives
    a figure that repeats to 1% and is wrong by up to 12%, because every
    repetition shares the same bias; this gives a figure whose stated
    uncertainty includes the bias."""
    n = len(v)
    m = sum(v) / float(n)
    if n < 2:
        return m, None
    var = sum((x - m) ** 2 for x in v) / (n - 1)
    return m, (var ** 0.5) / (n ** 0.5)


base, base_se = stats(rows["s0-cell"]) if "s0-cell" in rows else (None, None)
nv = max((len(v) for v in rows.values()), default=0)
print("%-12s %10s %10s %12s" % ("stage", "ms", "vs cell", "+/- (1 SE)"))
for st in order:
    if st not in rows:
        continue
    m, se = stats(rows[st])
    ratio = m / base if base else 0.0
    if se is not None and base_se:
        # ratio of two means, errors combined in quadrature
        rel = ((se / m) ** 2 + (base_se / base) ** 2) ** 0.5
        err = "%.3f" % (ratio * rel)
    else:
        err = "1 build"
    print("%-12s %10.2f %10.3f %12s" % (st, m / 1e6, ratio, err))
print()
print("mean over %d layout variant(s), each the minimum of %s rounds;"
      % (nv, sys.argv[3]))
print("startup subtracted per binary; cell width %s." % sys.argv[2])
print("The +/- is one standard error of the ratio and is dominated by")
print("per-build layout bias, not by run-to-run noise.")
if nv == 1:
    print()
    print("Only one build per stage. The per-build layout bias is larger")
    print("than the run-to-run noise and is invisible here: rebuild with")
    print("LAYOUTS=5 to measure it.")
PY
