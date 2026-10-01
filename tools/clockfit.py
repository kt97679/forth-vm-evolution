#!/usr/bin/env python3
"""clockfit.py - tell the clock apart from work outside user space.

CPU time and user-space cycles disagree for two reasons, and both weigh
most on short runs:

  the clock      at a lower one the same cycles take longer: CPU time
                 grows, cycles do not
  the kernel     starting the process, mapping memory, taking page
                 faults: CPU time counts it, user-space cycles do not

Their disagreement alone cannot tell the two apart. Each engine's runs
can. CPU time plotted against cycles over its five runs - start-up and
four workloads - is a line whose slope is the clock during the work. At
that clock a start-up run's cycles account for only part of its CPU
time, and the rest was spent outside user space. A clock that is 2% off
moves that estimate by 2% of the start-up's user-space time: about a
microsecond for the interpreters, whose start-up is mostly the kernel's,
some tens for the SPN systems, and about 0.15 ms for s8-full, which
translates everything at boot - hence the start-up column beside it.

The kernel's own split of CPU time into user and system time cannot do
this: it is sampled at timer ticks, and a run of a few milliseconds is
reported as all user or all system time depending on where one tick
fell. Tested: the same 2.7 ms of system calls came out as either.

    clockfit.py REPORT.md             the two sections, from the raw minima
                                      of a report tools/spn-bench.py wrote
    clockfit.py REPORT.md --rewrite   replace them in the report itself

tools/spn-bench.py writes them with the same functions.
"""
import re, statistics, sys

WORKLOADS = ['kernel', 'fib', 'corpus', 'parse']
SYSTEMS = ['s0-cell', 's5-cv8spec', 's6-cv8b', 's7-spn', 's8-spncv8', 's8-lazy', 's8-full', 'relf']
BASE = 's0-cell'
SAME_CLOCK = 3.0        # per cent: closer than this, the systems shared a clock


def stage_of(engine):
    """'s8-lazy-64-v2' -> 's8-lazy'"""
    return re.sub(r'-(32|64)(-v\d+)?$', '', engine.rsplit('/', 1)[-1])


def by_stage(best):
    """{(stage, engine): value} -> {stage: median over its engines}"""
    out = {}
    for (s, _e), v in best.items():
        out.setdefault(s, []).append(v)
    return {s: statistics.median(v) for s, v in out.items()}


def agreement(raw, systems=SYSTEMS, base=BASE, workloads=WORKLOADS):
    """The section 'Does CPU time agree with cycles?', as lines."""
    T = {w: by_stage(raw[w]['cpu']) for w in workloads}
    C = {w: by_stage(raw[w]['cyc']) for w in workloads}
    L = ['## Does CPU time agree with cycles?', '',
         'The CPU-time ratio minus the cycle ratio, as a percentage of the',
         'cycle ratio. Two things make them differ, and both weigh most on',
         'short runs: the clock - at a lower one the same cycles take longer,',
         'which CPU time sees and cycles do not - and work outside user space,',
         'the kernel starting the process, mapping memory and taking page',
         'faults, which CPU time counts and user-space cycles do not. The next',
         'section tells them apart.', '',
         '    %-12s' % 'stage' + ''.join('%12s' % w for w in workloads)]
    worst = 0.0
    for s in systems:
        if s == base or not any(s in T[w] for w in workloads):
            continue
        row = '    %-12s' % s
        for w in workloads:
            if s in T[w] and s in C[w] and base in T[w] and base in C[w]:
                rt, rc = T[w][s] / T[w][base], C[w][s] / C[w][base]
                d = 100.0 * (rt - rc) / rc
                worst = max(worst, abs(d))
                row += '%11.1f%%' % d
            else:
                row += '%12s' % '-'
        L.append(row)
    return L + ['', 'Largest difference: %.1f%%.' % worst, '']


