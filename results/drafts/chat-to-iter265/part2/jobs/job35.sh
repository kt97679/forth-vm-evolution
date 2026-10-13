#!/bin/sh
cd /tmp/b45
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j35-build.log 2>&1; echo "exit $?: $(tail -1 /tmp/j35-build.log)"; } > /tmp/j35.log 2>&1
{ echo "== names-check"; runuser -u claude -- python3 lab/evolve/names-check.py 2>&1 | grep -E "^- |PASS|FAIL|rror"; } >> /tmp/j35.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j35-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j35-rt.log)"; } >> /tmp/j35.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j35.log 2>&1
touch /tmp/job35.done
