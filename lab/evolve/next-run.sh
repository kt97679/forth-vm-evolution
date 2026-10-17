#!/bin/sh
# lab/evolve/next-run.sh [SEED | compare [ROUNDS] | experiment TOOL [ARGS] | none] - the next run on the laptop, in
# one command (Iteration 15): the newest bundle pulled into the clone, the
# previous run's outputs archived (moved, never deleted), everything rebuilt
# and checked, the run, its front measured again, and what to send back
# packed into one file.
#
#     sh lab/evolve/next-run.sh         # in the clone: what lab/evolve/NEXT-RUN says
#     sh lab/evolve/next-run.sh 4       # a run with seed 4
#     sh lab/evolve/next-run.sh seed 25 tag2 night
#                                       # a run for a night: population 96, 80
#                                       # generations, ~3 hours (Iteration 93)
#     sh lab/evolve/next-run.sh seed 28 tag2 12h
#                                       # a run of 12 hours, comparison included:
#                                       # population 256, generations until a
#                                       # deadline 50 minutes before (Iteration 99)
#     sh lab/evolve/next-run.sh compare # every run's front here, measured again
#                                       # in one session; nothing archived (Iteration 20)
#     sh lab/evolve/next-run.sh experiment cpu-noise.py --rounds 20
#                                       # any tracked tool in lab/evolve/, given every
#                                       # database here; nothing archived (Iteration 23)
#     sh lab/evolve/next-run.sh status  # where the chain is - its step, its progress
#     sh lab/evolve/next-run.sh monitor # its one log, followed until it ends (read only)
#     sh lab/evolve/next-run.sh stop    # the chain ended - and its archive made all the same
#
# Iteration 313: every step of a line ("A then B") is one chain - one session, one
# log, and at the end one archive in RUNS, forth-vm-evolution-chain-*.tar.gz, with
# every step's pack and the logs of any that failed (lab/evolve/chainctl.py). A
# measurement that fails does not stop what follows it; the tests run once a chain.
#
# It pulls first and then runs the copy in the repository, so a newer
# bundle brings its own script. After the pull it goes on in the
# background: closing the terminal does not stop it.
#
#   REPO      the clone                 default the clone this script is in;
#                                       a copy outside one: ~/git/my/forth-vm-evolution-iter14
#   BUNDLES   where bundles arrive      default ~/Downloads
#   RUNS      logs, archives, the pack  default runs/ in the clone (Iteration 84)
#   POP GENS ROUNDS REMEASURE           default 32 40 3 6 - seed 3's run; night: 96 80
#   JOBS                                workers, each on its own core: default 4 (Iteration 99)
#
# Interrupted? Run it again with the same seed: with nothing new pulled the
# run resumes from its database (RUNNING.md). A new commit, another seed or
# another size starts afresh, the old outputs archived first. Not as root:
# the evolver refuses (Iteration 10).
set -eu
# Iteration 20: `compare [ROUNDS]` measures every run's front here again in one
# session (lab/evolve/compare-fronts.py) - it archives and removes nothing.
# The arguments are read after the pull, in the copy pulled (below).
# Iteration 17: the clone this script is in, wherever it is - not a fixed
# path, which a clone elsewhere would have had pulled into and archived
self=$(cd "$(dirname "$0")" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || true)
[ -z "${REPO:-}" ] && [ -n "$self" ] && [ -f "$self/lab/evolve/next-run.sh" ] && REPO=$self
REPO=${REPO:-$HOME/git/my/forth-vm-evolution-iter14}
BUNDLES=${BUNDLES:-$HOME/Downloads}
RUNS=${RUNS:-$REPO/runs}       # Iteration 84 (the owner): in the clone, ignored by git - all in one place
POP=${POP:-32}; GENS=${GENS:-40}; ROUNDS=${ROUNDS:-3}; REMEASURE=${REMEASURE:-6}
JOBS=${JOBS:-4}; UNTIL=                 # Iteration 99: four workers, each on its own core
# Iteration 313: the chain's commands (lab/evolve/chainctl.py) - where it is, its one log
# followed, or the chain ended and still packed. Nothing pulled, nothing started.
case "${1:-}" in
    status|monitor|stop) exec python3 "$REPO/lab/evolve/chainctl.py" "$1" "$RUNS" ;;
esac

