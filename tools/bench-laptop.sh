#!/bin/bash
# bench-laptop.sh - build everything, check it, measure it, pack the results.
#
#   tools/bench-laptop.sh           the full run - about 15 to 30 minutes
#   QUICK=1 tools/bench-laptop.sh   a smoke test first - a few minutes, no
#                                   error bars; checks the whole pipeline
#   CHECK=1 tools/bench-laptop.sh   only the checks below - seconds: are
#                                   the counters readable, which core
#   ENGINE_RT=nolibc tools/bench-laptop.sh
#                                   engines without the C library - see
#                                   tools/engine-rt.sh
#
# What it does, in order, stopping at the first failure:
#   1. builds every stage with LAYOUTS layout variants of each engine
#      (the SPN stages too, on an x86-64 host)
#   2. runs the test suite - nothing is measured unless everything passes
#   3. tools/collect-results.sh sweep: the stage tables, net of start-up,
#      measured SWEEPS times and checked for agreement
#   4. tools/spn-bench.py: what the sweep does not measure - start-up, end
#      to end with nothing subtracted, memory, image sizes
#   5. packs results and logs into one archive, to send back
#
# Settings, from the environment: LAYOUTS (5), SWEEPS (2), ROUNDS (12, end
# to end), START_ROUNDS (40, start-up), NO_COUNTERS=1 (CPU time only).
#
# CYCLES, NOT SECONDS. CPU time already leaves out time spent waiting for
# other processes, but not the clock speed while this one runs: boost,
# heat and the governor change it, and could change short runs - the SPN
# systems' - most. So the measurements also count CPU cycles, which do
# not depend on the clock (tools/cputime.c); in user space only, which
# tools/clockfit.py accounts for. Reading the counters needs
# kernel.perf_event_paranoid at 2 or below; Ubuntu ships 4. If it is
# higher, this script lowers it to 2 at the start - sudo asks for your
# password then, not half an hour later - and puts it back when the run
# ends, however it ends: finished, failed or interrupted. It keeps sudo's
# credential fresh meanwhile, so the restore needs no one at the keyboard.
# Only a kill -9 or a power cut skip the restore, and a reboot undoes the
# change anyway: sysctl without a file in /etc/sysctl.d is not saved.
#
# The machine need not be idle: other programs can stay open. Runs are
# pinned to the core that is quietest when the run starts, not to cpu 0,
# which takes more interrupts. Plugged in is still better than battery.
# Using the machine heavily during the run still costs: a busy SMT sibling
# or a full cache slows the work itself, which no counter can remove -
# the sweeps' agreement check will say if it went too far.
set -u
cd "$(dirname "$0")/.."
ROOT=$PWD
O=$ROOT/build
if [ "${QUICK:-0}" = 1 ]; then
    LAYOUTS=${LAYOUTS:-2}; SWEEPS=${SWEEPS:-1}; ROUNDS=${ROUNDS:-3}; START_ROUNDS=${START_ROUNDS:-6}
else
    LAYOUTS=${LAYOUTS:-5}; SWEEPS=${SWEEPS:-2}; ROUNDS=${ROUNDS:-12}; START_ROUNDS=${START_ROUNDS:-40}
fi
LOG=$O/bench-laptop
T0=$(date +%s)
say()  { printf '\n== %s\n' "$*"; }
warn() { printf '   warning: %s\n' "$*"; }
die()  { printf '\n   STOPPED: %s\n' "$*"; exit 1; }

# ---- 0. prerequisites and the state of the machine --------------------
say "checking this machine"
for t in cc make python3; do
    command -v "$t" >/dev/null 2>&1 || die "'$t' is needed and not found"
done
command -v taskset >/dev/null 2>&1 || warn "no taskset: runs will not be pinned to one core"
[ "$(uname -m)" = x86_64 ] || warn "not x86-64: the SPN stages (s7, s8) will be skipped"
gov=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo unknown)
echo "   cpu:       $(sed -n 's/^model name[ \t]*: //p' /proc/cpuinfo | head -1)"
echo "   governor:  $gov"
# (the governor matters little when counting cycles; see "metric" below)
ac=$(cat /sys/class/power_supply/A*/online 2>/dev/null | head -1)
[ "$ac" = 0 ] && warn "on battery - plug in: power saving moves every number"
load=$(cut -d' ' -f1 /proc/loadavg)
echo "   load:      $load"

