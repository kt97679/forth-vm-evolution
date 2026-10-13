#!/bin/sh
cd /tmp/batch43
s=$(date +%s)
runuser -u claude -- python3 lab/evolve/readline-check.py > /tmp/rlc2.log 2>&1; echo "exit $? $(( $(date +%s) - s )) s" >> /tmp/rlc2.log
s=$(date +%s)
runuser -u claude -- env TREE=/tmp/batch43 python3 /tmp/fsys-count.py be1620e346 a0c7010722 9a3de58ebe 28677d13b1 --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --levels 4,5 --works kernel,corpus --words 14 --diff 14 > /tmp/fc3.log 2>&1; echo "exit $? $(( $(date +%s) - s )) s" >> /tmp/fc3.log
touch /tmp/job1.done
