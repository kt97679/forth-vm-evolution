import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
g = E.canon(E.recorded_genome('3456ac1e5e')); d = os.path.join(E.EV, 'elf'); shutil.rmtree(d, ignore_errors=True)
eng, img = E.build(g, d)
print('engine', os.path.getsize(eng), 'image', os.path.getsize(img))
print(subprocess.run(['readelf', '-lSW', eng], stdout=subprocess.PIPE, text=True).stdout)
