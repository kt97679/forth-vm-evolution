import os, sys, shutil, collections
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
g = E.canon(E.recorded_genome('3456ac1e5e')); d = os.path.join(E.EV, 'cm'); shutil.rmtree(d, ignore_errors=True)
cm = d + '.map'; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
try: eng, img = E.build(g, d)
finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
lines = [l.rstrip('\n') for l in open(cm)]
print(collections.Counter(l.split()[0] for l in lines if l.strip()))
for t in sorted(set(l.split()[0] for l in lines if l.strip())):
    print(t, '|', next(l for l in lines if l.startswith(t + ' '))[:150])
