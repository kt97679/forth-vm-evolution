#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j13-b.log 2>&1
runuser -u claude -- python3 lab/evolve/jitstack.py 28677d13b1 --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --works kernel,bubble,sieve,corpus,ackermann,fib,loop,parse > /tmp/j13.log 2>&1; echo "exit $?" >> /tmp/j13.log
touch /tmp/job13.done
