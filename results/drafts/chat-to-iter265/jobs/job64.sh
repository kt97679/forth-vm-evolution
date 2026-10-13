#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 /tmp/gate47.py 2>&1 | grep -v pinned > /tmp/j64.log
touch /tmp/job64.done
