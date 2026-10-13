#!/bin/sh
cd /tmp
runuser -u claude -- python3 /tmp/eng-id.py /home/claude/forth-vm-evolution /tmp/engM d3149e10c6 cc6d168e0a add5ec8937 > /tmp/j19-m.log 2>&1
runuser -u claude -- python3 /tmp/eng-id.py /tmp/b44 /tmp/engB2 d3149e10c6 cc6d168e0a add5ec8937 > /tmp/j19-b.log 2>&1
touch /tmp/job19.done
