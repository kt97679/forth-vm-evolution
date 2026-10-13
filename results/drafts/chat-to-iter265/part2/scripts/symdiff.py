import os, sys, shutil
tree = sys.argv[1]; out = sys.argv[2]
sys.argv = ['x']; sys.path.insert(0, tree + '/lab/evolve'); import evolve as E
E.setup()
g = E.canon(E.recorded_genome('add5ec8937')); d = os.path.join(E.EV, 'sym'); shutil.rmtree(d, ignore_errors=True)
os.environ['SYMMAP'] = out; E.PROFILING[0] = True
try: eng, img = E.build(g, d)
finally: E.PROFILING[0] = False
print(tree, os.path.getsize(img))
