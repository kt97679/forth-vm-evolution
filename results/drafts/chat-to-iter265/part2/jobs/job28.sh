#!/bin/sh
cd /tmp/b45
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh 2>&1 | tail -1; } > /tmp/j28.log 2>&1
{ echo "== s8 division"; cd build; printf "1 2 + . CR\n: T 1 0 / ; ' T CATCH . CR\n1 0 /\n.\" after\" CR\n" | ./s8-full-64 s8-full-s64.img 2>&1 | tr -d '\r' | tr '\n' '|'; echo " status $?"; printf ": T 1 0 / ; ' T CATCH . CR\n" | ./s8-spncv8-64 s8-spncv8-s64.img 2>&1 | tr -d '\r' | tr '\n' '|'; echo " status $?"; cd ..; } >> /tmp/j28.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j28-ob.log 2>&1; echo "exit $?"; grep "fsys 0:" /tmp/j28-ob.log | tail -1; } >> /tmp/j28.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j28-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j28-rt.log)"; } >> /tmp/j28.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j28.log 2>&1
{ echo "== sizes"; rm -rf /tmp/engG/*; runuser -u claude -- python3 /tmp/eng-id.py /tmp/b45 /tmp/engG add5ec8937 d3149e10c6 cc6d168e0a 2>&1 | grep -v pinned; } >> /tmp/j28.log 2>&1
sed -i 's#/home/claude/forth-vm-evolution/lab/evolve#/tmp/b45/lab/evolve#' /tmp/gate45.py
{ echo "== gate"; runuser -u claude -- python3 /tmp/gate45.py 2>&1 | grep -v pinned; } >> /tmp/j28.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids d3149e10c6,cc6d168e0a 2>&1 | grep -E "differ from s6|Negative"; } >> /tmp/j28.log 2>&1
touch /tmp/job28.done
