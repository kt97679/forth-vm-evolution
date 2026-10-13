"""gene-interactions.py - how one gene's effect depends on another, read from a
run's own single-gene mutations (Iteration 250; results/gene-interactions-seed46.md).
REG=jit|nojit|all picks the parents; edit the db path below for another run."""
import json, collections, math, re, sys
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
R = {}
for l in open('/tmp/s46/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
ok = lambda r: r and r.get('status') == 'ok' and isinstance(r.get('speed'), (int, float)) and r.get('total')
EX = {}
def ex(r):
    if r['id'] not in EX: EX[r['id']] = E.express(E.canon(r['genome']))
    return EX[r['id']]
def on(v): return bool(v) and v not in ('0', 'None')
samples = collections.defaultdict(list)       # binary gene A -> [(d_speed, d_size, parent expressed)]
for c in R.values():
    h = c.get('how') or ''
    m = re.fullmatch(r'mutation: ([a-z0-9]+)=(\S+)', h)
    if not m or not ok(c) or not c.get('parents'): continue
    p = R.get(c['parents'][0])
    if not ok(p): continue
    A, v = m.group(1), m.group(2)
    if v not in ('0', '1'): continue
    pe, ce = ex(p), ex(c)
    if on(pe.get(A)) == on(ce.get(A)): continue           # the flip not expressed
    if any(pe.get(k) != ce.get(k) for k in set(pe) | set(ce) if k != A): continue   # only A changed in what is expressed - no gating
    sgn = 1 if v == '1' else -1                            # oriented: the effect of turning A on
    samples[A].append((sgn * math.log(c['speed'] / p['speed']), sgn * math.log(c['total'] / p['total']), pe))
print('binary genes with flips: %d; samples %d' % (len(samples), sum(map(len, samples.values()))))
LINKS = [set(t) for t in E.LINKS]
def linked(a, b): return any(a in t and b in t for t in LINKS)
def stats(xs):
    n = len(xs); m = sum(xs) / n; v = sum((x - m) ** 2 for x in xs) / max(1, n - 1); return n, m, v
res = {'speed': [], 'size': []}
import os
REG = os.environ.get('REG', 'all')
for A, ss0 in samples.items():
    ss = [x for x in ss0 if REG == 'all' or (REG == 'jit') == on(x[2].get('jit'))]
    if len(ss) < 150: continue
    genes = set(k for _, _, pe in ss for k in pe if k != A and not (REG != 'all' and k.startswith('jit')))
    for B in genes:
        g1 = [s for s in ss if on(s[2].get(B))]; g0 = [s for s in ss if not on(s[2].get(B))]
        if len(g1) < 30 or len(g0) < 30: continue
        for k, name in ((0, 'speed'), (1, 'size')):
            n1, m1, v1 = stats([s[k] for s in g1]); n0, m0, v0 = stats([s[k] for s in g0])
            se = math.sqrt(v1 / n1 + v0 / n0) or 1e-9
            res[name].append((abs(m1 - m0) / se, A, B, m0, m1, n0, n1))
for name in ('speed', 'size'):
    top = sorted(res[name], reverse=True)[:16]
    print('\n%s - turning A on, by B (log change; negative = faster / smaller):' % name)
    for t, A, B, m0, m1, n0, n1 in top:
        print('  %-9s x %-9s t %5.1f   B off %+.3f (%d)  B on %+.3f (%d)%s' % (A, B, t, m0, n0, m1, n1, '  [linked]' if linked(A, B) else ''))

FR = [json.loads(l)['id'] for l in open('/home/claude/forth-vm-evolution/results/evolve-amd-ryzen-7-pro-8840hs-seed46.md') if l.startswith('{"bin"')]
fj = [R[i] for i in FR if i in R and on(ex(R[i]).get('jit'))]
print('\nfront JIT designs: %d; rtloop on %d' % (len(fj), sum(on(ex(r).get('rtloop')) for r in fj)))
aj = [r for r in R.values() if ok(r) and on(ex(r).get('jit'))]
print('alive JIT designs: %d; rtloop on %d' % (len(aj), sum(on(ex(r).get('rtloop')) for r in aj)))
