#!/bin/sh
# lab/evolve/vm-run.sh SEED [REQ] - a run on the development VM (Iteration 79).
#
# The owner: odd seeds here, even seeds on the laptop, at the same time.
# The VM keeps no process between Claude's turns, so a run starts and ends
# within one turn. It carries the newest CARRY_LAST fronts - the laptop's
# runs, unpacked as $VMRUNS/archived-<the laptop's archive name>/build/
# evolve/db.jsonl (the name keeps the comparison's credit right), and the
# VM's own in lab/evolve/runs/ - and stores its front as
# lab/evolve/runs/archived-<UTC>-vm/build/evolve/: the front's records,
# remeasure.json and report.md - what the laptop's carry-over and
# comparison read (next-run.sh's archives()), tens of KB, not the 2.7 MB
# database. ROUNDS 4: timing here is ~4% noisy (the laptop's ~1%).
set -eu
ROOT=$(cd "$(dirname "$0")/../.." && pwd); cd "$ROOT"
SEED=${1:?usage: vm-run.sh SEED [REQ]}; REQ=${2:-}
POP=${POP:-32}; GENS=${GENS:-40}; ROUNDS=${ROUNDS:-4}; REMEASURE=${REMEASURE:-6}
VMRUNS=${VMRUNS:-$HOME/runs}; CLAST=${CARRY_LAST:-4}
list() {
    for f in "$VMRUNS"/archived-*/build/evolve/db*.jsonl lab/evolve/runs/archived-*/build/evolve/db*.jsonl; do
        [ -f "$f" ] || continue
        d=${f%/build/evolve/*}; printf '%s %s\n' "${d##*/}" "$f"
    done | sort | cut -d' ' -f2-
}
n=$(list | wc -l); skip=0
if [ "$CLAST" -gt 0 ] && [ "$n" -gt "$CLAST" ]; then skip=$((n - CLAST)); fi
CARRY=$(list | tail -n +$((skip + 1)) | paste -sd, -)
mkdir -p build/evolve
[ ! -f build/evolve/db.jsonl ] || mv build/evolve/db.jsonl "build/evolve/db.jsonl.before-seed$SEED"
rm -f build/evolve/remeasure.json build/evolve/report.md
set -- --pop "$POP" --gens "$GENS" --rounds "$ROUNDS" --seed "$SEED"
[ -z "$CARRY" ] || set -- "$@" --carry "$CARRY"
[ -z "$REQ" ] || set -- "$@" --require "$REQ"
echo "== $(date -u +%H:%M:%S) seed $SEED${REQ:+ $REQ} at $(git rev-parse --short=8 HEAD) on the VM, pop $POP gens $GENS rounds $ROUNDS"
echo "   carried: $CARRY"
python3 lab/evolve/evolve.py "$@"
echo "== $(date -u +%H:%M:%S) the front, measured again - $REMEASURE rounds"
python3 lab/evolve/evolve.py --remeasure "$REMEASURE"
python3 lab/evolve/evolve.py --report
A=lab/evolve/runs/archived-$(date -u +%Y%m%d-%H%M%S)-vm/build/evolve
mkdir -p "$A"
VMRUN_OUT=$A python3 - <<'EOF'
import json, os, sys
sys.argv = ['vm-run']; sys.path.insert(0, 'lab/evolve'); import evolve as E
R = {}
for l in open('build/evolve/db.jsonl'):
    if l.startswith('{'): r = json.loads(l); R[r['id']] = r
ok = [i for i in R if R[i]['status'] == 'ok']
keep = set(E.fronts(ok, R)[0]) if ok else set()
if os.path.exists('build/evolve/remeasure.json'): keep |= set(json.load(open('build/evolve/remeasure.json')))
with open(os.path.join(os.environ['VMRUN_OUT'], 'db.jsonl'), 'w') as f:
    for i in R:
        if i in keep: f.write(json.dumps(R[i]) + '\n')
print('   stored %d of %d designs (%d alive): the front and the re-measured' % (len(keep), len(R), len(ok)))
EOF
cp build/evolve/remeasure.json build/evolve/report.md "$A/"
echo "seed $SEED${REQ:+ $REQ} at $(git rev-parse --short=8 HEAD), on the VM: pop $POP gens $GENS rounds $ROUNDS" > "$A/run.txt"
echo "== $(date -u +%H:%M:%S) stored: $A"
