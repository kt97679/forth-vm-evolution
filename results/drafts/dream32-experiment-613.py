#!/usr/bin/env python3
"""results/drafts/dream32-experiment-613.py DIR [CANDIDATES] | --self-test - the dream 32-bit experiment read (Iteration
613, prepared while seed 88 ran; the designs: results/candidates-dream32-612.md, the default CANDIDATES).
DIR: a chain's readings laid out by lab/evolve/chain-sessions.py - DIR/sK: the laptop's loadtest.md (its K-th
experiment step), each remote line's HOST-HOW.out.json (its K-th session); a flat DIR is one session.
For each design: each source's speed, the geometric mean of its sessions - the laptop alone at 8 and 4 bytes, every
remote line (x86 at 8 or 4 bytes, ARMv7) - and each x86 line's ratio to the laptop at its width, ARMv7's to the
laptop at 4 bytes. For each variant against its base: the change in each ratio and in each source's speed; a remote
line's change paired by session (the SE of the mean log difference over the sessions both have). Verdicts, as 612's
predictions put them: a variant RESTORES when its 4-byte x86 line's ratio is within 15% of the control's (782f3ad7ff):
(3) the clang build (compiler=1) restores both bases; (4) one other reverted gene, reverted on both bases, restores both.
--self-test: synthetic readings, known answers."""
import glob, json, math, os, shutil, statistics, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAP = (('laptop64', 'idle'), ('laptop32', 'idle32'))
gm = lambda v: math.exp(sum(math.log(t) for t in v) / len(v))
pc = lambda x: '%+.1f%%' % ((math.exp(x) - 1) * 100)


def source(env):
    m = str(env.get('machine', ''))
    if m.startswith('arm') or m.startswith('aarch'): return 'arm', 'laptop32'
    return ('x32', 'laptop32') if env.get('cell') == 4 else ('x64', 'laptop64')


def read(d, ids):
    """-> {source: {id: [per-session readings, None where the session lacks it]}}, {source: (kind, laptop source)}"""
    dirs = sorted(glob.glob(os.path.join(d, 's[0-9]*')), key=lambda p: int(p.rsplit('s', 1)[1])) or [d]
    S, kind = {}, {}
    for k, sd in enumerate(dirs):
        p = os.path.join(sd, 'loadtest.md')
        if os.path.exists(p):
            L = {}
            for l in open(p, errors='replace'):
                if l.startswith('{"'):
                    try: r = json.loads(l)
                    except ValueError: continue
                    L[r.get('id')] = r
            for s, key in LAP:
                kind[s] = ('laptop', s)
                for i in ids: S.setdefault(s, {}).setdefault(i, {})[k] = L.get(i, {}).get(key)
        for f in sorted(glob.glob(os.path.join(sd, '*.out.json'))):
            o = json.load(open(f)); s = os.path.basename(f)[:-9]; kind[s] = source(o.get('env', {}))
            got = {x.get('id'): x.get('speed_here') for x in o.get('designs', []) if not x.get('rejected')}
            for i in ids: S.setdefault(s, {}).setdefault(i, {})[k] = got.get(i)
    return S, kind


