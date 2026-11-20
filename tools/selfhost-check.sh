#!/bin/sh
# tools/selfhost-check.sh [--self-test] [--32] [NAME] - a design's fixed point under the CV8 cross compiler (Iterations
# 667, 669, 671; results/drafts/selfhost-plan-666.md). NAME is s6 (the ladder's s6-cv8b, the default) or a design in
# designs/; --32 takes its 4-byte-cell build instead (forth32, image32.img, genes32.4). The design's translator-built
# image, on the design's engine, runs forth/cross-cv8.4 with the design's genes (stages/s6-genes.4, designs/NAME/
# genes.4 - lab/evolve/export-genes.py) and writes image A; A, booted on the same engine, runs it and writes B. A must
# equal B byte for byte, and A must pass the evolver's own gate (lab/evolve/evolve.py's alive(): the corpus against
# the cell engine, the kernel workload against the seed, the far tests, an ALLOT past the dictionary refused - at
# 4-byte cells against the 4-byte references, as eval32 runs it). With --32 the 64-bit build of the design also
# builds the 32-bit image, and it must be A too: the host's width does not reach the image. A JIT design's engine
# knows its image's layout (src/vm-jit-ops.h's jit_wends and JIT_W_ lines - every code word's body, a few words'
# offsets): the cross compiler writes them for its image (cv8-self-jit.h), and A and B run on the design's engine
# rebuilt with A's (build/selfhost/check-NAME/eng/); B's (and the 64-bit build's) must be A's. --self-test first plants
# a fault - a bit of PARSE's body in A flipped - and fails unless the check catches it. From the repository's top, as
# the build user, in a built tree (tools/build-stages.sh); a design's engines are made if missing. Works in
# build/selfhost/check-NAME/ (check-NAME-32/); exit 1 on any failure. Iteration 675 (phase 5): DESIGNS=DIR another
# designs directory (an export); SHIP=1, the check passed, ships A - image.img (image32.img) and, for a JIT design,
# A's layout into src/vm-jit-ops.h (src32/) - tools/selfhost-ship.sh's step; the design's engine always made (make
# decides), as a shipped layout leaves the built one stale. A shipped image is its own starting image: A = B = it.
set -e
cd "$(dirname "$0")/.."
TEST=; [ "$1" = --self-test ] && { TEST=1; shift; }
W=8; [ "$1" = --32 ] && { W=4; shift; }
N=${1:-s6}
T=$(pwd) D=$(pwd)/build/selfhost/check-$N
DS=$(cd "${DESIGNS:-designs}" && pwd) || exit 1
if [ "$N" = s6 ]; then
    [ $W = 8 ] || { echo "selfhost-check: s6 is 8-byte cells only"; exit 1; }
    ENG=$T/build/s6-cv8b-64 IMG=$T/build/s6-cv8b-s64.img GENES=$T/stages/s6-genes.4
    [ -x "$ENG" ] && [ -f "$IMG" ] || { echo "selfhost-check: build first (tools/build-stages.sh)"; exit 1; }
else
    G=genes.4; [ $W = 4 ] && { G=genes32.4; D=$D-32; }
    [ -f "$DS/$N/$G" ] || { echo "selfhost-check: no $DS/$N/$G (lab/evolve/export-genes.py $N)"; exit 1; }
    ENG=$DS/$N/forth IMG=$DS/$N/image.img GENES=$DS/$N/$G
    make -s -C "$DS/$N" forth > /dev/null 2>&1 || { echo "selfhost-check: can't make $DS/$N/forth"; exit 1; }
    if [ $W = 4 ]; then
        ENG64=$ENG IMG64=$IMG ENG=$DS/$N/forth32 IMG=$DS/$N/image32.img
        make -s -C "$DS/$N" forth32 > /dev/null 2>&1 || { echo "selfhost-check: can't make $DS/$N/forth32"; exit 1; }
    fi
