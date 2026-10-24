#!/usr/bin/env python3
"""appbench.py DB [DB ...] --zip PATH [--sample N] [--rounds R] [--apps fcp,brainless,cd16sim] - applications held out

Iteration 468 (the owner: run more applications); Iteration 469: and our own, written from scratch - sim16
(lab/evolve/apps/), a CPU simulated in Forth; Iteration 470: gc16 (a collector), scan (a scanner
generator), evo (a genetic algorithm) - ours too, needing no zip. The newest database's front - N designs across it, fastest to
slowest - each built and run on Appbench's applications (Ertl and Paysan; the owner's appbench.zip, kept outside this
repository, read where it lies), against s6 the same way, R rounds alternating; each design's output checked as the
application's own result (fcp's nodes, brainless's nodes and evaluations, cd16sim's "should be" line). The
applications' source is folded to upper case (appbench/fold.py - our lookup is case-sensitive, theirs were written for
Forths that fold case) and loaded after our own extend.4 and coreext.4 and a few stubs (appbench/prelude.fth); the
time is the child's CPU time, the whole run - the prelude's load in it, a constant against s6's. Per design: each
application's time over s6's, their geometric mean; then Spearman between the in-run speed and that mean - do the
applications rank the front as the selection's workloads did (results/drafts/appbench-466.md, -467.md).
"""
import argparse, json, math, os, re, resource, shutil, statistics, sys, tempfile, zipfile
ap = argparse.ArgumentParser(usage=__doc__.split('\n')[0])
ap.add_argument('dbs', nargs='+'); ap.add_argument('--zip', default=''); ap.add_argument('--sample', type=int, default=16)
ap.add_argument('--rounds', type=int, default=2); ap.add_argument('--apps', default='sim16,gc16,scan,evo,wordfreq,minif,fcp,brainless,cd16sim')
ap.add_argument('--ids', default=''); ap.add_argument('--set', action='append', default=[])   # Iteration 473: named designs, genes set
a = ap.parse_args()
SET = {k: int(v) for k, v in (x.split('=', 1) for x in a.set)}
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, 'appbench')); from fold import fold
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
CALLS = {'fcp': 'include fcp-1.31-64.f||!: setup SETUP ;||bench bye', 'brainless': 'include benchmark.fs benchmark bye',
         'cd16sim': ': 3drop 2drop drop ; include bench.f 1000000 benchmark bye',
         'lexex': 'include run.fth bye', 'benchgc': '64000 include bench-gc5.fs bye'}
OWN = {'sim16': ('sim16.fth', '60 BENCH BYE'), 'gc16': ('gc16.fth', '50000 BENCH BYE'),     # Iterations 469-470: ours,
       'scan': ('scan.fth', '600 BENCH BYE'), 'evo': ('evo.fth', '3000 BENCH BYE'),          # from scratch (lab/evolve/apps/)
       'wordfreq': ('wordfreq.fth', '140 BENCH BYE'), 'minif': ('minif.fth', '6000 BENCH BYE')}   # Iteration 500: held out only
CHECKS = {'wordfreq': r'WORDFREQ WORDS 20000 DISTINCT 1591 TOP 1163 CHECK 26703\b', 'minif': r'MINIF CHECK 21282 ERRS 6000 DEFS 14\b',
          'sim16': r'SIM16 SIEVE 303 FIB 6765 STEPS 21936820\b', 'gc16': r'GC16 GCS 618 FREED 7454729 CHECK 2636\b',
          'scan': r'SCAN NFA 44 DFA 17 IDENT 1723 NUMBER 908 SPACE 5407 ERRS 0 CHECK 20235\b', 'evo': r'EVO BEST 445 AT 200 CHECK 24466\b',
           'fcp': r'(?s)\b120287\b.*Results:', 'brainless': r'110023 nodes .* 163278 evals', 'cd16sim': r'(\d+ \d+ \d+ \d+) should be \1\b'}
apps = a.apps.split(',')
def hexfix(t): return re.sub(r'(?<![\w$])\$([0-9A-F]+)\b', lambda m: str(int(m.group(1), 16)), t)
work = tempfile.mkdtemp(prefix='appbench-'); text = {}
for prog in [p for p in apps if p in OWN]:
    d = os.path.join(work, prog); os.makedirs(d)
    f, call = OWN[prog]; text[prog] = open(os.path.join(HERE, 'apps', f), 'rb').read() + b'\n' + call.encode() + b'\n'
