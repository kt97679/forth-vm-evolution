import collections
L = [l.split() for l in open('/home/claude/forth-vm-evolution/build/evolve/cm.map') if l.strip()]
IMG = open('/home/claude/forth-vm-evolution/build/evolve/cm/image.img', 'rb').read()
HOFF = next(int(f[1]) for f in L if f[0] == 'H')
W = sorted((int(f[1]), int(f[2]), f[3], ' '.join(f[4:])) for f in L if f[0] == 'W')
T = set(int(f[1]) for f in L if f[0] == 'T')
ins = {}
for f in L:
    if f[0] == 'O': ins[int(f[1])] = ('O', f[2], f[-1])
    elif f[0] == 'C': ins[int(f[1])] = ('C', f[2], f[-1])       # width, callee name
UNSAFE = {'EXIT', '>R', 'R>', 'R@', 'I', 'J', '(DO)', '(?DO)', '(LOOP)', '(+LOOP)', 'UNLOOP', 'LEAVE', 'RDROP', '2>R', '2R>', '2R@', 'EXECUTE', 'DOVAR', 'DOCON', 'DOES>', '(DOES>)', 'RP@', 'RP!', 'SP@', 'SP!'}
seqs = []                                          # per word: [(token, size)]
for a, b, kind, name in W:
    if kind != 'code': continue
    offs = sorted(o for o in ins if a <= o < b)
    run = []
    for i, o in enumerate(offs):
        nxt = offs[i + 1] if i + 1 < len(offs) else b
        t, k, nm = ins[o]
        size = nxt - o
        bad = (t == 'O' and (k in ('QBRS', 'BRS', 'NEQBR', 'LITOFF', 'LP', 'PX') or nm in UNSAFE)) or (t == 'C' and nm in UNSAFE)
        if o in T and run: seqs.append(run); run = []          # a branch target starts a new run
        if bad:
            if run: seqs.append(run)
            run = []; continue
        run.append(((t, k, nm, IMG[HOFF + o:HOFF + o + size]), size))
    if run: seqs.append(run)
print('safe runs: %d, tokens %d, bytes %d' % (len(seqs), sum(map(len, seqs)), sum(s for r in seqs for _, s in r)))
HDR, CALL = 8, 2                                   # a helper's header (link, count, name) and a call's bytes
def best(seqs):
    occ = collections.defaultdict(list)
    for si, r in enumerate(seqs):
        for i in range(len(r)):
            for n in range(2, 9):
                if i + n > len(r): break
                key = tuple((t[0], t[3]) if len(t) > 3 else t for t, _ in r[i:i + n])
                occ[key].append((si, i))
    top = None
    for key, places in occ.items():
        if len(places) < 2: continue
        places.sort(); used = []; last = {}
        for si, i in places:                       # non-overlapping within a run
            if si in last and i < last[si]: continue
            used.append((si, i)); last[si] = i + len(key)
        k = len(used)
        sb = sum(s for _, s in seqs[used[0][0]][used[0][1]:used[0][1] + len(key)])
        net = k * (sb - CALL) - (sb + 1 + HDR)
        if top is None or net > top[0]: top = (net, key, used, sb)
    return top
total = 0; picked = []
for step in range(40):
    t = best(seqs)
    if not t or t[0] <= 0: break
    net, key, used, sb = t
    names = [t[0][2] for t in seqs[used[0][0]][used[0][1]:used[0][1] + len(key)]]
    total += net; picked.append((net, len(used), sb, ' '.join(names)))
    # replace each use by a single call token (so later picks see it)
    new = []
    usedset = collections.defaultdict(list)
    for si, i in used: usedset[si].append(i)
    for si, r in enumerate(seqs):
        if si not in usedset: new.append(r); continue
        out = []; j = 0; starts = set(usedset[si])
        while j < len(r):
            if j in starts: out.append((('C', '2', 'helper%d' % step), CALL)); j += len(key)
            else: out.append(r[j]); j += 1
        new.append(out)
    seqs = new
print('greedy factoring, %d helpers: net %d bytes' % (len(picked), total))
for p in picked[:25]: print('  net %4d  x%-3d %2d bytes  %s' % p)
