#!/bin/sh
rm -rf /tmp/cmp43 /tmp/engA /tmp/engB; mkdir -p /tmp/engA /tmp/engB; chown claude:claude /tmp/engA /tmp/engB
runuser -u claude -- git clone -q /home/claude/forth-vm-evolution /tmp/cmp43
cd /tmp/cmp43 && runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j10-b.log 2>&1
IDS="28677d13b1 cc6d168e0a fc09f6373d add5ec8937"
runuser -u claude -- python3 /tmp/eng-id.py /tmp/cmp43 /tmp/engA $IDS > /tmp/j10-a.log 2>&1
cd /home/claude/forth-vm-evolution && runuser -u claude -- python3 /tmp/eng-id.py /home/claude/forth-vm-evolution /tmp/engB $IDS > /tmp/j10-bb.log 2>&1
for i in $IDS; do cmp -s /tmp/engA/$i.engine /tmp/engB/$i.engine && cmp -s /tmp/engA/$i.image /tmp/engB/$i.image && echo "$i: engine and image identical" || echo "$i: DIFFER"; done > /tmp/j10.log
runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL >> /tmp/j10.log
touch /tmp/job10.done
