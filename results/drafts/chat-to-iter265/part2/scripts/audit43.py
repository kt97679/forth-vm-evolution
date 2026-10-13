import json, os, sys, time
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
R = {}
for l in open('/tmp/seed43/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
for i in ('8dab7c6af4', '5116aa0812', 'add5ec8937', 'cc6d168e0a'):
    t0 = time.time(); d = os.path.join(E.EV, 'audit43')
    eng, img = E.build(E.canon(R[i]['genome']), d); t1 = time.time()
    E.alive(eng, img, E.private_work(d)); t2 = time.time()
    print('%s fsys %s: image %d (recorded %d), engine %d (recorded %d); build %.1f s, alive %.1f s' % (i, R[i]['genome'].get('fsys', 0),
          os.path.getsize(img), R[i]['size'], os.path.getsize(eng), R[i]['bin'], t1 - t0, t2 - t1), flush=True)
