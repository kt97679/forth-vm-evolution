#!/bin/sh
cd /tmp/b45
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j44-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j44-rt.log)"; } > /tmp/j44.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j44.log 2>&1
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate45.py 2>&1 | grep -v pinned | tail -4; } >> /tmp/j44.log 2>&1
{ echo "== names-check"; runuser -u claude -- python3 lab/evolve/names-check.py 2>&1 | grep -E "WRONG|^PASS|^FAIL|rror"; } >> /tmp/j44.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids dde890d478,cc6d168e0a,f20de05a64,4a351e360a > /tmp/j44-ans.log 2>&1; grep -E "differ from s6|Negative|^\| [0-9a-f]{10} " /tmp/j44-ans.log; } >> /tmp/j44.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j44-ob.log 2>&1; echo "exit $?: $(tail -1 /tmp/j44-ob.log)"; } >> /tmp/j44.log 2>&1
touch /tmp/job44.done
