#!/usr/bin/env python3
"""scan.py - every single-gene change of every hand-made design, checked
for correctness only (corpus identical to the cell engine, kernel
reproduced), no timing.

Evolution can only be trusted if a design dies for what it IS. Three
times a design died for how the lab built it - a setting of the compiler
inside the image that the genome treated as free but the dump fixed
(README, phases 2b and 2c). A death here is either another such bug or a
real limit of that design, and each one should be explained.

    lab/evolve/scan.py --list                  the changes, numbered
    lab/evolve/scan.py --design NAME [--part I/N]
                                               check one design's changes
                                               (or the I-th of N slices),
                                               appending to scan.jsonl
    lab/evolve/scan.py --report                build/evolve/scan.md

Slices keep each run short, and results survive an interrupted scan.
"""
import json, os, subprocess, sys, shutil
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evolve as E

def neighbours(g):
    """(label, genome) for each single change that alters what is built."""
    out = []
    def add(label, **kw):
        n = E.canon(dict(g, **kw))
        if E.express(n) != E.express(g): out.append((label, n))
    for k in E.EXPRESSED[g['enc']] + list(E.CC0):
        v = g.get(k)
        if k == 'scale':
            for s in range(4):
                if s != v: add('scale=%d' % s, scale=s)
        elif k == 'opt':
            for o in ('O2', 'O3', 'Os'):
                if o != v: add('-' + o, opt=o)
        elif k == 'spec':
            for f in E.SPECS:
                add(('-spec ' if f in v else '+spec ') + f, spec=[x for x in v if x != f] if f in v else v + [f])
        elif k == 'folds':
            f = list(v)
            if f:
                add('-fold %s' % f[0], folds=f[1:])
                if 'LIT' in f: add('-fold LIT', folds=[x for x in f if x != 'LIT'])
                add('first %d folds' % (len(f) // 2), folds=f[:len(f) // 2])
                add('folds reversed', folds=f[::-1])
            extra = [p for p in E.POOL if p not in f]
            if extra: add('+fold %s' % extra[0], folds=f + [extra[0]])
        elif k == 'ops10':
            for w in E.OPS10_POOL:
                if w not in v: add('+op %s' % w, ops10=v + [w])
        elif k == 'supers':
            add('+pair %s %s' % tuple(E.SUPER_POOL[0]), supers=[E.SUPER_POOL[0]])
            add('+pair %s %s, run-time fusion' % tuple(E.SUPER_POOL[0]), supers=[E.SUPER_POOL[0]], rtfuse=1)
        elif isinstance(v, int) and v in (0, 1):
            add('%s=%d' % (k, 1 - v), **{k: 1 - v})
    return out

def check(g):
    d = os.path.join(E.EV, 'scan-work'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    try:
        eng, img = E.build(g, d)
        E.alive(eng, img, E.private_work(d)); status = 'ok'
    except subprocess.TimeoutExpired: status = 'died: timed out'
    except RuntimeError as e: status = str(e)
    except Exception as e: status = 'died: %s' % type(e).__name__
    shutil.rmtree(d, ignore_errors=True)
    return status

if __name__ == '__main__':
    OUT = os.path.join(E.EV, 'scan.jsonl')
    if '--report' in ARGS:
        res = {}
        for l in open(OUT): r = json.loads(l); res.setdefault(r['design'], {})[r['change']] = r['status']
        L = ['# Mutational scan', '', 'Every single-gene change of every hand-made design, checked for',
             'correctness only: corpus identical to the cell engine, kernel reproduced.', '',
             '| design | changes | alive | the changes that die |', '|---|---|---|---|']
        for name in E.HUMAN:
            r = res.get(name, {})
            dead = ['%s (%s)' % (l, s.replace('died: ', '')) for l, s in r.items() if s != 'ok']
            L.append('| %s | %d | %d | %s |' % (name, len(r), len(r) - len(dead), '; '.join(dead) or '-'))
        open(os.path.join(E.EV, 'scan.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L)); sys.exit()
    E.setup()
    if '--list' in ARGS:
        for name, g in E.HUMAN.items(): print('%-12s %d changes' % (name, len(neighbours(E.canon(g)))))
        sys.exit()
    name = ARGS[ARGS.index('--design') + 1]
    todo = neighbours(E.canon(E.HUMAN[name]))
    if '--part' in ARGS:
        i, n = map(int, ARGS[ARGS.index('--part') + 1].split('/'))
        todo = todo[(i - 1) * len(todo) // n: i * len(todo) // n]
    with open(OUT, 'a') as f:
        for label, g in todo:
            status = check(g)
            f.write(json.dumps({'design': name, 'change': label, 'status': status}) + '\n'); f.flush()
            if status != 'ok': print('  %-12s %-34s %s' % (name, label, status), flush=True)
    print('  %s: %d checked' % (name, len(todo)))
