#!/usr/bin/env python3
"""lab/evolve/outliers.py DB [--remeasure32 FILE] | --self-test - readings to look at before the verdict (Iteration 701).

A design whose one workload reads FACTOR (2) times or more off its parent's while its other workloads are within 10 % of
the parent's: seed 94's 2806f89619, its 32-bit kernel 0.119 against its parent's 0.362 (the next of the 50 fastest at 32
bits 0.296), measured in the stall at generation 44 - built again here, 1.019 of its parent's time
(results/drafts/stall-seed94.py, ktime-seed94.py). Checked at both widths (t, t32) where selection and the stopping rule
look: the alive fastest 1 % at each width (at least 10), and only a reading POP (1.5) times or more off the median of
the checked designs at that workload - a gene can move one workload (a12e4b32ef's loop 0.031, its parent's 0.082, the
fast end's median 0.033 - jitloop), a stall moves it off the population too. A crossover child is flagged only when it is so against every
parent. Each flag prints the speed with that workload at its parent's reading - what the design would score without it.
With FILE (remeasure32.json, evolve.py --remeasure from Iteration 701) the 32-bit fastest measured again beside their
in-run readings. A flag is for the chat's judgment - stopping.py --strike ID --why TEXT - never applied by itself.
Run with python3 -I. process-seed.sh puts its first lines in summary.md."""
import json, math, os, re, statistics as st, sys

FACTOR, CLOSE, POP = 2.0, 1.10, 1.5
HERE = os.path.dirname(os.path.abspath(__file__))
SEL = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps']     # evolve.py's WORK_SEL (the self-test checks)
WIDTHS = (('64-bit', 't', 'speed'), ('32-bit', 't32', 'speed32'))


def gmean(t): return math.exp(sum(math.log(t[w]) for w in SEL) / len(SEL))


def odd_one(t, p):
    """(workload, factor, the others' median off) when one workload of t is FACTOR or more off p's and the rest close."""
    if not all(t.get(w) and p.get(w) for w in SEL): return None
    off = {w: abs(math.log(t[w] / p[w])) for w in SEL}
    w = max(off, key=off.get)
    rest = st.median(v for k, v in off.items() if k != w)
    return (w, math.exp(off[w]), math.exp(rest)) if off[w] >= math.log(FACTOR) and rest <= math.log(CLOSE) else None


