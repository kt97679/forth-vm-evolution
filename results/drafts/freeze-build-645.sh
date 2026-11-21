#!/bin/sh
# results/drafts/freeze-build-645.sh TREE RECORDS NAME=ID[,NAME=ID...] - the freeze's build-out, in order (Iteration 645;
# results/drafts/portable-plan-602.md, "Then the freeze": the final roles packed and exported from the final code - each
# engine the lab's bytes, every design right against s6 at both widths, make test, the C-library builds). Rehearsed at 645
# in a scratch tree with results/queued-freeze's two patches applied and today's ten roles; at the freeze, the same on
# master after the batch is applied, with the final roles' records. As the build user; one status line a step in
# /tmp/fz/status (sh tools/wait-for.sh /tmp/fz/status DONE), every log beside it:
#   1. the stages built, evolve.py --validate (7 of 7 IDENTICAL);
#   2. lab/evolve/export-designs.py /tmp/fz/designs - its own check: in a fresh directory each Makefile builds the lab's
#      engine byte for byte; then each exported design against TREE/designs/NAME (diff -r: what the freeze would change);
#   2b. (646) lab/evolve/export-arm.py: forth-arm for the designs without the JIT - the clang ones here (CROSS=1 setup:
#      lld, qemu-user), the GCC ones with --gcc arm-linux-gnueabihf-gcc when that cross GCC is installed (its package
#      removes gcc-multilib: install it after this script, run export-arm.py --gcc on the export, put gcc-multilib
#      back) - and on the Tegra itself: RAGECHECK_CMD='sh tools/rage-designs-check.sh' sh tools/rage-check.sh (the owner);
#   2c. (675) tools/selfhost-ship.sh on the export: the genes as Forth, each self-built image shipped (A = B, the gate),
#      the JIT designs' layout lines, `make selfhost` - last, as export-arm.py checks image32.img is the translator's
#      (an export-arm.py --gcc run by hand goes before it);
#   3. the export put in TREE/designs/ (designs/forth/ made again for all its designs: SOURCES=1), then `make`,
#      `make test`, `make selfhost`, `make 32` and `make libc` from TREE's top;
#   4. lab/evolve/pack-designs.py /tmp/fz/pkg - every design at both widths right on the nine workloads against s6.
set -u
T=${1:?TREE}; R=${2:?RECORDS}; NAMES=${3:?NAME=ID,...}
O=/tmp/fz; rm -rf "$O"; mkdir -p "$O"; S=$O/status; : > "$S"
st() { echo "$* $(date +%T)" >> "$S"; }
cd "$T" || { st "STOP - no $T"; exit 1; }
case $R in /*) ;; *) R=$T/$R ;; esac
IDS=$(echo "$NAMES" | tr ',' '\n' | sed 's/.*=//' | paste -sd, -)
env LAYOUTS=1 bash tools/build-stages.sh > $O/build.log 2>&1; st "build=$?"
python3 lab/evolve/evolve.py --validate > $O/validate.log 2>&1; st "validate=$? $(grep -c IDENTICAL $O/validate.log) of 7 IDENTICAL"
python3 lab/evolve/export-designs.py $O/designs "$R" "$NAMES" > $O/export.log 2>&1; st "export=$? $(tail -n 1 $O/export.log | cut -c1-120)"
python3 lab/evolve/export-arm.py $O/designs "$R" "$NAMES" > $O/export-arm.log 2>&1; st "export-arm=$? $(tail -n 1 $O/export-arm.log | cut -c1-100)"
if command -v arm-linux-gnueabihf-gcc > /dev/null; then python3 lab/evolve/export-arm.py $O/designs "$R" "$NAMES" --gcc arm-linux-gnueabihf-gcc > $O/export-arm-gcc.log 2>&1
    st "export-arm --gcc=$? $(tail -n 1 $O/export-arm-gcc.log | cut -c1-100)"; else st "export-arm --gcc: no cross GCC here - the GCC designs' forth-arm as designs/ has it"; fi
sh tools/selfhost-ship.sh $O/designs $(echo "$NAMES" | tr ',' '\n' | sed 's/=.*//') > $O/selfhost-ship.log 2>&1; st "selfhost-ship=$? $(tail -n 1 $O/selfhost-ship.log | cut -c1-100)"
same=0; diff=''
for nm in $(echo "$NAMES" | tr ',' '\n' | sed 's/=.*//'); do
    if diff -r -q "$O/designs/$nm" "designs/$nm" > $O/diff-$nm.log 2>&1; then same=$((same + 1)); else diff="$diff $nm"; fi
done
st "designs/ against the export: $same the same${diff:+, differ:$diff}"
for nm in $(echo "$NAMES" | tr ',' '\n' | sed 's/=.*//'); do rm -rf "designs/$nm" && cp -r "$O/designs/$nm" "designs/$nm"; done
rm -f designs/TRANSLATOR-BUILT; [ -f "$O/designs/TRANSLATOR-BUILT" ] && cp "$O/designs/TRANSLATOR-BUILT" designs/   # 714: the roles shipped translator-built, named
SOURCES=1 sh tools/selfhost-ship.sh designs > $O/sources.log 2>&1; st "designs/forth=$? $(tail -n 1 $O/sources.log | cut -c1-80)"
make > $O/make.log 2>&1; st "make=$?"
make test > $O/test.log 2>&1; st "make test=$? $(grep -c ': ok' $O/test.log) ok"
make selfhost > $O/selfhost.log 2>&1; st "make selfhost=$? $(grep -c ' ok - rebuilt' $O/selfhost.log) ok"
make 32 > $O/make32.log 2>&1; st "make 32=$?"
make libc > $O/libc.log 2>&1; st "make libc=$?"
python3 lab/evolve/pack-designs.py $O/pkg "$R" "$IDS" > $O/pack.log 2>&1; st "pack=$? $(grep -c -w right $O/pack.log) lines right"
st DONE
