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
#           bundle, copied to HOST:fve-xcheck/CHAIN/ and run there detached, to a deadline.
#           Iteration 379: only the sampling before the evolution (it builds on the laptop's
#           CPUs, which the run's timings need); the copying and starting go to remote/launch.sh,
#           in the background - seed 57's run waited 52 minutes for them, 38 of it the Tegra's
#   gather  at the chain's end (chainctl.py pack): each host's results copied back,
#           xcheck.py --report into CHAIN/remote/HOST.md, the host's directory removed - a
#           host not done waits until its own deadline, unless nowait (stopped, interrupted)
#   stop    each host's run ended - by its process group, not by name
#
# Iteration 381 (the owner): probes - each host's connection timed, each check's copy timed with
# its bytes (remote/HOST-HOW/transfer.txt), and the host's load at the check's start and every 30 s
# while it runs (load-start.txt, load.log): both appended to the host's report by gather.
#
# Never costs the chain: whatever fails is a line in CHAIN/steps and the next host goes on.
# SSH and SCP may name stand-ins (the tests), and REMOTES_FILE the hosts' file (Iteration 379).
set -u
CMD=${1:-}; CHAIN=${2:-}; NOWAIT=${3:-}
[ -n "$CMD" ] && [ -d "$CHAIN" ] || { echo "usage: remote-checks.sh probe|start|gather|stop CHAIN [nowait]" >&2; exit 2; }
REPO=$(cd "$(dirname "$0")/../.." && pwd)
CONF=${REMOTES_FILE:-$REPO/lab/evolve/REMOTES}
SSH=${SSH:-ssh}; SCP=${SCP:-scp}
O="-o BatchMode=yes -o ConnectTimeout=10 -o ControlMaster=auto -o ControlPath=/tmp/fve-ssh-%C -o ControlPersist=120"   # 379: one connection a host
R=$CHAIN/remote
RDIR=fve-xcheck/$(basename "$CHAIN")
note() { echo "remote $1: $2" >> "$CHAIN/steps"; echo "next-run: remote $1: $2"; }
conf() { sed -n '/^[^#]/p' "$CONF" 2>/dev/null; }

case $CMD in
probe)
    conf | grep -q . || exit 0
    mkdir -p "$R"; : > "$R/hosts"
    conf | while read -r host how n rounds minutes opts; do
        t0=$(date +%s%N)                                              # Iteration 381: the connection, timed
        if $SSH $O "$host" true < /dev/null > /dev/null 2>&1; then ms=$(( ($(date +%s%N) - t0) / 1000000 )); echo "$host $ms" >> "$R/connect"; echo "$host" >> "$R/hosts"; echo "next-run: remote $host answers in $ms ms - its check runs alongside the seed run"
        else note "$host" "does not answer (ssh, no password asked) - skipped"; fi
    done ;;
start)
    [ -s "$R/hosts" ] || exit 0
    rep=$(ls -d "$(dirname "$CHAIN")"/archived-*/build/evolve/report.md 2>/dev/null | sort | tail -1)
    [ -n "$rep" ] || { note all "no archived front to sample - skipped"; exit 0; }
    git -C "$REPO" bundle create "$R/repo.bundle" HEAD > /dev/null 2>&1 || { note all "git bundle failed - skipped"; exit 0; }
    # Iteration 331: a check is a host and a mode - dream.lan has two (64-bit and 32-bit x86) -
    # each with its own directories; one host's checks run one after another (run.sh waits on the
    # host's lock), each deadline from its own start; the laptop waits at most their sum
    : > "$R/queued"
    L=$R/launch.sh                                                   # Iteration 379: the copying, in the background
    printf '#!/bin/sh\n# the copying and starting of %s'"'"'s checks (remote-checks.sh start, Iteration 379)\n' "$(basename "$CHAIN")" > "$L"
    printf 'note() { echo "remote $1: $2" >> "%s/steps"; echo "next-run: remote $1: $2"; }\n' "$CHAIN" >> "$L"
    conf | while read -r host how n rounds minutes opts; do
        grep -qx "$host" "$R/hosts" || continue
        CHK=$host-$how; H=$R/$CHK; RD=$RDIR/$how; mkdir -p "$H"
        before=$(awk -v h="$host" '$1 == h {s += $2} END {print s + 0}' "$R/queued"); echo "$host $minutes" >> "$R/queued"
        offset=$(( (before + minutes) * 60 ))                         # 379: the deadline counted from the start
        case " $opts " in *" --from "*)                               # Iteration 335: another check's designs
            frm=$(printf '%s\n' $opts | awk 'p {print; exit} $1 == "--from" {p = 1}')
            [ -s "$R/$host-$frm/designs.json" ] || { note "$CHK" "FAILED - its pair $host-$frm sampled nothing"; continue; }
            opts=$(printf ' %s' $opts | sed "s| --from $frm| --ids $R/$host-$frm/designs.json|") ;;
        esac
        set -- --n "$n" $opts
        case $how in prebuilt|prebuilt32|prebuilt64) set -- "$@" --bundle "$H/bins.tar.gz" ;; esac
        (cd "$REPO" && python3 lab/evolve/xcheck.py --sample "$rep" "$H/designs.json" "$@") > "$H/sample.log" 2>&1 \
            || { note "$CHK" "FAILED - the sample (remote/$CHK/sample.log)"; continue; }
        rm -rf "$REPO"/build/evolve/xcheck-b-* "$REPO/build/evolve/xcheck-bundle"
        cat > "$H/run.sh" << RUN
