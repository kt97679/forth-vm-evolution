#!/bin/sh
# lab/evolve/next-run.sh [SEED] - the next evolution run on the laptop, in
# one command (Iteration 15): the newest bundle pulled into the clone, the
# previous run's outputs archived (moved, never deleted), everything rebuilt
# and checked, the run, its front measured again, and what to send back
# packed into one file.
#
#     sh ~/Downloads/next-run.sh 4
#
# It pulls first and then runs the copy in the repository, so a newer
# bundle brings its own script. After the pull it goes on in the
# background: closing the terminal does not stop it.
#
#   REPO      the clone                 default ~/git/my/forth-vm-evolution-iter14
#   BUNDLES   where bundles arrive      default ~/Downloads
#   RUNS      logs, archives, the pack  default ~/forth-vm-evolution-runs
#   POP GENS ROUNDS REMEASURE           default 32 40 3 6 - seed 3's run
#
# Interrupted? Run it again with the same seed: with nothing new pulled the
# run resumes from its database (RUNNING.md). A new commit, another seed or
# another size starts afresh, the old outputs archived first. Not as root:
# the evolver refuses (Iteration 10).
set -eu
SEED=${1:-4}
REPO=${REPO:-$HOME/git/my/forth-vm-evolution-iter14}
BUNDLES=${BUNDLES:-$HOME/Downloads}
RUNS=${RUNS:-$HOME/forth-vm-evolution-runs}
POP=${POP:-32}; GENS=${GENS:-40}; ROUNDS=${ROUNDS:-3}; REMEASURE=${REMEASURE:-6}
say() { echo "next-run: $*"; }
die() { echo "next-run: $*" >&2; exit 1; }
case $SEED in ''|*[!0-9]*) die "the seed must be a number, not '$SEED'";; esac
[ "$(id -u)" != 0 ] || die "not as root - the evolver refuses it (Iteration 10)"
cd "$REPO" 2>/dev/null || die "no clone at $REPO - set REPO=..."
running() { pgrep -f 'lab/evolve/evolve.py' >/dev/null 2>&1; }

# ---- 1. the newest bundle, fast-forward only; then this script as pulled
if [ -z "${NEXT_RUN_PULLED:-}" ]; then
    running && die "an evolution is running already (pgrep -f lab/evolve/evolve.py) - let it finish"
    b=$(ls -t "$BUNDLES"/forth-vm-evolution*.bundle 2>/dev/null | sed 1q)
    [ -n "$b" ] || die "no forth-vm-evolution*.bundle in $BUNDLES"
    if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
        git status --short --untracked-files=no >&2
        die "tracked files are changed in $REPO - commit or stash them first"
    fi
    say "pulling $b"
    git fetch -q "$b" HEAD || die "cannot read $b"
    git merge -q --ff-only FETCH_HEAD || die "$REPO has commits the bundle has not - not merging"
    [ -f lab/evolve/next-run.sh ] || die "the pulled commit has no lab/evolve/next-run.sh"
    NEXT_RUN_PULLED=1 exec sh "$REPO/lab/evolve/next-run.sh" "$@"
fi

HEAD=$(git rev-parse --short HEAD)
RUN=$RUNS/seed$SEED-$HEAD
STATE=build/evolve/next-run.state
WANT="seed $SEED at $HEAD, pop $POP gens $GENS rounds $ROUNDS"

# ---- 2. fresh or resumed - decided here, where it can be seen - then detach
if [ -z "${NEXT_RUN_DETACHED:-}" ]; then
    if [ -f "$STATE" ] && [ "$(cat "$STATE")" = "$WANT" ]; then MODE=resume; else MODE=fresh; fi
    mkdir -p "$RUN"
    say "at $(git log -1 --format='%h %s')"
    say "$WANT - $MODE"
    [ "$MODE" = fresh ] && say "the previous run's outputs will be moved to $RUNS/archived-..."
    NEXT_RUN_DETACHED=$MODE nohup sh "$0" "$@" >> "$RUN/next-run.log" 2>&1 < /dev/null &
    say "going on in the background; follow it with"
    echo "    tail -f $RUN/next-run.log"
    exit 0
fi
MODE=$NEXT_RUN_DETACHED
exec 9> "$RUNS/.lock"
flock -n 9 || die "another run holds $RUNS/.lock - two runs would measure each other"
running && die "an evolution is running already - let it finish"
step() { echo; echo "== $(date -u +%H:%M:%S) $*"; }
trap 'echo; echo "next-run: FAILED in the step above - $RUN/next-run.log"' EXIT
step "$WANT - $MODE"

