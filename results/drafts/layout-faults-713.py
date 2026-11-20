#!/usr/bin/env python3
"""results/drafts/layout-faults-713.py REPO ID,ID,... - the faults (medians of 15) as built and with the data sections sorted by alignment (-Wl,--sort-section=alignment): memory's layout luck (Iteration 713, early-games-713.md)."""
import json, os, subprocess, sys, tempfile, shutil
ROOT = sys.argv[1]; IDS = sys.argv[2].split(',')
sys.path.insert(0, os.path.join(ROOT, 'lab/evolve')); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
R = {json.loads(l)['id']: json.loads(l) for l in open(os.path.join(ROOT, 'results/followup-seed96-roles-b.md')) if l.startswith('{"')}
env = {'PATH': '/usr/bin:/bin'}
import statistics
def faults(eng, img, pw, inp, n=15):
    v = [faults1(eng, img, pw, inp) for _ in range(n)]
    return '%g [%d-%d]' % (statistics.median(v), min(v), max(v))
def faults1(eng, img, pw, inp):
    p = subprocess.run([E.CPUT, eng, img], input=inp, capture_output=True, cwd=pw, env=env)
    m = [l for l in (p.stdout + p.stderr).decode(errors='replace').split('\n') if l.startswith('MINFLT')]
    return int(m[-1].split()[1]) if m else None
for i in IDS:
    row = []
    for extra in ('', '-Wl,--sort-section=alignment'):
        E._EXTRA_CFLAGS[:] = extra.split()
        dd = tempfile.mkdtemp(prefix='f3-'); eng, img = E.build(E.canon(R[i]['genome']), dd); pw = E.private_work(dd)
        row.append((os.path.getsize(eng), faults(eng, img, pw, b'BYE\n'), faults(eng, img, pw, E.KERNEL_IN + b'BYE\n')))
        shutil.rmtree(dd, ignore_errors=True)
    print('%s: as built: engine %d B, start-up %s pages, kernel %s; sorted by alignment: %d B, %s, %s (medians of 15 [range])' % ((i,) + row[0] + row[1]))