def fit(raw, workloads=WORKLOADS):
    """-> {stage: [(clock GHz, start-up outside user space us), ...]},
    one pair per engine that has all five runs."""
    runs = ['bye'] + list(workloads)
    pts = {}
    for w in runs:
        for k, ns in raw[w]['cpu'].items():
            c = raw[w]['cyc'].get(k)
            if c:
                pts.setdefault(k, {})[w] = (c, ns)
    out = {}
    for (s, _e), p in pts.items():
        if len(p) < len(runs):
            continue
        xs = [p[w][0] for w in runs]
        ys = [p[w][1] for w in runs]
        mx, my = statistics.mean(xs), statistics.mean(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        if sxx == 0:
            continue
        a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx    # ns per cycle
        if a <= 0:
            continue
        c0, n0 = p['bye']
        out.setdefault(s, []).append((1.0 / a, (n0 - c0 * a) / 1000.0))
    return out


def clock(raw, systems=SYSTEMS, workloads=WORKLOADS):
    """The section 'Clock, and time outside user space', as lines."""
    per = fit(raw, workloads)
    L = ['## Clock, and time outside user space', '',
         "Each engine's CPU time against its cycles, over its five runs: the",
         'slope is the clock during the work. At that clock, the start-up',
         "run's cycles account for only part of its CPU time; the rest went",
         'outside user space - less exact the longer the start-up, by 2% of its',
         "user-space time if the clock is 2% off. Medians over layout variants.",
         "(The kernel's own user/system split cannot do this: it is sampled at",
         'timer ticks.)', '',
         '    %-12s %8s %14s %22s' % ('stage', 'GHz', 'start-up', 'outside user space')]
    ghz, out = {}, {}
    start = by_stage(raw['bye']['cpu'])
    for s in [s for s in systems if s in per] + sorted(set(per) - set(systems)):
        ghz[s] = statistics.median(x[0] for x in per[s])
        out[s] = statistics.median(x[1] for x in per[s])
        L.append('    %-12s %8.2f %11.2f ms %19.0f us' % (s, ghz[s], start[s] / 1e6, out[s]))
    L.append('')
    if not ghz:
        return L + ['No engine had all five runs; nothing to fit.', '']
    lo, hi = min(ghz.values()), max(ghz.values())
    spread = 100.0 * (hi - lo) / statistics.median(ghz.values())
    ko, kh = min(out.values()) / 1000.0, max(out.values()) / 1000.0
    if spread <= SAME_CLOCK:
        L += ['Every system ran at the same clock, %.2f-%.2f GHz, %.1f%% apart: the' % (lo, hi, spread),
              'clock does not explain the section above. What does is %.2f-%.2f ms' % (ko, kh),
              'per run outside user space - real cost, which the cycles table leaves',
              'out, so it flatters short runs. End to end, the CPU-time table is the',
              'measure. The stage tables subtract start-up, which removes most of it.', '']
    else:
        L += ['The systems ran at different clocks, %.2f-%.2f GHz, %.1f%% apart: CPU' % (lo, hi, spread),
              'time is distorted by the clock, so compare in cycles - remembering that',
              'they leave out the %.2f-%.2f ms per run spent outside user space.' % (ko, kh), '']
    return L


def parse(text):
    """The raw minima of a spn-bench report -> {run: {metric: {(stage, engine): n}}}."""
    if '## Raw minima' not in text:
        sys.exit('no "## Raw minima" section: not a tools/spn-bench.py report')
    raw = {}
    for m in re.finditer(r'^\s+(start-up|kernel|fib|corpus|parse)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$',
                         text.split('## Raw minima', 1)[1], re.M):
        w = 'bye' if m.group(1) == 'start-up' else m.group(1)
        d = raw.setdefault(w, {'cpu': {}, 'cyc': {}, 'ins': {}})
        k = (stage_of(m.group(2)), m.group(2))
        d['cpu'][k], d['cyc'][k], d['ins'][k] = (int(m.group(i)) for i in (3, 4, 5))
    if not raw or any(w not in raw for w in ['bye'] + WORKLOADS):
        sys.exit('no cycle counts in the raw minima: the report was measured without counters')
    return raw


def main(argv):
    if len(argv) < 2 or argv[1:2] == ['-h']:
        sys.exit(__doc__)
    path = argv[1]
    text = open(path).read()
    raw = parse(text)
    new = '\n'.join(agreement(raw) + clock(raw)) + '\n'
    if '--rewrite' not in argv[2:]:
        sys.stdout.write(new)
        return
    # Replace from the agreement section up to the section after it (and
    # an older report's clock section, if it had one).
    m = re.search(r'^## Does CPU time agree with cycles\?\n.*?(?=^## (?!Clock, and time)(?!Does CPU))',
                  text, re.M | re.S)
    if not m:
        sys.exit('no "## Does CPU time agree with cycles?" section to replace')
    open(path, 'w').write(text[:m.start()] + new + text[m.end():])
    print('rewrote %s' % path)


if __name__ == '__main__':
    main(sys.argv)
