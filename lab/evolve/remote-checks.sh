#!/bin/sh
# lab/evolve/remote-checks.sh probe|start|gather|stop CHAIN [nowait] - the previous front
# measured on other machines alongside a seed chain (Iteration 315; the hosts in
# lab/evolve/REMOTES; results/drafts/runner-protocol.md). next-run.sh and chainctl.py call it:
#
#   probe   in the foreground, at a chain's start: each host tried (ssh, no password asked);
#           one that does not answer is said here and skipped
#   (Iteration 315: every host builds the stages - prebuilt too: evolve.py's setup refuses an
#   incomplete build/, and the test's prebuilt host failed so; the first run would have on dream)
#   start   in the seed step, before the evolution: a sample of the previous front
#           (xcheck.py --sample, and for prebuilt the laptop's binaries), the commit as a
#           bundle, copied to HOST:fve-xcheck/CHAIN/ and run there detached, to a deadline
#   gather  at the chain's end (chainctl.py pack): each host's results copied back,
#           xcheck.py --report into CHAIN/remote/HOST.md, the host's directory removed - a
#           host not done waits until its own deadline, unless nowait (stopped, interrupted)
#   stop    each host's run ended - by its process group, not by name
#
# Never costs the chain: whatever fails is a line in CHAIN/steps and the next host goes on.
# SSH and SCP may name stand-ins (the tests).
set -u
CMD=${1:-}; CHAIN=${2:-}; NOWAIT=${3:-}
[ -n "$CMD" ] && [ -d "$CHAIN" ] || { echo "usage: remote-checks.sh probe|start|gather|stop CHAIN [nowait]" >&2; exit 2; }
REPO=$(cd "$(dirname "$0")/../.." && pwd)
CONF=$REPO/lab/evolve/REMOTES
SSH=${SSH:-ssh}; SCP=${SCP:-scp}
O="-o BatchMode=yes -o ConnectTimeout=10"
R=$CHAIN/remote
RDIR=fve-xcheck/$(basename "$CHAIN")
note() { echo "remote $1: $2" >> "$CHAIN/steps"; echo "next-run: remote $1: $2"; }
conf() { sed -n '/^[^#]/p' "$CONF" 2>/dev/null; }

case $CMD in
probe)
    conf | grep -q . || exit 0
    mkdir -p "$R"; : > "$R/hosts"
    conf | while read -r host how n rounds minutes opts; do
        if $SSH $O "$host" true < /dev/null > /dev/null 2>&1; then echo "$host" >> "$R/hosts"; echo "next-run: remote $host answers - its check runs alongside the seed run"
        else note "$host" "does not answer (ssh, no password asked) - skipped"; fi
    done ;;
start)
    [ -s "$R/hosts" ] || exit 0
    rep=$(ls -d "$(dirname "$CHAIN")"/archived-*/build/evolve/report.md 2>/dev/null | sort | tail -1)
    [ -n "$rep" ] || { note all "no archived front to sample - skipped"; exit 0; }
    git -C "$REPO" bundle create "$R/repo.bundle" HEAD > /dev/null 2>&1 || { note all "git bundle failed - skipped"; exit 0; }
    conf | while read -r host how n rounds minutes opts; do
        grep -qx "$host" "$R/hosts" || continue
        H=$R/$host; mkdir -p "$H"
        until=$(( $(date +%s) + minutes * 60 ))
        set -- --n "$n" $opts
        [ "$how" = prebuilt ] && set -- "$@" --bundle "$H/bins.tar.gz"
        (cd "$REPO" && python3 lab/evolve/xcheck.py --sample "$rep" "$H/designs.json" "$@") > "$H/sample.log" 2>&1 \
            || { note "$host" "FAILED - the sample (remote/$host/sample.log)"; continue; }
        rm -rf "$REPO"/build/evolve/xcheck-b-* "$REPO/build/evolve/xcheck-bundle"
        cat > "$H/run.sh" << RUN
