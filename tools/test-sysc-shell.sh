#!/bin/sh
# tools/test-sysc-shell.sh - the gene sysc's shell half (Iterations 135, 141):
# at each cell width built, s5's engine built with SYSC, a shell image with
# forth/shell-sysc.4 loaded before shell.4 (dumped on the cell stage,
# translated with s5's options, as build-stages.sh makes s5-cv8spec-*.img), and
# tests/shell run through it - every assertion must pass, as on the plain
# shell; then a few paths compared line for line with the plain s5 shell. The
# overlay's numbers are x86-64's; at 4-byte cells the engine maps i386's.
# x86 hosts only. Not yet in run-tests.sh: run it after build-stages.sh.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd); cd "$ROOT"
. tools/engine-rt.sh
O=$ROOT/build; W=$O/work; T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
case "$(uname -m)" in x86_64|i?86) ;; *) echo "SKIP   x86 only"; exit 0 ;; esac
[ -s "$O/vm-lab-tos.c" ] || { echo "SKIP   build-stages.sh has not run"; exit 0; }
# build-stages.sh links every forth/*.4 into the work directory; copy only
# into a tree built before the overlay existed (never through a link)
cmp -s forth/shell-sysc.4 "$W/shell-sysc.4" 2>/dev/null || { rm -f "$W/shell-sysc.4"; cp forth/shell-sysc.4 "$W/"; }
SB='S" cv8.4" INCLUDED\nS" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\nS" shell-sysc.4" INCLUDED\nS" shell.4" INCLUDED\nS" cv8-save.4" INCLUDED\nS" dict-dump-addr.4" INCLUDED\nBYE\n'
HOT='+,=,!,@,LSHIFT,RSHIFT,C@,C!,AND,OR,XOR,LIT,<,U<,OVER,DROP,DUP,SWAP,ROT,>R,R>,R@,NEGATE'
CMD='echo ~root; echo ~nosuchuser42; ulimit -f; ulimit -f 4096; ulimit -f; export SYSCT=yes; sh -c "echo child sees \$SYSCT"; unset SYSCT; sh -c "echo after unset: [\$SYSCT]"; env | grep -c "="; cd / && pwd; echo a b | tr a-z A-Z'
bad=0
for w in 64 32; do
    [ -x "$O/s0-cell-$w" ] && [ -x "$O/s5-cv8spec-$w" ] || { echo "SKIP   $w-bit: not built"; continue; }
    # each width's own call-target alignment, as build-stages.sh: SCALE=3 and --cpt 3, SCALE=2 and --cpt 2
    if [ $w = 64 ]; then c=8; cpt=3; k=kernel.img; cc_="cc -O2 -DSCALE=3"; rt=$RT_FLAGS
    else c=4; cpt=2; k=kernel32.img; cc_="cc -m32 -O2 -fno-pie -no-pie -DSCALE=2"; rt=$RT_FLAGS32; fi
    ( cd "$W" && printf "$SB" | "$O/s0-cell-$w" $k ) | tr -d '\r' > "$T/d$w.txt"
    if grep -q -i 'undefined word\|not found' "$T/d$w.txt"; then
        echo "FAIL   $w-bit: the overlay did not compile: $(grep -i -m2 'undefined word\|not found' "$T/d$w.txt" | tr '\n' ' ')"; bad=1; continue; fi
    ( cd "$W" && python3 "$ROOT/tools/layout.py" "$T/d$w.txt" $c --v8 --cpt $cpt --dataprims --fold --fold-set "$HOT" \
        --spec loc,var,tiny,small,imm --cv8-compiler --emit-image "$T/sh$w.img" ) > "$T/layout$w.log" 2>&1 \
        || { echo "FAIL   $w-bit: the shell image did not translate"; bad=1; continue; }
    $cc_ -DENC=3 -DREG=1 -DFOLD=1 -DSPEC=1 -DSHAREDCALL=1 -DSYSC=1 -o "$T/eng$w" "$O/vm-lab-tos.c" $rt
    [ -n "${SYSC_KEEP:-}" ] && cp "$T/eng$w" "$T/sh$w.img" "$SYSC_KEEP/"
    printf '#!/bin/sh\nexec "%s" "%s" "$@"\n' "$T/eng$w" "$T/sh$w.img" > "$T/sh$w"; chmod +x "$T/sh$w"
    printf '#!/bin/sh\nexec "%s" "%s" "$@"\n' "$O/s5-cv8spec-$w" "$O/s5-cv8spec-$w.img" > "$T/plain$w"; chmod +x "$T/plain$w"
    echo "$w-bit: s5's engine $(stat -c%s "$O/s5-cv8spec-$w") bytes, $(stat -c%s "$T/eng$w") with SYSC"
    if THIS_SH="$T/sh$w" sh tests/shell/run-all > "$T/suite$w.log" 2>&1; then
        echo "ok     $w-bit: tests/shell on the SYSC shell, $(grep -o '^[0-9]* assertions' "$T/suite$w.log" | awk '{s+=$1} END {print s}') assertions"
    else echo "FAIL   $w-bit: tests/shell on the SYSC shell: $(grep '^FAIL' "$T/suite$w.log" | head -3 | tr '\n' ' ')"; bad=1; fi
    for s in plain sh; do env -i HOME="$HOME" PATH=/usr/bin:/bin USER="${USER:-x}" "$T/$s$w" -c "$CMD" > "$T/$s$w.out" 2>&1 || true; done
    if cmp -s "$T/plain$w.out" "$T/sh$w.out"; then echo "ok     $w-bit: ~user, ulimit -f, export, unset, the environment, cd, a pipe: as the plain shell"
    else echo "FAIL   $w-bit: differs from the plain shell:"; diff "$T/plain$w.out" "$T/sh$w.out" | head -6; bad=1; fi
    # the cell stage (engine/relf.c, Iteration 142): its shell as build-stages.sh's
    # cellshell makes it, the overlay loaded before shell.4, on a SYSC cell engine
    ccc="cc -O2 -Wall"; [ $w = 32 ] && ccc="cc -m32 -O2 -Wall"
    $ccc -DSYSC=1 -o "$T/celleng$w" engine/relf.c $rt
    ( cd "$W" && printf 'S" pool.4" INCLUDED\nS" locals.4" INCLUDED\nS" save-system.4" INCLUDED\nS" shell-sysc.4" INCLUDED\nS" shell.4" INCLUDED\n'"' MAIN SET-BOOT\nS\" $T/cellsh$w.img\" SAVE-SYSTEM\nBYE\n" \
        | "$T/celleng$w" $k > /dev/null 2>&1 )
    if [ ! -s "$T/cellsh$w.img" ]; then echo "FAIL   $w-bit cell: no shell image"; bad=1; continue; fi
    printf '#!/bin/sh\nexec "%s" "%s" "$@"\n' "$T/celleng$w" "$T/cellsh$w.img" > "$T/csh$w"; chmod +x "$T/csh$w"
    printf '#!/bin/sh\nexec "%s" "%s" "$@"\n' "$O/s0-cell-$w" "$O/s0-cell-$w.img" > "$T/cplain$w"; chmod +x "$T/cplain$w"
    echo "$w-bit: the cell engine $(stat -c%s "$O/s0-cell-$w") bytes, $(stat -c%s "$T/celleng$w") with SYSC"
    if THIS_SH="$T/csh$w" sh tests/shell/run-all > "$T/csuite$w.log" 2>&1; then
        echo "ok     $w-bit cell: tests/shell on the SYSC shell, $(grep -o '^[0-9]* assertions' "$T/csuite$w.log" | awk '{s+=$1} END {print s}') assertions"
    else echo "FAIL   $w-bit cell: tests/shell on the SYSC shell: $(grep '^FAIL' "$T/csuite$w.log" | head -3 | tr '\n' ' ')"; bad=1; fi
    for s in cplain csh; do env -i HOME="$HOME" PATH=/usr/bin:/bin USER="${USER:-x}" "$T/$s$w" -c "$CMD" > "$T/$s$w.out" 2>&1 || true; done
    if cmp -s "$T/cplain$w.out" "$T/csh$w.out"; then echo "ok     $w-bit cell: the same paths as the plain cell shell"
    else echo "FAIL   $w-bit cell: differs from the plain cell shell:"; diff "$T/cplain$w.out" "$T/csh$w.out" | head -6; bad=1; fi
done
exit $bad
