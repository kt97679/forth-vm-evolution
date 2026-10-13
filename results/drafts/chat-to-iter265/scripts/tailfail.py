import json, os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
R = {}
for l in open('/tmp/s46/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
g = E.canon(R['cb0545f94f']['genome']); d = os.path.join(E.EV, 'tf'); shutil.rmtree(d, ignore_errors=True)
try:
    E.build(g, d); print('built OK')
except Exception as e:
    print('error:', str(e)[:300])
