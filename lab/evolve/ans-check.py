#!/usr/bin/env python3
"""ans-check.py [--ids A,B,...] [DB ...] - the held-out check (Iteration 119).

The ANS Forth test suite (tests/ans: Hayes's core.fr, Jackson's 0.3) run on
each design and compared, file by file and byte for byte, with hand-made
s6's output: a design must say what s6 says. Not part of selection - the
corpus and the kernel workload are the gate - but a second, wider check: it
found the stack-guard gene killing the engine on a stack underflow, which
neither the corpus nor the kernel workload ever does.

The designs: --ids (genomes from results/*.md), or each DB's re-measured
front (remeasure.json beside it), or its first front. The files are
lowercase: tools/ans-upper.py upper-cases them; prelude.fth adds TRUE FALSE
.( - and an empty line follows core.fr, whose ACCEPT test reads the next
line (without it the next file never runs).
"""
import os, sys, json, glob, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]; ids = None
if '--ids' in args: i = args.index('--ids'); ids = args[i + 1].split(','); del args[i:i + 2]
if any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
sys.path.insert(0, os.path.join(ROOT, 'tools')); import importlib.util
spec = importlib.util.spec_from_file_location('ansup', os.path.join(ROOT, 'tools', 'ans-upper.py'))
E.setup()
T = os.path.join(ROOT, 'tests', 'ans'); CONV = os.path.join(E.EV, 'ans')
os.makedirs(CONV, exist_ok=True)
FILES = ['core.fr', 'coreplus.fth', 'coreexttest.fth', 'doubletest.fth', 'exceptiontest.fth', 'filetest.fth',
         'memorytest.fth', 'searchordertest.fth', 'stringtest.fth', 'toolstest.fth']
for f in FILES + ['tester.fr']:
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'ans-upper.py'), os.path.join(T, f), os.path.join(CONV, f)], check=True)
shutil.copy(os.path.join(T, 'prelude.fth'), os.path.join(CONV, 'prelude.fth'))
def run_all(eng, img, pw):
    for f in os.listdir(CONV): shutil.copy(os.path.join(CONV, f), os.path.join(pw, f))
    out = {}
    for f in FILES:
        prog = 'S" prelude.fth" INCLUDED\nS" tester.fr" INCLUDED\nS" core.fr" INCLUDED\n\n'
        if f != 'core.fr': prog += 'S" %s" INCLUDED\n' % f
        r = subprocess.run([eng, img], input=(prog + 'BYE\n').encode(), cwd=pw, capture_output=True, timeout=120)
        out[f] = (r.returncode, r.stdout, r.stderr)
    return out
designs = []
recs = {}
for fl in glob.glob(os.path.join(ROOT, 'results', '*.md')):
    for l in open(fl):
        try: r = json.loads(l)
        except ValueError: continue
        if isinstance(r, dict) and 'genome' in r: recs[r['id']] = r['genome']
if ids: designs = [(i, recs[i]) for i in ids if i in recs]
for db in args:
    R = {}
    for l in open(db):
        try: r = json.loads(l); R[r['id']] = r
        except ValueError: pass
    rmf = os.path.join(os.path.dirname(db), os.path.basename(db).replace('db', 'remeasure', 1).replace('.jsonl', '.json'))
    front = list(json.load(open(rmf))) if os.path.exists(rmf) else E.first_front([i for i in R if R[i]['status'] == 'ok'], R)
    designs += [(i, R[i]['genome']) for i in front if i in R]
ref = run_all(*E.REF)
print('# The ANS suite against hand-made s6 (held out)\n')
print('| design | guard | files as s6 | differing |\n|---|---|---|---|')
bad = 0
for did, g in designs:
    d = os.path.join(E.EV, 'ans-' + did); shutil.rmtree(d, ignore_errors=True)
    try:
        g = E.canon(g); eng, img = E.build(g, d); out = run_all(eng, img, E.private_work(d))
    except Exception as e:
        print('| %s | | build failed: %s | |' % (did, str(e)[:60])); continue
    diff = [f for f in FILES if out[f][:2] != ref[f][:2]]
    bad += bool(diff)
    print('| %s | %d | %d of %d | %s |' % (did, E.express(g).get('guard', 0), len(FILES) - len(diff), len(FILES),
          ', '.join('%s (rc %d)' % (f, out[f][0]) for f in diff) or '-'))
    shutil.rmtree(d, ignore_errors=True)
print('\n%d of %d designs differ from s6 somewhere.' % (bad, len(designs)))