#!/bin/sh
# $host's check of $(basename "$CHAIN") (lab/evolve/remote-checks.sh): $how, $rounds rounds, until $(date -u -d @$until +%H:%M) UTC
cd "\$(dirname "\$0")" || exit 1
W=\$(pwd); echo \$\$ > "\$W/pid"
fail() { echo "\$*" > "\$W/FAILED"; echo 1 > "\$W/DONE"; exit 1; }
git clone -q "\$W/repo.bundle" "\$W/repo" || fail "the clone of the bundle failed"
cd "\$W/repo" || fail "no clone"
PRE=
LAYOUTS=1 bash tools/build-stages.sh > "\$W/build.log" 2>&1 || fail "build-stages.sh failed (build.log)"
if [ $how = prebuilt ]; then mkdir -p "\$W/bins" && tar -xzf "\$W/bins.tar.gz" -C "\$W/bins" || fail "the binaries did not unpack"; PRE="--prebuilt \$W/bins/bin"; fi
python3 lab/evolve/xcheck.py "\$W/designs.json" "\$W/out.json" --rounds $rounds --until $until \$PRE > "\$W/xcheck.log" 2>&1 || fail "xcheck.py failed (xcheck.log)"
echo 0 > "\$W/DONE"
RUN
        files="$R/repo.bundle $H/designs.json $H/run.sh"; [ "$how" = prebuilt ] && files="$files $H/bins.tar.gz"
        if $SSH $O "$host" "mkdir -p $RDIR" < /dev/null > "$H/ssh.log" 2>&1 \
            && $SCP -q $O $files "$host:$RDIR/" >> "$H/ssh.log" 2>&1 \
            && $SSH $O "$host" "cd $RDIR && setsid nohup sh run.sh > run.log 2>&1 < /dev/null &" < /dev/null >> "$H/ssh.log" 2>&1; then
            echo "$until" > "$H/until"
            note "$host" "started - $(python3 -c 'import json, sys; d = json.load(open(sys.argv[1])); print(len(d.get("designs", d)) if isinstance(d, dict) else len(d))' "$H/designs.json" 2>/dev/null || echo ?) designs, $how, until $(date -u -d @$until +%H:%M) UTC"
        else note "$host" "FAILED - copying or starting there (remote/$host/ssh.log)"; fi
    done ;;
stop)
    for H in "$R"/*/; do
        [ -f "$H/until" ] || continue; host=$(basename "$H")
        $SSH $O "$host" "[ -f $RDIR/pid ] && kill -TERM -\$(cat $RDIR/pid) 2>/dev/null; true" < /dev/null > /dev/null 2>&1 \
            && note "$host" "stopped" || note "$host" "could not be reached to stop"
    done ;;
gather)
    for H in "$R"/*/; do
        [ -f "$H/until" ] || continue; host=$(basename "$H"); until=$(cat "$H/until")
        if [ -z "$NOWAIT" ]; then
            while [ "$(date +%s)" -lt $(( until + 300 )) ] && ! $SSH $O "$host" "[ -f $RDIR/DONE ]" < /dev/null > /dev/null 2>&1; do sleep 30; done
        fi
        for f in out.json run.log xcheck.log build.log FAILED DONE; do $SCP -q $O "$host:$RDIR/$f" "$H/" > /dev/null 2>&1 || true; done
        $SSH $O "$host" "[ -f $RDIR/pid ] && kill -TERM -\$(cat $RDIR/pid) 2>/dev/null; rm -rf $RDIR" < /dev/null > /dev/null 2>&1 || true
        if [ -s "$H/out.json" ] && (cd "$REPO" && python3 lab/evolve/xcheck.py --report "$H/out.json") > "$R/$host.md" 2> "$H/report.log"; then
            note "$host" "gathered - remote/$host.md$( [ -f "$H/FAILED" ] && echo ", though: $(cat "$H/FAILED")")"
        else note "$host" "FAILED - no results$( [ -f "$H/FAILED" ] && echo ": $(cat "$H/FAILED")") (remote/$host/)"; fi
    done ;;
*) echo "remote-checks.sh: no command $CMD" >&2; exit 2 ;;
esac
exit 0
