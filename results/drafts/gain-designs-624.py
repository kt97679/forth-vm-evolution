# results/drafts/gain-designs-624.py - why seed 89's 32-bit gain is off the true front: each design's place on it and what
# dominates it under evolve.py's tolerances (Iteration 624; results/drafts/gain-designs-624.md). As the build user, from the
# repository's root, with seed 89's pack unpacked under /tmp/process (process-seed.sh).
import sys; sys.path.insert(0, 'lab/evolve'); sys.argv = ['x']
import evolve as E, hv
R = hv.load('/tmp/process/forth-vm-evolution-seed89-eca15d532f-fury-20261108-020020/pack/db.jsonl', E)
T = hv.true_front(R, E)
for i in ('ee34931cd7', 'd8471f1b16', '1d8000a2c1', '88233c0551'):
    r = R[i]; print(i, 'on the true front:', i in T, {k: r.get(k) for k in ('speed', 'speed32', 'total', 'rss', 'status')}, 'ov total', E.ov(r, 'total'))
    dom = [a for a in R if a != i and R[a].get('status') == 'ok' and R[a].get('speed32') and E.dominates(R[a], R[i])]
    print('   dominated by', len(dom), [(a, round(R[a]['speed'], 4), round(R[a]['speed32'], 4), R[a]['total'], E.ov(R[a], 'total'), R[a]['rss']) for a in dom[:3]])
import inspect; print(inspect.getsource(E.dominates)[:700])
