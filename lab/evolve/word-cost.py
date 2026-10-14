#!/usr/bin/env python3
"""word-cost.py ID[,ID...] WORD[,WORD...] - the dispatches each workload spends inside
chosen words, on chosen designs (Iteration 281, the second source audit).

Builds each design with the call map and the profiler (as hotwords.py does, the JIT
off: the interpreter's view), runs the selection workloads, and charges every
dispatched instruction to the word whose body holds it - a word's SELF cost. A word
made an opcode saves at most that: its body's dispatches go, the call's one becomes
the opcode's (the words it calls keep their own costs). Exact counts: the price is
measured here, not on the laptop's clock. `s6` names the hand-made s6.

    python3 lab/evolve/word-cost.py s6,7535695a36 2@,2!,DEPTH
"""
import bisect, collections, glob, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
if len(sys.argv) != 3: sys.exit(__doc__)
ids, words = sys.argv[1].split(','), sys.argv[2].split(',')
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
print('| design | workload | dispatches | ' + ' | '.join('in %s' % w for w in words) + ' | all of them |')
print('|---|---|---|' + '---|' * (len(words) + 1))
for ident in ids:
    g = dict(E.HUMAN['s6-cv8b']) if ident == 's6' else E.recorded_genome(ident)
    if g is None: sys.exit('word-cost: no recorded design %s' % ident)
    g = dict(E.canon(g), jit=0, tail=0, msc=0)
    d = os.path.join(E.EV, 'word-cost'); shutil.rmtree(d, ignore_errors=True)
    cm = d + '.map'; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    try: eng, img = E.build(g, d)
    finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
    W = sorted((int(f[1]), int(f[2]), ' '.join(f[4:])) for f in (l.rstrip('\n').split(' ') for l in open(cm)) if f[0] == 'W')
    at = [w[0] for w in W]; pw = E.private_work(d)
    missing = [w for w in words if w not in {x[2] for x in W}]
    if missing: print('| %s | - | the design has no word %s | %s |' % (ident, ', '.join(missing), ' | ' * len(words)))
    for wl in E.WORK_SEL:
        pf = os.path.join(d, 'p-' + wl)
        E.sh([eng, img], cwd=pw, inp=E.program(wl), timeout=240, cpu=20, env=dict(os.environ, VMPROF=pf))
        tot, inw = 0, collections.Counter()
        for f in (l.split() for l in open(pf)):
            if f[0] != 'I': continue
            a, n = int(f[1]), int(f[2]); tot += n
            i = bisect.bisect_right(at, a) - 1
            if i >= 0 and W[i][0] <= a < W[i][1] and W[i][2] in words: inw[W[i][2]] += n
        print('| %s | %s | %d | %s | %.1f%% |' % (ident, wl, tot, ' | '.join('%d (%.1f%%)' % (inw[w], 100.0 * inw[w] / tot) for w in words),
              100.0 * sum(inw.values()) / tot))
    shutil.rmtree(d, ignore_errors=True); os.path.exists(cm) and os.remove(cm)
