#!/usr/bin/env python3
"""loopwords.py ID [ID ...] [--db FILE] - the loop words in code compiled at
run time, priced by counting (Iteration 28).

The converter turns a loop word in the IMAGE's code into its format-10
opcode - (DO), (?DO), (LOOP), (+LOOP), (LEAVE), I, J, UNLOOP; since
Iteration 13 really. Code compiled at RUN TIME - each workload's own words,
the cross-compiler's - still calls their colon bodies, and before each call
with an inline operand the compiler pads with alignment NOOPs (0-7, by where
HERE lands; Iteration 13). Counted, not timed: dispatch counts are the same
on every machine, so this prices on the development VM what the laptop
would. Per workload: the dispatches spent inside each loop word's colon body
(the profiler's per-address counts within the converter's symbol map), how
often it was entered, how many of those entries the image's own call sites
made (the call-site map), and the NOOPs executed outside the image. The
price of compiling the opcodes at run time: each run-time entry costs one
dispatch instead of its body, and the padding goes. Also the highest code
address each workload runs - against the far-call reach (2 MB at scale 0
with one-byte calls; 4 MB without).
"""
import collections, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; db = os.path.join(HERE, '..', '..', 'build', 'evolve', 'db.jsonl')
if '--db' in args: i = args.index('--db'); db = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
recs = {}
for l in open(db):
    try: r = json.loads(l); recs[r['id']] = r
    except ValueError: pass
prims = [l.split()[1] for l in open(os.path.join(E.ROOT, 'forth', 'kernel.4')) if l.startswith('PRIMITIVE')]
WORDS = ['(DO)', '(?DO)', '(LOOP)', '(+LOOP)', '(LEAVE)', 'I', 'J', 'UNLOOP']
WORKS = E.WORK_SEL + E.WORK_HELD

def opcode_of(g, name):
    """The plain opcode of a primitive in design g - price.py's name(), inverted."""
    for op in range(128):
        if g.get('escape') == 2: i = op if op < 27 else None
        elif g.get('escape'): i = op if op < 32 else op + 1 if op < 36 else None
        else: i = op if op < 68 else None
        if i is not None and i < len(prims) and prims[i] == name: return op
    return None

for did in args:
    if did not in recs: sys.exit('no design %s in %s' % (did, db))
    g = E.canon(recs[did]['genome'])
    d = os.path.join(E.EV, 'loopwords'); shutil.rmtree(d, ignore_errors=True)
    sm, cm = d + '.sym', d + '.map'
    os.environ['SYMMAP'] = sm; os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)        # the stream, not the dispatch, is what is counted
    finally: E.PROFILING[0] = False; del os.environ['SYMMAP']; del os.environ['CALLMAP']
    ranges = collections.defaultdict(list)
    for l in open(sm):
        a, b, n = l.split(None, 2); ranges[n.strip()].append((int(a), int(b)))
    lines = [l.split() for l in open(cm)]
    hdr, n_img = int(lines[0][1]), int(lines[0][2])
    from_site = collections.defaultdict(list)                  # target offset -> the image's call sites to it
    for f in lines[1:]:
        if f[0] == 'C': from_site[int(f[3])].append(int(f[1]))
    im = open(img, 'rb').read()[hdr:]
    noop = opcode_of(g, 'NOOP')
    pw = E.private_work(d)
    print('## %s - %s bytes, format-10 words in the image: %s\n' % (did, format(recs[did]['size'], ','),
          ', '.join(w for w, _ in E.ops10_in(g) if w in WORDS) or 'none'))
    print('| workload | dispatches | run-time entries: ' + ', '.join(WORDS) + ' | in their bodies | NOOPs outside the image | the price: fewer dispatches | highest address run |')
    print('|---|---|---|---|---|---|---|')
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
        ipc, col = collections.Counter(), collections.Counter()
        for line in open(pf):
            f = line.split()
            if f[0] == 'I': ipc[int(f[1])] += int(f[2])
            elif f[0] != 'C' and int(f[1]) < 256 and int(f[0]) != 0x7D: col[int(f[1])] += int(f[2])
        total = sum(ipc.values())
        rt_noop = col[noop] - sum(k for a, k in ipc.items() if a < n_img and im[a] == noop) if noop is not None else 0
        ent, inside, save = [], 0, 0
        for word in WORDS:
            e_rt = 0
            for a, b in ranges.get(word, []):
                entries = ipc.get(a, 0); from_img = sum(ipc.get(s, 0) for s in from_site.get(a, []))
                body = sum(k for x, k in ipc.items() if a <= x < b)
                rt = max(0, entries - from_img)
                e_rt += rt; inside += body
                if entries: save += (body - entries) * rt / entries   # each run-time entry: one dispatch, not the body
            ent.append(e_rt)
        save += max(0, rt_noop)
        top = max(a for a, k in ipc.items() if k)       # the profiler's window is 1 MB (PROFIP masks 20 bits)
        print('| %s | %d | %s | %d | %d | %d (%.1f%%) | %s |' % (w, total, ', '.join(map(str, ent)), inside, rt_noop, save, 100 * save / total, format(top, ',')))
    print()
    shutil.rmtree(d, ignore_errors=True)
