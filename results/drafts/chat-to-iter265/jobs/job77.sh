#!/bin/sh
cd /tmp/mo
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j77-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j77-rt.log)"; grep -A1 "engine generators" /tmp/j77-rt.log | tail -1; } > /tmp/j77.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j77.log 2>&1
{ echo "== ans"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids cl3456ac1e,cl3bb2087f > /tmp/j77-ans.log 2>&1; grep -E "differ from s6|^\| cl" /tmp/j77-ans.log; } >> /tmp/j77.log 2>&1
touch /tmp/job77.done
