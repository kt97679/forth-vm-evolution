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
        # Iteration 125: a stage missing where its cell width WAS built is a
        # failed build, not a skip - a build that stopped half way passed here.
        case $eng in *-64) w_=64 ;; *-32) w_=32 ;; *) w_= ;; esac
        if [ -n "$w_" ] && [ -x "$O/s0-cell-$w_" ]; then
            printf '  %-12s FAIL   not built, though the %s-bit build ran\n' "$label" "$w_"; rc=1
        else printf '  %-12s SKIP   not built\n' "$label"; fi
        return
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
    # Iteration 127: upstream SOD32, the ancestor, keeps the +LOOP rule this
    # project fixed in Iteration 125 - so it fails exactly the corpus's seven
    # Haley cases (GD8, GD9), checked to be those and no others.
    kn=0; [ "$label" = sod32 ] && kn=7
    if [ "$gd" -ne "$kn" ] || { [ "$kn" -gt 0 ] && [ "$(grep -aE "$ERRS" "$O/.t.out" | grep -cE 'GD8|GD9')" -ne "$kn" ]; }; then
        printf '  %-12s FAIL   %s bad cases\n' "$label" "$gd"
        grep -aE "$ERRS" "$O/.t.out" | head -4 | sed 's/^/       /'
        rc=1; return
    fi
    # negative control
    b=$(one "$BAD" "$eng" "$img" "$wd"); bs=${b%%|*}; bd=${b#*|}
    if [ "$bs" != ran ] || [ "$bd" -le "$kn" ]; then
        printf '  %-12s BROKEN the deliberately wrong case was not detected\n' "$label"
        rc=1; return
    fi
    if [ $xf -eq 1 ]; then
        printf '  %-12s XPASS  %s cases (expected no compiler - update XFAIL)\n' "$label" "$CASES"
    else
        printf '  %-12s ok     %s cases%s\n' "$label" "$CASES" "$([ "$kn" -gt 0 ] && echo "; the $kn +LOOP cases fail, as expected of the ancestor")"
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
run s7-spn     "$O/s7-spn-64"     "$O/s7-spn-s64.img"
run s7-full    "$O/s7-full-64"    "$O/s7-full-s64.img"
run s8-spncv8  "$O/s8-spncv8-64"  "$O/s8-spncv8-s64.img"
run s8-full    "$O/s8-full-64"    "$O/s8-full-s64.img"
run s8-lazy    "$O/s8-lazy-64"    "$O/s8-lazy-s64.img"
run relf       "$O/relf-64"       "$O/relf-s64.img"
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
run relf       "$O/relf-32"       "$O/relf-s32.img"

if [ -x "$O/sod32/sod32" ]; then
    echo
    echo "SOD32 (upstream, 32-bit):"
    run sod32 "$O/sod32/sod32" "$O/sod32/forth.img" "$O/sod32"
fi

echo
# ---- SYSCALL's shell and ?DO/LEAVE in extensions (the after-seed-39 batch) --
echo
echo "?DO and LEAVE in extensions (tools/test-ext-loops.sh):"
if sh tools/test-ext-loops.sh > "$O/.extl.log" 2>&1; then printf '  %-12s ok     %s\n' ext-loops "$(grep -c '^ok' "$O/.extl.log") stages"
else printf '  %-12s FAIL   %s\n' ext-loops "$(grep '^FAIL' "$O/.extl.log" | head -2 | tr '\n' ' ')"; FAILED=1; fi

# ---- the shell suite ---------------------------------------------------
# tests/shell: the parent project's shell suite, removed in 5c87022 as unrun
# and restored in Iteration 134 (two tests' assumptions fixed: HOME=/root,
# the parent's file layout). Every file, through a shell that boots into
# MAIN: the cell stage's and s5's (CV8 - s6 is not built with a shell).
# The negative control is a "shell" that ignores its command - the suite
# must fail on it, or it is not checking what the shell does.
echo
echo "the shell suite (tests/shell, every file):"
SHT=$(mktemp -d); trap 'rm -rf "$SHT"' EXIT
mksh() { # mksh NAME ENGINE IMAGE: a wrapper the suite runs as $THIS_SH
    printf '#!/bin/sh\nexec "%s" "%s" "$@"\n' "$2" "$3" > "$SHT/$1"; chmod +x "$SHT/$1"
}
shsuite() { # shsuite LABEL WRAPPER: the suite's own verdict, its exit status
    THIS_SH="$SHT/$2" sh tests/shell/run-all > "$SHT/$2.log" 2>&1
}
if [ -x "$O/s0-cell-64" ] && [ -s "$O/work/s0-cell-64.img" ]; then
    mksh s0 "$O/s0-cell-64" "$O/work/s0-cell-64.img"
    [ -x "$O/s5-cv8spec-64" ] && [ -s "$O/s5-cv8spec-64.img" ] && mksh s5 "$O/s5-cv8spec-64" "$O/s5-cv8spec-64.img"
    # Iteration 147: every shell is SYSCALL's, so the 4-byte ones too (i386's numbers mapped)
    sw="s0 s5"
    if [ -x "$O/s0-cell-32" ] && [ -s "$O/s0-cell-32.img" ]; then
        mksh s0-32 "$O/s0-cell-32" "$O/s0-cell-32.img"; sw="$sw s0-32"
        [ -x "$O/s5-cv8spec-32" ] && [ -s "$O/s5-cv8spec-32.img" ] && mksh s5-32 "$O/s5-cv8spec-32" "$O/s5-cv8spec-32.img" && sw="$sw s5-32"
    fi
    for w in $sw; do
        if [ ! -x "$SHT/$w" ]; then printf '  %-12s FAIL   no shell image\n' "$w"; FAILED=1; continue; fi
        if shsuite "$w" "$w"; then printf '  %-12s ok     %s assertions\n' "$w" "$(grep -o '^[0-9]* assertions' "$SHT/$w.log" | awk '{s+=$1} END {print s}')"
        else printf '  %-12s FAIL   %s\n' "$w" "$(grep '^FAIL' "$SHT/$w.log" | head -3 | tr '\n' ' ')"; FAILED=1; fi
    done
    printf '#!/bin/sh\nexec "%s" "%s" -c "echo CONTROL"\n' "$O/s0-cell-64" "$O/work/s0-cell-64.img" > "$SHT/control"; chmod +x "$SHT/control"
    if shsuite control control; then printf '  %-12s FAIL   a shell ignoring its commands passed the suite\n' control; FAILED=1
    else printf '  %-12s ok     a shell ignoring its commands fails it (%s assertions)\n' control "$(grep -c '^FAIL' "$SHT/control.log")"; fi
else
    printf '  %-12s FAIL   the cell stage or its shell image was not built\n' s0; FAILED=1
fi

# The stages built at a cell width: SPN's native code is x86-64, so s7 and
# s8 exist at 8 bytes only - as the corpus section above lists them. Iteration
# 129: the two sections below listed them at both widths; on the laptop, which
# builds the 4-byte half, that failed the suite before seed 38 (this VM, not
# building it, never saw the half - prompts/08).
stages_for() {
    echo s0-cell p4-pack4 p8-pack8 s1-sod16 s2-cpt16 s3-cpt16f s4-cv8 s5-cv8spec s6-cv8b
    [ "$1" = 64 ] && echo s7-spn s7-full s8-spncv8 s8-full s8-lazy
    echo relf
}

# ---- tabs (Iteration 145) ------------------------------------------------
# No tab is made a space any more: SKIP and SCAN - and the C operations that
# stand in for them - take any control character for a space delimiter.
# tests/core/tabs.fth: tabs between words and at a line's start, in a
# definition, in a string (kept: 9, not 32), in an EVALUATEd string, before
# CHAR and a comment. Every stage at every width built; the negative
# control is the file with its tabs made X, which must not give the answers.
echo
echo "tabs (tests/core/tabs.fth):"
TABS_WANT='3 |25 |3 |9 |56 |65 |1 |'
for w in 64 32; do
    [ -x "$O/s0-cell-$w" ] || continue
    bad=""; n=0
    for st in $(stages_for $w); do
        e="$O/$st-$w"; i="$O/$st-s$w.img"; [ "$st" = relf ] && continue
        case "$st" in s7-*|s8-*) e="$O/$st-64"; i="$W/$st-s64.img" ;; esac
        [ -x "$e" ] && [ -s "$i" ] || continue
        got=$( (cd "$W" && timeout 15 "$e" "$i" < "$ROOT/tests/core/tabs.fth" 2>&1) | tr -d '\r' | grep -E '^[0-9]+ $' | tr '\n' '|')
        n=$((n + 1)); [ "$got" = "$TABS_WANT" ] || bad="$bad $st"
    done
    [ "$n" -gt 0 ] || bad=" (no stage tested)"
    if [ -n "$bad" ]; then printf '  %-12s FAIL  %s\n' "$w-bit" "$bad"; FAILED=1
    else printf '  %-12s ok     %s stages\n' "$w-bit" "$n"; fi
