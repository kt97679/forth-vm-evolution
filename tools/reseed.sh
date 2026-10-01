#!/bin/sh
# tools/reseed.sh - bootstrap a changed kernel.4 into the committed seeds.
#
# Every image this project builds starts from forth/kernel-seed.img (and
# forth/kernel32-seed.img): prebuilt binaries of the kernel. Editing
# kernel.4 changes what gets compiled, NOT the compiler doing it, so a
# kernel change has no effect until it is bootstrapped into the seeds.
# This does that, and refuses to install anything that fails a check.
#
#   8-byte seed   compile kernel.4 with the old seed (stage 1), then with
#                 the result (stage 2). Stage 2 must equal stage 1: the new
#                 kernel must compile itself to itself - a fixed point.
#   4-byte seed   compiled on THIS host by cross.4 with TARGET-CELL-BYTES
#                 set to 4, so a 64-bit host with no 32-bit C library can
#                 still produce it. Built twice - by the old seed and by
#                 the new one - and the two must be identical, since the
#                 output may depend only on the source, never on which
#                 correct compiler produced it.
#
# Proven before first use: this host, targeting 4-byte cells, reproduces
# the committed kernel32-seed.img byte for byte from unchanged sources.
# A 4-byte fixed point can only be checked on a 32-bit host; run
# tools/build-stages.sh and tools/run-tests.sh there afterwards.
#
# Usage: tools/reseed.sh        (then rebuild: tools/build-stages.sh)
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
ENG="$W/relf-64"
cc -O2 -o "$ENG" "$ROOT/engine/relf.c"
# The committed seed was made for the committed engines. When a change
# alters what a primitive DOES - not only what kernel.4 says, as when
# slots 30 and 31 went from EMIT and KEY to WRITE and READ - the old seed
# cannot run on the new engine. So every step that runs the OLD seed runs
# on the engine as committed (OLD_ENGINE_REV, default HEAD), and every
# step that runs the new seed on the engine in the tree. With the engines
# unchanged, the two are the same program.
OLD_ENGINE_REV=${OLD_ENGINE_REV:-HEAD}
ENG_OLD="$W/relf-64-old"
git -C "$ROOT" show "$OLD_ENGINE_REV:engine/relf.c" > "$W/relf-old.c"
cc -O2 -o "$ENG_OLD" "$W/relf-old.c"
cp "$ROOT"/forth/kernel.4 "$ROOT"/forth/extend.4 "$ROOT"/forth/cross.4 "$W/"
sed 's/^8 TARGET-CELL-BYTES !/4 TARGET-CELL-BYTES !/' "$ROOT/forth/cross.4" > "$W/cross32.4"
grep -q '^4 TARGET-CELL-BYTES !' "$W/cross32.4" || { echo "cannot retarget cross.4"; exit 1; }

# compile SRC (cross.4 or cross32.4) with IMAGE; the result replaces IMAGE
xc() ( cd "$W" && cp "$1" kernel.img &&
       printf 'S" extend.4" INCLUDED\nS" %s" INCLUDED\n' "$2" | "$4" kernel.img >/dev/null 2>&1 &&
       cp kernel.img "$3" )

xc "$ROOT/forth/kernel-seed.img" cross.4   "$W/s1.img"      "$ENG_OLD"
xc "$W/s1.img"                   cross.4   "$W/s2.img"      "$ENG"
cmp -s "$W/s1.img" "$W/s2.img" || { echo "FAIL: 8-byte kernel is not a fixed point"; exit 1; }
echo "8-byte kernel: fixed point reached ($(wc -c < "$W/s1.img") bytes)"

xc "$ROOT/forth/kernel-seed.img" cross32.4 "$W/k32-old.img"  "$ENG_OLD"
xc "$W/s1.img"                   cross32.4 "$W/k32-new.img"  "$ENG"
cmp -s "$W/k32-old.img" "$W/k32-new.img" || { echo "FAIL: 4-byte kernel depends on which seed built it"; exit 1; }
echo "4-byte kernel: identical from old and new seed ($(wc -c < "$W/k32-new.img") bytes)"

cp "$W/s1.img"      "$ROOT/forth/kernel-seed.img"
cp "$W/k32-new.img" "$ROOT/forth/kernel32-seed.img"
echo "seeds installed; now run tools/build-stages.sh and tools/run-tests.sh"
