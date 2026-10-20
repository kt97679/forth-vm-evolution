import json, os, shutil, sys
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
R = {}
for f in ('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md', 'results/evolve-amd-ryzen-7-pro-8840hs-seed60.md'):
    for l in open(f):
        if l.startswith('{"'): x = json.loads(l); R[x['id']] = (f[-6:-3], x)
WORKS = ['kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann']
SRC = (': L1 ( -- n ) 0 10 0 DO I + LOOP ;\nL1 .\n: L2 ( -- n ) 0 4 0 DO 3 0 DO I J * + LOOP LOOP ;\nL2 .\n'
       ': L3 ( -- n ) 0 100 0 DO I 7 = IF I UNLOOP EXIT THEN LOOP ;\nL3 .\n: L4 ( n -- m ) 0 SWAP 0 ?DO 1+ LOOP ;\n5 L4 . 0 L4 .\n'
       ': L5 ( -- n ) 0 20 0 DO I 9 > IF LEAVE THEN 1+ LOOP ;\nL5 .\n: L6 ( -- n ) 0 30 0 DO I + 5 +LOOP ;\nL6 .\nBYE\n')
g0 = dict(R['09de03f091'][1]['genome']); base = None
def run(g, prof):
    d = os.path.join(E.EV, 'rml'); shutil.rmtree(d, ignore_errors=True); g = E.canon(g)
    if not prof:
        eng, img = E.build(g, d); pw = E.private_work(d); E.alive(eng, img, pw)
        out = getattr(E.sh([eng, img], cwd=pw, inp=SRC.encode(), timeout=60, cpu=20), 'stdout', b'')
        return os.path.getsize(eng) + os.path.getsize(img), ' '.join(x for x in out.decode('latin-1').split() if x.lstrip('-').isdigit())
    os.makedirs(d); E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)
    finally: E.PROFILING[0] = False
    pw = E.private_work(d); disp = {}
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w); E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=300, cpu=60, env=dict(os.environ, VMPROF=pf))
        disp[w] = sum(int(f[2]) for f in (l.split() for l in open(pf)) if f and f[0].isdigit() and not (int(f[0]) == 0x7D or 128 <= int(f[1]) <= 255))
    return disp
for cell in (8, 4):
    for name, g in [('as it is', g0), ('rtloop=1', dict(g0, rtloop=1)), ('rtloop=2', dict(g0, rtloop=2))]:
        size, out = run(dict(g, cell=cell), False)
        print('cell %d %-9s %d bytes | L1..L6: %s' % (cell, name, size, out), flush=True)
b = run(g0, True); n = run(dict(g0, rtloop=2), True)
print('rtloop=2 dispatches against as it is: ' + ', '.join('%s %+.1f%%' % (w, 100 * (n[w] / b[w] - 1)) for w in WORKS), flush=True)
ok = bad = 0; deltas = []
for did, (s, r) in R.items():
    g = E.canon(r['genome'])
    if not E.rtloop_on(g): continue
    try: size, _ = run(r['genome'], False); ok += 1; deltas.append(size - r['total'])
    except Exception as x: bad += 1; print('%s %s: %s' % (s, did, str(x)[:150]), flush=True)
deltas.sort(); print('front designs with the loop compiler: %d alive, %d failed; bytes against their records: min %+d, median %+d, max %+d' % (ok, bad, deltas[0], deltas[len(deltas) // 2], deltas[-1]) if deltas else 'none')
