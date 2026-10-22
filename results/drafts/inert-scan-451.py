# results/drafts/inert-scan-451.md - genes switched on but doing nothing. python3 THIS RESULTS.md OUT
# Four designs of a front - the fastest, the fastest without the JIT, the best by Q, the smallest - and for each gene it
# expresses (not frozen, not structural), the design rebuilt with that gene off: binary + image bytes, and the
# profiler's dispatch counts on kernel, loop and fib (deterministic). A gene that changes neither is inert in that design;
# one that changes the bytes but no dispatch count is "no run-time effect" - right for a compiler flag, a question for a
# run-time mechanism (rtiplus without its fuser was one, Iteration 446).
import json, os, re, shutil, sys
RES, OUT = sys.argv[1], sys.argv[2]; sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
SKIP = {'enc', 'opt', 'compiler', 'spec', 'folds', 'ops10', 'cell'} | set(getattr(E, 'FROZEN', {}))
WORKS = ['kernel', 'loop', 'fib']
rows, gen = {}, {}
for l in open(RES):
    m = re.match(r'\| ([0-9a-f]{10}) \| ([0-9.]+) \|.*?\| ([0-9,]+) \| ([0-9]+) \|', l)
    if m: rows[m.group(1)] = (float(m.group(2)), int(m.group(3).replace(',', '')), int(m.group(4)))
    if l.startswith('{"'):
        r = json.loads(l); gen.setdefault(r['id'], r['genome'])
ids = [i for i in rows if i in gen]
ex = {i: E.express(E.canon(gen[i])) for i in ids}
fast = min(ids, key=lambda i: rows[i][0]); fastnj = min((i for i in ids if not ex[i].get('jit')), key=lambda i: rows[i][0])
q = min(ids, key=lambda i: rows[i][0] * rows[i][1] * rows[i][2]); small = min(ids, key=lambda i: rows[i][1])
def dispatches(g):
    d = os.path.join(E.EV, 'inert-p'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d); E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False
    pw = E.private_work(d); out = {}
    for w in WORKS:
        pf = os.path.join(d, 'p-' + w); E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=300, cpu=60, env=dict(os.environ, VMPROF=pf))
        out[w] = sum(int(f[2]) for f in (x.split() for x in open(pf)) if f and f[0].isdigit() and not (int(f[0]) == 0x7D or 128 <= int(f[1]) <= 255))
    return out
def size(g):
    d = os.path.join(E.EV, 'inert-b'); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d); E.alive(eng, img, E.private_work(d)); return os.path.getsize(eng) + os.path.getsize(img)
o = open(OUT, 'w')
for role, i in (('the fastest', fast), ('the fastest without the JIT', fastnj), ('the best by Q', q), ('the smallest', small)):
    g0 = E.canon(gen[i]); e0 = ex[i]; s0 = size(g0); d0 = dispatches(g0)
    o.write('\n## %s - %s (speed %.3f, %s bytes, %s; JIT %s)\n\n| gene | bytes | %s | verdict |\n|---|---|%s---|\n' % (role, i, rows[i][0], '{:,}'.format(s0), 'tag 2' if e0.get('tag2') else 'plain', bool(e0.get('jit')), ' | '.join(WORKS), '---|' * len(WORKS))); o.flush()
    for x in [k for k in E.EXPRESSED['cv8'] if k not in SKIP and e0.get(k)]:
        off = [] if isinstance(gen[i].get(x), list) else 0
        g1 = E.canon(dict(gen[i], **{x: off}))
        if E.express(g1) == e0: o.write('| %s | - | %s | off changes nothing it expresses |\n' % (x, ' | '.join('-' for _ in WORKS))); o.flush(); continue
        try: s1 = size(g1); d1 = dispatches(g1)
        except Exception as err: o.write('| %s | - | %s | off fails: %s |\n' % (x, ' | '.join('-' for _ in WORKS), str(err)[:60])); o.flush(); continue
        dd = {w: (d1[w] / d0[w] - 1) * 100 if d0[w] else 0.0 for w in WORKS}
        moved = any(abs(v) >= 0.05 for v in dd.values())
        verdict = 'works' if moved else ('inert' if s1 == s0 else 'no run-time effect')
        o.write('| %s | %+d | %s | %s |\n' % (x, s1 - s0, ' | '.join('%+.2f%%' % (-dd[w]) for w in WORKS), verdict)); o.flush()
o.close()
for d in ('inert-p', 'inert-b'): shutil.rmtree(os.path.join(E.EV, d), ignore_errors=True)
