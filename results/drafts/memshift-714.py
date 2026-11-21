#!/usr/bin/env python3
"""results/drafts/memshift-714.py TREE LIST ID ... - chain B's laptop read the lean end 4 KB above chain A's (fb0d57c8a2
108 -> 112 KB, d180351903 116 -> 120; results/followup-roles-seed96-roles-b.md): is it the after-seed-96 batch? Each ID's
record from LIST built in TREE (evolve.build, 8-byte cells) and its pages read as evolve.measure reads them - the
faults of the start-up alone and of the kernel workload (rss = the kernel's), medians of 15 and 9 - with this process's
environment as it is, and 4 KB larger (the stack's page the environment can push over). Run once per tree, the same
shell: the trees' difference is the batch's (3a04c66 before, 7081f96 after)."""
import json, os, sys, tempfile, shutil, statistics
ROOT, LST, IDS = sys.argv[1], sys.argv[2], sys.argv[3:]
sys.path.insert(0, os.path.join(ROOT, 'lab/evolve')); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
R = {r['id']: r for r in (json.loads(l) for l in open(LST) if l.startswith('{"'))}
def flt(eng, img, pw, inp, n):
    v, outs = [], set()
    for _ in range(n):
        p = E.sh(E.PIN + [E.CPUT, eng, img], cwd=pw, inp=inp)
        t = (p.stdout + p.stderr).decode(errors='replace')
        v.append(int([l for l in t.split('\n') if l.startswith('MINFLT')][-1].split()[1]))
        outs.add('\n'.join(l for l in p.stdout.decode(errors='replace').split('\n') if not l[:6].isupper()))
    return statistics.median(v), min(v), max(v), len(outs)
base = dict(os.environ)
for i in IDS:
    dd = tempfile.mkdtemp(prefix='ms-'); eng, img = E.build(E.canon(R[i]['genome']), dd); pw = E.private_work(dd)
    for pad in (0, 4096):
        os.environ.clear(); os.environ.update(base); os.environ['PADX'] = 'y' * pad
        a = flt(eng, img, pw, b'BYE\n', 15); k = flt(eng, img, pw, E.KERNEL_IN + b'BYE\n', 9)
        print('%s %s engine %d B, env +%4d B: start-up %g [%d-%d] pages, kernel %g [%d-%d] = %g KB; outputs alike: %s' % (
              os.path.basename(ROOT.rstrip('/')), i, os.path.getsize(eng), pad, a[0], a[1], a[2], k[0], k[1], k[2], 4 * k[0],
              'yes' if a[3] == 1 and k[3] == 1 else 'NO'))
    os.environ.clear(); os.environ.update(base)
    shutil.rmtree(dd, ignore_errors=True)
