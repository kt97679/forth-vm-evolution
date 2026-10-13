#!/bin/sh
W=fib,loop,corpus,kernel,bubble,ackermann
runuser -u claude -- python3 /tmp/pages2.py /tmp/b44s add5ec8937,d3149e10c6,cc6d168e0a,fc09f6373d $W > /tmp/j22-after.log 2>&1
runuser -u claude -- python3 /tmp/pages2.py /home/claude/forth-vm-evolution add5ec8937,d3149e10c6,cc6d168e0a,fc09f6373d $W > /tmp/j22-master.log 2>&1
touch /tmp/job22.done
