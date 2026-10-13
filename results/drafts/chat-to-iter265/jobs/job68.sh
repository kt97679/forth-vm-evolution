#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 lab/evolve/ans-check.py --ids 3456ac1e5e,fe3c9c3940,3bb2087f9d,c05f76468e > /tmp/j68-ans.log 2>&1
touch /tmp/job68.done