done
CTRL=$(mktemp); tr '\t' 'X' < "$ROOT/tests/core/tabs.fth" > "$CTRL"
got=$( (cd "$W" && timeout 15 "$O/s0-cell-64" "$O/s0-cell-s64.img" < "$CTRL" 2>&1) | tr -d '\r' | grep -E '^[0-9]+ $' | tr '\n' '|'); rm -f "$CTRL"
if [ "$got" = "$TABS_WANT" ]; then printf '  %-12s FAIL   the file without tabs gave the answers too\n' control; FAILED=1
else printf '  %-12s ok     the file without tabs does not give them\n' control; fi

# tests/core/audit.fth (Iteration 156): the words the audit rewrote - CMOVE and
# CMOVE> by D+ with overlaps both ways and lengths 0 and 1, FILL by 1 -1 D+ with
# a sentinel, MOVE, 2SWAP, 2!, WORD's trailing space, and INTERPRET's stack check
# where the stack can change (a definition compiled over values, an underflow
# that ends its line). The answers the kernel gave before the audit. The negative
# control swaps CMOVE> for CMOVE, which an overlap must tell apart.
echo
echo "the audit's words (tests/core/audit.fth):"
AUDIT_WANT='104 |97 |103 97 |104 104 |98 104 |101 97 0 |97 102 |101 98 |42 42 0 |43 98 |102 97 |99 104 |2143 |7 5 75 |5 32 |7 2 1 |6 0 |'
for w in 64 32; do
    [ -x "$O/s0-cell-$w" ] || continue
    bad=""; n=0
    for st in $(stages_for $w); do
        e="$O/$st-$w"; i="$O/$st-s$w.img"; [ "$st" = relf ] && continue
        case "$st" in s7-*|s8-*) e="$O/$st-64"; i="$W/$st-s64.img" ;; esac
        [ -x "$e" ] && [ -s "$i" ] || continue
        got=$( (cd "$W" && timeout 15 "$e" "$i" < "$ROOT/tests/core/audit.fth" 2>&1) | tr -d '\r' | grep -E '^[0-9 ]+ $' | tr '\n' '|')
        n=$((n + 1)); [ "$got" = "$AUDIT_WANT" ] || bad="$bad $st"
    done
    [ "$n" -gt 0 ] || bad=" (no stage tested)"
    if [ -n "$bad" ]; then printf '  %-12s FAIL  %s\n' "$w-bit" "$bad"; FAILED=1
    else printf '  %-12s ok     %s stages\n' "$w-bit" "$n"; fi
