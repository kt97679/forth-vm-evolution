import os, sys, json
sys.argv = ['x']; sys.path.insert(0, '/tmp/b44s/lab/evolve'); import evolve as E
E.setup()
recs = [json.loads(l) for l in open('/tmp/b44s/results/evolve-amd-ryzen-7-pro-8840hs-seed43.md') if l.startswith('{"bin"')]
bad = 0
for r in recs:
    d = os.path.join(E.EV, 'g44d')
    try: eng, img = E.build(E.canon(r['genome']), d); E.alive(eng, img, E.private_work(d))
    except Exception as e: bad += 1; print('DIED', r['id'], e, flush=True)
print('seed 43 front designs alive: %d of %d' % (len(recs) - bad, len(recs)), flush=True)
