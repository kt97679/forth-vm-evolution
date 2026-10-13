import os, sys, json, re
sys.argv = ['x']; sys.path.insert(0, '/tmp/b45/lab/evolve'); import evolve as E
E.setup()
f44 = [json.loads(l)['id'] for l in open('/home/claude/forth-vm-evolution/results/evolve-amd-ryzen-7-pro-8840hs-seed44.md') if l.startswith('{"bin"')]
cf = open('/tmp/cf44/pack/compare-fronts.md').read()
line = [l for l in cf.split('\n') if l.startswith('The front of all runs together')][0]
joint = re.findall(r'\b([0-9a-f]{10}) [0-9.]+ at', line)
ids = list(dict.fromkeys(f44 + joint)); bad = 0
for did in ids:
    d = os.path.join(E.EV, 'g45')
    try: eng, img = E.build(E.canon(E.recorded_genome(did)), d); E.alive(eng, img, E.private_work(d))
    except Exception as e: bad += 1; print('DIED', did, str(e)[:120], flush=True)
print('alive: %d of %d (seed 44 front %d, joint front %d, %d in both)' % (len(ids) - bad, len(ids), len(f44), len(joint), len(f44) + len(joint) - len(ids)), flush=True)
pick = sorted(f44, key=lambda i: E.recorded_genome(i) and 0)[:0]
