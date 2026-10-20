import json, os, shutil, sys
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
rows = []
for f in ('results/evolve-amd-ryzen-7-pro-8840hs-seed58.md', 'results/evolve-amd-ryzen-7-pro-8840hs-seed60.md'):
    for l in open(f):
        if l.startswith('{"'):
            r = json.loads(l); g = E.canon(r['genome'])
            if E.express(g).get('rtimm') == 2: rows.append((f[-6:-3], r, g))
print('%d front designs with rtimm=2 expressed' % len(rows), flush=True)
lean = same = bad = 0; saved = []
for s, r, g in rows:
    d = os.path.join(E.EV, 'rmf'); shutil.rmtree(d, ignore_errors=True)
    try:
        eng, img = E.build(g, d); E.alive(eng, img, E.private_work(d)); size = os.path.getsize(eng) + os.path.getsize(img)
    except Exception as x:
        bad += 1; print('%s %s: %s' % (s, r['id'], str(x)[:120]), flush=True); continue
    if E.rtimm_lean(g): lean += 1; saved.append(size - r['total'])
    elif size == r['total']: same += 1
    else: print('%s %s not lean, %d bytes, record %d' % (s, r['id'], size, r['total']), flush=True)
print('lean %d (bytes against the record: %s), not lean and unchanged %d, failures %d' % (lean, ' '.join('%+d' % x for x in sorted(saved)), same, bad))