zapps = [p for p in apps if p not in OWN]
LOCAL = {'brainless': os.path.join(HERE, 'apps', 'brainless')}   # Iteration 492: public domain - copied in, no zip needed
need_zip = [p for p in zapps if p not in LOCAL]
if need_zip and not a.zip: sys.exit('appbench.py: --zip PATH (Appbench) for ' + ', '.join(need_zip))
z = zipfile.ZipFile(os.path.expanduser(a.zip)) if need_zip else None
for prog in zapps:
    d = os.path.join(work, prog)
    if prog in LOCAL:
        entries = [(os.path.relpath(os.path.join(r_, f_), LOCAL[prog]), open(os.path.join(r_, f_), 'rb').read())
                   for r_, _, fs_ in os.walk(LOCAL[prog]) for f_ in fs_]
    else:
        entries = []
        for n in z.namelist():
            m = re.match(r'[^/]+/%s/(.+)' % re.escape(prog), n)
            if not m or '/CVS/' in '/' + m.group(1) or n.endswith('/'): continue
            entries.append((m.group(1), z.read(n)))
    for rel, data in entries:
        out = os.path.join(d, rel); os.makedirs(os.path.dirname(out), exist_ok=True)
        if re.search(r'\.(fs|f|fth|fb|4th|vhd)$', rel, re.I): data = hexfix(fold(data.decode('latin-1'))).encode('latin-1')
        open(out, 'wb').write(data)
    for f in ('extend.4', 'coreext.4'): shutil.copy(os.path.join(ROOT, 'forth', f), d)
    text[prog] = (open(os.path.join(HERE, 'appbench', 'prelude.fth')).read() + '\n' + ' '.join(
        s[1:] if s.startswith('!') else hexfix(fold(s)) for s in CALLS[prog].split('||')) + '\n').encode('latin-1')
def run(eng, img, prog):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = E.sh(list(E.PIN) + [eng, img], cwd=os.path.join(work, prog), inp=text[prog], timeout=900, cpu=600)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), p.stdout.decode('latin-1').replace('\r', '')
db = max(a.dbs, key=os.path.getmtime); R = {}
for l in open(db):
    try: r = json.loads(l); R[r['id']] = r
    except (ValueError, KeyError, TypeError): pass
rmf = os.path.join(os.path.dirname(db), 'remeasure.json')
if os.path.basename(db) == 'db.jsonl' and os.path.exists(rmf):
    rm = json.load(open(rmf)); sp = {i: (rm[i]['speed'] if isinstance(rm[i], dict) else rm[i]) for i in rm if i in R}; how = 're-measured front'
else:
    ids = E.fronts([i for i, r in R.items() if r.get('status') == 'ok'], R)[0]; sp = {i: R[i]['speed'] for i in ids}; how = 'selection front'
order = sorted(sp, key=sp.get); k = min(a.sample, len(order))
pick = [order[round(j * (len(order) - 1) / max(1, k - 1))] for j in range(k)] if k > 1 else order[:1]
pick = list(dict.fromkeys(pick))
if a.ids: pick = [i for i in a.ids.split(',') if i in R]
print('# Applications held out (lab/evolve/appbench.py, Iteration 468)\n')
print('Front: %s, %s (%d designs); %d sampled fastest to slowest; %s; %d rounds, CPU time, against s6.\n' % (db, how, len(order), len(pick), ', '.join(apps), a.rounds))
print('| design | in-run speed | %s | geometric mean |\n|---|---|%s---|' % (' | '.join(apps), '---|' * len(apps)), flush=True)
reng, rimg = E.REF[0], E.REF[1]; xs, ys, fails = [], [], []
for i in pick:
    d = os.path.join(E.EV, 'appbench-d'); shutil.rmtree(d, ignore_errors=True)
    try: eng, img = E.build(E.canon(dict(E.canon(R[i]['genome']), **SET)), d)
    except Exception as x: print('| %s | %.3f | %s | build failed |' % (i, sp[i], ' | '.join('-' for _ in apps)), flush=True); fails.append(i); continue
    ratios, cells = [], []
    for prog in apps:
        td, ts, ok = [], [], True
        for _ in range(a.rounds):
            try:
                t, out = run(eng, img, prog); td.append(t)
                if prog in CHECKS and not re.search(CHECKS[prog], out): ok = False
            except Exception: ok = False; break
            t, _ = run(reng, rimg, prog); ts.append(t)
        if ok and td and ts: q = statistics.median(td) / statistics.median(ts); ratios.append(q); cells.append('%.3f' % q)
        else: cells.append('**wrong**'); fails.append('%s %s' % (i, prog))
    g = math.exp(sum(math.log(q) for q in ratios) / len(ratios)) if len(ratios) == len(apps) else None
    if g: xs.append(sp[i]); ys.append(g)
    print('| %s | %.3f | %s | %s |' % (i, sp[i], ' | '.join(cells), '%.3f' % g if g else '-'), flush=True)
shutil.rmtree(os.path.join(E.EV, 'appbench-d'), ignore_errors=True); shutil.rmtree(work, ignore_errors=True)
def ranks(v): s = sorted(range(len(v)), key=lambda j: v[j]); r = [0] * len(v); [r.__setitem__(j, k) for k, j in enumerate(s)]; return r
if len(xs) > 2:
    rx, ry = ranks(xs), ranks(ys); n = len(xs)
    rho = 1 - 6 * sum((p - q) ** 2 for p, q in zip(rx, ry)) / (n * (n * n - 1))
    print('\n**Spearman, in-run speed against the applications\' geometric mean: %.3f over %d designs.**' % (rho, n))
print('Wrong or failed: %s.' % (', '.join(fails) if fails else 'none'))