#!/bin/sh
# $CHK's check of $(basename "$CHAIN") (lab/evolve/remote-checks.sh): $how, $rounds rounds, $minutes minutes from its start
cd "\$(dirname "\$0")" || exit 1
W=\$(pwd); echo \$\$ > "\$W/pid"
# Iteration 381: the host's load - at the start, and every 30 s while this check runs
{ echo "start \$(date +%s)"; echo "nproc \$(nproc 2>/dev/null || grep -c ^processor /proc/cpuinfo)"; echo "loadavg \$(cat /proc/loadavg)"; ps -eo pcpu,comm --sort=-pcpu 2>/dev/null | sed -n '2,6p'; } > "\$W/load-start.txt" 2>&1
( while kill -0 \$\$ 2>/dev/null; do echo "\$(date +%s) \$(cut -d' ' -f1-3 /proc/loadavg)" >> "\$W/load.log"; sleep 30; done ) &
fail() { echo "\$*" > "\$W/FAILED"; echo 1 > "\$W/DONE"; exit 1; }
exec 9> "\$W/../.lock"; flock 9 || fail "the host's lock"          # one check at a time on a host
UNTIL=\$(( \$(date +%s) + $minutes * 60 ))
git clone -q "\$W/repo.bundle" "\$W/repo" || fail "the clone of the bundle failed"
cd "\$W/repo" || fail "no clone"
PRE=
LAYOUTS=1 bash tools/build-stages.sh > "\$W/build.log" 2>&1 || fail "build-stages.sh failed (build.log)"
case $how in prebuilt|prebuilt32|prebuilt64) mkdir -p "\$W/bins" && tar -xzf "\$W/bins.tar.gz" -C "\$W/bins" || fail "the binaries did not unpack"; PRE="--prebuilt \$W/bins/bin" ;; esac
if [ $how = prebuilt32 ]; then              # the 4-byte references this host cannot make
    cp "\$W"/bins/bin/build32/* build/ && touch build/s0-cell-32 build/s0-cell-s32.img build/k32-self.txt build/k32-b.txt || fail "the 4-byte references did not install"
    export EVOLVE_CELL=4 EVOLVE_PREBUILT_REF="\$W/bins/bin/s6"
fi
python3 lab/evolve/xcheck.py "\$W/designs.json" "\$W/out.json" --rounds $rounds --until \$UNTIL \$PRE > "\$W/xcheck.log" 2>&1 || fail "xcheck.py failed (xcheck.log)"
echo 0 > "\$W/DONE"
RUN
        files="$R/repo.bundle $H/designs.json $H/run.sh"; case $how in prebuilt|prebuilt32|prebuilt64) files="$files $H/bins.tar.gz" ;; esac
        ndes=$(python3 -c 'import json, sys; d = json.load(open(sys.argv[1])); print(len(d.get("designs", d)) if isinstance(d, dict) else len(d))' "$H/designs.json" 2>/dev/null || echo '?')
        cat >> "$L" << LAUNCH
t0=\$(date +%s%N)
if $SSH $O "$host" "mkdir -p $RD" < /dev/null > "$H/ssh.log" 2>&1 && t1=\$(date +%s%N) \\
    && $SCP -q $O $files "$host:$RD/" >> "$H/ssh.log" 2>&1 && t2=\$(date +%s%N) \\
    && $SSH $O "$host" "cd $RD && setsid nohup sh run.sh > run.log 2>&1 < /dev/null &" < /dev/null >> "$H/ssh.log" 2>&1 && t3=\$(date +%s%N); then
    b=\$(cat $files | wc -c)                                    # Iteration 381: the copy, timed
    tx=\$(awk -v b=\$b -v m=\$(( (t1 - t0) / 1000000 )) -v c=\$(( (t2 - t1) / 1000000 )) -v st=\$(( (t3 - t2) / 1000000 )) 'BEGIN { cs = c / 1000; printf "%.1f MB in %dm %02ds (%.0f KB/s); mkdir %d ms, start %d ms", b / 1048576, cs / 60, cs % 60, (cs > 0 ? b / 1024 / cs : 0), m, st }')
    echo "\$tx" > "$H/transfer.txt"
    echo \$(( \$(date +%s) + $offset )) > "$H/until"; echo "$host $RD" > "$H/where"
    note "$CHK" "started - $ndes designs, $how, $minutes minutes from its start - copied \$tx"
else note "$CHK" "FAILED - copying or starting there (remote/$CHK/ssh.log)"; fi
LAUNCH
    done
    if [ -s "$L" ] && grep -q '^if ' "$L"; then                   # 379: the run does not wait for the network
        : > "$R/launched"
        nohup sh "$L" >> "$CHAIN/chain.log" 2>&1 < /dev/null &
        echo "next-run: remote checks sampled - copied and started in the background (remote/launch.sh); the run starts now"
    fi ;;
stop)
    for H in "$R"/*/; do
        [ -f "$H/until" ] || continue; CHK=$(basename "$H"); read -r host RD < "$H/where"
        $SSH $O "$host" "[ -f $RD/pid ] && kill -TERM -\$(cat $RD/pid) 2>/dev/null; true" < /dev/null > /dev/null 2>&1 \
            && note "$CHK" "stopped" || note "$CHK" "could not be reached to stop"
    done ;;
