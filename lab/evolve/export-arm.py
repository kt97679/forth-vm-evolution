#!/usr/bin/env python3
"""lab/evolve/export-arm.py OUT DB NAME=ID[,NAME=ID...] [--gcc CC] [--list] - the 32-bit ARM build added to exported designs
(Iteration 646; the owner: engines without the C library everywhere - designs/ shipped them for x86 only, ARM pointed at
forth-libc). After lab/evolve/export-designs.py OUT: for each design of the list without the JIT, evolve.py's own build
at 4-byte cells for ARMv7 without the C library (engine/rt-linux-armv7.c, Iteration 570), as the lab built what the Tegra
measured - every command recorded (as export-designs.py), the compile command's inputs copied into OUT/NAME/srcarm/, and
the rule written into OUT/NAME/Makefile as `forth-arm`, its compiler $(CCARM):
  a clang design: cross-built on x86-64 (EVOLVE_TARGET=armv7 - clang, lld; the Tegra has no clang), CCARM the cross clang
      - the bytes the Tegra ran;
  a GCC design: built as on an ARM host (evolve.ARM32), CCARM `cc` - the ARM host's own: on the Tegra natively (the bytes
      it measured, GCC 16); on x86-64 with --gcc CC (arm-linux-gnueabihf-gcc), the Tegra simulated - the rule and its
      running checked, not the Tegra's bytes.
The image must be the one exported for 4-byte cells (OUT/NAME/image32.img). Then the check, in a fresh directory holding
only OUT/NAME: `make forth-arm` (CCARM=CC with --gcc) builds the lab's engine byte for byte (tightened as build() does),
and it runs ': SQ DUP * ; 7 SQ .' to 49 - under qemu-arm on x86-64, natively on ARM. Exit 1 if any design fails.
Which designs a run takes: on x86-64 without --gcc the clang ones, with --gcc the GCC ones; on an ARM host the GCC ones.
Each design's class (clang or GCC, the JIT or not) is the lab's x86-64 export's - OUT/NAME/Makefile's `CC =` and src/jit.c
among its sources - never this host's express(): on the Tegra jit_on() wants x86_64 and the compiler gene clang on the
PATH, so every design looked a GCC one without the JIT (Iteration 652: the chain at 2e9343d91f took best-all-round, a
clang JIT design, and failed on its image). On x86-64 the two must agree. --list: each design's class and whether this
host takes it, nothing built.
Needs on x86-64 `CROSS=1 sh tools/setup-sandbox.sh` (lld, qemu-user) and, for --gcc, gcc-arm-linux-gnueabihf. As the
build user, in a built tree; after export-designs.py OUT, every time (it writes the Makefiles afresh)."""
import hashlib, json, os, re, shlex, shutil, subprocess, sys, tempfile
A = sys.argv[1:]
gcc = None
if '--gcc' in A: k = A.index('--gcc'); gcc = A[k + 1]; del A[k:k + 2]
LIST = '--list' in A
if LIST: A.remove('--list')
if len(A) != 3: sys.exit(__doc__)
OUT, DB = os.path.abspath(A[0]), A[1]
PAIRS = [tuple(p.split('=', 1)) for p in A[2].split(',')]
NATIVE = os.uname().machine.startswith('arm')
if NATIVE and gcc: sys.exit('export-arm: --gcc simulates the Tegra on x86-64; on an ARM host its cc builds')
os.environ['EVOLVE_CELL'] = '4'                          # as tools/arm-cross-check.py sets up a 4-byte-cell ARM build
if gcc: os.environ['EVOLVE_CC'] = gcc
elif not NATIVE: os.environ.setdefault('EVOLVE_CC', 'gcc -m32 -fno-pie -no-pie')
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
if gcc: E.ARM32 = True                                   # as on the Tegra: ccflags drops alignhot, rt() is ARM's
if not LIST: E.setup()                                  # --list builds nothing (652)
R = {json.loads(l)['id']: json.loads(l) for l in open(DB) if l.startswith('{')}
LOG = []
_sh = E.sh
def sh(cmd, cwd=None, inp=None, timeout=300, env=None, cpu=60):
    LOG.append([str(c) for c in cmd])
    if not NATIVE and cmd and str(cmd[0]).endswith('/engine') and '/arm-' in str(cmd[0]):   # an ARM engine: qemu-arm
        return subprocess.run(['qemu-arm'] + list(cmd), cwd=cwd, input=inp, capture_output=True, timeout=4 * timeout)
    return _sh(cmd, cwd=cwd, inp=inp, timeout=timeout, env=env, cpu=cpu)
