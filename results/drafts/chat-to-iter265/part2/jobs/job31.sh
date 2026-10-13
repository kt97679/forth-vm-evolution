#!/bin/sh
cd /tmp/b45
runuser -u claude -- bash tools/run-tests.sh > /tmp/j31-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j31-rt.log)" > /tmp/j31.log
touch /tmp/job31.done
