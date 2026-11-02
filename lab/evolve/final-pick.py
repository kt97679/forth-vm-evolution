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
  5. Across machines (GOALS.md, Iteration 377; the owner's terms at 576 - lose no good design): each candidate's speed in
     three classes, each class once - x86-64 (the laptop alone and every 8-byte x86 host, their geometric mean), x86 at 32
     bits (the laptop's 32-bit alone and every 4-byte x86 host), ARMv7 (the Tegra; a JIT design there is its own genome
     with the JIT off - ARMv7 has no JIT, so that is the design as it builds there; marked). The mean: their geometric
     mean. The veto (--veto, 25%) removes nothing - it only decides which design is named the generic pick: the best
     mean within the margin of every class's best; the best mean if vetoed is named beside it. ADDED to the set (never
     taken out): the --top 3 best means and each class's fastest, when the laptop's set lacks them.
stdout: markdown. --json OUT: the set (alone), one record a line, the re-measured speeds in and the in-run ones kept as
inrun / inrun32. --self-test: synthetic candidates, known answers.
--also-session DIR (Iteration 588; repeatable): another session's readings beside these - DIR's loadtest.md merged
into the laptop's (each speed the geometric mean of the sessions that have it; a reading one session lacks does not count
against the design - lose no good design), DIR's *.out.json added to the hosts (step 5 takes each host's mean; step 4
names each line). Chain C's processing: --also-session results/chainB-seed86.
"""
import glob, importlib.util, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
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


def merge_sessions(Ls):
    """Iteration 588: the laptop's re-measures from several sessions -> one record an id: each speed the geometric mean
    of the sessions that have it (a failed reading in one does not count against the design), sessions = how many."""
    by = {}
    for L in Ls:
        for i, r in L.items(): by.setdefault(i, []).append(r)
    M = {}
    for i, rs in by.items():
        m = dict(rs[0], sessions=len(rs))
        for k in ('idle', 'loaded', 'idle32', 'loaded32'):
            v = [r[k] for r in rs if r.get(k)]
            m[k] = math.exp(sum(math.log(t) for t in v) / len(v)) if v else None
        M[i] = m
    return M


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


def hostkey(h):
    """Iteration 585: the laptop's speed a host is ranked against - its own width (4-byte cells: speed32). It read the
    64-bit for every host: chain A's dream-32 Spearman -0.183 was +0.588 at its width."""
    return 'speed32' if h.get('env', {}).get('cell') == 4 else 'speed'


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


CLASSES = ('x86-64', 'x86-32', 'ARMv7')


def klass(env):
    """A host's class from its out.json env: ARM by the machine, else the width by the cell (Iteration 331: measured)."""
    m = str(env.get('machine', ''))
    if m.startswith('arm') or m.startswith('aarch'): return 'ARMv7'
    return 'x86-32' if env.get('cell') == 4 else 'x86-64'


