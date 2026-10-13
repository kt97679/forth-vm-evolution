#!/bin/sh
cd /tmp/batch43
B="runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh"
cp /tmp/file-sysc5.4.new forth/file-sysc5.4
sed -i "s/  R> R> IF 1+ -1 ELSE 0 THEN  SWAP FS-E @ +! ;/  R> R> IF -1 ELSE 0 THEN  SWAP FS-E @ +! ;/" forth/file-sysc5.4
if cmp -s forth/file-sysc5.4 /tmp/file-sysc5.4.new; then echo "fault B: NOT PLANTED" > /tmp/v-faultB.txt; else
  $B > /tmp/b-fault.log 2>&1
  runuser -u claude -- python3 lab/evolve/readline-check.py be1620e346 > /tmp/v-fault-B.log 2>&1
  echo "fault B: readline-check exit $? - $(grep -E 'fsys 5:' /tmp/v-fault-B.log | head -1)" > /tmp/v-faultB.txt
fi
cp /tmp/file-sysc5.4.new forth/file-sysc5.4; $B > /tmp/b-restore.log 2>&1
cmp forth/file-sysc5.4 /tmp/file-sysc5.4.new && echo "restored, rebuilt" >> /tmp/v-faultB.txt
runuser -u claude -- python3 lab/evolve/fsys-count.py be1620e346 --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --levels 5 --works kernel > /tmp/v-fc-tool.log 2>&1
touch /tmp/job5.done