done
CTRL=$(mktemp); sed 's/CMOVE>/CMOVE/g' "$ROOT/tests/core/audit.fth" > "$CTRL"
got=$( (cd "$W" && timeout 15 "$O/s0-cell-64" "$O/s0-cell-s64.img" < "$CTRL" 2>&1) | tr -d '\r' | grep -E '^[0-9 ]+ $' | tr '\n' '|'); rm -f "$CTRL"
if [ "$got" = "$AUDIT_WANT" ]; then printf '  %-12s FAIL   CMOVE for CMOVE> gave the answers too\n' control; FAILED=1
else printf '  %-12s ok     CMOVE for CMOVE> does not give them\n' control; fi

# tests/core/far.fth (Iteration 158): code and data past 64 KB, then 8 MB more
# - calls, recursion, DOES>, data, EXECUTE across. tools/farcheck.py: every
# answer right, any missing one refused out loud. Most of the ladder could not
# reach that far and broke instead (crashed, hung, lost words); since Iteration
# 159 each answers or refuses - cv8 and cpt16 refuse, the 1 MB engines hold 16.
# The stages still broken are listed and shown, not hidden: a wrong answer from
# any stage fails, and a listed stage that passes says so. The control: the
# file without its gaps gives every answer on s6, which refuses with them.
echo
echo "far from the image base (tests/core/far.fth):"
FAR_KNOWN=" "      # Iteration 159: none - every stage answers or refuses (keep the mechanism)
for w in 64 32; do
    for st in $(stages_for $w); do
        e="$O/$st-$w"; i="$O/$st-s$w.img"
        [ -x "$e" ] && [ -s "$i" ] || continue
        # 2>&1: a refusal may come on stderr (RelF's "dictionary full")
        out=$( (cd "$W" && timeout 30 "$e" "$i" < "$ROOT/tests/core/far.fth" 2>&1) | tr -d '\000'; exit ${PIPESTATUS[0]} ); c=$?
        v=$(printf '%s' "$out" | python3 "$ROOT/tools/farcheck.py" "$c")
        case "$v" in
            all|refused*) case "$FAR_KNOWN" in *" $st "*) printf '  %-15s ok     %s - listed as broken: take it off FAR_KNOWN\n' "$st-$w" "$v" ;;
                          *) printf '  %-15s ok     %s\n' "$st-$w" "$v" ;; esac ;;
            WRONG*) printf '  %-15s FAIL   %s\n' "$st-$w" "$v"; FAILED=1 ;;
            *) case "$FAR_KNOWN" in *" $st "*) printf '  %-15s known  %s\n' "$st-$w" "$v" ;;
               *) printf '  %-15s FAIL   %s\n' "$st-$w" "$v"; FAILED=1 ;; esac ;;
        esac
    done
