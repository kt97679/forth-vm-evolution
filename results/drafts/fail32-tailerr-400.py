# Iteration 400 (results/fail32-400.md): one design's 4-byte build with every failing command and its errors printed -
# how the __int128 error was found. python3 THIS TREE DB ID.
import json, os, shutil, sys
tree, db, i = sys.argv[1], sys.argv[2], sys.argv[3]; os.chdir(tree)
sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab/evolve')); import evolve as E
g = next(json.loads(l)['genome'] for l in open(db) if i in l and json.loads(l)['id'] == i)
orig = E.sh
def sh(cmd, *a, **k):
    r = orig(cmd, *a, **k)
    if getattr(r, 'returncode', 0):
        print('FAILED:', ' '.join(map(str, cmd))[:700]); err = r.stderr if isinstance(r.stderr, str) else (r.stderr or b'').decode('utf-8', 'replace')
        print('STDERR:', '\n'.join(l for l in err.splitlines() if 'error' in l.lower())[:1500] or err[:1500])
    return r
E.sh = sh
g32 = E.canon(dict(g, jit=0)); d = '/tmp/s58/tail32'; shutil.rmtree(d, ignore_errors=True)
os.environ.update(E.W4_ENV)
try: E.build(g32, d); print('BUILT at 4-byte cells')
except Exception as e: print('EXC', str(e)[:300])
