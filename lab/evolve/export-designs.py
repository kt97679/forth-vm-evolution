#!/usr/bin/env python3
"""lab/evolve/export-designs.py OUT DB NAME=ID[,NAME=ID...] - designs exported so `make` alone builds them (Iteration
608; the owner: interested folks should get a working Forth by running make - the image shipped, as SOD32 shipped its
own; the engine always compiled from source). DB: records, one a line (results/final-set-chainsBCD-seed86.md).

For each design and each cell width (8, and 4 for the optional forth32), evolve.py's own build() runs, every command
recorded (as pack-designs.py); the compile command's real inputs come from the compiler itself (the same command with
-MM), and each is copied into OUT/NAME/src/ - so the directory holds exactly what the engine is built from. The compile
command is written into OUT/NAME/Makefile with every absolute path made relative and the compiler as $(CC) (default the
design's own); the image is copied as OUT/NAME/image.img (and image32.img). Then the check that makes it an export, not
a copy: in a fresh directory holding only OUT, the Makefile's own command builds each engine, which must be byte for
byte the engine the lab built and measured (exit 1 otherwise). OUT/NAME/record.json: the design's record. As the build
user, in a built and validated tree (tools/build-stages.sh, then evolve.py --validate)."""
import hashlib, json, os, re, shlex, shutil, subprocess, sys, tempfile
if len(sys.argv) != 4: sys.exit(__doc__)
OUT, DB = os.path.abspath(sys.argv[1]), sys.argv[2]
PAIRS = [p.split('=') for p in sys.argv[3].split(',')]
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
R = {json.loads(l)['id']: json.loads(l) for l in open(DB) if l.startswith('{')}
miss = [i for _, i in PAIRS if i not in R]
if miss: sys.exit('export-designs: not in %s: %s' % (DB, ', '.join(miss)))
LOG = []
_sh = E.sh
def sh(cmd, *a, **k):
    LOG.append([str(c) for c in cmd]); return _sh(cmd, *a, **k)
E.sh = sh
E.setup(); E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
CCS = ('cc', 'gcc', 'clang')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
made = []
for name, i in PAIRS:
    d = os.path.join(OUT, name); shutil.rmtree(d, ignore_errors=True); os.makedirs(os.path.join(d, 'src')); os.makedirs(os.path.join(d, 'src32'))
    json.dump(R[i], open(os.path.join(d, 'record.json'), 'w'), indent=1, sort_keys=True)
    rules = {}
    for cell in (8, 4, 'libc'):                                 # 'libc': 8-byte cells with the C library (EVOLVE_LIBC=1) - any host
        b = os.path.join(E.EV, 'export-%s-%s' % (i, cell)); shutil.rmtree(b, ignore_errors=True)
        if cell == 'libc': os.environ['EVOLVE_LIBC'] = '1'
        del LOG[:]
        ctx = E.at_width(E.WIDTH4) if cell == 4 else __import__('contextlib').nullcontext()
        with ctx: eng, img = E.build(E.canon(R[i]['genome']), b)
        os.environ.pop('EVOLVE_LIBC', None)
        cc = [c for c in LOG if os.path.basename(c[0]) in CCS and '-o' in c and c[c.index('-o') + 1] == eng]
        if len(cc) != 1: sys.exit('export-designs: %s cell %d - %d compile commands for the engine' % (i, cell, len(cc)))
        cmd = cc[0]; k = cmd.index('-o')
        dep = subprocess.run(cmd[:k] + cmd[k + 2:] + ['-MM'], cwd=b, capture_output=True, text=True)
        if dep.returncode: sys.exit('export-designs: -MM failed for %s cell %d: %s' % (i, cell, dep.stderr[-300:]))
        files = sorted({os.path.normpath(os.path.join(b, t)) for t in dep.stdout.replace('\\\n', ' ').split() if not t.endswith(':')})
        sd = {8: 'src', 4: 'src32', 'libc': 'src'}[cell]                    # each width its own: their generated headers share names
        for f in files:
            t = os.path.join(d, sd, os.path.basename(f))
            if os.path.exists(t) and sha(t) != sha(f): sys.exit('export-designs: two files named %s for %s' % (os.path.basename(f), i))
            shutil.copy(f, t)
        out = []
        for j, a in enumerate(cmd):
            if j == 0: out.append('$(CC)'); continue
            if j == k + 1: out.append({8: 'forth', 4: 'forth32', 'libc': 'forth-libc'}[cell]); continue
            if j > 0 and cmd[j - 1] in ('-I', '-iquote', '-isystem') and os.path.isdir(a): out.append(sd); continue   # every input is in sd/
            if re.match(r'^-I/', a) and os.path.isdir(a[2:]): out.append('-I' + sd); continue
            m = re.match(r'^(-[A-Za-z][^/]*?)?(/.*)$', a)
            if m and os.path.isfile(m.group(2)):
                n = os.path.basename(m.group(2)); t = os.path.join(d, sd, n)
                if not os.path.exists(t): shutil.copy(m.group(2), t)
                elif sha(t) != sha(m.group(2)): sys.exit('export-designs: two files named %s for %s' % (n, i))
                out.append((m.group(1) or '') + sd + '/' + n); continue
            if '/' in a and os.path.isabs(a.split('=')[-1]): sys.exit('export-designs: %s - an absolute path left in %r' % (i, a))
            out.append(a)
        srcs = [a for a in out if a.startswith(sd + '/')]
        rules[cell] = (os.path.basename(cmd[0]), ' '.join(shlex.quote(a) if a != '$(CC)' else a for a in out), srcs, eng)
        if cell != 'libc': shutil.copy(img, os.path.join(d, 'image.img' if cell == 8 else 'image32.img'))
        elif sha(img) != sha(os.path.join(d, 'image.img')): sys.exit('export-designs: %s - the C-library build\'s image differs' % i)
        shutil.rmtree(b, ignore_errors=True)
    srcall = sorted(os.listdir(os.path.join(d, 'src'))); src32 = sorted(os.listdir(os.path.join(d, 'src32')))
    cc8 = rules[8][0]
    mk = ['# %s - design %s of forth-vm-evolution. Generated by lab/evolve/export-designs.py; do not edit.' % (name, i),
          '# `make` builds ./forth (8-byte cells, x86-64 Linux - the build the lab measured, no C library: its own',
          '# runtime, src/rt-linux-*.c); `make forth32` the 4-byte-cell engine (needs 32-bit support: gcc-multilib);',
          '# `make forth-libc` the same design with the C library, for any other host (not the JIT designs: x86 code).',
          '# Run: ./forth image.img   (or ./forth32 image32.img). Names are upper case; BYE leaves. `make tight`: the',
          '# file exactly as measured (python3; the same loaded bytes, no section headers). Compiler and linker warnings',
          '# about attributes and an RWX segment are expected.',
          '', 'CC = %s' % cc8, 'SRC = %s' % ' '.join('src/' + s for s in srcall), 'SRC32 = %s' % ' '.join('src32/' + s for s in src32), '',
          'all: forth', '', 'forth: $(SRC)', '\t' + rules[8][1], '', 'forth32: $(SRC32)', '\t' + rules[4][1].replace('$(CC)', '$(CC32)', 1), '', 'forth-libc: $(SRC)', '\t' + rules['libc'][1], '',
          'tight: forth', '\tpython3 ../elf_tight.py forth   # optional: the file exactly as measured - no section headers or symbols', '',
          'run: forth', '\t./forth image.img', '', 'clean:', '\trm -f forth forth32 forth-libc forth.tight', '', '.PHONY: all tight run clean', '']
    mk.insert(6, 'CC32 = %s' % rules[4][0])
    open(os.path.join(d, 'Makefile'), 'w').write('\n'.join(mk))
    made.append((name, i, rules))
    print('%s (%s): src %d files, src32 %d, image %d bytes' % (name, i, len(srcall), len(src32), os.path.getsize(os.path.join(d, 'image.img'))), flush=True)
