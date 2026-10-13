import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
orig_rt = E.rt
res = {}
for mode in ('as is', '-flto'):
    if mode == '-flto': E.rt = lambda: orig_rt() + ['-flto']
    else: E.rt = orig_rt
    for did in ('3456ac1e5e', 'fe3c9c3940', '3bb2087f9d'):
        g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'lto'); shutil.rmtree(d, ignore_errors=True)
        try:
            eng, img = E.build(g, d)
            r = subprocess.run([eng, img], input=E.program('corpus', single=True), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd=E.EV)
            res[(mode, did)] = '%d (%s)' % (os.path.getsize(eng), 'corpus ok' if b'CORPUS-REACHED-END' in r.stdout else 'corpus FAILED')
        except Exception as e:
            res[(mode, did)] = 'died: ' + str(e)[:60]
for did in ('3456ac1e5e', 'fe3c9c3940', '3bb2087f9d'):
    print(did, ' | '.join('%s: %s' % (m, res[(m, did)]) for m in ('as is', '-flto')))
