#!/bin/sh
cd /tmp/b45
{ echo "== names-check"; runuser -u claude -- python3 lab/evolve/names-check.py 2>&1 | grep -E "WRONG|PASS|FAIL|rror|not built"; } > /tmp/j40.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j40-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j40-rt.log)"; } >> /tmp/j40.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j40.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j40-ob.log 2>&1; echo "exit $?: $(tail -1 /tmp/j40-ob.log)"; } >> /tmp/j40.log 2>&1
{ echo "== readline-check"; runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 d3149e10c6 > /tmp/j40-rl.log 2>&1; echo "exit $?: $(tail -1 /tmp/j40-rl.log)"; } >> /tmp/j40.log 2>&1
touch /tmp/job40.done
