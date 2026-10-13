import os, sys, glob, re, shutil, subprocess
ROOT = '/home/claude/forth-vm-evolution'
sys.argv = ['x']; sys.path.insert(0, ROOT + '/lab/evolve'); import evolve as E
E.setup()
def scan(files):
    t = set()
    for p in files:
        if os.path.isfile(p): t |= {x.upper() for x in re.findall(r'\S+', open(p, errors='replace').read())}
    return t
base = (glob.glob(ROOT + '/tests/ans/*') + glob.glob(ROOT + '/tests/core/*') + glob.glob(ROOT + '/bench/*.fth') + glob.glob(ROOT + '/tests/shell/*')
        + [E.CORPUS] + [ROOT + '/forth/' + f for f in ('extend.4', 'cross.4', 'kernel.4')])
runtime = [ROOT + '/forth/' + f for f in ('coreext.4', 'locals.4', 'save-system.4', 'shell.4', 'shell-sysc.4')]
T0, T1 = scan(base), scan(base + runtime)
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
    if test == 'prelimtest.fth': inp = 'S" prelimtest.fth" INCLUDED\nBYE\n'
    else: inp = ('S" prelude.fth" INCLUDED\nS" extend.4" INCLUDED\nS" coreext.4" INCLUDED\nS" tester.fr" INCLUDED\nS" core.fr" INCLUDED\n\n'
                 'S" utilities.fth" INCLUDED\nS" errorreport.fth" INCLUDED\nS" %s" INCLUDED\nBYE\n' % test)
    r = subprocess.run([eng, img], cwd=pw, input=inp.encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    return r.returncode, r.stdout.decode(errors='replace')
def names(g, d):
    sm = d + '.sym'; os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
    try: E.build(g, d)
    finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
    return [n for n in (l.split(None, 2)[2].strip() for l in open(sm)) if n]
# 1. the tools test with the old and the wider scan
g = E.canon(E.recorded_genome('add5ec8937')); d = os.path.join(E.EV, 'dg'); nm = names(g, d)
old = sorted({n for n in nm if n.upper() not in T0}); new = sorted({n for n in nm if n.upper() not in T1})
print('add5ec8937: hidden %d by the first scan, %d with coreext/locals/save-system/shell; written there: %s' % (len(old), len(new), ' '.join(sorted(set(old) - set(new)))))
res = {}
for k, h in (('normal', []), ('old', old), ('new', new)):
    eng, img = build(g, d + k, h); res[k] = run(eng, img, E.private_work(d + k), 'toolstest.fth')
for k in ('old', 'new'):
    a, b = res['normal'][1].split('\n'), res[k][1].split('\n')
    i = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), None)
    print('  toolstest %s hiding: %s' % (k, 'same as normal' if i is None and len(a) == len(b) else 'differs at line %d: normal %r / hidden %r' % ((i or 0) + 1, a[i or 0][:150], b[i or 0][:150])))
# 2. the crash: bisect 5f4a21fbdb's list on prelimtest
g = E.canon(E.recorded_genome('5f4a21fbdb')); d = os.path.join(E.EV, 'dg2'); nm = names(g, d)
lst = sorted({n for n in nm if n.upper() not in T0})
def crashes(h):
    eng, img = build(g, d + 'b', h); rc, out = run(eng, img, E.private_work(d + 'b'), 'prelimtest.fth'); return rc != 0
print('5f4a21fbdb: crashes with all %d hidden: %s' % (len(lst), crashes(lst)))
cur = lst
while len(cur) > 1:
    half = cur[:len(cur) // 2]
    cur = half if crashes(half) else cur[len(cur) // 2:]
print('  the culprit, alone: %s - crashes alone: %s' % (cur, crashes(cur)))