gather)
    for H in "$R"/*/; do
        [ -f "$H/until" ] || continue; CHK=$(basename "$H"); until=$(cat "$H/until"); read -r host RD < "$H/where"
        if [ -z "$NOWAIT" ]; then
            while [ "$(date +%s)" -lt $(( until + 300 )) ] && ! $SSH $O "$host" "[ -f $RD/DONE ]" < /dev/null > /dev/null 2>&1; do sleep 30; done
        fi
        for f in out.json run.log xcheck.log build.log FAILED DONE load.log load-start.txt; do $SCP -q $O "$host:$RD/$f" "$H/" > /dev/null 2>&1 || true; done
        $SSH $O "$host" "[ -f $RD/pid ] && kill -TERM -\$(cat $RD/pid) 2>/dev/null; rm -rf $RD" < /dev/null > /dev/null 2>&1 || true
        if [ -s "$H/out.json" ] && (cd "$REPO" && python3 lab/evolve/xcheck.py --report "$H/out.json") > "$R/$CHK.md" 2> "$H/report.log"; then
            {   # Iteration 381: how the check was copied, and the host's load while it ran
                echo; [ -s "$H/transfer.txt" ] && echo "Copied there: $(cat "$H/transfer.txt"); the connection $(awk -v h="$host" '$1 == h {print $2 " ms"}' "$R/connect" 2>/dev/null) at the chain's start."
                [ -s "$H/load.log" ] && awk -v np="$(sed -n 's/^nproc //p' "$H/load-start.txt" 2>/dev/null)" -v st="$(sed -n 's/^loadavg //p' "$H/load-start.txt" 2>/dev/null | cut -d' ' -f1)" -v top="$(sed -n '4,6p' "$H/load-start.txt" 2>/dev/null | awk '{printf "%s%s %s%%", (NR > 1 ? ", " : ""), $2, $1}')" \
                    '{n++; s += $2; if ($2 > m) m = $2} END {if (n) printf "The host'"'"'s load while the check ran: the 1-minute load average %.2f on average, %.2f at most, over %d samples 30 s apart%s; at its start %s, the busiest then: %s.\n", s / n, m, n, (np ? ", on " np (np == 1 ? " CPU" : " CPUs") : ""), st, top}' "$H/load.log"
            } >> "$R/$CHK.md"
            note "$CHK" "gathered - remote/$CHK.md$( [ -f "$H/FAILED" ] && echo ", though: $(cat "$H/FAILED")")"
        else note "$CHK" "FAILED - no results$( [ -f "$H/FAILED" ] && echo ": $(cat "$H/FAILED")") (remote/$CHK/)"; fi
    done
    for host in $(cat "$R/hosts" 2>/dev/null); do $SSH $O "$host" "rmdir $RDIR 2>/dev/null; rm -f $RDIR/.lock; rmdir $RDIR 2>/dev/null; true" < /dev/null > /dev/null 2>&1 || true
    done ;;
*) echo "remote-checks.sh: no command $CMD" >&2; exit 2 ;;
esac
exit 0