E.sh = sh
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
CROSS = ' '.join(E.ARM_CROSS_CC)
def lab_class(d):
    """(clang, jit) as the lab's x86-64 export made the design: its Makefile's `CC =`, src/jit.c in its SRC (Iteration 652)."""
    t = open(os.path.join(d, 'Makefile')).read(); m = re.search(r'^CC = (\S+)', t, re.M)
    if not m: sys.exit('export-arm: %s - no `CC =` in its Makefile' % d)
    return m.group(1) == 'clang', bool(re.search(r'^SRC = .*\bsrc/jit\.c\b', t, re.M))
made, bad = [], 0
for name, i in PAIRS:
    d = os.path.join(OUT, name); sd = os.path.join(d, 'srcarm')
    if not os.path.exists(os.path.join(d, 'Makefile')): sys.exit('export-arm: %s - export-designs.py first' % d)
    clang, jit = lab_class(d)
    if not NATIVE and i in R:                         # on x86-64 express() is the lab's: the export must say the same
        g = E.canon(R[i]['genome'])
        if (clang, jit) != (E.CC(g) == 'clang', bool(E.express(g).get('jit'))):
            sys.exit('export-arm: %s (%s) - its Makefile and express() disagree on clang or the JIT' % (name, i))
    take = not jit and clang == (not gcc and not NATIVE)   # the JIT is x86 code; each design its host's run
    if LIST:
        print('%s (%s): %s, %s - %s' % (name, i, 'clang' if clang else 'GCC', 'the JIT' if jit else 'no JIT',
              'taken here' if take else 'not this host\'s'), flush=True); continue
    if not take: continue
    if i not in R: sys.exit('export-arm: %s not in %s' % (i, DB))
    g = E.canon(R[i]['genome'])
    shutil.rmtree(sd, ignore_errors=True); os.makedirs(sd)
    b = os.path.join(E.EV, 'arm-export-%s' % i); shutil.rmtree(b, ignore_errors=True); del LOG[:]
    if clang: os.environ['EVOLVE_TARGET'] = 'armv7'
    try: eng, img = E.build(g, b)
    finally: os.environ.pop('EVOLVE_TARGET', None)
    pre = E.ARM_CROSS_CC if clang else None
    cc = [c for c in LOG if '-o' in c and c[c.index('-o') + 1] == eng and (c[:len(pre)] == pre if pre else
          os.path.basename(c[0]) in ('cc', 'gcc') or c[0] == (gcc or '').split()[0])]
    if len(cc) != 1: sys.exit('export-arm: %s - %d compile commands for the engine' % (i, len(cc)))
    cmd = cc[0]; k = cmd.index('-o'); n0 = len(pre) if pre else 1
    dep = subprocess.run(cmd[:k] + cmd[k + 2:] + ['-MM'], cwd=b, capture_output=True, text=True)
    if dep.returncode: sys.exit('export-arm: -MM failed for %s: %s' % (i, dep.stderr[-300:]))
    for f in sorted({os.path.normpath(os.path.join(b, t)) for t in dep.stdout.replace('\\\n', ' ').split() if not t.endswith(':')}):
        shutil.copy(f, os.path.join(sd, os.path.basename(f)))
    out = ['$(CCARM)']
    for j, a in enumerate(cmd):
        if j < n0: continue
        if j == k + 1: out.append('forth-arm'); continue
        if cmd[j - 1] in ('-I', '-iquote', '-isystem') and os.path.isdir(a): out.append('srcarm'); continue
        if re.match(r'^-I/', a) and os.path.isdir(a[2:]): out.append('-Isrcarm'); continue
        m = re.match(r'^(-[A-Za-z][^/]*?)?(/.*)$', a)
        if m and os.path.isfile(m.group(2)):
            t = os.path.join(sd, os.path.basename(m.group(2)))
            if not os.path.exists(t): shutil.copy(m.group(2), t)
            elif sha(t) != sha(m.group(2)): sys.exit('export-arm: two files named %s for %s' % (os.path.basename(t), i))
            out.append((m.group(1) or '') + 'srcarm/' + os.path.basename(t)); continue
        if '/' in a and os.path.isabs(a.split('=')[-1]): sys.exit('export-arm: %s - an absolute path left in %r' % (i, a))
        out.append(a)
    if sha(img) != sha(os.path.join(d, 'image32.img')): sys.exit('export-arm: %s - the ARM image is not image32.img' % i)
    mk = open(os.path.join(d, 'Makefile')).read().split('\n')
    mk = [l for l in mk if not l.startswith(('CCARM = ', 'SRCARM = ', 'forth-arm:', '\t$(CCARM)', '# `make forth-arm`'))]
    mk = [l for j, l in enumerate(mk) if not (l == '' and j and mk[j - 1] == '')]   # 652: its blank line once - again idempotent
    at = next(j for j, l in enumerate(mk) if l.startswith('SRC32 = '))
    mk[at + 1:at + 1] = ['CCARM = %s' % (CROSS if clang else 'cc'),
                         'SRCARM = %s' % ' '.join('srcarm/' + s for s in sorted(os.listdir(sd)))]
    at = next(j for j, l in enumerate(mk) if l.startswith('forth-libc:'))
    mk[at:at] = ['forth-arm: $(SRCARM)', '\t' + ' '.join(shlex.quote(a) if a != '$(CCARM)' else a for a in out), '']
    at = next(j for j, l in enumerate(mk) if not l.startswith('#'))
    mk[at:at] = ['# `make forth-arm` 4-byte cells for 32-bit ARM Linux (ARMv7, hard float), no C library (srcarm/rt-linux-armv7.c):'
                 + (' cross-built by clang and lld from any host - the bytes the Tegra ran.' if clang else
                    ' the ARM host\'s own GCC (CCARM=arm-linux-gnueabihf-gcc to cross-build; the Tegra measured GCC 16).')
                 + ' Run: ./forth-arm image32.img']
    mk = [l.replace('rm -f forth forth32 forth-libc', 'rm -f forth forth32 forth-arm forth-libc') for l in mk]
    open(os.path.join(d, 'Makefile'), 'w').write('\n'.join(mk))
    made.append((name, i, sha(eng), clang)); size = os.path.getsize(eng); shutil.rmtree(b, ignore_errors=True)
    print('%s (%s, %s): srcarm %d files, the engine %d bytes' % (name, i, 'clang' if clang else 'GCC', len(os.listdir(sd)), size), flush=True)
