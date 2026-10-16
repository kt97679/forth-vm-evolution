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
"""
import bisect, collections, glob, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
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

def profile(g, d):
    """-> (the words: [(start, end, name)], {workload: {address: dispatches}})"""
    shutil.rmtree(d, ignore_errors=True); cm = d + '.map'; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    try: eng, img = E.build(g, d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
    W = sorted((int(f[1]), int(f[2]), ' '.join(f[4:])) for f in (l.rstrip('\n').split(' ') for l in open(cm)) if f[0] == 'W' and f[3] == 'code')
    pw = E.private_work(d); runs = {}
    for wl in E.WORK_SEL:
        pf = os.path.join(d, 'p-' + wl)
        E.sh([eng, img], cwd=pw, inp=E.program(wl), timeout=240, cpu=20, env=dict(os.environ, VMPROF=pf))
        c = collections.Counter()
        for f in (l.split() for l in open(pf)):
            if f[0] == 'I': c[int(f[1])] += int(f[2])
        runs[wl] = c
    shutil.rmtree(d, ignore_errors=True); os.path.exists(cm) and os.remove(cm)
    return W, runs

def by_word(W, c):
    at = [w[0] for w in W]; s = collections.Counter()
    for a, n in c.items():
        i = bisect.bisect_right(at, a) - 1
        s[W[i][2] if i >= 0 and W[i][0] <= a < W[i][1] else '(compiled at run time)'] += n
    return s

for ident in args:
    g = E.canon(recs[ident]['genome'])
    if not E.express(g).get('jit'): print('%s: no JIT - nothing for the JIT to leave' % ident); continue
    W0, off = profile(dict(g, jit=0), os.path.join(E.EV, 'jitleft-off'))
    W1, on = profile(g, os.path.join(E.EV, 'jitleft-on'))
    print('\n## %s\n\n| workload | dispatches, JIT off | left by the JIT | left |\n|---|---|---|---|' % ident)
    left = collections.Counter(); work = collections.Counter()
    for wl in E.WORK_SEL:
        t0, t1 = sum(off[wl].values()), sum(on[wl].values())
        print('| %s | %s | %s | %.1f%% |' % (wl, format(t0, ','), format(t1, ','), 100.0 * t1 / max(1, t0)))
        for k, v in by_word(W1, on[wl]).items(): left[k] += v / max(1, t1) / len(E.WORK_SEL)
        for k, v in by_word(W0, off[wl]).items(): work[k] += v / max(1, t0) / len(E.WORK_SEL)
    print('\nWhat is left, by word (the mean share over the workloads), beside the word\'s share of the JIT-off work:\n')
    for k, v in left.most_common(12): print('- %-24s %5.1f%% of what is left; %5.1f%% of the work, JIT off' % (k, 100 * v, 100 * work.get(k, 0.0)))
