#!/bin/sh
cd /tmp/w230 && runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j49-build.log 2>&1
runuser -u claude -- python3 /tmp/disp.py /tmp/w230 add5ec8937,c1cc8e127c > /tmp/j49.log 2>&1
runuser -u claude -- python3 /tmp/disp.py /home/claude/forth-vm-evolution add5ec8937,c1cc8e127c >> /tmp/j49.log 2>&1
touch /tmp/job49.done
