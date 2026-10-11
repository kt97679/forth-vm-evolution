"""hybprice: the hybrid stack/register design priced on every executed dispatch,
run-time code included - from the profiler's opcode pairs (JIT off)."""
import os, sys, json, collections, shutil
os.chdir('/tmp/fb/r'); sys.path.insert(0, '/tmp/fb/r/lab/evolve')
__file__ = '/tmp/fb/r/lab/evolve/regprice.py'; src = open(__file__).read()
sys.argv = ['regprice.py', 's6']
exec(compile(src[:src.index('for did in args:')], __file__, 'exec'))
recs = {}
for f in ('seed38', 'seed39'):
    for l in open('/home/claude/forth-vm-evolution/results/evolve-amd-ryzen-7-pro-8840hs-%s.md' % f):
        if l.startswith('{"bin"'): r = json.loads(l); recs[r['id']] = r
smallest = min((r for r in recs.values() if r['id'] in open('/tmp/s39/run/pack/report.md').read()), key=lambda r: r['size'] + r.get('bin', 0))['id']
WK = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'sieve', 'parse']
for did in ['s6', '9932cc5c32', smallest]:
    g = E.canon(E.HUMAN['s6-cv8b']) if did == 's6' else E.canon(recs[did]['genome'])
    d = os.path.join(E.EV, 'hybprice'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    cm = os.path.join(d, 'callmap'); os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0, jit=0), d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
    opn = {}                                          # the converter's own names: O addr kind opcode name
    for l in open(cm):
        f = l.split()
        if f[0] == 'O' and len(f) >= 5 and f[2] in ('P', 'SP', 'LIT'): opn.setdefault(int(f[3]), f[4])
    SAMPLE = sorted(set(v for v in opn.values() if not v.isalpha()))[:12]
    def name(op):
        if op >= 128: return ('call',)
        v = opn.get(op)
        if v is None: return ('op%d' % op,)
        for sep in ('+', '_', '|'):
            if sep in v and v not in ('+', '1+', '2+', 'D+', 'M+', '+!'): return tuple(x for x in v.split(sep) if x)
        return (v,)
    print('names sample: %s; %d opcodes named' % (' '.join(SAMPLE), len(opn)))
    pw = E.private_work(d)
    print('\n## %s%s (JIT %s)\n' % (did, ' - the smallest of seed 39' if did == smallest else '', 'on' if g.get('jit') else 'off'))
    print('| workload | dispatches | unnamed | moves (bound) | move -> use | R-stack -> use | literal -> binop | absorbed: top pairs |')
    print('|---|---|---|---|---|---|---|---|')
    for w in WK:
        pf = os.path.join(d, 'prof-' + w)
        if os.path.exists(pf): os.remove(pf)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=600, cpu=60, env=dict(os.environ, VMPROF=pf))
        pairs = collections.Counter()
        for line in open(pf):
            f = line.split()
            if len(f) == 3 and f[0].lstrip('-').isdigit(): pairs[(int(f[0]), int(f[1]))] += int(f[2])
        total = sum(c for (i, j), c in pairs.items())
        byop = collections.Counter()
        for (i, j), c in pairs.items(): byop[j] += c
        moves = sum(c for op, c in byop.items() if all(x in MOVE for x in name(op)))
        unk = sum(c for op, c in byop.items() if name(op)[0].startswith('op'))
        mu = ru = lb = 0; top = collections.Counter()
        for (i, j), c in pairs.items():
            a, b = name(i), name(j)
            if a[-1] in MOVE and (len(a) == 1 or all(x in MOVE for x in a)) and b[0] in USE and b[0] not in PRODUCE:
                mu += c; top[' '.join(a) + ' > ' + b[0]] += c
            elif a[-1] in RMOVE and len(a) == 1 and a[0] != '>R' and b[0] in USE and b[0] not in PRODUCE: ru += c
            elif a == ('LIT',) and b[0] in ('+', '-', 'AND', 'OR', 'XOR', '=', '<', '>', 'U<', '*', 'LSHIFT', 'RSHIFT'): lb += c
        pc = lambda x: '%.1f%%' % (100.0 * x / total) if total else '-'
        print('| %s | %s | %s | %s | %s | %s | %s | %s |' % (w, format(total, ','), pc(unk), pc(moves), pc(mu), pc(ru), pc(lb),
              ', '.join('%s %s' % (k, pc(v)) for k, v in top.most_common(4))), flush=True)
