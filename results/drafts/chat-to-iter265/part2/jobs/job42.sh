#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 lab/evolve/c-baseline.py --runs 5 > /tmp/j42.log 2>&1; echo "exit $?" >> /tmp/j42.log
touch /tmp/job42.done
