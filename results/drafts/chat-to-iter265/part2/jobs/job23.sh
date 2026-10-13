#!/bin/sh
cd /tmp/b44s
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j23-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j23-rt.log)"; } > /tmp/j23.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j23.log 2>&1
{ echo "== gate, all 165"; runuser -u claude -- python3 /tmp/gate44d.py 2>&1 | grep -v pinned; } >> /tmp/j23.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids add5ec8937,fc09f6373d 2>&1 | grep -E "differ from s6|Negative"; } >> /tmp/j23.log 2>&1
{ echo "== engine sizes (master -> b44s)"; mkdir -p /tmp/engD; chown claude:claude /tmp/engD
  runuser -u claude -- python3 /tmp/eng-id.py /tmp/b44s /tmp/engD add5ec8937 d3149e10c6 cc6d168e0a 2>&1 | grep -v pinned
  for i in add5ec8937 d3149e10c6 cc6d168e0a; do echo "$i engine $(stat -c %s /tmp/engM/$i.engine) -> $(stat -c %s /tmp/engD/$i.engine)"; done; } >> /tmp/j23.log 2>&1
touch /tmp/job23.done
