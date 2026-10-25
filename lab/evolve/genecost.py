#!/usr/bin/env python3
"""genecost.py DB ID [ID ...] - what each gene costs in bytes, gene by gene, on given designs (Iteration 519).

jitexec cost 585 KB for three runs before anyone looked (results/drafts/jit-genes-517.md): its JIT table's extra rows sat
past the JIT's own opcode, and the search quietly refused the gene. Nothing measured a gene's own byte cost. Here, for
each design named (from DB, a run's db.jsonl or results file's records): every gene of its family that is not frozen,
switched to another value it may take (a binary gene flipped; a valued one to the next value of its table; lists left
alone), built if that changes what the design expresses, and the engine's and the image's bytes compared with the
design's own. A cost far beyond what the mechanism implies - tens of KB - is the sign to look for. stdout: the report.
"""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 3: sys.exit(__doc__)
DB, IDS = sys.argv[1], sys.argv[2:]
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
def say(*a): print(*a, file=sys.stderr, flush=True)

R = {}
for l in open(DB, errors='replace'):
    if l.startswith('{') and '"genome"' in l:
        try: r = json.loads(l)
        except ValueError: continue
        if r.get('id') in IDS: R[r['id']] = r

def size(g, d):
    shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    return os.path.getsize(eng), os.path.getsize(img)

print('# What each gene costs in bytes (lab/evolve/genecost.py)\n')
print('Each design\'s genes of its family, not frozen, one at a time to another value; built when the design then expresses '
      'something else. Bytes: the engine file and the image, against the design as it is.\n')
flag = []
for i in IDS:
    if i not in R: print('%s: not in %s\n' % (i, DB)); continue
    g = E.canon(R[i]['genome']); ex = E.express(g); fam = g.get('enc')
    d = os.path.join(E.EV, 'genecost')
    try: be, bi = size(g, d)
    except Exception as x: print('%s: does not build (%s)\n' % (i, str(x)[:80])); continue
    print('## %s (%s, speed %.4f): engine %d, image %d bytes\n' % (i, fam, R[i].get('speed') or 0, be, bi))
    print('| gene | from | to | engine | image | together |')
    print('|---|---|---|---|---|---|')
    rows = []
    for k in E.EXPRESSED.get(fam, []):
        if k in E.FROZEN: continue
        v = g.get(k)
        if isinstance(v, (list, dict, tuple)) or isinstance(ex.get(k), (list, dict, tuple)): continue
        vals = list(E.GENE_VALUES[k][0]) if k in E.GENE_VALUES and len(E.GENE_VALUES[k][0]) > 2 else [0, 1]
        cur = v if v in vals else (vals[0] if not v else v)
        to = vals[(vals.index(cur) + 1) % len(vals)] if cur in vals else vals[1]
        g2 = E.canon(dict(g, **{k: to}))
        if E.express(g2) == ex: continue
        try:
            e2, i2 = size(g2, d)
            de, di = e2 - be, i2 - bi
            rows.append((abs(de + di), k, cur, to, '%+d' % de, '%+d' % di, '%+d' % (de + di)))
            say('  %s %s: %s -> %s  %+d' % (i, k, cur, to, de + di))
            if abs(de + di) > 10000: flag.append((i, k, cur, to, de + di))
        except Exception as x:
            rows.append((0, k, cur, to, 'fails', str(x)[:40].replace('|', '/'), ''))
    for _, k, cur, to, a, b, c in sorted(rows, reverse=True):
        print('| %s | %s | %s | %s | %s | %s |' % (k, cur, to, a, b, c))
    print()
    shutil.rmtree(os.path.join(E.EV, 'genecost'), ignore_errors=True)
print('**Over 10 KB**: ' + ('; '.join('%s on %s (%s -> %s): %+d bytes' % (k, i, a, b, c) for i, k, a, b, c in flag) if flag else 'none') + '.')
