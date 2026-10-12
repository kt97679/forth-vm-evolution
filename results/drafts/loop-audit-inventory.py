import re, json, sys, importlib.util, collections
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('E', '/tmp/fe/b/lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
LOOPW = {'DO': 'DO', '?DO': 'DO', 'LOOP': 'DO', '+LOOP': 'DO', 'BEGIN': 'BEGIN', 'UNTIL': 'BEGIN', 'WHILE': 'BEGIN', 'REPEAT': 'BEGIN', 'AGAIN': 'BEGIN'}
defs = {}
for f in ('cross.4', 'kernel.4', 'cv8.4', 'cv8b.4', 'cv8t.4', 'cv8bt.4', 'cv8-fuse.4', 'cv8t-fuse.4', 'cv8-fuse-imm.4', 'cv8t-fuse-imm.4', 'cv8-fuse-loop.4',
          'cv8b-kfast.4', 'cv8b-kinput.4', 'cv8b-klookup.4', 'kstack.4', 'cv8t-jit.4', 'file-sysc.4'):
    try: src = open('/tmp/fe/b/forth/' + f).read()
    except IOError: continue
    src = re.sub(r'\\ [^\n]*|\(\s[^)]*\)', ' ', src)
    for m in re.finditer(r'(?:^|\s):\s+(\S+)(.*?)\s;(?:\s|$)', src, re.S):
        body = m.group(2).split(); kinds = sorted(set(LOOPW[w] for w in body if w in LOOPW))
        defs[m.group(1)] = (f, kinds)
loops = {n: v for n, v in defs.items() if v[1]}
P = json.load(open('/tmp/fe/loopaudit.json'))
WS = ['corpus', 'parse', 'kernel', 'loop', 'bubble', 'sieve']
rows = []
for n, (f, kinds) in loops.items():
    sh = [P[w]['per'].get(n, 0) / P[w]['total'] for w in WS]
    rows.append((sum(sh), n, f, kinds, sh))
rows.sort(reverse=True)
print('looping colon words in the image sources: %d (of %d definitions)' % (len(loops), len(defs)))
print('| word | source | loops | ' + ' | '.join(WS) + ' |')
for s, n, f, kinds, sh in rows[:14]:
    print('| %s | %s | %s | %s |' % (n, f, '+'.join(kinds), ' | '.join('%.1f%%' % (100 * x) for x in sh)))
print('looping words with no dispatches in any of these: %d' % sum(1 for r in rows if r[0] == 0))
ids = re.findall(r'^\| ([0-9a-f]{10}) \|', open('/tmp/fe/b/results/evolve-amd-ryzen-7-pro-8840hs-seed41.md').read(), re.M)
gs = [E.express(E.recorded_genome(i)) for i in dict.fromkeys(ids) if E.recorded_genome(i)]
c = collections.Counter()
for e in gs:
    for k in ('klookup', 'kinput', 'kfast', 'tfind', 'thinhdr', 'rtloop', 'rtloopall', 'jit'): c[k] += bool(e.get(k))
print('seed 41 front, %d designs: %s' % (len(gs), ', '.join('%s %d' % kv for kv in c.items())))
