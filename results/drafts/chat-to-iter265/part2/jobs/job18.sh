#!/bin/sh
cd /tmp/b44
t() { s=$(date +%s); "$@"; echo "exit $? $(( $(date +%s) - s )) s"; }
{ echo "== readline-check"; t runuser -u claude -- python3 lab/evolve/readline-check.py d3149e10c6 cc6d168e0a 2>&1 | grep -v pinned | tail -4; } > /tmp/v44b.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/v44b-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/v44b-rt.log)"; } >> /tmp/v44b.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/v44b.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/v44b-ob.log 2>&1; echo "exit $?: $(tail -1 /tmp/v44b-ob.log)"; } >> /tmp/v44b.log 2>&1
{ echo "== gate"; t runuser -u claude -- python3 /tmp/gate44b.py 2>&1 | grep -v pinned; } >> /tmp/v44b.log 2>&1
{ echo "== ans-check"; runuser -u claude -- python3 lab/evolve/ans-check.py --ids d3149e10c6,cc6d168e0a 2>&1 | grep -E "differ from s6|Negative"; } >> /tmp/v44b.log 2>&1
{ echo "== engine sizes (master / with both changes)"; for id in d3149e10c6 cc6d168e0a add5ec8937; do
    a=$(runuser -u claude -- python3 /tmp/eng-id.py /home/claude/forth-vm-evolution /tmp/engC $id 2>/dev/null | grep -v pinned)
    b=$(runuser -u claude -- python3 /tmp/eng-id.py /tmp/b44 /tmp/engC $id 2>/dev/null | grep -v pinned)
    echo "$a  ->  $b"; done; } >> /tmp/v44b.log 2>&1
touch /tmp/job18.done
