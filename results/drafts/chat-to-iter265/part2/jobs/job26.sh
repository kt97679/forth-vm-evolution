#!/bin/sh
cd /home/claude/forth-vm-evolution
{ echo "== reseed"; runuser -u claude -- sh tools/reseed.sh 2>&1 | tail -2; } > /tmp/j26.log 2>&1
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh 2>&1 | tail -1; } >> /tmp/j26.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j26-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j26-rt.log)"; } >> /tmp/j26.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j26.log 2>&1
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate45.py 2>&1 | grep -v pinned; } >> /tmp/j26.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids dde890d478,7e75098550,6c6e22311b,6838c1e840,7736a2e7de,e566e2711d,a80ae33266,860a70d9d3,d562c3ce5a,b679202541,fc97d8fcf7,9d6632d0b5 > /tmp/j26-ans.log 2>&1; grep -E "differ from s6|Negative" /tmp/j26-ans.log; python3 - <<'PY' >> /tmp/j26.log
import re
s = open('/tmp/j26-ans.log').read()
rows = re.findall(r'^\| ([a-z]+[^|]*\.f[a-z]*) \| (\d+) \| (\d+) \| (\S+) \|', s, re.M)
print('s6: %d files, %d tests, %d failed, %d whole' % (len(rows), sum(int(r[1]) for r in rows), sum(int(r[2]) for r in rows), sum(r[3] == 'yes' for r in rows)))
PY
} >> /tmp/j26.log 2>&1
touch /tmp/job26.done
