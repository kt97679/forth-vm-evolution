#!/bin/sh
cd /tmp/mo
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j75-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j75-rt.log)"; grep -A1 "engine generators" /tmp/j75-rt.log | tail -1; } > /tmp/j75.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j75.log 2>&1
{ echo "== gate"; runuser -u claude -- python3 lab/evolve/gate.py results/evolve-amd-ryzen-7-pro-8840hs-seed46.md /tmp/c46/pack/compare-fronts.md 2>&1 | grep -v pinned | tail -2; } >> /tmp/j75.log 2>&1
touch /tmp/job75.done
