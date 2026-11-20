#!/usr/bin/env python3
"""results/drafts/env-pages-713.py REPO ID - the memory reading (cputime's faults) at start-up and on the kernel workload with the environment as it is, empty, and 20 KB larger (Iteration 713, early-games-713.md)."""
import json, os, subprocess, sys, tempfile, shutil
ROOT, ID = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(ROOT, 'lab/evolve')); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
r = [json.loads(l) for l in open(os.path.join(ROOT, 'results/followup-seed96-roles-b.md')) if l.startswith('{"') and ('"%s"' % ID) in l][0]
dd = tempfile.mkdtemp(prefix='flt-'); eng, img = E.build(E.canon(r['genome']), dd); pw = E.private_work(dd)
def faults(inp, env):
    p = subprocess.run([E.CPUT, eng, img], input=inp, capture_output=True, cwd=pw, env=env)
    t = (p.stdout + p.stderr).decode(errors='replace')
    m = [l for l in t.split('\n') if l.startswith('MINFLT')]
    return int(m[-1].split()[1]) if m else None
full = dict(os.environ); empty = {'PATH': '/usr/bin:/bin'}
big = dict(full, PAD='x' * 20000)
print('%s: engine %d B, image %d B; the record: rss %s, kernel %s' % (ID, os.path.getsize(eng), os.path.getsize(img), r['rss'], r['mem'].get('kernel')))
for name, inp in (('BYE only (start-up)', b'BYE\n'), ('the kernel workload', E.KERNEL_IN + b'BYE\n')):
    print('  %-22s pages: env of %5d B -> %s; empty env -> %s; env + 20 KB -> %s' % (name, sum(len(k) + len(v) + 2 for k, v in full.items()),
          faults(inp, full), faults(inp, empty), faults(inp, big)))
shutil.rmtree(dd, ignore_errors=True)
