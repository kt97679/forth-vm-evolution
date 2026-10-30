#!/bin/sh
# results/drafts/rage-check-e2e-571.sh ROOT - tools/rage-check.sh end to end on this machine (Iteration 571): ROOT a tree
# with the after-seed-83 batch committed (its HEAD is what the "host" clones); ssh and scp stand-ins make /tmp/rc/host
# the host. On x86-64 the host's arm-cross-check.py takes its x86 mode (clang cross-built, qemu-arm) - the plumbing is
# what this tests: the bundle, the copy, the clone, the stages built there, the check streamed back, the verdict, the
# clean-up after a pass. RAGECHECK_OPTS="--n 2" keeps it short. Iteration 571: PASS, 2 designs.
set -u; ROOT=$1; E=/tmp/rc; rm -rf $E; mkdir -p $E
cat > $E/ssh << 'S'
#!/bin/sh
while [ $# -gt 0 ]; do case $1 in -o) shift 2 ;; -q) shift ;; *) break ;; esac; done
shift; mkdir -p /tmp/rc/host; cd /tmp/rc/host && exec sh -c "$*"
S
cat > $E/scp << 'S'
#!/bin/sh
while [ $# -gt 0 ]; do case $1 in -o) shift 2 ;; -q) shift ;; *) break ;; esac; done
n=$#; i=0; src=""; for a in "$@"; do i=$((i + 1)); if [ $i -lt $n ]; then src="$src $a"; else dst=$a; fi; done
m() { case $1 in *:*) echo "/tmp/rc/host/${1#*:}" ;; *) echo "$1" ;; esac; }
for s in $src; do cp "$(m "$s")" "$(m "$dst")" || exit 1; done
S
chmod 755 $E/ssh $E/scp
SSH=$E/ssh SCP=$E/scp RAGECHECK_OPTS="--n 2" sh "$ROOT/tools/rage-check.sh" rage.lan; echo "rage-check.sh exit $?"
ls $E/host/fve-ragecheck
