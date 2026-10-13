import os, sys, json
sys.argv = ['x']; sys.path.insert(0, '/tmp/b44/lab/evolve'); import evolve as E
E.setup()
recs = [json.loads(l) for l in open('/tmp/b44/results/evolve-amd-ryzen-7-pro-8840hs-seed43.md') if l.startswith('{"bin"')]
bad = 0; n = 0
for r in recs:
    if r['genome'].get('fsys', 0): continue
    n += 1; d = os.path.join(E.EV, 'g44')
    try: eng, img = E.build(E.canon(r['genome']), d); E.alive(eng, img, E.private_work(d))
    except Exception as e: bad += 1; print('DIED', r['id'], e)
print('fsys 0 front designs alive: %d of %d' % (n - bad, n))
