import os, sys, shutil, collections, importlib.util
ARGS = [int(x) for x in sys.argv[1:]]; sys.argv = ['evolve.py']
spec = importlib.util.spec_from_file_location('E', '/tmp/fe/b/lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
E.setup()
if not E.LONGF: E.long_files()
for v in ARGS:
    g = dict(E.recorded_genome('0ceb043115'))
    if v: g['threads'] = v
    d = os.path.join(E.EV, 'th2-%d' % v); shutil.rmtree(d, ignore_errors=True)
    E.PROFILING[0] = True
    try: eng, img = E.build(dict(E.canon(g), tail=0, msc=0), d)
    finally: E.PROFILING[0] = False
    pw = E.private_work(d); out = []
    for w in ('kernel', 'corpus', 'parse'):
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=60, env=dict(os.environ, VMPROF=pf))
        out.append('%s %.2fM' % (w, sum(int(l.split()[2]) for l in open(pf) if l.startswith('I ')) / 1e6))
    print('%3d chains: %s' % ({0: 32, 1: 64, 2: 128, 3: 16}[v], ', '.join(out)), flush=True)
