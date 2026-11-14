#!/bin/sh
# tools/selfhost-check.sh [--self-test] [--32] [NAME] - a design's fixed point under the CV8 cross compiler (Iterations
# 667, 669, 671; results/drafts/selfhost-plan-666.md). NAME is s6 (the ladder's s6-cv8b, the default) or a design in
# designs/; --32 takes its 4-byte-cell build instead (forth32, image32.img, genes32.4). The design's translator-built
# image, on the design's engine, runs forth/cross-cv8.4 with the design's genes (stages/s6-genes.4, designs/NAME/
# genes.4 - lab/evolve/export-genes.py) and writes image A; A, booted on the same engine, runs it and writes B. A must
# equal B byte for byte, and A must pass the evolver's own gate (lab/evolve/evolve.py's alive(): the corpus against
# the cell engine, the kernel workload against the seed, the far tests, an ALLOT past the dictionary refused - at
# 4-byte cells against the 4-byte references, as eval32 runs it). With --32 the 64-bit build of the design also
# builds the 32-bit image, and it must be A too: the host's width does not reach the image. --self-test first plants
# a fault - a bit of PARSE's body in A flipped - and fails unless the check catches it. From the repository's top, as
# the build user, in a built tree (tools/build-stages.sh); a design's engines are made if missing. Works in
# build/selfhost/check-NAME/ (check-NAME-32/); exit 1 on any failure.
set -e
cd "$(dirname "$0")/.."
TEST=; [ "$1" = --self-test ] && { TEST=1; shift; }
W=8; [ "$1" = --32 ] && { W=4; shift; }
N=${1:-s6}
T=$(pwd) D=$(pwd)/build/selfhost/check-$N
if [ "$N" = s6 ]; then
    [ $W = 8 ] || { echo "selfhost-check: s6 is 8-byte cells only"; exit 1; }
    ENG=$T/build/s6-cv8b-64 IMG=$T/build/s6-cv8b-s64.img GENES=$T/stages/s6-genes.4
    [ -x "$ENG" ] && [ -f "$IMG" ] || { echo "selfhost-check: build first (tools/build-stages.sh)"; exit 1; }
else
    G=genes.4; [ $W = 4 ] && { G=genes32.4; D=$D-32; }
    [ -f "designs/$N/$G" ] || { echo "selfhost-check: no designs/$N/$G (lab/evolve/export-genes.py $N)"; exit 1; }
    ENG=$T/designs/$N/forth IMG=$T/designs/$N/image.img GENES=$T/designs/$N/$G
    [ -x "$ENG" ] || make -s -C "designs/$N" forth > /dev/null 2>&1 || { echo "selfhost-check: can't make designs/$N/forth"; exit 1; }
    if [ $W = 4 ]; then
        ENG64=$ENG IMG64=$IMG ENG=$T/designs/$N/forth32 IMG=$T/designs/$N/image32.img
        [ -x "$ENG" ] || make -s -C "designs/$N" forth32 > /dev/null 2>&1 || { echo "selfhost-check: can't make designs/$N/forth32"; exit 1; }
    fi
fi
rm -rf "$D"; mkdir -p "$D"
cp forth/*.4 "$D/"      # the cross compiler reads kernel.4 and the overlays the genes name
cp "$GENES" "$D/genes.4"
cross() {   # cross IMAGE OUT [ENGINE] - run the cross compiler on IMAGE, its image moved to OUT
    rm -f "$D/cv8-self.img"
    ( cd "$D" && printf 'S" extend.4" INCLUDED\nS" genes.4" INCLUDED\nS" cross-cv8.4" INCLUDED\n' | timeout 300 "${3:-$ENG}" "$1" > "$2.log" 2>&1 ) || true
    [ -s "$D/cv8-self.img" ] && mv "$D/cv8-self.img" "$2"
}
cross "$IMG" "$D/A.img" || { echo "selfhost-check: FAIL - the translator-built $N wrote no image ($D/A.img.log)"; exit 1; }
if [ -n "$TEST" ]; then
    # A planted fault: the first byte of PARSE's body in A flipped - a word the cross compiler cannot run
    # without. Either the build dies or B differs; the check must say so.
    cp "$D/A.img" "$D/A-good.img"
    python3 -c "
import sys; b = bytearray(open(sys.argv[1], 'rb').read()); i = b.find(bytes([5]) + b'PARSE')
assert i > 0, 'no PARSE header in A'
b[i + 6] ^= 0x01; open(sys.argv[1], 'wb').write(b)" "$D/A.img"
    if cross "$D/A.img" "$D/B.img" && cmp -s "$D/A-good.img" "$D/B.img"; then
        echo "selfhost-check: self-test FAILED - a planted fault went unnoticed"; exit 1
    fi
    echo "selfhost-check: self-test - a planted fault caught"
    mv "$D/A-good.img" "$D/A.img"
fi
cross "$D/A.img" "$D/B.img" || { echo "selfhost-check: FAIL - A wrote no image ($D/B.img.log)"; exit 1; }
cmp -s "$D/A.img" "$D/B.img" || { echo "selfhost-check: FAIL - A rebuilt itself differently"; exit 1; }
X=
if [ $W = 4 ]; then
    cross "$IMG64" "$D/C.img" "$ENG64" || { echo "selfhost-check: FAIL - the 64-bit $N wrote no 32-bit image ($D/C.img.log)"; exit 1; }
    cmp -s "$D/A.img" "$D/C.img" || { echo "selfhost-check: FAIL - the 64-bit $N built the 32-bit image differently"; exit 1; }
    X="; the 64-bit build makes it too"
fi
python3 - "$ENG" "$D/A.img" $W <<'EOF' || exit 1
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
[ $W = 4 ] && N="$N (4-byte cells)"
echo "selfhost-check: PASS - $N self-hosting: A = B, $(stat -c %s "$D/A.img") bytes ($P)$X; the gate passed (the translator's: $(stat -c %s "$IMG"))"
