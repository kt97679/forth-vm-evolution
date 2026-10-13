#!/bin/sh
cd /home/claude/forth-vm-evolution
runuser -u claude -- python3 lab/evolve/gate.py results/evolve-amd-ryzen-7-pro-8840hs-seed46.md /tmp/c46/pack/compare-fronts.md 2>&1 | grep -v pinned > /tmp/j71.log
touch /tmp/job71.done
