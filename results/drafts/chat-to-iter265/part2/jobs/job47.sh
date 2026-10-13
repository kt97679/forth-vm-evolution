#!/bin/sh
cd /tmp/b45
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j47-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j47-rt.log)"; } > /tmp/j47.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j47.log 2>&1
{ echo "== ans-check, jitos on"; runuser -u claude -- env ANS_SET=jitos=1 python3 lab/evolve/ans-check.py --ids cc6d168e0a,28677d13b1 > /tmp/j47-ans.log 2>&1; grep -E "differ from s6|Negative|^\| [0-9a-f]{10} " /tmp/j47-ans.log; } >> /tmp/j47.log 2>&1
{ echo "== gate (jitos off)"; runuser -u claude -- python3 /tmp/gate45.py 2>&1 | grep -v pinned | tail -3; } >> /tmp/j47.log 2>&1
touch /tmp/job47.done
