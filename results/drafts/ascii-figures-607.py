"""results/drafts/ascii-figures-607.py [--ru] - the article's two ASCII diagrams, from the records (Iteration 607; the
owner: no pictures, ASCII diagrams where useful). 1: each run's hypervolume as bars (results/stopping-series.md: the
series 77-83, the confirmation runs, the random baseline). 2: the pooled true front (confirm.py's pool, 444) as speed
against size - J a design with the JIT, o one without - beside the random baseline's front (r, its results file) and
s6 (S, speed 1 by definition, 22,265 bytes at 8-byte cells: design.py s6-cv8b --keep). Speed in-run against s6, log
scale; size the stripped engine plus the image. --ru: the labels in Russian. As the build user (it imports the evolver)."""
import importlib.util, json, math, os, sys
RU = '--ru' in sys.argv
sys.argv = ['x']; sys.path.insert(0, 'lab/evolve'); import evolve as E, hv, stopping
_s = importlib.util.spec_from_file_location('confirm', 'lab/evolve/confirm.py'); CF = importlib.util.module_from_spec(_s); _s.loader.exec_module(CF)
T = (lambda en, ru: ru if RU else en)
L = [json.loads(l) for l in open('results/stopping-series.md') if l.startswith('{')]
rows = {}
for r in L:
    for k in ('seed', 'confirmation', 'random'):
        if r.get(k, 0) >= 77 and 'hv' in r: rows[(k, r[k])] = r
print('```')
print(T('hypervolume of each run\'s front (higher is better)', 'гиперобъём фронта каждого прогона (больше - лучше)'))
print()
for (k, n), r in sorted(rows.items(), key=lambda kv: kv[0][1]):
    name = {'seed': T('seed %d', 'seed %d'), 'confirmation': T('seed %d, confirming', 'seed %d, подтверждение'),
            'random': T('seed %d, random', 'seed %d, случайный')}[k] % n
    print('%-24s %-46s %.3f' % (name, '#' * int(round(r['hv'] / 0.38 * 46)), r['hv']))
print('```\n')
method, runs = stopping.series(stopping.LEDGER); runs = [r for r in runs if r['seed'] < 87]
P = {}
for f in CF.pool_files(runs + CF.confirmations(stopping.LEDGER, 87)): P.update(hv.load(f, E))
F = [P[i] for i in hv.true_front(P, E)]
Rr = hv.load('results/evolve-amd-ryzen-7-pro-8840hs-seed85.md', E); RF = [Rr[i] for i in hv.true_front(Rr, E)]
W, H, x0, x1, y0, y1 = 60, 16, math.log(0.125), math.log(2.4), 13000, 45000
grid = [[' '] * W for _ in range(H)]; rank = {' ': 0, 'o': 1, 'J': 2, 'r': 3, 'S': 4}
def put(speed, total, c):
    x = int((math.log(speed) - x0) / (x1 - x0) * (W - 1)); y = int((total - y0) / (y1 - y0) * (H - 1))
    if 0 <= x < W and 0 <= y < H and rank[c] > rank[grid[H - 1 - y][x]]: grid[H - 1 - y][x] = c
for r in F:
    if r.get('speed') and r.get('total'): put(r['speed'], r['total'], 'J' if E.express(E.canon(r['genome'])).get('jit') else 'o')
for r in RF:
    if r.get('speed') and r.get('total'): put(r['speed'], r['total'], 'r')
put(1.0, 22265, 'S')
print('```')
print(T('the pooled front: speed against s6 (log scale) and size', 'объединённый фронт: скорость к s6 (логарифмическая шкала) и размер'))
print()
for i, row in enumerate(grid):
    yv = y1 - i * (y1 - y0) / (H - 1)
    lab = (('%2d ' + T('KB', 'КБ')) % round(yv / 1000)) if i % 3 == 0 else '     '
    print('%s |%s' % (lab, ''.join(row).rstrip()))
print('      +' + '-' * W)
ticks = [0.15, 0.25, 0.5, 1.0, 2.0]; line = [' '] * (W + 8)
for t in ticks:
    x = int((math.log(t) - x0) / (x1 - x0) * (W - 1)) + 7; s = ('%g' % t)
    for k, ch in enumerate(s): line[x + k] = ch
print(''.join(line).rstrip())
print(T('       faster <- speed (CPU time against s6) -> slower', '       быстрее <- скорость (процессорное время к s6) -> медленнее'))
print()
print(T('J  a design with the JIT (x86 only)        o  a design without it',
        'J  вариант с JIT (только x86)              o  вариант без JIT'))
print(T('r  the random search\'s front               S  s6, where the ladder ended',
        'r  фронт случайного поиска                 S  s6, где закончилась лесенка'))
print(T('%d designs on the pooled front (%d with the JIT); the random search\'s %d' % (len(F), sum(1 for r in F if E.express(E.canon(r["genome"])).get("jit")), len(RF)),
        'на объединённом фронте вариантов: %d (с JIT: %d); у случайного поиска: %d' % (len(F), sum(1 for r in F if E.express(E.canon(r["genome"])).get("jit")), len(RF))))
print('```')
