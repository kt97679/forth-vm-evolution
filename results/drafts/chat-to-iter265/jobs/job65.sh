#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 lab/evolve/ans-check.py --ids $(cat /tmp/ans47-ids.txt) > /tmp/j65-ans.log 2>&1
touch /tmp/job65.done