done
CTRL=$(mktemp); grep -v '^[0-9]* ALLOT$' "$ROOT/tests/core/far.fth" > "$CTRL"      # no gap: lines 1-9, and 10, 11 rightly absent
v=$( (cd "$W" && timeout 30 "$O/s6-cv8b-64" "$O/s6-cv8b-s64.img" < "$CTRL" 2>/dev/null) | python3 "$ROOT/tools/farcheck.py" 0); rm -f "$CTRL"
if [ "$v" = 'MISSING 2 answers, no refusal' ]; then printf '  %-15s ok     without the gaps s6 gives every answer, and takes no gap\n' control
else printf '  %-15s FAIL   without the gaps s6 gives: %s\n' control "$v"; FAILED=1; fi

# tests/core/paths.fth (Iteration 159, the coverage audit: gcov over this suite
# found handlers no test ran - READ-FILE, RESIZE on every engine; FREE,
# ALLOCATE, WRITE-FILE, SYSCALL on most): memory, the file cycle and a system
# call, on every stage at both widths. The control writes other bytes.
echo
echo "paths no test ran (tests/core/paths.fth):"
PATHS_WANT='0 |0 77 |0 |0 |0 |0 |0 |0 |0 0 13 |0 5 104 111 |0 |0 0 7 |0 4 102 |0 0 |1 |1 0 |'
for w in 64 32; do
    [ -x "$O/s0-cell-$w" ] || continue
    bad=""; n=0
    for st in $(stages_for $w); do
        e="$O/$st-$w"; i="$O/$st-s$w.img"; [ "$st" = relf ] && continue
        case "$st" in s7-*|s8-*) e="$O/$st-64"; i="$W/$st-s64.img" ;; esac
        [ -x "$e" ] && [ -s "$i" ] || continue
        got=$( (cd "$W" && timeout 15 "$e" "$i" < "$ROOT/tests/core/paths.fth" 2>&1) | tr -d '\r' | grep -E '^[0-9 ]+ $' | tr '\n' '|')
        n=$((n + 1)); [ "$got" = "$PATHS_WANT" ] || bad="$bad $st"
    done
    [ "$n" -gt 0 ] || bad=" (no stage tested)"
    if [ -n "$bad" ]; then printf '  %-12s FAIL  %s\n' "$w-bit" "$bad"; FAILED=1
    else printf '  %-12s ok     %s stages\n' "$w-bit" "$n"; fi
done
CTRL=$(mktemp); sed 's/hello, file/hi/' "$ROOT/tests/core/paths.fth" > "$CTRL"
got=$( (cd "$W" && timeout 15 "$O/s0-cell-64" "$O/s0-cell-s64.img" < "$CTRL" 2>&1) | tr -d '\r' | grep -E '^[0-9 ]+ $' | tr '\n' '|'); rm -f "$CTRL"
if [ "$got" = "$PATHS_WANT" ]; then printf '  %-12s FAIL   other bytes gave the answers too\n' control; FAILED=1
else printf '  %-12s ok     other bytes do not give them\n' control; fi

