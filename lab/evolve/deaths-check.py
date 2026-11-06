#!/usr/bin/env python3
"""lab/evolve/deaths-check.py DB [--all] [--max N] - a returned seed's deaths and wrong outputs, rebuilt on this tree
(Iteration 560). Every record of DB (a seed pack's db.jsonl) whose status is "died: W" or "wrong output: W" is built here
and run on W; its output against s6's. The expected causes are listed, not rebuilt: "not run" (reach_lethal screens a
reach the design cannot have - Iteration 556), the same reach at scale 1 on the kernel workload (2^15 bytes: reach_lethal
runs these, most lived in seed 2 - Iteration 10; seed 78's three died, 564), and cpt16 wrong on apps (it stops early on the applications' undefined
words - Iteration 516); --all rebuilds those too. A death by a retired value (build()'s refusal since the consolidation of
599: "died: varcall 0 - retired (Iteration 592); ...") is made again here, not waived - build() refuses it before it
compiles anything - and is expected when the refusal here is the run's, word for word; else open (Iteration 615; seed 88's
two carried designs, open at 614). --self-test: the refusal's three cases, nothing compiled. A design that computes right here is a fault this tree has fixed (seed
77's corpus death, a JIT value hole - Iteration 557); one that still differs or dies is an open correctness issue, and
GOALS.md's stop needs none: exit 1. As the build user, in a built tree, alone (it is an evolver process: process-checks.sh
runs it after ans-check, before the jail).
"""
import json, os, re, shutil, sys
a = sys.argv[1:]
RETIRED = re.compile(r'died: \w+ \S+ - retired \(Iteration \d+\)')     # 615: build()'s refusal of a value retired at 599
if a[:1] == ['--self-test']: a = ['--self-test']
elif not a or a[0].startswith('-'):
    print(__doc__.strip()); sys.exit(2)
DB, ALL = a[0], '--all' in a
MAX = int(a[a.index('--max') + 1]) if '--max' in a else 40
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E

def expected(r, w):
    if 'not run' in r['status']: return 'reach limit, not run (556)'
    if w == 'apps' and r['genome'].get('enc') == 'cpt16': return 'cpt16 on apps (516)'
    g = r['genome']                                     # 564: reach_lethal's scale 1 - run, jailed (Iteration 10)
    if w == 'kernel' and g.get('enc') == 'cv8' and g.get('scale') == 1 and not (g.get('varcall') and g.get('doesfar')):
        return 'the reach limit at scale 1, run and jailed (10; back with doesfar lifted, 556)'
    # 576: seed 85's random genomes reach it at scale 2 too - 69 kernel deaths, every one bytehdr=0, lean=0, threads=2 without
    # both far forms; 83 of 83 such designs with both lived (results/evolve-amd-ryzen-7-pro-8840hs-seed85.md)
    if w == 'kernel' and g.get('enc') == 'cv8' and g.get('scale') == 2 and not (g.get('varcall') and g.get('doesfar')) \
            and not g.get('bytehdr') and not g.get('lean'):
        return 'the reach limit at scale 2, large dictionaries (576)'
    # 576: the converter's size check at the scale-0 call reach (results/drafts/body-size-drift-576.md) - dies before any run
    if 'body size drift' in r['status'] and g.get('scale') == 0: return 'the scale-0 call reach, the converter refuses (576)'
    return None

def refused(r):
    """615: a death by a retired value made again here - build() refuses before compiling (evolve.py's _build); the same
    words as the run's, or the death is open"""
    d = os.path.join(E.EV, 'deaths-check'); shutil.rmtree(d, ignore_errors=True)
    try:
        E.build(E.canon(r['genome']), d); return False
    except Exception as x:
        return str(x) == r['status']
    finally:
        shutil.rmtree(d, ignore_errors=True)

if a == ['--self-test']:             # 615: the three cases, from a living cv8 genome - each refused before compiling
    E.setup()
    g = next(json.loads(l)['genome'] for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'results',
             'followup-seed88.md')) if l.startswith('{'))
    v0 = 'died: varcall 0 - retired (Iteration 592); s4 is frozen (stages/frozen)'
    cases = [('refused the same - expected', dict(id='t1', status=v0, genome=dict(g, varcall=0)), True, True),
             ('refused in other words - open', dict(id='t2', status=v0, genome=dict(g, doesfar=0)), True, False),
             ('a death of another kind - rebuilt, not this rule', dict(id='t3', status='died: kernel', genome=g), False, None)]
    ok = 0
    for name, r, m, want in cases:
        got = bool(RETIRED.match(r['status'])), (refused(r) if RETIRED.match(r['status']) else None)
        ok += got == (m, want); print('  %-48s %s' % (name, 'ok' if got == (m, want) else 'WRONG %s' % (got,)))
    print('deaths-check self-test: %s - %d of %d' % ('PASS' if ok == len(cases) else 'FAIL', ok, len(cases)))
    sys.exit(0 if ok == len(cases) else 1)

def sign(g):            # the genes of the known faults, for reading the table
    s = [k for k in ('jit', 'tracer', 'nocrossjump') if g.get(k)]
    return '+'.join(s) + (' (the 557 hole pair)' if len(s) == 3 else '') if s else '-'

todo, skip, ret = [], {}, []
for l in open(DB):
    r = json.loads(l); m = re.match(r'(died|wrong output): (\w+)', r.get('status', ''))
    if not m: continue
    if not ALL and RETIRED.match(r['status']): ret.append(r); continue        # 615: made again below, not rebuilt
    e = None if ALL else expected(r, m.group(2))
    if e: skip[e] = skip.get(e, 0) + 1
    else: todo.append((r, m.group(2)))
print('deaths-check: %s - %d to rebuild%s%s' % (DB, len(todo), ''.join('; expected, not rebuilt: %s %d' % kv for kv in skip.items()),
      '; a retired value, its refusal made again here: %d' % len(ret) if ret else ''))
if len(todo) > MAX: print('deaths-check: only the first %d (--max)' % MAX); todo = todo[:MAX]
E.setup(); ref, bad = {}, 0
same = [r for r in ret if refused(r)]; diff = [r for r in ret if r not in same]
print('| design | gen | in the run | genes | here |\n|---|---|---|---|---|')
for r in diff: print('| %s | %s | %s | %s | NOT refused the same here - open |' % (r['id'], r.get('gen'), r['status'], sign(r['genome'])))
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
print('deaths-check: %d of %d rebuilt compute right here; %d open%s' % (len(todo) - bad, len(todo), bad + len(diff),
      '; %d refused here the same - retired values (599)' % len(same) if same else ''))
sys.exit(1 if bad or diff else 0)
