#!/usr/bin/env python3
"""lab/evolve/design.py DESIGN [GENE=VALUE ...] [--db FILE] [--width 4] [--keep DIR] INPUT ... - one design built and
run against s6 (Iteration 567; results/drafts/automation-audit-567.md, candidate 2): the step every fault starts with,
written afresh each time until then - 566's minimal design narrowed gene by gene by hand, 567's two throwaway scripts.

DESIGN: a recorded id (results/evolve-*.md's records, or --db FILE's - a run's db.jsonl), or a hand-made stage
(s6-cv8b, s4-cv8, ...). GENE=VALUE sets a gene on it - a number, a word (opt=Os), or a list as a,b,c ([] empty).
INPUT, one or more: a workload by name - the input a run measures it on (kernel, fib, corpus, loop, bubble, ackermann,
apps, sieve, parse, far) - jit-diff (tests/jit's programs, as engines-check runs them on every JIT variant), or a file.
Each is run on the design and on s6 at the same width: right, WRONG (the first line that differs, both sides) or DIES
(the exit status, the end of stderr). First the genes set, each as expressed or not: express() decides the build (567).
--keep DIR builds in DIR and leaves it (engine, image.img, work/) to run by hand. Exit 0 when every input is right.

    python3 lab/evolve/design.py s6-cv8b tag2=1 jit=1 jitx=1 jitexec=1 alignhot=3 apps jit-diff
    python3 lab/evolve/design.py 2d4a69fc8d --db /tmp/process/<pack>/pack/db.jsonl --width 4 apps

As the build user, in a built tree (tools/build-stages.sh). gene-narrow.py asks which genes a wrong output needs.
"""
import contextlib, json, os, shutil, sys

a = sys.argv[1:]
def opt(k):
    if k not in a: return None
    i = a.index(k); v = a[i + 1] if i + 1 < len(a) else sys.exit(__doc__); del a[i:i + 2]; return v
db, width, keep = opt('--db'), int(opt('--width') or 8), opt('--keep')
if len(a) < 2 or a[0] in ('-h', '--help'): sys.exit(__doc__)
name, sets = a[0], dict(x.split('=', 1) for x in a[1:] if '=' in x and not os.path.exists(x))
inputs = [x for x in a[1:] if not ('=' in x and not os.path.exists(x))]
if not inputs: sys.exit('design: no INPUT - a workload, jit-diff or a file')
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E

if name in E.HUMAN: g0 = dict(E.HUMAN[name])
elif db:
    g0 = next((json.loads(l)['genome'] for l in open(db) if l.startswith('{') and '"%s"' % name in l
               and json.loads(l).get('id') == name), None)
else: g0 = E.recorded_genome(name)
if g0 is None: sys.exit('design: %s - no hand-made stage of that name, and no record of it%s' % (name, ' in ' + db if db else ' in results/'))
LISTS = ('spec', 'folds', 'supers', 'ops10', 'opcall')
def val(k, v):
    if k in LISTS: return [] if v in ('', '[]') else v.split(',')
    return int(v) if v.lstrip('-').isdigit() else v
g = E.canon(dict(g0, **{k: val(k, v) for k, v in sets.items()}))
ex = E.express(g)
print('design %s%s -> %s, %d-byte cells%s' % (name, ''.join(' %s=%s' % kv for kv in sets.items()), E.gid(g), width,
      ''.join('\n  %s=%s %s' % (k, sets[k], 'expressed' if ex.get(k) not in (None, 0, [], '') else 'NOT expressed - builds nothing')
              for k in sets)))

E.setup()
if width == 4: E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
def feed(x):
    if x == 'jit-diff': return E.jit_diff_in()
    if os.path.exists(x): return open(x, 'rb').read()
    return E.program(x)
def run(eng, img, pw, inp):
    try: r = E.sh([eng, img], inp=inp, cwd=pw, timeout=300, cpu=120)
    except Exception as x: return None, [], 'timeout (%s)' % str(x)[:60]
    return r.returncode, r.stdout.decode('latin-1').replace('\r', '').split('\n'), r.stderr.decode('latin-1').strip()[-160:]
d = keep or os.path.join(E.EV, 'design-%d' % os.getpid()); dr = os.path.join(E.EV, 'design-ref-%d' % os.getpid())
bad = 0
with (E.at_width(E.WIDTH4) if width == 4 else contextlib.nullcontext()):
    try:
        shutil.rmtree(d, ignore_errors=True); eng, img = E.build(g, d); pw = E.private_work(d)
    except Exception as x: sys.exit('design: the build DIED - %s' % str(x)[:200])
    if width == 4:
        shutil.rmtree(dr, ignore_errors=True); re_, ri = E.build(E.canon(dict(E.HUMAN['s6-cv8b'])), dr)
    else: re_, ri = E.REF[0], E.REF[1]
    rw = E.private_work(dr)
    for x in inputs:
        try: inp = feed(x)
        except Exception as e: print('  %-12s no such input (%s)' % (x, str(e)[:60])); bad += 1; continue
        (c0, o0, _), (c1, o1, e1) = run(re_, ri, rw, inp), run(eng, img, pw, inp)
        if c1 == c0 and o1 == o0: print('  %-12s right' % x); continue
        bad += 1
        if c1 != c0: print('  %-12s DIES - exit %s (s6 %s)%s' % (x, c1, c0, ': ' + e1 if e1 else ''))
        else:
            i = next(k for k in range(max(len(o0), len(o1))) if (o0[k:k + 1] or ['']) != (o1[k:k + 1] or ['']))
            print('  %-12s WRONG - line %d: s6 %r, this %r' % (x, i + 1, (o0[i:i + 1] or [''])[0][:70], (o1[i:i + 1] or [''])[0][:70]))
if keep: print('design: kept in %s - %s %s, run in %s' % (d, eng, img, pw))
else: shutil.rmtree(d, ignore_errors=True)
shutil.rmtree(dr, ignore_errors=True)
sys.exit(1 if bad else 0)
