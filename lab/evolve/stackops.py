#!/usr/bin/env python3
"""stackops.py ID [ID ...] [--db FILE] - a register machine priced by
counting (Iteration 29).

A register VM's gain over a stack VM is the dispatches the stack VM spends
moving values - Shi, Gregg and Beatty (VEE 2005) found a register JVM ran
46% fewer instructions for 26% more code. Here, for a design's dispatch
stream on every workload (the profiler's counts by opcode - the same on
every machine): the share that moves values and nothing else - DUP DROP
SWAP OVER ROT >R R> R@ 2DUP 2DROP, I J UNLOOP, and pairs made only of
those - and the share that pushes a literal on its own (LIT, LIT8, LIT32,
LIT64, lit0, lit1, litm1), which a register instruction would carry as an
operand. Their sum bounds what a register machine could remove from
dispatch: an upper bound - Forth words pass everything on the stack, so
the moves at every call and return remain as register moves.
"""
import collections, json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; db = os.path.join(HERE, '..', '..', 'build', 'evolve', 'db.jsonl')
if '--db' in args: i = args.index('--db'); db = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
recs = {}
for l in open(db):
    try: r = json.loads(l); recs[r['id']] = r
    except ValueError: pass
prims = [l.split()[1] for l in open(os.path.join(E.ROOT, 'forth', 'kernel.4')) if l.startswith('PRIMITIVE')]
src = open(os.path.join(E.ROOT, 'engine', 'vm-lab.c')).read()        # the specialised band, as price.py reads it
band = src[src.index('#if ENC == 3 && SPEC\n        [0x60]'):]; band = band[:band.index('#endif')]
SPECBAND = {0x60 + k: n for k, n in enumerate(re.findall(r'&&L_(\w+)', band))}
FIXED = {68: 'LIT32', 69: 'DOVAR', 70: 'DODOES', 71: 'LIT8', 72: 'LIT8X', 0x7C: 'LIT64', 0x7D: 'ESC'}   # tools/sod16.py's V8_*
MOVE = {'DUP', 'DROP', 'SWAP', 'OVER', 'ROT', '>R', 'R>', 'R@', '2dup', '2drop', 'I', 'J', 'UNLOOP'}
LIT = {'LIT', 'LIT8', 'LIT8X', 'LIT32', 'LIT64', 'lit0', 'lit1', 'litm1'}
WORKS = E.WORK_SEL + E.WORK_HELD

for did in args:
    if did not in recs: sys.exit('no design %s in %s' % (did, db))
    g = E.canon(recs[did]['genome'])
    sup = {op: '%s %s' % (a, b) for a, b, op in E.supers_in(g)}
    o10 = {op: w for w, op in E.ops10_in(g)}
    folds = g['folds'] if g.get('fold') else []
    def name(op):                          # price.py's name(), with folds and the fixed opcodes
        if op in sup: return sup[op]
        if op in o10: return o10[op]
        if op >= 128: return 'call'
        if op in FIXED: return FIXED[op]
        if 73 <= op < 73 + len(folds): return folds[op - 73] + ';EXIT'
        if g.get('escape') == 2: i = op if op < 27 else None
        elif g.get('escape'): i = op if op < 32 else op + 1 if op < 36 else None
        else: i = op if op < 68 else None
        if i is not None and i < len(prims): return prims[i]
        return SPECBAND.get(op, 'op%d' % op)
    def kind(n):
        parts = n.split(' ')
        if all(p in MOVE for p in parts): return 'move'
        if n in LIT: return 'literal'
        return 'work'
    d = os.path.join(E.EV, 'stackops'); shutil.rmtree(d, ignore_errors=True); E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False
    pw = E.private_work(d)
    print('## %s - %s bytes\n' % (did, format(recs[did]['size'], ',')))
    print('| workload | dispatches | moves only | literals alone | bound on what registers remove | the biggest movers |')
    print('|---|---|---|---|---|---|')
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
        by = collections.Counter()
        for line in open(pf):
            f = line.split()
            if f[0] in ('I', 'C'): continue
            a, b, k = int(f[0]), int(f[1]), int(f[2])
            if a == 0x7D or 128 <= b <= 255: continue       # not dispatches (Iteration 13)
            by['call' if b == 256 else name(b)] += k
        total = sum(by.values())
        mv = sum(k for n, k in by.items() if kind(n) == 'move'); lt = sum(k for n, k in by.items() if kind(n) == 'literal')
        top = sorted(((k, n) for n, k in by.items() if kind(n) == 'move'), reverse=True)[:4]
        print('| %s | %d | %.1f%% | %.1f%% | %.1f%% | %s |' % (w, total, 100 * mv / total, 100 * lt / total, 100 * (mv + lt) / total,
              ', '.join('%s %.1f%%' % (n, 100 * k / total) for k, n in top)))
    print()
    shutil.rmtree(d, ignore_errors=True)
