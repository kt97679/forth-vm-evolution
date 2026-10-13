import json, os, re, sys, time
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
R = {}
for l in open('/tmp/seed43/pack/db.jsonl'):
    try: r = json.loads(l); R[r['id']] = r
    except ValueError: pass
front = list(dict.fromkeys(m.group(1) for l in open('/tmp/seed43/pack/report.md') for m in [re.match(r'^\| ([0-9a-f]{10}) \|', l)] if m))
cf = open('/tmp/cf43/pack/compare-fronts.md').read()
joint = re.findall(r'([0-9a-f]{10}) [0-9.]+ at', re.search(r'The front of all runs together \(speed, binary \+ image, peak memory\), by binary \+ image: (.*)', cf).group(1))
ids = list(dict.fromkeys(front + joint)); bad = []; t0 = time.time()
print('%d designs: the run front %d, the joint front %d' % (len(ids), len(front), len(joint)), flush=True)
for n, i in enumerate(ids, 1):
    d = os.path.join(E.EV, 'alive43')
    try:
        eng, img = E.build(E.canon(R[i]['genome']), d)
        E.alive(eng, img, E.private_work(d)); ok = 'alive'
    except Exception as e: ok = 'DIED %s' % str(e)[:100]; bad.append(i)
    print('%3d %s fsys %s: %s (%.0f s)' % (n, i, R[i]['genome'].get('fsys', 0), ok, time.time() - t0), flush=True)
print('ALIVE %d of %d%s' % (len(ids) - len(bad), len(ids), ('; died: ' + ' '.join(bad)) if bad else ''), flush=True)
