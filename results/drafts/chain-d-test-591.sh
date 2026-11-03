#!/bin/sh
# results/drafts/chain-d-test-591.sh ROOT [guard] - chain D's two mechanisms tested on this machine (Iteration 591).
# 1. The laptop's guard: next-run.sh's then_next, cut out and run with stand-ins - a repeat of the same experiment goes
#    on while lab/evolve/repeat-fits.sh says another session ends by the deadline, else the chain is packed (a stand-in
#    chainctl.py) and the rest skipped; a different next step is never guarded. "guard" runs this part alone.
#    597: run as next-run.sh runs it - under set -eu, the EXIT trap (unpacked) armed as after a step's pack: set -u
#    alone hid chain D's fault (repeat-fits' "no" ended the shell at "r_=$(...); rc_=$?", the chain never packed). The
#    trap itself (an exit in that window packs the chain; stopping leaves it to stop) and ncpus (1 without --cpus).
# 2. A REMOTES line's --sessions, end to end with 570's ssh and scp stand-ins (/tmp/e2e/host the host): a dream-like
#    pair - prebuilt32 up to 3 sessions in 30 minutes, prebuilt64 (--from it) up to 9 in 4 minutes, so its deadline
#    stops it - two of the shortlist's designs at 1 round; gather's reports, one a session.
set -u; ROOT=$(cd "$1" && pwd); ok=0; bad=0
t() { if [ "$1" = "$2" ]; then ok=$((ok + 1)); echo "ok   $3"; else bad=$((bad + 1)); echo "FAIL $3: got '$1', want '$2'"; fi; }
G=/tmp/guard-591; rm -rf $G; mkdir -p $G/repo/lab/evolve $G/chain/remote/h-a
cp "$ROOT/lab/evolve/repeat-fits.sh" $G/repo/lab/evolve/
printf 'import sys\nopen("%s/packed", "w").write(sys.argv[3])\n' $G > $G/repo/lab/evolve/chainctl.py
printf 'echo "exec $*" > %s/execd\n' $G > $G/repo/lab/evolve/next-run.sh
for f in then_next unpacked ncpus; do sed -n "/^$f() {/,/^}/p" "$ROOT/lab/evolve/next-run.sh"; done > $G/fn.sh
guard() {   # $1 the step's length in s, $2 the deadline from now in s, $3 the next step's words
    rm -f $G/packed $G/execd; : > $G/chain/steps; echo "line" > $G/chain/line; echo running > $G/chain/status
    echo $(( $(date +%s) + $2 )) > $G/chain/remote/h-a/until
    ( set -eu; say() { echo "next-run: $*"; }; REPO=$G/repo; KIND=experiment; CHAIN=$G/chain
      STEPLINE='experiment loadtest.py --ids x.md --rounds 10'; THEN="$3"; STEP_T0=$(( $(date +%s) - $1 ))
      . $G/fn.sh; trap unpacked EXIT; then_next ) > $G/out 2>&1
    if [ -f $G/packed ]; then echo "packed $(cat $G/packed)"; elif [ -f $G/execd ]; then echo "next"; else echo "neither"; fi
}
R='experiment loadtest.py --ids x.md --rounds 10'
t "$(guard 600 3600 "$R then $R")" next "a repeat with time for it goes on - the exec runs no EXIT trap"
t "$(guard 600 300 "$R then $R")" "packed done" "a repeat past the deadline packs the chain"
t "$(grep -c 'skipped: 2 more' $G/chain/steps)" 1 "the skip counts both repeats left"
t "$(guard 600 300 "experiment xcheck.py --other")" next "a different next step is never guarded"
t "$(guard 600 300 "$R")" "packed done" "the last repeat guarded too"
net() {     # 597: the shell ends in the window after a step's pack; $1 the chain's status
    rm -f $G/packed; : > $G/chain/steps; echo "$1" > $G/chain/status
    ( set -eu; REPO=$G/repo; CHAIN=$G/chain; . $G/fn.sh; trap unpacked EXIT; false ) > $G/out 2>&1
    if [ -f $G/packed ]; then echo "packed $(cat $G/packed)"; else echo "neither"; fi
}
t "$(net running)" "packed done-some-failed" "an exit after a step's pack packs the chain"
t "$(grep -c '^FAILED after the step' $G/chain/steps)" 1 "that exit recorded in steps"
t "$(net stopping)" neither "stopping: the trap leaves the pack to stop"
t "$( (set -eu; . $G/fn.sh; a=$(ncpus '--rounds 6'); b=$(ncpus '--rounds 6 --cpus 2,8'); echo "$a $b") 2>&1)" "1 2" "ncpus: 1 without --cpus, under set -e"
rm $G/chain/remote/h-a/until; touch -d '-700 minutes' $G/chain/line
t "$(sh $G/repo/lab/evolve/repeat-fits.sh $G/chain 60 > /dev/null; echo $?)" 1 "no remote line: the chain's start + 690 minutes"
touch $G/chain/line
t "$(sh $G/repo/lab/evolve/repeat-fits.sh $G/chain 60 > /dev/null; echo $?)" 0 "no remote line, a fresh chain: fits"
[ "${2:-}" = guard ] && { echo "guard: $ok ok, $bad failed"; exit $bad; }

