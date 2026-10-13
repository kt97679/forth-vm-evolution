#!/bin/sh
cd /tmp/batch43
IDS="be1620e346 a0c7010722 9a3de58ebe 28677d13b1"
B="runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh"
runuser -u claude -- python3 /tmp/sizes.py $IDS > /tmp/size-new.log 2>&1
cp /tmp/file-sysc5.4.orig forth/file-sysc5.4; cp /tmp/evolve.py.old lab/evolve/evolve.py; $B > /tmp/b-old.log 2>&1
runuser -u claude -- python3 /tmp/sizes.py $IDS > /tmp/size-old.log 2>&1
cp /tmp/file-sysc5.4.cell forth/file-sysc5.4; cp /tmp/evolve.py.cell lab/evolve/evolve.py; $B > /tmp/b-cell.log 2>&1
runuser -u claude -- python3 /tmp/sizes.py $IDS > /tmp/size-cell.log 2>&1
runuser -u claude -- env TREE=/tmp/batch43 python3 /tmp/fsys-count.py be1620e346 9a3de58ebe 28677d13b1 --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --levels 5 --works kernel,corpus --words 6 > /tmp/fc-cell.log 2>&1
cp /tmp/file-sysc5.4.new forth/file-sysc5.4; cp /tmp/evolve.py.new lab/evolve/evolve.py; $B > /tmp/b-new.log 2>&1
touch /tmp/job2.done