T = tempfile.mkdtemp(prefix='export-arm-check-')
shutil.copy(os.path.join(E.ROOT, 'tools', 'elf_tight.py'), os.path.join(T, 'elf_tight.py'))
if LIST: sys.exit(0)
for name, i, esha, clang in made:
    dd = os.path.join(T, name); shutil.copytree(os.path.join(OUT, name), dd)
    r = subprocess.run(['make', '-s', '-C', dd, 'forth-arm'] + (['CCARM=' + gcc] if gcc else []), capture_output=True, text=True)
    p = os.path.join(dd, 'forth-arm')
    if r.returncode == 0 and os.path.exists(p): subprocess.run(['python3', os.path.join(T, 'elf_tight.py'), p, p + '.tight'], check=True)
    same = r.returncode == 0 and os.path.exists(p + '.tight') and sha(p + '.tight') == esha
    run = None
    if r.returncode == 0:
        o = subprocess.run(([] if NATIVE else ['qemu-arm']) + [p, os.path.join(dd, 'image32.img')], input=b': SQ DUP * ; 7 SQ . BYE\n',
                           capture_output=True, timeout=60)
        run = b'49' in o.stdout
    print('  %s forth-arm: %s, %s' % (name, 'the lab\'s bytes' if same else 'DIFFERS - %s' % (r.stderr.strip()[-160:] or 'other bytes'),
          'runs (7 SQ . -> 49)' if run else 'does NOT run'), flush=True)
    bad += not (same and run)
shutil.rmtree(T, ignore_errors=True)
print('export-arm: %d designs, %s' % (len(made), 'all the lab\'s bytes and running' if not bad else '%d failed' % bad))
sys.exit(1 if bad else 0)
