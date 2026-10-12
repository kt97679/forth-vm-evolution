import re, collections, sys, importlib.util
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('E', '/tmp/fe/b/lab/evolve/evolve.py'); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
names = [l.split(None, 2)[2].strip() for l in open('/tmp/fe/b/build/evolve/loopaudit.sym')]   # image order, oldest first
def h(n, T):
    b = n.encode('latin-1'); v = (b[0] << 1) ^ ((b[1] << 2) if len(b) > 1 else 0) ^ len(b)
    return v & (T - 1)
toks = re.findall(r'\S+', open(E.CORPUS).read().upper())
cnt = collections.Counter(toks)
for T in (32, 64, 128):
    chains = collections.defaultdict(list)
    for n in names: chains[h(n, T)].insert(0, n)        # newest first
    pos = {n: i + 1 for c in chains.values() for i, n in enumerate(c)}
    hit = miss = steps = 0
    for t, k in cnt.items():
        if t in pos: hit += k; steps += k * pos[t]
        else: miss += k; steps += k * 2 * len(chains.get(h(t, T), []))     # FORTH twice in the order
    lens = sorted((len(c) for c in chains.values()), reverse=True)
    print('%3d chains: longest %s, mean walk per lookup %.1f (hits %d%%: %.1f; misses: %.1f each, twice)' % (T, lens[:5], steps / (hit + miss), 100 * hit // (hit + miss),
          sum(k * pos[t] for t, k in cnt.items() if t in pos) / max(hit, 1), sum(k * 2 * len(chains.get(h(t, T), [])) for t, k in cnt.items() if t not in pos) / max(miss, 1)))
    if T == 32:
        miss_only = sum(k * len(chains.get(h(t, T), [])) for t, k in cnt.items() if t not in pos)
        print('     the second search of FORTH on every miss: %.0f%% of all chain steps' % (100.0 * miss_only / steps))
        print('     the hottest hits and their depth: %s' % ', '.join('%s %d' % (t, pos[t]) for t, k in cnt.most_common(40) if t in pos)[:300])
