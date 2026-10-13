import os, sys, json, re
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
f46 = [json.loads(l)['id'] for l in open('/home/claude/forth-vm-evolution/results/evolve-amd-ryzen-7-pro-8840hs-seed46.md') if l.startswith('{"bin"')]
cf = open('/tmp/c46/pack/compare-fronts.md').read()
line = [l for l in cf.split('\n') if l.startswith('The front of all runs together')][0]
joint = re.findall(r'\b([0-9a-f]{10}) [0-9.]+ at', line)
ids = list(dict.fromkeys(f46 + joint)); bad = 0
for did in ids:
    d = os.path.join(E.EV, 'g46')
    try: eng, img = E.build(E.canon(E.recorded_genome(did)), d); E.alive(eng, img, E.private_work(d))
    except Exception as e: bad += 1; print('DIED', did, str(e)[:120], flush=True)
print('alive: %d of %d (seed 46 front %d, joint front %d, %d in both)' % (len(ids) - bad, len(ids), len(f46), len(joint), len(f46) + len(joint) - len(ids)), flush=True)