# ---- the counters: lowered for this run, restored however it ends -------
# PARANOID_FILE only exists to test this logic without root.
PARANOID_FILE=${PARANOID_FILE:-/proc/sys/kernel/perf_event_paranoid}
ORIG_PARANOID=$(cat "$PARANOID_FILE" 2>/dev/null || echo unknown)
CHANGED=0; KEEPALIVE=
restore_counters() {       # $1: the status the script is exiting with
    [ -n "$KEEPALIVE" ] && kill "$KEEPALIVE" 2>/dev/null
    [ "$CHANGED" = 1 ] || return 0
    # Without a password first (the keep-alive saw to that); if that fails
    # and someone is at the terminal, ask.
    sudo -n sysctl -q kernel.perf_event_paranoid="$ORIG_PARANOID" 2>/dev/null \
        || { [ -t 0 ] && sudo sysctl -q kernel.perf_event_paranoid="$ORIG_PARANOID"; }
    local now; now=$(cat "$PARANOID_FILE" 2>/dev/null)
    if [ "$now" = "$ORIG_PARANOID" ]; then
        echo "   kernel.perf_event_paranoid restored to $now"
        CHANGED=0
    else
        printf '\n   WARNING: kernel.perf_event_paranoid is still %s, not %s. Restore it:\n' \
            "$now" "$ORIG_PARANOID" >&2
        printf '       sudo sysctl kernel.perf_event_paranoid=%s\n' "$ORIG_PARANOID" >&2
        printf '   (a reboot restores it too: the change was never saved)\n' >&2
        # A run that otherwise succeeded must not look clean.
        [ "${1:-0}" = 0 ] && exit 3
    fi
}
trap 'restore_counters $?' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

if [ "${NO_COUNTERS:-0}" = 1 ]; then
    echo "   counters:  not used (NO_COUNTERS=1)"
elif [ "$ORIG_PARANOID" = unknown ]; then
    echo "   counters:  no $PARANOID_FILE"
elif [ "$ORIG_PARANOID" -gt 2 ]; then
    echo "   counters:  kernel.perf_event_paranoid is $ORIG_PARANOID; lowering it to 2 for"
    echo "              this run - restored when it ends. sudo may ask for your password."
    if sudo sysctl -q kernel.perf_event_paranoid=2 && [ "$(cat "$PARANOID_FILE")" = 2 ]; then
        CHANGED=1
        # sudo forgets a password after 15 minutes; the run takes longer.
        # Refresh it every minute, so the restore at the end needs no one.
        # Its own stdio: a background sleep that inherited the script's
        # output would hold a pipe (| tee) open for a minute after the end.
        # And it takes its sleep with it when stopped - background jobs
        # ignore Ctrl-C, so nothing else would.
        ( trap 'kill $nap 2>/dev/null; exit 0' TERM
          while kill -0 $$ 2>/dev/null; do
              sudo -n -v 2>/dev/null
              sleep 60 & nap=$!; wait $nap
          done ) </dev/null >/dev/null 2>&1 &
        KEEPALIVE=$!
    else
        warn "could not lower it"
    fi
else
    echo "   counters:  kernel.perf_event_paranoid is $ORIG_PARANOID - nothing to change"
fi
# Can this machine count cycles? Build the timer now and ask it - before a
# long build, while you are still here to fix it.
mkdir -p "$O"
cc -O2 -Wall -o "$O/cputime" tools/cputime.c || die "tools/cputime.c did not compile"
if [ "${NO_COUNTERS:-0}" != 1 ] && "$O/cputime" /bin/true 2>&1 >/dev/null | grep -q '^CYCLES'; then
    export BENCH_METRIC=cycles
    echo "   metric:    CPU cycles, from the hardware counters"
else
    export BENCH_METRIC=cpu
    echo "   metric:    CPU time"
    [ "${NO_COUNTERS:-0}" = 1 ] || \
        warn "the hardware counters cannot be read - measuring CPU time, which
            the clock speed moves. Steadier: a quiet machine and the performance
            governor (now '$gov'): sudo cpupower frequency-set -g performance"
fi

# ---- the core: the quietest one now, counting its SMT sibling ------------
export BENCH_CPU=$(python3 - << 'EOF'
import os, time
def snap():
    d = {}
    for line in open('/proc/stat'):
        f = line.split()
        if f and f[0].startswith('cpu') and f[0][3:].isdigit():
            v = [int(x) for x in f[1:]]
            d[int(f[0][3:])] = (v[3] + (v[4] if len(v) > 4 else 0), sum(v))
    return d
def siblings(c):
    try:
        txt = open('/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list' % c).read()
    except OSError:
        return {c}
    out = set()
    for part in txt.strip().split(','):
        lo, _, hi = part.partition('-')
        out |= set(range(int(lo), int(hi or lo) + 1))
    return out
a = snap(); time.sleep(2); b = snap()
busy = {c: 1 - (b[c][0] - a[c][0]) / max(1, b[c][1] - a[c][1]) for c in b if c in a}
ok = [c for c in busy if c in os.sched_getaffinity(0)] or [0]
# least busy physical core, then least busy thread on it; cpu 0 last
print(min(ok, key=lambda c: (round(sum(busy.get(x, 0) for x in siblings(c)), 2),
                             busy.get(c, 0), c == 0, -c)))
EOF
)
# If the choice failed for any reason, cpu 0 as before - never an empty
# BENCH_CPU, which would hand taskset an empty list and fail every run.
case "$BENCH_CPU" in
    ''|*[!0-9]*) BENCH_CPU=0
                 echo "   core:      cpu 0 - could not work out the quietest";;
    *)           echo "   core:      cpu $BENCH_CPU - the quietest over two seconds, with its SMT sibling";;
