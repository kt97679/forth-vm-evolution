#!/bin/sh
cd /tmp/b45
{ echo "== reseed"; runuser -u claude -- sh tools/reseed.sh > /tmp/j34-reseed.log 2>&1; echo "exit $?"; tail -3 /tmp/j34-reseed.log; } > /tmp/j34.log 2>&1
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j34-build.log 2>&1; echo "exit $?: $(tail -1 /tmp/j34-build.log)"; } >> /tmp/j34.log 2>&1
{ echo "== names-check"; runuser -u claude -- python3 lab/evolve/names-check.py 2>&1 | grep -E "^- |PASS|FAIL|Error|error"; } >> /tmp/j34.log 2>&1
touch /tmp/job34.done
