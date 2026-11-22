#!/usr/bin/env python3
"""results/drafts/hashk-727.py [NAME ...] - the gene hashk priced on a prototype (Iteration 727; results/drafts/numfirst-722.py's
harness, results/drafts/demoscene-ioccc-727.md's candidate): the lab's translator build of each design's record, and the
same with results/drafts/hashk-727.4 loaded last (HASH8: the multiplicative chain hash) and the converter threading the
image by it (HASHK=K for tools/layout.py - a scratch tree's, which has the switch: run it there, from the top). The
dispatches (VMPROF) and instructions (cachegrind) of kernel, corpus, parse (held out) and apps, proto / base, the outputs
compared. Default the smallest (the lookup in Forth, 16 chains: K 50919, the shift 12 - hashk-727.4's literals); HK_K and
HK_SHIFT for another design - the engine built with -DHASHK=K (EVOLVE_CFLAGS: vm-lab.c's CHAIN, the scratch tree's), so a
lookup in C hashes as the overlay and the converter do."""
import json, os, re, shutil, subprocess, sys
ROOT = os.getcwd(); HERE = os.path.join(ROOT, 'lab', 'evolve'); DS = os.path.join(ROOT, 'designs')
PHASE = os.environ.get('HK_PHASE')
OUT = os.path.join(ROOT, 'build', 'hashk'); os.makedirs(OUT, exist_ok=True)
WORK = ['kernel', 'corpus', 'parse', 'apps']

if PHASE:                                   # a build process: base or proto
    names = sys.argv[1:]; sys.argv = ['x']; sys.path.insert(0, HERE)
    import evolve as E
    if PHASE == 'proto':
        nw = os.path.join(E.O, 'hashk-work'); shutil.rmtree(nw, ignore_errors=True); shutil.copytree(E.W, nw)
        E.W = nw
    E.setup()
    if PHASE == 'proto':
        t = open(os.path.join(ROOT, 'results', 'drafts', 'hashk-727.4')).read().replace('50919 * 65535 AND 12 RSHIFT', '%s * 65535 AND %s RSHIFT' % (os.environ['HASHK'], os.environ.get('HK_SHIFT', '12')))
        open(os.path.join(E.W, 'hashk.4'), 'w').write(t)
        orig = E.boot_files; E.boot_files = lambda name: orig(name) + ['hashk.4']
    res = {}
    for n in names:
        rec = json.load(open(os.path.join(DS, n, 'record.json')))
        d = os.path.join(E.EV, 'hashk-%s-%s' % (PHASE, n)); shutil.rmtree(d, ignore_errors=True)
        et, it = E.build(E.canon(dict(rec['genome'])), d)
        E.PROFILING[0] = 1; pe, _ = E.build(E.canon(dict(rec['genome'])), d + '-prof'); E.PROFILING[0] = 0
        res[n] = {'eng': et, 'img': it, 'peng': pe, 'work': E.private_work(d), 'id': rec['id'],
                  'prog': {w: E.program(w).decode('latin-1') for w in WORK}}
    json.dump(res, open(os.path.join(OUT, PHASE + '.json'), 'w'))
    sys.exit(0)

names = sys.argv[1:] or ['smallest']
K, SH = os.environ.get('HK_K', '50919'), os.environ.get('HK_SHIFT', '12')   # K and 16 - log2 chains: the design's
for ph in ('base', 'proto'):
    subprocess.run([sys.executable, os.path.abspath(__file__)] + names, env=dict(os.environ, HK_PHASE=ph, **({'HASHK': K, 'EVOLVE_CFLAGS': '-DHASHK=' + K} if ph == 'proto' else {})), check=True,
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

print('# hashk on a prototype: dispatches and instructions, proto / base (results/drafts/hashk-727.py)\n')
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
