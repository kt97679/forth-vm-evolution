#!/usr/bin/env python3
"""hidden-names.py ID [ID ...] - the dictionary names no program here writes,
made headerless with the converter's existing switch (tools/layout.py
--headerless), image bytes measured and the gate run (Iteration 222).

"Programs here": the standard suite and the core tests, the benchmarks, the
corpus, the shell tests and the sources compiled at run time (extend.4,
cross.4, kernel.4). A name none of them writes is never looked up by them.
A pricing tool, not a gene: a gene would hide lists kept by hand per overlay
(as FSYS_INTERNAL and RTLOOP_INTERNAL are), not a list derived from tests."""
import os, sys, shutil, json, glob, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
ids = sys.argv[1:] or ['add5ec8937']
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
E.setup()
srcs = (glob.glob(os.path.join(ROOT, 'tests', 'ans', '*')) + glob.glob(os.path.join(ROOT, 'tests', 'core', '*')) +
        glob.glob(os.path.join(ROOT, 'bench', '*.fth')) + glob.glob(os.path.join(ROOT, 'tests', 'shell', '*')) +
        [E.CORPUS] + [os.path.join(ROOT, 'forth', f) for f in ('extend.4', 'cross.4', 'kernel.4')])
toks = set()
for p in srcs:
    if os.path.isfile(p): toks |= {t.upper() for t in re.findall(r'\S+', open(p, errors='replace').read())}
for did in ids:
    g = E.canon(E.recorded_genome(did))
    d = os.path.join(E.EV, 'hide'); shutil.rmtree(d, ignore_errors=True); sm = d + '.sym'
    os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
    try: E.build(g, d)
    finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
    named = [n for n in (l.split(None, 2)[2].strip() for l in open(sm)) if n]
    hide = sorted({n for n in named if n.upper() not in toks})
    eng0, img0 = E.build(g, d); s0 = os.path.getsize(img0)
    saved = E.FSYS_INTERNAL
    if E.fsys_on(g): E.FSYS_INTERNAL = tuple(E.FSYS_INTERNAL) + tuple(hide)
    else: E.CONVERT_EXTRA[:] = ['--headerless', ','.join(hide)]
    try:
        eng1, img1 = E.build(g, d); s1 = os.path.getsize(img1)
        try: E.alive(eng1, img1, E.private_work(d)); ok = 'alive'
        except Exception as e: ok = 'DIED: %s' % e
    finally: E.FSYS_INTERNAL = saved; E.CONVERT_EXTRA[:] = []
    print('%s: %d of %d names no program here writes; image %d -> %d (-%d); %s' % (did, len(hide), len(named), s0, s1, s0 - s1, ok))
    print('  ' + ' '.join(hide))
    shutil.rmtree(d, ignore_errors=True)
