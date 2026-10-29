#!/usr/bin/env python3
"""results/drafts/ccflags-diff-567.py [OLD] - which recorded designs ccflags-after-seed81.patch builds differently (Iteration
567): each record of seeds 76-80's results files, its flags under the old ccflags (evolve.py at commit OLD, default
1531873 - before the batch) and today's. 567: 9 of 1,481 (seed 78 6, seed 79 3), each an unexpressed alignhot.
"""
import json, os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); OLD = sys.argv[1] if len(sys.argv) > 1 else '1531873'
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
src = subprocess.run(['git', '-C', ROOT, 'show', OLD + ':lab/evolve/evolve.py'], capture_output=True, text=True).stdout
i = src.index('def ccflags(g):'); j = src.index('_EXTRA_CFLAGS = os.environ', i)
ns = dict(vars(E)); exec(src[i:j], ns); old = ns['ccflags']
for f in [os.path.join(ROOT, 'results', 'evolve-amd-ryzen-7-pro-8840hs-seed%d.md' % s) for s in (76, 77, 78, 79, 80)]:
    n = ch = 0; what = {}
    for l in open(f):
        if not l.startswith('{"bin"'): continue
        try: g = E.canon(json.loads(l)['genome'])
        except Exception: continue
        n += 1; a, b = old(g), E.ccflags(g)
        if a != b:
            ch += 1; k = ' '.join(sorted(set(a) - set(b))); what[k] = what.get(k, 0) + 1
    print(f.split('-')[-1], 'records', n, 'built differently', ch, sorted(what.items(), key=lambda x: -x[1])[:4])
