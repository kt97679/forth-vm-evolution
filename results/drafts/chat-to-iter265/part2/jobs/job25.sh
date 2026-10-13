#!/bin/sh
cd /tmp/b44s
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j25-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j25-rt.log)"; } > /tmp/j25.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j25.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j25-ob.log 2>&1; echo "exit $?"; grep -E "DIVZERO|THROW|engine fault|PASS|FAIL" /tmp/j25-ob.log | cut -c1-160; } >> /tmp/j25.log 2>&1
{ echo "== readline-check"; runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 d3149e10c6 2>&1 | grep -E "PASS|FAIL|DIFFERS|WRONG"; } >> /tmp/j25.log 2>&1
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate44d.py 2>&1 | grep -v pinned; } >> /tmp/j25.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids add5ec8937,cc6d168e0a,f20de05a64 2>&1 | grep -E "differ from s6|Negative|^\| [0-9a-f]{10} "; } >> /tmp/j25.log 2>&1
{ echo "== sizes"; mkdir -p /tmp/engE; chown claude:claude /tmp/engE
  runuser -u claude -- python3 /tmp/eng-id.py /tmp/b44s /tmp/engE add5ec8937 d3149e10c6 cc6d168e0a 2>&1 | grep -v pinned; } >> /tmp/j25.log 2>&1
touch /tmp/job25.done
