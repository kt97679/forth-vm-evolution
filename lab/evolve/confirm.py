#!/usr/bin/env python3
"""lab/evolve/confirm.py DB --seed N [--ledger LEDGER] [--candidates FILE] [--pool FILE ...] | --pool-files N | --self-test - GOALS.md step 2, the confirmation
test, mechanical (Iteration 573, prepared while seed 84 ran; prompts/21, item 9: the arithmetic a script, the judgment the
chat's). The confirmation run (`seed N HOURS widths carryall`) against the method's last runs:

  1. The pool: the records of the series' results files ({"bin" lines - their fronts; default results/evolve-*-seedS.md
     for each run of the ledger's newest series before N: seeds 77-83), a design in several the last file's; its true
     front (hv.true_front) and that front's hypervolume in the fixed box - GOALS.md's "pooled true front".
  2. The run: its true front's hypervolume and its four extremes from every alive design (hv.measure; the series' way
     since 556), at its end - the pooled runs are taken at theirs, no matching by generation.
  3. Confirmed when the hypervolume is not 1% above the pool's and no extreme beats the series' best by its threshold -
     speed 2%, binary + image 1%, memory 4 KB, the 32-bit speed 2% (stopping.py's bar on the runs' ledger lines - their
     strict extremes - with the hypervolume's replaced by the pool's).
  4. What the run added: its front's designs carried in (evolve.py's how, 'carried from' or 'named, carried from')
     against bred; the pool and the run's front together - the front step 3 chooses from - their hypervolume.
  5. Each re-enabled gene's enrichment (lifted.py's LIFTED: the genes and the values they were frozen at): among the
     designs that express the gene (express(), as built), the share of the run's true front off the frozen value over
     the share of the children off it - the alive designs the run bred, generation 1 on (the founders are earlier fronts,
     selected already). The screen, fixed before seed 84 returned (573): REVISIT at an enrichment of 1.5 or more with 5
     or more designs of the front off the frozen value - "a gene well above 1 has its freeze revisited before anything is
     called final"; the chat judges. The fastest tenth's count a first look only.
--pool-files N: the default pool's files, one a line (process-seed.sh passes them to final-set.py with the run's database).
The owner's decisions of Iteration 573 (GOALS.md step 2), before seed 84 returned:
  6. A stricter criterion besides: the pool and the run's BRED front designs together 1% or more over the pool's
     hypervolume - not confirmed (the pool's numbers are the best of seven runs' in-run measures; the run re-times the
     carried designs once, so its own front leans to confirmed).
  7. What a gain means, by where it came from: bred designs (that criterion, an extreme by a bred design, or the
     hypervolume where the bred designs add more than the carried) - the search had more to find: NOT CONFIRMED - the
     search, another confirmation run pooled over the series and this run; carried designs only (earlier fronts outside
     the pool, re-timed) - NOT CONFIRMED - the pool widened: no new search, the pool widened. Either way every gaining
     design joins the final set's candidates; an extreme's gain stands only after its re-measure.
  8. The genes' classes, a gene never filtered out on one run's absence: REVISIT as above; KEEP - its other value on a
     candidate (--candidates: final-set.py's, the set and the bands), on an extreme, or in the fastest tenth of the run's
     or the pool's front; stays - its other value on a true front of any of the pooled runs or this one; retire
     candidate - on none of them: its other value's code, the gene fixed at its old value (consolidation's to decide).
stdout: markdown; the verdict in one line, "verdict: seed N CONFIRMED" or "verdict: seed N NOT CONFIRMED - ...". As the
build user (it imports the evolver). --self-test: synthetic records, known answers."""
import ast, glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import hv, stopping
SCREEN = (1.5, 5)
CARRIED = ('carried from', 'named, carried from')


def lifted_genes():
    """lifted.py's LIFTED, read - one place for the genes and their old values (lifted.py runs as it is imported)."""
    m = re.search(r'^LIFTED = (\{.*\})$', open(os.path.join(HERE, 'lifted.py')).read(), re.M)
    return ast.literal_eval(m.group(1))


