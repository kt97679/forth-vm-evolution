# 539's ranges of the true fronts of seeds 70-72 in each objective, behind lab/evolve/hv-bounds.json; reads /tmp/rv/seedN.jsonl. Copied from /tmp at Iteration 542, as run.
import bisect, json, sys
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.TWO_WIDTHS[0] = True
def front(R, ok):
    arch = []
    for i in sorted(ok, key=lambda i: (E.ov(R[i], 'total'), R[i]['speed'])):
        if any(E.dominates(R[a], R[i]) for a in arch): continue
        arch = [a for a in arch if not E.dominates(R[i], R[a])]; arch.append(i)
    by_t = sorted(ok, key=lambda i: E.ov(R[i], 'total')); tots = [E.ov(R[i], 'total') for i in by_t]
    return [b for b in arch if not any(a != b and E.dominates(R[a], R[b]) for a in by_t[:bisect.bisect_right(tots, E.ov(R[b], 'total'))])]
for s in (70, 71, 72):
    R = {}
    for l in open('/tmp/rv/seed%d.jsonl' % s):
        if l.startswith('{'):
            try: r = json.loads(l)
            except ValueError: continue
            R[r['id']] = r
    ok = [i for i, r in R.items() if r.get('status') == 'ok' and r.get('speed') and E.ov(r, 'total') and r.get('rss') and r.get('speed32')]
    F = front(R, ok)
    col = lambda k: [E.ov(R[i], k) if k == 'total' else R[i][k] for i in F]
    print('seed %d front %d: speed %.3f-%.3f | total %d-%d | rss %d-%d | speed32 %.3f-%.3f' % (s, len(F), min(col('speed')), max(col('speed')), min(col('total')), max(col('total')), min(col('rss')), max(col('rss')), min(col('speed32')), max(col('speed32'))))
