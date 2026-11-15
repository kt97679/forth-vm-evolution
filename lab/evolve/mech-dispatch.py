#!/usr/bin/env python3
"""lab/evolve/mech-dispatch.py [--design NAME] [--apps A,B] - the dispatches relf's mechanisms would take out of genapps.py's
programs, on an interpreted design, attributed by the profiler (Iteration 684: step 2 of
results/drafts/search-reopen-plan-677.md; lab/evolve/mech-price.py is the bytes).

The design's profiling engine (build/genapps/prof/NAME-prof, genapps-dispatch.py makes it) runs each benchmark - its
full run less its load, per address (VMPROF's I lines) - and a third run, the load and then `' X START @ - .` for every
word mech-census.py found the program referring to, places each word: its executions are the count at its first byte.
Per execution: a constant compiled as its value saves its body's dispatches (the call stays as the literal); a
variable's fetch or store as one operation saves 2 (the call and DOVAR) on the share of its references followed by @
or ! (static, per variable); an inlined small word saves 2 (the call and its EXIT); a VALUE's fetch, 1 - 680's CELL+.
A name the program never defined (a census reading of a string or a comment) is found by FIND as -1 and left out. Against the benchmark's dispatches."""
import json, os, re, subprocess, sys
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
a = sys.argv[1:]; D = a[a.index('--design') + 1] if '--design' in a else 'portable-knee'
APPS = (a[a.index('--apps') + 1] if '--apps' in a else 'sim16,gc16,scan,evo,wordfreq,minif,brainless').split(',')
W = os.path.join(ROOT, 'build', 'genapps', 'work-8'); P = os.path.join(ROOT, 'build', 'genapps', 'prof')
ENG, IMG = os.path.join(P, D + '-prof'), os.path.join(ROOT, 'designs', D, 'image.img')
if not os.path.exists(ENG): sys.exit('mech-dispatch: no %s (lab/evolve/genapps-dispatch.py --designs %s)' % (ENG, D))
C = json.load(open(os.path.join(ROOT, 'build', 'genapps', 'mech-census.json')))
def prof(name):
    f = os.path.join(P, 'mech-vmprof.txt')
    if os.path.exists(f): os.remove(f)
    subprocess.run([ENG, IMG], cwd=W, input=('S" %s" INCLUDED\n' % name).encode(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   env=dict(os.environ, VMPROF=f), timeout=600)
    out = {}
    for l in open(f):
        p = l.split()
        if p and p[0] == 'I': out[int(p[1])] = out.get(int(p[1]), 0) + int(p[2])
    return out
R = {}
for app in APPS:
    full, load = prof('lab-%s-full.fs' % app), prof('lab-%s-load.fs' % app)
    run = {k: v - load.get(k, 0) for k, v in full.items() if v - load.get(k, 0) > 0}
    tot = sum(run.values()); names = C[app]['names']
    pre = open(os.path.join(W, 'lab-%s-load.fs' % app)).read().replace('BYE\n', '')
    drv = os.path.join(W, 'mech-%s-where.fs' % app)
    open(drv, 'w').write(pre + 'CREATE WBUF-684 64 ALLOT  : WHERE-684 ( c-addr u --- )  DUP WBUF-684 C! WBUF-684 1+ SWAP CMOVE WBUF-684 FIND IF START @ - ELSE DROP -1 THEN . ;\n'
                         + ''.join('777001 . S" %s" WHERE-684 777002 .\n' % n for n in names) + 'BYE\n')   # FIND: an unknown name -1
    o = subprocess.run([ENG, IMG], cwd=W, input=('S" %s" INCLUDED\n' % os.path.basename(drv)).encode(), capture_output=True, timeout=600).stdout.decode('latin-1')
    offs = [int(x) for x in re.findall(r'777001 (-?\d+) +777002', o)]
    if len(offs) != len(names): sys.exit('mech-dispatch: %s - %d of %d words placed' % (app, len(offs), len(names)))
    starts = sorted(set(x for x in offs if x >= 0)); print('mech-dispatch: %s - %d of %d words placed' % (app, len(starts), len(names)), flush=True)
    s = dict.fromkeys(('1 constants', '2 data word @ !', '4 small4 inlined', '4 small8 inlined', 'VALUE kind cell (680)'), 0)
    for (n, (kind, refs, pairs)), x in zip(names.items(), offs):
        e = run.get(x, 0) if x >= 0 else 0
        if not e: continue
        if kind == 'const':
            nxt = min([y for y in starts if y > x] or [x + 16]); s['1 constants'] += sum(run.get(y, 0) for y in range(x, min(nxt, x + 16)))
        elif kind == 'var': s['2 data word @ !'] += 2 * e * (pairs / refs if refs else 0)
        elif kind == 'small4': s['4 small4 inlined'] += 2 * e; s['4 small8 inlined'] += 2 * e
        elif kind == 'small8': s['4 small8 inlined'] += 2 * e
        elif kind == 'value': s['VALUE kind cell (680)'] += e       # 680's CELL+ a fetch, gone
    R[app] = dict(dispatches=tot, saved={k: v / tot for k, v in s.items()})
    print('mech-dispatch: %-10s %s dispatches; saved %s' % (app, format(tot, ','), ', '.join('%s %.1f %%' % (k, 100 * v / tot) for k, v in s.items())), flush=True)
json.dump(R, open(os.path.join(ROOT, 'build', 'genapps', 'mech-dispatch-%s.json' % D), 'w'), indent=1)
