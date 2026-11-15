#!/usr/bin/env python3
"""lab/evolve/appsize-check.py [--quick] [--out FILE] - evolve.py's rec['app'] checked against genapps.py (Iteration 677:
step 0 of results/drafts/search-reopen-plan-677.md - the size score counts the code the selection's four apps lay).

 1. The same binaries: genapps.py --sizes on s6 and the ten designs of designs/ (their engines, the self-built images
    since 676), and evolve.py's app_size() on the same files - every app's code equal, byte for byte, at both widths.
 2. The search's own images: each design built by evolve.build() from its record's genome - the translator's image, the
    one the records measure - app_size() at both widths, beside results/generic-apps-674.md's table (designs/ held the
    translator's images at 674). Reported: a kernel change since 674 moves it, and that is not a fault of the measure.
 3. Planted (prompts/15): one definition more in sim16 must move its code; an ALLOT more must not (it is data).
 4. The guard: a database holding a design of the old size is refused a resume.
 5. The cross-run tools (Iteration 679): compare-fronts refuses databases of both sizes; stopping.py judges a run only
    against a series of its own size; appsize.one_size(), which they and final-pick call.
--quick (run-tests): 1 on s6 at 8-byte cells, 3 and 5. Exit 0 when 1, 3 and 4 hold; the last line says PASS or FAIL."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
sys.path.insert(0, HERE_); import appsize
sys.argv, ARGV = sys.argv[:1], sys.argv[1:]          # evolve.py reads sys.argv at import for a few settings
import importlib.util
spec = importlib.util.spec_from_file_location('evolve', os.path.join(HERE_, 'evolve.py')); E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)
QUICK = '--quick' in ARGV
OUT = ARGV[ARGV.index('--out') + 1] if '--out' in ARGV else os.path.join(ROOT, 'build', 'appsize-check.json')
B = os.path.join(ROOT, 'build')
fails, report = [], {}

def workdir(tmp, plant=None):
    """A directory with the four programs and their drivers, as evolve.py's setup() lays them (plant: sim16's text)."""
    os.makedirs(tmp, exist_ok=True)
    for app in appsize.SELECTION:
        src = open(os.path.join(HERE_, 'apps', appsize.FILES[app]), 'rb').read()
        if app == 'sim16' and plant: src = src + plant
        open(os.path.join(tmp, appsize.FILES[app]), 'wb').write(src)
        for m in ('size', 'count'): open(os.path.join(tmp, appsize.driver_name(app, m)), 'w').write(appsize.lab_text(app, m))
    return tmp

def systems(cells):
    """genapps.py's lab systems at a width: name -> (engine, image)."""
    s = {'s6': (os.path.join(B, 's6-cv8b-%d' % (64 if cells == 8 else 32)), os.path.join(B, 's6-cv8b-s%d.img' % (64 if cells == 8 else 32)))}
    if not QUICK:
        for d in [l for l in re.findall(r"'([\w-]+)'", re.search(r'DESIGNS = \[([^\]]*)\]', open(os.path.join(HERE_, 'genapps.py')).read()).group(1))]:
            s[d] = (os.path.join(ROOT, 'designs', d, 'forth' if cells == 8 else 'forth32'), os.path.join(ROOT, 'designs', d, 'image.img' if cells == 8 else 'image32.img'))
    return s

