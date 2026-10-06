#!/usr/bin/env python3
"""tag2-rank.py OUT.json DB ID [ID ...] - the reference ranking
behind the two-bit tag's one-byte codes (FORMAT-TAG2.md, Iteration 67).

Each design, as recorded (the old format), built with the profiler and run
on every selected workload; each operation's dispatches counted by its
logical number (one-byte codes; an escaped primitive, 128 + its selector),
named by the converter's own t2_names (SOD16_T2NAMES), and taken as a share
of its workload's dispatches - so each selected workload weighs the same,
as in the speed score. Shares summed over workloads, averaged over designs:
name -> weight. layout.py --tag2-rank ranks by it. Frozen once a run has
used it: a new version is a new file."""
import json, os, shutil, sys, collections
sys.argv, args = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
E.setup()
out, db, ids = args[0], args[1], args[2:]       # a file, not stdout: the evolver prints there
recs = {json.loads(l)['id']: json.loads(l) for l in open(db) if l.startswith('{')}
total = collections.Counter()
for did in ids:
    g = E.canon(recs[did]['genome'])
    d = os.path.join(E.EV, 'rank-' + did); shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d); nf = os.path.join(d, 'names.json'); os.environ['SOD16_T2NAMES'] = nf
    E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False; del os.environ['SOD16_T2NAMES']
    names = {int(k): v for k, v in json.load(open(nf)).items()}
    pw = E.private_work(d)
    for w in E.WORK_SEL:
        pf = os.path.join(d, 'p-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=300, cpu=20, env=dict(os.environ, VMPROF=pf))
        c = collections.Counter()
        for line in open(pf):
            f = line.split()
            if f[0] in ('I', 'C'): continue
            a, b, k = int(f[0]), int(f[1]), int(f[2])
            if a == 0x7D: c[128 + b] += k; continue          # an escaped primitive: its selector
            if b < 128 and b != 0x7D: c[b] += k
        n = sum(c.values()) or 1
        for L, k in c.items():
            if L in names: total[names[L]] += k / n / len(ids)
    print('%s: profiled' % did, file=sys.stderr)
json.dump(dict(sorted(total.items(), key=lambda x: -x[1])), open(out, 'w'), indent=0)
print('%d names -> %s' % (len(total), out), file=sys.stderr)
