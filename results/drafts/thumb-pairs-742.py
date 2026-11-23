#!/usr/bin/env python3
"""results/drafts/thumb-pairs-742.py SESSIONS CANDIDATES - the thumb variants against their parents on the Tegra (Iteration
742; results/drafts/thumb-742.txt). SESSIONS: a follow-up chain's readings by session (chain-sessions.py's DEST: sK/
rage.lan-prebuiltarm.out.json); CANDIDATES: results/candidates-thumb-742.md (each variant's why names its parent). For
each pair measured in the same sessions: the variant's speed over its parent's (speed_here - CPU time against the
Tegra's s6, lower is faster), the mean of the sessions' log ratios as a ratio, its SE, the sessions; then the reading by
the roles' speed rule - 2 % slower or more at 2 SE is a loss, else none shown. Thumb-2's ARM bytes are 25-31 % fewer
(thumb-742.txt); whether to ship it is the owner's. Exit 1 if a pair has no session in common.
--self-test: synthetic sessions (a variant 1 % faster, one 3 % slower, one with no readings) - the arithmetic and the
verdicts checked."""
import glob, json, math, os, re, statistics, sys, tempfile

def pairs(cand):
    P = []
    for l in open(cand):
        if not l.startswith('{'): continue
        r = json.loads(l); m = re.search(r"'s (\w{10}) with thumb=1", r.get('why', ''))
        if m: P.append((r['id'], m.group(1), r['why'].split(': ', 1)[1].split("'s ")[0]))
    return P

def read(ses):
    S = {}
    for d in glob.glob(os.path.join(ses, 's[0-9]*')):
        k = int(d.rsplit('s', 1)[1]); f = os.path.join(d, 'rage.lan-prebuiltarm.out.json')
        if os.path.exists(f):
            for x in json.load(open(f))['designs']:
                if x.get('speed_here'): S.setdefault(x['id'], {})[k] = x['speed_here']
    return S

def report(ses, cand, out=sys.stdout):
    S, bad, res = read(ses), 0, {}
    print('| role | thumb | parent | sessions | thumb / parent | SE | the rule |', file=out)
    print('|---|---|---|---:|---:|---:|---|', file=out)
    for v, p, role in pairs(cand):
        ks = sorted(set(S.get(v, {})) & set(S.get(p, {})))
        if not ks:
            print('| %s | %s | %s | 0 | - | - | NO READINGS |' % (role, v, p), file=out); bad += 1; res[v] = None; continue
        d = [math.log(S[v][k] / S[p][k]) for k in ks]; m = statistics.fmean(d)
        se = statistics.stdev(d) / math.sqrt(len(d)) if len(d) > 1 else float('nan')
        loss = math.exp(m) >= 1.02 and len(d) > 1 and m - 2 * se > 0
        res[v] = 'loss' if loss else 'none'
        print('| %s | %s | %s | %d | %.4f | %.2f%% | %s |' % (role, v, p, len(d), math.exp(m), se * 100,
              'a loss (2 % slower at 2 SE)' if loss else 'no loss shown'), file=out)
    return bad, res

if __name__ == '__main__':
    if sys.argv[1:] == ['--self-test']:
        t = tempfile.mkdtemp(); c = os.path.join(t, 'c.md')
        with open(c, 'w') as f:
            for v, p, r in (('aaaaaaaaaa', 'pppppppppp', 'one'), ('bbbbbbbbbb', 'qqqqqqqqqq', 'two'), ('cccccccccc', 'rrrrrrrrrr', 'three')):
                f.write(json.dumps({'id': v, 'why': "thumb variant (742): %s's %s with thumb=1 - its ARM build in Thumb-2" % (r, p)}) + '\n')
        for k, jit in enumerate((1.00, 1.002, 0.998), 1):
            os.makedirs(os.path.join(t, 's%d' % k))
            D = [{'id': 'pppppppppp', 'speed_here': 0.50 * jit}, {'id': 'aaaaaaaaaa', 'speed_here': 0.495 * jit},
                 {'id': 'qqqqqqqqqq', 'speed_here': 0.40 * jit}, {'id': 'bbbbbbbbbb', 'speed_here': 0.412 * jit * (1 + 0.001 * k)},
                 {'id': 'rrrrrrrrrr', 'speed_here': 0.30}]
            json.dump({'designs': D}, open(os.path.join(t, 's%d' % k, 'rage.lan-prebuiltarm.out.json'), 'w'))
        import io
        bad, res = report(t, c, io.StringIO())
        ok = bad == 1 and res == {'aaaaaaaaaa': 'none', 'bbbbbbbbbb': 'loss', 'cccccccccc': None}
        print('thumb-pairs self-test: %s (%s)' % ('PASS' if ok else 'FAIL', res)); sys.exit(0 if ok else 1)
    if len(sys.argv) != 3: sys.exit(__doc__)
    bad, _ = report(sys.argv[1], sys.argv[2])
    sys.exit(1 if bad else 0)
