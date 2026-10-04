#!/usr/bin/env python3
"""price.py ID [ID ...] [--db FILE] - what a fusion could save, before building it.

Builds each design with the engine's profiler (VMPROF), runs the four
selection workloads, and reads the stream of operations the design really
dispatches - its own pairs, words and specialisations already fused. For
each workload, as shares of all dispatches (upper bounds: overlaps and the
opcode slots a fusion would need are ignored):

  pairs save        dispatches the design's pairs already removed
  triples           a pair and a primitive next to it: what the best 8 and
                    16 three-operation fusions could add
  next 16 pairs     the hottest primitive pairs still unfused - what more
                    opcode slots (a second escape level) could host
                    CAUTION (Iteration 11): pairs and triples OVERLAP - DUP >R,
                    >R DUP and SWAP DUP count the same operations, each fusable
                    once - so these two columns overstate, by 3-10 times: the
                    nine best of the next 16, given slots, removed 0.2-2.4%
                    where this column said 6.4-12.9%. A test before a branch
                    cannot overlap: that column held (4% priced, 3% measured).
  test -> branch    a test followed by a conditional branch, by test - what
                    fusing them could save
  calls, EXIT       how much of the stream they are

prompts/10: price a change before making it. Iteration 8 priced triples
with this (not built: 0-4% of dispatches) and found the tests before
conditional branches (7-9% on every workload). Names come from the
kernel's primitives, the design's pairs and format-10 words, and the
engine's specialisation band (engine/vm-lab.c, from 0x60).
"""
import collections, json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; db = os.path.join(HERE, '..', '..', 'build', 'evolve', 'db.jsonl')
if '--db' in args: i = args.index('--db'); db = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
recs = {}
for l in open(db):
    try: r = json.loads(l); recs[r['id']] = r
    except ValueError: pass
prims = [l.split()[1] for l in open(os.path.join(E.ROOT, 'forth', 'kernel.4')) if l.startswith('PRIMITIVE')]
src = open(os.path.join(E.ROOT, 'engine', 'vm-lab.c')).read()
band = src[src.index('#if ENC == 3 && SPEC\n        [0x60]'):]; band = band[:band.index('#endif')]
SPECBAND = {0x60 + k: n for k, n in enumerate(re.findall(r'&&L_(\w+)', band))}
TESTS = {'<', '=', 'U<', '0=', '0<', '>', 'U>', '<>', '0<>', 'zeq', 'eqi', 'eqix', 'ne', 'zlt', 'sgt', 'sub', '-'}
BRANCHES = {'?BRANCH', '?BRANCH8', '0BRANCH', 'x_qbr8'}
for did in args:
    if did not in recs: sys.exit('no design %s in %s' % (did, db))
    g = E.canon(recs[did]['genome'])
    def prim(op):              # a fusable primitive (as design_pairs)
        if g.get('escape') == 2: i = op if op < 27 else None
        elif g.get('escape'): i = op if op < 32 else op + 1 if op < 36 else None
        else: i = op if op < 68 else None
        return prims[i] if i is not None and i < 33 and prims[i] not in E.PAIRS_BAD else None
    sup = {x[2]: '%s+%s' % (x[0], x[1]) for x in E.supers_in(g)}
    o10 = {o: w for w, o in E.ops10_in(g)}
    def name(op):
        if op in sup: return sup[op]
        if op in o10: return o10[op]
        if op >= 128: return 'call'
        if g.get('escape') == 2: i = op if op < 27 else None
        elif g.get('escape'): i = op if op < 32 else op + 1 if op < 36 else None
        else: i = op if op < 68 else None
        if i is not None and i < len(prims): return prims[i]
        return SPECBAND.get(op, 'op%d' % op)
    d = os.path.join(E.EV, 'price'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)      # the stream, not the dispatch, is what is priced
    finally: E.PROFILING[0] = False
    pw = E.private_work(d)
    D, P, CALL, EXIT = (collections.Counter() for _ in range(4))
    T, UP, PRE = (collections.Counter() for _ in range(3))
    for w in E.WORK_SEL:
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
        for line in open(pf):
            m = re.match(r'^(\d+) (\d+) (\d+)$', line)
            if not m: continue
            a, b, k = map(int, m.groups())
            # Iteration 13: two profiler events that are not dispatches - L_esc profiles its
            # selector (pairs out of 125), and with the 256-entry dispatch NEXT profiles a
            # call's first byte before do_call profiles 256 (pairs into 128-255). Counted,
            # they inflated D by the calls (8% of kernel's) and doubled the calls column.
            if a == 0x7D or 128 <= b <= 255: continue
            D[w] += k
            na, nb = name(a), name(b)
            if b in sup: P[w] += k
            if a in sup and prim(b): T[(w, sup[a] + '+' + prim(b))] += k
            if b in sup and prim(a): T[(w, prim(a) + '+' + sup[b])] += k
            if prim(a) and prim(b): UP[(w, prim(a) + ' ' + prim(b))] += k
            if nb in BRANCHES and na in TESTS: PRE[(w, na)] += k
            if nb == 'call': CALL[w] += k
            if nb == 'EXIT': EXIT[w] += k
    shutil.rmtree(d, ignore_errors=True)
    mean = collections.Counter()
    for (w, t), k in T.items(): mean[t] += k / D[w] / len(E.WORK_SEL)
    best = [t for t, _ in mean.most_common(16)]
    print('## %s - %d pairs, %d format-10 words\n' % (did, len(sup), len(o10)))
    print('| workload | dispatches | pairs save | best 8 triples (overlap: overstated) | best 16 | next 16 pairs (overlap: overstated) | test -> branch | calls | EXIT |')
    print('|---|---|---|---|---|---|---|---|---|')
    for w in E.WORK_SEL:
        up = sorted((k for (ww, _), k in UP.items() if ww == w), reverse=True)
        pct = lambda k: '%.1f%%' % (100 * k / D[w])
        print('| %s | %d | %.1f%% | %s | %s | %s | %s | %s | %s |' % (
            w, D[w], 100 * P[w] / (D[w] + P[w]), pct(sum(T[(w, t)] for t in best[:8])), pct(sum(T[(w, t)] for t in best[:16])),
            pct(sum(up[:16])), pct(sum(k for (ww, _), k in PRE.items() if ww == w)), pct(CALL[w]), pct(EXIT[w])))
    print('\nthe tests before a conditional branch, by workload:')
    for w in E.WORK_SEL:
        pre = sorted(((k, n) for (ww, n), k in PRE.items() if ww == w), reverse=True)[:5]
        print('  %-7s %s' % (w, ', '.join('%s %.1f%%' % (n, 100 * k / D[w]) for k, n in pre) or '-'))
    print('the best triples, mean share: %s\n' % ', '.join('%s %.1f%%' % (t, 100 * mean[t]) for t in best[:6]))
