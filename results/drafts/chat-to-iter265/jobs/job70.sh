#!/bin/sh
cd /tmp/ff
runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j70-build.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j70-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j70-rt.log)"; } > /tmp/j70.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j70.log 2>&1
touch /tmp/job70.done
