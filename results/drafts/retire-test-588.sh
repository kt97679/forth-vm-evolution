#!/bin/sh
# results/drafts/retire-test-588.sh SCRATCH - a retirement patch tested (Iteration 588): a clone of SCRATCH at its HEAD, built, validated (its dumps made),
# (/tmp/vh/status, polled to DONE; --validate before the hashes: it makes the dictionary dumps the 8-byte build reads -
# a tree built but not validated kills designs with FileNotFoundError, 588). Before the bundle: rm -rf /tmp/hx /tmp/vh (589: its
# clone holds the scratch commits - the queue's patches - and handoff-check stops on it). As the build user, detached:
#   setsid nohup sh results/drafts/retire-test-588.sh /tmp/x > /dev/null 2>&1 &
# build-hash-584.py at both widths against master's 584 hashes, then batch-check of the queue from the main tree
# RESUME=1 (Iteration 593): a run cut off by a turn's end (the sandbox suspends; /tmp stays) goes on - the clone, build
# and validate kept when the status has them, each width's hashes kept and the rest appended (--resume).
S=/tmp/vh/status; mkdir -p /tmp/vh; R=/home/claude/forth-vm-evolution
if [ "${RESUME:-0}" = 1 ] && grep -q '^validate=0 ' $S 2>/dev/null && [ -d /tmp/hx ]; then
  sed -i '/^validate=/q' $S; echo "resumed $(date +%H:%M)" >> $S; cd /tmp/hx
else
rm -f $S; rm -rf /tmp/hx; git clone -q "${1:?SCRATCH}" /tmp/hx && cd /tmp/hx || { echo "clone failed" >> $S; echo DONE >> $S; exit 1; }
echo "tree $(git log --oneline -1 | cut -c1-40)" >> $S
LAYOUTS=1 bash tools/build-stages.sh > /tmp/vh/build.log 2>&1; echo "build=$? $(grep -c 'copied s2-s5' /tmp/vh/build.log) copy line" >> $S
python3 lab/evolve/evolve.py --validate > /tmp/vh/validate.log 2>&1; echo "validate=$? $(grep -c ' image IDENTICAL' /tmp/vh/validate.log) of $(grep -c ' image ' /tmp/vh/validate.log)" >> $S
fi
for w in 8 4; do
  a=; [ $w = 4 ] && a=--cell4; [ "${RESUME:-0}" = 1 ] && a="$a --resume"
  python3 $R/results/drafts/build-hash-584.py /tmp/vh/freeze-$w.jsonl $a > /tmp/vh/hash-$w.log 2>&1; echo "hash$w=$?" >> $S
  python3 $R/results/drafts/build-hash-cmp-588.py $R/results/drafts/build-hash-584-$w.jsonl /tmp/vh/freeze-$w.jsonl >> $S 2>&1
done
cd $R && PENDING=results/queued-consolidation RECORD=1 sh tools/batch-check.sh > /dev/null 2>&1
echo "batch-check: $(cat /tmp/batch-check/summary | tr '\n' ' ')" >> $S
echo DONE >> $S
