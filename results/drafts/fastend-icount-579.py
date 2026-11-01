#!/usr/bin/env python3
"""results/drafts/fastend-icount-579.py OUT.jsonl [--ids-file F] [--only A,B] [--width 8] - the fast-end re-measure's
designs counted, not timed (Iteration 579; the owner: while seed 86 runs).

The question (576): seed 84's bred designs led its founders by 0.8% in their run (the group medians) and by 4.5%
re-measured on the laptop - unexplained. Timing is the laptop's; here the count is deterministic: each design's user-space
instructions on the seven selection workloads (valgrind --tool=cachegrind --cache-sim=no, --smc-check=all for the JIT's
code), against hand-made s6's on the same inputs, the geometric mean over the workloads as evolve.py's speed. If the bred
designs execute about 4% fewer instructions than the founders, the lead is in the code and should travel; if their counts
are equal, it is the laptop's core (alignment, prediction) and may not.

The designs: the records of --ids-file (default results/fastend-remeasure-575.md) at --width (8: the verdict's), their
genomes from the results files. Resumable: designs already in OUT are skipped. Each line: id, why, the ratio per workload,
icount (the geometric mean), the in-run and re-measured speeds (from the ids file and the chain's loadtest.md if given
as --loadtest)."""
import glob, json, math, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
a = sys.argv[1:]
def opt(k, d=None):
    if k in a: j = a.index(k); v = a[j + 1]; del a[j:j + 2]; return v
    return d
idsf = opt('--ids-file', os.path.join(ROOT, 'results', 'fastend-remeasure-575.md')); only = opt('--only')
width = opt('--width', '8'); ltf = opt('--loadtest')
if len(a) != 1: sys.exit(__doc__)
OUT = a[0]
if width == '4': os.environ['EVOLVE_CELL'] = '4'; os.environ.setdefault('EVOLVE_CC', 'gcc -m32')
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E

asked = [json.loads(l) for l in open(idsf) if l.startswith('{"')]
if only: asked = [r for r in asked if r['id'] in only.split(',')]
asked = [r for r in asked if width == '8' or '32 bits' in r.get('why', '')]   # every design at 64 bits; at 32 the 32-bit fast end
gen = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'results', 'evolve-*-seed*.md'))) + sorted(glob.glob(os.path.join(ROOT, 'results', 'candidates-*.md'))):
    for l in open(f, errors='replace'):
        if l.startswith('{"'):
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('id') and 'genome' in r: gen.setdefault(r['id'], r['genome'])
LT = {}
if ltf:
    for l in open(ltf):
        if l.startswith('{"'): r = json.loads(l); LT[r['id']] = r
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        try: done.add(json.loads(l)['id'])
        except (ValueError, KeyError): pass

def icount(eng, img, pw, w):
    """User-space instructions of one run of workload w (cachegrind's I refs); its output's hash beside it."""
    r = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null',
                        '--smc-check=all', eng, img], input=E.program(w), cwd=pw, capture_output=True, timeout=1800)
    m = re.search(rb'I\s+refs:\s+([\d,]+)', r.stderr)
    if not m: raise RuntimeError('no count for %s (exit %s): %s' % (w, r.returncode, r.stderr[-200:]))
    return int(m.group(1).replace(b',', b''))

E.setup()
W = E.WORK_SEL
ref = None
if os.path.exists(OUT + '.s6'): ref = json.load(open(OUT + '.s6'))
else:
    ref = {w: icount(E.REF[0], E.REF[1], E.REF[2], w) for w in W}; json.dump(ref, open(OUT + '.s6', 'w'))
print('fastend-icount: s6 %s' % ', '.join('%s %s' % (w, format(ref[w], ',')) for w in W), flush=True)
for r in asked:
    i = r['id']
    if i in done: continue
    if i not in gen: print('fastend-icount: %s - no genome in a results file, left out' % i, flush=True); continue
    d = os.path.join(E.EV, 'icount-' + i)
    try:
        eng, img = E.build(E.canon(gen[i]), d); pw = E.private_work(d)
        c = {w: icount(eng, img, pw, w) for w in W}
    except Exception as ex:
        print('fastend-icount: %s - %s' % (i, str(ex)[:120]), flush=True); continue
    ratio = {w: c[w] / ref[w] for w in W}
    ic = math.exp(sum(math.log(v) for v in ratio.values()) / len(W))
    lt = LT.get(i, {}); k = '' if width == '8' else '32'
    rec = dict(id=i, why=r.get('why'), width=int(width), icount=round(ic, 5), ratio={w: round(v, 5) for w, v in ratio.items()},
               count=c, inrun=lt.get('inrun' + k) or r.get('speed' + k), idle=lt.get('idle' + k), loaded=lt.get('loaded' + k))
    open(OUT, 'a').write(json.dumps(rec, sort_keys=True) + '\n')
    print('fastend-icount: %s %-45s icount %.4f  idle %s' % (i, r.get('why'), ic, rec['idle']), flush=True)
print('fastend-icount: DONE', flush=True)