def across(R, hosts, isjit, inset, veto=0.25, top=3):
    """Step 5 -> dict(rows, present, best, pick, topmean, fastest, twin, added). R: the laptop's re-measured candidates
    (speed, speed32 - alone); hosts: out.json dicts; isjit(id): the design has the JIT (its ARMv7 reading is the JIT-off
    build); inset: the laptop's set. A design missing a class is ranked on those it has, marked partial, kept."""
    per = {i: {'x86-64': {'the laptop': [r['speed']]}, 'x86-32': {'the laptop': [r['speed32']]}, 'ARMv7': {}} for i, r in R.items()}
    twin = set(); src = {'x86-64': ['the laptop'], 'x86-32': ['the laptop'], 'ARMv7': []}
    for h in hosts:
        k = klass(h.get('env', {})); hn = h.get('env', {}).get('host', '?')
        for x in h.get('designs', []):
            i, v = x.get('id'), x.get('speed_here')
            if i in per and v:
                per[i][k].setdefault(hn, []).append(v)           # each host once in its class (dream's two 8-byte lines)
                if hn not in src[k]: src[k].append(hn)
                if k == 'ARMv7' and isjit(i): twin.add(i)
    gm = lambda v: math.exp(sum(math.log(t) for t in v) / len(v))
    cls = {i: {k: gm([gm(v) for v in hr.values()]) for k, hr in d.items() if hr} for i, d in per.items()}
    present = [k for k in CLASSES if any(k in c for c in cls.values())]
    best = {k: min(c[k] for c in cls.values() if k in c) for k in present}
    rows = []
    for i, c in cls.items():
        behind = {k: c[k] / best[k] - 1 for k in present if k in c}
        rows.append(dict(id=i, cls=c, mean=gm([c[k] for k in present if k in c]), full=all(k in c for k in present),
                         behind=behind, vetoed=[k for k in present if behind.get(k, 0) > veto]))
    rows.sort(key=lambda r: (not r['full'], r['mean'], r['id']))
    full = [r for r in rows if r['full']]
    pk = next((r for r in full if not r['vetoed']), None)
    fastest = {k: min((r for r in rows if k in r['cls']), key=lambda r: (r['cls'][k], r['id']))['id'] for k in present}
    added = []
    for n, r in enumerate(full[:top], 1):
        if r['id'] not in inset: added.append((r['id'], 'across machines: the best mean #%d' % n))
    for k in present:
        i = fastest[k]
        if i not in inset and i not in [a for a, _ in added]: added.append((i, 'across machines: the fastest at %s' % k))
    return dict(rows=rows, present=present, best=best, pick=pk, topmean=full[0] if full else None, fastest=fastest,
                twin=twin, added=added, veto=veto, src=src)


def pick(C, L, hosts, E, b, k=10, veto=0.25, top=3):
    """The whole choice -> dict(alone, loaded: select() results with their records; out: left out; hosts: per host)."""
    res = {}
    for name, key, key32 in (('alone', 'idle', 'idle32'), ('loaded', 'loaded', 'loaded32')):
        R, out = remeasured(C, L, key, key32)
        res[name] = (FS.select(R, E, b, k) if R else None, R, out)
    sa = {i for i, _, _ in res['alone'][0]['set']} if res['alone'][0] else set()
    H = []
    for h in hosts:
        d = [x for x in h.get('designs', []) if x.get('id') in C and x.get('speed_here')]
        if not d: continue                                            # 585: a sample line - no candidate in it
        ra = res['alone'][1]
        both = [x for x in d if x['id'] in ra]
        rho = spearman([x['speed_here'] for x in both], [ra[x['id']][hostkey(h)] for x in both])
        fast = sorted(d, key=lambda x: (x['speed_here'], x['id']))
        H.append(dict(host=h.get('env', {}).get('host', '?'), cell=h.get('env', {}).get('cell', '?'), n=len(d), rho=rho, nboth=len(both),
                      fastest=fast[0] if fast else None, flagged=[x['id'] for x in fast[:5] if x['id'] not in sa]))
    A = None
    if res['alone'][0]:
        def isjit(i):
            g = C.get(i, {}).get('genome')
            return bool(g) and bool(E.express(E.canon(g)).get('jit'))
        A = across(res['alone'][1], hosts, isjit, sa, veto, top)
    return dict(alone=res['alone'], loaded=res['loaded'], hosts=H, across=A)


