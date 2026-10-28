#!/usr/bin/env python3
"""lab/evolve/deaths-check.py DB [--all] [--max N] - a returned seed's deaths and wrong outputs, rebuilt on this tree
(Iteration 560). Every record of DB (a seed pack's db.jsonl) whose status is "died: W" or "wrong output: W" is built here
and run on W; its output against s6's. The expected causes are listed, not rebuilt: "not run" (reach_lethal screens a
reach the design cannot have - Iteration 556) and cpt16 wrong on apps (it stops early on the applications' undefined
words - Iteration 516); --all rebuilds those too. A design that computes right here is a fault this tree has fixed (seed
77's corpus death, a JIT value hole - Iteration 557); one that still differs or dies is an open correctness issue, and
GOALS.md's stop needs none: exit 1. As the build user, in a built tree, alone (it is an evolver process: process-checks.sh
runs it after ans-check, before the jail).
"""
import json, os, re, shutil, sys
a = sys.argv[1:]
if not a or a[0].startswith('-'):
    print(__doc__.strip()); sys.exit(2)
DB, ALL = a[0], '--all' in a
MAX = int(a[a.index('--max') + 1]) if '--max' in a else 40
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E

def expected(r, w):
    if 'not run' in r['status']: return 'reach limit, not run (556)'
    if w == 'apps' and r['genome'].get('enc') == 'cpt16': return 'cpt16 on apps (516)'
    return None

def sign(g):            # the genes of the known faults, for reading the table
    s = [k for k in ('jit', 'tracer', 'nocrossjump') if g.get(k)]
    return '+'.join(s) + (' (the 557 hole pair)' if len(s) == 3 else '') if s else '-'

todo, skip = [], {}
for l in open(DB):
    r = json.loads(l); m = re.match(r'(died|wrong output): (\w+)', r.get('status', ''))
    if not m: continue
    e = None if ALL else expected(r, m.group(2))
    if e: skip[e] = skip.get(e, 0) + 1
    else: todo.append((r, m.group(2)))
print('deaths-check: %s - %d to rebuild%s' % (DB, len(todo), ''.join('; expected, not rebuilt: %s %d' % kv for kv in skip.items())))
if len(todo) > MAX: print('deaths-check: only the first %d (--max)' % MAX); todo = todo[:MAX]
E.setup(); ref, bad = {}, 0
print('| design | gen | in the run | genes | here |\n|---|---|---|---|---|')
for r, w in todo:
    if w not in ref: E.run_metric(*E.REF, w); ref[w] = E.OUT_LAST[0]
    d = os.path.join(E.EV, 'deaths-check'); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(E.canon(r['genome']), d)
        E.run_metric(eng, img, E.private_work(d), w)
        here = 'right - as s6' if E.OUT_LAST[0] == ref[w] else 'DIFFERS from s6'
    except Exception as x:
        here = 'DIES here: %s' % str(x)[:80]
    shutil.rmtree(d, ignore_errors=True)
    bad += not here.startswith('right')
    print('| %s | %s | %s | %s | %s |' % (r['id'], r.get('gen'), r['status'], sign(r['genome']), here))
print('deaths-check: %d of %d rebuilt compute right here; %d open' % (len(todo) - bad, len(todo), bad))
sys.exit(1 if bad else 0)
