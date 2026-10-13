import os, sys, re, json, subprocess
TREE = sys.argv[1]; ids = sys.argv[2].split(','); works = sys.argv[3].split(',')
sys.argv = ['x']; sys.path.insert(0, TREE + '/lab/evolve'); import evolve as E
E.setup()
for did in ids:
    for fb in (0, 2):
        g = E.canon(dict(E.recorded_genome(did), fbuf=fb)); d = os.path.join(E.EV, 'pages')
        eng, img = E.build(g, d); pw = E.private_work(d); out = []
        for w in works:
            r = subprocess.run([E.CPUT, eng, img], cwd=pw, input=E.program(w), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
            m = re.search(rb'^MINFLT (\d+)', r.stderr, re.M); out.append('%s %d KB' % (w, int(m.group(1)) * 4 if m else -1))
        print('%s fbuf=%d: %s' % (did, fb, ', '.join(out)), flush=True)
