#!/bin/sh
# tools/selfhost-lab.sh [--32] NAME [NAME ...] - tools/selfhost-check.sh on the lab's state, not designs/'s (Iteration 683).
# designs/ holds the shipped roles: each engine's source, its tag-2 map (src/vm-tag2-one.h) and its genes (genes.4) as
# they were exported. selfhost-check runs those against today's cross compiler and kernel sources, so after a change to
# the engine or the converter it can fail on a mismatch the lab does not have - 681's unpadded strings: jit.c's skip in
# the jitexec designs' shipped source, and fastest-x86-64's tag-2 map (ALIGNED's rank moved with its uses). Here each
# NAME is exported from the lab into a scratch designs directory (lab/evolve/export-designs.py, its record from
# designs/NAME/record.json), built, its genes exported from that export (DESIGNS= lab/evolve/export-genes.py), and
# checked there (DESIGNS= tools/selfhost-check.sh). designs/ is not touched. The last line says PASS or FAIL.
W=; [ "$1" = --32 ] && { W=--32; shift; }
[ $# -gt 0 ] || { echo "usage: tools/selfhost-lab.sh [--32] NAME [NAME ...]"; exit 2; }
R=$(pwd) X=$(pwd)/build/selfhost-lab
rm -rf "$X"; mkdir -p "$X"
P=
for n in "$@"; do
    [ -f "designs/$n/record.json" ] || { echo "selfhost-lab: no designs/$n/record.json"; exit 1; }
    python3 -c "import json; print(json.dumps(json.load(open('designs/$n/record.json'))))" >> "$X/db.jsonl"
    P="$P${P:+,}$n=$(python3 -c "import json; print(json.load(open('designs/$n/record.json'))['id'])")"
done
python3 lab/evolve/export-designs.py "$X/out" "$X/db.jsonl" "$P" > "$X/export.log" 2>&1 || { echo "selfhost-lab: FAIL - the export ($X/export.log)"; exit 1; }
DESIGNS="$X/out" python3 lab/evolve/export-genes.py "$@" > "$X/genes.log" 2>&1 || { echo "selfhost-lab: FAIL - the genes ($X/genes.log)"; exit 1; }
fail=0
for n in "$@"; do
    (cd "$X/out/$n" && make -s forth forth32 > "$X/make-$n.log" 2>&1) || { echo "selfhost-lab: FAIL - $n did not build ($X/make-$n.log)"; fail=1; continue; }
    DESIGNS="$X/out" sh tools/selfhost-check.sh $W "$n" > "$X/check-$n.log" 2>&1; s=$?
    echo "selfhost-lab: $n - $(tail -1 "$X/check-$n.log" | cut -c17-140)"
    [ $s = 0 ] || fail=1
done
[ $fail = 0 ] && echo "selfhost-lab: PASS - $# design(s) self-host on the lab's engine, map and genes" || { echo "selfhost-lab: FAIL"; exit 1; }
