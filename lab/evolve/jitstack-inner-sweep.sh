#!/bin/sh
# jitstack-inner-sweep.sh - lab/evolve/jitstack-inner.{c,S} with every loop head
# placed at eight offsets in a 64-byte line (Iteration 219): on the development
# VM's Intel core the same loop ran 0.68 or 1.8 ns by where it landed, so one
# placement proves nothing. Prints ns per iteration for each version at each
# offset. Run on the machine whose time matters:  sh lab/evolve/jitstack-inner-sweep.sh
set -e
d=$(mktemp -d); here=$(dirname "$0")
for off in 0 8 16 24 32 40 48 56; do
    sed -E "s/^\.L(A|B|C|F2|F3):/    .p2align 6\n    .skip $off, 0x90\n.L\1:/" "$here/jitstack-inner.S" > "$d/i.S"
    gcc -O2 -no-pie -o "$d/i" "$here/jitstack-inner.c" "$d/i.S" 2>/dev/null
    "$d/i" | awk -v o=$off '/^now/{n=$4} /^cached/{c=$4} /^\+loop/{l=$4} /^fixed2/{f2=$4} /^fixed3/{f3=$4} /^same/{s=$3}
        END{printf "offset %2d: today %s  cached %s  +loop %s  fixed K=2 %s  fixed K=3 %s  (results agree: %s)\n", o, n, c, l, f2, f3, s}'
done
rm -rf "$d"
