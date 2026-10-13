#!/bin/sh
cd /home/claude/forth-vm-evolution
{ for f in rebind fsys5 guard fsys5fast; do runuser -u claude -- git apply results/pending/$f-after-seed43.patch && echo "applied $f" || { echo "FAILED $f"; exit 1; }; done
  runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j6-build.log 2>&1; echo "build exit $?"
  runuser -u claude -- bash tools/run-tests.sh > /tmp/j6-tests.log 2>&1; echo "run-tests exit $?: $(tail -1 /tmp/j6-tests.log)"
  runuser -u claude -- python3 lab/evolve/evolve.py --validate > /tmp/j6-validate.log 2>&1; echo "validate exit $?: $(grep -c IDENTICAL /tmp/j6-validate.log) IDENTICAL"
} > /tmp/j6.log 2>&1
runuser -u claude -- python3 /tmp/alive43.py > /tmp/j6-alive.log 2>&1
touch /tmp/j6-alive.done
while [ ! -e /tmp/ans43.ids ]; do sleep 5; done
runuser -u claude -- python3 lab/evolve/ans-check.py --ids $(cat /tmp/ans43.ids) > /tmp/j6-ans.log 2>&1; echo "ans-check exit $?" >> /tmp/j6-ans.log
touch /tmp/job6.done
