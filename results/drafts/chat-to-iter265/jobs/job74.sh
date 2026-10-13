#!/bin/sh
cd /tmp/mo
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j74-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j74-rt.log)"; grep -A1 "engine generators" /tmp/j74-rt.log | tail -1; } > /tmp/j74.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j74.log 2>&1
touch /tmp/job74.done
