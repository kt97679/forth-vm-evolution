#!/usr/bin/env python3
"""run.py ZIP PROGRAM [--engine ENG IMG] - an Appbench program on our Forth (Iteration 467, a study's tool)

ZIP is Appbench's archive (appbench.zip, kept outside this repository - its programs' terms differ: brainless public
domain; benchgc, lexex and brew GPL; fcp and cd16sim no notice). The program's files are unpacked into a scratch
folder, their source folded to upper case by fold.py (strings, comments, file and character names kept; strings that
EVALUATE takes upper-cased unless they hold a '/'; $hex made decimal), our own forth/extend.4 and forth/coreext.4
copied beside them, and the program run on the hand-made s6 (or ENG IMG) after prelude.fth, with the call Appbench's
benchstrings gives. Prints the time and the program's check: fcp's node count, brainless's nodes and evaluations,
cd16sim's own "X should be X" line.
"""
import os, re, shutil, subprocess, sys, tempfile, time, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE); from fold import fold
CALLS = {'fcp': 'include fcp-1.31-64.f||!: setup SETUP ;||bench bye',          # fcp evaluates a lower-case "setup"
         'brainless': 'include benchmark.fs benchmark bye',
         'cd16sim': ': 3drop 2drop drop ; include bench.f 1000000 benchmark bye',
         'lexex': 'include run.fth bye', 'benchgc': '64000 include bench-gc5.fs bye'}
CHECKS = {'fcp': r'(?s)\b120287\b.*Results:', 'brainless': r'110023 nodes .* 163278 evals',
          'cd16sim': r'(\d+ \d+ \d+ \d+) should be \1\b'}
zp, prog = sys.argv[1], sys.argv[2]
if '--engine' in sys.argv: k = sys.argv.index('--engine'); eng, img = sys.argv[k + 1], sys.argv[k + 2]
else:
    sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
    E.setup(); eng, img = E.REF[0], E.REF[1]
def hexfix(t): return re.sub(r'(?<![\w$])\$([0-9A-F]+)\b', lambda m: str(int(m.group(1), 16)), t)
with tempfile.TemporaryDirectory() as d:
    with zipfile.ZipFile(zp) as z:
        for n in z.namelist():
            m = re.match(r'[^/]+/%s/(.+)' % re.escape(prog), n)
            if not m or '/CVS/' in '/' + m.group(1) or n.endswith('/'): continue
            out = os.path.join(d, m.group(1)); os.makedirs(os.path.dirname(out), exist_ok=True); data = z.read(n)
            if re.search(r'\.(fs|f|fth|fb|4th|vhd)$', n, re.I): data = hexfix(fold(data.decode('latin-1'))).encode('latin-1')
            open(out, 'wb').write(data)
    for f in ('extend.4', 'coreext.4'): shutil.copy(os.path.join(ROOT, 'forth', f), d)
    text = open(os.path.join(HERE, 'prelude.fth')).read() + '\n' + ' '.join(s[1:] if s.startswith('!') else hexfix(fold(s)) for s in CALLS[prog].split('||')) + '\n'
    t = time.time(); r = subprocess.run([eng, img], input=text.encode('latin-1'), capture_output=True, timeout=600, cwd=d); dt = time.time() - t
out = r.stdout.decode('latin-1').replace('\r', '')
bad = [l.strip() for l in out.split('\n') if re.search(r'Undefined|rror', l)]
ok = bool(re.search(CHECKS[prog], out)) if prog in CHECKS else None
print('%s: %.2f s, rc %d, check %s%s' % (prog, dt, r.returncode, {True: 'PASS', False: 'FAIL', None: 'none'}[ok], ('; ' + ' | '.join(dict.fromkeys(bad))[:200]) if bad else ''))
sys.exit(0 if ok else 1)
