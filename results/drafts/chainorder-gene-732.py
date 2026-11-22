#!/usr/bin/env python3
"""results/drafts/chainorder-gene-732.py [NAME ...] - the gene chainorder checked (Iteration 732; hashk-gene-729.py with GENES=a,b: those on together, default chainorder): for each role (designs/*/record.json,
default all ten), at 8-byte cells, its record built by the lab with the genes off and on (evolve.build); the engine's and the
image's bytes; each workload (kernel, corpus, parse - held out -, apps) run on both, the outputs compared; the
instructions (cachegrind) of corpus and parse, on / off. HK_W4=1: at 4-byte cells instead (the W4 environment). Run from
the top of a built tree with the gene, as the build user; python3 -B. Prints one table."""
import json, os, re, subprocess, sys
ROOT = os.getcwd(); sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve'))
names = sys.argv[1:]; sys.argv = ['x']; GENES = os.environ.get('GENES', 'chainorder').split(',')
import evolve as E
if os.environ.get('HK_W4'): os.environ.update(E.W4_ENV)
E.setup()
DS = os.path.join(ROOT, 'designs'); names = names or sorted(os.listdir(DS))
names = [n for n in names if os.path.exists(os.path.join(DS, n, 'record.json'))]
def run(eng, img, prog, cwd):
    return subprocess.run([eng, img], cwd=cwd, input=prog, capture_output=True, timeout=900).stdout
def ir(eng, img, prog, cwd):
    p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null', eng, img],
                       input=prog, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=3600)
    n = re.findall(rb'I\s+refs:\s+([\d,]+)', p.stderr)
    return int(n[-1].replace(b',', b'')) if n else 0
W = ('kernel', 'corpus', 'parse', 'apps'); P = {w: E.program(w) for w in W}
print('# %s checked, %s cells (results/drafts/chainorder-gene-732.py)\n' % (' and '.join(GENES), '4-byte' if os.environ.get('HK_W4') else '8-byte'))
print('| role | id | chains | engine off / on | image off / on | outputs | corpus instructions on / off | parse |')
print('|---|---|---:|---|---|---|---:|---:|')
bad = 0
for n in names:
    rec = json.load(open(os.path.join(DS, n, 'record.json'))); g = rec['genome']
    b = {}
    for v in (0, 1):
        d = os.path.join(E.EV, 'cogene-%s-%s-%d' % ('+'.join(GENES), n, v))
        et, it = E.build(E.canon(dict(g, **{x: v for x in GENES})), d)
        b[v] = (et, it, E.private_work(d))
    same = all(run(b[0][0], b[0][1], P[w], b[0][2]) == run(b[1][0], b[1][1], P[w], b[0][2]) for w in W)
    bad += not same
    r = {w: ir(b[1][0], b[1][1], P[w], b[0][2]) / max(1, ir(b[0][0], b[0][1], P[w], b[0][2])) for w in ('corpus', 'parse')}
    print('| %s | %s | %d | %d / %d | %d / %d | %s | %.4f | %.4f |' % (n, rec['id'], E.THREADS_N.get(g.get('threads', 0), 32),
          os.path.getsize(b[0][0]), os.path.getsize(b[1][0]), os.path.getsize(b[0][1]), os.path.getsize(b[1][1]),
          'same' if same else 'DIFFER', r['corpus'], r['parse']), flush=True)
print('\ngene-check: %s' % ('PASS - every output the same' if not bad else 'FAILED - %d roles differ' % bad))
sys.exit(1 if bad else 0)
