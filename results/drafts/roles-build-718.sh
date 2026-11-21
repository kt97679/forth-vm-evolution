#!/bin/sh
# results/drafts/roles-build-718.sh PHASE TREE RECORDS NAME=ID[,NAME=ID...] - results/drafts/freeze-build-645.sh in two
# phases around the cross GCC (Iteration 718, the new roles' build-out): its package removes gcc-multilib, which the stages
# and the 32-bit x86 exports need, and export-arm.py --gcc must run on the export after the clang ARM builds and before
# selfhost-ship.sh (which replaces image32.img). So:
#   PHASE 1 (as the build user): the stages, validate, export-designs.py, export-arm.py (the clang designs) - /tmp/fz;
#   by hand: as root `apt-get install -y gcc-arm-linux-gnueabihf` (gcc-multilib goes), as the build user
#     `python3 lab/evolve/export-arm.py /tmp/fz/designs RECORDS NAMES --gcc arm-linux-gnueabihf-gcc`, as root
#     `apt-get install -y gcc-multilib` (the cross GCC goes);
#   PHASE 2 (as the build user): selfhost-ship.sh on the export and the rest of 645's steps, unchanged.
# The Tegra's own GCC (16) then confirms the GCC designs' bytes: RAGECHECK_CMD='sh tools/rage-designs-check.sh' sh tools/rage-check.sh.
set -u
P=${1:?PHASE}; shift
set -u
T=${1:?TREE}; R=${2:?RECORDS}; NAMES=${3:?NAME=ID,...}
O=/tmp/fz; [ "$P" = 1 ] && rm -rf "$O"; mkdir -p "$O"; S=$O/status; [ "$P" = 1 ] && : > "$S"
st() { echo "$* $(date +%T)" >> "$S"; }
cd "$T" || { st "STOP - no $T"; exit 1; }
case $R in /*) ;; *) R=$T/$R ;; esac
IDS=$(echo "$NAMES" | tr ',' '\n' | sed 's/.*=//' | paste -sd, -)
if [ "$P" = 1 ]; then
    env LAYOUTS=1 bash tools/build-stages.sh > $O/build.log 2>&1; st "build=$?"
    python3 lab/evolve/evolve.py --validate > $O/validate.log 2>&1; st "validate=$? $(grep -c IDENTICAL $O/validate.log) of 7 IDENTICAL"
    python3 lab/evolve/export-designs.py $O/designs "$R" "$NAMES" > $O/export.log 2>&1; st "export=$? $(tail -n 1 $O/export.log | cut -c1-120)"
    python3 lab/evolve/export-arm.py $O/designs "$R" "$NAMES" > $O/export-arm.log 2>&1; st "export-arm=$? $(tail -n 1 $O/export-arm.log | cut -c1-100)"
    st "phase 1 DONE"; exit 0
fi
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
