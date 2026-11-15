#!/usr/bin/env python3
"""lab/evolve/rtinline-check.py [DESIGN] - the gene rtinline checked on a design (Iteration 694: forth/cv8-fuse-inline.4).

Builds DESIGN (default portable-knee; its record's genome) with rtinline 0 and 1 as the search does, and checks:
  alive     both pass the gate's alive() (corpus, kernel workload, far);
  values    short words of every kind the overlay copies (two operations, a literal and an operation, three, a 16-bit
            literal, an empty body, an EXIT within) and of every kind it must not (four operations, the return stack,
            calls, a DOES> child, a variable) give the same values with 0 and 1 - and the right ones;
  copies    with 1 a call to a short body compiles as its bytes (T1's code no longer the 0 build's); a call to a body it
            must not copy stays a call (T7's code does not begin with B2's - the addresses differ between the builds);
and reports the apps workload's time (medians of 15) and each selection program's benchmark alone (genapps.py's
drivers, the full run less the load; build/genapps/work-8 must hold them - genapps.py --rounds 1 --systems s6).
The last line says PASS or FAIL."""
import importlib.util, json, os, re, subprocess, sys, time
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
D = sys.argv[1] if len(sys.argv) > 1 else 'portable-knee'; sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('evolve', os.path.join(HERE_, 'evolve.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
E.setup()
g0 = E.canon(json.load(open(os.path.join(ROOT, 'designs', D, 'record.json')))['genome']); g0['rtinline'] = 0; g0 = E.canon(g0)
g1 = dict(g0); g1['rtinline'] = 1; g1 = E.canon(g1)
if not E.rtinline_on(g1): sys.exit('rtinline-check: %s cannot express rtinline (it needs the run-time fusers)' % D)
PROG = b''': A1 SWAP DROP ;  : A2 1+ 1+ ;  : A3 OVER OVER + ;  : A4 5 + ;  : A5 1000 + ;  : A6 ;  : A7 DUP EXIT DROP ;
: B1 DUP DUP DUP DUP ;  : B2 >R 1+ R> ;  : B3 A1 A1 ;  : K CREATE , DOES> @ ;  9 K B4  VARIABLE B5  6 B5 !
: DMP ( a n -- ) 0 DO DUP I + C@ . LOOP DROP ;
: T1 A2 ;  : T7 B2 ;
: T2 3 4 A1 . 7 A2 . 2 5 A3 . . . 1 A4 . 1 A5 . 8 A6 . 4 A7 . . ;
: T3 1 B1 + + + + . 2 3 B2 . . 1 2 3 B3 . B4 . B5 @ . ;
777001 . T2 T3 777002 .
777003 . ' T1 6 DMP 777004 . ' T7 6 DMP 777005 . ' B2 3 DMP 777006 .
BYE
'''
WANT = ['4', '9', '7', '5', '2', '6', '1001', '8', '4', '4', '5', '3', '3', '3', '9', '6']
fails, out = [], {}
W = os.path.join(ROOT, 'build', 'genapps', 'work-8')
def med(cmd, data, k=15, cwd=None):
    ts = []
    for _ in range(k):
        t = time.perf_counter(); subprocess.run(['taskset', '-c', '1'] + cmd, input=data, capture_output=True, cwd=cwd); ts.append(time.perf_counter() - t)
    return sorted(ts)[k // 2]
for tag, g in (('0', g0), ('1', g1)):
    d = os.path.join(ROOT, 'build', 'rtinline-check', D + '-' + tag); eng, img = E.build(g, d); pw = E.private_work(d)
    try: E.alive(eng, img, pw, far=True)
    except Exception as e: fails.append('alive with rtinline %s: %s' % (tag, str(e)[:120]))
    o = subprocess.run([eng, img], input=PROG, capture_output=True, cwd=pw, timeout=30).stdout.decode('latin-1')
    v = re.search(r'777001 (.*?) ?777002', o, re.S); b = re.search(r'777003 (.*?) ?777004 (.*?) ?777005 (.*?) ?777006', o, re.S)
    out[tag] = dict(vals=v.group(1).split() if v else o[-200:], t1=b.group(1).split() if b else None, t7=b.group(2).split() if b else None, b2=b.group(3).split() if b else None,
                    apps=med([eng, img], E.APPS_IN, cwd=pw))
    bench = {}
    for app in E.appsize.SELECTION:
        if os.path.exists(os.path.join(W, 'lab-%s-full.fs' % app)):
            f, l = (med([eng, img], ('S" lab-%s-%s.fs" INCLUDED\n' % (app, m)).encode(), 7, W) for m in ('full', 'load'))
            bench[app] = f - l
    out[tag]['bench'] = bench
    print('rtinline-check: rtinline %s - values %s; T1 %s; T7 %s; apps %.1f ms' % (tag, out[tag]['vals'], out[tag]['t1'], out[tag]['t7'], 1e3 * out[tag]['apps']), flush=True)
for tag in '01':
    if out[tag]['vals'] != WANT: fails.append('values with rtinline %s: %s, not %s' % (tag, out[tag]['vals'], WANT))
if out['1']['t1'] == out['0']['t1']: fails.append('rtinline 1: T1 compiled as with 0 - A2 not copied')
if not out['1']['t7'] or out['1']['t7'][:3] == out['1']['b2']: fails.append('rtinline 1: T7 begins with B2\'s bytes - the return stack copied')
print('rtinline-check: the apps workload %.1f -> %.1f ms (%.3f)' % (1e3 * out['0']['apps'], 1e3 * out['1']['apps'], out['1']['apps'] / out['0']['apps']))
for app in out['0']['bench']:
    a, b = out['0']['bench'][app], out['1']['bench'].get(app)
    if b: print('rtinline-check: %-9s alone %.1f -> %.1f ms (%.3f)' % (app, 1e3 * a, 1e3 * b, b / a))
for f in fails: print('rtinline-check: ' + f)
print('rtinline-check: %s - %s' % ('PASS' if not fails else 'FAIL', D))
sys.exit(1 if fails else 0)
