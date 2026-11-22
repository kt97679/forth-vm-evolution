#!/bin/sh
# results/drafts/rebuild-rehearsal-723.sh [NAME] - after chain D's one-design rebuild rehearsed (Iteration 723): NAME
# (default small-jit, the step the card names - "small-jit made again if it changes") through
# results/drafts/roles-build-718.sh's two phases with its own record, in a scratch clone (/tmp/rb/tree, its own build/;
# the export in /tmp/fz as the real step's), now that all ten ship self-built (designs/TRANSLATOR-BUILT gone, 722). The
# same ID must give the same design: every file git has in designs/NAME the export's byte for byte - genes.4's and
# genes32.4's first line apart (a comment naming the export's path from the tree, which a clone elsewhere moves) - and
# phase 2's steps all 0, make selfhost every design at both widths. A JIT design (no ARM build) needs no cross GCC; for
# one that does, run phase 1's by-hand steps between (roles-build-718.sh's head). As the build user, from the top.
set -u
N=${1:-small-jit}; R=/tmp/rb
[ -f "designs/$N/record.json" ] || { echo "rebuild-rehearsal: no designs/$N"; exit 2; }
rm -rf "$R"; mkdir -p "$R"
git clone -q . "$R/tree" || exit 1
python3 -I -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))))' "designs/$N/record.json" > "$R/records.jsonl"
I=$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "designs/$N/record.json")
(sh results/drafts/roles-build-718.sh 1 "$R/tree" "$R/records.jsonl" "$N=$I" &&
 sh results/drafts/roles-build-718.sh 2 "$R/tree" "$R/records.jsonl" "$N=$I") > "$R/log" 2>&1
S=/tmp/fz/status; f=
grep -q '^phase 1 DONE' $S || f="$f phase-1"
grep -q '^DONE' $S || f="$f phase-2"
for k in selfhost-ship designs/forth make 'make test' 'make 32' 'make libc' pack; do grep -q "^$k=0" $S || f="$f $k"; done
nd=$(ls -d designs/*/record.json | wc -l)
grep -q "^make selfhost=0 $((2 * nd)) ok" $S || f="$f make-selfhost"
for x in $(git ls-files "designs/$N"); do
    e=/tmp/fz/$x
    case $x in
        */genes.4|*/genes32.4) [ "$(tail -n +2 "$e")" = "$(tail -n +2 "$x")" ] || f="$f $x" ;;
        *) cmp -s "$e" "$x" || f="$f $x" ;;
    esac
done
sed 's/ [0-9:]*$//' $S | sed 's/^/  /'
echo "rebuild-rehearsal: $N=$I ${f:+FAIL -$f}${f:-PASS - the same design, the build-out's steps all passed}"
