#!/bin/sh
# results/drafts/designs-table-741.sh - results/drafts/designs-table-741.py tested (Iteration 741): on 718's inputs (the
# records results/relf-designs-718.md, chain B's and chain C's readings, the ten in designs/README.md's order) it must
# print designs-table-718.py's rows byte for byte, and those are designs/README.md's table. PASS or FAIL. As the build
# user, from the repository's top; seconds.
set -u
O=/tmp/designs-table-741; rm -rf "$O"; mkdir -p "$O"
N=$(grep '^| `' designs/README.md | grep -v '^| `make`' | awk -F'|' '{gsub(/[ `]/, "", $2); gsub(/ /, "", $3); printf "%s%s=%s", (NR > 1 ? "," : ""), $2, $3}')
python3 -B results/drafts/designs-table-718.py > "$O/old.txt" 2>&1 || { echo "designs-table: FAIL - 718's script"; exit 1; }
python3 -B results/drafts/designs-table-741.py results/relf-designs-718.md "$N" results/chain-followup96-roles-b=B \
    results/chain-followup96-roles-c=C > "$O/new.txt" 2> "$O/new.err" || { echo "designs-table: FAIL - the general one ($(tail -n 1 "$O/new.err"))"; exit 1; }
f=
cmp -s "$O/old.txt" "$O/new.txt" || f="$f rows"
sed 's/  <!--.*//' "$O/new.txt" > "$O/new.rows"; grep '^| `' designs/README.md | grep -v '^| `make`' > "$O/readme.rows"
cmp -s "$O/new.rows" "$O/readme.rows" || f="$f readme"
echo "designs-table: $(wc -l < "$O/new.txt") rows; ${f:+FAIL -$f}${f:-PASS}"