def main(d, cf):
    C = [json.loads(l) for l in open(cf) if l.startswith('{')]
    ids = [r['id'] for r in C]; base = {r['id']: r['base'] for r in C if r.get('base')}
    ctrl = next(r['id'] for r in C if 'control' in r.get('why', ''))
    S, kind = read(d, ids)
    P = {s: {i: gm([v for v in S[s][i].values() if v]) for i in ids if any(S[s][i].values())} for s in S}
    print('# The dream 32-bit experiment (results/drafts/dream32-experiment-613.py %s)\n' % d)
    for s in sorted(S):
        n = len(next(iter(S[s].values())))
        miss = [i for i in ids if i not in P[s]]
        print('- %s (%s): %d session(s); %d of %d designs measured%s' % (
            s, kind[s][0], n, len(ids) - len(miss), len(ids), '' if not miss else ' - not: ' + ', '.join(miss)))
    rl = [s for s in sorted(S) if kind[s][0] != 'laptop']
    ratio = lambda s, i: P[s][i] / P[kind[s][1]][i] if i in P[s] and i in P.get(kind[s][1], {}) else None
    print('\n| design | what | %s | %s |' % (' | '.join(s for s in sorted(S)), ' | '.join('%s / laptop' % s for s in rl)))
    print('|---|---|%s|%s|' % ('---|' * len(S), '---|' * len(rl)))
    for r in C:
        i = r['id']; what = 'the control' if i == ctrl else ('%s with %s' % (base[i], r['reverted']) if i in base else 'a base')
        print('| %s | %s | %s | %s |' % (i, what, ' | '.join('%.4f' % P[s][i] if i in P[s] else '-' for s in sorted(S)),
              ' | '.join('%.3f' % ratio(s, i) if ratio(s, i) else '-' for s in rl)))
    x32 = [s for s in rl if kind[s][0] == 'x32']
    if not x32 or ratio(x32[0], ctrl) is None:
        print('\nno 4-byte x86 line with the control measured - no verdict'); return 1
    h = x32[0]; c = ratio(h, ctrl); bar = c * 1.15
    print('\n%s / laptop at 4 bytes: the control %s %.3f - a variant RESTORES at %.3f or below.\n' % (h, ctrl, c, bar))
    print('| variant | %s / laptop: base -> variant | change (%s paired SE) | %s |' % (h, h, ' | '.join('%s speed' % s for s in sorted(S))))
    print('|---|---|---|%s' % ('---|' * len(S)))
    rest = {}
    for r in C:
        i = r['id']
        if i not in base: continue
        b = base[i]; rb, rv = ratio(h, b), ratio(h, i)
        if rv is None or rb is None:
            print('| %s %s | not measured | | %s |' % (b, r['reverted'], ' | '.join('' for _ in S))); continue
        dd = [math.log(S[h][i][k] / S[h][b][k]) for k in S[h][i] if S[h][i][k] and S[h][b].get(k)]
        se = statistics.stdev(dd) / math.sqrt(len(dd)) if len(dd) > 1 else float('nan')
        rest[(b, r['reverted'])] = rv <= bar
        sp = ' | '.join(pc(math.log(P[s][i] / P[s][b])) if i in P[s] and b in P[s] else '-' for s in sorted(S))
        print('| %s %s | %.3f -> %.3f%s | %s (%s +/- %.1f%%) | %s |' % (b, r['reverted'], rb, rv, ' RESTORES' if rv <= bar else '',
              pc(math.log(rv / rb)), h, se * 100, sp))
    bs = sorted(set(base.values()))
    comp = [rest.get((b, 'compiler=1')) for b in bs]
    genes = sorted({g for (_, g) in rest if g != 'compiler=1' and all((b, g) in rest for b in bs)})
    one = [g for g in genes if all(rest[(b, g)] for b in bs)]
    print('\n(3) the clang build restores both bases: %s' % ('RIGHT' if all(comp) else 'WRONG' if all(x is not None for x in comp) else 'open - not measured on both'))
    print('(4) one other gene, reverted on both, restores both: %s' % (('RIGHT - ' + ', '.join(one)) if one else 'WRONG - none of %s' % ', '.join(genes) if genes else 'open - no gene measured on both'))
    return 0


def self_test():
    t = tempfile.mkdtemp()
    try:
        C = [dict(id='b' * 10, why='a base'), dict(id='c' * 10, why='the control'),
             dict(id='v' * 10, base='b' * 10, reverted='compiler=1'), dict(id='w' * 10, base='b' * 10, reverted='regpin=0')]
        open(os.path.join(t, 'cand.md'), 'w').write(''.join(json.dumps(r) + '\n' for r in C))
        lap = {'b' * 10: 0.30, 'c' * 10: 0.31, 'v' * 10: 0.33, 'w' * 10: 0.30}         # the laptop at 4 bytes
        dr = {'b' * 10: 0.63, 'c' * 10: 0.33, 'v' * 10: 0.37, 'w' * 10: 0.60}          # dream: c 1.065, b 2.10, v 1.12, w 2.0
        for k in (1, 2, 3):
            sd = os.path.join(t, 's%d' % k); os.makedirs(sd)
            if k == 1:
                open(os.path.join(sd, 'loadtest.md'), 'w').write(''.join(json.dumps(dict(id=i, idle=v, idle32=v)) + '\n' for i, v in lap.items()))
            j = 1 + 0.002 * (k - 2)
            json.dump(dict(env=dict(cell=4, machine='x86_64'), designs=[dict(id=i, speed_here=v * j) for i, v in dr.items()]),
                      open(os.path.join(sd, 'dream.lan-prebuilt32.out.json'), 'w'))
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): main(t, os.path.join(t, 'cand.md'))
        o = buf.getvalue()
        checks = [('RESTORES' in [l for l in o.split('\n') if l.startswith('| ' + 'b' * 10 + ' compiler=1')][0], 'the clang build restores'),
                  ('RESTORES' not in [l for l in o.split('\n') if l.startswith('| ' + 'b' * 10 + ' regpin=0')][0], 'regpin=0 does not'),
                  ('(3) the clang build restores both bases: RIGHT' in o, 'prediction 3 scored RIGHT'),
                  ('(4) one other gene, reverted on both, restores both: WRONG - none of regpin=0' in o, 'prediction 4 scored WRONG')]
        bad = [w for ok, w in checks if not ok]
        print('dream32-experiment-613.py self-test: %d checks - %s' % (len(checks), 'PASS' if not bad else 'FAIL: ' + '; '.join(bad)))
        return 1 if bad else 0
    finally:
        shutil.rmtree(t)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--self-test']: sys.exit(self_test())
    if not a: sys.exit(__doc__)
    sys.exit(main(a[0], a[1] if len(a) > 1 else os.path.join(ROOT, 'results', 'candidates-dream32-612.md')))
