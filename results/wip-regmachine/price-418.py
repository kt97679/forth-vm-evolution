# results/wip-regmachine/README.md - what a register stage could remove from the dispatches of code as it runs.
# python3 THIS ID [ID ...] - each design of seed 58's or 60's front built with the profiler (VMPROF) and the
# converter's opcode names (CALLMAP), run on the workloads; from the profiler's pairs and triples, per workload:
#   bound   - every move and lone literal gone (stackops.py's)
#   pairs   - a move or literal straight before an operation that consumes it, taken in as its operand
#   +chain  - and the one before that, where it too feeds the operation (a triple)
#   control - calls, EXIT, branches and loop words: what no register form removes
# With --top: the patterns taken in, by name, summed over the workloads - what a targeted set of forms would cover.
import collections, json, os, shutil, sys
TOP = '--top' in sys.argv; ids = [a for a in sys.argv[1:] if a != '--top']; sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
MOVE = {'DUP', 'DROP', 'SWAP', 'OVER', 'ROT', '-ROT', 'NIP', 'TUCK', '>R', 'R>', 'R@', '2DUP', '2DROP', '2SWAP', '2OVER', 'I', 'J', 'UNLOOP'}
CONTROL = {'EXIT', 'BRANCH', '?BRANCH', '0BRANCH', '(LOOP)', '(+LOOP)', '(DO)', '(?DO)', 'EXECUTE', 'DOVAR', 'DODOES', 'DOCON'}
recs = {}
for f in ('results/evolve-amd-ryzen-7-pro-8840hs-seed60.md', 'results/evolve-amd-ryzen-7-pro-8840hs-seed58.md'):
    for l in open(f):
        if l.startswith('{"'):
            r = json.loads(l); recs.setdefault(r['id'], r)
WORKS = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'sieve']
for did in ids:
    g = E.canon(recs[did]['genome'])
    d = os.path.join(E.EV, 'rmprice'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d); E.PROFILING[0] = True
    cm = os.path.join(d, 'callmap'); os.environ['CALLMAP'] = cm
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False; os.environ.pop('CALLMAP', None)
    conv = {}
    for l in open(cm):
        f = l.split()
        if f and f[0] == 'O' and len(f) >= 5: conv.setdefault(int(f[3]), (f[2], f[4]))
    def kind(op):
        if op >= 128: return 'C'
        k, n = conv.get(op, ('?', '?'))
        if k in ('LIT', 'LITX') or n.startswith('LIT'): return 'L'
        if k in ('LP', 'BR', 'CALL') or n in CONTROL or n.endswith('BRANCH'): return 'C'
        parts = [p for p in n.replace(';', ' ').replace('|', ' ').split() if p]
        if parts and all(p in MOVE for p in parts): return 'M'
        if any(p in CONTROL for p in parts) or n == '?': return 'C' if n != '?' else '?'
        return 'W'
    pw = E.private_work(d); tops = collections.Counter(); nm = lambda op: 'call' if op >= 128 else conv.get(op, ('?', 'op%d' % op))[1]
    print('## %s (%s, %s bytes)' % (did, 'tag 2' if E.express(g).get('tag2') else 'plain CV8', recs[did].get('total')))
    print('| workload | dispatches | bound | pairs | +chain | control | unnamed |')
    print('|---|---|---|---|---|---|---|')
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=300, cpu=60, env=dict(os.environ, VMPROF=pf))
        by, pr, tr = collections.Counter(), collections.Counter(), collections.Counter()
        for line in open(pf):
            f = line.split()
            if not f: continue
            if f[0] == 'T' and len(f) == 5 and f[1].isdigit(): tr[(int(f[1]), int(f[2]), int(f[3]))] += int(f[4]); continue
            if not f[0].isdigit(): continue
            a, b, k = int(f[0]), int(f[1]), int(f[2])
            if a == 0x7D or 128 <= b <= 255: continue
            by[b] += k; pr[(a, b)] += k
        D = sum(by.values()) or 1
        K = {op: kind(op) for op in set(by) | {a for a, b in pr}}
        bound = sum(k for op, k in by.items() if K.get(op) in ('M', 'L'))
        pairs = sum(k for (a, b), k in pr.items() if K.get(a) in ('M', 'L') and K.get(b) == 'W')
        chain = sum(k for (a, b, c), k in tr.items() if K.get(a, kind(a)) in ('M', 'L') and K.get(b, kind(b)) in ('M', 'L') and K.get(c, kind(c)) == 'W')
        for (a, b), k in pr.items():
            if K.get(a) in ('M', 'L') and K.get(b) == 'W': tops['%s %s' % (nm(a), nm(b))] += k
        for (a, b, c), k in tr.items():
            if K.get(a, kind(a)) in ('M', 'L') and K.get(b, kind(b)) in ('M', 'L') and K.get(c, kind(c)) == 'W': tops['%s %s %s' % (nm(a), nm(b), nm(c))] += k
        ctl = sum(k for op, k in by.items() if K.get(op) == 'C'); unk = sum(k for op, k in by.items() if K.get(op) == '?')
        print('| %s | %d | %.1f%% | %.1f%% | %.1f%% | %.1f%% | %.1f%% |' % (w, D, 100 * bound / D, 100 * pairs / D, 100 * (pairs + chain) / D, 100 * ctl / D, 100 * unk / D), flush=True)
    if TOP:
        tot = sum(tops.values()) or 1
        print('Taken in, the largest: ' + '; '.join('`%s` %.0f%%' % (p, 100 * k / tot) for p, k in tops.most_common(10)))
    print()
