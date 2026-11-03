"""results/drafts/article-figures-600.py - the figures the article's method section quotes, recomputed from the runs'
records on the true fronts (Iteration 600; GOALS.md step 3's last part; results/drafts/article-method-548.md, whose [74+]
markers wait on them). From the repository only: the stopping series' ledger (results/stopping-series.md - each run's true
front, its hypervolume in the fixed box and its extremes, from seed 77), each run's results file (its counts: designs,
one round first, the screen, the fast end re-measured, held out), the genome (lab/evolve/evolve.py after consolidation),
the final set (results/final-set-chainsBCD-seed86.md) and the chains' readings across machines (results/chain*-seed86/).
Markdown on stdout: results/article-figures-600.md. As the build user (it imports the evolver)."""
import glob, json, math, os, re, statistics, sys
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
gm = lambda v: math.exp(sum(map(math.log, v)) / len(v))
med = statistics.median
num = lambda s: int(s.replace(',', ''))
c = lambda v: '-' if v is None else format(v, ',')

# the genome
g = E.random_genome(__import__('random').Random(1)); fz = set(E.FROZEN)
print('# The method section\'s figures, recomputed (Iteration 600; results/drafts/article-figures-600.py)\n')
print('## The genome (lab/evolve/evolve.py, after consolidation - 599)\n')
print('%d genes; %d frozen at one value (%s); %d free.\n' % (len(g), len(fz & set(g)), ', '.join(sorted(fz & set(g))), len(set(g) - fz)))

# the runs: the ledger and the results files
L = [json.loads(l) for l in open('results/stopping-series.md') if l.startswith('{"seed"') or l.startswith('{"confirmation"') or l.startswith('{"random"')]
L = list({(r.get('seed') or r.get('confirmation') or r.get('random')): r for r in L}.values())   # seed 77 opens both of the series' method lines
L = sorted((r for r in L if (r.get('seed') or r.get('confirmation') or r.get('random')) >= 77), key=lambda r: r.get('seed') or r.get('confirmation') or r.get('random'))
rows = []
for r in L:
    s = r.get('seed') or r.get('confirmation') or r.get('random')
    kind = 'series' if 'seed' in r else 'confirmation' if 'confirmation' in r else 'random'
    t = open('results/evolve-amd-ryzen-7-pro-8840hs-seed%d.md' % s).read()
    f = lambda p, k=num: (lambda m: k(m.group(1)) if m else None)(re.search(p, t))
    one = re.search(r'\*\*One round first\*\*: [\d,]+ children stopped after one round, ([\d.]+)% of those measured; ([\d,]+) audited in full, (\d+) of them on the front', t)
    scr = re.search(r'audited \(one in 10, measured anyway\): (\d+), of them on the front: (\d+)', t)
    fe = re.search(r'the fastest ten ([\d.]*\d) re-measured / in-run, the JIT designs ([\d.]*\d), the rest ([\d.]*\d)', t)
    rows.append(dict(seed=s, kind=kind, hours=f(r'seed %d (\d+)h' % s), gens=f(r'designs, generations 0-(\d+)'), designs=f(r'([\d,]+) designs, generations'),
                     ok=f(r'generations 0-\d+: ([\d,]+) ok'), one=f(r'([\d,]+) stopped after one round'), screened=f(r'([\d,]+) screened'),
                     hour=f(r'([\d,]+) designs an hour'), one_audit=num(one.group(2)) if one else None, one_front=int(one.group(3)) if one else None,
                     scr_audit=int(scr.group(1)) if scr else None, scr_front=int(scr.group(2)) if scr else None,
                     fast10=float(fe.group(1)) if fe else None, fastjit=float(fe.group(2)) if fe else None, fastrest=float(fe.group(3)) if fe else None,
                     heldout=f(r'Spearman with the selection speed ([\d.]*\d)', float) or f(r"sieve's Spearman ([\d.]*\d)", float), front=r['front'], hv=r['hv'], fastest=r['fastest'],
                     fastest32=r['fastest32'], smallest=r['smallest'], memory=r['memory']))
