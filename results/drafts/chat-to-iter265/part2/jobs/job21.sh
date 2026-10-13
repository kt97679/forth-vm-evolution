#!/bin/sh
cd /tmp/b44s
B="runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh"
cp forth/file-sysc3.4 /tmp/fs3-good.4
# the planted fault (prompts/15): READ from a seekable stdin no longer stops at the first editing character
sed -i 's/    0 SWAP DUP FS-UPTO-EDIT FS-BACK EXIT/    0 SWAP DUP FS-BACK EXIT/' forth/file-sysc3.4
if cmp -s forth/file-sysc3.4 /tmp/fs3-good.4; then echo "fault NOT planted" > /tmp/j21.log; else
  $B > /dev/null 2>&1
  runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 2>&1 | grep -E "READ from a stdin|PASS|FAIL" > /tmp/j21.log
fi
cp /tmp/fs3-good.4 forth/file-sysc3.4; $B > /dev/null 2>&1
cmp forth/file-sysc3.4 /tmp/fs3-good.4 && echo "restored" >> /tmp/j21.log
t() { s=$(date +%s); "$@"; echo "exit $? $(( $(date +%s) - s )) s"; }
{ echo "== readline-check"; runuser -u claude -- python3 lab/evolve/readline-check.py add5ec8937 d3149e10c6 2>&1 | grep -v pinned | tail -6; } >> /tmp/j21.log 2>&1
{ echo "== outbuf-check"; runuser -u claude -- python3 lab/evolve/outbuf-check.py > /tmp/j21-ob.log 2>&1; echo "exit $?: $(tail -1 /tmp/j21-ob.log)"; } >> /tmp/j21.log 2>&1
{ echo "== run-tests"; runuser -u claude -- bash tools/run-tests.sh > /tmp/j21-rt.log 2>&1; echo "exit $?: $(tail -1 /tmp/j21-rt.log)"; } >> /tmp/j21.log 2>&1
{ echo "== validate"; runuser -u claude -- python3 lab/evolve/evolve.py --validate 2>&1 | grep -c IDENTICAL; } >> /tmp/j21.log 2>&1
cat > /tmp/gate44c.py <<'PY'
import os, sys, json
sys.argv = ['x']; sys.path.insert(0, '/tmp/b44s/lab/evolve'); import evolve as E
E.setup()
recs = [json.loads(l) for l in open('/tmp/b44s/results/evolve-amd-ryzen-7-pro-8840hs-seed43.md') if l.startswith('{"bin"')]
bad = n = 0
for r in recs:
    for lev in ((3, 4, 5) if r['genome'].get('fsys', 0) >= 3 else ()):
        n += 1; d = os.path.join(E.EV, 'g44c')
        try: eng, img = E.build(E.canon(dict(r['genome'], fsys=lev)), d); E.alive(eng, img, E.private_work(d))
        except Exception as e: bad += 1; print('DIED', r['id'], lev, e, flush=True)
print('seed 43 front designs with fsys 3-4, each at fsys 3, 4 and 5: %d of %d alive' % (n - bad, n), flush=True)
PY
{ echo "== gate"; t runuser -u claude -- python3 /tmp/gate44c.py 2>&1 | grep -v pinned; } >> /tmp/j21.log 2>&1
{ echo "== ans-check fsys 3"; runuser -u claude -- env ANS_SET=fsys=3 python3 lab/evolve/ans-check.py --ids add5ec8937,8dab7c6af4 2>&1 | grep -E "differ from s6|Negative"; } >> /tmp/j21.log 2>&1
touch /tmp/job21.done
