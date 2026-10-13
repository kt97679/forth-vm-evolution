import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
orig_rt = E.rt
for mode in ('as is', '-march=x86-64-v3'):
    E.rt = (lambda: orig_rt() + ['-march=x86-64-v3']) if mode != 'as is' else orig_rt
    out = []
    for did in ('3456ac1e5e', 'fe3c9c3940', '3bb2087f9d'):
        g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'march'); shutil.rmtree(d, ignore_errors=True)
        try:
            eng, img = E.build(g, d)
            r = subprocess.run([eng, img], input=E.program('corpus', single=True), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd=E.EV)
            out.append('%s %d%s' % (did, os.path.getsize(eng), '' if b'CORPUS-REACHED-END' in r.stdout else ' (corpus FAILED)'))
        except Exception as e: out.append('%s died %s' % (did, str(e)[:50]))
    print('%-18s %s' % (mode, ' | '.join(out)), flush=True)
