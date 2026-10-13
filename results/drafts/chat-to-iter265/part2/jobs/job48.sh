#!/bin/sh
cd /home/claude/forth-vm-evolution
{ echo "== reseed"; runuser -u claude -- sh tools/reseed.sh > /tmp/j48-reseed.log 2>&1; echo "exit $?: $(tail -2 /tmp/j48-reseed.log | head -1)"; } > /tmp/j48.log 2>&1
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j48-build.log 2>&1; echo "exit $?: $(tail -1 /tmp/j48-build.log)"; } >> /tmp/j48.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j48-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j48-rt.log)"; } >> /tmp/j48.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j48.log 2>&1
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate46.py 2>&1 | grep -v pinned | tail -4; } >> /tmp/j48.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids c1cc8e127c,4a417667da,d94d690e00,af9bd39051,844d178ca9,a1b35be27d,fe43c4b065,53b9580a2c,08c4b838cb,6755326e2f,33b9339183,cfee5345ab > /tmp/j48-ans.log 2>&1; grep -E "differ from s6|Negative" /tmp/j48-ans.log; python3 - <<'PY'
import re
s = open('/tmp/j48-ans.log').read()
rows = re.findall(r'^\| ([a-z]+[^|]*\.f[a-z]*) \| (\d+) \| (\d+) \| (\S+) \|', s, re.M)
print('s6: %d files, %d tests, %d failed, %d whole' % (len(rows), sum(int(r[1]) for r in rows), sum(int(r[2]) for r in rows), sum(r[3] == 'yes' for r in rows)))
PY
} >> /tmp/j48.log 2>&1
touch /tmp/job48.done
