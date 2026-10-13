import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
g = E.canon(E.recorded_genome('28677d13b1')); d = os.path.join(E.EV, 'jd'); shutil.rmtree(d, ignore_errors=True)
eng, img = E.build(g, d)
print('engine', eng, os.path.getsize(eng))
print({k: g[k] for k in sorted(g) if k.startswith('jit') or k in ('tail', 'enc', 'tos')})