# Iteration 79: the archived databases, oldest first by their archive name
# (a UTC timestamp) - the laptop's, in $RUNS, and the odd seeds' run on the
# development VM, kept in the repository (lab/evolve/runs/, vm-run.sh).
archives() {
    for f in "$RUNS"/archived-*/build/evolve/db*.jsonl lab/evolve/runs/archived-*/build/evolve/db*.jsonl; do
        [ -f "$f" ] || continue
        d=${f%/build/evolve/*}; printf '%s %s\n' "${d##*/}" "$f"
    done | sort | cut -d' ' -f2-
}
say() { echo "next-run: $*"; }
# Iteration 85 (the owner): what is in this clone, exactly, in every pack -
# every path but the insides of .git, build/ and runs/ (generated: thousands
# of files, summed instead), with type, size and date; and git's own view.
repo_files() {
    { echo "# $(pwd) at $(date -u +%Y-%m-%dT%H:%M:%SZ): type size date path"
      find . \( -path ./.git -o -path ./build -o -path ./runs \) -prune -o -printf '%y %s %TY-%Tm-%Td %p\n' | sort -k4
      for d in .git build runs; do
          [ -d "$d" ] && echo "# $d/: $(find "$d" -type f | wc -l) files, $(du -sk "$d" | cut -f1) KB"
      done
      [ -d build ] && { echo "# build/, by entry (KB):"; du -sk build/* 2>/dev/null | sort -k2; }
      echo "# git status --porcelain --ignored:"
      git status --porcelain --ignored 2>&1
    } > "$1/repo-files.txt" 2>&1 || true
}
die() { echo "next-run: $*" >&2; exit 1; }
[ "$(id -u)" != 0 ] || die "not as root - the evolver refuses it (Iteration 10)"
cd "$REPO" 2>/dev/null || die "no clone at $REPO - set REPO=..."
running() { pgrep -f 'lab/evolve/evolve.py' >/dev/null 2>&1; }

# ---- 1. the newest bundle, fast-forward only; then this script as pulled
if [ -z "${NEXT_RUN_PULLED:-}" ]; then
    running && die "an evolution is running already (pgrep -f lab/evolve/evolve.py) - let it finish"
    # Iteration 313: one chain at a time; and before anything starts, what an earlier one left -
    # a chain that ended without finishing archived as interrupted, root's files given back, here,
    # where sudo can still ask
    python3 lab/evolve/chainctl.py alive "$RUNS" 2>/dev/null && die "a chain is running - sh lab/evolve/next-run.sh status, monitor or stop"
    rc=0; python3 lab/evolve/chainctl.py recover "$RUNS" "$REPO" || rc=$?
    if [ "$rc" = 3 ]; then
        say "giving them back to $(id -un) - sudo asks once"
        sudo chown -R "$(id -u):$(id -g)" $(find "$REPO" -xdev -uid 0) || die "root's files in $REPO not given back - nothing started"
    fi
    b=$(ls -t "$BUNDLES"/forth-vm-evolution*.bundle 2>/dev/null | sed 1q)
    [ -n "$b" ] || die "no forth-vm-evolution*.bundle in $BUNDLES"
    # Iteration 18: tools/bench-laptop.sh writes its measurements into tracked
    # files under results/ - a benchmark run, not an edit. Those are kept as a
    # stash and sent back in the pack; a change anywhere else stops it.
    changed=$(git status --porcelain --untracked-files=no | cut -c4-)
    if [ -n "$changed" ]; then
        if printf '%s\n' "$changed" | grep -qv '^results/'; then
            git status --short --untracked-files=no >&2
            die "tracked files outside results/ are changed in $REPO - commit or stash them first"
        fi
        git stash push -q -m "next-run: results/ as the benchmarks here left it, $(date -u +%Y-%m-%d)" -- results/
        say "results/ held measurements made here - kept as $(git stash list | sed 1q | cut -d: -f1), sent back in the pack:"
        printf '%s\n' "$changed" | sed 's/^/    /'
    fi
    say "pulling $b"
    git fetch -q "$b" HEAD || die "cannot read $b"
    git merge -q --ff-only FETCH_HEAD || die "$REPO has commits the bundle has not - not merging"
    [ -f lab/evolve/next-run.sh ] || die "the pulled commit has no lab/evolve/next-run.sh"
    NEXT_RUN_PULLED=1 exec sh "$REPO/lab/evolve/next-run.sh" "$@"
fi

# The arguments are read only here, in the copy just pulled: an older copy
# that checked them before pulling refused `compare`, which it did not know,
# and so never fetched the version that does (Iteration 20; prompts/07, 8).
# Iteration 22: with none, the bundle's own lab/evolve/NEXT-RUN decides - a
# default of seed 4 started a second 38-minute seed 4 after a pull that only
# wanted a comparison. The same command after every pull; the bundle says.
if [ $# -eq 0 ]; then
    [ -f lab/evolve/NEXT-RUN ] || die "no argument and no lab/evolve/NEXT-RUN - say a seed, compare or none"
    set -- $(sed -n '/^[^#]/{p;q}' lab/evolve/NEXT-RUN)
    say "lab/evolve/NEXT-RUN says: ${*:-none}"
fi
# Iteration 35: "A then B" - B starts when A has finished and packed, as if
# given to this script by hand: one sitting for everything that needs the
# laptop's clock (the owner asked for as few as possible). Split here; the
# detached run carries B in NEXT_RUN_THEN, and starts it at the end.
THEN=${NEXT_RUN_THEN:-}
case " $* " in
    *" then "*) ALL="$*"; THEN=${ALL#* then }; set -- ${ALL%% then *} ;;
esac
then_next() {   # the second half of "A then B": the lock released, the mode decided anew
    [ -n "$THEN" ] || return 0
    echo; say "then: $THEN"
    exec 9>&-
    unset NEXT_RUN_DETACHED NEXT_RUN_THEN NEXT_RUN_NOCARRY NEXT_RUN_FROMZERO NEXT_RUN_WIDTHS
    NEXT_RUN_PULLED=1 exec sh "$REPO/lab/evolve/next-run.sh" $THEN
}
# Iteration 114 (the owner): "nocarry" - a run from scratch, no archived front
# carried in: only the hand-made and random designs. The anchoring test - does
# a fresh search find what the carried runs, each starting from the last
# fronts, missed? It travels to the detached run in the environment, as THEN.
NOCARRY=${NEXT_RUN_NOCARRY:-}
WIDTHS=${NEXT_RUN_WIDTHS:-}
case " $* " in *" nocarry "*) NOCARRY=1; set -- $(printf '%s\n' "$@" | grep -vx nocarry) ;; esac
# Iteration 338: "widths" - select at both widths (evolve.py --widths 8,4: each design also measured
# as a 32-bit x86 engine at 4-byte cells here, its JIT off - speed32 a fourth objective)
case " $* " in *" widths "*) WIDTHS=1; set -- $(printf '%s\n' "$@" | grep -vx widths) ;; esac
# Iteration 115 (the owner): "fromzero" - nocarry and more: the first
# generation all random genomes, no hand-made design or founder in it.
FROMZERO=${NEXT_RUN_FROMZERO:-}
case " $* " in *" fromzero "*) FROMZERO=1; NOCARRY=1; set -- $(printf '%s\n' "$@" | grep -vx fromzero) ;; esac
case "${1:-none}" in
    none) say "nothing to run for this commit - pulled, and stopping"; exit 0 ;;
    compare) KIND=experiment; TOOL=compare-fronts.py; SEED=0; CROUNDS=${2:-${CROUNDS:-10}}; TARGS="--rounds $CROUNDS" ;;
    experiment) KIND=experiment; TOOL=${2:-}; SEED=0; CROUNDS=10
        TARGS=$(printf '%s\n' "$@" | sed -n '3,$p' | tr '\n' ' ') ;;
    seed) KIND=seed; SEED=${2:-}; REQ=${3:-}; SIZE=${4:-}; CROUNDS=10 ;;
    *) KIND=seed; SEED=$1; REQ=${2:-}; SIZE=${3:-}; CROUNDS=10 ;;
esac
# Iteration 93 (the owner): "night" after the seed (and tag2) - a longer run.
# The population first: under three objectives the front outgrew it (seeds
# 21-23: 38-46 designs on the front, 32 in the population, so part of the
# front was cut from breeding every generation); then the generations (a
# third of each front was still found in the last 10 of 40). 96 x 80 at seed
# 23's pace, 1.4 s a design: ~3 hours, then the re-measure as always.
case ${REQ:-} in night|*[0-9]h) SIZE=$REQ; REQ= ;; esac
# Iteration 99 (the owner): "12h" - a run of so many hours, its comparison
# included: generations until a deadline 80 minutes before the end, for the
# re-measure, the report and the comparison (~1 hour with the long workloads). The population 256: the night
# run's front came from the second half of its generations, and four cores
# (JOBS) evaluate ~4 times as many designs - ~90,000 in 12 hours.
# Iteration 152 (the owner: a 6-hour run took ~7): what follows the evolution -
# the front re-measured, and the comparison if one follows - is reserved from
# what it took last time ($RUNS/phase-times, written by each chain), scaled to
# this one's rounds and CPUs, plus a tenth and 10 minutes for the builds,
# checks and packing; the evolution keeps at least 40% of the hours. A fixed
# 80 minutes had held until the longer workloads (Iteration 127); seed 38's
# re-measure and comparison took 126.
PT=$RUNS/phase-times
phase_record() {   # phase_record KEY SECONDS ROUNDS [CPUS]
    mkdir -p "$RUNS"; { grep -v "^$1 " "$PT" 2>/dev/null; echo "$*"; } > "$PT.new" && mv "$PT.new" "$PT"
}
reserve() {        # seconds to keep for what follows the evolution
    rs=1120; rr=6; cs=6400; cr=6; cc=2                      # seed 38's, until a chain records its own
    l=$(grep '^remeasure ' "$PT" 2>/dev/null | tail -1); [ -z "$l" ] || { set -- $l; rs=$2; rr=$3; }
    l=$(grep '^compare ' "$PT" 2>/dev/null | tail -1);   [ -z "$l" ] || { set -- $l; cs=$2; cr=$3; cc=$4; }
    r=$(( rs * ${REMEASURE:-6} / rr ))
    case " $THEN " in *compare-fronts.py*)
        tr_=$(printf '%s\n' "$THEN" | sed -n 's/.*--rounds \([0-9][0-9]*\).*/\1/p'); tr_=${tr_:-10}
        tc_=$(printf '%s\n' "$THEN" | sed -n 's/.*--cpus \([0-9,]*\).*/\1/p' | tr ',' '\n' | grep -c .); [ "$tc_" -gt 0 ] || tc_=1
        c_=$(( cs * tr_ * tc_ / (cr * cc) ))
        # Iteration 355: --widths 8,4 - each design measured at 32 bits too: half again (Iteration 352)
        case " $THEN " in *" --widths "*) c_=$(( c_ * 3 / 2 )) ;; esac
        r=$(( r + c_ )) ;;
    esac
    r=$(( r * 11 / 10 + 600 ))
    [ "$r" -le $(( HOURS * 3600 * 6 / 10 )) ] || r=$(( HOURS * 3600 * 6 / 10 ))
    echo "$r"
}
HOURS=
case ${SIZE:-} in
    '') ;;
    night) POP=96; GENS=80 ;;
    *[0-9]h) HOURS=${SIZE%h}
         case $HOURS in *[!0-9]*) die "a number of hours, as 12h - not '$SIZE'" ;; esac
         POP=256; GENS=100000; RESERVE=$(reserve); UNTIL=$(( $(date +%s) + HOURS * 3600 - RESERVE )) ;;
    *) die "after the seed and tag2: nothing, night, or hours (12h) - not '$SIZE'" ;;