shutil.copy(os.path.join(E.ROOT if hasattr(E, 'ROOT') else os.getcwd(), 'tools', 'elf_tight.py'), os.path.join(OUT, 'elf_tight.py'))
# the check: a fresh directory holding only OUT; each engine from its Makefile, then tightened as build() does
# (tools/elf_tight.py: the loaded bytes, nothing after them) - byte for byte the lab's
bad = 0; T = tempfile.mkdtemp(prefix='export-check-'); shutil.copytree(OUT, os.path.join(T, 'designs'))
for name, i, rules in made:
    for cell, target in ((8, 'forth'), (4, 'forth32')):
        r = subprocess.run(['make', '-s', '-C', os.path.join(T, 'designs', name), target], capture_output=True, text=True)
        p = os.path.join(T, 'designs', name, target)
        lab = os.path.join(E.EV, 'export-lab-%s-%d' % (i, cell)); shutil.rmtree(lab, ignore_errors=True)
        ctx = E.at_width(E.WIDTH4) if cell == 4 else __import__('contextlib').nullcontext()
        with ctx: eng, img = E.build(E.canon(R[i]['genome']), lab)
        if False: pass
        if r.returncode == 0 and os.path.exists(p): subprocess.run(['python3', os.path.join(T, 'designs', 'elf_tight.py'), p, p + '.tight'], check=True)
        same = r.returncode == 0 and os.path.exists(p + '.tight') and sha(p + '.tight') == sha(eng)
        print('  %s %s: %s' % (name, target, 'the lab\'s bytes' if same else 'DIFFERS - %s' % (r.stderr.strip()[-200:] or 'other bytes')), flush=True)
        bad += not same; shutil.rmtree(lab, ignore_errors=True)
for name, i, rules in made:                                # the C-library build: no measured bytes to match - it must run
    if E.express(E.canon(R[i]['genome'])).get('jit'): continue
    dd = os.path.join(T, 'designs', name)
    r = subprocess.run(['make', '-s', '-C', dd, 'forth-libc'], capture_output=True, text=True)
    o = subprocess.run([os.path.join(dd, 'forth-libc'), os.path.join(dd, 'image.img')], input=b': SQ DUP * ; 7 SQ . BYE\n',
                       capture_output=True, timeout=20) if r.returncode == 0 else None
    ok = o is not None and b'49' in o.stdout
    print('  %s forth-libc: %s' % (name, 'runs (7 SQ . -> 49)' if ok else 'FAILS - %s' % (r.stderr.strip()[-200:] if r.returncode else o.stdout[-80:])), flush=True)
    bad += not ok
shutil.rmtree(T, ignore_errors=True)
sys.exit(1 if bad else 0)
