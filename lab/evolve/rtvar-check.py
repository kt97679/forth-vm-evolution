#!/usr/bin/env python3
"""lab/evolve/rtvar-check.py [DESIGN] - the gene rtvar checked on a design (Iteration 687: forth/cv8-fuse-var.4).

Builds DESIGN (default portable-knee; its record's genome) with rtvar 0 and 1 as the search does, and checks:
  alive     both pass the gate's alive() (corpus, kernel workload, far);
  fuses     with 1, `V @` and `V !` in a colon definition compile to vf and vs (the bytes shrink by the calls' and
            @'s, and hold the codes), with 0 they do not; a CREATEd word's @ too;
  labels    no fusion across a branch target: `IF V ELSE W THEN @` and `BEGIN @` after a call give the right values,
            and so do loops over variables (the same output with 0 and 1);
and reports the five applications' code (app_size) and the apps workload's time, 0 against 1 (measure(), 5 rounds).
The last line says PASS or FAIL."""
import importlib.util, json, os, re, subprocess, sys
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
D = sys.argv[1] if len(sys.argv) > 1 else 'portable-knee'; sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location('evolve', os.path.join(HERE_, 'evolve.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
E.setup()
g0 = E.canon(json.load(open(os.path.join(ROOT, 'designs', D, 'record.json')))['genome']); g0['rtvar'] = 0; g0 = E.canon(g0)
g1 = dict(g0); g1['rtvar'] = 1; g1 = E.canon(g1)
if not E.rtvar_on(g1): sys.exit('rtvar-check: %s cannot express rtvar (needs the fusers, spec var, the byte header)' % D)
PROG = b'''VARIABLE V  VARIABLE W  CREATE C 0 ,
: DMP ( a n -- ) 0 DO DUP I + C@ . LOOP DROP ;
: T1 V @ ;  : T2 5 V ! ;  : T3 C @ ;  : T4 ( f -- n ) IF V ELSE W THEN @ ;  : T5 V BEGIN @ ;
: T6 0 10 0 DO V @ I + V ! V @ + LOOP ;
7 V !  9 W !  3 C !
777001 . T1 . 777002 .  T2 777003 . V @ . 777004 .  777005 . T3 . 777006 .
777007 . -1 T4 . 0 T4 . 777008 .  0 V ! 777009 . T6 . V @ . 777010 .
777011 . ' T1 12 DMP 777012 .  777013 . ' T2 12 DMP 777014 .
BYE
'''
fails, out = [], {}
for tag, g in (('0', g0), ('1', g1)):
    d = os.path.join(ROOT, 'build', 'rtvar-check', tag); eng, img = E.build(g, d); pw = E.private_work(d)
    try: E.alive(eng, img, pw, far=True)
    except Exception as e: fails.append('alive with rtvar %s: %s' % (tag, str(e)[:120]))
    o = subprocess.run([eng, img], input=PROG, capture_output=True, cwd=pw, timeout=30).stdout.decode('latin-1')
    val = lambda a, b: re.search(r'%d (.*?) ?%d' % (a, b), o, re.S)
    out[tag] = dict(vals=[(val(a, a + 1).group(1).split() if val(a, a + 1) else None) for a in (777001, 777003, 777005, 777007, 777009)],
                    t1=[int(x) for x in val(777011, 777012).group(1).split()] if val(777011, 777012) else [],
                    t2=[int(x) for x in val(777013, 777014).group(1).split()] if val(777013, 777014) else [],
                    app=E.app_size(eng, img, pw))
    t, raw = E.measure(eng, img, pw, ['apps'], 5); out[tag]['apps'] = t['apps']
    print('rtvar-check: rtvar %s - values %s; T1 %s; T2 %s; apps code %d; apps %.4f s' % (tag, out[tag]['vals'], out[tag]['t1'][:8], out[tag]['t2'][:8], sum(out[tag]['app']), t['apps']), flush=True)
want = [['7'], ['5'], ['3'], ['5', '9'], ['165', '45']]   # T1; T2 then V @; T3; T4 true (V, 5 since T2), false; T6, V after
for tag in '01':
    if out[tag]['vals'] != want: fails.append('values with rtvar %s: %s, not %s' % (tag, out[tag]['vals'], want))
vf, vs = 0x63, 0x64
if vf not in out['1']['t1'][:3]: fails.append("rtvar 1: T1's code does not begin with vf: %s" % out['1']['t1'][:6])
if vs not in out['1']['t2'][:5]: fails.append("rtvar 1: T2's code holds no vs: %s" % out['1']['t2'][:8])
if vf in out['0']['t1'][:3]: fails.append("rtvar 0: T1 fused: %s" % out['0']['t1'][:6])
print('rtvar-check: the five applications\' code %d -> %d bytes; the apps workload %.4f -> %.4f s (%.3f)' % (
    sum(out['0']['app']), sum(out['1']['app']), out['0']['apps'], out['1']['apps'], out['1']['apps'] / out['0']['apps']))
for f in fails: print('rtvar-check: ' + f)
print('rtvar-check: %s - %s' % ('PASS' if not fails else 'FAIL', D))
sys.exit(1 if fails else 0)