esac
# Iteration 71: "seed N tag2" - every design of the run in the two-bit tag
case ${REQ:-} in ''|tag2) ;; *) die "after the seed: nothing, or tag2 - not '$REQ'";; esac
case $SEED in ''|*[!0-9]*) die "the seed must be a number, or 'compare' - not '$SEED'";; esac
case $CROUNDS in ''|*[!0-9]*) die "the rounds must be a number, not '$CROUNDS'";; esac
if [ "$KIND" = experiment ]; then      # a tool of this repository, nothing else
    case $TOOL in ''|.*|*/*|*[!A-Za-z0-9._-]*) die "an experiment is a tool in lab/evolve/, not '$TOOL'";; esac
    git ls-files --error-unmatch -- "lab/evolve/$TOOL" >/dev/null 2>&1 || die "lab/evolve/$TOOL is not a tracked file"
fi
HEAD=$(git rev-parse --short HEAD)
RUN=$RUNS/seed$SEED-$HEAD
STATE=build/evolve/next-run.state
WANT="seed $SEED${REQ:+ $REQ}${FROMZERO:+ fromzero}${NOCARRY:+ nocarry} at $HEAD, pop $POP gens $GENS rounds $ROUNDS"
if [ "$KIND" = experiment ]; then
    NAME=${TOOL%.py}
    RUN=$RUNS/$NAME-$HEAD
    WANT="lab/evolve/$TOOL ${TARGS% } over every run's database here, at $HEAD"
fi

# ---- 2. fresh or resumed - decided here, where it can be seen - then detach
if [ -z "${NEXT_RUN_DETACHED:-}" ]; then
    if [ "$KIND" = experiment ]; then MODE=experiment
    elif [ -f "$STATE" ] && [ "$(cat "$STATE")" = "$WANT" ]; then MODE=resume; else MODE=fresh; fi
    mkdir -p "$RUN"
    say "at $(git log -1 --format='%h %s')"
    say "$WANT - $MODE"
    [ "$MODE" = fresh ] && say "the previous run's outputs will be moved to $RUNS/archived-..."
    [ "$MODE" = experiment ] && say "nothing will be archived or removed"
    [ -z "$THEN" ] || say "then, when this has finished and packed: $THEN"
    [ -z "${RESERVE:-}" ] || say "the evolution stops at $(date -u -d @"$UNTIL" +%H:%M) UTC ($(date -d @"$UNTIL" +%H:%M) here) - $(( RESERVE / 60 )) min kept for the re-measure${THEN:+ and the comparison} ($([ -s "$PT" ] && echo "as the last chain took" || echo "seed 38's times"))"
    # Iteration 282: counters.py needs perf's user-space counters, and the chain is
    # about to go to the background, where sudo cannot ask: ask now, once, and leave
    # perf-hold.py to hold the setting while counters.py measures (perf-hold-start.sh).
    # A later step of the chain comes back here detached, with PERF_HOLD_START set.
    # Iteration 314: the chain's directory made before anything is left behind it - perf-hold
    # watches it for the chain's end; the first detach is the one before the session file exists
    if [ -z "${NEXT_RUN_CHAIN:-}" ]; then
        NEXT_RUN_CHAIN=$RUNS/chain-$(date -u +%Y%m%d-%H%M%S)
        mkdir -p "$NEXT_RUN_CHAIN/packs"
        echo "$*${THEN:+ then $THEN}" > "$NEXT_RUN_CHAIN/line"; echo "$HEAD" > "$NEXT_RUN_CHAIN/head"
        echo running > "$NEXT_RUN_CHAIN/status"; : > "$NEXT_RUN_CHAIN/steps"
        export NEXT_RUN_CHAIN
        # Iteration 315: the remote checks' hosts tried here, where it is seen (lab/evolve/REMOTES)
        case " $* $THEN " in *" seed "*) sh lab/evolve/remote-checks.sh probe "$NEXT_RUN_CHAIN" || true ;; esac
    fi
    case " ${TOOL:-} $THEN " in *" counters.py "*|*" missmap.py "*)   # Iteration 294: missmap.py too
        if [ -z "${PERF_HOLD_START:-}" ]; then
            PERF=$(python3 lab/evolve/counters.py --find-perf) || die "counters.py: no perf runs here - nothing started"
            export PERF                 # Iteration 284: the perf that runs, found once, here, for the whole chain
            PERF_HOLD_START=$RUNS/perf-hold-$(date +%Y%m%d-%H%M%S).start; PERF_HOLD_DONE=${PERF_HOLD_START%.start}.done
            sh lab/evolve/perf-hold-start.sh "$PERF_HOLD_START" "$PERF_HOLD_DONE" "$RUNS/perf-hold.log" "$NEXT_RUN_CHAIN" || die "counters.py cannot have perf's counters - nothing started"
            export PERF_HOLD_START PERF_HOLD_DONE
        fi;;
    esac
    # Iteration 313: a chain - every step of the line - is one session, one directory, one log
    # (lab/evolve/chainctl.py): made here by the first step, carried by the rest.
    if [ ! -s "$NEXT_RUN_CHAIN/sid" ]; then
        NEXT_RUN_DETACHED=$MODE NEXT_RUN_THEN=$THEN NEXT_RUN_NOCARRY=$NOCARRY NEXT_RUN_FROMZERO=$FROMZERO NEXT_RUN_WIDTHS=$WIDTHS setsid nohup sh "$0" "$@" >> "$NEXT_RUN_CHAIN/chain.log" 2>&1 < /dev/null &
        say "going on in the background, as one chain - watch it with"
        echo "    sh lab/evolve/next-run.sh monitor     (status: where it is; stop: ends it, and still packs)"
        exit 0
    fi
    NEXT_RUN_DETACHED=$MODE NEXT_RUN_THEN=$THEN NEXT_RUN_NOCARRY=$NOCARRY NEXT_RUN_FROMZERO=$FROMZERO NEXT_RUN_WIDTHS=$WIDTHS nohup sh "$0" "$@" >> "$NEXT_RUN_CHAIN/chain.log" 2>&1 < /dev/null &
    exit 0
fi
MODE=$NEXT_RUN_DETACHED
CHAIN=${NEXT_RUN_CHAIN:-}; CHAINLOG=${CHAIN:+$CHAIN/chain.log}
[ -z "$CHAIN" ] || [ -s "$CHAIN/sid" ] || ps -o sid= -p $$ | tr -d ' ' > "$CHAIN/sid"
mkdir -p "$RUNS"
exec 9> "$RUNS/.lock"
flock -n 9 || die "another run holds $RUNS/.lock - two runs would measure each other"
# ---- one-off (Iteration 84): the runs directory moved into the clone ----
# Until then it was ~/forth-vm-evolution-runs. Once, under this lock: what
# the next runs need comes over - the newest archives (the carry and the
# comparison read them: four, or as many as CARRY_LAST / COMPARE_LAST, all
# if either is 0) and the newest eight pack tarballs. Old run directories
# stay behind: their logs are in their tarballs. A marker says it is done.
OLD=$HOME/forth-vm-evolution-runs
if [ -d "$OLD" ] && [ "$(cd "$OLD" && pwd)" != "$(cd "$RUNS" && pwd)" ] && [ ! -e "$RUNS/.moved-in" ]; then
    k=4
    for v in "${CARRY_LAST:-4}" "${COMPARE_LAST:-4}"; do
        [ "$v" = 0 ] && k=1000000
        [ "$v" -gt "$k" ] 2>/dev/null && k=$v
    done
    ls -d "$OLD"/archived-* 2>/dev/null | sort | tail -n "$k" > "$RUNS/.moved-in.list" || true
    ls "$OLD"/forth-vm-evolution-*.tar.gz 2>/dev/null \
        | sed -n 's/^\(.*-\([0-9]\{8\}-[0-9]\{6\}\)\.tar\.gz\)$/\2 \1/p' | sort | tail -n 8 | cut -d' ' -f2- >> "$RUNS/.moved-in.list" || true
    while read -r x; do mv -- "$x" "$RUNS"/; done < "$RUNS/.moved-in.list"
    say "moved into $RUNS from $OLD: $(grep -c /archived- "$RUNS/.moved-in.list" || true) archives, $(grep -c '\.tar\.gz$' "$RUNS/.moved-in.list" || true) pack tarballs - the rest of $OLD is not needed: delete it when you like"
    mv "$RUNS/.moved-in.list" "$RUNS/.moved-in"
fi
# Iteration 83 (the owner): outdated files out, before every run - archives
# past the newest four, run directories already in their pack tarballs, pack
# tarballs past the newest eight (tools/clean-runs.sh says what and why).
# Under this lock; a failure never stops the run.
RUNS="$RUNS" sh tools/clean-runs.sh --held 2>&1 | while read -r l; do say "$l"; done || true
running && die "an evolution is running already - let it finish"
step() { echo; echo "== $(date -u +%H:%M:%S) $*"; }
# Iteration 313: a step that fails is recorded, its logs kept in the chain. A measurement's
# failure does not cost what follows it; a seed run's does - the comparison after it would
# measure a run that did not finish. Stopped (chainctl.py stop): nothing follows. Either way
# the chain is packed - the one archive, whatever happened.
failed() {
    trap - EXIT
    echo; echo "next-run: FAILED in the step above"
    [ -n "$CHAIN" ] || exit 1
    F=$CHAIN/packs/failed-${NAME:-seed$SEED}-$(date -u +%H%M%S); mkdir -p "$F"
    for f in "$RUN"/*.log "$RUN"/*.md evolve.log; do [ ! -f "$f" ] || cp "$f" "$F/" 2>/dev/null || true; done
    if [ "$(sed 1q "$CHAIN/status" 2>/dev/null)" = stopping ]; then
        echo "STOPPED $WANT" >> "$CHAIN/steps"
        [ -z "$THEN" ] || echo "skipped: $THEN - the chain was stopped" >> "$CHAIN/steps"
        python3 lab/evolve/chainctl.py pack "$CHAIN" stopped; exit 1
    fi
    echo "FAILED $WANT" >> "$CHAIN/steps"
    if [ "$KIND" = experiment ] && [ -n "$THEN" ]; then
        say "a failed lab/evolve/$TOOL does not stop what follows it"
        then_next
    fi
    [ -z "$THEN" ] || echo "skipped: $THEN - after a failed seed run" >> "$CHAIN/steps"
    python3 lab/evolve/chainctl.py pack "$CHAIN" failed
    exit 1
}
trap failed EXIT
trap 'exit 143' TERM INT HUP                # dash runs no EXIT trap on a signal without these
step "$WANT - $MODE"

checks() {   # build/ made current, then everything that must pass before a measurement
    LAYOUTS=1 bash tools/build-stages.sh > "$RUN/build.log" 2>&1 || { tail -20 "$RUN/build.log"; exit 1; }
    tail -1 "$RUN/build.log"
    # Iteration 313: the tests, the validation and the jail once a chain - its code does not
    # change after the pull; a later step keeps the first one's logs, and only builds.
    if [ -n "${NEXT_RUN_CHECKED:-}" ] && [ "${NEXT_RUN_CHECKED%%:*}" = "$HEAD" ]; then
        for f in tests validate jail; do cp "${NEXT_RUN_CHECKED#*:}/$f.log" "$RUN/" 2>/dev/null || true; done
        step "tests, the hand-made stages, the jail - passed in this chain's first step at $HEAD, not run again"
        return 0
    fi
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
    NEXT_RUN_CHECKED=$HEAD:$RUN; export NEXT_RUN_CHECKED
}

if [ "$MODE" = experiment ]; then
    step "build/ made current - build-stages.sh leaves build/evolve/ alone"
    checks
    # Iteration 62: the newest COMPARE_LAST archived databases (default 4; 0:
    # all). Every run carries the earlier fronts, and since then the front of
    # all runs has come from the newest one or two: re-timing seeds 1-10 cost
    # minutes a session and grew with every run.
    LAST=${COMPARE_LAST:-4}
    step "the databases: this clone's run, and the newest $LAST archived (0: all)"
    n=$(archives | wc -l)
    skip=0; if [ "$LAST" -gt 0 ] && [ "$n" -gt "$LAST" ]; then skip=$((n - LAST)); fi
    set --
    if [ -f build/evolve/db.jsonl ]; then set -- build/evolve/db.jsonl; fi
    i=0
    for f in $(archives); do                                    # oldest first; no spaces in these paths
        i=$((i + 1)); [ "$i" -gt "$skip" ] || continue
        set -- "$@" "$f"
    done
    [ $# -gt 0 ] || { echo "   no database in build/evolve, $RUNS/archived-* or lab/evolve/runs/"; exit 1; }
    for f in "$@"; do echo "   $f"; done
    step "lab/evolve/$TOOL $TARGS"
    T0=$(date +%s)
    python3 "lab/evolve/$TOOL" $TARGS "$@" > "$RUN/$NAME.md" 2> "$RUN/$NAME.log" || { tail -20 "$RUN/$NAME.log"; exit 1; }
    if [ "$TOOL" = compare-fronts.py ]; then                      # Iteration 152: the next chain's reserve
        cr_=$(printf '%s\n' "$TARGS" | sed -n 's/.*--rounds \([0-9][0-9]*\).*/\1/p'); cr_=${cr_:-10}
        cc_=$(printf '%s\n' "$TARGS" | sed -n 's/.*--cpus \([0-9,]*\).*/\1/p' | tr ',' '\n' | grep -c .); [ "$cc_" -gt 0 ] || cc_=1
        t_=$(( $(date +%s) - T0 ))
        case " $TARGS " in *" --widths "*) t_=$(( t_ * 2 / 3 )) ;; esac   # Iteration 355: kept as one width's
        phase_record compare "$t_" "$cr_" "$cc_"
    fi
    grep -m2 -E 'Calibration|front of all runs' "$RUN/$NAME.md" || true
    step "packed to send back"
    K=$RUN/pack; rm -rf "$K"; mkdir -p "$K"
    for f in "$NAME.md" "$NAME.log" build.log tests.log validate.log jail.log; do cp "$RUN/$f" "$K/"; done
    lscpu > "$K/lscpu.txt" 2>&1 || true
    { git log -1 --format='%H %s'; uname -a; cc --version 2>&1 | sed 1q; python3 --version 2>&1; echo "$WANT"; } > "$K/machine.txt"
    cp "${CHAINLOG:-$RUN/next-run.log}" "$K/next-run.log"   # Iteration 313: the chain's log so far
    repo_files "$K"                            # Iteration 85: the clone, listed
    P=${CHAIN:-$RUNS}${CHAIN:+/packs}/forth-vm-evolution-$NAME-$HEAD-$(uname -n)-$(date -u +%Y%m%d-%H%M%S).tar.gz
    tar -czf "$P" -C "$RUN" pack
    rm -rf "$K"
    trap - EXIT
    echo; say "this step DONE - $(basename "$P"), in the chain's archive"
    [ -z "$CHAIN" ] || echo "ok $WANT - $(basename "$P")" >> "$CHAIN/steps"
    if [ -z "$THEN" ] && [ -n "$CHAIN" ]; then st=done; ! grep -q "^FAILED" "$CHAIN/steps" || st=done-some-failed; python3 lab/evolve/chainctl.py pack "$CHAIN" $st; exit 0; fi
    then_next
    exit 0
