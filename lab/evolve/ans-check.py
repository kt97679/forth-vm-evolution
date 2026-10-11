#!/usr/bin/env python3
"""ans-check.py [--ids A,B,...] [DB ...] - the held-out check (Iteration 119; the
Forth 2012 test suite since Iteration 124).

The test suite of the Forth 2012 standard (tests/ans: Gerry Jackson's, now kept
by the Forth Standard committee, around John Hayes's core.fr; tests/ans/UPSTREAM)
run on each design, every file in its own process, and compared file by file
and byte for byte with hand-made s6's output: a design must say what s6 says.
Not part of selection - the corpus and the kernel workload are the gate - but a
wider check: it found the stack guard killing the engine on an underflow
(Iteration 118).

A comparison with s6 cannot see a fault every stage shares, so s6's own result
against the suite's expected values comes first: each file's tests run, failed,
whether it reached its end and where it stopped. The end is a sentinel appended
to the file itself - an abort inside INCLUDED returns to the next line of input,
so a sentinel after the INCLUDED prints anyway. Every }T is counted. Then a
negative control: core.fr with one wrong expected value must change s6's
output, or the comparison is BROKEN.

The designs: --ids (genomes from results/*.md), or each DB's re-measured front
(remeasure.json beside it), or its first front. This Forth is case-sensitive and
the files are not all upper case: tools/ans-upper.py upper-cases them.
prelude.fth gives the harness what the kernel lacks. An empty line follows
core.fr: its ACCEPT test reads the next line of input. The suite's files are
copied into each work directory replacing what is there: those are symlinks
into build/work, and copying through one overwrote tests/core/tester.fr from
Iteration 118 to 123. Exit status 1 if a design differs or the control fails.
"""
import os, sys, re, json, glob, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]; ids = None
if '--ids' in args: i = args.index('--ids'); ids = args[i + 1].split(','); del args[i:i + 2]
if any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
T = os.path.join(ROOT, 'tests', 'ans'); CONV = os.path.join(E.EV, 'ans')
shutil.rmtree(CONV, ignore_errors=True); os.makedirs(CONV)
# What comes before a test file: '' is the empty line core.fr's ACCEPT test reads.
HARNESS = ['tester.fr', 'core.fr', '', 'utilities.fth', 'errorreport.fth']
# Each test file and how much of the harness precedes it: none (prelimtest
# stands alone), the tester and core.fr, or all of it - the optional word sets
# use utilities.fth and end with errorreport.fth's SET-ERROR-COUNT.
FILES = [('prelimtest.fth', 0), ('core.fr', 3), ('coreplustest.fth', 3)] + [(f, 5) for f in (
    'coreexttest.fth', 'blocktest.fth', 'doubletest.fth', 'exceptiontest.fth', 'facilitytest.fth', 'filetest.fth',
    'localstest.fth', 'memorytest.fth', 'toolstest.fth', 'searchordertest.fth', 'stringtest.fth')]
TESTED = [f for f, _ in FILES]
for f in dict.fromkeys(TESTED + [h for h in HARNESS if h] + ['required-helper1.fth', 'required-helper2.fth']):
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'ans-upper.py'), os.path.join(T, f), os.path.join(CONV, f)], check=True)
    if f in TESTED:
        with open(os.path.join(CONV, f), 'a', encoding='latin-1') as fh: fh.write('\nS" <<END OF %s>>" TYPE CR\n' % f)
shutil.copy(os.path.join(T, 'prelude.fth'), os.path.join(CONV, 'prelude.fth'))
# Iteration 165: the system's own extensions under test too - coreext.4 (the
# standard words the kernel leaves out) and extend.4 (the search order).
for _x in ('coreext.4', 'extend.4'): shutil.copy(os.path.join(ROOT, 'forth', _x), os.path.join(CONV, _x))
core = open(os.path.join(CONV, 'core.fr'), encoding='latin-1').read(); k = core.rindex('S" <<END OF core.fr>>"')
open(os.path.join(CONV, 'core-control.fr'), 'w', encoding='latin-1').write(core[:k] + 'T{ 1 2 + -> 4 }T\n' + core[k:])

