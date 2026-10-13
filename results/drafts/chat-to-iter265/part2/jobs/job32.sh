#!/bin/sh
cd /tmp/b45
{ echo "== names-check"; runuser -u claude -- python3 lab/evolve/names-check.py 2>&1 | grep -E "^- |PASS|FAIL"; } > /tmp/j32.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j32-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j32-rt.log)"; } >> /tmp/j32.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j32.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j32-ob.log 2>&1; echo "exit $?: $(tail -1 /tmp/j32-ob.log)"; } >> /tmp/j32.log 2>&1
{ echo "== readline-check"; runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 d3149e10c6 > /tmp/j32-rl.log 2>&1; echo "exit $?: $(tail -1 /tmp/j32-rl.log)"; } >> /tmp/j32.log 2>&1
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate45.py 2>&1 | grep -v pinned | tail -5; } >> /tmp/j32.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids dde890d478,add5ec8937,cc6d168e0a,f20de05a64,4a351e360a,d827d54f60 > /tmp/j32-ans.log 2>&1; grep -E "differ from s6|Negative|^\| [0-9a-f]{10} " /tmp/j32-ans.log; } >> /tmp/j32.log 2>&1
touch /tmp/job32.done
