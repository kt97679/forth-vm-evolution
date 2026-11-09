#!/usr/bin/env python3
"""lab/evolve/remote-load.py REMOTE [--over L] - each remote line's sessions against its host's load (Iteration 633; 630
found dream's 32-bit line of seed 90's chain measured under another load - a backup copied from USB, load 8.45 on
average - by reading results/drafts/dream-load-630.py by hand). REMOTE: a chain's remote directory (process-seed.sh's
OUT/chain-*/remote); for each line HOST-HOW, its sessions.txt (each session's length), its reports (HOST-HOW.md the
first session's, HOST-HOW-sK.md the K-th: \"measured ... UTC\", the session's start) and its load.log (the 1-minute load
average every 30 s). Prints, a line each, every session's mean and peak load and those over L on average (default 2.0:
the checks' own load on dream and the Tegra about 1.4 - seeds 88-90's quiet sessions). Linux counts processes waiting on
a disk in the load average too, so a copy's load overstates its CPU use; the sessions' spread is what it costs
(dream-load-630.py: a paired difference's spread doubled at 12-22). process-seed.sh puts its lines in the summary."""
import glob, os, re, statistics, sys
from datetime import datetime, timezone
a = sys.argv[1:]
if not a: sys.exit(__doc__)
R, over = a[0], float(a[a.index('--over') + 1]) if '--over' in a else 2.0
for d in sorted(x for x in glob.glob(os.path.join(R, '*')) if os.path.isdir(x)):
    line = os.path.basename(d); st = os.path.join(d, 'sessions.txt'); ll = os.path.join(d, 'load.log')
    if not (os.path.exists(st) and os.path.exists(ll)): continue
    secs = [int(m.group(1)) for m in re.finditer(r'session \d+: (\d+) s', open(st).read())]
    load = [(int(f[0]), float(f[1])) for f in (l.split() for l in open(ll)) if len(f) >= 2 and f[0].isdigit()]
    rows = []
    for k, n in enumerate(secs, 1):
        rp = os.path.join(R, line + ('.md' if k == 1 else '-s%d.md' % k))
        m = re.search(r'measured (\S+ \S+) UTC', open(rp).read()) if os.path.exists(rp) else None
        if not m: rows.append((k, None, None)); continue
        t0 = datetime.strptime(m.group(1), '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc).timestamp()
        v = [x for t, x in load if t0 <= t < t0 + n]
        rows.append((k, statistics.fmean(v) if v else None, max(v) if v else None))
    hot = [k for k, mu, _ in rows if mu is not None and mu > over]
    print('%s: %d sessions - load mean/peak %s; over %.1f on average: %s' % (line, len(rows), ', '.join(
        's%d %s' % (k, '%.1f/%.0f' % (mu, pk) if mu is not None else '?') for k, mu, pk in rows), over,
        ' '.join('s%d' % k for k in hot) if hot else 'none'))
