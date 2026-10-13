#!/bin/sh
cd /tmp/b46b
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate46c.py 2>&1 | grep -v pinned | tail -3; } > /tmp/j59.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids c1cc8e127c,cc6d168e0a,f20de05a64,4a351e360a,26be0b1ed2,a1b35be27d > /tmp/j59-ans.log 2>&1; grep -E "differ from s6|Negative|^\| [0-9a-f]{10} " /tmp/j59-ans.log; } >> /tmp/j59.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j59-ob.log 2>&1; echo "exit $?: $(tail -1 /tmp/j59-ob.log)"; } >> /tmp/j59.log 2>&1
{ echo "== readline-check"; runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 d3149e10c6 > /tmp/j59-rl.log 2>&1; echo "exit $?: $(tail -1 /tmp/j59-rl.log)"; } >> /tmp/j59.log 2>&1
touch /tmp/job59.done
