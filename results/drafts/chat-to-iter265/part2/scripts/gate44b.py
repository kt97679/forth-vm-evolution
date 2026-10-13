import os, sys, json
sys.argv = ['x']; sys.path.insert(0, '/tmp/b44/lab/evolve'); import evolve as E
E.setup()
recs = [json.loads(l) for l in open('/tmp/b44/results/evolve-amd-ryzen-7-pro-8840hs-seed43.md') if l.startswith('{"bin"')]
bad = n = 0
for r in recs:
    if r['genome'].get('fsys', 0) > 2: continue
    n += 1; d = os.path.join(E.EV, 'g44b')
    try: eng, img = E.build(E.canon(r['genome']), d); E.alive(eng, img, E.private_work(d))
    except Exception as e: bad += 1; print('DIED', r['id'], e, flush=True)
print('native READ-LINE front designs alive: %d of %d' % (n - bad, n), flush=True)
