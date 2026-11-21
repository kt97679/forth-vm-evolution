#!/usr/bin/env python3
"""lab/evolve/selfhost-speed.py [--rounds R] [--pairs K] [NAME ...] [DB ...] - the self-hosting gate's speed half
(Iteration 720; results/drafts/premortem-roles-707.md: a role ships self-built when its self-built image runs at the
translator's speed, else translator-built, named in designs/TRANSLATOR-BUILT). For each design of designs/ (NAME ...,
default all) not named in TRANSLATOR-BUILT: its own engine and self-built image as shipped (designs/NAME/forth
image.img; forth32 image32.img - a JIT design's engine carries its image's layout lines) against the lab's build of its
record (evolve.build: the translator's engine and image), each alive first (evolve.alive: the corpus, the kernel
workload's image byte for byte), then over the selection workloads by evolve.measure (each run against s6 in the same
round), K alternations (self first, then the translator first, ...), at 8- and 4-byte cells. Per design and width the
ratio of the geometric means, self / translator: the median over the alternations and its range. The gate's reading:
at most 1.02 (the roles' 2 % speed rule) keeps the self-built image. A chain's laptop step - NEXT-RUN's `experiment
selfhost-speed.py` (next-run.sh passes every database here: files, unused). One JSON line a design at the end."""
import json, math, os, shutil, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); D = os.path.join(ROOT, 'designs')
A = sys.argv[1:]
def opt(n, d):
    if n not in A: return d
    i = A.index(n); v = A[i + 1]; del A[i:i + 2]; return v
rounds, K = int(opt('--rounds', '10')), int(opt('--pairs', '5'))
names = [x for x in A if os.path.isdir(os.path.join(D, x))]
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
tb = os.path.join(D, 'TRANSLATOR-BUILT')
TB = {l.split()[0] for l in open(tb) if l.strip() and not l.startswith('#')} if os.path.exists(tb) else set()
if not names: names = sorted(n for n in os.listdir(D) if os.path.exists(os.path.join(D, n, 'record.json')))
skip = [n for n in names if n in TB]; names = [n for n in names if n not in TB]
gm = lambda t: math.exp(sum(math.log(t[w]) for w in E.WORK_SEL) / len(E.WORK_SEL))
print('# The self-hosting gate\'s speed half (lab/evolve/selfhost-speed.py, Iteration 720)\n')
print('%d designs, self-built against the translator\'s build, %d alternations of %d rounds over %s at both widths%s.\n'
      % (len(names), K, rounds, ', '.join(E.WORK_SEL), '; translator-built, not timed: ' + ', '.join(skip) if skip else ''))
print('| design | id | 8-byte: self / translator, median (range) | 4-byte: self / translator, median (range) | gate |')
print('|---|---|---|---|---|', flush=True)
out = []
def pairs(es, is_, et, it, pw, r):
    E.alive(es, is_, pw, far=True); E.alive(et, it, pw, far=True)
    q, by = [], {w: [] for w in E.WORK_SEL}
    for k in range(K):
        v = {}
        for who in (('s', 't') if k % 2 == 0 else ('t', 's')):
            t, _ = E.measure(*((es, is_) if who == 's' else (et, it)), pw, E.WORK_SEL, r); v[who] = t
        q.append(gm(v['s']) / gm(v['t']))
        for w in E.WORK_SEL: by[w].append(v['s'][w] / v['t'][w])
    return q, {w: round(statistics.median(x), 4) for w, x in by.items()}   # by workload: which one moves
for n in names:
    rec = json.load(open(os.path.join(D, n, 'record.json'))); i = rec['id']; row = {'name': n, 'id': i}
    for w, (eng, img) in (('8', ('forth', 'image.img')), ('4', ('forth32', 'image32.img'))):
        es, is_ = os.path.join(D, n, eng), os.path.join(D, n, img); d = os.path.join(E.EV, 'selfspeed-%s-%s' % (n, w))
        shutil.rmtree(d, ignore_errors=True)
        try:
            if not (os.path.exists(es) and os.path.exists(is_)): raise RuntimeError('no %s or %s - make, make 32 in designs/%s' % (eng, img, n))
            if w == '8':
                et, it = E.build(E.canon(rec['genome']), d); q, bw = pairs(es, is_, et, it, E.private_work(d), rounds)
            else:
                g32 = dict(rec['genome'])
                if (g32.get('scale') or 0) > 2: g32['scale'] = 2       # as eval32 builds it
                with E.at_width(E.WIDTH4):
                    et, it = E.build(E.canon(g32), d); q, bw = pairs(es, is_, et, it, E.private_work(d), max(1, rounds - 1))
            row['r' + w] = q; row['by' + w] = bw
        except Exception as x:
            row['r' + w] = None; row['why' + w] = str(x)[:300]
        finally:
            shutil.rmtree(d, ignore_errors=True)
    cell = lambda q, why: ('%.4f (%.4f-%.4f)' % (statistics.median(q), min(q), max(q))) if q else 'failed: ' + (why or '')[:80]
    ok = all(row.get('r' + w) and statistics.median(row['r' + w]) <= 1.02 for w in '84')
    row['gate'] = 'pass' if ok else 'FAIL'
    print('| %s | %s | %s | %s | %s |' % (n, i, cell(row.get('r8'), row.get('why8')), cell(row.get('r4'), row.get('why4')), row['gate']), flush=True)
    out.append(row)
print()
for r in out: print(json.dumps(r, sort_keys=True))
print('\nselfhost-speed: %d of %d pass the gate (self-built at most 1.02 of the translator\'s at both widths)' % (sum(r['gate'] == 'pass' for r in out), len(out)))
