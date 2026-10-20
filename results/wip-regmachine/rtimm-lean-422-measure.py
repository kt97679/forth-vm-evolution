import json, os, shutil, sys, time
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
t = time.time(); E.setup(); print('setup %.0fs' % (time.time() - t), flush=True)
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md') if l.startswith('{"') and '09de03f091' in l)
g0 = dict(r['genome']); WORKS = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann']; base = None
for name, g in [('as it is', g0), ('rtimm=2 lean', dict(g0, rtimm=2)), ('rtimm=2 lean + rtloop=2', dict(g0, rtimm=2, rtloop=2))]:
    g = E.canon(g); d = os.path.join(E.EV, 'rmlean'); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d); ok = E.alive(eng, img, E.private_work(d)); size = os.path.getsize(eng) + os.path.getsize(img)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d); E.PROFILING[0] = True
    try: peng, pimg = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False
    pw = E.private_work(d); disp = {}
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w); E.sh([peng, pimg], cwd=pw, inp=E.program(w), timeout=300, cpu=60, env=dict(os.environ, VMPROF=pf))
        disp[w] = sum(int(f[2]) for f in (l.split() for l in open(pf)) if f and f[0].isdigit() and not (int(f[0]) == 0x7D or 128 <= int(f[1]) <= 255))
    base = base or (size, disp)
    print('%-26s lean %s alive %s | %d bytes (%+d) | %s' % (name, E.rtimm_lean(g), ok, size, size - base[0], ', '.join('%s %+.1f%%' % (w, 100 * (disp[w] / base[1][w] - 1)) for w in WORKS)), flush=True)
