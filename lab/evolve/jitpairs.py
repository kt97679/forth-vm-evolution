"""jitpairs.py - the operation pairs a JIT design runs, over the selection workloads (Iteration 506).

Prices JIT super-stencils: seed 70's fastest JIT design (77d42fd7da, with the four JIT genes) built with the
JIT off and the profiler on, so every operation the JIT would copy is a dispatch counted in pairs (VMPROF);
each named from the JIT build's vm-jit-ops.h (the same op numbering - the JIT build inserts one code of its own
in the one-byte table, 65533). Each workload weighted equally, as the selection's geometric mean. Reads seed
70's db from /tmp/process (process-seed.sh's). results/drafts/jit-pairs-506.md.
"""
import collections, json, os, re, sys, shutil
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
dbp = [os.path.join(r, 'db.jsonl') for r, _, f in os.walk('/tmp/process') if 'db.jsonl' in f and 'seed70' in r][0]
r = next(json.loads(l) for l in open(dbp) if '"id": "77d42fd7da"' in l)
g = E.canon(dict(E.canon(r['genome']), jitmul=1, jitdoes=1, jitexec=1, jitcfa=1))
dA = os.path.join(E.EV, 'jpA'); shutil.rmtree(dA, ignore_errors=True); E.build(g, dA)        # the JIT build: names
NAMES = {}
for l in open(os.path.join(dA, 'vm-jit-ops.h')):
    m = re.match(r'\[(\d+)\] = \{.*/\* *(.+?) *\*/', l) or re.match(r'/\* \[(\d+)\] (.+?) - no stencils \*/', l)
    if m: NAMES[int(m.group(1))] = m.group(2).split(' - ')[0].split(' (')[0]
oneA = open(os.path.join(dA, 'vm-tag2-one.h')).read()
dB = os.path.join(E.EV, 'jpB'); shutil.rmtree(dB, ignore_errors=True); E.PROFILING[0] = True
try: eng, img = E.build(dict(g, jit=0, tail=0, msc=0), dB)
finally: E.PROFILING[0] = False
oneB = open(os.path.join(dB, 'vm-tag2-one.h')).read()
print('the same one-byte codes with and without the JIT:', oneA == oneB, '| ops named:', len(NAMES), flush=True)
one = [int(x) for x in re.findall(r'-?\d+', oneB)]
def op_of(code):
    i = code if code < 64 else code - 64 if 128 <= code < 192 else None
    return one[i] if i is not None and i < len(one) else None
CTRL = {'EXIT', 'BRANCH', '?BRANCH', 'NOOP', 'BYE', 'EXECUTE', '(LOOP)', '(+LOOP)', '(DO)', '(?DO)'}
pw = E.private_work(dB); share = collections.Counter(); single = collections.Counter(); within = 0.0
for w in E.WORK_SEL:
    pf = os.path.join(dB, 'prof-' + w)
    E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=600, cpu=300, env=dict(os.environ, VMPROF=pf))
    c, total, ops = collections.Counter(), 0, collections.Counter()
    for line in open(pf):
        m = re.match(r'^(\d+) (\d+) (\d+)$', line)
        if not m: continue
        a, b, k = map(int, m.groups()); total += k
        oa, ob = op_of(a), op_of(b)
        na, nb = NAMES.get(oa, '?%s' % oa) if oa is not None else None, NAMES.get(ob, '?%s' % ob) if ob is not None else None
        if na: ops[na] += k
        if na and nb and na not in CTRL and nb not in CTRL: c[(na, nb)] += k
    for pr, k in c.items(): share[pr] += k / max(total, 1) / len(E.WORK_SEL)
    for o, k in ops.items(): single[o] += k / max(total, 1) / len(E.WORK_SEL)
    within += sum(c.values()) / max(total, 1) / len(E.WORK_SEL)
    print('  %-10s %12d pairs dispatched; op-op pairs outside control flow %.1f%%' % (w, total, 100.0 * sum(c.values()) / max(total, 1)), flush=True)
print('\nall seven, each weighted equally: op-op pairs outside control flow %.1f%% of dispatched pairs' % (100 * within))
cum = 0.0
print('the top 25 pairs (share of all dispatched pairs, cumulative):')
for (a, b), s in share.most_common(25):
    cum += s; print('  %-12s %-12s %5.2f%%  %5.1f%%' % (a, b, 100 * s, 100 * cum))
print('the top 12 single operations:', ', '.join('%s %.1f%%' % (o, 100 * s) for o, s in single.most_common(12)))
shutil.rmtree(dA, ignore_errors=True); shutil.rmtree(dB, ignore_errors=True)
