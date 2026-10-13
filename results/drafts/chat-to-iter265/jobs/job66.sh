#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- bash tools/run-tests.sh > /tmp/j66-rt.log 2>&1; echo "exit $?" >> /tmp/j66-rt.log
touch /tmp/job66.done
