#!/bin/sh
# results/drafts/ship-rehearsal-714.sh - the roles step's export and ship rehearsed with the provisional roles (Iteration
# 714, while chain C runs): results/drafts/freeze-build-645.sh's steps 2 and 2c in a scratch directory (/tmp/ship-rh) -
# lab/evolve/export-designs.py of chain B's leaders under the ten role names (the smallest 219878ec89, the rest kept
# as chain B leaves them), then tools/selfhost-ship.sh on the export, twice (idempotent). portable-fastest is
# d727605472, which the cross compiler cannot yet build (--factor, =I?BRANCH / DUP?NBRANCH): it must keep its
# translator-built images, named in TRANSLATOR-BUILT, without `make selfhost` rules, and the other nine ship. Then the
# checks; PASS or FAIL. As the build user, from the repository's top, in a built tree. About 20 minutes: run it detached.
set -u
O=/tmp/ship-rh; rm -rf "$O"; mkdir -p "$O"
NAMES=fastest-x86-64=9b15ba26f7,fastest-x86-32=ea782c6094,best-all-round=df097ba2e2,small-jit=c6f1c1331b,portable-fastest=d727605472,portable-arm=a8d35bdccc,portable-knee=48a012411a,portable-small=ae99617f06,least-memory=fb0d57c8a2,smallest=219878ec89
for i in $(echo "$NAMES" | tr ',' '\n' | sed 's/.*=//'); do grep -h "\"id\": \"$i\"" results/followup-seed96-roles-b.md | head -n 1; done > "$O/db.jsonl"
python3 lab/evolve/export-designs.py "$O/designs" "$O/db.jsonl" "$NAMES" > "$O/export.log" 2>&1; echo "export: $? - $(tail -n 1 "$O/export.log" | cut -c1-120)"
N=$(echo "$NAMES" | tr ',' '\n' | sed 's/=.*//' | tr '\n' ' ')
sh tools/selfhost-ship.sh "$O/designs" $N > "$O/ship1.log" 2>&1; echo "ship 1: $? - $(tail -n 1 "$O/ship1.log" | cut -c1-160)"
md5sum "$O"/designs/*/image.img "$O"/designs/*/image32.img > "$O/sums1"; cp "$O/designs/TRANSLATOR-BUILT" "$O/tb1" 2> /dev/null
sh tools/selfhost-ship.sh "$O/designs" $N > "$O/ship2.log" 2>&1; echo "ship 2: $? - $(tail -n 1 "$O/ship2.log" | cut -c1-160)"
md5sum "$O"/designs/*/image.img "$O"/designs/*/image32.img > "$O/sums2"
f=
grep -q '^portable-fastest ' "$O/designs/TRANSLATOR-BUILT" 2> /dev/null || f="$f; portable-fastest not named"
[ "$(grep -c -v '^#' "$O/designs/TRANSLATOR-BUILT" 2> /dev/null)" = 1 ] || f="$f; TRANSLATOR-BUILT names $(grep -c -v '^#' "$O/designs/TRANSLATOR-BUILT" 2> /dev/null) designs"
grep -q '^selfhost:' "$O/designs/portable-fastest/Makefile" && f="$f; portable-fastest has selfhost rules"
for n in $N; do [ "$n" = portable-fastest ] && continue
    grep -q '^selfhost:' "$O/designs/$n/Makefile" || f="$f; $n has no selfhost rules"
    (cd "$O/designs/$n" && make -s selfhost selfhost32 > "$O/make-$n.log" 2>&1) || f="$f; $n: make selfhost failed"; done
ORIG=$(mktemp -d); python3 lab/evolve/export-designs.py "$ORIG/d" "$O/db.jsonl" portable-fastest=d727605472 > /dev/null 2>&1
cmp -s "$ORIG/d/portable-fastest/image.img" "$O/designs/portable-fastest/image.img" && cmp -s "$ORIG/d/portable-fastest/image32.img" "$O/designs/portable-fastest/image32.img" || f="$f; portable-fastest's images not the converter's"
rm -rf "$ORIG"
cmp -s "$O/sums1" "$O/sums2" || f="$f; the second ship changed an image"
cmp -s "$O/tb1" "$O/designs/TRANSLATOR-BUILT" || f="$f; the second ship changed TRANSLATOR-BUILT"
echo "ship-rehearsal: $(echo $N | wc -w) roles, $(grep -c -v '^#' "$O/designs/TRANSLATOR-BUILT" 2> /dev/null) translator-built - ${f:+FAIL$f}${f:-PASS}"
