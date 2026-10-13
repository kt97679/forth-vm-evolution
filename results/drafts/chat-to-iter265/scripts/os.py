import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
base = E.recorded_genome('3456ac1e5e')
for opt in ('O2', 'Os'):
    g = E.canon(dict(base, opt=opt)); d = os.path.join(E.EV, 'os-' + opt); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    vm = [l.split() for l in subprocess.run(['nm', '-S', eng + '.full'], stdout=subprocess.PIPE, text=True).stdout.split('\n') if l.endswith(' virtual_machine')]
    print('%s: engine %d bytes, the interpreter function %d bytes' % (opt, os.path.getsize(eng), int(vm[0][1], 16) if vm else -1), flush=True)
