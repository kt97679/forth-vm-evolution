#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 lab/evolve/regprice.py add5ec8937 --db results/evolve-amd-ryzen-7-pro-8840hs-seed43.md > /tmp/j14.log 2>&1; echo "exit $?" >> /tmp/j14.log
touch /tmp/job14.done
