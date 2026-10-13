import os, sys, json
sys.argv = ['x']; sys.path.insert(0, '/tmp/b44s/lab/evolve'); import evolve as E
E.setup()
recs = [json.loads(l) for l in open('/tmp/b44s/results/evolve-amd-ryzen-7-pro-8840hs-seed43.md') if l.startswith('{"bin"')]
bad = n = 0
for r in recs:
    for lev in ((3, 4, 5) if r['genome'].get('fsys', 0) >= 3 else ()):
        n += 1; d = os.path.join(E.EV, 'g44c')
        try: eng, img = E.build(E.canon(dict(r['genome'], fsys=lev)), d); E.alive(eng, img, E.private_work(d))
        except Exception as e: bad += 1; print('DIED', r['id'], lev, e, flush=True)
print('seed 43 front designs with fsys 3-4, each at fsys 3, 4 and 5: %d of %d alive' % (n - bad, n), flush=True)
