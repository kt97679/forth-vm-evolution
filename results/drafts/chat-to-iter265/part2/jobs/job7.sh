#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j7-build.log 2>&1; echo "build exit $?" > /tmp/j7.log
runuser -u claude -- python3 lab/evolve/jitstack.py 28677d13b1 --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --works fib,loop >> /tmp/j7.log 2>&1; echo "exit $?" >> /tmp/j7.log
touch /tmp/job7.done