def front_hv(R, E, b):
    F = hv.true_front(R, E)
    return F, hv.hv4([z for z in (hv.norm(R[i], b) for i in F) if z is not None])


def judge(run, pool_hv, runs):
    """run: the hypervolume and the four extremes; runs: the series' ledger lines. -> (the bar, the criteria gained)."""
    b = stopping.bar([dict(r, hv=pool_hv) for r in runs])
    return b, [k for k in stopping.KEYS if (run[k] >= b[k] if k == 'hv' else run[k] <= b[k])]


def enrichment(front, children, val, frozen):
    """-> (front expressing, front off the frozen value, children expressing, children off, enrichment or None)."""
    fe = [i for i in front if val(i) != 'n/e']; fo = [i for i in fe if val(i) != frozen]
    ce = [i for i in children if val(i) != 'n/e']; co = [i for i in ce if val(i) != frozen]
    return len(fe), len(fo), len(ce), len(co), ((len(fo) / len(fe)) / (len(co) / len(ce)) if fe and co else None)


def origin(gains, ids, bredgain, carriedgain, bred):
    """573: the gained criteria by where they came from -> 'search' (any bred), 'pool' (carried only) or None.
    gains: the criteria the run's own numbers gained; ids: the extreme designs by criterion; bredgain, carriedgain: the
    pool's hypervolume increase from the run's bred and carried front designs; bred(i): a bred design."""
    src = []
    for k in gains:
        if k == 'bred': continue
        if k == 'hv': src.append('search' if bredgain >= carriedgain else 'pool')
        else: src.append('search' if bred(ids[k]) else 'pool')
    if 'bred' in gains or 'search' in src: return 'search'
    return 'pool' if src else None


def screened(fo, en):
    return en is not None and en >= SCREEN[0] and fo >= SCREEN[1]


