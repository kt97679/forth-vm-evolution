# results/wip-regmachine/README.md, "What exists already" - seed 58's smallest design (plain CV8, no run-time fuser) with
# the fusions the project already has turned on: the run-time fuser and its immediates (rtfuse, rtimm, with DUP<I and
# DUP+I first among its format-10 words), then the loop words and I+ (rtloopall, rtiplus). Per variant: binary + image
# bytes (a plain build) and the dispatches of each workload (the profiler's - deterministic).
import collections, json, os, shutil, sys
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
# Iteration 419, the second try: the first prepended to the format-10 words and so pushed others out of their slots -
# now nothing else changes; rtloop alone (its run-time loop compiler), on the smallest and on a larger design.
R = {}
for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md'):
    if l.startswith('{"'):
        x = json.loads(l); R[x['id']] = x['genome']
V = []
for did in ('09de03f091', 'b966d06523'):
    V += [(did + ' as it is', dict(R[did])), (did + ' + rtloop', dict(R[did], rtloop=1))]
WORKS = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann']; base = None
for name, g in V:
    g = E.canon(g); e = E.express(g)
    d = os.path.join(E.EV, 'rmex'); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d); E.alive(eng, img, E.private_work(d)); size = os.path.getsize(eng) + os.path.getsize(img)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d); E.PROFILING[0] = True
    try: peng, pimg = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False
    pw = E.private_work(d); disp = {}
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w); E.sh([peng, pimg], cwd=pw, inp=E.program(w), timeout=300, cpu=60, env=dict(os.environ, VMPROF=pf))
        n = 0
        for line in open(pf):
            f = line.split()
            if f and f[0].isdigit() and not (int(f[0]) == 0x7D or 128 <= int(f[1]) <= 255): n += int(f[2])
        disp[w] = n
    if name.endswith('as it is'): base = (size, disp)
    print('%-32s on: %s | %d bytes (%+d) | %s' % (name, ','.join(k for k in ('rtfuse', 'rtimm', 'rtloop', 'rtloopall', 'rtiplus') if e.get(k)) or '-', size, size - base[0],
          ', '.join('%s %+.1f%%' % (w, 100 * (disp[w] / base[1][w] - 1)) for w in WORKS)), flush=True)
