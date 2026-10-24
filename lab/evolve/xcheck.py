#!/usr/bin/env python3
"""xcheck.py - the front measured on another machine (Iteration 307).

Three modes, for next-run.sh's remote checks (results/drafts/runner-protocol.md):

  xcheck.py --sample RESULTS.md OUT.json [--n 24] [--no-jit] [--gcc-only] [--rejected K]
      on the laptop: designs of a front, to measure elsewhere - the fastest, those
      about the best Q (speed times binary + image), the smallest, and some between,
      a quarter each - with each design's genome, its expression here and its speed
      here. --no-jit and --gcc-only keep to the designs that can be themselves on a
      host without the JIT (32-bit) or without clang. --rejected K (Iteration 377): K of the n
      are designs the laptop's selection REJECTED - living, off the front, within its speed span,
      from the run's db.jsonl beside RESULTS.md, spread by speed - so a design good there and
      rejected here can be seen at all (results/drafts/cross-machine-weighing.md); marked in the
      report, with how many ran faster there than the front's median and fastest. --also ID,ID...
      (Iteration 428): designs asked for by id, from the repository's results/evolve-*.md (and any beside
      RESULTS.md - Iteration 429: in a chain RESULTS.md is the archived run's report.md), after the
      sample - the Tegra's rebuild test of the designs that once failed there (open item 0d); marked
      'asked', reported apart and kept out of the agreement, which is about this front. Iteration 430: genomes
      from results/candidates-*.md too, and a paired check (--from) takes its pair's asked designs.

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
      --laptop32 FILE (Iteration 402): the laptop's records, so a 4-byte host is compared against
      their 32-bit speeds too.
"""
import struct, json, math, os, platform, re, shutil, subprocess, sys, time

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
    L32 = opt('--laptop32')                                             # Iteration 402: see below
    R = json.load(open(opt('--report')))
    env = R.get('env', {})
    print('## %s - %s\n' % (env.get('host', '?'), env.get('cpu', '?')))
    print('%s-endian, %s-byte cells - measured on the host (Iteration 331)\n' % (env.get('byteorder', '?'), env.get('cell', '?')))   # Iteration 331
    print('%s, %s; %s; Python %s; measured %s, %d round(s) a design.\n' % (
        env.get('machine', '?'), env.get('kernel', '?'), env.get('cc', '?'), env.get('python', '?'), R.get('when', '?'), R.get('rounds', 0)))
    if not R.get('s6_ok'):
        print('**Not usable: hand-made s6 - %s.**' % R.get('s6_why', '?')); sys.exit(0)
    d = [x for x in R['designs'] if x.get('speed_here') is not None and not x.get('asked')]
    for x in R['designs']:
        if x.get('speed_here') is None and not x.get('asked'): print('- %s not measured: %s' % (x['id'], x.get('why', '?')))
    print()
    A = [x for x in R['designs'] if x.get('asked')]                   # Iteration 428: apart from the agreement
    if A:
        print('**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): %d of %d built and measured here.\n'
              % (sum(1 for x in A if x.get('speed_here') is not None), len(A)))
        for x in A: print('- %s %s' % (x['id'], 'speed %.3f here' % x['speed_here'] if x.get('speed_here') is not None else 'not measured: %s' % x.get('why', '?')))
        print()
    if len(d) < 3: print('Too few measured to rank (%d).' % len(d)); sys.exit(0)
    rho = spearman([x['speed'] for x in d], [x['speed_here'] for x in d])
    rh = ranks([x['speed_here'] for x in d])
    top = sorted(range(len(d)), key=lambda i: d[i]['speed'])[:6]
    print('**%d designs measured on both: Spearman %.3f** between the laptop\'s speeds and this host\'s.\n' % (len(d), rho))
    # Iteration 402 (open item 0g): --laptop32 FILE - the laptop's records (a results/evolve-*.md's front lines, or a
    # db.jsonl): for a run selected at both widths, a 4-byte host is compared against their speed32 as well - the laptop's
    # own 32-bit speeds, a two-encoding front ranking differently at 32 bits. Without it, as before.
    if L32:
        s32 = {}
        for line in open(L32):
            if line.startswith('{'):
                try: r = json.loads(line)
                except ValueError: continue
                if r.get('id') and r.get('speed32') is not None: s32[r['id']] = r['speed32']
        d32 = [x for x in d if x['id'] in s32]
        if len(d32) >= 3:
            print('**Against the laptop\'s 32-bit speeds** (%d of them, --laptop32): Spearman %.3f.\n' % (len(d32), spearman([s32[x['id']] for x in d32], [x['speed_here'] for x in d32])))
        else: print('Against the laptop\'s 32-bit speeds: %d of the designs have one (--laptop32) - too few to rank.\n' % len(d32))
    print('The laptop\'s six fastest, their rank here (of %d): %s.\n' % (len(d), ' '.join(str(rh[i] + 1) for i in top)))
    mv = sorted(d, key=lambda x: x['speed_here'] / x['speed'])
    print('| design | laptop | here | here / laptop |\n|---|---|---|---|')
    for x in mv[:3] + mv[-3:]:
        print('| %s%s | %.3f | %.3f | %.2f |' % (x['id'], ' (rejected)' if x.get('rejected') else '', x['speed'], x['speed_here'], x['speed_here'] / x['speed']))
    rj = [x for x in d if x.get('rejected')]; fr = [x for x in d if not x.get('rejected')]
    if rj and fr:                                                       # Iteration 377: the owner's question, measured
        fh = sorted(x['speed_here'] for x in fr); med, best = fh[len(fh) // 2], fh[0]
        am = [x['id'] for x in rj if x['speed_here'] < med]; ab = [x['id'] for x in rj if x['speed_here'] < best]
        print('\n**Rejected by the laptop\'s selection, measured here: %d** - faster here than the front\'s median: %d%s; '
              'than its fastest: %d%s.' % (len(rj), len(am), (' (%s)' % ', '.join(am)) if am else '', len(ab), (' (%s)' % ', '.join(ab)) if ab else ''))
    sys.exit(0)

# ---- --sample: the designs to measure elsewhere, picked on the laptop ----
if '--sample' in ARGS:
    src = opt('--sample'); n = int(opt('--n', '24')); nojit = opt('--no-jit', flag=True); gcc = opt('--gcc-only', flag=True); bundle = opt('--bundle')
    nrej = int(opt('--rejected', '0'))                                # Iteration 377: designs the selection rejected
    also = [i for i in (opt('--also') or '').split(',') if i]         # Iteration 428: designs asked for by id
    # Iteration 331: --cell 4 - a 32-bit check (the owner: 32-bit x86 and the Tegra, at native
    # 4-byte cells). The sample built here as 32-bit x86 at 4-byte cells (gcc -m32, static), each
    # design taken only if it builds and lives so - no JIT, no clang - and with --bundle the
    # 4-byte references a 64-bit-only host cannot make (build32/: the 32-bit cell engine, its
    # image, the base k32 dumps).
    cell4 = opt('--cell', '8') == '4'
    # Iteration 335: --ids FILE - exactly another check's designs (its designs.json), at this width:
    # the same designs at 64 bits and at 32 on one host, the width alone (seed 55's two samples
    # shared 8 designs, nearly all slow)
    idsf = opt('--ids'); idsd = json.load(open(idsf)) if idsf else None; ids = [d['id'] for d in idsd] if idsf else None
    if cell4:
        # Iteration 408: GCC only where the host builds the designs itself (native - the Tegra has no clang); a
        # prebuilt sample (--bundle) is built here, where clang builds 32-bit engines too (Iteration 336) - so
        # clang's designs are taken: with them out, dream's 32-bit check of seed 59's front had 6 eligible of 171.
        # Iteration 461: the JIT builds at 32-bit x86 now - a prebuilt sample (--bundle, built here with -m32) keeps the
        # designs with it; a host that builds itself at 4-byte cells (the Tegra, 32-bit ARM) has no JIT, so takes none.
        os.environ.setdefault('EVOLVE_CC', 'gcc -m32'); os.environ['EVOLVE_CELL'] = '4'; nojit = nojit or not bundle; gcc = gcc or not bundle
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
    pick = []; built = {}
    if cell4: E.setup()
    def good(i):
        """Iteration 331: at --cell 4, a design only if it builds and lives as a 32-bit engine here."""
        if not cell4: return True
        if i not in built:
            try:
                eng, img = E.build(E.canon(gen[i]), os.path.join(E.EV, 'xcheck-b-' + i)); E.alive(eng, img, E.private_work(os.path.join(E.EV, 'xcheck-b-' + i)))
                built[i] = (eng, img)
            except Exception as ex:
                built[i] = None; print('xcheck: %s left out at 4-byte cells - %s' % (i, str(ex)[:90]), flush=True)
        return built[i] is not None
    def take(seq, k):
        for x in seq:
            if k <= 0: break
            if x[0] not in [p[0] for p in pick] and good(x[0]): pick.append(x); k -= 1
    rejected = set(); asked = set()
    if ids is not None:
        byid = {x[0]: x for x in ok}
        for x in idsd:                                                   # Iteration 377: a rejected design, from the file itself
            if x['id'] not in byid and (x.get('rejected') or x.get('asked')) and 'genome' in x:   # 430: and one asked for by id
                e = E.express(E.canon(x['genome'])); gen[x['id']] = x['genome']
                if not (nojit and e.get('jit')) and not (gcc and (e.get('compiler') or e.get('tailpn'))):
                    byid[x['id']] = (x['id'], x['speed'], x.get('total'), e); (asked if x.get('asked') else rejected).add(x['id'])
        for i in ids:
            if i in byid and good(i): pick.append(byid[i])
    else:
        n_all = n; n = n - nrej if nrej > 0 else n
        q = n // 4
        take(sorted(ok, key=lambda x: x[1]), q)                          # the fastest
        take(sorted(ok, key=lambda x: x[1] * x[2]), q)                   # about the best Q (speed x size)
        take(sorted(ok, key=lambda x: x[2]), q)                          # the smallest
        rest = sorted([x for x in ok if x[0] not in [p[0] for p in pick]], key=lambda x: x[1])
        k = n - len(pick)
        if rest and k > 0: take([rest[int(j * (len(rest) - 1) / max(1, k - 1))] for j in range(k)], k)   # between, evenly
        if nrej > 0:                                                     # Iteration 377: the rejected, from the run's database
            dbp = os.path.join(os.path.dirname(os.path.abspath(src)), 'db.jsonl'); span = max((x[1] for x in ok), default=0); pool = []
            if not os.path.exists(dbp): print('xcheck: --rejected: no %s - none sampled' % dbp, flush=True)
            else:
                for l in open(dbp):
                    try: r = json.loads(l)
                    except ValueError: continue
                    i = r.get('id')
                    if r.get('status') != 'ok' or i in rows or 'genome' not in r or r.get('speed') is None or r['speed'] > span: continue
                    e = E.express(E.canon(r['genome']))
                    if nojit and e.get('jit'): continue
                    if gcc and (e.get('compiler') or e.get('tailpn')): continue
                    gen[i] = r['genome']; pool.append((i, r['speed'], r.get('total', r.get('size')), e))
                pool.sort(key=lambda x: x[1]); before = len(pick)
                if pool: take([pool[int(j * (len(pool) - 1) / max(1, nrej - 1))] for j in range(min(nrej, len(pool)))], nrej)
                rejected = {x[0] for x in pick[before:]}
        n = n_all
    if also:                                                             # Iteration 428: after the sample, by id
        import glob
        recs = {}
        # Iteration 429: the repository's results first - in a chain src is runs/archived-*/build/evolve/report.md,
        # where no results file lies (428's lookup looked only beside it, and would have found none there)
        # Iteration 430: and results/candidates-*.md - designs kept by id that no front holds (a rejected one's genome)
        for f in sorted(glob.glob(os.path.join(E.ROOT, 'results', 'evolve-*-seed*.md'))) + sorted(glob.glob(os.path.join(E.ROOT, 'results', 'candidates-*.md'))) + sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(src)), 'evolve-*-seed*.md'))):
            for l in open(f):
                if l.startswith('{"'):
                    try: r = json.loads(l)
                    except ValueError: continue
                    if r.get('id') in also and 'genome' in r: recs.setdefault(r['id'], r)
        for i in also:
            if i in [p[0] for p in pick]: continue
            r = recs.get(i)
            if not r: print('xcheck: --also %s: in no results file here - left out' % i, flush=True); continue
            e = E.express(E.canon(r['genome'])); gen[i] = r['genome']
            if (nojit and e.get('jit')) or (gcc and (e.get('compiler') or e.get('tailpn'))):
                print('xcheck: --also %s: not itself on this host (the JIT or clang) - left out' % i, flush=True); continue
            if not good(i): continue
            pick.append((i, r.get('speed') or 0.0, r.get('total'), e)); asked.add(i)
        print('xcheck: %d of %d asked for by id (--also, Iteration 428)' % (len(asked), len(also)), flush=True)
    json.dump([dict({'id': i, 'genome': gen[i], 'expressed': norm(e), 'speed': sp, 'total': tot}, **({'rejected': True} if i in rejected else {}), **({'asked': True} if i in asked else {})) for i, sp, tot, e in pick], open(out, 'w'), indent=1)
    if rejected: print('xcheck: %d of them rejected by the laptop\'s selection (Iteration 377)' % len(rejected), flush=True)
    print('xcheck: %d designs sampled from %d eligible (%s%s%s) into %s' % (len(pick), len(ok), 'no JIT ' if nojit else '', 'GCC only' if gcc else '', ', at 4-byte cells, each alive so' if cell4 else '', out))
    if bundle:
        import tarfile
        if not cell4: E.setup()
        stage = os.path.join(E.EV, 'xcheck-bundle'); shutil.rmtree(stage, ignore_errors=True)
        def put(name, eng, img):
            os.makedirs(os.path.join(stage, name)); shutil.copy2(eng, os.path.join(stage, name, 'engine')); shutil.copy2(img, os.path.join(stage, name, 'image'))
        put('s6', E.REF[0], E.REF[1])
        for i, *_ in pick:
            eng, img = built[i] if cell4 else E.build(E.canon(gen[i]), os.path.join(E.EV, 'xcheck-b-' + i)); put(i, eng, img)
        if cell4:
            os.makedirs(os.path.join(stage, 'build32'))
            for f in ('s0-cell-32', 's0-cell-s32.img', 'k32-self.txt', 'k32-b.txt'): shutil.copy2(os.path.join(E.O, f), os.path.join(stage, 'build32', f))
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
       'governor': readf('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'), 'load': readf('/proc/loadavg'),
       'byteorder': sys.byteorder, 'cell': int(os.environ.get('EVOLVE_CELL') or (4 if struct.calcsize('P') == 4 else 8))}   # Iteration 331: measured, not assumed
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
    if x.get('rejected'): rec['rejected'] = True                      # Iteration 377: carried to the report
    if x.get('asked'): rec['asked'] = True                            # Iteration 428: so is a design asked for by id
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
