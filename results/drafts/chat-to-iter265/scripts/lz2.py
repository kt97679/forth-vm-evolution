L = [l.split() for l in open('/home/claude/forth-vm-evolution/build/evolve/cm.map') if l.strip()]
IMG = open('/home/claude/forth-vm-evolution/build/evolve/cm/image.img', 'rb').read()
H = next(int(f[1]) for f in L if f[0] == 'H')
W = sorted((int(f[1]), int(f[2]), f[3]) for f in L if f[0] == 'W')
T = set(int(f[1]) for f in L if f[0] == 'T')
ins = {}
for f in L:
    if f[0] in ('O', 'C'): ins[int(f[1])] = (f[0], f[2], f[-1])
BAD = {'EXIT', '>R', 'R>', 'R@', 'I', 'J', '(DO)', '(?DO)', '(LOOP)', '(+LOOP)', 'UNLOOP', 'LEAVE', 'RDROP', 'EXECUTE', 'DOVAR', 'DOCON', '(DOES>)', 'RP@', 'RP!'}
toks = []                       # the whole image's code as instructions: (bytes, echoable, branch target)
for a, b, kind in W:
    if kind != 'code': continue
    offs = sorted(o for o in ins if a <= o < b)
    for i, o in enumerate(offs):
        n = (offs[i + 1] if i + 1 < len(offs) else b) - o
        t, k, nm = ins[o]
        ok = not ((t == 'O' and (k in ('QBRS', 'BRS', 'NEQBR', 'LITOFF', 'LP') or nm in BAD or k == 'PX')) or (t == 'C' and nm in BAD))
        toks.append((IMG[H + o:H + o + n], ok, o in T))
    toks.append((None, False, False))           # a word boundary: no fragment crosses it (conservative)
code = sum(len(t[0]) for t in toks if t[0])
for cost, win in ((3, 4096), (2, 256)):
    pos = []; p = 0
    for t in toks: pos.append(p); p += len(t[0]) if t[0] else 0
    i = saved = matches = 0
    while i < len(toks):
        best, bestb = 0, 0
        if toks[i][1]:
            for j in range(i - 1, -1, -1):
                if pos[i] - pos[j] > win: break
                k = b = 0
                while i + k < len(toks) and toks[i + k][1] and toks[j + k][1] and toks[j + k][0] == toks[i + k][0] and j + k < i \
                      and (k == 0 or not toks[i + k][2]):
                    b += len(toks[i + k][0]); k += 1
                if b > bestb: best, bestb = k, b
        if bestb > cost: saved += bestb - cost; matches += 1; i += best
        else: i += 1
    print('whole instructions, no branch or return-stack word, no target inside, within a word: echo %d bytes, window %d - %d matches, %d bytes (%.1f%% of the code, %.1f%% of the image)' % (
        cost, win, matches, saved, 100 * saved / code, 100 * saved / len(IMG)))
