"""results/drafts/relf-handoff-611.py [--json OUT] - the relf handoff's ten designs (Iteration 611; results/handoff-relf-611.md),
as results/drafts/relf-handoff-601.py: each design's speed in the three machine classes (final-pick.py step 5; each a
geometric mean of every session), its exact size and memory, and the genes where its expression differs from s6-cv8b's.
The six portable designs from the follow-up chain's sessions (results/chain-followup87, read side by side); the four JIT
designs from chains B, C and D's (seed 86's), as 601 had them. Markdown on stdout; --json: one record a line. As the build
user (it imports the evolver)."""
import glob, json, math, os, re, sys
a = sys.argv[1:]; out = a[a.index('--json') + 1] if '--json' in a else None
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
gm = lambda v: math.exp(sum(map(math.log, v)) / len(v))
F = [json.loads(l) for l in open('results/relf-designs-611.md') if l.startswith('{')]
num = lambda p: int(re.search(r's(\d+)$', p).group(1))
SESS = {True: sorted(glob.glob('results/chainD-seed86/s[0-9]*'), key=num) + ['results/chainB-seed86', 'results/chainC-seed86'],
        False: sorted(glob.glob('results/chain-followup87/s[0-9]*'), key=num)}
def readings(sess):
    lap, host = {}, {}
    lap, host = {}, {}
    for d in sess:
        p = os.path.join(d, 'loadtest.md')
        if os.path.exists(p):
            for l in open(p):
                if l.startswith('{"id"'):
                    j = json.loads(l)
                    for k in ('idle', 'idle32'):
                        if j.get(k): lap.setdefault((k, j['id']), []).append(j[k])
        for f in glob.glob(os.path.join(d, '*.out.json')):
            h = os.path.basename(f)[:-9]
            for x in json.load(open(f))['designs']:
                if x.get('speed_here'): host.setdefault((h, x['id']), []).append(x['speed_here'])
    return lap, host
RD = {k: readings(v) for k, v in SESS.items()}
s6 = E.express(E.canon(E.HUMAN['s6-cv8b']))
rows = []
for r in F:
    i = r['id']; e = E.express(E.canon(r['genome'])); lap, host = RD[bool(e.get('jit'))]
    m = lambda k: gm(v) if (v := k) else None
    l64, l32 = m(lap.get(('idle', i))), m(lap.get(('idle32', i)))
    d64, d32, arm = m(host.get(('dream.lan-prebuilt64', i))), m(host.get(('dream.lan-prebuilt32', i))), m(host.get(('rage.lan-prebuiltarm', i)))
    c64 = gm([x for x in (l64, d64) if x]); c32 = gm([x for x in (l32, d32) if x])
    diff = {k: e.get(k) for k in sorted(set(e) | set(s6)) if e.get(k) != s6.get(k)}
    rows.append(dict(id=i, why=r.get('why'), sets=r.get('sets'), source='seed 86 chains B-D' if e.get('jit') else 'the follow-up chain (611)', x86_64=c64, x86_32=c32, armv7=arm, mean=gm([x for x in (c64, c32, arm) if x]),
                     laptop64=l64, laptop32=l32, dream64=d64, dream32=d32, total=r['total'], bin=r.get('bin'), rss=r['rss'],
                     enc=e.get('enc'), jit=bool(e.get('jit')), compiler=e.get('compiler'), differs=diff, genome=r['genome']))
rows.sort(key=lambda x: x['mean'])   # 611: the roles' order is relf-readme-611.py's
print('| design | x86-64 | x86-32 | ARMv7 | mean | binary + image | memory KB | enc | JIT | compiler | genes off s6 | why (the final set) |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for x in rows:
    print('| %s | %.4f | %.4f | %s | %.4f | %s | %d | %s | %s | %s | %d | %s |' % (x['id'], x['x86_64'], x['x86_32'], '%.4f%s' % (x['armv7'], '*' if x['jit'] else '') if x['armv7'] else '-',
          x['mean'], format(x['total'], ','), x['rss'], x['enc'], 'yes' if x['jit'] else 'no', x['compiler'], len(x['differs']), x['why']))
if out:
    with open(out, 'w') as o:
        for x in rows: o.write(json.dumps(x, sort_keys=True) + '\n')
