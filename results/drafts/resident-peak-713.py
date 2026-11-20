#!/usr/bin/env python3
"""results/drafts/resident-peak-713.py REPO ID - VmHWM polled to the exit, at start-up and on the kernel workload, beside the fault count (Iteration 713, early-games-713.md)."""
import json, os, subprocess, sys, tempfile, shutil, time
ROOT, ID = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(ROOT, 'lab/evolve')); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
r = [json.loads(l) for l in open(os.path.join(ROOT, 'results/followup-seed96-roles-b.md')) if l.startswith('{"') and ('"%s"' % ID) in l][0]
dd = tempfile.mkdtemp(prefix='hwm-'); eng, img = E.build(E.canon(r['genome']), dd); pw = E.private_work(dd)
for name, inp in (('start-up', b''), ('kernel', E.KERNEL_IN)):
    p = subprocess.Popen([eng, img], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=pw, env={'PATH': '/usr/bin:/bin'})
    p.stdin.write(inp); p.stdin.flush()
    hwm, last, maps = 0, time.time(), None
    while p.poll() is None and time.time() - last < 2.0:
        try:
            s = open('/proc/%d/status' % p.pid).read()
            h = int([l for l in s.split('\n') if l.startswith('VmHWM')][0].split()[1])
            if h > hwm: hwm, last = h, time.time()
            maps = open('/proc/%d/smaps_rollup' % p.pid).read()
        except Exception: pass
    p.stdin.close(); p.wait()
    an = [l for l in (maps or '').split('\n') if l.startswith(('Rss:', 'Anonymous:'))]
    print('%-9s VmHWM %d KB (%d pages); %s' % (name, hwm, hwm // 4, ' '.join(' '.join(l.split()) for l in an)))
shutil.rmtree(dd, ignore_errors=True)
