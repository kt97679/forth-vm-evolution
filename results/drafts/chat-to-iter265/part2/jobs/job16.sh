#!/bin/sh
cd /tmp/b44
t() { s=$(date +%s); "$@"; echo "exit $? $(( $(date +%s) - s )) s"; }
{ echo "== build"; t runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh 2>&1 | tail -1; } > /tmp/v44.log 2>&1
{ echo "== readline-check"; t runuser -u claude -- python3 lab/evolve/readline-check.py be1620e346 cc6d168e0a 2>&1 | grep -v pinned; } >> /tmp/v44.log 2>&1
{ echo "== run-tests"; t runuser -u claude -- bash tools/run-tests.sh 2>&1 | tail -1; } >> /tmp/v44.log 2>&1
{ echo "== validate"; t runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/v44.log 2>&1
{ echo "== outbuf-check"; t runuser -u claude -- python3 lab/evolve/outbuf-check.py 2>&1 | tail -1; } >> /tmp/v44.log 2>&1
cat > /tmp/gate44.py <<'PY'
import os, sys, json
sys.argv = ['x']; sys.path.insert(0, '/tmp/b44/lab/evolve'); import evolve as E
E.setup()
recs = [json.loads(l) for l in open('/tmp/b44/results/evolve-amd-ryzen-7-pro-8840hs-seed43.md') if l.startswith('{"bin"')]
bad = 0; n = 0
for r in recs:
    if r['genome'].get('fsys', 0): continue
    n += 1; d = os.path.join(E.EV, 'g44')
    try: eng, img = E.build(E.canon(r['genome']), d); E.alive(eng, img, E.private_work(d))
    except Exception as e: bad += 1; print('DIED', r['id'], e)
print('fsys 0 front designs alive: %d of %d' % (n - bad, n))
PY
{ echo "== gate, every fsys-0 design of seed 43's front"; t runuser -u claude -- python3 /tmp/gate44.py 2>&1 | grep -v pinned; } >> /tmp/v44.log 2>&1
{ echo "== ans-check"; t runuser -u claude -- python3 lab/evolve/ans-check.py --ids cc6d168e0a,5609c7f1b3 2>&1 | grep -E "differ from s6|Negative"; } >> /tmp/v44.log 2>&1
touch /tmp/job16.done
