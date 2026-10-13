#!/bin/sh
cd /tmp/b45
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate45.py 2>&1 | grep -v pinned | tail -4; } > /tmp/j41.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids dde890d478,add5ec8937,cc6d168e0a,f20de05a64,4a351e360a,d827d54f60 > /tmp/j41-ans.log 2>&1; grep -E "differ from s6|Negative|^\| [0-9a-f]{10} " /tmp/j41-ans.log; } >> /tmp/j41.log 2>&1
touch /tmp/job41.done
