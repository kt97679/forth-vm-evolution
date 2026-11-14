#!/usr/bin/env python3
"""lab/evolve/genapps-report.py RESULTS.json [...] - genapps.py's measurements as Markdown tables (Iteration 674): per
system and program the application's code (code, names and headers), its run time and its load; the systems' start;
each against relf's CV8 (relf64, or relf32 at 4-byte cells) and against s6; and, across the ten designs, the
Spearman rank correlation of the lab's own scores (designs/NAME/record.json: the kernel image, engine and image,
speed on the selection's workloads) with these."""
import json, math, os, statistics, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DESIGNS = ['smallest', 'least-memory', 'portable-small', 'portable-knee', 'portable-arm', 'portable-fastest',
           'best-all-round', 'small-jit', 'fastest-x86-64', 'fastest-x86-32']
def gmean(xs): return math.exp(sum(math.log(x) for x in xs) / len(xs))
def ranks(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0] * len(xs)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r
def spearman(xs, ys):
    rx, ry = ranks(xs), ranks(ys); mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float('nan')
for path in sys.argv[1:]:
    R = json.load(open(path)); S = R['systems']; apps = R['apps']; cells = R['cells']
    base = 'relf64' if 'relf64' in S else 'relf32'
    names = [s for s in S]
    print('### %d-byte cells (relf %s; %d rounds; %s)\n' % (cells, R['relf'], R['rounds'], R['when']))
    print('**Application code** - code, names and headers the program\'s load adds, its own data left out; bytes:\n')
    print('| system | ' + ' | '.join(apps) + ' | all seven | vs %s | vs s6 |' % base)
    print('|---|' + '---:|' * (len(apps) + 3))
    tot = {s: sum(S[s]['apps'][a]['code'] for a in apps) for s in names}
    for s in names:
        print('| %s | ' % s + ' | '.join('{:,}'.format(S[s]['apps'][a]['code']) for a in apps) +
              ' | {:,} | {:.3f} | {:.3f} |'.format(tot[s], tot[s] / tot[base], tot[s] / tot['s6']))
    data = {a: sorted(set(S[s]['apps'][a]['data'] for s in names)) for a in apps}
    print('\nTheir data (ALLOT , C,), bytes: ' + '; '.join('%s %s' % (a, ' or '.join('{:,}'.format(d) for d in data[a])) for a in apps) + '.\n')
    print('**Run time** - each program\'s benchmark, CPU seconds (the median of the full runs less the median of the loads):\n')
    print('| system | ' + ' | '.join(apps) + ' | geomean vs %s | vs s6 | load, all seven (ms) | start (ms) |' % base)
    print('|---|' + '---:|' * (len(apps) + 4))
    gm = {}
    for s in names:
        rr = [S[s]['apps'][a]['run'] / S[base]['apps'][a]['run'] for a in apps]
        r6 = [S[s]['apps'][a]['run'] / S['s6']['apps'][a]['run'] for a in apps]
        gm[s] = gmean(rr)
        print('| %s | ' % s + ' | '.join('%.3f' % S[s]['apps'][a]['run'] for a in apps) +
              ' | %.3f | %.3f | %.0f | %.1f |' % (gmean(rr), gmean(r6), 1000 * sum(S[s]['apps'][a]['load_med'] for a in apps), 1000 * S[s]['start']))
    print('\n**The whole system for one application** - the engine (as the lab packs it, where it can: designs/elf_tight.py),'
          ' the kernel image, and brainless\'s code; bytes:\n')
    print('| system | engine | kernel image | brainless\'s code | together |')
    print('|---|---:|---:|---:|---:|')
    for s in names:
        e = S[s].get('engine_tight') or S[s]['engine']; img = S[s]['image'] or 0
        b = S[s]['apps'].get('brainless', {}).get('code', 0)
        print('| {} | {:,} | {:,} | {:,} | {:,} |'.format(s, e, img, b, e + img + b))
    ds = [d for d in DESIGNS if d in S]
    if len(ds) >= 5:
        rec = {d: json.load(open(os.path.join(ROOT, 'designs', d, 'record.json'))) for d in ds}
        sk = 'speed' if cells == 8 else 'speed32'
        print('\n**Design against design** (Spearman, the %d designs):\n' % len(ds))
        print('- the kernel image\'s bytes (the lab\'s size score\'s image) against application code: %.2f' %
              spearman([S[d]['image'] for d in ds], [tot[d] for d in ds]))
        print('- engine and image (the lab\'s size score) against engine and brainless\'s code: %.2f' %
              spearman([rec[d]['total'] for d in ds], [(S[d].get('engine_tight') or S[d]['engine']) + S[d]['apps']['brainless']['code'] for d in ds]))
        print('- the lab\'s speed score (%s, on the selection\'s workloads) against these programs\' geomean: %.2f' %
              (sk, spearman([rec[d][sk] for d in ds], [gm[d] for d in ds])))
    print()
