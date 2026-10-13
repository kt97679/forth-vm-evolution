#!/bin/sh
cd /tmp/b45
{ echo "== reseed"; runuser -u claude -- sh tools/reseed.sh > /tmp/j36-reseed.log 2>&1; echo "exit $?: $(tail -2 /tmp/j36-reseed.log | head -1)"; } > /tmp/j36.log 2>&1
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j36-build.log 2>&1; echo "exit $?: $(tail -1 /tmp/j36-build.log)"; } >> /tmp/j36.log 2>&1
{ echo "== names-check"; runuser -u claude -- python3 lab/evolve/names-check.py 2>&1 | grep -E "^- |PASS|FAIL|rror"; } >> /tmp/j36.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j36-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j36-rt.log)"; } >> /tmp/j36.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j36.log 2>&1
touch /tmp/job36.done
