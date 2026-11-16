#!/usr/bin/env python3
"""lab/evolve/heldout-code.py DB RESULTS.md [--every K] [--ids A,B,...] - the held-out programs' code on a run's front
(Iteration 698; results/drafts/search-reopen-plan-677.md: "each processing reports them beside the selection").

The size score counts the code the selection's five programs lay (appsize.SELECTION, rec['app']); wordfreq, minif and
brainless are held out. This builds front designs (every K-th of the results file's front table by binary + image +
app, default 10, and the extremes: the fastest, the smallest, the leanest, the fastest at 32 bits) at 8-byte cells and
counts each held-out program's code bytes as appsize.py counts the selection's (and the selection's again, a check: the record's appby) (two deterministic loads: HERE's advance
less the program's own ALLOT , and C,; brainless after the lab's appbench prelude, folded, as genapps.py loads it). No
timing - bytes are exact here. Prints a row a design, then: the Spearman of the selection's code against the held-out
code over them, and the small end - the front's smallest by its score against the smallest once the held-out code is
added (the regret, in bytes). Run it as the build user in a tree whose build is done (a scratch tree while another
evolver works on master: never two on one tree).
"""
import json, os, re, shutil, statistics, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]
opt = lambda k, d: (args[args.index(k) + 1] if k in args else d)
EVERY = int(opt('--every', '10')); IDS = [x for x in opt('--ids', '').split(',') if x]
pos = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or not args[i - 1].startswith('--'))]
if len(pos) != 2: sys.exit(__doc__)
DBP, RES = pos
sys.argv = ['x']; sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'appbench'))
import evolve as E, appsize
from fold import fold

HELD = {'wordfreq': 'wordfreq.fth', 'minif': 'minif.fth', 'brainless': 'benchmark.fs'}
R = {}
for l in open(DBP, errors='replace'):
    try: r = json.loads(l)
    except ValueError: continue
    if r.get('status') == 'ok' and 'genome' in r: R[r['id']] = r
front = []
for l in open(RES, errors='replace').read().split('## How the front came about')[0].split('\n'):
    f = [x.strip() for x in l.split('|')]
    if len(f) > 10 and re.fullmatch(r'[0-9a-f]{10}', f[1] or '') and f[1] in R: front.append(f[1])
F = sorted((R[i] for i in front), key=lambda r: r['total'])
pick = IDS or [r['id'] for r in F[::EVERY]]
for e in (min(F, key=lambda r: r['speed']), F[0], min(F, key=lambda r: r.get('rss', 9e9)), min(F, key=lambda r: r.get('speed32', 9e9))):
    if not IDS and e['id'] not in pick: pick.append(e['id'])

E.setup()
T = tempfile.mkdtemp(prefix='heldout-code-'); W = os.path.join(T, 'work'); os.makedirs(W)
hexfix = lambda t: re.sub(r'(?<![\w$])\$([0-9A-F]+)\b', lambda m: str(int(m.group(1), 16)), t)   # genapps.py's
for f in ['wordfreq.fth', 'minif.fth'] + [appsize.FILES[a] for a in appsize.SELECTION]: shutil.copy(os.path.join(HERE, 'apps', f), W)
for app in appsize.SELECTION:                     # the check: the selection's code counted on the same build and path
    for m in ('size', 'count'): open(os.path.join(W, appsize.driver_name(app, m)), 'w').write(appsize.lab_text(app, m))
bl = os.path.join(HERE, 'apps', 'brainless')
for f in os.listdir(bl):
    data = open(os.path.join(bl, f), 'rb').read()
    if re.search(r'\.(fs|f|fth)$', f, re.I): data = hexfix(fold(data.decode('latin-1'))).encode('latin-1')
    open(os.path.join(W, f), 'wb').write(data)
for f in ('extend.4', 'coreext.4'): shutil.copy(os.path.join(ROOT, 'forth', f), W)
shutil.copy(os.path.join(HERE, 'appbench', 'prelude.fth'), os.path.join(W, 'lab-prelude.fth'))
for app, f in HELD.items():
    pre = 'S" lab-prelude.fth" INCLUDED\n' if app == 'brainless' else ''
    inc = ('INCLUDE %s\n' % f) if app == 'brainless' else ('S" %s" INCLUDED\n' % f)
    for m in ('size', 'count'):
        open(os.path.join(W, appsize.driver_name(app, m)), 'w').write(appsize.text(inc, m, pre))

def held(r):
    d = os.path.join(T, 'ind-' + r['id'])
    eng, img = E.build(E.canon(r['genome']), d)
    out = {}
    for app in HELD:
        o = [E.sh([eng, img], cwd=W, inp=appsize.stdin(app, m), timeout=120, cpu=30).stdout.decode('latin-1') for m in ('size', 'count')]
        v = appsize.parse(*o)
        out[app] = None if v is None else v[0] - v[1]
    sel = []
    for app in appsize.SELECTION:
        v = appsize.parse(*[E.sh([eng, img], cwd=W, inp=appsize.stdin(app, m), timeout=120, cpu=30).stdout.decode('latin-1') for m in ('size', 'count')])
        sel.append(None if v is None else v[0] - v[1])
    SAME.append(sel == r.get('appby'))
    shutil.rmtree(d, ignore_errors=True)
    return out

rows = []; SAME = []
print('| design | speed | binary + image + app | the selection\'s code | wordfreq | minif | brainless | held out |')
print('|---|---|---|---|---|---|---|---|')
for i in pick:
    r = R[i]
    try: h = held(r)
    except RuntimeError as e: print('| %s | %.3f | %s | %s | %s | | | |' % (i, r['speed'], format(r['total'], ','), format(r['app'], ','), e)); continue
    s = sum(v for v in h.values() if v is not None) if None not in h.values() else None
    rows.append((r, h, s))
    print('| %s | %.3f | %s | %s | %s | %s |' % (i, r['speed'], format(r['total'], ','), format(r['app'], ','),
          ' | '.join('-' if h[a] is None else format(h[a], ',') for a in HELD), '-' if s is None else format(s, ',')))
ok = [(r, s) for r, h, s in rows if s is not None]
def spearman(x, y):
    rk = lambda v: [sorted(v).index(a) + (sorted(v).count(a) - 1) / 2 for a in v]
    return statistics.correlation(rk(x), rk(y)) if len(x) > 2 else float('nan')
print()
print('%d designs measured, %d with every held-out reading; the selection\'s code counted again here the record\'s for %d of %d' % (
    len(rows), len(ok), sum(SAME), len(SAME)))
if ok:
    print('Spearman, the selection\'s code against the held-out code: %.3f; the score (binary + image + app) against the score '
          'with the held-out code added: %.3f' % (spearman([r['app'] for r, s in ok], [s for r, s in ok]),
                                                  spearman([r['total'] for r, s in ok], [r['total'] + s for r, s in ok])))
    a = min(ok, key=lambda x: x[0]['total']); b = min(ok, key=lambda x: x[0]['total'] + x[1])
    print('the small end: the score\'s smallest %s (%s + held out %s = %s); with the held-out code the smallest %s (%s) - '
          'the regret %+d bytes' % (a[0]['id'], format(a[0]['total'], ','), format(a[1], ','), format(a[0]['total'] + a[1], ','),
                                    b[0]['id'], format(b[0]['total'] + b[1], ','), (a[0]['total'] + a[1]) - (b[0]['total'] + b[1])))
shutil.rmtree(T, ignore_errors=True)
