# 534's first count of the frozen genes on the true fronts of seeds 59-69 (results/drafts/frozen-recheck-534.md) - jitos and alignhot from it; reads the chain archives in /mnt/user-data/uploads. Copied from /tmp at Iteration 542, as run.
import bisect, io, json, os, sys, tarfile, glob
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
GENES = ['msc', 'scale', 'sharedcall', 'tail', 'tailpn', 'kstack', 'alignhot', 'jitos', 'jithelp', 'jitre']
KNOWN = set(x for fam in E.EXPRESSED.values() for x in fam)
def front(R, ok):
    arch = []
    for i in sorted(ok, key=lambda i: (E.ov(R[i], 'total'), R[i]['speed'])):
        if any(E.dominates(R[a], R[i]) for a in arch): continue
        arch = [a for a in arch if not E.dominates(R[i], R[a])]; arch.append(i)
    by_t = sorted(ok, key=lambda i: E.ov(R[i], 'total')); tots = [E.ov(R[i], 'total') for i in by_t]
    return [b for b in arch if not any(a != b and E.dominates(R[a], R[b]) for a in by_t[:bisect.bisect_right(tots, E.ov(R[b], 'total'))])]
for seed in range(int(os.environ.get('S0', 59)), int(os.environ.get('S1', 70))):
    arcs = [p for p in glob.glob('/mnt/user-data/uploads/forth-vm-evolution-chain-*_tar.gz')]
    R = None
    for p in arcs:
        with tarfile.open(p) as t:
            inner = [m for m in t.getmembers() if ('-seed%d-' % seed) in m.name and m.name.endswith('.tar.gz')]
            if not inner: continue
            data = t.extractfile(inner[0]).read()
        with tarfile.open(fileobj=io.BytesIO(data)) as t2:
            m = [x for x in t2.getmembers() if x.name.endswith('db.jsonl')][0]
            R = {}
            for l in t2.extractfile(m).read().decode('utf-8', 'replace').split('\n'):
                if l.startswith('{'):
                    try: r = json.loads(l)
                    except ValueError: continue
                    if r.get('id'): R[r['id']] = r
        break
    if R is None: print('seed %d: no records' % seed, flush=True); continue
    ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and E.ov(r, 'total') and r.get('rss')]
    E.TWO_WIDTHS[0] = sum(1 for i in ok if R[i].get('speed32')) * 2 > len(ok)
    if E.TWO_WIDTHS[0]: ok = [i for i in ok if R[i].get('speed32')]
    F = front(R, ok); n = len(F); k = max(1, n // 10)
    sp = {i: R[i]['speed'] for i in F}; by = {i: E.ov(R[i], 'total') for i in F}; mem = {i: R[i]['rss'] for i in F}
    fast = set(sorted(F, key=sp.get)[:k]); small = set(sorted(F, key=by.get)[:k]); bq = set(sorted(F, key=lambda i: sp[i] * by[i] * mem[i])[:k])
    out = []
    for g in GENES:
        def on(i):
            gg = R[i]['genome']
            if g in KNOWN:
                try: return bool(E.express(E.canon(gg)).get(g))
                except Exception: return bool(gg.get(g))
            return bool(gg.get(g))
        s_ = set(i for i in F if on(i)); share = 100.0 * len(s_) / n
        f, sm, q = len(s_ & fast), len(s_ & small), len(s_ & bq)
        v = (share < 10) + (f == 0) + (sm == 0) + (q == 0)
        out.append('%s %.0f%% %d/%d/%d v%d' % (g, share, f, sm, q, v))
    print('seed %d (front %d, widths %s): ' % (seed, n, E.TWO_WIDTHS[0]) + ' | '.join(out), flush=True)
