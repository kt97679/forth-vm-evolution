#!/usr/bin/env python3
"""results/drafts/rehearsal-instr-735.py [NAME ...] - where the new genes move the score, by instructions (Iteration 735;
rehearsal-735.py's timing is the sandbox's, noisier than the genes' effect). Each role (designs/NAME/record.json, default
all ten) built by the lab with the new genes off and with every one it can express on (jitdead, jitfew, hashk,
chainorder, numfirst), 8-byte cells; every selection workload and the two held out run under cachegrind (instructions,
deterministic); the ratio on / off per workload and the selection's geometric mean (the speed score's form). The time
per instruction is the laptop's to show (the JIT's native code, the walk's branches); this is the work done."""
import json, math, os, re, subprocess, sys
ROOT = os.getcwd(); sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve'))
names = sys.argv[1:]; sys.argv = ['x']
import evolve as E
E.setup()
NEW = ('jitdead', 'jitfew', 'hashk', 'chainorder', 'numfirst')
DS = os.path.join(ROOT, 'designs'); names = names or sorted(x for x in os.listdir(DS) if os.path.exists(os.path.join(DS, x, 'record.json')))
W = list(E.WORK_SEL) + list(E.WORK_HELD)
def ir(eng, img, pw, w):
    p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null', eng, img],
                       input=E.program(w), cwd=pw, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=7200)
    n = re.findall(rb'I\s+refs:\s+([\d,]+)', p.stderr)
    return int(n[-1].replace(b',', b'')) if n else 0
print('# The new genes by instructions (results/drafts/rehearsal-instr-735.py): on / off, 8-byte cells, cachegrind\n')
print('| role | ' + ' | '.join(W) + ' | the selection (geomean) |')
print('|---|' + '---:|' * (len(W) + 1))
for n in names:
    g = json.load(open(os.path.join(DS, n, 'record.json')))['genome']
    r = {}
    for v in (0, 1):
        gg = E.canon(dict(g, **({k: 1 for k in NEW} if v else {})))
        d = os.path.join(E.EV, 'rhi-%s-%d' % (n, v)); eng, img = E.build(gg, d); pw = E.private_work(d)
        r[v] = {w: ir(eng, img, pw, w) for w in W}
    q = {w: r[1][w] / r[0][w] if r[0][w] and r[1][w] else float('nan') for w in W}
    gm = math.exp(sum(math.log(q[w]) for w in E.WORK_SEL) / len(E.WORK_SEL))
    print('| %s | %s | **%.3f** |' % (n, ' | '.join('%.3f' % q[w] for w in W), gm), flush=True)
