#!/bin/sh
# tools/selfhost-check.sh [--self-test] - the CV8 cross compiler's fixed point (Iteration 667;
# results/drafts/selfhost-plan-666.md, phase 1). s6-cv8b's translator-built image runs forth/cross-cv8.4 and writes
# image A; A, booted, runs it and writes B. A must equal B byte for byte, and A must pass the evolver's own gate
# (lab/evolve/evolve.py's alive(): the corpus against the cell engine, the kernel workload against the seed, the far
# tests, an ALLOT past the dictionary refused). --self-test first plants a fault - a bit of PARSE's body in A flipped - and
# fails unless the check catches it. From the repository's top, as the build user, in a
# built tree (tools/build-stages.sh). Works in build/selfhost/; exit 1 on any failure.
set -e
cd "$(dirname "$0")/.."
T=$(pwd) ENG=$(pwd)/build/s6-cv8b-64 IMG=$(pwd)/build/s6-cv8b-s64.img D=$(pwd)/build/selfhost/check
[ -x "$ENG" ] && [ -f "$IMG" ] || { echo "selfhost-check: build first (tools/build-stages.sh)"; exit 1; }
rm -rf "$D"; mkdir -p "$D"
for f in extend.4 kernel.4 cv8.4 cv8b.4 cross-cv8.4; do cp "forth/$f" "$D/"; done
cross() {   # cross IMAGE OUT - run the cross compiler on IMAGE, its image moved to OUT
    rm -f "$D/cv8-self.img"
    ( cd "$D" && printf 'S" extend.4" INCLUDED\nS" cross-cv8.4" INCLUDED\n' | timeout 300 "$ENG" "$1" > "$2.log" 2>&1 ) || true
    [ -s "$D/cv8-self.img" ] && mv "$D/cv8-self.img" "$2"
}
cross "$IMG" "$D/A.img" || { echo "selfhost-check: FAIL - the translator-built s6 wrote no image ($D/A.img.log)"; exit 1; }
if [ "$1" = --self-test ]; then
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
echo "selfhost-check: PASS - s6-cv8b self-hosting: A = B, $(stat -c %s "$D/A.img") bytes; the gate passed (the translator's s6: $(stat -c %s "$IMG"))"
