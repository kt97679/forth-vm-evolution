"""results/drafts/rage-select-as-tegra-652.py OUT DB NAME=ID,... --list - lab/evolve/export-arm.py's choice of designs as the
Tegra makes it, on any host (Iteration 652): os.uname() says armv7l and clang is off the PATH before evolve.py is imported,
so express() sees what the Tegra's sees - no design with the JIT (jit_on() wants x86_64), none with clang (the compiler
gene needs it on the PATH): the ten all GCC without the JIT, why the chain at 2e9343d91f took best-all-round. Then
export-arm.py --list must take only the GCC three. 652: least-memory, portable-arm, portable-small taken; the rest not."""
import os, shutil, runpy, sys, json
r = os.uname(); U = type('U', (), dict(sysname=r.sysname, nodename='rage', release=r.release, version=r.version, machine='armv7l'))
os.uname = lambda: U(); w = shutil.which; shutil.which = lambda c, *a, **k: None if c == 'clang' else w(c, *a, **k)
sys.path.insert(0, 'lab/evolve'); argv = sys.argv[1:]; sys.argv = ['x']; import evolve as E
print('as the Tegra: ARM32 %s, HAVE_CLANG %s - express() for the ten:' % (E.ARM32, E.HAVE_CLANG))
for l in open(argv[1]):
    g = E.canon(json.loads(l)['genome']); print('  %s %s, jit %s' % (json.loads(l)['id'], E.CC(g), bool(E.express(g).get('jit'))))
sys.argv = ["lab/evolve/export-arm.py"] + argv; runpy.run_path('lab/evolve/export-arm.py', run_name='__main__')
