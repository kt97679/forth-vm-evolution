#!/bin/sh
cd /tmp/b45
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh 2>&1 | tail -1; } > /tmp/j27.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j27-ob.log 2>&1; echo "exit $?"; sed -n '/## T3/,$p' /tmp/j27-ob.log; } >> /tmp/j27.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j27-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j27-rt.log)"; } >> /tmp/j27.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j27.log 2>&1
{ echo "== sizes master -> terminal fix"; runuser -u claude -- python3 /tmp/eng-id.py /home/claude/forth-vm-evolution /tmp/engF add5ec8937 d3149e10c6 cc6d168e0a 2>&1 | grep -v pinned
  runuser -u claude -- python3 /tmp/eng-id.py /tmp/b45 /tmp/engG add5ec8937 d3149e10c6 cc6d168e0a 2>&1 | grep -v pinned; } >> /tmp/j27.log 2>&1
touch /tmp/job27.done
