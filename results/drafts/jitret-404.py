# results/jitret-404.md - python3 THIS TREE ROUNDS, its stages built with the pending batch to patch 8.
# Iteration 404: the JIT design of engines-check, jitret 0 and 1 - built, alive, its engine not the same, and
# measured against s6 on the selection's workloads (evolve.measure: medians of R rounds, s6 run beside it).
import os, shutil, sys
tree, R = sys.argv[1], int(sys.argv[2]); os.chdir(tree); sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab/evolve')); import evolve as E
E.setup(); S6 = dict(E.HUMAN['s6-cv8b'])
JIT = dict(tag2=1, jit=1, jitx=1, jitloop=1, jitinl=1, jittail=1)
works = ['ackermann', 'fib', 'bubble', 'loop', 'corpus', 'kernel']
out, M = {}, {}
for r in (0, 1):
    g = E.canon(dict(S6, **JIT, jitret=r)); d = os.path.join(E.EV, 'jr%d' % r); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw); out[r] = open(eng, 'rb').read()
    M[r] = E.measure(eng, img, pw, works, R)
    print('jitret=%d (expressed %s): alive; measure: %s' % (r, E.express(g).get('jitret'), M[r]), flush=True)
print('engines differ: %s' % (out[0] != out[1]))
