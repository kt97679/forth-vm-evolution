#!/bin/bash
# run-tests.sh [BUILDDIR] - run the shared ANS CORE corpus on every stage.
#
# WHY THIS IS SHAPED THIS WAY. A suite that reports "0 failures" because
# the engine died on line 9 is worse than no suite: that exact thing
# happened in the parent project and went unnoticed for several
# iterations. Absence of error text is never treated as success here.
#
# A stage passes only if ALL of:
#   * the engine exits 0 - no segfault, no timeout;
#   * the end-of-corpus sentinel is printed, proving the whole file was
#     interpreted rather than abandoned somewhere in the middle;
#   * no case reported INCORRECT RESULT / WRONG NUMBER OF RESULTS and no
#     word was undefined;
#   * and the NEGATIVE CONTROL run - the same corpus with one deliberately
#     wrong case appended - is detected as failing. If the control passes,
#     the harness cannot distinguish right from wrong on this stage and
#     its "ok" would be worthless, so it is reported as BROKEN.
#
# The images tested are the SELF-HOSTING ones (-s*): the corpus
# compiles hundreds of definitions at run time, so a run-only image
# cannot take part.
#
# Stages with no self-hosting compiler cannot run a corpus that compiles
# definitions at run time. Those are declared xfail below and reported
# as such: expected, and not counted as a regression. Each one becomes a
# real pass when its emitter overlay lands.
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
CORPUS=$ROOT/tests/corpus/core.fth
[ -r "$CORPUS" ] || { echo "missing corpus: $CORPUS"; exit 1; }

SENTINEL=CORPUS-REACHED-END
CASES=$(grep -cE '^[[:space:]]*\{' "$CORPUS")

# `.(` is not in every kernel here, so the sentinel uses S" and TYPE.
GOOD=$O/.corpus-good.fth
BAD=$O/.corpus-bad.fth
{ cat "$CORPUS"; printf '\nS" %s" TYPE CR\nBYE\n' "$SENTINEL"; } > "$GOOD"
{ cat "$CORPUS"; printf '\n{ 1 2 + -> 4 }\nS" %s" TYPE CR\nBYE\n' "$SENTINEL"; } > "$BAD"

# The report format is "<message>: <the offending source line>", so a
# real failure is always followed by the test case's opening brace. The
# looser pattern also matched tester.fr's OWN definition of ERROR when an
# engine echoes its input, which SOD32 does - two phantom failures.
ERRS='INCORRECT RESULT: \{|WRONG NUMBER OF RESULTS: \{|Undefined word'

# Stages whose image has no compiler for its own encoding yet.
XFAIL=" "

rc=0
one() { # one INFILE ENGINE IMAGE WORKDIR -> prints "status|detail"
    local inf=$1 eng=$2 img=$3 wd=$4 st out
    ( cd "$wd" && timeout 15 "$eng" "$img" < "$inf" > "$O/.t.out" 2>/dev/null )
    st=$?
    out=$(tr -d '\r' < "$O/.t.out")
    [ $st -ne 0 ] && { echo "died|engine exited $st"; return; }
    printf '%s' "$out" | grep -q "$SENTINEL" || { echo "short|stopped before end of corpus"; return; }
    echo "ran|$(printf '%s' "$out" | grep -cE "$ERRS")"
}

