import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
orig = E.ccflags
for param in (None, 0, 32, 128):
    E.ccflags = (lambda g, p=param: orig(g) + ['--param', 'max-goto-duplication-insns=%d' % p]) if param is not None else orig
    out = []
    for did in ('3456ac1e5e', 'fe3c9c3940', '697f12fecc'):
        g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'gd3'); shutil.rmtree(d, ignore_errors=True)
        try:
            eng, img = E.build(g, d)
            r = subprocess.run([eng, img], input=E.program('corpus', single=True), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd=E.EV)
            out.append('%s %d%s' % (did, os.path.getsize(eng), '' if b'CORPUS-REACHED-END' in r.stdout else ' FAILED'))
        except Exception as e: out.append('%s died' % did)
    print('max-goto-duplication-insns=%-7s %s' % ('default' if param is None else param, ' | '.join(out)), flush=True)
