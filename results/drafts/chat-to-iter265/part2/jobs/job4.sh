#!/bin/sh
# planted faults (prompts/15): each must turn readline-check red; then the tightened library back
while [ ! -e /tmp/job3.done ]; do sleep 5; done
cd /tmp/batch43
B="runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh"
for f in A B; do
  cp /tmp/file-sysc5.4.new forth/file-sysc5.4
  if [ $f = A ]; then   # the fast path keeps a CR before the LF
    sed -i 's/      DUP IF 2DUP + 1- C@ 13 = IF 1- THEN THEN    \\ a CR before the LF ends the line too/      DUP IF 2DUP + 1- C@ 13 = IF THEN THEN/' forth/file-sysc5.4
  else                  # the general way leaves the LF it found unconsumed
    sed -i "s/  R> R> IF 1+ -1 ELSE 0 THEN  SWAP FS-E @ +! ;/  R> R> IF -1 ELSE 0 THEN  SWAP FS-E @ +! ;/" forth/file-sysc5.4
  fi
  if cmp -s forth/file-sysc5.4 /tmp/file-sysc5.4.new; then echo "fault $f: NOT PLANTED (the edit missed)" >> /tmp/v-faults.log; continue; fi
  $B > /tmp/b-fault.log 2>&1
  runuser -u claude -- python3 lab/evolve/readline-check.py be1620e346 > /tmp/v-fault-$f.log 2>&1
  echo "fault $f: readline-check exit $? - $(grep -E 'fsys 5:' /tmp/v-fault-$f.log | head -1)" >> /tmp/v-faults.log
done
cp /tmp/file-sysc5.4.new forth/file-sysc5.4; $B > /tmp/b-restore.log 2>&1
cmp forth/file-sysc5.4 /tmp/file-sysc5.4.new && echo "restored" >> /tmp/v-faults.log
touch /tmp/job4.done
