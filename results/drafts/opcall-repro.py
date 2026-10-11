import os, sys, json, shutil, subprocess
os.chdir('/tmp/fb/r'); sys.path.insert(0, '/tmp/fb/r/lab/evolve'); sys.argv = ['x']
import evolve as E
E.setup()
G = {}
for l in open('/tmp/s40/run/pack/db.jsonl'):
    try: r = json.loads(l)
    except ValueError: continue
    if str(r.get('status', '')).startswith('died: corpus'): G[r['id']] = r['genome']
def run(g, tag):
    d = os.path.join(E.EV, 'cd'); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(E.canon(g), d); pw = E.private_work(d)
        out = subprocess.run([eng, img], cwd=pw, input=open(E.CORPUS, 'rb').read(), capture_output=True, timeout=60).stdout
        ok = out == E.REF_CORPUS
        if not ok and tag == 'as recorded':
            a, b = E.REF_CORPUS.split(b'\n'), out.split(b'\n'); i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            print('   first difference, line %d: expected %r got %r' % (i, a[i][:70] if i < len(a) else b'', b[i][:70] if i < len(b) else b''))
        return 'right' if ok else 'WRONG'
    except Exception as e: return 'error: ' + str(e)[:80]
for did in ('f7dc8437ff', '9586059a75'):
    g = G[did]; print('== %s: opcall %s' % (did, g.get('opcall')))
    print('   as recorded: %s' % run(g, 'as recorded'))
    for k, v in (('jit', 0), ('opcall', []), ('tracer', 0), ('varslot', 0), ('jitloop', 0), ('jitinl', 0)):
        if g.get(k) not in (None, v, 0, []): print('   %s=%s: %s' % (k, v, run(dict(g, **{k: v}), k)), flush=True)