tmp = tempfile.mkdtemp(prefix='appsize-check-')
try:
    # ---- 1: the same binaries, both counts
    for cells in ((8,) if QUICK else (8, 4)):
        S = systems(cells); out = os.path.join(tmp, 'g%d.json' % cells)
        r = subprocess.run([sys.executable, os.path.join(HERE_, 'genapps.py'), '--sizes', '--cells', str(cells), '--apps', ','.join(appsize.SELECTION),
                            '--systems', ','.join(S), '--out', out], capture_output=True, text=True)
        if r.returncode: fails.append('genapps.py at %d: %s' % (cells, (r.stdout + r.stderr)[-300:])); continue
        G = json.load(open(out))['systems']; pw = workdir(os.path.join(tmp, 'w%d' % cells))
        for name, (eng, img) in S.items():
            mine = E.app_size(eng, img, pw); theirs = [G[name]['apps'][a]['code'] for a in appsize.SELECTION]
            report.setdefault('same-binaries-%d' % cells, {})[name] = {'evolve': mine, 'genapps': theirs}
            if mine != theirs: fails.append('1: %s at %d: evolve %s, genapps %s' % (name, cells, mine, theirs))
        print('appsize-check: 1 at %d-byte cells: %d systems, %s' % (cells, len(S), 'equal' if not [f for f in fails if f.startswith('1: ')] else 'DIFFER'), flush=True)
    # ---- 3: planted
    eng, img = systems(8)['s6']
    base = E.app_size(eng, img, workdir(os.path.join(tmp, 'p0')))
    more = E.app_size(eng, img, workdir(os.path.join(tmp, 'p1'), b'\n: PLANTED-677 DUP + ;\n'))
    data = E.app_size(eng, img, workdir(os.path.join(tmp, 'p2'), b'\nCREATE PLANTED-677B 100 ALLOT\n'))
    report['planted'] = {'base': base, 'definition': more, 'allot': data}
    if not (more[0] > base[0] and more[1:] == base[1:]): fails.append('3: a definition more in sim16 did not move it only: %s -> %s' % (base, more))
    # CREATE lays a header (code, names and headers count); the 100 bytes it ALLOTs must not
    if not (0 < data[0] - base[0] < 100): fails.append('3: CREATE + 100 ALLOT moved sim16 by %d (its header only, under 100)' % (data[0] - base[0]))
    print('appsize-check: 3 planted: sim16 %d, a definition more %d, CREATE 100 ALLOT %d' % (base[0], more[0], data[0]), flush=True)
    # ---- 5 (Iteration 679): the cross-run tools never pool the two sizes
    def fake(path, app):
        with open(path, 'w') as f:
            for k in range(3):
                r = dict(id='%010x' % (k + 16 * app), status='ok', speed=1.0 + k / 10, speed32=1.0 + k / 10, size=9000, bin=20000,
                         total=29000 - 100 * k + 7000 * app, rss=100, genome={}, gen=k)
                if app: r['app'] = 7000
                f.write(json.dumps(r) + '\n')
        return path
    o5, n5 = fake(os.path.join(tmp, 'old.jsonl'), 0), fake(os.path.join(tmp, 'new.jsonl'), 1)
    run_ = lambda *c: subprocess.run([sys.executable] + list(c), capture_output=True, text=True)
    five = {}
    r = run_(os.path.join(HERE_, 'compare-fronts.py'), o5, n5); five['compare-fronts mixed'] = r.returncode != 0 and 'never pooled' in r.stdout + r.stderr
    for name, line, want in (('stopping old series', {'seed': 1, 'hv': 0.5, 'fastest': 1.0, 'smallest': 29000, 'memory': 100, 'fastest32': 1.0}, True),
                             ('stopping new series', {'seed': 1, 'hv': 0.5, 'fastest': 1.0, 'smallest': 36000, 'memory': 100, 'fastest32': 1.0, 'app': True}, False)):
        led = os.path.join(tmp, 'ledger.md'); open(led, 'w').write('{"method": "check"}\n' + json.dumps(line) + '\n')
        r = run_(os.path.join(HERE_, 'stopping.py'), n5, '--seed', '2', '--ledger', led); refused = 'open a new series' in r.stdout + r.stderr
        five[name] = refused == want and (want or 'verdict' in r.stdout)
    try: appsize.one_size(list(appsize.db_records(o5)) + list(appsize.db_records(n5)), 'x'); five['one_size mixed'] = False
    except SystemExit: five['one_size mixed'] = True
    five['one_size one each'] = appsize.one_size(appsize.db_records(n5), 'x') is True and appsize.one_size(appsize.db_records(o5), 'x') is False
    report['cross-run'] = five
    for k, v in five.items():
        if not v: fails.append('5: %s' % k)
    print('appsize-check: 5 the cross-run tools: %d of %d right (%s)' % (sum(five.values()), len(five), ', '.join(k for k, v in five.items() if not v) or 'all'), flush=True)
    if not QUICK:
        # ---- 2: the translator's images of the ten, from their genomes
        t674 = open(os.path.join(ROOT, 'results', 'generic-apps-674.md')).read().split('## What each construct costs')[0]
        tabs = re.split(r'\n\| system \| sim16', t674)[1:3]
        want = {c: {m.group(1): [int(x.replace(',', '')) for x in m.groups()[1:]] for m in re.finditer(r'\n\| ([\w-]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|', tab)}
                for c, tab in zip((8, 4), tabs)}
        E.TWO_WIDTHS[0] = True; E.setup_widths()
        for d in [n for n in systems(8) if n != 's6']:
            g = E.canon(json.load(open(os.path.join(ROOT, 'designs', d, 'record.json')))['genome'])
            dd = os.path.join(tmp, 'b-' + d); eng, img = E.build(g, dd); a8 = E.app_size(eng, img, E.private_work(dd))
            g32 = dict(g)
            if (g32.get('scale') or 0) > 2: g32['scale'] = 2
            g32 = E.canon(g32); dd = os.path.join(tmp, 'b32-' + d)
            with E.at_width(E.WIDTH4):
                eng, img = E.build(g32, dd); a4 = E.app_size(eng, img, E.private_work(dd))
            report.setdefault('translator', {})[d] = {'8': a8, '4': a4, '674-8': want[8].get(d), '674-4': want[4].get(d)}
            print('appsize-check: 2 %-16s 8: %s %s 674   4: %s %s 674' % (d, sum(a8), '=' if a8 == want[8].get(d) else '!=', sum(a4), '=' if a4 == want[4].get(d) else '!='), flush=True)
        # ---- 4: the guard - main() on a database of the old size (setup skipped, as test-resume.py does)
        db = os.path.join(tmp, 'old.jsonl')
        open(db, 'w').write(json.dumps({'id': '0123456789', 'status': 'ok', 'speed': 1.0, 'size': 9000, 'bin': 20000, 'total': 29000, 'rss': 100, 'genome': {}}) + '\n')
        E.setup_widths = E.setup = lambda *a, **k: None
        try: E.main(['--db', db, '--pop', '2', '--gens', '1']); msg = 'ran'
        except SystemExit as e: msg = str(e.code)
        report['guard'] = msg
        if 'before Iteration 677' not in msg: fails.append('4: a database of the old size resumed: %s' % msg[:120])
        print('appsize-check: 4 the guard: %s' % ('refused' if 'before Iteration 677' in msg else 'NOT refused'), flush=True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
report['fails'] = fails
if not QUICK: json.dump(report, open(OUT, 'w'), indent=1)
for f in fails: print('appsize-check: ' + f)
print('appsize-check: %s - %s' % ('PASS' if not fails else 'FAIL', 'the measure is genapps.py\'s' if not fails else '%d failed' % len(fails)))
sys.exit(1 if fails else 0)
