# results/rehearsal-405.md - the after-seed-62 batch's rehearsal (Iteration 405); run in a scratch clone with the batch applied.
import json, os, shutil, sys
os.chdir('/tmp/b62'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed59.md') if l.startswith('{"bin"') and '"cd9d470f51"' in l)
g = dict(r['genome'], tail=1, jit=0); g = E.canon(g); d = '/tmp/rh/t2c'; shutil.rmtree(d, ignore_errors=True)
os.environ.update(E.W4_ENV)
try: E.build(g, d); print('built')
except Exception as e: print('EXC', str(e)[:200])
print('tag2', g.get('tag2'), 'tos', g.get('tos'), 'compiler', E.express(g).get('compiler'))
