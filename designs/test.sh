#!/bin/sh
# designs/test.sh NAME... - each design's engine runs its image (make test): a definition, a call, a number printed;
# and THROW and CATCH across the JIT's levels (Iteration 672, relf's report - its Iteration 942): a THROW in native
# code, or in an interpreter nested under it, whose CATCH is an outer interpreter's, goes on after that CATCH - the
# C stack unwound to it - and an uncaught one, many times over, frees what it left. forth32 too where it is built.
cd "$(dirname "$0")" || exit 1
fail=0
leak=$(mktemp) || exit 1
trap 'rm -f "$leak"' EXIT
{ echo ': T ABORT ;'; i=0; while [ $i -lt 30000 ]; do echo T; i=$((i + 1)); done; echo '7 . BYE'; } > "$leak"
check() {   # check DESIGN ENGINE IMAGE NAME EXPECTED INPUT - the output must hold EXPECTED
    out=$(printf '%s\n' "$6" | timeout 60 ./"$1"/"$2" "$1"/"$3" 2>&1)
    case $out in *"$5"*) return 0 ;; esac
    echo "$1 $2: $4 FAILED - $(printf '%s' "$out" | tail -n 2 | tr '\n' ' ' | cut -c1-100)"; fail=1; return 1
}
for d in "$@"; do
    for e in forth forth32; do
        img=image.img; [ $e = forth32 ] && img=image32.img
        [ -x "$d/$e" ] || { [ $e = forth ] && { echo "$d: FAILED - no $d/forth (make)"; fail=1; }; continue; }
        ok=1
        check $d $e $img square '49' ': SQ DUP * ; 7 SQ . BYE' || ok=0
        check $d $e $img throw-abort '-1 5 ' ": T2 ABORT ; : T3 ['] T2 CATCH . ; : T5 ['] T3 EXECUTE 5 . ; T5 CR BYE" || ok=0
        check $d $e $img throw '-1 5 ' ": T2 -1 THROW ; : T3 ['] T2 CATCH . ; : T5 ['] T3 EXECUTE 5 . ; T5 CR BYE" || ok=0
        check $d $e $img throw-outer '-1 4 5 ' ": T2 ABORT ; : T3 ['] T2 CATCH . ; : T4 ['] T3 EXECUTE 4 . ; : T5 ['] T4 EXECUTE 5 . ; T5 CR BYE" || ok=0
        check $d $e $img throw-nested '-1 5 ' ": T2 ABORT ; : T7 ['] T2 EXECUTE RP@ DROP ; : T6 ['] T7 EXECUTE ; : T3 ['] T6 CATCH . ; : T5 ['] T3 EXECUTE 5 . ; T5 CR BYE" || ok=0
        out=$(timeout 120 ./"$d"/$e "$d"/$img < "$leak" 2>&1 | tail -n 1)
        [ "$out" = "7 " ] || { echo "$d $e: uncaught FAILED - $(printf '%s' "$out" | cut -c1-100)"; fail=1; ok=0; }
        [ $ok = 1 ] && echo "$d $e: ok"
    done
done
exit $fail
