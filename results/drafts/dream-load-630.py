#!/usr/bin/env python3
"""results/drafts/dream-load-630.py [REMOTE] - dream's load during seed 90's chain against the screen's readings (Iteration
630). REMOTE: the chain's remote directory (default /tmp/process/chain-*/remote - process-seed.sh's unpacking), for each
line's sessions.txt (the sessions' lengths) and load.log (the 1-minute load average every 30 s); the readings from
results/chain-screen89 (chain-sessions.py), each session's start from its report. Per session of each dream line: the
mean and peak load; the session's spread - each design's log speed against its median over the sessions, the median of
the absolute deviations (the designs measured in every session, not rejected); the same for the paired difference
against the knee's holder c2ef9488ff (what the screen judges); then the knee's flagged 11a56ff9e4 session by session."""
import glob, json, math, os, re, statistics, sys
from datetime import datetime, timezone
R = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob('/tmp/process/chain-*/remote'))[-1]
D, H, F = 'results/chain-screen89', 'c2ef9488ff', '11a56ff9e4'
load = [(int(t), float(v)) for t, v, *_ in (l.split() for l in open(os.path.join(R, 'dream.lan-prebuilt64', 'load.log')) if l.strip())]
pct = lambda x: '%+.2f%%' % ((math.exp(x) - 1) * 100)
for w in ('32', '64'):
    line = 'dream.lan-prebuilt' + w
    secs = [int(m.group(1)) for m in re.finditer(r'session \d+: (\d+) s', open(os.path.join(R, line, 'sessions.txt')).read())]
    S, start = [], []
    for k in range(1, len(secs) + 1):
        o = json.load(open(os.path.join(D, 's%d' % k, line + '.out.json')))
        S.append({x['id']: math.log(x['speed_here']) for x in o['designs'] if x.get('speed_here') and not x.get('rejected')})
        t = re.search(r'measured (\S+ \S+) UTC', open(os.path.join(D, 's%d' % k, line + '.md')).read()).group(1)
        start.append(datetime.strptime(t, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc).timestamp())
    ids = [i for i in S[0] if all(i in s for s in S)]
    med = {i: statistics.median(s[i] for s in S) for i in ids}
    pm = {i: statistics.median(s[i] - s[H] for s in S) for i in ids if i != H}
    print('dream %s-bit: %d sessions, %d designs in every one' % (w, len(S), len(ids)))
    print('  session  start(UTC)  load mean/peak  spread: speed  paired with %s   %s against it' % (H, F))
    for k, s in enumerate(S):
        lv = [v for t, v in load if start[k] <= t < start[k] + secs[k]]
        sp = statistics.median(abs(s[i] - med[i]) for i in ids)
        pp = statistics.median(abs(s[i] - s[H] - pm[i]) for i in pm)
        print('  s%d       %s       %5.1f / %4.0f      %.2f%%         %.2f%%                     %s'
              % (k + 1, datetime.fromtimestamp(start[k], timezone.utc).strftime('%H:%M'), statistics.fmean(lv), max(lv),
                 sp * 100, pp * 100, pct(s[F] - s[H])))
    q = [k for k in range(len(S)) if statistics.fmean([v for t, v in load if start[k] <= t < start[k] + secs[k]]) < 2]
    d = [S[k][F] - S[k][H] for k in range(len(S))]
    dq = [d[k] for k in q]
    print('  %s against %s: all %d sessions %s +/- %.2f%%; the quiet (load under 2) %s: %s' % (F, H, len(d), pct(statistics.fmean(d)),
          statistics.stdev(d) / math.sqrt(len(d)) * 100, ' '.join('s%d' % (k + 1) for k in q) or 'none',
          (pct(statistics.fmean(dq)) + (' +/- %.2f%%' % (statistics.stdev(dq) / math.sqrt(len(dq)) * 100) if len(dq) > 1 else '')) if dq else '-'))
