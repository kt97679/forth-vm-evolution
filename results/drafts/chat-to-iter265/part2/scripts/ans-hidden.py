# ans-check.py on designs whose unused names are hidden (Iteration 223): the hidden-names.py rule, applied in E.build
import os, sys, glob, re, shutil, runpy
ROOT = '/home/claude/forth-vm-evolution'; ids = sys.argv[1].split(',')
sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); sys.argv = ['x']; import evolve as E
E.setup()
srcs = (glob.glob(ROOT + '/tests/ans/*') + glob.glob(ROOT + '/tests/core/*') + glob.glob(ROOT + '/bench/*.fth') + glob.glob(ROOT + '/tests/shell/*')
        + [E.CORPUS] + [ROOT + '/forth/' + f for f in ('extend.4', 'cross.4', 'kernel.4')])
toks = set()
for p in srcs:
    if os.path.isfile(p): toks |= {t.upper() for t in re.findall(r'\S+', open(p, errors='replace').read())}
orig = E.build; table = {}
for did in ids:
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'anshide'); shutil.rmtree(d, ignore_errors=True); sm = d + '.sym'
    os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
    try: orig(g, d)
    finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
    table[E.gid(g)] = sorted({n for n in (l.split(None, 2)[2].strip() for l in open(sm)) if n and n.upper() not in toks})
    print('%s: %d names hidden' % (did, len(table[E.gid(g)])), flush=True)
def build(g, d):
    hide = table.get(E.gid(E.canon(g)))
    if not hide or E.hand_made(g): return orig(g, d)
    saved = E.FSYS_INTERNAL
    if E.fsys_on(g): E.FSYS_INTERNAL = tuple(E.FSYS_INTERNAL) + tuple(hide)
    else: E.CONVERT_EXTRA[:] = ['--headerless', ','.join(hide)]
    try: return orig(g, d)
    finally: E.FSYS_INTERNAL = saved; E.CONVERT_EXTRA[:] = []
E.build = build
sys.argv = [ROOT + '/lab/evolve/ans-check.py', '--ids', ','.join(ids)]
runpy.run_path(ROOT + '/lab/evolve/ans-check.py', run_name='__main__')
