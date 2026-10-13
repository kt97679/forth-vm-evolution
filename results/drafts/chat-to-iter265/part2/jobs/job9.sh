#!/bin/sh
cd /home/claude/forth-vm-evolution
for id in 28677d13b1 cc6d168e0a fc09f6373d; do
  runuser -u claude -- python3 lab/evolve/jitstack.py $id --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --db results/evolve-amd-ryzen-7-pro-8840hs-seed43.md > /tmp/j9-$id.log 2>&1; echo "exit $?" >> /tmp/j9-$id.log
done
touch /tmp/job9.done
