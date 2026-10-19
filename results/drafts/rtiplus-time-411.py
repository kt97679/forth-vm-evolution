# Iteration 411: seed 60's fastest interpreted design with and without rtiplus (I + compiled as I+ at run time), measured
# against s6 on the six selection workloads (evolve.measure, medians of 5 rounds).
import json, os, shutil, sys
os.chdir('/home/claude/forth-vm-evolution'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed60.md') if l.startswith('{"') and '4ac602c8bd' in l)
works = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann']; M = {}
for v in (0, 1):
    g = E.canon(dict(r['genome'], rtiplus=v)); d = os.path.join(E.EV, 'rti%d' % v); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw)
    M[v] = E.measure(eng, img, pw, works, 5)[0]
    print('rtiplus=%d (expressed %s), image %d bytes: %s' % (v, E.express(g).get('rtiplus'), os.path.getsize(img), {w: round(M[v][w], 3) for w in works}), flush=True)
import math
gm = lambda m: math.exp(sum(math.log(m[w]) for w in works) / len(works))
print('change with rtiplus: ' + ', '.join('%s %+.1f%%' % (w, 100 * (M[1][w] / M[0][w] - 1)) for w in works) + ' | geometric mean %+.1f%%' % (100 * (gm(M[1]) / gm(M[0]) - 1)))