def shortlist(p, E, b, n=40, fast=5):
    """580 (the owner, 579: the final pick in two chains): chain A's laptop re-measures narrowed to the designs chain B
    asks dream and the Tegra for, beside the laptop's second re-measure. In order, none dropped for n: the set alone,
    the set loaded, step 5's additions, each width's `fast` fastest alone and loaded; then the alone set's greedy
    continued (the next by hypervolume) up to n. -> [(id, why)]"""
    out, have = [], set()
    def add(i, w):
        if i not in have: have.add(i); out.append((i, w))
    for name in ('alone', 'loaded'):
        if p[name][0]:
            for i, w, _ in p[name][0]['set']: add(i, 'the set %s: %s' % (name, w))
    for i, w in (p['across']['added'] if p['across'] else []): add(i, w)
    for name in ('alone', 'loaded'):
        RR = p[name][1]
        for key, bits in (('speed', 64), ('speed32', 32)):
            for i in sorted(RR, key=lambda i: (RR[i][key], i))[:fast]: add(i, 'among the %d fastest %s at %d bits' % (fast, name, bits))
    R = p['alone'][1]
    if R and len(out) < n:
        for i, w, _ in FS.select(R, E, b, max(n, len(out)))['set']:
            if len(out) >= n: break
            add(i, 'next by hypervolume (%s)' % w)
    if R and len(out) < n:                         # the near-misses: off the front, closest to the fastest no larger
        def behind(i):
            t = E.ov(R[i], 'total'); return R[i]['speed'] / min(R[j]['speed'] for j in R if E.ov(R[j], 'total') <= t)
        for i in sorted((i for i in R if i not in have), key=lambda i: (behind(i), i))[:n - len(out)]:
            add(i, 'near the front: %.1f%% behind the fastest no larger' % ((behind(i) - 1) * 100))
    return out


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
    S = shortlist(p, E, b, 40); si = [i for i, _ in S]
    check(set(i for i, _, _ in p['alone'][0]['set']) <= set(si) and len(si) == len(set(si))
          and set(si) <= set(p['alone'][1]) | set(p['loaded'][1]), 'the shortlist holds the set, once each, each re-measured: %s' % si)
    check(len(shortlist(p, E, b, 1)) >= len(p['alone'][0]['set']), 'the shortlist drops none of the set for n')
    # 576: across machines - a laptop specialist (spec: fastest here, 38% behind on ARMv7) the best mean but vetoed; gen,
    # good everywhere, the generic pick; arm1, the Tegra's fastest, outside the set: ADDED; partial: no ARMv7 reading, kept
    Rx = {i: dict(speed=a, speed32=b_) for i, a, b_ in (('spec', 0.110, 0.130), ('gen', 0.135, 0.160), ('f2', 0.146, 0.170),
                                                         ('arm1', 0.200, 0.240), ('partial', 0.140, 0.165))}
    hx = [dict(env=dict(host='d', machine='x86_64', cell=8), designs=[dict(id=i, speed_here=v) for i, v in (('spec', 0.110), ('gen', 0.135), ('f2', 0.146), ('arm1', 0.200), ('partial', 0.140))]),
          dict(env=dict(host='d', machine='x86_64', cell=4), designs=[dict(id=i, speed_here=v) for i, v in (('spec', 0.130), ('gen', 0.160), ('f2', 0.170), ('arm1', 0.240))]),
          dict(env=dict(host='r', machine='armv7l', cell=4), designs=[dict(id=i, speed_here=v) for i, v in (('spec', 0.40), ('gen', 0.30), ('f2', 0.50), ('arm1', 0.29))])]
    A = across(Rx, hx, lambda i: i == 'f2', {'spec', 'gen', 'f2'}, 0.25, 3)
    check(A['topmean']['id'] == 'spec' and A['topmean']['vetoed'] == ['ARMv7'], 'the specialist the best mean, vetoed at ARMv7: %s' % A['topmean'])
    check(A['pick']['id'] == 'gen', 'the design good everywhere the generic pick: %s' % (A['pick'] or {}).get('id'))
    check(('arm1', 'across machines: the fastest at ARMv7') in A['added'] and A['fastest']['ARMv7'] == 'arm1', 'the Tegra\'s fastest ADDED: %s' % A['added'])
    check(not [r for r in A['rows'] if r['id'] == 'partial'][0]['full'] and 'partial' in [r['id'] for r in A['rows']], 'a design without an ARMv7 reading kept, partial')
    check(A['twin'] == {'f2'} and klass(dict(machine='armv7l', cell=4)) == 'ARMv7' and klass(dict(machine='x86_64', cell=4)) == 'x86-32', 'the JIT-off twin marked; the classes')
    check(len(A['rows']) == 5, 'nothing removed by the veto')
    check(hostkey(dict(env=dict(cell=4))) == 'speed32' and hostkey(dict(env=dict(cell=8))) == 'speed' and hostkey({}) == 'speed', 'a host at its own width (585)')
    check(abs(spearman([1, 2, 3, 4], [10, 20, 30, 40]) - 1) < 1e-12 and abs(spearman([1, 2, 3, 4], [4, 3, 2, 1]) + 1) < 1e-12, 'Spearman')
    M = merge_sessions([{'a': dict(id='a', idle=0.10, loaded=0.2, idle32=None, loaded32=0.3)},
                        {'a': dict(id='a', idle=0.40, loaded=0.2, idle32=0.5, loaded32=0.3), 'b': dict(id='b', idle=0.1, loaded=0.1, idle32=0.1, loaded32=0.1)}])
    check(abs(M['a']['idle'] - 0.2) < 1e-12 and M['a']['idle32'] == 0.5 and M['a']['sessions'] == 2 and M['b']['sessions'] == 1,
          'two sessions merged - the geometric mean, a failed reading not counted (588): %s' % M)
    print('final-pick self-test: the fastest by re-measure, the loaded reading, a failed re-measure named, a host\'s fastest, '
          'Spearman; across machines - the veto, the pick, the additions; the shortlist - %s' % ('pass' if ok else 'FAIL'))
    return 0 if ok else 1


