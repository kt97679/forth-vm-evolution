#!/bin/sh
# results/drafts/selfhost-ids-714.sh [--32] LIST NAME=ID [NAME=ID ...] - tools/selfhost-lab.sh for designs off designs/
# (Iteration 714: the new roles' candidates, self-hosting phase 6): each ID's record from LIST (one JSON record a line -
# results/followup-seed96-roles-b.md) exported from the lab into build/selfhost-ids/out (lab/evolve/export-designs.py),
# its genes exported from that export (DESIGNS= lab/evolve/export-genes.py), checked there (DESIGNS= tools/selfhost-check.sh),
# then results/drafts/fusetab-714.py: the run-time compiler's tables (VAR-OPS, INL-OPS) and the five programs' code in
# the translator-built image and in A, on the design's engine. designs/ is not touched. The last line says PASS or FAIL.
W=; [ "$1" = --32 ] && { W=--32; shift; }
L=$1; shift
[ -f "$L" ] && [ $# -gt 0 ] || { echo "usage: results/drafts/selfhost-ids-714.sh [--32] LIST NAME=ID ..."; exit 2; }
X=$(pwd)/build/selfhost-ids
rm -rf "$X"; mkdir -p "$X"
P= N=
for p in "$@"; do
    i=${p#*=}; n=${p%%=*}
    grep "\"id\": \"$i\"" "$L" | head -n 1 >> "$X/db.jsonl"
    P="$P${P:+,}$p"; N="$N $n"
done
python3 lab/evolve/export-designs.py "$X/out" "$X/db.jsonl" "$P" > "$X/export.log" 2>&1 || { echo "selfhost-ids: FAIL - the export ($X/export.log)"; exit 1; }
DESIGNS="$X/out" python3 lab/evolve/export-genes.py $N > "$X/genes.log" 2>&1 || { echo "selfhost-ids: FAIL - the genes ($X/genes.log)"; exit 1; }
fail=0
for n in $N; do
    (cd "$X/out/$n" && make -s forth forth32 > "$X/make-$n.log" 2>&1) || { echo "selfhost-ids: FAIL - $n did not build ($X/make-$n.log)"; fail=1; continue; }
    DESIGNS="$X/out" sh tools/selfhost-check.sh $W "$n" > "$X/check-$n.log" 2>&1; s=$?
    echo "selfhost-ids: $n - $(tail -1 "$X/check-$n.log" | cut -c17-160)"
    [ $s = 0 ] || { fail=1; continue; }
    D=build/selfhost/check-$n; [ -n "$W" ] && D=$D-32
    E=$X/out/$n/forth T=$X/out/$n/image.img EA=$D/eng/forth C=8
    [ -n "$W" ] && { E=$X/out/$n/forth32 T=$X/out/$n/image32.img EA=$D/eng/forth32 C=4; }
    [ -x "$EA" ] || EA=$E
    python3 results/drafts/fusetab-714.py "$n" "$E" "$T" "$EA" "$D/A.img" $C || fail=1
done
[ $fail = 0 ] && echo "selfhost-ids: PASS - $# design(s) self-host, the tables and the programs' code the translator's" || { echo "selfhost-ids: FAIL"; exit 1; }