def self_test():
    sys.argv = ['x']; import evolve as E
    b = json.load(open(hv.BOUNDS)); ok = True
    def rec(i, s, t, m, w, how='mutation'): return dict(id=i, status='ok', speed=s, total=t, size=t, rss=m, speed32=w, how=how, gen=1)
    def check(c, what):
        nonlocal ok
        if not c: ok = False; print('confirm self-test: FAIL - %s' % what)
    P = {r['id']: r for r in [rec('a', 0.15, 30000, 150, 0.17), rec('b', 0.3, 15000, 140, 0.3), rec('c', 0.5, 20000, 110, 0.5)]}
    F, ph = front_hv(P, E, b)
    led = [dict(seed=1, hv=ph * 0.95, fastest=0.15, smallest=15000, memory=110, fastest32=0.17)]
    m = lambda R: (lambda F, h: dict(hv=h, fastest=min(R[i]['speed'] for i in R), smallest=min(R[i]['total'] for i in R),
                                     memory=min(R[i]['rss'] for i in R), fastest32=min(R[i]['speed32'] for i in R)))(*front_hv(R, E, b))
    check(judge(m(P), ph, led)[1] == [], 'the pool itself again: nothing gained')
    Q = dict(P, d=rec('d', 0.145, 30000, 150, 0.17))                      # 3.3% faster: the speed extreme, not 2% more volume
    check('fastest' in judge(m(Q), ph, led)[1], 'a fastest 3%% better gains: %s' % judge(m(Q), ph, led)[1])
    Q = dict(P, d=rec('d', 0.149, 30000, 150, 0.17))                      # under 2%: no extreme
    check('fastest' not in judge(m(Q), ph, led)[1], 'a fastest under 2% better gains nothing by the speed')
    Q = dict(P, d=rec('d', 0.2, 16000, 115, 0.2))                         # a new middle design: volume, no extreme
    check(judge(m(Q), ph, led)[1] == ['hv'], 'a design in the middle gains by the hypervolume alone: %s' % judge(m(Q), ph, led)[1])
    V = dict(f1=1, f2=1, f3=0, f4='n/e', c1=0, c2=0, c3=0, c4=1, c5='n/e')   # front 2 of 3 off 0; children 1 of 4
    e = enrichment(['f1', 'f2', 'f3', 'f4'], ['c1', 'c2', 'c3', 'c4', 'c5'], V.get, 0)
    check(e[:4] == (3, 2, 4, 1) and abs(e[4] - (2 / 3) / (1 / 4)) < 1e-12, 'the enrichment among the expressing: %s' % (e,))
    check(enrichment(['f1'], ['c1'], V.get, 0)[4] is None, 'no child off the frozen value: no enrichment')
    br = lambda i: i.startswith('b')
    check(origin([], {}, 0, 0, br) is None, 'nothing gained: no origin')
    check(origin(['fastest'], {'fastest': 'c1'}, 0, 0, br) == 'pool' and origin(['fastest'], {'fastest': 'b1'}, 0, 0, br) == 'search',
          'an extreme by where its design came from')
    check(origin(['hv'], {}, 0.01, 0.02, br) == 'pool' and origin(['hv'], {}, 0.02, 0.02, br) == 'search', 'the hypervolume by the larger part, a tie the search')
    check(origin(['bred', 'smallest'], {'smallest': 'c1'}, 0.02, 0, br) == 'search', 'the bred criterion is the search')
    check(screened(5, 1.5) and not screened(4, 3.0) and not screened(9, 1.49), 'the screen at 1.5 and 5 designs')
    check(set(lifted_genes()) == {'bytehdr', 'doesfar', 'thinhdr', 'varcall', 'bss', 'lean', 'msc', 'scale', 'sharedcall', 'alignhot'},
          'the ten re-enabled genes (GOALS.md step 2)')
    print('confirm self-test: the pool again, the speed extreme either side of 2%%, a gain by volume alone, the enrichment, '
          'the origins, the screen, the genes - %s' % ('pass' if ok else 'FAIL'))
    return 0 if ok else 1


