# an LZ77 parse of the smallest design's code (word bodies only): what an echo instruction could save
L = [l.split() for l in open('/home/claude/forth-vm-evolution/build/evolve/cm.map') if l.strip()]
IMG = open('/home/claude/forth-vm-evolution/build/evolve/cm/image.img', 'rb').read()
H = next(int(f[1]) for f in L if f[0] == 'H')
W = sorted((int(f[1]), int(f[2])) for f in L if f[0] == 'W' and f[3] == 'code')
code = b''.join(IMG[H + a:H + b] for a, b in W)
for cost, win in ((3, 4096), (2, 256)):
    i = saved = matches = 0
    while i < len(code):
        best = 0
        lo = max(0, i - win)
        for j in range(lo, i):
            k = 0
            while i + k < len(code) and k < 15 + cost and code[j + k] == code[i + k] and j + k < i: k += 1
            if k > best: best = k
        if best > cost: saved += best - cost; matches += 1; i += best
        else: i += 1
    print('echo costing %d bytes, window %d: %d matches, %d bytes saved of %d code bytes (%.1f%%; %.1f%% of the image)' % (cost, win, matches, saved, len(code), 100 * saved / len(code), 100 * saved / len(IMG)))
