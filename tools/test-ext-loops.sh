#!/bin/sh
# tools/test-ext-loops.sh - ?DO and LEAVE in an extension (Iteration 139). The
# converter refused both until the kernel's leave addresses became offsets;
# now they are loop words like (LOOP). Four words using them are compiled on
# the cell stage before shell.4, translated with s1's, s3's, s4's and s5's
# own options, as build-stages.sh translates those stages' shell images, and
# run on each stage's engine: a skipped ?DO, a LEAVE, a ?DO that runs, a
# LEAVE in a nested loop. Not yet in run-tests.sh; run it after build-stages.sh.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd); cd "$ROOT"
O=$ROOT/build; W=$O/work; T=$(mktemp -d); trap 'rm -rf "$T"; rm -f "$W/t-ext-loops.4"' EXIT
[ -x "$O/s0-cell-64" ] || { echo "SKIP   needs the 8-byte build"; exit 0; }
eval "$(grep -E '^(SHELL_BOOT|SELF_BOOT|HOT|SPECS)=' tools/build-stages.sh)"; CPTF="--dataprims --fold --fold-set $HOT"
cat > "$W/t-ext-loops.4" << 'F'
: XT1 0 0 ?DO 99 LOOP 7 ;
: XT2 10 0 DO I 3 = IF LEAVE THEN LOOP 8 ;
: XT3 5 0 ?DO I LOOP ;
: XT4 3 0 ?DO 10 0 DO I 5 = IF LEAVE THEN I LOOP LOOP ;
F
ins() { printf '%s' "$1" | sed 's|S" shell.4" INCLUDED|S" t-ext-loops.4" INCLUDED\\nS" shell.4" INCLUDED|'; }
( cd "$W" && printf "$(ins "$SHELL_BOOT")" | "$O/s0-cell-64" kernel.img ) | tr -d '\r' > "$T/d64.txt"
( cd "$W" && printf "$(ins "$SELF_BOOT")" | "$O/s0-cell-64" kernel.img ) | tr -d '\r' > "$T/d64-self.txt"
want='7 8 4 3 2 1 0 4 3 2 1 0 4 3 2 1 0 4 3 2 1 0'; bad=0
for st in "s1-sod16 d64.txt --skip-pad" "s3-cpt16f d64.txt --cpt 3 $CPTF" \
          "s4-cv8 d64.txt --v8 --cpt 3 $CPTF --no-varcall --no-varslot" \
          "s5-cv8spec d64-self.txt --v8 --cpt 3 $CPTF --spec $SPECS --cv8-compiler"; do
  set -- $st; n=$1; d=$2; shift 2
  if ! ( cd "$W" && python3 "$ROOT/tools/layout.py" "$T/$d" 8 "$@" --emit-image "$T/$n.img" ) > "$T/$n.log" 2>&1; then
    echo "FAIL   $n: did not translate"; bad=1; continue; fi
  got=$(timeout 10 "$O/$n-64" "$T/$n.img" -c "forth 'XT1 . XT2 . XT3 . . . . . XT4 . . . . . . . . . . . . . . .'" 2>&1 \
        | tr -d '\r' | tr -s ' \n' ' ' | sed 's/^ *//; s/ *$//')
  if [ "$got" = "$want" ]; then echo "ok     $n"; else echo "FAIL   $n: $got"; bad=1; fi
done
exit $bad
