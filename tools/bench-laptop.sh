#!/bin/bash
# bench-laptop.sh - build everything, check it, measure it, pack the results.
#
#   tools/bench-laptop.sh           the full run - about 15 to 30 minutes
#   QUICK=1 tools/bench-laptop.sh   a smoke test first - a few minutes, no
#                                   error bars; checks the whole pipeline
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
# to end), START_ROUNDS (40, start-up).
#
# Before running: plug the laptop in, close what you can, and if you can,
# set the CPU governor to performance - the checks below say where it
# stands. Leave the machine alone while it runs.
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
[ "$gov" = performance ] || [ "$gov" = unknown ] || \
    warn "governor is '$gov'; 'performance' gives steadier numbers:
            sudo cpupower frequency-set -g performance"
ac=$(cat /sys/class/power_supply/A*/online 2>/dev/null | head -1)
[ "$ac" = 0 ] && warn "on battery - plug in: power saving moves every number"
load=$(cut -d' ' -f1 /proc/loadavg)
awk -v l="$load" 'BEGIN { exit !(l > 1.0) }' && warn "load average is $load - close other work"
echo "   settings:  LAYOUTS=$LAYOUTS SWEEPS=$SWEEPS ROUNDS=$ROUNDS START_ROUNDS=$START_ROUNDS"
TAG=$(sed -n 's/^model name[ \t]*: //p' /proc/cpuinfo | head -1 \
      | sed 's/([A-Za-z]*)//g; s/ CPU//; s/ Processor//; s/ w\/.*//; s/ @.*//; s/^ *//; s/ *$//' \
      | tr 'A-Z ' 'a-z-' | tr -s '-' | tr -cd 'a-z0-9-' | cut -c1-24)
TAG="${TAG:-unknown}-$(uname -m)"
echo "   results will be tagged '$TAG'"

mkdir -p "$O" "$LOG"

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
{ uname -a; cc --version | head -1; git describe --always --dirty 2>/dev/null; } > "$LOG/host.txt"
ARCH=$LOG/bench-$TAG-$(date +%Y%m%d-%H%M).tar.gz
tar czf "$ARCH" results/"$TAG"-run*.md "results/spn-$TAG.md" \
    build/bench-laptop/*.log build/bench-laptop/*.txt build/results/*.txt build/sizes*.csv 2>/dev/null
echo "   results:  results/$TAG-run*.md (stage tables), results/spn-$TAG.md"
echo "   archive:  $ARCH"
printf '\ndone in %d min - send the archive back.\n' $(( ($(date +%s) - T0 + 59) / 60 ))
