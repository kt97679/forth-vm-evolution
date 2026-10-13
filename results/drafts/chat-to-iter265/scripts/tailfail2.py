import json, os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/tmp/b46b/lab/evolve'); import evolve as E
E.setup()
R = {}
for l in open('/tmp/s46/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
g = E.canon(R['cb0545f94f']['genome']); d = os.path.join(E.EV, 'tf'); shutil.rmtree(d, ignore_errors=True)
eng, img = E.build(g, d); print('built OK', os.path.getsize(eng), os.path.getsize(img))
import subprocess
r = subprocess.run([eng, img], input=E.program('corpus', single=True), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd=E.EV)
print('corpus exit', r.returncode, r.stdout.replace(b'\r', b'').decode(errors='replace').strip().split('\n')[-1][:80])
print('reference', open(os.path.join(E.EV, 'corpus-ref.txt')).read()[-80:] if os.path.exists(os.path.join(E.EV, 'corpus-ref.txt')) else '')