def main(a):
    if a == ['--self-test']: return self_test()
    if len(a) < 2: sys.exit(__doc__)
    k, out = 10, None
    if '--k' in a: j = a.index('--k'); k = int(a[j + 1]); del a[j:j + 2]
    if '--json' in a: j = a.index('--json'); out = a[j + 1]; del a[j:j + 2]
    veto, top = 0.25, 3
    if '--veto' in a: j = a.index('--veto'); veto = float(a[j + 1]); del a[j:j + 2]
    if '--top' in a: j = a.index('--top'); top = int(a[j + 1]); del a[j:j + 2]
    sl, sn = None, 40
    if '--shortlist' in a: j = a.index('--shortlist'); sl = a[j + 1]; del a[j:j + 2]
    if '--n' in a: j = a.index('--n'); sn = int(a[j + 1]); del a[j:j + 2]
    also = []
    while '--also-session' in a: j = a.index('--also-session'); also.append(a[j + 1]); del a[j:j + 2]
    sys.argv = ['x']; import evolve as E
    b = json.load(open(hv.BOUNDS))
    C = {i: r for i, r in records(a[0]).items() if r.get('genome') is not None}; L = records(a[1])
    H = [json.load(open(f)) for f in a[2:]]
    if also:                                             # Iteration 588: another session's readings beside these
        L = merge_sessions([L] + [records(os.path.join(d, 'loadtest.md')) for d in also])
        H += [json.load(open(f)) for d in also for f in sorted(glob.glob(os.path.join(d, '*.out.json')))]
    p = pick(C, L, H, E, b, k, veto, top)
    res, R, left = p['alone']
    print('# The final set, re-measured - %d candidates, %d re-measured at both widths (final-pick.py; GOALS.md step 3, '
          'the owner\'s decisions of Iteration 573)\n' % (len(C), len(R)))
    if also: print('Two or more sessions (Iteration 588): this one and %s - the laptop\'s re-measures each the geometric mean of the '
                   'sessions that have it; each host\'s lines its mean in step 5, each named in step 4.\n' % ', '.join(also))
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
    A = p['across']
    if A:
        print('\n## Across machines (GOALS.md, Iteration 377; the owner\'s terms at 576)\n')
        print('Each class once - %s; the mean their geometric mean (lower is faster). %s The veto (%d%%) removes nothing: it '
              'names the generic pick only.\n' % (', '.join('%s (%s)' % (k, ', '.join(A['src'][k])) for k in A['present']), 'A JIT design\'s ARMv7 reading is its JIT-off build (*).'
              if 'ARMv7' in A['present'] else 'No ARMv7 reading - two classes.', round(A['veto'] * 100)))
        print('| # | design | %s | mean | behind its class\'s best | in the set |' % ' | '.join(A['present']))
        print('|---|---|%s---|---|---|' % ('---|' * len(A['present'])))
        ins = {i for i, _, _ in res['set']}; addi = dict(A['added'])
        shown = A['rows'][:12] + [r for r in A['rows'][12:] if r['id'] in ins or r['id'] in addi]
        for n, r in enumerate(shown, 1):
            print('| %d | %s | %s | %.4f%s | %s | %s |' % (n, r['id'], ' | '.join(
                ('%.4f%s' % (r['cls'][k], '*' if k == 'ARMv7' and r['id'] in A['twin'] else '')) if k in r['cls'] else '-' for k in A['present']),
                r['mean'], '' if r['full'] else ' (partial)', ', '.join('%s +%d%%' % (k, round(r['behind'][k] * 100)) for k in A['present']
                if r['behind'].get(k, 0) >= 0.005) or 'the best', 'yes' if r['id'] in ins else 'ADDED' if r['id'] in addi else '-'))
        pk, tm = A['pick'], A['topmean']
        print('\n**The generic pick**: %s.' % ('%s, the mean %.4f, within %d%% of every class\'s best' % (pk['id'], pk['mean'], round(A['veto'] * 100))
              if pk else 'none within the veto - the best mean %s named instead' % (tm['id'] if tm else '-')))
        if pk and tm and tm['id'] != pk['id']:
            print('The best mean, %s (%.4f), is vetoed - %s behind; NAMED, kept, the owner\'s to weigh.' % (
                tm['id'], tm['mean'], ', '.join('%s %d%%' % (k, round(tm['behind'][k] * 100)) for k in tm['vetoed'])))
        print('Each class\'s fastest: %s.' % '; '.join('%s %s' % (k, A['fastest'][k]) for k in A['present']))
        print('**Added to the set across machines** (never taken out): %s.' % ('; '.join('%s - %s' % x for x in A['added']) if A['added'] else 'none - the set holds them'))
    if sl and res:
        S = shortlist(p, E, b, sn)
        with open(sl, 'w') as o:
            o.write('# The final pick\'s shortlist - chain B\'s designs (final-pick.py --shortlist, Iteration 580)\n\n'
                    'From %s and the laptop\'s re-measures of chain A (%s): %d designs - the set alone and loaded, the additions '
                    'across machines, each width\'s %d fastest alone and loaded, then the next by hypervolume and the near-misses up to %d. Chain B: '
                    'NEXT-RUN `experiment loadtest.py --ids %s`, REMOTES `--also @%s` (dream, rage) - one record a line.\n\n'
                    % (os.path.basename(a[0]), os.path.basename(a[1]), len(S), 5, sn, os.path.relpath(sl, ROOT), os.path.relpath(sl, ROOT)))
            for i, w in S: o.write(json.dumps(dict(C[i], why=w), sort_keys=True) + '\n')
        print('\n**The shortlist for chain B**: %d designs in %s.' % (len(S), sl))
    if out:
        with open(out, 'w') as o:
            for i, w, ad in res['set']: o.write(json.dumps(dict(R[i], why=w, adds=ad), sort_keys=True) + '\n')
            for i, w in (A['added'] if A else []): o.write(json.dumps(dict(R[i], why=w, adds=0.0), sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
