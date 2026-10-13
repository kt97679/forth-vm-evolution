#!/bin/sh
cd /tmp/batch43
t() { s=$(date +%s); "$@"; echo "exit $? $(( $(date +%s) - s )) s"; }
{ echo "== run-tests"; t runuser -u claude -- bash tools/run-tests.sh 2>&1 | tail -2; } > /tmp/v-tests.log 2>&1
{ echo "== validate"; t runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | tail -8; } > /tmp/v-validate.log 2>&1
{ echo "== gate at fsys 5"; t runuser -u claude -- python3 /tmp/gate5.py be1620e346 a0c7010722 9a3de58ebe 28677d13b1; } > /tmp/v-gate.log 2>&1
{ echo "== readline-check"; t runuser -u claude -- python3 lab/evolve/readline-check.py be1620e346 9a3de58ebe 28677d13b1; } > /tmp/v-rlc.log 2>&1
{ echo "== outbuf-check"; t runuser -u claude -- python3 lab/evolve/outbuf-check.py; } > /tmp/v-outbuf.log 2>&1
{ echo "== ans-check fsys 5"; t runuser -u claude -- env ANS_SET=fsys=5 python3 lab/evolve/ans-check.py --ids be1620e346,9a3de58ebe; } > /tmp/v-ans.log 2>&1
touch /tmp/job3.done
