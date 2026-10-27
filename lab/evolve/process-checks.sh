#!/bin/sh
# lab/evolve/process-checks.sh RESULTS [COMPARE] - the checks on master once a seed's processing has applied its batch
# (Iteration 551; HANDOFF.md, "Processing a returned seed" 5), in their order and the jail last, alone: build, run-tests,
# validate, the gate (RESULTS, and COMPARE - a comparison pack's compare-fronts.md - when the chain had one), ans-check on
# every fourth of RESULTS' front by size and its extremes, the jail. Started detached, polled by its status:
#     setsid nohup sh lab/evolve/process-checks.sh RESULTS > /dev/null 2>&1 &
# then wait for "DONE" in /tmp/process-checks/status - its lines the results, the logs beside it (OUT= elsewhere).
# Nothing else of this user may run while the jail does. After a sandbox restart (background jobs die, /tmp stays):
# FROM=tests, validate, gate, ans or jail starts there. Not as root - the evolver refuses it.
RES=$1; CMP=${2:-}; OUT=${OUT:-/tmp/process-checks}; FROM=${FROM:-build}
cd "$(dirname "$0")/../.." || exit 1
mkdir -p "$OUT"; S=$OUT/status; on=0
[ "$FROM" = build ] && : > "$S"
st() { echo "$* $(date +%T)" >> "$S"; }
step() { if [ "$on" = 0 ] && [ "$1" = "$FROM" ]; then on=1; fi; [ "$on" = 1 ]; }
st "START from $FROM at $(git rev-parse --short HEAD)"
if step build; then env LAYOUTS=1 bash tools/build-stages.sh > "$OUT/build.log" 2>&1; st "build=$?"; fi
if step tests; then bash tools/run-tests.sh > "$OUT/tests.log" 2>&1; st "run-tests=$? $(tail -n 1 "$OUT/tests.log")"; fi
if step validate; then python3 lab/evolve/evolve.py --validate > "$OUT/validate.log" 2>&1; st "validate=$? $(grep -c IDENTICAL "$OUT/validate.log") of 7 IDENTICAL"; fi
if step gate; then python3 lab/evolve/gate.py "$RES" $CMP > "$OUT/gate.log" 2>&1; st "gate=$? $(grep -m 1 '^alive' "$OUT/gate.log")"; fi
if step ans; then
    IDS=$(python3 - "$RES" << 'PY'
import re, sys
rows = []
for l in open(sys.argv[1], errors='replace').read().split('## How the front came about')[0].split('\n'):
    f = [x.strip() for x in l.split('|')]
    if len(f) > 10 and re.fullmatch(r'[0-9a-f]{10}', f[1] or ''):
        n = lambda v: float(v.replace(',', '')) if re.fullmatch(r'[0-9.,]+', v or '') else 9e9
        rows.append((f[1], n(f[2]), n(f[4]), n(f[7]), n(f[8])))
by = sorted(rows, key=lambda r: r[3]); ids = [r[0] for r in by[::4]]
for e in (min(rows, key=lambda r: r[1])[0], min(rows, key=lambda r: r[2])[0], by[0][0], by[-1][0], min(rows, key=lambda r: r[4])[0]):
    if e not in ids: ids.append(e)
print(','.join(ids))
PY
)
    python3 lab/evolve/ans-check.py --ids "$IDS" > "$OUT/ans.log" 2>&1
    st "ans-check=$? $(grep -m 1 'designs differ' "$OUT/ans.log"); negative control $(grep -q 'caught' "$OUT/ans.log" && echo caught || echo NOT caught)"
fi
if step jail; then st "jail - alone"; python3 lab/evolve/test-jail.py > "$OUT/jail.log" 2>&1; st "jail=$? $(tail -n 1 "$OUT/jail.log")"; fi
st DONE
