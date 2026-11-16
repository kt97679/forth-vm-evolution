#!/usr/bin/env python3
"""results/drafts/deaths-verify-698.py DB - seed 92's two death kinds, their causes checked on this tree (Iteration 698).

sod16 "wrong output: apps": the apps workload's output against s6's, line by line - which program's line differs (693:
shellmix's DOES> buffers past sod16's 128 KB DOES> reach). cpt16 "died: application size (gc16)": evolve.py's app_size
on the rebuilt design - does it give no reading of gc16 here too, and what each program's load prints. As the build user,
in a built tree, alone (an evolver process).
"""
import json, os, re, shutil, sys, tempfile
DB = sys.argv[1]
sys.argv = ['x']; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lab', 'evolve'))
import evolve as E, appsize
R = {}
for l in open(DB, errors='replace'):
    try: r = json.loads(l)
    except ValueError: continue
    R[r['id']] = r
E.setup()
E.run_metric(*E.REF, 'apps'); ref = E.OUT_LAST[0].decode('latin-1', 'replace') if isinstance(E.OUT_LAST[0], bytes) else str(E.OUT_LAST[0])
T = tempfile.mkdtemp(prefix='deaths-verify-')
for i, r in R.items():
    s = r.get('status', '')
    if not (s.startswith('wrong output: apps') or s.startswith('died: application size')): continue
    enc = r['genome'].get('enc'); d = os.path.join(T, i)
    eng, img = E.build(E.canon(r['genome']), d); pw = E.private_work(d)
    if s.startswith('wrong output'):
        try:
            E.run_metric(eng, img, pw, 'apps'); out = E.OUT_LAST[0]
            out = out.decode('latin-1', 'replace') if isinstance(out, bytes) else str(out)
        except Exception as e: out = 'raised: %s' % e
        a, b = ref.split('\n'), out.split('\n')
        diff = [(x, y) for x, y in zip(a, b) if x != y] + ([('(%d lines)' % len(a), '(%d lines)' % len(b))] if len(a) != len(b) else [])
        print('%s %s gen %s %s: %d lines differ; the first: s6 %r / here %r' % (i, enc, r.get('gen'), s, len(diff),
              diff[0][0][:70] if diff else '', diff[0][1][:70] if diff else ''))
    else:
        got = []
        for app in appsize.SELECTION:
            o = [E.sh([eng, img], cwd=pw, inp=appsize.stdin(app, m), timeout=60, cpu=5).stdout.decode('latin-1') for m in ('size', 'count')]
            v = appsize.parse(*o)
            got.append('%s %s' % (app, 'none' if v is None else v[0] - v[1]))
            if v is None: got[-1] += ' (its load ends: %r)' % o[0].strip().replace('\n', ' | ')[-90:]
        print('%s %s gen %s %s: %s' % (i, enc, r.get('gen'), s, '; '.join(got)))
    shutil.rmtree(d, ignore_errors=True)
shutil.rmtree(T, ignore_errors=True)
