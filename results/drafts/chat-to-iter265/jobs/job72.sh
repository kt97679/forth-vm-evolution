#!/bin/sh
cd /tmp/mo
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j72-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j72-rt.log)"; grep -A1 "engine generators" /tmp/j72-rt.log | tail -1; } > /tmp/j72.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j72.log 2>&1
{ echo "== gate"; runuser -u claude -- python3 lab/evolve/gate.py results/evolve-amd-ryzen-7-pro-8840hs-seed46.md /tmp/c46/pack/compare-fronts.md 2>&1 | grep -v pinned | tail -2; } >> /tmp/j72.log 2>&1
{ echo "== ans"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids 3456ac1e5e,fe3c9c3940,3bb2087f9d,c05f76468e,697f12fecc,b29d66205a > /tmp/j72-ans.log 2>&1; grep -E "differ from s6|^\| [0-9a-f]{10} " /tmp/j72-ans.log; } >> /tmp/j72.log 2>&1
touch /tmp/job72.done
