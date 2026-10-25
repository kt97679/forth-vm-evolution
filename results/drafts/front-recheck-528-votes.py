# 528's gene votes on the true fronts of seeds 70-72 (results/drafts/front-recheck-528.md); reads /tmp/rv/seedN.jsonl, each run's db.jsonl from its chain archive. Copied from /tmp at Iteration 542, as run.
import bisect, json, math, sys
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.TWO_WIDTHS[0] = True
def new_front(ids, R):          # the after-seed-73 batch's first_front (bughunt-evolver-after-seed73.patch)
    arch = []
    for i in sorted(ids, key=lambda i: (E.ov(R[i], 'total'), E.ov(R[i], 'speed'))):
        r = R[i]
        if any(E.dominates(R[a], r) for a in arch): continue
        arch = [a for a in arch if not E.dominates(r, R[a])]; arch.append(i)
    by_t = sorted(ids, key=lambda i: E.ov(R[i], 'total')); tots = [E.ov(R[i], 'total') for i in by_t]; out = set()
    for b in arch:
        k = bisect.bisect_right(tots, E.ov(R[b], 'total'))
        if not any(a != b and E.dominates(R[a], R[b]) for a in by_t[:k]): out.add(b)
    return [i for i in ids if i in out]
SKIP = {'enc', 'opt', 'compiler', 'spec', 'folds', 'ops10'}
def votes(ids, R):
    n = len(ids); k = max(1, n // 10)
    sp = {i: R[i]['speed'] for i in ids}; by = {i: E.ov(R[i], 'total') for i in ids}; mem = {i: R[i]['rss'] for i in ids}
    fast = set(sorted(ids, key=sp.get)[:k]); small = set(sorted(ids, key=by.get)[:k]); bestq = set(sorted(ids, key=lambda i: sp[i] * by[i] * mem[i])[:k])
    ex = {i: E.express(E.canon(R[i]['genome'])) for i in ids}
    fams = set(R[i]['genome'].get('enc') for i in ids); out = {}
    for g in dict.fromkeys(x for f, fam in E.EXPRESSED.items() if f in fams for x in fam):
        if g in SKIP: continue
        on = set(i for i in ids if ex[i].get(g)); share = 100.0 * len(on) / n
        out[g] = (share, len(on & fast), len(on & small), len(on & bestq), (share < 10) + (len(on & fast) == 0) + (len(on & small) == 0) + (len(on & bestq) == 0))
    return out
tot = {}
for seed in (70, 71, 72):
    R = {}
    for l in open('/tmp/rv/seed%d.jsonl' % seed):
        if l.startswith('{'):
            try: r = json.loads(l)
            except ValueError: continue
            R[r['id']] = r
    ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and r.get('total') and r.get('rss') and r.get('speed32')]
    old = E.first_front(ok, R); new = new_front(ok, R)
    vo, vn = votes(old, R), votes(new, R)
    print('seed %d: the reported front %d, by dominates() %d (%d in both)' % (seed, len(old), len(new), len(set(old) & set(new))), flush=True)
    for g in ('rtfuse', 'rtimm', 'jitret', 'jitfuse', 'jitexec', 'jitmul', 'jitdoes', 'jitcfa', 'jitrp'):
        if g in vo or g in vn:
            a, b = vo.get(g), vn.get(g)
            print('   %-8s reported: share %5.1f%% tenths %s votes %s | by dominates(): share %5.1f%% tenths %s votes %s' % (g, a[0] if a else 0, a[1:4] if a else '-', a[4] if a else '-', b[0] if b else 0, b[1:4] if b else '-', b[4] if b else '-'))
    for g in set(vo) | set(vn):
        tot.setdefault(g, [0, 0]); tot[g][0] += vo.get(g, (0, 0, 0, 0, 0))[4]; tot[g][1] += vn.get(g, (0, 0, 0, 0, 0))[4]
cand_old = sorted(g for g, (a, b) in tot.items() if a >= 11); cand_new = sorted(g for g, (a, b) in tot.items() if b >= 11)
print('candidates over 70-72 (11 or 12 of 12): reported %s | by dominates() %s' % (cand_old, cand_new))
print('changed totals:', {g: tuple(v) for g, v in sorted(tot.items()) if v[0] != v[1]})