E=/tmp/e2e; rm -rf $E; mkdir -p $E/runs/archived-86/build/evolve $E/runs/chain-591
cat > $E/ssh << 'S'
#!/bin/sh
while [ $# -gt 0 ]; do case $1 in -o) shift 2 ;; -q) shift ;; *) break ;; esac; done
shift; mkdir -p /tmp/e2e/host; cd /tmp/e2e/host && exec sh -c "$*"
S
cat > $E/scp << 'S'
#!/bin/sh
while [ $# -gt 0 ]; do case $1 in -o) shift 2 ;; -q) shift ;; *) break ;; esac; done
n=$#; i=0; src=""; for a in "$@"; do i=$((i + 1)); if [ $i -lt $n ]; then src="$src $a"; else dst=$a; fi; done
m() { case $1 in *:*) echo "/tmp/e2e/host/${1#*:}" ;; *) echo "$1" ;; esac; }
for s in $src; do cp "$(m "$s")" "$(m "$dst")" || exit 1; done
S
chmod 755 $E/ssh $E/scp
cp "$ROOT/results/evolve-amd-ryzen-7-pro-8840hs-seed86.md" $E/runs/archived-86/build/evolve/report.md
grep '^{"' "$ROOT/results/shortlist-seed86.md" | head -2 > $E/two.md
printf 'dream.lan    prebuilt32  1  1  30  --cell 4 --rejected 1 --sessions 3 --also @%s\ndream.lan    prebuilt64  1  1  4  --from prebuilt32 --sessions 9\n' $E/two.md > $E/remotes
cd "$ROOT" && export SSH=$E/ssh SCP=$E/scp REMOTES_FILE=$E/remotes; C=$E/runs/chain-591
sh lab/evolve/remote-checks.sh probe $C; s=$(date +%s)
sh lab/evolve/remote-checks.sh start $C; echo "start: $(( $(date +%s) - s )) s"
while [ ! -f $E/host/fve-xcheck/chain-591/prebuilt64/DONE ] || [ ! -f $E/host/fve-xcheck/chain-591/prebuilt32/DONE ]; do sleep 10; done
cat $E/host/fve-xcheck/chain-591/*/sessions.txt
sh lab/evolve/remote-checks.sh gather $C; cat $C/steps
t "$(grep -c '^session [0-9]*:' $C/remote/dream.lan-prebuilt32/sessions.txt)" 3 "prebuilt32: its 3 sessions"
t "$(ls $C/remote/dream.lan-prebuilt32.md $C/remote/dream.lan-prebuilt32-s2.md $C/remote/dream.lan-prebuilt32-s3.md | wc -l)" 3 "prebuilt32: a report a session"
n64=$(grep -c '^session [0-9]*:' $C/remote/dream.lan-prebuilt64/sessions.txt)
t "$( [ "$n64" -ge 1 ] && [ "$n64" -lt 9 ] && echo yes)" yes "prebuilt64: stopped by its deadline ($n64 of 9)"
t "$(grep -c 'not started' $C/remote/dream.lan-prebuilt64/sessions.txt)" 1 "prebuilt64: the stop said"
t "$(ls $C/remote/dream.lan-prebuilt64*.md | wc -l)" "$n64" "prebuilt64: a report a session"
t "$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["designs"]))' $C/remote/dream.lan-prebuilt32/out-s3.json)" \
  "$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["designs"]))' $C/remote/dream.lan-prebuilt32/out.json)" "the same designs each session"
t "$(ls $E/host/fve-xcheck/chain-591 2> /dev/null | wc -l)" 0 "the host's directories removed"
echo "chain-d-test-591: $ok ok, $bad failed"; exit $bad
