#!/usr/bin/env python3
"""xcheck.py - the front measured on another machine (Iteration 307).

Three modes, for next-run.sh's remote checks (results/drafts/runner-protocol.md):

  xcheck.py --sample RESULTS.md OUT.json [--n 24] [--no-jit] [--gcc-only]
      on the laptop: designs of a front, to measure elsewhere - the fastest, those
      about the best Q (speed times binary + image), the smallest, and some between,
      a quarter each - with each design's genome, its expression here and its speed
      here. --no-jit and --gcc-only keep to the designs that can be themselves on a
      host without the JIT (32-bit) or without clang.

  xcheck.py DESIGNS.json OUT.json [--rounds N] [--until EPOCH]
      on the host, in a clone at the same commit, its stages built: the host's
      environment; hand-made s6 built and alive; then each design - itself here only if
      it expresses here as it did on the laptop (no clang: compiler and tailpn do not
      express; a 32-bit host: no JIT, 4-byte cells) - built, alive, and measured with
      evolve.measure against s6, back to back, as the comparison measures: the speed
      the geometric mean of the selection workloads' ratios, the held-out ones apart.
      At --until it stops measuring and keeps what it has. A progress line a design.

  xcheck.py --sample RESULTS.md OUT.json --bundle BIN.tar.gz [...]
      the same, and the designs built here - each engine and image, and s6's, in one
      tarball - for a host of the same architecture (dream.lan, x86-64): it measures
      these very binaries (--prebuilt), so a ranking that moves there moved for the
      machine alone, and a design built with clang is itself there without clang. The
      builds use no -march or -mtune: the x86-64 baseline (Iteration 307).

  xcheck.py DESIGNS.json OUT.json --prebuilt DIR [...]
      on the host, the bundle unpacked into DIR: no expression to compare and nothing
      to build - the binary is the design; s6 is the shipped one.

  xcheck.py --report OUT.json
      on the laptop: the host's speeds against the laptop's for the designs measured on
      both - the Spearman rank correlation, where the laptop's fastest rank there, the
      designs that moved most - as markdown.
"""
import json, math, os, platform, re, shutil, subprocess, sys, time

ARGS = sys.argv[1:]
def opt(name, default=None, flag=False):
    if name not in ARGS: return default
    i = ARGS.index(name)
    if flag: del ARGS[i]; return True
    v = ARGS[i + 1]; del ARGS[i:i + 2]; return v

def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
    for k, i in enumerate(o): r[i] = k
    return r

def spearman(a, b):
    n = len(a)
    if n < 3: return float('nan')
    ra, rb = ranks(a), ranks(b)
    return 1 - 6.0 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (n * (n * n - 1))

def norm(e):
    return json.loads(json.dumps(e, sort_keys=True))

# ---- --report: the laptop's speeds against the host's ----
if '--report' in ARGS:
    R = json.load(open(opt('--report')))
    env = R.get('env', {})
    print('## %s - %s\n' % (env.get('host', '?'), env.get('cpu', '?')))
    print('%s, %s; %s; Python %s; measured %s, %d round(s) a design.\n' % (
        env.get('machine', '?'), env.get('kernel', '?'), env.get('cc', '?'), env.get('python', '?'), R.get('when', '?'), R.get('rounds', 0)))
    if not R.get('s6_ok'):
        print('**Not usable: hand-made s6 - %s.**' % R.get('s6_why', '?')); sys.exit(0)
    d = [x for x in R['designs'] if x.get('speed_here') is not None]
    for x in R['designs']:
        if x.get('speed_here') is None: print('- %s not measured: %s' % (x['id'], x.get('why', '?')))
    print()
    if len(d) < 3: print('Too few measured to rank (%d).' % len(d)); sys.exit(0)
    rho = spearman([x['speed'] for x in d], [x['speed_here'] for x in d])
    rh = ranks([x['speed_here'] for x in d])
    top = sorted(range(len(d)), key=lambda i: d[i]['speed'])[:6]
    print('**%d designs measured on both: Spearman %.3f** between the laptop\'s speeds and this host\'s.\n' % (len(d), rho))
    print('The laptop\'s six fastest, their rank here (of %d): %s.\n' % (len(d), ' '.join(str(rh[i] + 1) for i in top)))
    mv = sorted(d, key=lambda x: x['speed_here'] / x['speed'])
    print('| design | laptop | here | here / laptop |\n|---|---|---|---|')
    for x in mv[:3] + mv[-3:]:
        print('| %s | %.3f | %.3f | %.2f |' % (x['id'], x['speed'], x['speed_here'], x['speed_here'] / x['speed']))
    sys.exit(0)

