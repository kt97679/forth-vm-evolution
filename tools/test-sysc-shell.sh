#!/bin/sh
# tools/test-sysc-shell.sh - the gene sysc's shell half (Iteration 135): s5's
# engine built with SYSC, a shell image with forth/shell-sysc.4 loaded before
# shell.4 (dumped on the cell stage, translated with s5's options, as
# build-stages.sh makes s5-cv8spec-64.img), and tests/shell run through it -
# every assertion must pass, as on the plain shell; then a few paths compared
# line for line with the plain s5 shell. x86-64 with 8-byte cells only (SYSC's
# own #error elsewhere). Not yet in run-tests.sh: run it after build-stages.sh.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd); cd "$ROOT"
. tools/engine-rt.sh
O=$ROOT/build; W=$O/work; T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
[ "$(uname -m)" = x86_64 ] && [ -x "$O/s0-cell-64" ] && [ -s "$O/vm-lab-tos.c" ] || { echo "SKIP   needs x86-64 and the 8-byte build"; exit 0; }
cp forth/shell-sysc.4 "$W/"
SB='S" cv8.4" INCLUDED\nS" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\nS" shell-sysc.4" INCLUDED\nS" shell.4" INCLUDED\nS" cv8-save.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
( cd "$W" && printf "$SB" | "$O/s0-cell-64" kernel.img ) | tr -d '\r' > "$T/d64.txt"
if grep -q -i 'undefined word\|not found' "$T/d64.txt"; then echo "FAIL   the overlay did not compile: $(grep -i -m2 'undefined word\|not found' "$T/d64.txt" | tr '\n' ' ')"; exit 1; fi
HOT='+,=,!,@,LSHIFT,RSHIFT,C@,C!,AND,OR,XOR,LIT,<,U<,OVER,DROP,DUP,SWAP,ROT,>R,R>,R@,NEGATE'
( cd "$W" && python3 "$ROOT/tools/layout.py" "$T/d64.txt" 8 --v8 --cpt 3 --dataprims --fold --fold-set "$HOT" \
    --spec loc,var,tiny,small,imm --cv8-compiler --emit-image "$T/sh.img" ) > "$T/layout.log" 2>&1 \
    || { echo "FAIL   the shell image did not translate"; grep -A6 UNTRANSLATED "$T/layout.log" | head -8; exit 1; }
cc -O2 -DENC=3 -DREG=1 -DFOLD=1 -DSCALE=3 -DSPEC=1 -DSHAREDCALL=1 -DSYSC=1 -o "$T/eng" "$O/vm-lab-tos.c" $RT_FLAGS
printf '#!/bin/sh\nexec "%s" "%s" "$@"\n' "$T/eng" "$T/sh.img" > "$T/sh"; chmod +x "$T/sh"
printf '#!/bin/sh\nexec "%s" "%s" "$@"\n' "$O/s5-cv8spec-64" "$O/s5-cv8spec-64.img" > "$T/plain"; chmod +x "$T/plain"
echo "s5's engine: $(stat -c%s "$O/s5-cv8spec-64") bytes, $(stat -c%s "$T/eng") with SYSC"
if THIS_SH="$T/sh" sh tests/shell/run-all > "$T/suite.log" 2>&1; then
    echo "ok     tests/shell on the SYSC shell: $(grep -o '^[0-9]* assertions' "$T/suite.log" | awk '{s+=$1} END {print s}') assertions"
else echo "FAIL   tests/shell on the SYSC shell: $(grep '^FAIL' "$T/suite.log" | head -3 | tr '\n' ' ')"; exit 1; fi
CMD='echo ~root; echo ~nosuchuser42; ulimit -f; ulimit -f 4096; ulimit -f; export SYSCT=yes; sh -c "echo child sees \$SYSCT"; unset SYSCT; sh -c "echo after unset: [\$SYSCT]"; env | grep -c "="; cd / && pwd'
for s in plain sh; do env -i HOME="$HOME" PATH=/usr/bin:/bin USER="${USER:-x}" "$T/$s" -c "$CMD" > "$T/$s.out" 2>&1 || true; done
if cmp -s "$T/plain.out" "$T/sh.out"; then echo "ok     ~user, ulimit -f, export, unset, the environment, cd: as the plain shell"
else echo "FAIL   differs from the plain shell:"; diff "$T/plain.out" "$T/sh.out" | head -6; exit 1; fi
