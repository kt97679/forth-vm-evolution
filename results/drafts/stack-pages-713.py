# results/drafts/stack-pages-713.py ROOT IDS N LIST (Iteration 713, results/drafts/early-computers-713.md): each design built from ROOT,
# its pages (cputime MINFLT) per selection workload and a bare start, medians of N, and each output hashed
import json, os, subprocess, sys, tempfile, shutil, statistics, re
ROOT = sys.argv[1]; IDS = sys.argv[2].split(','); N = int(sys.argv[3]); LIST = sys.argv[4]
sys.path.insert(0, os.path.join(ROOT, 'lab/evolve')); sys.argv = ['x']
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
R = {json.loads(l)['id']: json.loads(l) for l in open(LIST) if l.startswith('{"')}
env = {'PATH': '/usr/bin:/bin'}
def f1(eng, img, pw, inp):
    p = subprocess.run([E.CPUT, eng, img], input=inp, capture_output=True, cwd=pw, env=env)
    m = re.search(rb'^MINFLT (\d+)', p.stderr, re.M)
    return int(m.group(1)) if m else -1, __import__('hashlib').sha1(re.sub(rb'(?m)^Redefining:[^\n]*\n', b'', p.stdout)).hexdigest()[:8]
for i in IDS:
    dd = tempfile.mkdtemp(prefix='sp-'); eng, img = E.build(E.canon(R[i]['genome']), dd); pw = E.private_work(dd)
    row = []; hs = []
    for w in E.WORK_SEL + ['start']:
        inp = b'BYE\n' if w == 'start' else E.program(w)
        v = [f1(eng, img, pw, inp) for _ in range(N)]
        row.append('%s %g' % (w, statistics.median(x[0] for x in v))); hs.append(v[0][1])
    print('%s rec %s, engine %d B: %s | out %s' % (i, R[i].get('rss'), os.path.getsize(eng), ', '.join(row), ' '.join(hs))); sys.stdout.flush()
    shutil.rmtree(dd, ignore_errors=True)
