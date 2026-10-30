#!/bin/sh
# results/drafts/prebuiltarm-e2e-570.sh ROOT - rage's prebuiltarm check end to end on this machine (Iteration 570): ROOT a
# tree with the after-seed-83 batch committed (its HEAD is what the "host" clones); ssh and scp stand-ins make /tmp/e2e/host
# the host; seed 82's results file stands for the archived front. remote-checks.sh probe, start (xcheck.py --arm: the
# sample, the ARM cross-builds, the bundle), the host's run.sh (clone, stages, the partial bundle: s6 and GCC's built
# there), gather (remote/rage.lan-prebuiltarm.md). On x86 the shipped ARM engines cannot run - "Exec format error" is
# the expected line for each; s6 and the GCC designs are measured. Needs CROSS=1 setup-sandbox.sh. Iteration 570: 12
# sampled, 10 cross-built (74 KB), 2 GCC measured, gathered.
set -u; ROOT=$1; E=/tmp/e2e; rm -rf $E; mkdir -p $E/runs/archived-82/build/evolve $E/runs/chain-83
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
cp "$ROOT/results/evolve-amd-ryzen-7-pro-8840hs-seed82.md" $E/runs/archived-82/build/evolve/report.md
grep '^rage' "$ROOT/lab/evolve/REMOTES" > $E/remotes
cd "$ROOT" && export SSH=$E/ssh SCP=$E/scp REMOTES_FILE=$E/remotes; C=$E/runs/chain-83
sh lab/evolve/remote-checks.sh probe $C; s=$(date +%s)
sh lab/evolve/remote-checks.sh start $C; echo "start: $(( $(date +%s) - s )) s"
while [ ! -f $E/host/fve-xcheck/chain-83/prebuiltarm/DONE ]; do sleep 10; done
sh lab/evolve/remote-checks.sh gather $C; cat $C/steps; cat $C/remote/rage.lan-prebuiltarm.md
