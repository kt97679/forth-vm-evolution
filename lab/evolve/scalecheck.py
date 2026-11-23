#!/usr/bin/env python3
"""lab/evolve/scalecheck.py OLD-DB NEW-DB (Iteration 746) - did the machine's scale move between two runs? The stopping
rule compares a run's extremes with the previous run's at 2 % (speed) - a reading against s6 in the same round, so a step
in the scale between the runs (the machine's state, or a change that moves s6 and the designs unequally) would read as a
gain or hide one. The designs carried into both runs' generation 0 (the fronts of the newest databases, measured again
before any selection in either run) are the same designs read twice, unselected both times: their median ratio is the
step. One series' runs are one method, so nothing in the code moves it; a step there is the machine's.

Prints, for the JIT designs and the rest (the JIT expressed, as the roles' screen), the median of NEW / OLD over the
designs in both, with a 95 % interval (bootstrap of the median, 400 draws, a fixed seed) - at 64 bits and at 32; s6's
own time per workload in each run (the median over every generation-0 record of raw / t: t is a time over s6's in the
same round); the designs' times NEW / OLD per workload; the bytes and memory (exact: a difference means the code
differs). Last a line 'scalecheck: ...' that says whether the step is within 1 % for both kinds - outside that, the
stopping rule's speed criteria between these two runs carry it. Reads only; python3 -I -B. Half a minute per database.

OLD or NEW may be an extract instead of a database: lab/evolve/scalecheck.py --extract DB OUT.jsonl.gz writes a run's
generation-0 readings (each alive record's id, the JIT expressed, speeds, bytes, memory, raw and t, a few genes) - about
1 MB, so the next run's processing has its reference without the database: process-seed.sh compares the newest
results/gen0/seed*.jsonl.gz with the run's database (summary.md's section beside stopping.py) and writes the run's own.

Validated (Iteration 746, results/drafts/scalecheck-746.md): seed 95 -> 96 (one code, 19 lines of evolve.py's records
between) and seed 96 -> 97 (the series boundary: the after-seed-96 batch, fixenv, the layout)."""
import gzip, io, json, os, random, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv, sys.argv = sys.argv, sys.argv[:1]
import evolve as E                                             # noqa: E402 - for the JIT's expression only
sys.argv = _argv


KEEP = ('compiler', 'opt', 'threads', 'regpin', 'bss', 'lto', 'fsys', 'tag2', 'jit', 'factor', 'escape', 'opinline')


def gen0(path):
    out = {}
    if path.endswith('.gz'):                                    # an extract (--extract): generation 0 already
        for l in gzip.open(path, 'rt'):
            r = json.loads(l); out[r['id']] = r
        return out
    for l in open(path, errors='replace'):
        try: r = json.loads(l)
        except Exception: continue
        if r.get('gen') == 0 and r.get('status') == 'ok' and r.get('speed') and r.get('t'):
            out.setdefault(r['id'], r)
    return out


def jit(r):
    if 'jitx_' in r: return r['jitx_']                          # an extract's: the JIT expressed, worked out when written
    return bool(E.jit_on(E.canon(E.require(dict(r['genome'])))))


def extract(db, out):
    recs = gen0(db)
    tmp = out + '.tmp'
    with io.TextIOWrapper(gzip.GzipFile(tmp, 'wb', 9, mtime=0)) as f:     # mtime 0: the same run, the same bytes
        for i in sorted(recs):
            r = recs[i]
            x = {'id': i, 'jitx_': jit(r), 'speed': round(r['speed'], 6), 'speed32': r.get('speed32') and round(r['speed32'], 6),
                 'total': r.get('total'), 'rss': r.get('rss'), 'raw': r.get('raw', {}),
                 't': {w: round(v, 6) for w, v in r['t'].items()}, 'genome': {k: r['genome'].get(k) for k in KEEP if k in r['genome']}}
            f.write(json.dumps(x, separators=(',', ':'), sort_keys=True) + '\n')
    os.replace(tmp, out)
    print('scalecheck: extract %s - %d generation-0 records, %d bytes' % (out, len(recs), os.path.getsize(out)))


def interval(v, draws=400):
    rnd = random.Random(746)
    m = sorted(statistics.median(rnd.choices(v, k=len(v))) for _ in range(draws))
    return statistics.median(v), m[int(draws * 0.025)], m[int(draws * 0.975)]


