"""hybprice: the hybrid stack/register design priced on every executed dispatch,
run-time code included - from the profiler's opcode pairs (JIT off)."""
import os, sys, json, collections, shutil
os.chdir('/tmp/fb/r'); sys.path.insert(0, '/tmp/fb/r/lab/evolve')
__file__ = '/tmp/fb/r/lab/evolve/regprice.py'; src = open(__file__).read()
sys.argv = ['regprice.py', 's6']
exec(compile(src[:src.index('for did in args:')], __file__, 'exec'))
recs = {}
for l in open('/tmp/s40/run/pack/report.md'):
    if l.startswith('{"bin"'): r = json.loads(l); recs[r['id']] = r
smallest = min(recs.values(), key=lambda r: r['size'] + r.get('bin', 0))['id']
WK = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'sieve', 'parse']
for did in ['s6', 'd9247d19b0', smallest]:
    g = E.canon(E.HUMAN['s6-cv8b']) if did == 's6' else E.canon(recs[did]['genome'])
    d = os.path.join(E.EV, 'hybprice'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    cm = os.path.join(d, 'callmap'); os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0, jit=0), d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
    opn = {}                                          # the converter's own names: O addr kind opcode name
    for l in open(cm):
        f = l.split()
        if f[0] == 'O' and len(f) >= 5: opn.setdefault(int(f[3]), f[4])
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
    print('\n## %s%s (JIT %s)\n' % (did, ' - the smallest of seed 40' if did == smallest else '', 'on' if g.get('jit') else 'off'))
    IMM = {'ADDI', 'EQI', 'EQIH', 'ADDIX', 'EQIX', 'addi', 'eqi'} | set(TESTBR)
    UX = set(USE) | IMM | {'?BRANCH'}
    BIN = {'+', '-', 'AND', 'OR', 'XOR', '=', '<', '>', 'U<', 'U>', '*', 'LSHIFT', 'RSHIFT', '<>', 'MIN', 'MAX', '/', 'MOD', '+!'}
    mv = lambda n: all(x in MOVE for x in n)
    use = lambda n: n[0] in UX and n[0] not in PRODUCE
    lit = lambda n: len(n) == 1 and n[0].startswith('LIT')
    print('| workload | dispatches | unnamed | moves (bound) | moves absorbed: next op | through a literal | through a move | literals -> immediates | saved |')
    print('|---|---|---|---|---|---|---|---|---|')
    for w in WK:
        pf = os.path.join(d, 'prof-' + w)
        if os.path.exists(pf): os.remove(pf)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=900, cpu=120, env=dict(os.environ, VMPROF=pf))
        pairs, trips = collections.Counter(), collections.Counter()
        for line in open(pf):
            f = line.split()
            if len(f) == 3 and f[0].lstrip('-').isdigit(): pairs[(int(f[0]), int(f[1]))] += int(f[2])
            elif f[0] == 'T': trips[(int(f[1]), int(f[2]), int(f[3]))] += int(f[4])
        total = sum(pairs.values()); byop = collections.Counter()
        for (i, j), c in pairs.items(): byop[j] += c
        moves = sum(c for op, c in byop.items() if mv(name(op)))
        unk = sum(c for op, c in byop.items() if name(op)[0].startswith('op'))
        a1 = a2 = a3 = 0
        for (m, x, y), c in trips.items():
            nm, nx, ny = name(m), name(x), name(y)
            if not mv(nm): continue
            if use(nx): a1 += c
            elif lit(nx) and ny[0] in BIN: a2 += c
            elif mv(nx) and use(ny): a3 += c
        li = sum(c for (x, y), c in pairs.items() if lit(name(x)) and name(y)[0] in BIN)
        pc = lambda x: '%.1f%%' % (100.0 * x / total) if total else '-'
        print('| %s | %s | %s | %s | %s | %s | %s | %s | **%s** |' % (w, format(total, ','), pc(unk), pc(moves), pc(a1), pc(a2), pc(a3), pc(li), pc(a1 + a2 + a3 + li)), flush=True)