if [ "$MODE" = fresh ]; then
    # Iteration 16: by kind, not by name - the first version kept four named
    # files and removed the rest of build/, with the earlier seeds'
    # databases and the benchmark archives in it (the owner's find . showed
    # them before it ran). Moved, never deleted.
    step "the previous runs' records, kept"
    A=$RUNS/archived-$(date -u +%Y%m%d-%H%M%S)
    keep() { mkdir -p "$A/$(dirname "$1")"; mv "$1" "$A/$1"; echo "   $1"; }
    for f in * .[!.]*; do                     # at the top: every file git does not track -
        [ -f "$f" ] || continue                # logs, reports, checks saved by hand -
        [ "$f" != RESULTS.md ] || continue     # but the sweep's working copy (.gitignore)
        if git ls-files --error-unmatch -- "$f" >/dev/null 2>&1; then continue; fi
        keep "$f"
    done
    for f in build/evolve/*; do                # the evolver's records: databases, reports, re-measures
        [ -f "$f" ] || continue
        keep "$f"
    done
    for d in build/bench-laptop build/results; do    # the benchmark suite's archives and raw results
        [ -d "$d" ] || continue
        keep "$d"
    done
    if [ -d "$A" ]; then
        (cd "$A" && find . -type f | sort) > "$A/MANIFEST.txt"
        echo "   moved to $A (MANIFEST.txt lists them)"
    else echo "   (none)"; fi
    step "the rest of build/ removed, built again"
    rm -rf build
    LAYOUTS=1 bash tools/build-stages.sh > "$RUN/build.log" 2>&1 || { tail -20 "$RUN/build.log"; exit 1; }
    tail -1 "$RUN/build.log"
    step "tests"
    bash tools/run-tests.sh > "$RUN/tests.log" 2>&1 || { tail -30 "$RUN/tests.log"; exit 1; }
    tail -1 "$RUN/tests.log"
    tail -1 "$RUN/tests.log" | grep -q '^PASS' || exit 1
    step "the hand-made stages, rebuilt from their genomes"
    python3 lab/evolve/evolve.py --validate > "$RUN/validate.log" 2>&1 || { cat "$RUN/validate.log"; exit 1; }
    n=$(grep -c ' IDENTICAL' "$RUN/validate.log" || true)
    echo "   $n of 7 IDENTICAL"
    [ "$n" = 7 ] || { cat "$RUN/validate.log"; exit 1; }
    step "the jail"
    python3 lab/evolve/test-jail.py > "$RUN/jail.log" 2>&1 || { cat "$RUN/jail.log"; exit 1; }
    tail -1 "$RUN/jail.log"
    mkdir -p build/evolve; echo "$WANT" > "$STATE"
fi

step "the run - $POP designs x $GENS generations, $ROUNDS rounds; evolve.log"
python3 lab/evolve/evolve.py --pop "$POP" --gens "$GENS" --rounds "$ROUNDS" --seed "$SEED" >> evolve.log 2>&1 \
    || { tail -20 evolve.log; exit 1; }
tail -3 evolve.log
step "the front, measured again - $REMEASURE rounds"
python3 lab/evolve/evolve.py --remeasure "$REMEASURE" >> evolve.log 2>&1 || { tail -20 evolve.log; exit 1; }
python3 lab/evolve/evolve.py --report >> evolve.log 2>&1 || { tail -20 evolve.log; exit 1; }

step "packed to send back"
K=$RUN/pack; rm -rf "$K"; mkdir -p "$K"
cp build/evolve/report.md build/evolve/db.jsonl evolve.log "$K/"
[ ! -f build/evolve/remeasure.json ] || cp build/evolve/remeasure.json "$K/"
for f in build tests validate jail; do [ ! -f "$RUN/$f.log" ] || cp "$RUN/$f.log" "$K/"; done
lscpu > "$K/lscpu.txt" 2>&1 || true
{ git log -1 --format='%H %s'; uname -a; cc --version 2>&1 | sed 1q; python3 --version 2>&1; echo "$WANT, $MODE"; } > "$K/machine.txt"
cp "$RUN/next-run.log" "$K/next-run.log"
P=$RUNS/forth-vm-evolution-seed$SEED-$HEAD-$(uname -n)-$(date -u +%Y%m%d-%H%M%S).tar.gz
tar -czf "$P" -C "$RUN" pack
rm -rf "$K"
trap - EXIT
echo
say "DONE - send $P"
