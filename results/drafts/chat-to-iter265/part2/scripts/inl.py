import os, sys, shutil, json, glob, re, collections
ROOT = '/home/claude/forth-vm-evolution'
sys.argv = ['x']; sys.path.insert(0, ROOT + '/lab/evolve'); import evolve as E
E.setup()
srcs = (glob.glob(ROOT + '/tests/ans/*') + glob.glob(ROOT + '/tests/core/*') + glob.glob(ROOT + '/bench/*.fth') + glob.glob(ROOT + '/tests/shell/*')
        + [E.CORPUS] + [ROOT + '/forth/' + f for f in ('extend.4', 'cross.4', 'kernel.4')])
toks = set()
for p in srcs:
    if os.path.isfile(p): toks |= {t.upper() for t in re.findall(r'\S+', open(p, errors='replace').read())}
CONST = {'#FOLD-OPS', '0BRANCH-OP', '?BRANCH8-OP', 'BRANCH-OP', 'BRANCH8-OP', 'DODOES-OP', 'DOVAR-OP', 'ESC-OP', 'EXIT-OP', 'FOLD-BASE',
         'LIT16-OP', 'LIT32-OP', 'LIT64-OP', 'LIT8-OP'}
for did in ('add5ec8937', 'cc6d168e0a'):
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 'inl'); shutil.rmtree(d, ignore_errors=True)
    cm, sm = d + '.map', d + '.sym'; os.environ['CALLMAP'] = cm; os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
    try: E.build(g, d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']; del os.environ['SYMMAP']
    words, sites = {}, collections.defaultdict(list)
    for l in open(cm):
        f = l.split()
        if f[0] == 'W': words[' '.join(f[4:])] = (int(f[1]), int(f[2]), f[3])
        elif f[0] == 'C': sites[int(f[3])].append(int(f[2]))
    named = [n for n in (l.split(None, 2)[2].strip() for l in open(sm)) if n]
    hide = sorted({n for n in named if n.upper() not in toks})
    rows, tot = [], collections.Counter()
    for n in hide:
        if n not in words: continue
        a, b, kind = words[n]; s = sites.get(a, [])
        body = b - a
        if n in CONST: save = body + sum(max(0, x - 2) for x in s); how = 'constant -> literals'
        elif len(s) == 1 and kind == 'code': save = s[0] + 1; how = 'one call site: inline'
        elif not s: save = body; how = 'no call site: dead'
        else: save = 0; how = '%d call sites: keep' % len(s)
        tot[how.split(':')[0] if ':' in how else how] += save; tot['words ' + how.split(':')[0]] += 1
        rows.append('%s(%s %dB %d sites)' % (n, kind[0], body, len(s)))
    print('%s: %d hidden names with bodies; saving beyond hiding: %s' % (did, len(rows), dict(tot)))
    print('  ' + ' '.join(rows))