fi
rm -rf "$D"; mkdir -p "$D"
cp forth/*.4 "$D/"      # the cross compiler reads kernel.4 and the overlays the genes name
cp "$GENES" "$D/genes.4"
cross() {   # cross IMAGE OUT [ENGINE] - run the cross compiler on IMAGE, its image moved to OUT
    rm -f "$D/cv8-self.img" "$D/cv8-self-jit.h"
    ( cd "$D" && printf 'S" extend.4" INCLUDED\nS" genes.4" INCLUDED\nS" cross-cv8.4" INCLUDED\n' | timeout 300 "${3:-$ENG}" "$1" > "$2.log" 2>&1 ) || true
    rm -f "$2.jit.h"; [ -s "$D/cv8-self-jit.h" ] && mv "$D/cv8-self-jit.h" "$2.jit.h"
    [ -s "$D/cv8-self.img" ] && mv "$D/cv8-self.img" "$2"
}
cross "$IMG" "$D/A.img" || { echo "selfhost-check: FAIL - the translator-built $N wrote no image ($D/A.img.log)"; exit 1; }
ENGA=$ENG J=
if [ "$N" != s6 ] && grep -q "jit_wends" "$DS/$N/src/vm-jit-ops.h" 2>/dev/null; then
    # A JIT design: its engine for A, with A's layout in vm-jit-ops.h (the lines the design has)
    S=src; E=forth; [ $W = 4 ] && { S=src32; E=forth32; }
    [ -s "$D/A.img.jit.h" ] || { echo "selfhost-check: FAIL - no JIT layout with A ($D/A.img.log)"; exit 1; }
    mkdir -p "$D/eng"; cp -r "$DS/$N/Makefile" "$DS/$N/src" "$DS/$N/src32" "$D/eng/"
    python3 - "$D/eng/$S/vm-jit-ops.h" "$D/A.img.jit.h" <<'PYEOF' || exit 1
import sys
key = lambda l: 'jit_wends' if l.startswith('static const unsigned') and 'jit_wends[][2]' in l else ' '.join(l.split()[:2])   # 710: int or short
new = {key(l): l for l in open(sys.argv[2]).read().splitlines() if l}
old = open(sys.argv[1]).read().splitlines(); out = [new.get(key(l), l) for l in old]
assert {'#define JIT_NWENDS', 'jit_wends'} <= set(map(key, old)), 'selfhost-check: the layout lines not found'
open(sys.argv[1], 'w').write('\n'.join(out) + '\n')
PYEOF
    make -s -C "$D/eng" $E > "$D/eng.log" 2>&1 || { echo "selfhost-check: FAIL - the engine for A did not build ($D/eng.log)"; exit 1; }
    ENGA=$D/eng/$E J="; the engine rebuilt with A's layout ($(sed -n 's/^#define JIT_NWENDS //p' "$D/A.img.jit.h") code words)"
fi
if [ -n "$TEST" ]; then
    # A planted fault: the first byte of PARSE's body in A flipped - a word the cross compiler cannot run
    # without. Either the build dies or B differs; the check must say so.
    cp "$D/A.img" "$D/A-good.img"
    python3 -c "
import sys; b = bytearray(open(sys.argv[1], 'rb').read()); i = b.find(bytes([5]) + b'PARSE')
assert i > 0, 'no PARSE header in A'
b[i + 6] ^= 0x01; open(sys.argv[1], 'wb').write(b)" "$D/A.img"
    if cross "$D/A.img" "$D/B.img" "$ENGA" && cmp -s "$D/A-good.img" "$D/B.img"; then
        echo "selfhost-check: self-test FAILED - a planted fault went unnoticed"; exit 1
    fi
    echo "selfhost-check: self-test - a planted fault caught"
    mv "$D/A-good.img" "$D/A.img"
fi
cross "$D/A.img" "$D/B.img" "$ENGA" || { echo "selfhost-check: FAIL - A wrote no image ($D/B.img.log)"; exit 1; }
cmp -s "$D/A.img" "$D/B.img" || { echo "selfhost-check: FAIL - A rebuilt itself differently"; exit 1; }
if [ -n "$J" ]; then cmp -s "$D/A.img.jit.h" "$D/B.img.jit.h" || { echo "selfhost-check: FAIL - A's JIT layout differs from B's"; exit 1; }; fi
X=
if [ $W = 4 ]; then
    cross "$IMG64" "$D/C.img" "$ENG64" || { echo "selfhost-check: FAIL - the 64-bit $N wrote no 32-bit image ($D/C.img.log)"; exit 1; }
    cmp -s "$D/A.img" "$D/C.img" || { echo "selfhost-check: FAIL - the 64-bit $N built the 32-bit image differently"; exit 1; }
    if [ -n "$J" ]; then cmp -s "$D/A.img.jit.h" "$D/C.img.jit.h" || { echo "selfhost-check: FAIL - the 64-bit $N wrote another JIT layout"; exit 1; }; fi
    X="; the 64-bit build makes it too"
fi
python3 - "$ENGA" "$D/A.img" $W <<'EOF' || exit 1
import contextlib, os, sys, tempfile, shutil
eng, img = (os.path.abspath(a) for a in sys.argv[1:3]); w = int(sys.argv[3])
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
if w == 4: E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
else: E.setup()
with (E.at_width(E.WIDTH4) if w == 4 else contextlib.nullcontext()):
    pw = tempfile.mkdtemp(dir=E.EV)
    for f in os.listdir(E.W):
        if f != 'kernel.img': os.symlink(os.path.join(E.W, f), os.path.join(pw, f))
    shutil.copy(E.KREF, os.path.join(pw, 'kernel.img'))
    try: E.alive(eng, img, pw, far=True)
    except RuntimeError as e: print('selfhost-check: FAIL - the gate:', e); sys.exit(1)
    finally: shutil.rmtree(pw, ignore_errors=True)
EOF
P=$(grep "pass 3" "$D/B.img.log" | sed 's/^cross-cv8: pass 3 - [0-9]* bytes, //')
S0=$(stat -c %s "$IMG"); [ -n "${SHIP:-}" ] && [ "$N" != s6 ] && {
    I0=image.img; [ $W = 4 ] && I0=image32.img; cp "$D/A.img" "$DS/$N/$I0"
    if [ -n "$J" ]; then cp "$D/eng/$S/vm-jit-ops.h" "$DS/$N/$S/vm-jit-ops.h"; fi
    J="$J; shipped as $DS/$N/$I0${J:+ and $S/vm-jit-ops.h}"; }
[ $W = 4 ] && N="$N (4-byte cells)"
echo "selfhost-check: PASS - $N self-hosting: A = B, $(stat -c %s "$D/A.img") bytes ($P)$X$J; the gate passed (the starting image: $S0)"