fi

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
    checks
    mkdir -p build/evolve; echo "$WANT" > "$STATE"
fi

# Iteration 46 (the owner): every archived run's front carried into this
# one, so progress compounds - evolve.py --carry; sorted, so a resumed run
# starts from the same first generation.
# Iteration 63: the newest CARRY_LAST archived databases (default 4; 0: all),
# as the comparison - the older fronts are dominated, and carrying them
# cost minutes of every run's first generation (188 designs in seed 15).
CLAST=${CARRY_LAST:-4}
n=$(archives | wc -l)
skip=0; if [ "$CLAST" -gt 0 ] && [ "$n" -gt "$CLAST" ]; then skip=$((n - CLAST)); fi
CARRY=""; i=0
for f in $(archives); do                                        # oldest first, the VM's runs among them
    i=$((i + 1)); [ "$i" -gt "$skip" ] || continue
    CARRY="${CARRY:+$CARRY,}$f"
done
if [ -n "$NOCARRY" ]; then
    CARRY=""; say "carried in: nothing - nocarry, a run from scratch"
fi
if [ -n "$CARRY" ]; then
    set -- --carry "$CARRY"
    say "carried in: the fronts of $(echo "$CARRY" | tr ',' '\n' | wc -l) archived databases"
else
    set --
fi
if [ -n "${REQ:-}" ]; then set -- "$@" --require "$REQ"; say "every design of the run in the two-bit tag"; fi
if [ -n "$CHAIN" ] && [ -s "$CHAIN/remote/hosts" ] && ! ls "$CHAIN"/remote/*/until > /dev/null 2>&1; then
    step "the remote checks started - the previous front, measured there alongside (lab/evolve/REMOTES)"
    sh lab/evolve/remote-checks.sh start "$CHAIN" || true          # Iteration 315: never costs the run
fi
step "the run - $POP designs x $GENS generations, $ROUNDS rounds; evolve.log"
python3 lab/evolve/chainctl.py ticker $$ "${UNTIL:-0}" &     # Iteration 313: a progress line every 5 minutes
TICK=$!
python3 lab/evolve/evolve.py --pop "$POP" --gens "$GENS" --rounds "$ROUNDS" --seed "$SEED" --jobs "$JOBS" ${UNTIL:+--until "$UNTIL"} ${FROMZERO:+--fromzero} ${WIDTHS:+--widths 8,4} "$@" >> evolve.log 2>&1 \
    || { kill $TICK 2>/dev/null || true; tail -20 evolve.log; exit 1; }
kill $TICK 2>/dev/null || true
tail -3 evolve.log
step "the front, measured again - $REMEASURE rounds"
T0=$(date +%s)
python3 lab/evolve/evolve.py --remeasure "$REMEASURE" >> evolve.log 2>&1 || { tail -20 evolve.log; exit 1; }
python3 lab/evolve/evolve.py --report >> evolve.log 2>&1 || { tail -20 evolve.log; exit 1; }
phase_record remeasure $(( $(date +%s) - T0 )) "$REMEASURE"      # Iteration 152: the next chain's reserve

step "packed to send back"
K=$RUN/pack; rm -rf "$K"; mkdir -p "$K"
cp build/evolve/report.md build/evolve/db.jsonl evolve.log "$K/"
[ ! -f build/evolve/remeasure.json ] || cp build/evolve/remeasure.json "$K/"
for f in build tests validate jail; do [ ! -f "$RUN/$f.log" ] || cp "$RUN/$f.log" "$K/"; done
lscpu > "$K/lscpu.txt" 2>&1 || true
{ git log -1 --format='%H %s'; uname -a; cc --version 2>&1 | sed 1q; python3 --version 2>&1; echo "$WANT, $MODE"; } > "$K/machine.txt"
# results/ as the benchmarks here left it (step 1), every such stash
s=$(git stash list | grep 'next-run: results/' | cut -d: -f1 || true)
if [ -n "$s" ]; then
    for x in $s; do echo "# $x: $(git log -1 --format=%s "$x")"; git stash show -p "$x"; done > "$K/results-measured-here.patch"
fi
cp "${CHAINLOG:-$RUN/next-run.log}" "$K/next-run.log"   # Iteration 313: the chain's log so far
repo_files "$K"                                # Iteration 85: the clone, listed
P=${CHAIN:-$RUNS}${CHAIN:+/packs}/forth-vm-evolution-seed$SEED-$HEAD-$(uname -n)-$(date -u +%Y%m%d-%H%M%S).tar.gz
tar -czf "$P" -C "$RUN" pack
rm -rf "$K"
trap - EXIT
echo; say "this step DONE - $(basename "$P"), in the chain's archive"
[ -z "$CHAIN" ] || echo "ok $WANT - $(basename "$P")" >> "$CHAIN/steps"
if [ -z "$THEN" ] && [ -n "$CHAIN" ]; then st=done; ! grep -q "^FAILED" "$CHAIN/steps" || st=done-some-failed; python3 lab/evolve/chainctl.py pack "$CHAIN" $st; exit 0; fi
then_next
