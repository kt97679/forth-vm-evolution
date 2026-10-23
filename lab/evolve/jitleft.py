#!/usr/bin/env python3
"""jitleft.py ID [ID ...] [--db FILE ...] - what the JIT leaves to the interpreter (Iteration 339;
results/drafts/next-genes.md). The JIT translates a word only whole - an operation without a stencil
leaves the word interpreted - and the JIT designs are the speed frontier; and with selecting at both
widths a JIT design is judged too by the interpreter under it. Each design built twice with the call
map and the profiler, as hotwords.py does: the JIT off - every dispatch the workload makes - and the
JIT on, its own - where a translated word runs native and dispatches nothing, so what is counted is
what the JIT left. For each selection workload: the dispatches left, as a share of the JIT-off ones;
then the words that carry what is left (their share of it), each with its share of the JIT-off work.
Code compiled at run time (the benchmarks' own words) is in no body: it counts in the totals only.
--why (Iteration 340): the JIT-on build made with -DJITLOG=1 (engine/jit.c logs each refusal), and
for every word left, why: the operation that stopped its translation, followed through any callee
that was itself refused down to the root - named from the call map's O lines.
"""
import bisect, collections, glob, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
WHY = '--why' in sys.argv
SET = dict(a[6:].split('=', 1) for a in sys.argv if a.startswith('--set='))   # Iteration 341: --set=gene=value, a design varied
args = [a for a in sys.argv[1:] if not a.startswith('--')]
dbs = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == '--db']
args = [a for a in args if a not in dbs]
if not args: sys.exit(__doc__)
recs = {}
for db in dbs or sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*.md'))):
    for l in open(db, errors='replace'):
        try: r = json.loads(l)
        except ValueError: continue
        if isinstance(r, dict) and 'genome' in r and 'id' in r: recs[r['id']] = r
missing = [x for x in args if x not in recs]
if missing: sys.exit('jitleft: no recorded design %s' % ' '.join(missing))
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()

def profile(g, d, why=False):
    """-> (the words: [(start, end, name)], {workload: {address: dispatches}}, the ops {address: name}, refusals)"""
    shutil.rmtree(d, ignore_errors=True); cm = d + '.map'; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    if why: os.environ['EVOLVE_JITLOG'] = '1'
    try: eng, img = E.build(g, d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']; os.environ.pop('EVOLVE_JITLOG', None)
    lines = [l.rstrip('\n').split(' ') for l in open(cm)]
    W = sorted((int(f[1]), int(f[2]), ' '.join(f[4:])) for f in lines if f[0] == 'W' and f[3] == 'code')
    OPS = {int(f[1]): ' '.join(f[4:]) for f in lines if f[0] == 'O' and len(f) >= 5}
    pw = E.private_work(d); runs = {}; refused = {}
    jl = os.path.join(d, 'jitlog')
    for wl in E.WORK_SEL:
        pf = os.path.join(d, 'p-' + wl)
        E.sh([eng, img], cwd=pw, inp=E.program(wl), timeout=240, cpu=20, env=dict(os.environ, VMPROF=pf, **({'JITLOG': jl} if why else {})))
        c = collections.Counter()
        for f in (l.split() for l in open(pf)):
            if f[0] == 'I': c[int(f[1])] += int(f[2])
        runs[wl] = c
    if why and os.path.exists(jl):
        for f in (l.split() for l in open(jl)):
            if len(f) >= 4 and f[0] == 'R': refused.setdefault(int(f[1]), (int(f[2]), int(f[3])))   # 471: a fifth field now
    shutil.rmtree(d, ignore_errors=True); os.path.exists(cm) and os.remove(cm)
    return W, runs, OPS, refused

def by_word(W, c):
    at = [w[0] for w in W]; s = collections.Counter()
    for a, n in c.items():
        i = bisect.bisect_right(at, a) - 1
        s[W[i][2] if i >= 0 and W[i][0] <= a < W[i][1] else '(compiled at run time)'] += n
    return s

for ident in args:
    g = E.canon(dict(E.canon(recs[ident]['genome']), **{k: int(v) for k, v in SET.items()}))
    if not E.express(g).get('jit'): print('%s: no JIT - nothing for the JIT to leave' % ident); continue
    W0, off, _, _ = profile(dict(g, jit=0), os.path.join(E.EV, 'jitleft-off'))
    W1, on, OPS, refused = profile(g, os.path.join(E.EV, 'jitleft-on'), WHY)
    print('\n## %s\n\n| workload | dispatches, JIT off | left by the JIT | left |\n|---|---|---|---|' % ident)
    left = collections.Counter(); work = collections.Counter()
    for wl in E.WORK_SEL:
        t0, t1 = sum(off[wl].values()), sum(on[wl].values())
        print('| %s | %s | %s | %.1f%% |' % (wl, format(t0, ','), format(t1, ','), 100.0 * t1 / max(1, t0)))
        for k, v in by_word(W1, on[wl]).items(): left[k] += v / max(1, t1) / len(E.WORK_SEL)
        for k, v in by_word(W0, off[wl]).items(): work[k] += v / max(1, t0) / len(E.WORK_SEL)
    print('\nWhat is left, by word (the mean share over the workloads), beside the word\'s share of the JIT-off work:\n')
    at = [w[0] for w in W1]
    def word_at(a):
        i = bisect.bisect_right(at, a) - 1
        return W1[i] if i >= 0 and W1[i][0] <= a < W1[i][1] else None
    REASON = {1: 'no mapping for', 2: 'the return stack at', 3: 'no usable stencil for', 5: 'the JIT memory full'}
    def why_left(name):
        w = next((x for x in W1 if x[2] == name), None); seen = set(); path = []
        while w is not None and w[0] not in seen:
            seen.add(w[0]); r = next((refused[k] for k in refused if w[0] <= k < w[1]), None)
            if r is None: return ('never tried' if not path else ' > '.join(path) + ' > never tried')
            a, y = r
            if y == 4:
                c = word_at(a); path.append('callee %s' % (c[2] if c else a)); w = c; continue
            return ' > '.join(path + ['%s %s' % (REASON.get(y, 'why %d' % y), OPS.get(a, '@%d' % a))])
        return ' > '.join(path) + ' (a cycle)'
    blockers = collections.Counter()
    for k, v in left.most_common(12):
        print('- %-24s %5.1f%% of what is left; %5.1f%% of the work, JIT off%s' % (k, 100 * v, 100 * work.get(k, 0.0), ('; left: ' + why_left(k)) if WHY and not k.startswith('(') else ''))
    if WHY:
        for k, v in left.items():
            if not k.startswith('('): blockers[why_left(k).split(' > ')[-1]] += v
        print('\nThe root operations, by the share of what is left behind them:\n')
        for k, v in blockers.most_common(10): print('- %5.1f%%  %s' % (100 * v, k))
