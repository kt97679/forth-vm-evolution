#!/bin/sh
cd /tmp/ansall
runuser -u claude -- python3 lab/evolve/ans-check.py --ids $(cat /tmp/ansall-ids.txt) > /tmp/j69-ans.log 2>&1
touch /tmp/job69.done
