import os, sys, json
TREE = sys.argv[1]; ids = sys.argv[2].split(','); works = sys.argv[3].split(',')
sys.argv = ['x']; sys.path.insert(0, TREE + '/lab/evolve'); import evolve as E
E.setup()
out = {}
for did in ids:
    d = os.path.join('/tmp/pm', did); eng, img = E.build(E.canon(E.recorded_genome(did)), d); pw = E.private_work(d)
    progs = {}
    for w in works:
        p = E.program(w).decode()
        if p.rstrip().endswith('BYE'): p = p.rstrip()[:-3]
        progs[w] = p
    out[did] = {'eng': eng, 'img': img, 'pw': pw, 'progs': progs}
json.dump(out, open('/tmp/pm/builds.json', 'w'))
print('built', ', '.join(ids))
