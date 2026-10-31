#!/usr/bin/env python3
"""lab/evolve/final-pick.py CANDIDATES.md LOADTEST.md [HOST.json ...] [--k 10] [--json OUT] | --self-test - GOALS.md step 3
after the re-measures (Iteration 573, the owner's decisions: the extremes chosen only after re-measurement; no design
dropped on one noisy number).

CANDIDATES.md: final-set.py --candidates (one record a line, in-run numbers). LOADTEST.md: loadtest.py --ids's output on
the laptop (its JSON lines: idle and loaded, at 64 and 32 bits). HOST.json: xcheck.py's out.json from a host (dream, the
Tegra), its designs asked for by id (--also @CANDIDATES).
  1. Each candidate's two speeds replaced by the laptop's re-measures - alone (idle) and, as a second reading, under load;
     size and memory are exact, kept. A candidate without a re-measure at a width (it failed there) cannot be compared
     re-measured against re-measured: left out of the choice and NAMED, never dropped silently.
  2. final-set.py's select() on the re-measured candidates alone - never a re-measure against another design's in-run
     number, which is optimistic at the fast end: the four extremes, then the set by hypervolume in the fixed box, to K.
  3. The set by both readings; a design in one and not the other named - both stay candidates for the owner.
  4. Each host: its fastest of the candidates it measured, named (the fast end as a band across machines, the fastest
     named per machine - GOALS.md); Spearman between its speeds and the laptop's alone; a design among a host's fastest
     five but not in the set FLAGGED - kept on the list.
stdout: markdown. --json OUT: the set (alone), one record a line, the re-measured speeds in and the in-run ones kept as
inrun / inrun32. --self-test: synthetic candidates, known answers.
"""
import importlib.util, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hv
_s = importlib.util.spec_from_file_location('final_set', os.path.join(HERE, 'final-set.py')); FS = importlib.util.module_from_spec(_s); _s.loader.exec_module(FS)


def records(f):
    """The JSON lines of a file that carry an id."""
    out = {}
    for l in open(f, errors='replace'):
        if l.startswith('{"'):
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('id'): out[r['id']] = r
    return out


def remeasured(C, L, key, key32):
    """-> (records with the re-measured speeds, {id: why left out})."""
    R, out = {}, {}
    for i, r in C.items():
        m = L.get(i)
        if not m: out[i] = 'not re-measured'; continue
        if not m.get(key): out[i] = 'no re-measure at 64 bits'; continue
        if not m.get(key32): out[i] = 'no re-measure at 32 bits'; continue
        R[i] = dict(r, speed=m[key], speed32=m[key32], inrun=r.get('speed'), inrun32=r.get('speed32'))
    return R, out


def spearman(a, b):
    """Rank correlation of two equal-length lists (average ranks for ties)."""
    def rank(x):
        o = sorted(range(len(x)), key=lambda k: x[k]); r = [0.0] * len(x); k = 0
        while k < len(o):
            j = k
            while j + 1 < len(o) and x[o[j + 1]] == x[o[k]]: j += 1
            for t in range(k, j + 1): r[o[t]] = (k + j) / 2.0
            k = j + 1
        return r
    ra, rb = rank(a), rank(b); n = len(a)
    if n < 3: return None
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((p - ma) * (q - mb) for p, q in zip(ra, rb)); den = math.sqrt(sum((p - ma) ** 2 for p in ra) * sum((q - mb) ** 2 for q in rb))
    return num / den if den else None


def pick(C, L, hosts, E, b, k=10):
    """The whole choice -> dict(alone, loaded: select() results with their records; out: left out; hosts: per host)."""
    res = {}
    for name, key, key32 in (('alone', 'idle', 'idle32'), ('loaded', 'loaded', 'loaded32')):
        R, out = remeasured(C, L, key, key32)
        res[name] = (FS.select(R, E, b, k) if R else None, R, out)
    sa = {i for i, _, _ in res['alone'][0]['set']} if res['alone'][0] else set()
    H = []
    for h in hosts:
        d = [x for x in h.get('designs', []) if x.get('id') in C and x.get('speed_here')]
        ra = res['alone'][1]
        both = [x for x in d if x['id'] in ra]
        rho = spearman([x['speed_here'] for x in both], [ra[x['id']]['speed'] for x in both])
        fast = sorted(d, key=lambda x: (x['speed_here'], x['id']))
        H.append(dict(host=h.get('env', {}).get('host', '?'), cell=h.get('env', {}).get('cell', '?'), n=len(d), rho=rho, nboth=len(both),
                      fastest=fast[0] if fast else None, flagged=[x['id'] for x in fast[:5] if x['id'] not in sa]))
    return dict(alone=res['alone'], loaded=res['loaded'], hosts=H)


