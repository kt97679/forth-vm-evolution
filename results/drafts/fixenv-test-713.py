#!/usr/bin/env python3
"""results/drafts/fixenv-test-713.py TREE ID - fixenv-after-seed96.patch tested: the faults (medians of 15; the kernel workload 9) through evolve.sh with the parent's environment as it is and 20 KB larger, the fixed environment and EVOLVE_KEEP_ENV=1 (the old way); the outputs compared (Iteration 713). TREE: a tree with the patch applied."""
import json, os, sys, tempfile, shutil, statistics
ROOT, ID = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(ROOT, 'lab/evolve')); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
r = [json.loads(l) for l in open(os.path.join(ROOT, 'results/followup-seed96-roles-b.md')) if l.startswith('{"') and ('"%s"' % ID) in l][0]
dd = tempfile.mkdtemp(prefix='fe-'); eng, img = E.build(E.canon(r['genome']), dd); pw = E.private_work(dd)
def flt(inp, n=15):
    v, outs = [], set()
    for _ in range(n):
        p = E.sh(E.PIN + [E.CPUT, eng, img], cwd=pw, inp=inp)
        t = (p.stdout + p.stderr).decode(errors='replace')
        v.append(int([l for l in t.split('\n') if l.startswith('MINFLT')][-1].split()[1]))
        outs.add('\n'.join(l for l in p.stdout.decode(errors='replace').split('\n') if not l[:6].isupper()))
    return statistics.median(v), min(v), max(v), len(outs)
base = dict(os.environ)
for keep in ('', '1'):
    for pad in (0, 20000):
        os.environ.clear(); os.environ.update(base); os.environ['PADX'] = 'y' * pad
        if keep: os.environ['EVOLVE_KEEP_ENV'] = '1'
        a = flt(b'BYE\n'); k = flt(E.KERNEL_IN + b'BYE\n', 9)
        print('%-22s parent env +%5d B: start-up %g [%d-%d] pages, kernel %g [%d-%d]; outputs alike: %s' % (
              'as before (KEEP_ENV)' if keep else 'fixed environment', pad, a[0], a[1], a[2], k[0], k[1], k[2], 'yes' if a[3] == 1 and k[3] == 1 else 'NO'))
os.environ.clear(); os.environ.update(base)
print('the environment a run gets:', {k: (v if k != 'EVOLVE_PAD' else '%d x' % len(v)) for k, v in E.run_env(E.PIN + [E.CPUT, eng, img], 'cputime').items()})
shutil.rmtree(dd, ignore_errors=True)