# tests/core/full.fth (Iteration 161): ALLOT past the dictionary's room is
# refused - "dictionary full", HERE unmoved, the system going on. Before, the
# store past the engine's memory crashed (gdb: a byte store past the end) -
# RelF's own kernel already refused. The control allots a little: HERE moves.
echo
echo "the dictionary full (tests/core/full.fth):"
for w in 64 32; do
    [ -x "$O/s0-cell-$w" ] || continue
    bad=""; n=0
    for st in $(stages_for $w); do
        e="$O/$st-$w"; i="$O/$st-s$w.img"
        case "$st" in s7-*|s8-*) e="$O/$st-64"; i="$W/$st-s64.img" ;; esac
        [ -x "$e" ] && [ -s "$i" ] || continue
        out=$( (cd "$W" && timeout 15 "$e" "$i" < "$ROOT/tests/core/full.fth" 2>&1) | tr -d '\r\000'); c=$?
        got=$(printf '%s\n' "$out" | grep -E '^[0-9 ]+ $' | tr '\n' '|')
        n=$((n + 1)); { [ "$got" = '1 |42 |' ] && printf '%s' "$out" | grep -q 'dictionary full'; } || bad="$bad $st"
    done
    [ "$n" -gt 0 ] || bad=" (no stage tested)"
    if [ -n "$bad" ]; then printf '  %-12s FAIL  %s\n' "$w-bit" "$bad"; FAILED=1
    else printf '  %-12s ok     %s stages\n' "$w-bit" "$n"; fi
done
CTRL=$(mktemp); sed 's/^2000000000 ALLOT$/64 ALLOT/' "$ROOT/tests/core/full.fth" > "$CTRL"
got=$( (cd "$W" && timeout 15 "$O/s0-cell-64" "$O/s0-cell-s64.img" < "$CTRL" 2>&1) | tr -d '\r' | grep -E '^[0-9 ]+ $' | tr '\n' '|'); rm -f "$CTRL"
if [ "$got" = '1 |42 |' ]; then printf '  %-12s FAIL   a small ALLOT left HERE where it was\n' control; FAILED=1
else printf '  %-12s ok     a small ALLOT moves HERE\n' control; fi

# The tracer (Iteration 162): vm-lab.c with -DPROFILE=2 keeps a shadow call
# stack and records, the first time each instruction runs, its call path, the
# top three data-stack cells and the input line. The self-test traces
# ": SQ DUP * ; : TWICE SQ SQ ; 3 TWICE": SQ first reached from TWICE, 3 on
# the stack, that line - and a folded call path ending in SQ.
echo
echo "the tracer (tools/vmtrace.py --self-test):"
if out=$(python3 "$ROOT/tools/vmtrace.py" --self-test 2>&1); then printf '  %-12s ok     %s\n' s6 "$(printf '%s' "$out" | tail -1 | cut -c17-110)"
else printf '  %-12s FAIL   %s\n' s6 "$(printf '%s' "$out" | tail -1 | cut -c1-110)"; FAILED=1; fi

# ---- DELETE-FILE -------------------------------------------------------
# Iteration 124: DELETE-FILE segfaulted in every engine of the ladder since
# the baseline - its handler stored unlink's result over the name's address,
# then restored the name's byte at result + length. Nothing ran it: the
# corpus has no file words that delete, and the ANS suites stop before their
# DELETE-FILE tests. Here: a file made, deleted (ior 0), deleted again (ior
# not 0), and a clean exit - on every stage, the stages run counted.
echo
echo "DELETE-FILE (create, delete, delete again):"
DEL=.delete-check.tmp
printf ': DT S" %s" DELETE-FILE 0= S" %s" DELETE-FILE 0= 0= AND\n  IF S" DELETE-FILE-OK" ELSE S" DELETE-FILE-WRONG" THEN TYPE CR ;\nS" %s" R/W CREATE-FILE DROP CLOSE-FILE DROP DT\nBYE\n' \
    "$DEL" "$DEL" "$DEL" > "$O/.delete.fth"