esac
echo "   settings:  LAYOUTS=$LAYOUTS SWEEPS=$SWEEPS ROUNDS=$ROUNDS START_ROUNDS=$START_ROUNDS"
[ "${CHECK:-0}" = 1 ] && { echo; echo "   CHECK=1: checks only - nothing built or measured"; exit 0; }
TAG=$(sed -n 's/^model name[ \t]*: //p' /proc/cpuinfo | head -1 \
      | sed 's/([A-Za-z]*)//g; s/ CPU//; s/ Processor//; s/ w\/.*//; s/ @.*//; s/^ *//; s/ *$//' \
      | tr 'A-Z ' 'a-z-' | tr -s '-' | tr -cd 'a-z0-9-' | cut -c1-24)
TAG="${TAG:-unknown}-$(uname -m)"
echo "   results will be tagged '$TAG'"

mkdir -p "$O" "$LOG"
# Everything this run writes is newer than this; only that is packed.
STAMP=$LOG/.started; touch "$STAMP"; sleep 1

# ---- 1. build ------------------------------------------------------------
say "1/5 building every stage, $LAYOUTS layout(s) each"
LAYOUTS=$LAYOUTS bash tools/build-stages.sh > "$LOG/build.log" 2>&1 \
    || die "the build failed - see $LOG/build.log"
grep -E 'built  s[78]|SPN stages skipped' "$LOG/build.log" | sed 's/^/   /'

# ---- 2. correctness ------------------------------------------------------
say "2/5 test suite (nothing is measured unless it passes)"
bash tools/run-tests.sh > "$LOG/tests.log" 2>&1
grep -q '^PASS' "$LOG/tests.log" || { tail -25 "$LOG/tests.log"; die "tests failed - see $LOG/tests.log"; }
echo "   PASS - $(grep -c 'ok     616 cases' "$LOG/tests.log") systems at 616/616"

# ---- 3. the stage tables ---------------------------------------------------
say "3/5 stage benchmarks: collect-results.sh sweep $SWEEPS"
bash tools/collect-results.sh sweep "$SWEEPS" 2>&1 | tee "$LOG/sweep.log" | grep -E '^(=====|saved|sweeping)|agree|disagree' | sed 's/^/   /'

# ---- 4. SPN: start-up, end to end, memory ---------------------------------
say "4/5 start-up, end to end, memory (tools/spn-bench.py)"
python3 tools/spn-bench.py "$O" "results/spn-$TAG.md" "$ROUNDS" "$START_ROUNDS" 2>&1 \
    | tee "$LOG/spn.log" | sed 's/^/   /'
# (a pipeline's status is its last command's, so check the result itself)
[ -s "results/spn-$TAG.md" ] || die "no results/spn-$TAG.md - see $LOG/spn.log"

# ---- 5. pack --------------------------------------------------------------
say "5/5 packing"
cp /proc/cpuinfo "$LOG/cpuinfo.txt" 2>/dev/null
{ uname -a; cc --version | head -1; git describe --always --dirty 2>/dev/null
  echo "metric $BENCH_METRIC, pinned to cpu $BENCH_CPU, governor $gov, load at start $load"
  echo "engines linked: ENGINE_RT=${ENGINE_RT:-libc}"
  echo "kernel.perf_event_paranoid $ORIG_PARANOID before the run$([ "$CHANGED" = 1 ] && echo ', 2 during it')"
} > "$LOG/host.txt"
ARCH=$LOG/bench-$TAG-$(date +%Y%m%d-%H%M).tar.gz
# Only what this run wrote. A pattern alone swept in results/*-run2.md
# from a sweep sixteen days older, and stale files in build/results.
FILES=$( { find results build/results build/bench-laptop -maxdepth 1 -type f -newer "$STAMP" \
              \( -name '*.md' -o -name '*.txt' -o -name '*.log' \)
            find build -maxdepth 1 -type f -newer "$STAMP" -name 'sizes*.csv'; } | sort)
tar czf "$ARCH" $FILES
OLD=$(find results/"$TAG"-run*.md build/results -maxdepth 1 -type f ! -newer "$STAMP" 2>/dev/null | sort)
[ -n "$OLD" ] && echo "   not packed, older than this run: $(echo $OLD)"
echo "   results:  results/$TAG-run*.md (stage tables), results/spn-$TAG.md"
echo "   archive:  $ARCH"
printf '\ndone in %d min - send the archive back.\n' $(( ($(date +%s) - T0 + 59) / 60 ))
