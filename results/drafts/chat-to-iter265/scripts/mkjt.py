import sys, json
sys.argv = ['x']; sys.path.insert(0, '/tmp/b46b/lab/evolve'); import evolve as E
with open('/tmp/b46b/results/tmp-jittail.md', 'w') as f:
    for fake, real in (('jt28677d13', '28677d13b1'), ('jt0af26c8e', '0af26c8e89')):
        g = dict(E.recorded_genome(real), jittail=1)
        f.write(json.dumps({'id': fake, 'genome': g}) + '\n')
print(open('/tmp/b46b/results/tmp-jittail.md').read()[:200])
