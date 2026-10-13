import os, sys, glob, re, shutil, subprocess
ROOT = '/home/claude/forth-vm-evolution'
sys.argv = ['x']; sys.path.insert(0, ROOT + '/lab/evolve'); import evolve as E
E.setup()
srcs = (glob.glob(ROOT + '/tests/ans/*') + glob.glob(ROOT + '/tests/core/*') + glob.glob(ROOT + '/bench/*.fth') + glob.glob(ROOT + '/tests/shell/*')
        + [E.CORPUS] + [ROOT + '/forth/' + f for f in ('extend.4', 'cross.4', 'kernel.4')])
toks = set()
for p in srcs:
    if os.path.isfile(p): toks |= {t.upper() for t in re.findall(r'\S+', open(p, errors='replace').read())}
ANS = os.path.join(E.EV, 'ans')
def build(g, d, hide):
    saved = E.FSYS_INTERNAL
    if hide:
        if E.fsys_on(g): E.FSYS_INTERNAL = tuple(E.FSYS_INTERNAL) + tuple(hide)
        else: E.CONVERT_EXTRA[:] = ['--headerless', ','.join(hide)]
    try: return E.build(g, d)
    finally: E.FSYS_INTERNAL = saved; E.CONVERT_EXTRA[:] = []
def run(eng, img, pw, test):
    for f in os.listdir(ANS):
        p = os.path.join(pw, f)
        if os.path.lexists(p): os.remove(p)
        shutil.copy(os.path.join(ANS, f), p)
    pre = '' if test == 'prelimtest.fth' else 'S" tester.fr" INCLUDED\nS" core.fr" INCLUDED\n\nS" utilities.fth" INCLUDED\nS" errorreport.fth" INCLUDED\n'
    r = subprocess.run([eng, img], cwd=pw, input=(pre + 'S" %s" INCLUDED\nBYE\n' % test).encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    return r.returncode, r.stdout.decode(errors='replace')
for did, test in (('add5ec8937', 'toolstest.fth'), ('5f4a21fbdb', 'prelimtest.fth')):
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'diag'); shutil.rmtree(d, ignore_errors=True); sm = d + '.sym'
    os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
    try: E.build(g, d)
    finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
    hide = sorted({n for n in (l.split(None, 2)[2].strip() for l in open(sm)) if n and n.upper() not in toks})
    outs = {}
    for k, h in (('normal', []), ('hidden', hide)):
        dd = d + '-' + k; eng, img = build(g, dd, h); outs[k] = run(eng, img, E.private_work(dd), test)
    a, b = outs['normal'][1].split('\n'), outs['hidden'][1].split('\n')
    i = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
    print('== %s %s: normal rc %d, %d lines; hidden rc %d, %d lines; first difference at line %d' % (did, test, outs['normal'][0], len(a), outs['hidden'][0], len(b), i + 1))
    print('   normal: %r' % '\n'.join(a[max(0, i - 1):i + 3])[:400])
    print('   hidden: %r' % '\n'.join(b[max(0, i - 1):i + 3])[:400])
    if did == '5f4a21fbdb': print('   hidden names:', ' '.join(hide))
