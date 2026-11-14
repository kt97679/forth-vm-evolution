#!/usr/bin/env python3
"""lab/evolve/genapps-dispatch.py [--designs A,B] [--apps A,B] - genapps.py's programs counted in dispatches, on
interpreted designs and on relf's CV8 (Iteration 674): machine-independent, where the times are not.

A design: its Makefile's forth-libc engine with -DPROFILE=1 (the lab's per-address and per-pair counts, VMPROF);
dispatches are its per-address counts ("I" lines), calls the pseudo-operation 256 (counted there once - relf's
Iteration 944 correction), DOVAR and DODOES their operations' counts (69 and 70: CV8's numbering, which the
portable designs keep). relf: a counting engine made from vendor/relf/cv8.c as relf's tools/profile.py makes it
(every dispatch counted by its address). Each program's benchmark: its full run less its load - genapps.py's
drivers, in build/genapps/work-8 (run genapps.py first). Only the designs without a JIT: native code dispatches
nothing. Prints a Markdown table."""
import argparse, os, re, subprocess, sys
HERE_ = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE_))
ap = argparse.ArgumentParser(usage=__doc__.split('\n')[0])
ap.add_argument('--designs', default='smallest,least-memory,portable-small,portable-knee,portable-arm,portable-fastest')
ap.add_argument('--apps', default='sim16,gc16,scan,evo,wordfreq,minif,brainless')
a = ap.parse_args()
W = os.path.join(ROOT, 'build', 'genapps', 'work-8'); P = os.path.join(ROOT, 'build', 'genapps', 'prof')
if not os.path.isdir(W): sys.exit('genapps-dispatch: run genapps.py first (no %s)' % W)
os.makedirs(P, exist_ok=True)
def patch(text, old, new):
    if text.count(old) != 1: sys.exit('genapps-dispatch: the text to patch occurs %d times:\n%s' % (text.count(old), old))
    return text.replace(old, new)
# relf's counting engine (tools/profile.py's patch)
SLOTS = 1 << 18; counts = os.path.join(P, 'counts.bin'); reng = os.path.join(P, 'relf-prof')
src = open(os.path.join(ROOT, 'vendor', 'relf', 'cv8.c')).read()
src = patch(src, '#define PROF(k)\n#define PROFIP(a)\n#define PROFDUMP', '#include <sys/mman.h>\nstatic unsigned int *prof_map;\n'
            'static UNS64 prof_base;\n#define PROF(k)\n#define PROFIP(a) (prof_map[((a) - prof_base) & 0x3FFFF]++)\n#define PROFDUMP')
src = patch(src, '    NEXT();\ndo_call:', '    prof_base = cbase;\n    { int fd = open("%s", O_RDWR);\n      prof_map = mmap(0, %d * '
            'sizeof(unsigned int), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);\n      close(fd); }\n    NEXT();\ndo_call:' % (counts, SLOTS))
open(os.path.join(P, 'relf-prof.c'), 'w').write(src)
subprocess.run(['cc', '-O2', '-I', os.path.join(ROOT, 'vendor', 'relf'), '-o', reng, os.path.join(P, 'relf-prof.c')], check=True)
rimg = os.path.join(W, 'relf-tree', 'forth', 'kernel64.img')
def relf_count(name):
    open(counts, 'wb').write(bytes(SLOTS * 4))
    subprocess.run([reng, rimg], cwd=W, input=('S" %s" INCLUDED\n' % name).encode(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    b = open(counts, 'rb').read()
    return sum(int.from_bytes(b[i:i + 4], 'little') for i in range(0, len(b), 4))
# the designs' counting engines
def design_engine(d):
    mk = open(os.path.join(ROOT, 'designs', d, 'Makefile')).read()
    m = re.search(r'^forth-libc: .*\n\t(.*)$', mk, re.M)
    if not m: sys.exit('genapps-dispatch: no forth-libc rule in designs/%s/Makefile' % d)
    cc = re.search(r'^CC\s*[:?]?=\s*(\S+)', mk, re.M)       # the design's own compiler (cc: gcc, for three of them)
    cmd = m.group(1).replace('$(CC)', cc.group(1) if cc else 'cc').replace('-o forth-libc', '-DPROFILE=1 -o ' + os.path.join(P, d + '-prof'))
    subprocess.run(cmd, shell=True, cwd=os.path.join(ROOT, 'designs', d), check=True)
    return os.path.join(P, d + '-prof')
def design_count(eng, img, name):
    f = os.path.join(P, 'vmprof.txt')
    if os.path.exists(f): os.remove(f)
    subprocess.run([eng, img], cwd=W, input=('S" %s" INCLUDED\n' % name).encode(), stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, env=dict(os.environ, VMPROF=f))
    tot = calls = dovar = dodoes = 0
    for l in open(f):
        p = l.split()
        if p[0] == 'I': tot += int(p[2])
        elif p[0].isdigit():
            j, n = int(p[1]), int(p[2])
            if j == 256: calls += n
            elif j == 69: dovar += n
            elif j == 70: dodoes += n
    return tot, calls, dovar, dodoes
apps = a.apps.split(','); designs = a.designs.split(',')
rows = {}
for app in apps:
    rf = relf_count('relf-%s-full.fs' % app) - relf_count('relf-%s-load.fs' % app)
    rows[app] = {'relf64': rf}
for d in designs:
    eng = design_engine(d); img = os.path.join(ROOT, 'designs', d, 'image.img')
    for app in apps:
        f = design_count(eng, img, 'lab-%s-full.fs' % app); l = design_count(eng, img, 'lab-%s-load.fs' % app)
        rows[app][d] = tuple(x - y for x, y in zip(f, l))
    print('genapps-dispatch: %s counted' % d, file=sys.stderr, flush=True)
print('| program | relf64 | ' + ' | '.join(designs) + ' |'); print('|---|---:|' + '---:|' * len(designs))
for app in apps:
    r = rows[app]['relf64']
    print('| %s | {:,} | '.format(r) % app + ' | '.join('{:,} ({:.2f})'.format(rows[app][d][0], rows[app][d][0] / r) for d in designs) + ' |')
print('\nOn the designs, the share of calls, DOVAR and DODOES in those dispatches:\n')
print('| program | ' + ' | '.join(designs) + ' |'); print('|---|' + '---:|' * len(designs))
for app in apps:
    print('| %s | ' % app + ' | '.join('%.1f / %.1f / %.1f %%' % tuple(100 * x / rows[app][d][0] for x in rows[app][d][1:]) for d in designs) + ' |')
