import collections, math
L = [l.split() for l in open('/home/claude/forth-vm-evolution/build/evolve/cm.map') if l.strip()]
W = sorted((int(f[1]), int(f[2]), f[3]) for f in L if f[0] == 'W')
T = set(int(f[1]) for f in L if f[0] == 'T')
ins = {}
for f in L:
    if f[0] in ('O', 'C'): ins[int(f[1])] = (f[0], f[2], f[-1])
code_bytes = 0; ops1 = collections.Counter(); seqs = []
for a, b, kind in W:
    if kind != 'code': continue
    offs = sorted(o for o in ins if a <= o < b); code_bytes += b - a
    seq = []
    for i, o in enumerate(offs):
        size = (offs[i + 1] if i + 1 < len(offs) else b) - o
        t, k, nm = ins[o]
        one = t == 'O' and size == 1 and k in ('P', 'LIT')
        seq.append((nm if one else None, o in T))
        if one: ops1[nm] += 1
    seqs.append(seq)
print('code in word bodies: %d bytes; one-byte operations: %d (%d kinds)' % (code_bytes, sum(ops1.values()), len(ops1)))
for K in (7, 15):
    top = set(n for n, _ in ops1.most_common(K))
    cov = sum(ops1[n] for n in top)
    saved = 0; runs = collections.Counter()
    for seq in seqs:
        run = 0
        for nm, target in seq + [(None, False)]:
            if nm in top and not (target and run):
                run += 1; continue
            if run >= 4: saved += run - 1 - math.ceil((run + 1) / 2); runs[run] += 1
            run = 1 if nm in top else 0
    print('top %2d one-byte operations: %d of them (%.0f%%); runs of 4 or more %d; a nibble-run opcode would save %d bytes' % (K, cov, 100 * cov / sum(ops1.values()), sum(runs.values()), saved))
print('the 15 commonest:', ', '.join('%s %d' % kv for kv in ops1.most_common(15)))
