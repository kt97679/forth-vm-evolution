#!/usr/bin/env python3
"""lab/evolve/rtconst-check.py [DESIGN] - the gene rtconst checked on a design (Iteration 691: forth/cv8-fuse-const.4).

Builds DESIGN (default portable-knee; its record's genome) with rtconst 0 and 1 as the search does, and checks:
  alive     both pass the gate's alive() (corpus, kernel workload, far);
  values    constants of every literal width (LIT8, LIT16, a negative's LIT32, past 32 bits LIT64), `: F 7 ;`, BL,
            and one with + after it, give the same values with 0 and 1 - and the right ones;
  fuses     with 1 a call to a constant compiles as its literal (T1's code no longer the 0 build's);
and reports the apps workload's time (medians of 15) and each selection program's benchmark alone (genapps.py's
drivers, the full run less the load; build/genapps/work-8 must hold them - genapps.py --rounds 1 --systems s6).
The last line says PASS or FAIL."""
import importlib.util, json, os, re, subprocess, sys, time
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
D = sys.argv[1] if len(sys.argv) > 1 else 'portable-knee'; sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('evolve', os.path.join(HERE_, 'evolve.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
E.setup()
g0 = E.canon(json.load(open(os.path.join(ROOT, 'designs', D, 'record.json')))['genome']); g0['rtconst'] = 0; g0 = E.canon(g0)
g1 = dict(g0); g1['rtconst'] = 1; g1 = E.canon(g1)
if not E.rtconst_on(g1): sys.exit('rtconst-check: %s cannot express rtconst (it needs the run-time fusers)' % D)
PROG = b'''64 CONSTANT N  70000 CONSTANT M  -5 CONSTANT K  5000000000 CONSTANT G  : F 7 ;
: DMP ( a n -- ) 0 DO DUP I + C@ . LOOP DROP ;
: T1 N ;  : T2 N 1+ ;  : T3 M ;  : T4 K ;  : T5 G ;  : T6 F 2 + ;  : T7 BL ;  : T8 N 3 + M + ;
777001 . T1 . T2 . T3 . T4 . T5 . T6 . T7 . T8 . 777002 .
777003 . ' T1 8 DMP 777004 .
BYE
'''
WANT = ['64', '65', '70000', '-5', '5000000000', '9', '32', '70067']
fails, out = [], {}
W = os.path.join(ROOT, 'build', 'genapps', 'work-8')
def med(cmd, data, k=15, cwd=None):
    ts = []
    for _ in range(k):
        t = time.perf_counter(); subprocess.run(['taskset', '-c', '1'] + cmd, input=data, capture_output=True, cwd=cwd); ts.append(time.perf_counter() - t)
    return sorted(ts)[k // 2]
for tag, g in (('0', g0), ('1', g1)):
    d = os.path.join(ROOT, 'build', 'rtconst-check', tag); eng, img = E.build(g, d); pw = E.private_work(d)
    try: E.alive(eng, img, pw, far=True)
    except Exception as e: fails.append('alive with rtconst %s: %s' % (tag, str(e)[:120]))
    o = subprocess.run([eng, img], input=PROG, capture_output=True, cwd=pw, timeout=30).stdout.decode('latin-1')
    v = re.search(r'777001 (.*?) ?777002', o, re.S); b = re.search(r'777003 (.*?) ?777004', o, re.S)
    out[tag] = dict(vals=v.group(1).split() if v else None, t1=b.group(1).split() if b else None, apps=med([eng, img], E.APPS_IN, cwd=pw))
    bench = {}
    for app in E.appsize.SELECTION:
        if os.path.exists(os.path.join(W, 'lab-%s-full.fs' % app)):
            f, l = (med([eng, img], ('S" lab-%s-%s.fs" INCLUDED\n' % (app, m)).encode(), 7, W) for m in ('full', 'load'))
            bench[app] = f - l
    out[tag]['bench'] = bench
    print('rtconst-check: rtconst %s - values %s; T1 %s; apps %.1f ms' % (tag, out[tag]['vals'], out[tag]['t1'], 1e3 * out[tag]['apps']), flush=True)
for tag in '01':
    if out[tag]['vals'] != WANT: fails.append('values with rtconst %s: %s, not %s' % (tag, out[tag]['vals'], WANT))
if out['1']['t1'] == out['0']['t1']: fails.append('rtconst 1: T1 compiled as with 0 - no constant folded')
print('rtconst-check: the apps workload %.1f -> %.1f ms (%.3f)' % (1e3 * out['0']['apps'], 1e3 * out['1']['apps'], out['1']['apps'] / out['0']['apps']))
for app in out['0']['bench']:
    a, b = out['0']['bench'][app], out['1']['bench'].get(app)
    if b: print('rtconst-check: %-9s alone %.1f -> %.1f ms (%.3f)' % (app, 1e3 * a, 1e3 * b, b / a))
for f in fails: print('rtconst-check: ' + f)
print('rtconst-check: %s - %s' % ('PASS' if not fails else 'FAIL', D))
sys.exit(1 if fails else 0)
