#!/bin/sh
cd /tmp/b46b
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j58-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j58-rt.log)"; } > /tmp/j58.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j58.log 2>&1
sed -e "s#/home/claude/forth-vm-evolution/lab/evolve#/tmp/b46b/lab/evolve#; s#/home/claude/forth-vm-evolution/results#/tmp/b46b/results#" /tmp/gate46.py > /tmp/gate46c.py
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate46c.py 2>&1 | grep -v pinned | tail -3; } >> /tmp/j58.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids c1cc8e127c,cc6d168e0a,f20de05a64,4a351e360a,26be0b1ed2,a1b35be27d > /tmp/j58-ans.log 2>&1; grep -E "differ from s6|Negative|^\| [0-9a-f]{10} " /tmp/j58-ans.log; } >> /tmp/j58.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j58-ob.log 2>&1; echo "exit $?: $(tail -1 /tmp/j58-ob.log)"; } >> /tmp/j58.log 2>&1
{ echo "== readline-check"; runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 d3149e10c6 > /tmp/j58-rl.log 2>&1; echo "exit $?: $(tail -1 /tmp/j58-rl.log)"; } >> /tmp/j58.log 2>&1
touch /tmp/job58.done