def program(f, n, core='core.fr'):
    if not n: return 'S" %s" INCLUDED\nBYE\n' % f
    p, mark = 'S" prelude.fth" INCLUDED\nS" extend.4" INCLUDED\nS" coreext.4" INCLUDED\n', '[ DECIMAL .( <<FILE>> ) #T @ . CR\n'   # the file under test starts here
    for h in HARNESS[:n]:
        if h == 'core.fr' and f == 'core.fr': p += mark
        h = core if h == 'core.fr' else h
        p += ('S" %s" INCLUDED\n' % h) if h else '\n'
        if h == 'tester.fr': p += 'VARIABLE #T 0 #T !\n: }T 1 #T +! }T ;\n'          # every test counted
    # Iteration 192: filetest's nested SAVE-INPUT test uses SI_INC, SI1 and S$,
    # which coreexttest defines - upstream's runtests.fth includes that file
    # first, in the same session. Here each file has its own: the three, as
    # coreexttest has them.
    if f == 'filetest.fth':
        p += 'VARIABLE SI_INC 0 SI_INC !\n: SI1 SI_INC @ >IN +! 15 SI_INC ! ;\n: S$ S" SAVE-INPUT SI1 RESTORE-INPUT 12345" ;\n'
    if f != 'core.fr': p += mark + 'S" %s" INCLUDED\n' % f
    return p + '[ CR DECIMAL .( TESTS ) #T @ . .( FAILED ) #ERRORS @ . CR\nBYE\n'

def run_all(eng, img, pw, core='core.fr', only=None):
    for f in os.listdir(CONV):
        dst = os.path.join(pw, f)
        if os.path.lexists(dst): os.remove(dst)            # a symlink into build/work: never write through it
        shutil.copy(os.path.join(CONV, f), dst)
    out = {}
    for f, n in FILES:
        if only and f != only: continue
        try:
            r = subprocess.run([eng, img], input=program(f, n, core).encode(), cwd=pw, capture_output=True, timeout=120)
            rc, so = r.returncode, r.stdout
        except subprocess.TimeoutExpired as e:
            rc, so = 'timeout', e.stdout or b''
        t = so.decode('latin-1').replace('\r', '')
        if not n:
            tests, failed = len(re.findall(r'(?i)pass #\d+', t)), len(re.findall(r'(?i)error #\d+', t))
        else:
            m0 = re.search(r'<<FILE>> (\d+)', t); m = re.search(r'TESTS (\d+) FAILED (\d+)', t)
            tests = int(m.group(1)) - int(m0.group(1)) if m and m0 else None; failed = int(m.group(2)) if m else None
        tail = t.split('<<FILE>>', 1)[-1]
        stop = re.search(r'(Undefined word|Not found) (\S+)', tail)
        end = ('<<END OF %s>>' % f) in t
        out[f] = dict(rc=rc, out=so, tests=tests, failed=failed, end=end, stop='' if end or not stop else stop.group(2))
    return out

designs, recs = [], {}
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
print('# The Forth 2012 test suite: hand-made s6, then each design against it (held out)\n')
print('Hand-made s6 against the suite\'s expected values - its own tests in each file (core.fr\'s and the')
print('helpers\' not counted again), failed, and where a file stopped short of its end:\n')
print('| file | tests | failed | whole file | stopped at |\n|---|---|---|---|---|')
for f, _ in FILES:
    r = ref[f]
    print('| %s | %s | %s | %s | %s |' % (f, r['tests'], r['failed'], 'yes' if r['end'] else 'no', r['stop'] or ('exit %s' % r['rc'] if r['rc'] else '')))
ctl = run_all(*E.REF, core='core-control.fr', only='core.fr')['core.fr']
caught = ctl['out'] != ref['core.fr']['out'] and (ctl['failed'] or 0) == (ref['core.fr']['failed'] or 0) + 1
print('\nNegative control - core.fr with one wrong expected value: %s (failed %s -> %s).\n'
      % ('caught' if caught else 'BROKEN: the comparison cannot see a wrong answer', ref['core.fr']['failed'], ctl['failed']))
print('| design | guard | files as s6 | differing |\n|---|---|---|---|')
bad = 0
for did, g in designs:
    d = os.path.join(E.EV, 'ans-' + did); shutil.rmtree(d, ignore_errors=True)
    try:
        g = E.canon(g); eng, img = E.build(g, d); out = run_all(eng, img, E.private_work(d))
    except Exception as e:
        print('| %s | | build failed: %s | |' % (did, str(e)[:60])); bad += 1; continue
    diff = [f for f in TESTED if (out[f]['rc'], out[f]['out']) != (ref[f]['rc'], ref[f]['out'])]
    bad += bool(diff)
    print('| %s | %d | %d of %d | %s |' % (did, E.express(g).get('guard', 0), len(TESTED) - len(diff), len(TESTED),
          ', '.join('%s (rc %s)' % (f, out[f]['rc']) for f in diff) or '-'), flush=True)
    shutil.rmtree(d, ignore_errors=True)
print('\n%d of %d designs differ from s6 somewhere.' % (bad, len(designs)))
sys.exit(1 if bad or not caught else 0)