print('## The runs from seed 77 (the ledger\'s true fronts; each results file\'s counts)\n')
print('Speeds are against the hand-made s6 of the same commit (lower is faster); hv the hypervolume in the fixed box.\n')
print('| seed | kind | hours | generations | designs | an hour | ok | stopped after one round | screened | true front | hv | fastest | fastest 32-bit | smallest bytes | memory KB |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for x in rows:
    print('| %d | %s | %s | %s | %s | %s | %s | %s | %s | %d | %.4f | %.4f | %.4f | %s | %d |' % (x['seed'], x['kind'], x['hours'], x['gens'],
          c(x['designs']), c(x['hour']), c(x['ok']), c(x['one']), c(x['screened']),
          x['front'], x['hv'], x['fastest'], x['fastest32'], format(x['smallest'], ','), x['memory']))
S = [x for x in rows if x['kind'] == 'series']
rng = lambda k, fmt='%.4f': '%s (%s-%s)' % (fmt % med([x[k] for x in S]), fmt % min(x[k] for x in S), fmt % max(x[k] for x in S))
print('\n**The series** (seeds %d-%d, %d runs, the rule\'s): median (range) - hours %s; generations %s; designs %s; true front %s; hv %s; '
      'fastest %s; fastest 32-bit %s; smallest %s bytes; memory %s KB.\n' % (S[0]['seed'], S[-1]['seed'], len(S), rng('hours', '%d'), rng('gens', '%d'),
      rng('designs', '%d'), rng('front', '%d'), rng('hv'), rng('fastest'), rng('fastest32'), rng('smallest', '%d'), rng('memory', '%d')))
print('## The shortcuts\' audits, and the checks (each results file)\n')
print('| seed | stopped after one round | of them audited in full | on the front | screened | of them audited | on the front | the fast ten re-measured / in-run | JIT | the rest | held out: Spearman |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for x in rows:
    print('| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (x['seed'], c(x['one']), x['one_audit'], x['one_front'],
          c(x['screened']), x['scr_audit'], x['scr_front'], x['fast10'], x['fastjit'], x['fastrest'], x['heldout']))
A = [x for x in rows if x['kind'] != 'random']
print('\nSeeds 77-86 but the random one: stopped after one round %s of %s designs; audited in full %s, on the front %d; screened %s, audited %d, on the front %d.\n' % (
      format(sum(x['one'] or 0 for x in A), ','), format(sum(x['designs'] for x in A), ','), format(sum(x['one_audit'] or 0 for x in A), ','),
      sum(x['one_front'] or 0 for x in A), format(sum(x['screened'] or 0 for x in A), ','), sum(x['scr_audit'] or 0 for x in A), sum(x['scr_front'] or 0 for x in A)))
sh = lambda k: [x[k] for x in S if x[k] is not None]
print('The series alone: stopped after one round %s of %s designs (%s-%s a run); audited in full %s, on the front %d; screened %s (%s-%s a run), '
      'audited and run in full %d, on the front %d; the fast ten re-measured / in-run %.3f-%.3f, the JIT designs %.3f-%.3f, the rest %.3f-%.3f; '
      'held out (sieve) Spearman %.3f-%.3f.\n' % (format(sum(sh('one')), ','), format(sum(sh('designs')), ','), format(min(sh('one')), ','), format(max(sh('one')), ','),
      format(sum(sh('one_audit')), ','), sum(sh('one_front')), format(sum(sh('screened')), ','), format(min(sh('screened')), ','), format(max(sh('screened')), ','),
      sum(sh('scr_audit')), sum(sh('scr_front')), min(sh('fast10')), max(sh('fast10')), min(sh('fastjit')), max(sh('fastjit')), min(sh('fastrest')), max(sh('fastrest')),
      min(sh('heldout')), max(sh('heldout'))))
R = [x for x in rows if x['kind'] == 'random']
if R:
    r = R[0]
    print('**The random baseline** (seed %d, %s hours, %d generations): hv %.4f - %.2f of the series\' median at their ends (%.4f); fastest %.4f '
          '(the series\' median %.4f), fastest 32-bit %.4f (%.4f), smallest %s bytes (%s), memory %d KB (%d); true front %d designs (%d).\n' % (
          r['seed'], r['hours'], r['gens'], r['hv'], r['hv'] / med([x['hv'] for x in S]), med([x['hv'] for x in S]), r['fastest'], med([x['fastest'] for x in S]),
          r['fastest32'], med([x['fastest32'] for x in S]), format(r['smallest'], ','), format(int(med([x['smallest'] for x in S])), ','), r['memory'],
          med([x['memory'] for x in S]), r['front'], med([x['front'] for x in S])))

# the final set
F = [json.loads(l) for l in open('results/final-set-chainsBCD-seed86.md') if l.startswith('{')]
ex = lambda k: min(F, key=lambda r: r[k])
print('## The final set (results/final-set-chainsBCD-seed86.md - the laptop alone, every session\'s geometric mean)\n')
print('%d designs. Fastest %s %.4f (%.2f times s6\'s speed); fastest at 32 bits %s %.4f; smallest %s %s bytes; least memory %s %d KB.\n' % (
      len(F), ex('speed')['id'], ex('speed')['speed'], 1 / ex('speed')['speed'], ex('speed32')['id'], ex('speed32')['speed32'],
      ex('total')['id'], format(ex('total')['total'], ','), ex('rss')['id'], ex('rss')['rss']))

# across machines: each host's sessions pooled (geometric mean a design), against the laptop's pooled alone
sess = sorted(glob.glob('results/chainD-seed86/s[0-9]*'), key=lambda p: int(re.search(r's(\d+)$', p).group(1))) + ['results/chainB-seed86', 'results/chainC-seed86']
ids = [json.loads(l)['id'] for l in open('results/shortlist-seed86.md') if l.startswith('{')]
lap = {}
for d in sess:
    p = os.path.join(d, 'loadtest.md')
    if os.path.exists(p):
        for l in open(p):
            if l.startswith('{"id"'):
                j = json.loads(l)
                for k in ('idle', 'idle32'):
                    if j.get(k): lap.setdefault((k, j['id']), []).append(j[k])
host = {}
for d in sess:
    for f in glob.glob(os.path.join(d, '*.out.json')):
        h = os.path.basename(f)[:-9]
        for x in json.load(open(f))['designs']:
            if x.get('speed_here') and x['id'] in ids: host.setdefault(h, {}).setdefault(x['id'], []).append(x['speed_here'])


def sp(a, b):
    k = [i for i in ids if i in a and i in b]
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for n, i in enumerate(o): r[i] = n
        return r
    ra, rb = rank([a[i] for i in k]), rank([b[i] for i in k]); n = len(k)
    return 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (n * (n * n - 1))


L64 = {i: gm(lap[('idle', i)]) for i in ids if ('idle', i) in lap}; L32 = {i: gm(lap[('idle32', i)]) for i in ids if ('idle32', i) in lap}
lf = min(L64, key=L64.get)
print('## Across machines (the shortlist\'s 40; every session pooled - chains B, C, D)\n')
print('The laptop\'s fastest alone at 64 bits: %s.\n' % lf)
print('| host | sessions | Spearman with the laptop alone, pooled | its fastest | the laptop\'s fastest there, behind it |')
print('|---|---|---|---|---|')
for h, d in sorted(host.items()):
    P = {i: gm(v) for i, v in d.items()}; best = min(P, key=P.get); ref = L32 if 'prebuilt32' in h or 'arm' in h else L64
    print('| %s | %d | %.3f | %s %.4f | %+.1f%% |' % (h, max(len(v) for v in d.values()), sp(P, ref), best, P[best], (P[lf] / P[best] - 1) * 100))
