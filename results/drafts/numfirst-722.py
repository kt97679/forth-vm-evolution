#!/usr/bin/env python3
"""results/drafts/numfirst-722.py [NAME ...] - the gene numfirst priced on a prototype (Iteration 722;
results/drafts/esolangs-717.md proposed it: literals 28.6 % of the corpus's tokens, every one a whole chain's walk
before NUMBER?). For each design (default smallest and portable-fastest - 717's two), at 8-byte cells: the lab's
translator build of its record (evolve.build), and the same with results/drafts/numfirst-722.4 loaded last among its
overlays (INTERPRET8: a [0-9]+ token converted before the lookup) - built in a process of its own on a copy of
build/work (build/numfirst-work), so its dumps are a directory of their own. Each workload (kernel, corpus, parse - held
out - and apps) runs on its build's profiling engine (evolve.PROFILING - designs/'s engine is made for its shipped
image's layout, and segfaulted on the prototype's): the dispatches (VMPROF's I lines), the output compared; then under
cachegrind on its build's engine (instructions - the lookup is C where klookup is on, which dispatches do not see). Prints both and
proto / base. Run from the top, as the build user; about five minutes."""
import json, os, re, shutil, subprocess, sys
ROOT = os.getcwd(); HERE = os.path.join(ROOT, 'lab', 'evolve'); DS = os.path.join(ROOT, 'designs')
PHASE = os.environ.get('NF_PHASE')
OUT = os.path.join(ROOT, 'build', 'numfirst'); os.makedirs(OUT, exist_ok=True)
WORK = ['kernel', 'corpus', 'parse', 'apps']

if PHASE:                                   # a build process: base or proto
    names = sys.argv[1:]; sys.argv = ['x']; sys.path.insert(0, HERE)
    import evolve as E
    if PHASE == 'proto':
        nw = os.path.join(E.O, 'numfirst-work'); shutil.rmtree(nw, ignore_errors=True); shutil.copytree(E.W, nw)
        E.W = nw
    E.setup()
    if PHASE == 'proto':
        shutil.copy(os.path.join(ROOT, 'results', 'drafts', 'numfirst-722.4'), os.path.join(E.W, 'numfirst.4'))
        orig = E.boot_files; E.boot_files = lambda name: orig(name) + ['numfirst.4']
    res = {}
    for n in names:
        rec = json.load(open(os.path.join(DS, n, 'record.json')))
        d = os.path.join(E.EV, 'numfirst-%s-%s' % (PHASE, n)); shutil.rmtree(d, ignore_errors=True)
        et, it = E.build(E.canon(dict(rec['genome'])), d)
        E.PROFILING[0] = 1; pe, _ = E.build(E.canon(dict(rec['genome'])), d + '-prof'); E.PROFILING[0] = 0
        res[n] = {'eng': et, 'img': it, 'peng': pe, 'work': E.private_work(d), 'id': rec['id'],
                  'prog': {w: E.program(w).decode('latin-1') for w in WORK}}
    json.dump(res, open(os.path.join(OUT, PHASE + '.json'), 'w'))
    sys.exit(0)

names = sys.argv[1:] or ['smallest', 'portable-fastest']
for ph in ('base', 'proto'):
    subprocess.run([sys.executable, os.path.abspath(__file__)] + names, env=dict(os.environ, NF_PHASE=ph), check=True,
                   stdout=subprocess.DEVNULL)
B, P = (json.load(open(os.path.join(OUT, ph + '.json'))) for ph in ('base', 'proto'))

def dispatches(eng, img, prog, cwd):
    f = os.path.join(OUT, 'vmprof.txt')
    if os.path.exists(f): os.remove(f)
    p = subprocess.run([eng, img], cwd=cwd, input=prog.encode('latin-1'), capture_output=True, timeout=600,
                       env=dict(os.environ, VMPROF=f))
    return sum(int(l.split()[2]) for l in open(f) if l.startswith('I ')), p.stdout
def ir(eng, img, prog, cwd):
    p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null', eng, img],
                       input=prog.encode('latin-1'), cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=1800)
    n = re.findall(rb'I\s+refs:\s+([\d,]+)', p.stderr)
    return int(n[-1].replace(b',', b'')) if n else 0

print('# numfirst on a prototype: dispatches and instructions, proto / base (results/drafts/numfirst-722.py)\n')
for n in names:
    b, p = B[n], P[n]
    print('%s (%s), 8-byte cells - images %d / %d B (proto / base)' % (n, b['id'], os.path.getsize(p['img']), os.path.getsize(b['img'])))
    for w in WORK:
        db, ob = dispatches(b['peng'], b['img'], b['prog'][w], b['work'])
        dp, op = dispatches(p['peng'], p['img'], b['prog'][w], b['work'])
        ib, ip = ir(b['eng'], b['img'], b['prog'][w], b['work']), ir(p['eng'], p['img'], b['prog'][w], b['work'])
        print('  %-7s dispatches %13s -> %13s  %.4f   instructions %14s -> %14s  %.4f   output %s'
              % (w, '{:,}'.format(db), '{:,}'.format(dp), dp / db if db else 0, '{:,}'.format(ib), '{:,}'.format(ip),
                 ip / ib if ib else 0, 'same' if ob == op else 'DIFFERS'), flush=True)
    print()
