#!/bin/sh
cd /tmp/b46b
{ echo "== names-check"; runuser -u claude -- python3 lab/evolve/names-check.py 2>&1 | grep -E "PASS|FAIL" | tail -1; } > /tmp/j60.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids c1cc8e127c,cc6d168e0a,f20de05a64,4a351e360a,26be0b1ed2,a1b35be27d > /tmp/j60-ans.log 2>&1; grep -E "differ from s6|Negative|^\| [0-9a-f]{10} " /tmp/j60-ans.log; } >> /tmp/j60.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j60-ob.log 2>&1; echo "exit $?: $(tail -1 /tmp/j60-ob.log)"; } >> /tmp/j60.log 2>&1
{ echo "== readline-check"; runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 d3149e10c6 > /tmp/j60-rl.log 2>&1; echo "exit $?: $(tail -1 /tmp/j60-rl.log)"; } >> /tmp/j60.log 2>&1
touch /tmp/job60.done
