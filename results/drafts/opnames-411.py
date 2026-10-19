# Iteration 411: a tag-2 design's loop dispatches - the opcode numbers the profiler counts, named by the converter's own
# map (CALLMAP) and by stackops.py's name(), side by side.
import collections, json, os, re, shutil, sys
os.chdir('/home/claude/forth-vm-evolution'); sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E
E.setup()
did = '4ac602c8bd'
r = next(json.loads(l) for l in open('results/evolve-amd-ryzen-7-pro-8840hs-seed60.md') if l.startswith('{"') and did in l)
g = E.canon(r['genome']); e = E.express(g)
print('design', did, '| tag2', e.get('tag2'), 'escape', e.get('escape'), 'rtloopall', e.get('rtloopall'), 'rtiplus', e.get('rtiplus'), 'rtfuse', e.get('rtfuse'), 'rtimm', e.get('rtimm'))
d = '/tmp/rl/b'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
cm = os.path.join(d, 'callmap'); os.environ['CALLMAP'] = cm; E.PROFILING[0] = True
try: eng, img = E.build(dict(g, tail=0, msc=0), d)
finally: E.PROFILING[0] = False; del os.environ['CALLMAP']
conv = collections.defaultdict(collections.Counter)
for l in open(cm):
    f = l.split()
    if f and f[0] == 'O' and len(f) >= 5 and f[2] == 'P': conv[int(f[3])][f[4]] += 1
prims = [l.split()[1] for l in open('forth/kernel.4') if l.startswith('PRIMITIVE')]
sup = {op: '%s %s' % (a, b) for a, b, op in E.supers_in(g)}; o10 = {op: w for w, op in E.ops10_in(g)}
def sname(op):
    if op in sup: return sup[op]
    if op in o10: return o10[op]
    if op >= 128: return 'call'
    if g.get('escape') == 2: i = op if op < 27 else None
    elif g.get('escape'): i = op if op < 32 else op + 1 if op < 36 else None
    else: i = op if op < 68 else None
    return prims[i] if i is not None and i < len(prims) else 'op%d' % op
pw = E.private_work(d)
for w in ('loop', 'bubble'):
    pf = os.path.join(d, 'prof-' + w); E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
    by = collections.Counter()
    for line in open(pf):
        f = line.split()
        if not f or not f[0].isdigit(): continue
        a, b, k = int(f[0]), int(f[1]), int(f[2])
        if a == 0x7D or 128 <= b <= 255: continue
        by[b] += k
    tot = sum(by.values())
    print('\n%s: %d dispatches' % (w, tot))
    for op, k in by.most_common(8):
        print('  op %3d  %5.1f%%  stackops: %-10s converter: %s' % (op, 100 * k / tot, sname(op), dict(conv.get(op, {})) or '-'))
