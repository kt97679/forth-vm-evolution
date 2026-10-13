#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 lab/evolve/jitvariants.py 28677d13b1 --out /tmp/jitvariants.json > /tmp/j11-var.log 2>&1
runuser -u claude -- python3 lab/evolve/jitstack.py 28677d13b1 --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --variants /tmp/jitvariants.json --show 1 --works loop,fib,bubble,ackermann,kernel,corpus,sieve > /tmp/j11.log 2>&1; echo "exit $?" >> /tmp/j11.log
touch /tmp/job11.done