def self_test():
    sys.argv = ['x']; import evolve as E
    b = json.load(open(hv.BOUNDS)); ok = True
    def check(c, what):
        nonlocal ok
        if not c: ok = False; print('final-pick self-test: FAIL - %s' % what)
    def rec(i, s, t, m, w): return dict(id=i, status='ok', speed=s, total=t, size=t, rss=m, speed32=w, genome={})
    C = {r['id']: r for r in [rec('f1', 0.140, 40000, 200, 0.17), rec('f2', 0.142, 40000, 200, 0.17), rec('sm', 1.5, 14000, 120, 1.5),
                              rec('ln', 0.8, 16000, 108, 0.75), rec('mid', 0.33, 23000, 124, 0.34), rec('bad', 0.2, 30000, 150, 0.2)]}
    L = {i: dict(id=i, idle=r['speed'], loaded=r['speed'], idle32=r['speed32'], loaded32=r['speed32']) for i, r in C.items()}
    L['f1'] = dict(L['f1'], idle=0.152, loaded=0.150)           # the in-run fastest re-measures 8.6% slower: f2 the fastest
    L['f2'] = dict(L['f2'], idle=0.146, loaded=0.151)           # and under load f1 again
    L['bad'] = dict(L['bad'], idle32=None)                       # failed at 32 bits: out, named
    p = pick(C, L, [dict(env=dict(host='h', cell=8), designs=[dict(id=i, speed_here=v) for i, v in
              (('f1', 0.20), ('f2', 0.21), ('mid', 0.15), ('sm', 2.0), ('ln', 1.0))])], E, b, k=6)
    sa = p['alone'][0]['set']; sl = p['loaded'][0]['set']
    check(sa[0][0] == 'f2' and sa[0][1].startswith('fastest'), 'alone, the fastest by re-measure: %s' % sa[:1])
    check(sl[0][0] == 'f1', 'under load, the other: %s' % sl[:1])
    check(p['alone'][2] == {'bad': 'no re-measure at 32 bits'}, 'a failed re-measure left out and named: %s' % p['alone'][2])
    h = p['hosts'][0]
    check(h['fastest']['id'] == 'mid' and h['n'] == 5, 'the host\'s fastest named: %s' % h['fastest'])
    check(all(i in [x[0] for x in sa] for i in ('sm', 'ln')), 'the smallest and the leanest in the set')
    check(abs(spearman([1, 2, 3, 4], [10, 20, 30, 40]) - 1) < 1e-12 and abs(spearman([1, 2, 3, 4], [4, 3, 2, 1]) + 1) < 1e-12, 'Spearman')
    print('final-pick self-test: the fastest by re-measure, the loaded reading, a failed re-measure named, a host\'s fastest, '
          'Spearman - %s' % ('pass' if ok else 'FAIL'))
    return 0 if ok else 1


def main(a):
    if a == ['--self-test']: return self_test()
    if len(a) < 2: sys.exit(__doc__)
    k, out = 10, None
    if '--k' in a: j = a.index('--k'); k = int(a[j + 1]); del a[j:j + 2]
    if '--json' in a: j = a.index('--json'); out = a[j + 1]; del a[j:j + 2]
    sys.argv = ['x']; import evolve as E
    b = json.load(open(hv.BOUNDS))
    C = {i: r for i, r in records(a[0]).items() if r.get('genome') is not None}; L = records(a[1])
    H = [json.load(open(f)) for f in a[2:]]
    p = pick(C, L, H, E, b, k)
    res, R, left = p['alone']
    print('# The final set, re-measured - %d candidates, %d re-measured at both widths (final-pick.py; GOALS.md step 3, '
          'the owner\'s decisions of Iteration 573)\n' % (len(C), len(R)))
    if not res: print('**Nothing re-measured - no choice.**'); return 1
    print('Chosen from the laptop\'s re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four '
          'extremes, then by hypervolume to %d. Size and memory exact.\n' % k)
    print('| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |')
    print('|---|---|---|---|---|---|---|---|---|')
    for n, (i, w, ad) in enumerate(res['set'], 1):
        r = R[i]; lo = L[i].get('loaded')
        print('| %d | %s | %s%s | %.4f (%.4f) | %s | %d | %.4f (%.4f) | %s | %.5f |' % (
            n, i, w, ', the knee' if i == res['knee'] else '', r['speed'], r['inrun'], format(r['total'], ','), r['rss'], r['speed32'],
            r['inrun32'] or 0, '%.3f' % (lo / r['speed']) if lo else '-', ad))
    ins = {i for i, _, _ in res['set']}
    old = {i for i, rr in C.items() if any(str(w).startswith('the set') for w in rr.get('why', []))}
    print('\nAgainst the in-run set: %s.' % ('the same designs' if old == ins else 'in now %s; out now %s - both kept as candidates' % (
        ', '.join(sorted(ins - old)) or 'none', ', '.join(sorted(old - ins)) or 'none')))
    rl = p['loaded'][0]
    if rl:
        il = {i for i, _, _ in rl['set']}
        ex = lambda s: [(x[1], x[0]) for x in s['set'][:4]]
        print('Under load: %s.' % ('the same set and extremes' if il == ins and ex(rl) == ex(res) else
              'the extremes %s; in the set under load only %s, alone only %s' % ('; '.join('%s %s' % e for e in ex(rl)),
              ', '.join(sorted(il - ins)) or 'none', ', '.join(sorted(ins - il)) or 'none')))
    if left: print('\nLeft out of the choice, kept on the list: %s.' % '; '.join('%s - %s' % x for x in sorted(left.items())))
    for h in p['hosts']:
        f = h['fastest']
        print('\n%s (%s-byte cells): %d candidates measured; its fastest %s; Spearman with the laptop alone %s over %d%s.' % (
            h['host'], h['cell'], h['n'], '%s %.3f' % (f['id'], f['speed_here']) if f else 'none',
            '%.3f' % h['rho'] if h['rho'] is not None else '-', h['nboth'],
            '; FLAGGED, among its fastest five and not in the set: %s' % ', '.join(h['flagged']) if h['flagged'] else ''))
    if out:
        with open(out, 'w') as o:
            for i, w, ad in res['set']: o.write(json.dumps(dict(R[i], why=w, adds=ad), sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