run() { # run LABEL ENGINE IMAGE [WORKDIR]
    local label=$1 eng=$2 img=$3 wd=${4:-$W} g b gs gd bs bd xf=0
    case "$XFAIL" in *" $label "*) xf=1;; esac
    if [ ! -x "$eng" ] || [ ! -r "$img" ]; then
        printf '  %-12s SKIP   not built\n' "$label"; return
    fi
    g=$(one "$GOOD" "$eng" "$img" "$wd"); gs=${g%%|*}; gd=${g#*|}
    if [ "$gs" != ran ]; then
        if [ $xf -eq 1 ]; then
            printf '  %-12s xfail  %s (no compiler for this encoding yet)\n' "$label" "$gd"
        else
            printf '  %-12s FAIL   %s\n' "$label" "$gd"; rc=1
        fi
        return
    fi
    if [ "$gd" -ne 0 ]; then
        printf '  %-12s FAIL   %s bad cases\n' "$label" "$gd"
        grep -aE "$ERRS" "$O/.t.out" | head -4 | sed 's/^/       /'
        rc=1; return
    fi
    # negative control
    b=$(one "$BAD" "$eng" "$img" "$wd"); bs=${b%%|*}; bd=${b#*|}
    if [ "$bs" != ran ] || [ "$bd" -lt 1 ]; then
        printf '  %-12s BROKEN the deliberately wrong case was not detected\n' "$label"
        rc=1; return
    fi
    if [ $xf -eq 1 ]; then
        printf '  %-12s XPASS  %s cases (expected no compiler - update XFAIL)\n' "$label" "$CASES"
    else
        printf '  %-12s ok     %s cases\n' "$label" "$CASES"
    fi
}

echo "ANS CORE corpus: $CASES cases, plus a negative control per stage"
echo
echo "64-bit cells:"
run s0-cell    "$O/s0-cell-64"    "$O/s0-cell-s64.img"
run p4-pack4   "$O/p4-pack4-64"   "$O/p4-pack4-s64.img"
run p8-pack8   "$O/p8-pack8-64"   "$O/p8-pack8-s64.img"
run s1-sod16   "$O/s1-sod16-64"   "$O/s1-sod16-s64.img"
run s2-cpt16   "$O/s2-cpt16-64"   "$O/s2-cpt16-s64.img"
run s3-cpt16f  "$O/s3-cpt16f-64"  "$O/s3-cpt16f-s64.img"
run s4-cv8     "$O/s4-cv8-64"     "$O/s4-cv8-s64.img"
run s5-cv8spec "$O/s5-cv8spec-64" "$O/s5-cv8spec-s64.img"
run s6-cv8b    "$O/s6-cv8b-64"    "$O/s6-cv8b-s64.img"
echo
echo "32-bit cells:"
run s0-cell    "$O/s0-cell-32"    "$O/s0-cell-s32.img"
run p4-pack4   "$O/p4-pack4-32"   "$O/p4-pack4-s32.img"
run p8-pack8   "$O/p8-pack8-32"   "$O/p8-pack8-s32.img"
run s1-sod16   "$O/s1-sod16-32"   "$O/s1-sod16-s32.img"
run s2-cpt16   "$O/s2-cpt16-32"   "$O/s2-cpt16-s32.img"
run s3-cpt16f  "$O/s3-cpt16f-32"  "$O/s3-cpt16f-s32.img"
run s4-cv8     "$O/s4-cv8-32"     "$O/s4-cv8-s32.img"
run s5-cv8spec "$O/s5-cv8spec-32" "$O/s5-cv8spec-s32.img"
run s6-cv8b    "$O/s6-cv8b-32"    "$O/s6-cv8b-s32.img"

if [ -x "$O/sod32/sod32" ]; then
    echo
    echo "SOD32 (upstream, 32-bit):"
    run sod32 "$O/sod32/sod32" "$O/sod32/forth.img" "$O/sod32"
fi

echo
# ---- locals ----------------------------------------------------------
# locals.4 ships in the shell image and redefines `;` and `EXIT`, which
# is intrusive enough to deserve a check. tests/core/locals.fth existed
# for it and nothing ran it - an unrun test being exactly the thing this
# project says is worse than none. It runs on the cell engine, which is
# the one that carries the compiler locals.4 patches.
echo
echo "locals (locals.4, on the cell engine):"
for w in 64 32; do
    e=$O/s0-cell-$w; i=$([ "$w" = 64 ] && echo kernel.img || echo kernel32.img)
    if [ ! -x "$e" ]; then printf '  %-12s SKIP   not built\n' "$w-bit"; continue; fi
    cp "$W/$i" "$O/.locals-save.img"
    printf 'S" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" %s/tests/core/tester.fr" INCLUDED\nS" %s/tests/core/locals.fth" INCLUDED\nS" LOCALS-DONE" TYPE CR\nBYE\n' \
        "$ROOT" "$ROOT" > "$O/.locals.fth"
    ( cd "$W" && timeout 120 "$e" "$i" < "$O/.locals.fth" > "$O/.locals.out" 2>&1 )
    cp "$O/.locals-save.img" "$W/$i"
    if ! grep -aq LOCALS-DONE "$O/.locals.out"; then
        printf '  %-12s FAIL   did not finish\n' "$w-bit"; FAILED=1
    elif grep -aqE 'INCORRECT RESULT|WRONG NUMBER' "$O/.locals.out"; then
        printf '  %-12s FAIL   %s bad cases\n' "$w-bit" \
            "$(grep -acE 'INCORRECT RESULT|WRONG NUMBER' "$O/.locals.out")"; FAILED=1
    else
        printf '  %-12s ok\n' "$w-bit"
    fi
done

[ "${FAILED:-0}" = 0 ] || rc=1
[ $rc -eq 0 ] && echo "PASS - no regressions" || echo "FAIL - see above"
exit $rc
