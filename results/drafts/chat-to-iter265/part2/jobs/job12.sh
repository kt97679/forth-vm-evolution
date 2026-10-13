#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 lab/evolve/jitstack.py 28677d13b1 --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --works loop,fib,bubble,ackermann,kernel,sieve > /tmp/j12.log 2>&1; echo "exit $?" >> /tmp/j12.log
touch /tmp/job12.done