def check(R):
    """R: id -> its last ok record. Yields (width, rank, record, parent, workload, factor, rest, the speed without it)."""
    for name, tk, sk in WIDTHS:
        alive = sorted((r for r in R.values() if r.get(sk) and r.get(tk)), key=lambda r: r[sk])
        top = alive[:max(10, len(alive) // 100)]
        med = {w: st.median(r[tk][w] for r in top if r[tk].get(w)) for w in SEL}
        for rank, r in enumerate(top, 1):
            ps = [R[p] for p in (r.get('parents') or []) if p in R and R[p].get(tk)]
            hits = [(p, odd_one(r[tk], p[tk])) for p in ps]
            if not hits or not all(h for _, h in hits): continue
            p, (w, f, rest) = min(hits, key=lambda x: x[1][1])
            if max(r[tk][w] / med[w], med[w] / r[tk][w]) < POP: continue
            t = dict(r[tk]); t[w] = p[tk][w]
            yield name, rank, r, p, w, f, rest, gmean(t)


def load(path):
    R = {}
    for l in open(path, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('status') == 'ok' and r.get('id'): R[r['id']] = r
    return R


def report(R, rm32=None):
    flags = list(check(R))
    n = {name: max(10, sum(1 for r in R.values() if r.get(sk) and r.get(tk)) // 100) for name, tk, sk in WIDTHS}
    first = {name: min((r for r in R.values() if r.get(sk)), key=lambda r: r[sk], default=None) for name, _, sk in WIDTHS}
    out = ['outliers: %d of the fastest %s checked against their parents - one workload %gx or more off, the rest within '
           '%d %%, %gx off the fast end\'s median' % (len(flags), ' and '.join('%d at %s' % (n[k], k) for k in n), FACTOR, round((CLOSE - 1) * 100), POP)]
    for name, _, sk in WIDTHS:
        f = first[name]
        if f is None: continue
        hit = [x for x in flags if x[0] == name and x[2]['id'] == f['id']]
        out.append('  the fastest at %s, %s %.4f: %s' % (name, f['id'], f[sk], ('FLAGGED - %s %.3f against %s\'s %.3f; '
                   'without it %.4f' % (hit[0][4], f[WIDTHS[name == '32-bit'][1]][hit[0][4]], hit[0][3]['id'],
                   hit[0][3][WIDTHS[name == '32-bit'][1]][hit[0][4]], hit[0][7])) if hit else 'clean'))
    for name, rank, r, p, w, fac, rest, wo in flags:
        tk, sk = WIDTHS[name == '32-bit'][1:]
        out.append('  %s #%d %s (gen %s) %.4f: %s %.3f against parent %s\'s %.3f (x%.2f, the rest within %.1f %%) - '
                   'without it %.4f' % (name, rank, r['id'], r.get('gen'), r[sk], w, r[tk][w], p['id'], p[tk][w], fac,
                                       (rest - 1) * 100, wo))
    if rm32:
        pairs = sorted(((R[i]['speed32'], v['speed32'], i) for i, v in rm32.items() if v.get('speed32') and i in R
                        and R[i].get('speed32')), key=lambda x: x[0])
        if pairs:
            q = [b / a for a, b, _ in pairs]
            out.append('remeasure32: %d of the 32-bit fastest measured again - re-measured / in-run median %.3f, range '
                       '%.3f-%.3f; the in-run fastest %s %.4f, re-measured %.4f (x%.3f)'
                       % (len(q), st.median(q), min(q), max(q), pairs[0][2], pairs[0][0], pairs[0][1], q[0]))
            out.append('  re-measured, the fastest at 32 bits: %s %.4f' % min(((i, b) for a, b, i in pairs), key=lambda x: x[1]))
    return out


def self_test():
    src = open(os.path.join(HERE, 'evolve.py')).read()
    m = re.search(r"^WORK_SEL = (\[[^\]]*\])", src, re.M)
    assert m and eval(m.group(1)) == SEL, 'SEL is not evolve.py\'s WORK_SEL'
    base = {w: 0.3 for w in SEL}
    mk = lambda i, t, par=(), gen=1: dict(id=i, status='ok', gen=gen, parents=list(par), t=dict(t), speed=gmean(t),
                                          t32=dict(t), speed32=gmean(t))
    R = {'P': mk('P', base, gen=0), 'Q': mk('Q', dict({w: 0.4 for w in SEL}, kernel=0.1), gen=0)}
    one = dict(base, kernel=0.1); spread = {w: 0.3 * (1.25 if k % 2 else 0.8) for k, w in enumerate(SEL)}; spread['kernel'] = 0.1
    R['A'] = mk('A', one, ['P'])                      # seed 94's shape: flagged
    R['B'] = mk('B', spread, ['P'])                   # the rest moved too: a gene's effect, not flagged
    R['C'] = mk('C', dict(base, fib=0.28), ['P'])     # close everywhere: not flagged
    R['D'] = mk('D', one, ['P', 'Q'])                 # a crossover, Q reads the same kernel: not flagged
    R['E'] = mk('E', dict({w: 0.2 for w in SEL}, loop=0.06), ['G'])   # a gene's one workload, the fast end's own: not
    R['G'] = mk('G', dict({w: 0.2 for w in SEL}, loop=0.18), gen=0)       # flagged (seed 94's a12e4b32ef)
    for i in range(10): R['F%d' % i] = mk('F%d' % i, dict({w: 0.35 for w in SEL}, loop=0.06), ['P'])
    got = {(x[0], x[2]['id']) for x in check(R)}
    want = {('64-bit', 'A'), ('32-bit', 'A')}
    assert got == want, (sorted(got), sorted(want))
    wo = [x[7] for x in check(R) if x[2]['id'] == 'A'][0]
    assert abs(wo - 0.3) < 1e-9, wo                   # without the odd reading: its parent's speed
    rep = report(R, {'A': {'speed32': 0.3}})
    assert rep[0].startswith('outliers: 2 of the fastest'), rep[0]
    assert rep[1].endswith('clean') and sum(' A (gen 1)' in l for l in rep) == 2, rep      # E the fastest, clean
    assert any(l.startswith('remeasure32: 1') for l in rep), rep
    print('outliers.py self-test: %d checks - one workload off flagged; a gene\'s spread, a crossover\'s parent and a '
          'reading the fast end shares not; the speed without it, the 32-bit re-measure - pass' % 6)
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--self-test']: sys.exit(self_test())
    if not a or a[0].startswith('--'): sys.exit(__doc__)
    rm = a[a.index('--remeasure32') + 1] if '--remeasure32' in a else None
    rm32 = json.load(open(rm)) if rm and os.path.exists(rm) else None
    print('\n'.join(report(load(a[0]), rm32)))
