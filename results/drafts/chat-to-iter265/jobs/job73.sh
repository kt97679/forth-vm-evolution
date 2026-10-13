#!/bin/sh
cd /tmp/mo
runuser -u claude -- python3 lab/evolve/ans-check.py --ids k23bb2087f,k33bb2087f,k2fe3c9c39,k3fe3c9c39,k2cfee5345,k3cfee5345 > /tmp/j73-ans.log 2>&1
touch /tmp/job73.done
