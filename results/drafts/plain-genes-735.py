#!/usr/bin/env python3
"""results/drafts/plain-genes-735.py 8|4 off|on - the plain design (cv8 and byte headers alone - the -b dump) with hashk, chainorder
and numfirst (Iteration 735; the rehearsal's short run: 395e2f44e9, hashk on, "no HASH8 in the dump"): off, the image and
engine's hashes (to compare between two trees); on, each gene and all three built and four workloads' outputs hashed
against off. The genome: results/drafts/plain-genes-735.json (395e2f44e9 as it died). From the top of
a built tree as the build user, python3 -B."""
ROOT = os.getcwd(); sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); w4 = sys.argv[1] == '4'; mode = sys.argv[2]; sys.argv = ['x']
import evolve as E
if w4: os.environ.update(E.W4_ENV)
E.setup()
g = dict(json.load(open(os.path.join(ROOT, 'results', 'drafts', 'plain-genes-735.json')))['genome'], hashk=0)
sha = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()[:16]
if mode == 'off':
    eng, img = E.build(E.canon(g), os.path.join(E.EV, 'plain-off-%s' % w4)); print('off', sha(img), os.path.getsize(img), sha(eng))
else:
    out = {}
    for tag, on in (('off', {}), ('hashk', {'hashk': 1}), ('chainorder', {'chainorder': 1}), ('numfirst', {'numfirst': 1}), ('all3', {'hashk': 1, 'chainorder': 1, 'numfirst': 1})):
        d = os.path.join(E.EV, 'plain-%s-%s' % (tag, w4)); eng, img = E.build(E.canon(dict(g, **on)), d); pw = E.private_work(d)
        out[tag] = [hashlib.sha1(subprocess.run([eng, img], input=E.program(w), capture_output=True, cwd=pw, timeout=600).stdout).hexdigest()[:12] for w in ('kernel', 'corpus', 'parse', 'apps')]
        print(tag, os.path.getsize(img), out[tag], 'same' if out[tag] == out['off'] else 'DIFFER', flush=True)
