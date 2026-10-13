import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
g = E.canon(E.recorded_genome('3456ac1e5e')); d = os.path.join(E.EV, 'sz3'); shutil.rmtree(d, ignore_errors=True)
eng, img = E.build(g, d)
print('engine', os.path.getsize(eng))
out = subprocess.run(['nm', '-S', '--size-sort', os.path.join(d, 'engine.full')], stdout=subprocess.PIPE, text=True).stdout.split('\n')
rows = []
for l in out:
    f = l.split()
    if len(f) == 4: rows.append((int(f[1], 16), f[2], f[3]))
text = [r for r in rows if r[1] in 'tTrRdD']
print('in the file (code, read-only and initialised data), largest:')
for s, k, n in sorted(text, reverse=True)[:22]: print('  %5d %s %s' % (s, k, n))
print('  ... %d symbols, %d bytes in all' % (len(text), sum(s for s, _, _ in text)))