def main():
    if len(sys.argv) == 4 and sys.argv[1] == '--extract': return extract(sys.argv[2], sys.argv[3])
    if len(sys.argv) != 3: sys.exit(__doc__)
    old, new = gen0(sys.argv[1]), gen0(sys.argv[2])
    both = sorted(i for i in old if i in new)
    if len(both) < 20: sys.exit('scalecheck: only %d designs in both runs\' generation 0 - no reading' % len(both))
    kind = {i: jit(new[i]) for i in both}                     # the JIT expressed: a record's genome, or an extract's
    print('generation 0: old %d alive, new %d; in both %d (JIT %d)' % (len(old), len(new), len(both), sum(kind.values())))
    verdict = []
    for name, sel in (('JIT', True), ('not JIT', False)):
        ids = [i for i in both if kind[i] == sel]
        if len(ids) < 10:
            print('  %-8s %d designs - too few' % (name, len(ids))); continue
        m, lo, hi = interval([new[i]['speed'] / old[i]['speed'] for i in ids])
        v32 = [new[i]['speed32'] / old[i]['speed32'] for i in ids if new[i].get('speed32') and old[i].get('speed32')]
        t32 = '%.3f (%.3f-%.3f, n %d)' % (*interval(v32), len(v32)) if len(v32) >= 10 else '-'
        print('  %-8s speed new / old %.3f (95 %% %.3f-%.3f, n %d); at 32 bits %s' % (name, m, lo, hi, len(ids), t32))
        verdict.append((name, m, lo, hi))
    W = [w for w in ('kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps')
         if any(w in r.get('raw', {}) for r in old.values()) and any(w in r.get('raw', {}) for r in new.values())]
    print('  %-10s %12s %12s %7s | the designs\' times new / old: %6s %8s' % ('workload', 's6 old', 's6 new', 'new/old', 'JIT', 'not JIT'))
    for w in W:
        s = [statistics.median([r['raw'][w] / r['t'][w] for r in run.values() if r.get('raw', {}).get(w) and r['t'].get(w)])
             for run in (old, new)]
        d = lambda sel: statistics.median([new[i]['raw'][w] / old[i]['raw'][w] for i in both if kind[i] == sel
                                           and old[i].get('raw', {}).get(w) and new[i].get('raw', {}).get(w)] or [float('nan')])
        print('  %-10s %12.0f %12.0f %7.3f | %38.3f %8.3f' % (w, s[0], s[1], s[1] / s[0], d(True), d(False)))
    db = [new[i]['total'] - old[i]['total'] for i in both if new[i].get('total') and old[i].get('total')]
    dm = [new[i]['rss'] - old[i]['rss'] for i in both if new[i].get('rss') and old[i].get('rss')]
    print('  bytes new - old: %d of %d differ (median %+d); memory KB: %d differ (median %+d)' % (
        sum(1 for x in db if x), len(db), statistics.median(db), sum(1 for x in dm if x), statistics.median(dm)))
    if os.environ.get('GENES'):                                 # GENES=1: where a step sits - by each gene's value
        for name, sel in (('JIT', True), ('not JIT', False)):
            ids = [i for i in both if kind[i] == sel]
            rows = []
            for g in sorted({k for i in ids for k in new[i]['genome']}):
                by = {}
                for i in ids:
                    by.setdefault(json.dumps(new[i]['genome'].get(g), sort_keys=True)[:24], []).append(new[i]['speed'] / old[i]['speed'])
                big = {v: x for v, x in by.items() if len(x) >= 40}
                if len(big) >= 2:
                    med = {v: statistics.median(x) for v, x in big.items()}
                    rows.append((max(med.values()) - min(med.values()), g, ', '.join('%s %.3f (%d)' % (v, med[v], len(big[v])) for v in sorted(big))))
            cells = {}
            for i in ids:
                g = new[i]['genome']; cells.setdefault(('clang' if g.get('compiler') else 'gcc', g.get('opt')), []).append(i)
            print('  by compiler and -O, %s: the speed new / old; loop\'s own time new / old, its range' % name)
            for c in sorted(cells, key=str):
                if len(cells[c]) < 40: continue
                lp = sorted(new[i]['raw']['loop'] / old[i]['raw']['loop'] for i in cells[c]
                            if new[i].get('raw', {}).get('loop') and old[i].get('raw', {}).get('loop'))
                print('    %-5s %-3s n %4d  speed %.3f | loop %.3f (%.2f-%.2f)' % (c[0], c[1], len(cells[c]), statistics.median(
                    new[i]['speed'] / old[i]['speed'] for i in cells[c]), statistics.median(lp), lp[0], lp[-1]))
            print('  by gene, %s (the widest spreads):' % name)
            for s, g, txt in sorted(rows, reverse=True)[:int(os.environ.get('GENES_N', '12'))]:
                print('    %-11s %.3f | %s' % (g, s, txt))
    out = all(lo <= 1.01 and hi >= 0.99 and abs(m - 1) <= 0.01 for name, m, lo, hi in verdict)
    print('scalecheck: %s - %s' % ('within 1 %' if out else 'A STEP', ', '.join('%s %.3f (%.3f-%.3f)' % v for v in verdict)))


if __name__ == '__main__':
    main()