def pool_files(runs):
    miss = [r['seed'] for r in runs if not glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed%d.md' % r['seed']))]
    if miss: sys.exit('confirm.py: no results file for seeds %s' % miss)
    return [sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed%d.md' % r['seed'])))[0] for r in runs]


def main(a):
    opt = lambda k: a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else None
    if a == ['--self-test']: return self_test()
    if opt('--pool-files'):
        print('\n'.join(pool_files([r for r in stopping.series(opt('--ledger') or stopping.LEDGER)[1] if r['seed'] < int(opt('--pool-files'))])))
        return 0
    if opt('--seed') is None: sys.exit(__doc__)
    N = int(opt('--seed')); led = opt('--ledger') or stopping.LEDGER
    pool = a[a.index('--pool') + 1:] if '--pool' in a else []          # --pool last: every file after it
    db = next(x for x in (a[:a.index('--pool')] if pool else a) if not x.startswith('--') and x not in (opt('--seed'), opt('--ledger')))
    sys.argv = ['x']; import evolve as E
    b = json.load(open(hv.BOUNDS)); method, runs = stopping.series(led); runs = [r for r in runs if r['seed'] < N]
    pool = pool or pool_files(runs)
    P = {}
    for f in pool: P.update(hv.load(f, E))
    PF, ph = front_hv(P, E, b)
    R = hv.load(db, E); m = hv.measure(db, E, b, R=R); x = m['alive']
    run = dict(hv=m['hv'], fastest=x['fastest'], smallest=x['smallest'], memory=x['memory'], fastest32=x['fastest32'])
    bar, g = judge(run, ph, runs)
    T = hv.true_front(R, E)
    car = [i for i in T if str(R[i].get('how', '')).startswith(CARRIED)]; bred = [i for i in T if i not in car]
    isbred = lambda i: not str(R[i].get('how', '')).startswith(CARRIED)
    def with_(ids):
        U = dict(P); U.update({i: R[i] for i in ids}); return front_hv(U, E, b)
    UF, uh = with_(T); hb = with_(bred)[1]; hc = with_(car)[1]
    if hb >= ph * 1.01: g = g + ['bred']                                    # 573: the stricter criterion
    A = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss') and r.get('speed32')]
    xid = {k: min(A, key=lambda i: (R[i][f], i)) for k, f in (('fastest', 'speed'), ('smallest', 'total'), ('memory', 'rss'), ('fastest32', 'speed32'))}
    org = origin(g, xid, hb - ph, hc - ph, isbred)
    sd = ', '.join(str(r['seed']) for r in runs)
    print('# The confirmation test - seed %d against the pooled true front of seeds %s (confirm.py; GOALS.md step 2)\n' % (N, sd))
    print('The pool: %d records of %d results files (%s); its true front %d designs, hypervolume %.5f - the bar %.5f (1%% over).'
          % (len(P), len(pool), ', '.join(os.path.basename(f) for f in pool), len(PF), ph, bar['hv']))
    print('Seed %d: %d records, its true front %d (%d inside the box), hypervolume %.5f - %+.1f%% against the pool\'s.\n'
          % (N, len(R), m['front'], m['inside'], m['hv'], 100 * (m['hv'] / ph - 1)))
    print('| criterion | seed %d | the series\' best | the bar | gained |' % N); print('|---|---|---|---|---|')
    best = lambda k: (min if k != 'hv' else max)(runs, key=lambda r: r[k])
    for k in stopping.KEYS:
        bv, bs = (ph, 'the pool') if k == 'hv' else (best(k)[k], 'seed %d' % best(k)['seed'])
        print('| %s | %s | %s (%s) | %s | %s |' % (stopping.NAME[k], stopping.fmt(k, run[k]), stopping.fmt(k, bv), bs,
                                                 stopping.fmt(k, bar[k]), 'YES' if k in g else 'no'))
    print('| the pool and its bred front designs (573) | %.5f | %.5f (the pool) | %.5f | %s |' % (hb, ph, ph * 1.01, 'YES' if 'bred' in g else 'no'))
    nm = lambda k: 'the pool and its bred designs' if k == 'bred' else '%s (%s, %s)' % (stopping.NAME[k], 'its front' if k == 'hv' else xid[k],
                                                                                      'bred' if (k == 'hv' and hb - ph >= hc - ph) or (k != 'hv' and isbred(xid[k])) else 'carried')
    ext = ' - the extremes\' gains stand only after their re-measure (step 3\'s candidates)' if set(g) - {'hv', 'bred'} else ''
    print('\nverdict: seed %d %s' % (N, 'CONFIRMED - the hypervolume not 1% over the pool\'s, no extreme by its threshold, the bred designs adding under 1%' if not g
          else 'NOT CONFIRMED - the search: gained by %s; next: another confirmation run pooled over the series and seed %d (GOALS.md, 573)%s' % (', '.join(map(nm, g)), N, ext) if org == 'search'
          else 'NOT CONFIRMED - the pool widened: gained by %s, carried designs only; next: no new search - the pool widened, the gainers among the candidates (GOALS.md, 573)%s' % (', '.join(map(nm, g)), ext)))
    f0 = sum(1 for r in R.values() if str(r.get('how', '')).startswith(CARRIED))
    print('\nWhat it added: its front %d - %d carried in (of %d founders carried), %d bred%s. The pool and its front together: '
          'true front %d (%d of them seed %d\'s records), hypervolume %.5f, %+.1f%% over the pool\'s - the front step 3 chooses from; the bred designs alone %+.1f%%, the carried alone %+.1f%%.'
          % (len(T), len(car), f0, len(bred), ' (generations %d-%d)' % (min(R[i]['gen'] for i in bred), max(R[i]['gen'] for i in bred)) if bred else '',
             len(UF), sum(1 for i in UF if i in T), N, uh, 100 * (uh / ph - 1), 100 * (hb / ph - 1), 100 * (hc / ph - 1)))
    L = lifted_genes()
    C = [i for i, r in R.items() if (r.get('gen') or 0) >= 1 and r.get('status') == 'ok' and r.get('speed') and r.get('speed32') and r.get('genome')]
    XC = {}
    def ex(r):                                                   # a record's genes as built (564), by id once
        if r['id'] not in XC: XC[r['id']] = E.express(E.canon(r['genome']))
        return XC[r['id']]
    tenth = lambda F, Q: sorted(F, key=lambda i: Q[i]['speed'])[:max(1, len(F) // 10)]
    top = tenth(T, R)
    # 573: the places a gene's other value keeps it (KEEP), and every run's true front (stays) - 8 runs, never one's absence
    PA = [i for i, r in P.items() if r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss') and r.get('speed32')]
    keep = [R[i] for i in top + list(xid.values())] + [P[i] for i in tenth(PF, P)]
    keep += [P[min(PA, key=lambda i: (P[i][f], i))] for f in ('speed', 'total', 'rss', 'speed32')] if PA else []
    cf = opt('--candidates')
    if cf: keep += [r for r in hv.load(cf, E).values() if r.get('genome')]
    fronts = [(os.path.basename(f), [Q[i] for i in hv.true_front(Q, E)]) for f, Q in ((f, hv.load(f, E)) for f in pool)] + [('seed %d' % N, [R[i] for i in T])]
    print('\nThe re-enabled genes (lifted.py\'s ten): among the designs expressing each, the share of the front off its old value '
          'over the share of the %d children (alive, generation 1 on) off it. The classes (573): REVISIT at %.1f or more with %d or more '
          'on the front; KEEP - off it on %s, an extreme or a fastest tenth (the run\'s, the pool\'s); stays - off it on a true front '
          'of the %d runs; retire candidate - on none.\n' % (len(C), SCREEN[0], SCREEN[1], 'a candidate (%s)' % os.path.basename(cf) if cf else 'a candidate (none given)', len(fronts)))
    print('| gene | frozen at | the front off it (of expressing) | its values there | the children off it | enrichment | the fastest tenth off it | the fronts off it | class |')
    print('|---|---|---|---|---|---|---|---|---|')
    cls = {}
    for k, f in L.items():
        off = lambda r: k in ex(r) and ex(r)[k] != f
        val = lambda i: ex(R[i])[k] if k in ex(R[i]) else 'n/e'
        fe, fo, ce, co, en = enrichment(T, C, val, f)
        vs = {}
        for i in T:
            v = val(i)
            if v not in (f, 'n/e'): vs[v] = vs.get(v, 0) + 1
        fr = sum(1 for _, F in fronts if any(off(r) for r in F))
        cls[k] = 'REVISIT' if screened(fo, en) else 'KEEP' if any(off(r) for r in keep) else 'stays' if fr else 'retire candidate'
        print('| %s | %s | %d of %d | %s | %d of %d | %s | %d of %d | %d of %d | %s |' % (
            k, f, fo, fe, ', '.join('%s: %d' % (v, n) for v, n in sorted(vs.items(), key=str)) or '-', co, ce,
            '%.2f' % en if en is not None else '-', sum(1 for i in top if val(i) not in (f, 'n/e')), len(top), fr, len(fronts), cls[k]))
    by = lambda c: ', '.join(k for k in L if cls[k] == c) or 'none'
    print('\nthe screen: REVISIT %s; KEEP %s; stays %s; retire candidates %s - REVISIT\'s freeze revisited before anything is called '
          'final (GOALS.md step 2), a retire candidate consolidation\'s to decide.' % (by('REVISIT'), by('KEEP'), by('stays'), by('retire candidate')))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
