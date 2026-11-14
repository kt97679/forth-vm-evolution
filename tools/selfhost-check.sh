#!/bin/sh
# tools/selfhost-check.sh [--self-test] [NAME] - a design's fixed point under the CV8 cross compiler (Iterations 667,
# 669; results/drafts/selfhost-plan-666.md). NAME is s6 (the ladder's s6-cv8b, the default) or a design in designs/.
# The design's translator-built image, on the design's engine, runs forth/cross-cv8.4 with the design's genes
# (stages/s6-genes.4, designs/NAME/genes.4 - lab/evolve/export-genes.py) and writes image A; A, booted on the same
# engine, runs it and writes B. A must equal B byte for byte, and A must pass the evolver's own gate (lab/evolve/
# evolve.py's alive(): the corpus against the cell engine, the kernel workload against the seed, the far tests, an
# ALLOT past the dictionary refused). --self-test first plants a fault - a bit of PARSE's body in A flipped - and fails
# unless the check catches it. From the repository's top, as the build user, in a built tree (tools/build-stages.sh);
# a design's engine is made if it is missing. Works in build/selfhost/check-NAME/; exit 1 on any failure.
set -e
cd "$(dirname "$0")/.."
TEST=; [ "$1" = --self-test ] && { TEST=1; shift; }
N=${1:-s6}
T=$(pwd) D=$(pwd)/build/selfhost/check-$N
if [ "$N" = s6 ]; then
    ENG=$T/build/s6-cv8b-64 IMG=$T/build/s6-cv8b-s64.img GENES=$T/stages/s6-genes.4
    [ -x "$ENG" ] && [ -f "$IMG" ] || { echo "selfhost-check: build first (tools/build-stages.sh)"; exit 1; }
else
    [ -f "designs/$N/genes.4" ] || { echo "selfhost-check: no designs/$N/genes.4 (lab/evolve/export-genes.py $N)"; exit 1; }
    ENG=$T/designs/$N/forth IMG=$T/designs/$N/image.img GENES=$T/designs/$N/genes.4
    [ -x "$ENG" ] || make -s -C "designs/$N" forth > /dev/null 2>&1 || { echo "selfhost-check: can't make designs/$N/forth"; exit 1; }
fi
rm -rf "$D"; mkdir -p "$D"
cp forth/*.4 "$D/"      # the cross compiler reads kernel.4 and the overlays the genes name
cp "$GENES" "$D/genes.4"
cross() {   # cross IMAGE OUT - run the cross compiler on IMAGE, its image moved to OUT
    rm -f "$D/cv8-self.img"
    ( cd "$D" && printf 'S" extend.4" INCLUDED\nS" genes.4" INCLUDED\nS" cross-cv8.4" INCLUDED\n' | timeout 300 "$ENG" "$1" > "$2.log" 2>&1 ) || true
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
python3 - "$ENG" "$D/A.img" <<'EOF' || exit 1
import os, sys, tempfile, shutil
eng, img = (os.path.abspath(a) for a in sys.argv[1:3])
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
pw = tempfile.mkdtemp(dir=E.EV)
for f in os.listdir(E.W):
    if f != 'kernel.img': os.symlink(os.path.join(E.W, f), os.path.join(pw, f))
shutil.copy(E.KREF, os.path.join(pw, 'kernel.img'))
try: E.alive(eng, img, pw, far=True)
except RuntimeError as e: print('selfhost-check: FAIL - the gate:', e); sys.exit(1)
finally: shutil.rmtree(pw, ignore_errors=True)
EOF
P=$(grep "pass 3" "$D/B.img.log" | sed 's/^cross-cv8: pass 3 - [0-9]* bytes, //')
echo "selfhost-check: PASS - $N self-hosting: A = B, $(stat -c %s "$D/A.img") bytes ($P); the gate passed (the translator's: $(stat -c %s "$IMG"))"