for w in 64 32; do
    ran=0; bad=""
    for st in $(stages_for $w); do
        e=$O/$st-$w; i=$O/$st-s$w.img
        if [ ! -x "$e" ] || [ ! -r "$i" ]; then
            [ -x "$O/s0-cell-$w" ] && bad="$bad $st(not built)"; continue    # Iteration 125
        fi
        rm -f "$W/$DEL"; ran=$((ran + 1))
        ( cd "$W" && timeout 15 "$e" "$i" < "$O/.delete.fth" > "$O/.delete.out" 2>&1 ); st_=$?
        if [ $st_ -ne 0 ] || ! grep -aq DELETE-FILE-OK "$O/.delete.out" || [ -e "$W/$DEL" ]; then
            bad="$bad $st(exit $st_)"
        fi
        rm -f "$W/$DEL"
    done
    if [ $ran -eq 0 ] && [ -z "$bad" ]; then printf '  %-12s SKIP   not built\n' "$w-bit"
    elif [ -n "$bad" ]; then printf '  %-12s FAIL  %s\n' "$w-bit" "$bad"; rc=1
    else printf '  %-12s ok     %d stages\n' "$w-bit" "$ran"; fi
done

echo
# ---- the fixes of Iteration 125 ---------------------------------------
# What the Forth 2012 test suite and RelF found wrong (results/forth-
# standard-tests.md): coreplus-loop.fth (RelF's, the standard's +LOOP
# sections) and fixes.fth in one file with the sentinel at its end - an
# abort inside INCLUDED returns to stdin, so a sentinel after it proves
# nothing - and a copy with one wrong case that must be caught. Then the
# refusals, which abort and so cannot be tester cases: a name over 31
# characters, IF outside a definition (it killed the engine).
echo
echo "the fixes of Iteration 125 (+LOOP, strings, CONVERT, file words, refusals):"
FG=$O/.fixes-good.fth; FB=$O/.fixes-bad.fth; FR=$O/.fixes-refuse.fth
{ cat "$ROOT/tests/core/coreplus-loop.fth" "$ROOT/tests/core/fixes.fth"; printf '\nS" FIXES-REACHED-END" TYPE CR\n'; } > "$FG"
{ cat "$ROOT/tests/core/coreplus-loop.fth" "$ROOT/tests/core/fixes.fth"; printf '\n{ 1 2 + -> 4 }\nS" FIXES-REACHED-END" TYPE CR\n'; } > "$FB"
printf ': ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ 1 ;\n1 IF 2 THEN\nS" REFUSED-AND-ALIVE" TYPE CR\nBYE\n' > "$FR"
fixrun() { # fixrun ENGINE IMAGE FILE -> the output in $O/.fx.out, the status echoed
    rm -f "$W/fixes-test.tmp"
    ( cd "$W" && printf 'S" tester.fr" INCLUDED\n\nS" %s" INCLUDED\nBYE\n' "$3" | timeout 60 "$1" "$2" > "$O/.fx.out" 2>&1 ); echo $?
    rm -f "$W/fixes-test.tmp"
}
for w in 64 32; do
    ran=0; bad=""
    for st in $(stages_for $w); do
        e=$O/$st-$w; i=$O/$st-s$w.img
        if [ ! -x "$e" ] || [ ! -r "$i" ]; then
            [ -x "$O/s0-cell-$w" ] && bad="$bad $st(not built)"; continue
        fi
        ran=$((ran + 1))
        x=$(fixrun "$e" "$i" "$FG")
        if [ "$x" != 0 ] || ! grep -aq FIXES-REACHED-END "$O/.fx.out" || grep -aqE "$ERRS" "$O/.fx.out"; then
            bad="$bad $st(exit $x$(grep -acE "$ERRS" "$O/.fx.out" | sed 's/^/, failed /'))"; continue
        fi
        x=$(fixrun "$e" "$i" "$FB")
        if [ "$x" != 0 ] || [ "$(grep -acE "$ERRS" "$O/.fx.out")" -lt 1 ]; then bad="$bad $st(control not caught)"; continue; fi
        ( cd "$W" && timeout 15 "$e" "$i" < "$FR" > "$O/.fx.out" 2>&1 ); x=$?
        if [ $x != 0 ] || ! grep -aq 'name too long' "$O/.fx.out" || ! grep -aq 'compile only IF' "$O/.fx.out" \
           || ! grep -aq REFUSED-AND-ALIVE "$O/.fx.out"; then bad="$bad $st(refusals, exit $x)"; fi
    done
    if [ $ran -eq 0 ] && [ -z "$bad" ]; then printf '  %-12s SKIP   not built\n' "$w-bit"
    elif [ -n "$bad" ]; then printf '  %-12s FAIL  %s\n' "$w-bit" "$bad"; rc=1
    else printf '  %-12s ok     %d stages, each with its negative control\n' "$w-bit" "$ran"; fi
