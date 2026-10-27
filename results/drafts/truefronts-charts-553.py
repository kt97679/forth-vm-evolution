#!/usr/bin/env python3
"""results/drafts/truefronts-charts-553.py CHART.json OUT.png - the true fronts' charts drawn into a file (Iteration 553;
the owner, 551: charts drawn by a script into a file, never data points typed into a chart call). CHART.json is
results/drafts/truefronts-tables-550.py's second output (from results/truefronts-seed75.md): left, the fastest design
of each run against s6; right, every run's size-speed staircase, grouped by what the speed is over. A series is one
speed column - speeds compare only within one."""
import json, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
c = json.load(open(sys.argv[1]))
fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5.6))
for s in c['fastest_by_seed']:
    p = s['points']; a.plot([q['x'] for q in p], [q['y'] for q in p], 'o-', ms=4, label='over: ' + s['name'])
a.axvspan(73.5, max(q['x'] for s in c['fastest_by_seed'] for q in s['points']) + 0.5, color='0.9', zorder=0, label='the stopping series (74-)')
a.set(xlabel='seed', ylabel='the fastest design: times faster than s6 (in the run)', title="Each run's fastest, on its true front")
a.grid(alpha=.3); a.legend(fontsize=7, loc='lower left')
for s in c['size_speed']:
    p = sorted(s['points'], key=lambda q: q['x']); b.plot([q['x'] for q in p], [q['y'] for q in p], drawstyle='steps-post', lw=1.2, label=s['name'])
b.set(xscale='log', xlabel='binary + image, bytes (log)', ylabel='times faster than s6', title='Size against speed: the true fronts, by era')
b.grid(alpha=.3, which='both'); b.legend(fontsize=6.5, loc='upper left')
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=130); print('wrote', sys.argv[2])
