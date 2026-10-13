#!/bin/sh
cd /home/claude/forth-vm-evolution
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j67-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j67-rt.log)"; grep -A1 "engine generators" /tmp/j67-rt.log | tail -1; } > /tmp/j67.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j67.log 2>&1
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate47.py 2>&1 | grep -v pinned | tail -3; } >> /tmp/j67.log 2>&1
touch /tmp/job67.done