done

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

# ---- saved images ------------------------------------------------------
# Nothing booted an image written by SAVE-SYSTEM after tests/shell/ was
# removed, and for months every one of them crashed on start: the hashed
# word list's 32 thread heads were saved as absolute addresses, which
# COLD then relocated a second time. The shell image is written by
# SAVE-SYSTEM and boots into shell.4's MAIN, so running one command
# through it checks save, relocation and boot together.
echo
echo "saved image (SAVE-SYSTEM, then boot):"
for w in 64 32; do
    e=$O/s0-cell-$w; i=$O/s0-cell-$w.img
    if [ ! -x "$e" ] || [ ! -r "$i" ]; then printf '  %-12s SKIP   not built\n' "$w-bit"; continue; fi
    out=$( timeout 15 "$e" "$i" -c 'echo SAVED-IMAGE-BOOTS' 2>/dev/null )
    if [ "$out" != SAVED-IMAGE-BOOTS ]; then
        printf '  %-12s FAIL   the saved shell image did not boot\n' "$w-bit"; FAILED=1; continue
    fi
    # Leave addresses were absolute too: right in the session that compiled
    # them, wrong in any saved image. A skipped ?DO and a LEAVE, compiled,
    # saved, reloaded and run.
    k=$([ "$w" = 64 ] && echo kernel.img || echo kernel32.img)
    cp "$W/$k" "$O/.lv-save.img"; rm -f "$O/.lv.img"
    ( cd "$W" && printf 'S" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\n: T1 0 0 ?DO 99 LOOP 7 ;\n: T2 10 0 DO I 3 = IF LEAVE THEN LOOP 8 ;\nS" %s" SAVE-SYSTEM\nBYE\n' "$O/.lv.img" \
        | timeout 30 "$e" "$k" >/dev/null 2>&1 )
    cp "$O/.lv-save.img" "$W/$k"
    lv=$( printf 'T1 . T2 . CR\nBYE\n' | timeout 15 "$e" "$O/.lv.img" 2>/dev/null | tr -d '\r' | grep -c '^7 8 ' )
    if [ "$lv" = 1 ]; then printf '  %-12s ok     boots; ?DO and LEAVE survive the save\n' "$w-bit"
    else printf '  %-12s FAIL   ?DO or LEAVE broken in a saved image\n' "$w-bit"; FAILED=1; fi
done

[ "${FAILED:-0}" = 0 ] || rc=1

# A system saving ITSELF, from inside its own shell, as a user would -
# the cell system and the full self-hosting CV8 one. Nothing tested CV8
# saving before: its saver still wrote the header layout from before the
# word list was hashed again, and unrelocated the thread count instead
# of the heads, so no CV8 system could save itself. And both savers
# freed the live pool buffers, so a save from inside a shell command
# wrote a good image and then crashed the shell. Checked: the save
# exits cleanly, and the image it wrote boots and runs a command.
echo
echo "a system saving itself, from inside its shell:"
for w in 64 32; do
    for sys in s0-cell s5-cv8spec; do
        e=$O/$sys-$w; i=$O/$sys-$w.img; t=$O/.selfsave-$sys-$w.img
        if [ ! -x "$e" ] || [ ! -r "$i" ]; then
            printf '  %-12s %s  SKIP   not built\n' "$sys" "$w-bit"; continue; fi
        rm -f "$t"
        ( cd "$W" && timeout 30 "$e" "$i" -c "forth 'S\" $t\" SAVE-SYSTEM'" \
            >/dev/null 2>&1 ); st=$?
        out=$( timeout 15 "$e" "$t" -c 'echo SELF-SAVED-BOOTS' 2>/dev/null | tr -d '\r' )
        if [ $st -ne 0 ]; then
            printf '  %-12s %s  FAIL   the save exited %s\n' "$sys" "$w-bit" "$st"; rc=1
        elif [ "$out" != SELF-SAVED-BOOTS ]; then
            printf '  %-12s %s  FAIL   the saved image did not boot\n' "$sys" "$w-bit"; rc=1
        else
            printf '  %-12s %s  ok     saves cleanly; the image boots\n' "$sys" "$w-bit"
        fi
        rm -f "$t"
    done
done
[ $rc -eq 0 ] && echo "PASS - no regressions" || echo "FAIL - see above"
exit $rc
