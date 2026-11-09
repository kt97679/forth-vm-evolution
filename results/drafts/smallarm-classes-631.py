#!/usr/bin/env python3
"""results/drafts/smallarm-classes-631.py - small and fast on ARMv7's new holder in the relf handoff's table (Iteration
631): ae99617f06 and a627b954c6 in final-pick.py step 5's classes from seed 89's follow-up (results/chain-followup89,
every session): x86-64 the geometric mean of the laptop's idle readings' and dream64's, x86-32 of idle32's and dream32's,
ARMv7 the Tegra's - each source the geometric mean of its sessions (as results/drafts/relf-handoff-611.py reads them)."""
import glob, json, math, os, re
gm = lambda v: math.exp(sum(map(math.log, v)) / len(v))
S = sorted(glob.glob('results/chain-followup89/s[0-9]*'), key=lambda p: int(re.search(r's(\d+)$', p).group(1)))
lap, host = {}, {}
for d in S:
    p = os.path.join(d, 'loadtest.md')
    if os.path.exists(p):
        for l in open(p):
            if l.startswith('{"id"'):
                j = json.loads(l)
                for k in ('idle', 'idle32'):
                    if j.get(k): lap.setdefault((k, j['id']), []).append(j[k])
    for h in ('dream.lan-prebuilt64', 'dream.lan-prebuilt32', 'rage.lan-prebuiltarm'):
        p = os.path.join(d, h + '.out.json')
        if os.path.exists(p):
            for x in json.load(open(p))['designs']:
                if x.get('speed_here') and not x.get('rejected'): host.setdefault((h, x['id']), []).append(x['speed_here'])
for i in ('ae99617f06', 'a627b954c6'):
    c64 = gm([gm(lap[('idle', i)]), gm(host[('dream.lan-prebuilt64', i)])])
    c32 = gm([gm(lap[('idle32', i)]), gm(host[('dream.lan-prebuilt32', i)])])
    arm = gm(host[('rage.lan-prebuiltarm', i)])
    print('%s  x86-64 %.3f  x86-32 %.3f  ARMv7 %.3f  (laptop %d sessions, dream %d and %d, the Tegra %d)' % (i, c64, c32, arm,
          len(lap[('idle', i)]), len(host[('dream.lan-prebuilt64', i)]), len(host[('dream.lan-prebuilt32', i)]), len(host[('rage.lan-prebuiltarm', i)])))
