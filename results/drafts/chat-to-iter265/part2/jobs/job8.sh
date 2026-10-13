#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 lab/evolve/jitstack.py 28677d13b1 --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --works loop,fib --show 2 > /tmp/j8.log 2>&1; echo "exit $?" >> /tmp/j8.log
touch /tmp/job8.done
