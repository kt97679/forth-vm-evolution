#!/bin/sh
cd /tmp/b44s
runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 > /tmp/j20.log 2>&1; echo "exit $?" >> /tmp/j20.log
touch /tmp/job20.done