# ---- --sample: the designs to measure elsewhere, picked on the laptop ----
if '--sample' in ARGS:
    src = opt('--sample'); n = int(opt('--n', '24')); nojit = opt('--no-jit', flag=True); gcc = opt('--gcc-only', flag=True); bundle = opt('--bundle')
    if len(ARGS) != 1: sys.exit(__doc__)
    out = ARGS[0]
    sys.argv = [sys.argv[0]]; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
    L = open(src).read().split('\n')
    h = next(i for i, l in enumerate(L) if l.startswith('| design | speed |'))
    cols = [c.strip() for c in L[h].strip().strip('|').split('|')]
    si, ti = cols.index('speed'), cols.index('binary + image')
    rows = {}
    for l in L[h + 2:]:
        if not l.startswith('| '): break
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        try: rows[c[0]] = (float(c[si]), int(c[ti].replace(',', '')))
        except ValueError: pass
    gen = {}
    for l in L:
        if l.startswith('{"bin"'):
            r = json.loads(l); gen[r['id']] = r['genome']
    ok = []
    for i, (sp, tot) in rows.items():
        if i not in gen: continue
        e = E.express(E.canon(gen[i]))
        if nojit and e.get('jit'): continue
        if gcc and (e.get('compiler') or e.get('tailpn')): continue
        ok.append((i, sp, tot, e))
    pick = []
    def take(seq, k):
        for x in seq:
            if k <= 0: break
            if x[0] not in [p[0] for p in pick]: pick.append(x); k -= 1
    q = n // 4
    take(sorted(ok, key=lambda x: x[1]), q)                          # the fastest
    take(sorted(ok, key=lambda x: x[1] * x[2]), q)                   # about the best Q (speed x size)
    take(sorted(ok, key=lambda x: x[2]), q)                          # the smallest
    rest = sorted([x for x in ok if x[0] not in [p[0] for p in pick]], key=lambda x: x[1])
    k = n - len(pick)
    if rest and k > 0: take([rest[int(j * (len(rest) - 1) / max(1, k - 1))] for j in range(k)], k)   # between, evenly
    json.dump([{'id': i, 'genome': gen[i], 'expressed': norm(e), 'speed': sp, 'total': tot} for i, sp, tot, e in pick], open(out, 'w'), indent=1)
    print('xcheck: %d designs sampled from %d eligible (%s%s) into %s' % (len(pick), len(ok), 'no JIT ' if nojit else '', 'GCC only' if gcc else '', out))
    if bundle:
        import tarfile
        E.setup()
        stage = os.path.join(E.EV, 'xcheck-bundle'); shutil.rmtree(stage, ignore_errors=True)
        def put(name, eng, img):
            os.makedirs(os.path.join(stage, name)); shutil.copy2(eng, os.path.join(stage, name, 'engine')); shutil.copy2(img, os.path.join(stage, name, 'image'))
        put('s6', E.REF[0], E.REF[1])
        for i, *_ in pick:
            eng, img = E.build(E.canon(gen[i]), os.path.join(E.EV, 'xcheck-b-' + i)); put(i, eng, img)
        with tarfile.open(bundle + '.partial', 'w:gz') as t: t.add(stage, arcname='bin')
        os.replace(bundle + '.partial', bundle)
        print('xcheck: %d designs and s6 built into %s (%d KB)' % (len(pick), bundle, os.path.getsize(bundle) // 1024))
    sys.exit(0)

# ---- the host's run ----
rounds = int(opt('--rounds', '3')); until = float(opt('--until', '0')) or None; pre = opt('--prebuilt')
if len(ARGS) != 2: sys.exit(__doc__)
src, out = ARGS
sys.argv = [sys.argv[0]]; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E

def first(cmd):
    try: return (subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout or '').strip().split('\n')[0]
    except (OSError, subprocess.TimeoutExpired): return 'none'
def readf(p):
    try: return open(p).read().strip()
    except OSError: return '?'
cpu = next((l.split(':', 1)[1].strip() for l in readf('/proc/cpuinfo').split('\n') if l.startswith(('model name', 'Hardware', 'Processor'))), platform.processor() or '?')
env = {'host': platform.node(), 'cpu': cpu, 'machine': platform.machine(), 'kernel': platform.release(), 'cc': first(['cc', '--version']),
       'clang': first(['clang', '--version']), 'python': platform.python_version(), 'sh': os.path.realpath('/bin/sh'),
       'locale': os.environ.get('LC_ALL') or os.environ.get('LANG') or '', 'cores': os.cpu_count(), 'free_gb': round(shutil.disk_usage('.').free / 2 ** 30, 1),
       'governor': readf('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'), 'load': readf('/proc/loadavg')}
R = {'env': env, 'when': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), 'rounds': rounds, 'designs': [], 's6_ok': False}
def save(): json.dump(R, open(out + '.partial', 'w'), indent=1); os.replace(out + '.partial', out)
print('xcheck: %s, %s, %s cores; %s' % (env['host'], env['cpu'], env['cores'], env['cc']), flush=True)
D = json.load(open(src))
E.setup()
WS = E.WORK_SEL + E.WORK_HELD + E.WORK_FAR
R['prebuilt'] = bool(pre)
try:
    if pre:                                   # the laptop's binaries: s6 the shipped one, the reference too
        eng, img = os.path.join(pre, 's6', 'engine'), os.path.join(pre, 's6', 'image')
        shutil.rmtree(os.path.join(E.EV, 'xcheck-s6-pre'), ignore_errors=True)   # a run before this one's (private_work refuses it)
        E.REF = (eng, img, E.private_work(os.path.join(E.EV, 'xcheck-s6-pre')))
        E.alive(eng, img, E.REF[2])
    else:
        s6 = E.canon(E.HUMAN['s6-cv8b']); d = os.path.join(E.EV, 'xcheck-s6'); shutil.rmtree(d, ignore_errors=True)
        eng, img = E.build(s6, d); E.alive(eng, img, E.private_work(d))
    R['s6_ok'] = True
    print('xcheck: s6 built and alive', flush=True)
except Exception as ex:
    R['s6_why'] = str(ex)[:300]; save(); print('xcheck: s6 failed - %s' % R['s6_why'], flush=True); sys.exit(1)
save()
for k, x in enumerate(D, 1):
    rec = {'id': x['id'], 'speed': x['speed'], 'total': x.get('total')}
    R['designs'].append(rec)
    if until and time.time() > until: rec['why'] = 'the time limit'; save(); continue
    g = E.canon(x['genome']); e = norm(E.express(g))
    if not pre and e != x['expressed']:
        diff = sorted(set(k_ for k_ in set(e) | set(x['expressed']) if e.get(k_) != x['expressed'].get(k_)))
        rec['why'] = 'not itself here: %s' % ', '.join(diff); save()
        print('xcheck: %d/%d %s not itself here (%s)' % (k, len(D), x['id'], ', '.join(diff)), flush=True); continue
    try:
        d = os.path.join(E.EV, 'xcheck-' + x['id']); shutil.rmtree(d, ignore_errors=True)   # an earlier run's: a design recurs
        if pre: eng, img = os.path.join(pre, x['id'], 'engine'), os.path.join(pre, x['id'], 'image')
        else: eng, img = E.build(g, d)
        pw = E.private_work(d); E.alive(eng, img, pw)
        m = E.measure(eng, img, pw, WS, rounds)
        ratios = m[0] if isinstance(m, tuple) else m
        rec['ratios'] = {w: ratios[w] for w in WS if w in ratios}
        rec['speed_here'] = math.exp(sum(math.log(ratios[w]) for w in E.WORK_SEL) / len(E.WORK_SEL))
        print('xcheck: %d/%d %s speed %.3f here (laptop %.3f)' % (k, len(D), x['id'], rec['speed_here'], x['speed']), flush=True)
    except Exception as ex:
        rec['why'] = 'failed here: %s' % str(ex)[:300]
        print('xcheck: %d/%d %s failed - %s' % (k, len(D), x['id'], rec['why']), flush=True)
    save()
print('xcheck: done - %d of %d measured' % (sum(1 for r in R['designs'] if 'speed_here' in r), len(D)), flush=True)
