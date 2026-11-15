#!/bin/sh
# designs/selfhost.sh ENGINE IMAGE GENES SRC - `make selfhost` and `make selfhost32` in a design's directory (Iteration
# 675; results/drafts/selfhost-plan-666.md, phase 5): the image rebuilt from its source. ENGINE runs IMAGE, which
# cross-compiles a new image from ../forth/ - the kernel, the overlays GENES names, extend.4 and cross-cv8.4, the CV8
# cross compiler - with GENES, the design's genes as Forth; the new image must be IMAGE byte for byte. A JIT design's
# engine knows its image's layout (SRC/vm-jit-ops.h's JIT_NWENDS, jit_wends and JIT_W_ lines): the lines the cross
# compiler writes for the new image must be SRC's. Exit 1 on any difference. In the repository the lab's own check,
# with the evolver's gate, is tools/selfhost-check.sh; tools/selfhost-ship.sh made these images.
set -u
H=$(pwd) N=$(basename "$(pwd)") E=$1 I=$2 G=$3 S=$4
D=$(mktemp -d) || exit 1
trap 'rm -rf "$D"' EXIT
cp ../forth/*.4 "$D/" && cp "$G" "$D/genes.4" || exit 1
( cd "$D" && printf 'S" extend.4" INCLUDED\nS" genes.4" INCLUDED\nS" cross-cv8.4" INCLUDED\n' |
    timeout 300 "$H/$E" "$H/$I" > log 2>&1 )
[ -s "$D/cv8-self.img" ] || { echo "selfhost: $N $I FAIL - no image written:"; tail -n 3 "$D/log"; exit 1; }
cmp -s "$D/cv8-self.img" "$I" || { echo "selfhost: $N $I FAIL - rebuilt from source, it differs"; exit 1; }
J=
if grep -q jit_wends "$S/vm-jit-ops.h" 2> /dev/null; then
    [ -s "$D/cv8-self-jit.h" ] || { echo "selfhost: $N $I FAIL - no JIT layout written"; exit 1; }
    # each line the engine has (by name: `#define X`, or the table before ` = `; small-jit has no JIT_W_) as written
    n=0; while IFS= read -r L; do
        [ -n "$L" ] || continue
        case $L in *' = '*) k=${L%% = *} ;; *) k=$(printf '%s\n' "$L" | cut -d' ' -f1-2) ;; esac
        grep -qF "$k " "$S/vm-jit-ops.h" || continue
        grep -qxF "$L" "$S/vm-jit-ops.h" || { echo "selfhost: $N $I FAIL - the JIT layout written is not $S/vm-jit-ops.h's ($k)"; exit 1; }
        n=$((n + 1))
    done < "$D/cv8-self-jit.h"
    [ "$n" -ge 2 ] || { echo "selfhost: $N $I FAIL - $S/vm-jit-ops.h has $n of the layout's lines"; exit 1; }
    J="; its JIT layout $S/vm-jit-ops.h's ($n lines)"
fi
echo "selfhost: $N $I ok - rebuilt from source byte for byte, $(wc -c < "$I") bytes$J"
