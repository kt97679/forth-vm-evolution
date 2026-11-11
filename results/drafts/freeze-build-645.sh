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
#   3. the export put in TREE/designs/, then `make`, `make test`, `make 32` and `make libc` from TREE's top;
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
same=0; diff=''
for nm in $(echo "$NAMES" | tr ',' '\n' | sed 's/=.*//'); do
    if diff -r -q "$O/designs/$nm" "designs/$nm" > $O/diff-$nm.log 2>&1; then same=$((same + 1)); else diff="$diff $nm"; fi
done
st "designs/ against the export: $same the same${diff:+, differ:$diff}"
for nm in $(echo "$NAMES" | tr ',' '\n' | sed 's/=.*//'); do rm -rf "designs/$nm" && cp -r "$O/designs/$nm" "designs/$nm"; done
make > $O/make.log 2>&1; st "make=$?"
make test > $O/test.log 2>&1; st "make test=$? $(grep -c ': ok' $O/test.log) ok"
make 32 > $O/make32.log 2>&1; st "make 32=$?"
make libc > $O/libc.log 2>&1; st "make libc=$?"
python3 lab/evolve/pack-designs.py $O/pkg "$R" "$IDS" > $O/pack.log 2>&1; st "pack=$? $(grep -c -w right $O/pack.log) lines right"
st DONE
