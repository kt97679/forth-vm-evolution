#!/bin/sh
# lab/evolve/test-remote-clean.sh - remote-checks.sh's clean (Iteration 628) on two stand-in hosts: SSH a script running
# the command in a directory that stands for the host's home. Probe's clean ("before"): an earlier chain's directories
# removed on both hosts and the process working in one stopped, this chain's kept; gather's ("upto", nowait, no lines):
# this chain's removed too; a later chain's, a stranger in fve-xcheck and a file beside it left alone each time; a
# second clean by hand removes nothing; the steps' lines. Prints one line a check, "ok ..." last; exit 1 on a failure.
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd); T=$(mktemp -d); SP=
trap 'rm -rf "$T"' EXIT
F=0; ck() { if eval "$2"; then echo "  ok   $1"; else echo "  FAIL $1"; F=1; fi; }
alive() { [ -d "/proc/$1" ] && ! grep -q '^State:[[:space:]]*Z' "/proc/$1/status" 2> /dev/null; }
cat > "$T/ssh" << 'EOS'
#!/bin/sh
while [ $# -gt 0 ]; do case $1 in -o) shift 2 ;; -*) shift ;; *) break ;; esac; done
h=$1; shift; mkdir -p "$FAKE/$h"; cd "$FAKE/$h" && HOME="$FAKE/$h" exec sh -c "$*"
EOS
chmod +x "$T/ssh"; FAKE=$T/hosts; export FAKE
OLD=chain-20261101-120000; CUR=chain-20261108-034243; NEW=chain-20261201-000000
for h in rage.lan dream.lan; do
    X=$FAKE/$h/fve-xcheck; mkdir -p "$X/$OLD/prebuilt32/repo/build" "$X/$CUR/prebuilt64" "$X/$NEW/prebuiltarm" "$X/stranger"
    echo data > "$X/$OLD/prebuilt32/repo/build/big"; : > "$X/$OLD/.lock"; echo keep > "$FAKE/$h/beside.txt"
done
setsid sh -c 'echo $$ > "$1/sp"; cd "$2" && exec sleep 300' sh "$T" "$FAKE/rage.lan/fve-xcheck/$OLD/prebuilt32/repo" > /dev/null 2>&1 &
sleep 1; SP=$(cat "$T/sp")              # its own session, no terminal: as a chain's line runs (setsid nohup sh run.sh)
C=$T/runs/$CUR; mkdir -p "$C"
printf 'rage.lan     prebuiltarm 4 3 60 --cell 4\ndream.lan    prebuilt32  4 10 60 --cell 4\n' > "$T/remotes"
run() { SSH=$T/ssh REMOTES_FILE=$T/remotes sh "$REPO/lab/evolve/remote-checks.sh" "$@" > "$T/out.log" 2>&1; }
run probe "$C"
ck "probe: both hosts answer" '[ "$(sort -u "$C/remote/hosts" | tr "\n" " ")" = "dream.lan rage.lan " ]'
for h in rage.lan dream.lan; do X=$FAKE/$h/fve-xcheck
    ck "probe, $h: the earlier chain removed" '[ ! -e "$X/$OLD" ]'
    ck "probe, $h: this chain kept" '[ -d "$X/$CUR/prebuilt64" ]'
done
ck "probe: the process in the earlier chain stopped" '! alive $SP'
ck "probe: the steps say it" 'grep -q "^remote clean rage.lan: 1 chain directories removed (0 MB), 1 processes stopped; fve-xcheck keeps: $CUR $NEW stranger" "$C/steps"'
run gather "$C" nowait
for h in rage.lan dream.lan; do X=$FAKE/$h/fve-xcheck
    ck "gather, $h: this chain removed" '[ ! -e "$X/$CUR" ]'
    ck "gather, $h: a later chain, a stranger and a file beside left" '[ -d "$X/$NEW/prebuiltarm" ] && [ -d "$X/stranger" ] && [ -f "$FAKE/$h/beside.txt" ]'
done
ck "gather: the steps say it" 'grep -q "^remote clean dream.lan: 1 chain directories removed (0 MB), 0 processes stopped; fve-xcheck keeps: $NEW stranger;" "$C/steps"'
rm -rf "$FAKE/dream.lan/fve-xcheck/$NEW" "$FAKE/dream.lan/fve-xcheck/stranger"; run clean "$C"
ck "by hand: nothing left to remove, the empty fve-xcheck removed" 'grep -q "^remote clean dream.lan: 0 chain directories removed (0 MB), 0 processes stopped; fve-xcheck removed" "$C/steps" && [ ! -e "$FAKE/dream.lan/fve-xcheck" ]'
ck "not a chain's name: nothing done" 'mkdir -p "$T/runs/x" && SSH=$T/ssh REMOTES_FILE=$T/remotes sh "$REPO/lab/evolve/remote-checks.sh" clean "$T/runs/x" | grep -q "not a chain" && [ -d "$FAKE/rage.lan/fve-xcheck/$NEW" ]'
alive "$SP" && kill "$SP" 2> /dev/null
if [ "$F" = 0 ]; then echo "ok - clean: earlier chains at probe, this chain at gather, processes stopped, the rest kept (2 stand-in hosts)"; else grep "clean" "$C/steps" | sed "s/^/  steps: /"; exit 1; fi
