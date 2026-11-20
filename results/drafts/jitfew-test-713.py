# results/drafts/jitfew-test-713.py (Iteration 713, results/drafts/early-computers-713.md) - run from a root with the gene jitfew
import json, os, sys, tempfile, shutil, statistics, re, hashlib
# jitfew_test.py ROOT IDS N LIST: each design built with the gene jitfew off and on; per workload, interleaved rounds:
# time (run_metric, long workloads), pages (MINFLT), the output's hash; the engine's .text and file bytes
ROOT = sys.argv[1]; IDS = sys.argv[2].split(','); N = int(sys.argv[3]); LIST = sys.argv[4]
sys.path.insert(0, os.path.join(ROOT, 'lab/evolve')); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
R = {json.loads(l)['id']: json.loads(l) for l in open(LIST) if l.startswith('{"')}
for i in IDS:
    g0 = E.canon(R[i]['genome']); g1 = E.canon(dict(g0, jitfew=1))
    assert E.design_id(g0) == i if hasattr(E, 'design_id') else True
    B = []
    for g in (g0, g1):
        dd = tempfile.mkdtemp(prefix='jf-'); eng, img = E.build(g, dd); pw = E.private_work(dd)
        B.append((dd, eng, img, pw, os.path.getsize(eng), E.text_size(eng)))
    T = [{}, {}]; P = [{}, {}]; H = [{}, {}]
    for k in range(N):
        for w in E.WORK_SEL:
            for s in ((0, 1) if k % 2 == 0 else (1, 0)):
                dd, eng, img, pw = B[s][:4]
                T[s].setdefault(w, []).append(E.run_metric(eng, img, pw, w)); P[s].setdefault(w, []).append(E.RSS_LAST[0] // E.PAGE_KB)
                H[s].setdefault(w, set()).add(E.OUT_LAST[0])
    med = lambda d: {w: statistics.median(v) for w, v in d.items()}
    t0, t1, p0, p1 = med(T[0]), med(T[1]), med(P[0]), med(P[1])
    mem = lambda p: max(v for w, v in p.items() if w != 'apps')
    same = all(H[0][w] == H[1][w] and len(H[0][w]) == 1 for w in E.WORK_SEL)
    print(json.dumps({'id': i, 'expressed': bool(E.express(g1).get('jitfew')), 'bin': [B[0][4], B[1][4]], 'text': [B[0][5], B[1][5]],
                      'memory_pages': [mem(p0), mem(p1)], 'apps_pages': [p0['apps'], p1['apps']], 'pages': [p0, p1],
                      'time_pct': {w: round(100 * (t1[w] / t0[w] - 1), 2) for w in t0}, 'outputs_alike': same}))
    sys.stdout.flush()
    for b in B: shutil.rmtree(b[0], ignore_errors=True)
