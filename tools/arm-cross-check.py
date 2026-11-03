#!/usr/bin/env python3
"""tools/arm-cross-check.py RESULTS.md [--n K] [--ids ID,...] [--gcc CC] - the ARM engines checked (Iterations 570-571).

Each design built by evolve.py's own build at 4-byte cells, without the C library (engine/rt-linux-armv7.c), must pass
evolve.alive - the corpus, the kernel, far, full - and give the reference's output on fib and apps: the hand-made s6
as tools/build-stages.sh builds it here with the C library (build/s6-cv8b-32 - the stage engine, the way ARM engines
were built until Iteration 570; a correct design's output is every design's). A line a design, then the totals: built,
alive, identical, the engines' sizes; exit 0 only if every design passed.

  on x86-64, no --gcc: the designs the laptop sends the Tegra (cv8, clang, no JIT, from RESULTS.md's {"bin" lines),
      cross-built (EVOLVE_TARGET=armv7: clang, lld) and run under qemu-arm - outside evolve.py's jail (qemu starts a
      thread), so only designs the laptop already ran. Iteration 570: 40 of seed 82's 193, all passed, 6-16 KB.
  on x86-64, --gcc CC (the Tegra's side, simulated - CC arm-linux-gnueabihf-gcc, which removes gcc-multilib): the
      hand-made stages (cell, sod16, cpt16, cv8: relf.c and build_other) and RESULTS.md's GCC designs without the JIT,
      built as on an ARM host (evolve.ARM32), under qemu-arm.
  on the Tegra (an ARM host; Iteration 571 - tools/rage-check.sh runs it there): the same designs as --gcc, built by
      the host's cc as its check builds them, run natively - GCC 16 and the runtime's start (the legacy-layout
      re-exec, which qemu never takes) on the real machine before its check of the confirmation front.

--n K: K of the designs spread evenly by speed, the fastest and the slowest among them. The hand-made stages s3-s5 do
not convert at 4-byte cells and s2-cpt16 runs out of reach on apps, at either width's build (570) - known, listed apart.
Needs, on x86-64, `CROSS=1 sh tools/setup-sandbox.sh` (lld, qemu-user, libc6-dev-armhf-cross, libgcc-13-dev-armhf-cross).
"""
import json, os, shutil, subprocess, sys
A = sys.argv[1:]
def opt(name, default=None):
    if name not in A: return default
    i = A.index(name); v = A[i + 1]; del A[i:i + 2]; return v
n = int(opt('--n', '0')); ids = [x for x in (opt('--ids') or '').split(',') if x]; gcc = opt('--gcc')
if len(A) != 1: sys.exit(__doc__)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NATIVE = os.uname().machine.startswith('arm')          # the Tegra itself: its cc, no qemu
if NATIVE and gcc: sys.exit('arm-cross-check: --gcc is the Tegra simulated on x86-64; here the host\'s cc builds')
KNOWN = {'s2-cpt16': 'out of reach on apps (scale 1)', 's3-cpt16f': 'not converted at 4-byte cells',
         's4-cv8': 'frozen - not built from source (varcall 0, 592; bytehdr 0, 594)',
         's5-cv8spec': 'frozen - not built from source (doesfar 0, 593; bytehdr 0, 594)'}
os.environ['EVOLVE_CELL'] = '4'
if gcc: os.environ['EVOLVE_CC'] = gcc
elif not NATIVE: os.environ.setdefault('EVOLVE_CC', 'gcc -m32 -fno-pie -no-pie')
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
if gcc: E.ARM32 = True                                 # as on the Tegra: ccflags drops alignhot, rt() is ARM's
E.setup()

_sh = E.sh
def qsh(cmd, cwd=None, inp=None, timeout=300, env=None, cpu=60):
    """evolve.sh; on x86-64 an ARM engine under qemu-arm, outside the jail - its wall-clock limit 4x."""
    if not NATIVE and cmd and str(cmd[0]).endswith('/engine') and '/arm-' in str(cmd[0]):
        return subprocess.run(['qemu-arm'] + list(cmd), cwd=cwd, input=inp, capture_output=True, timeout=4 * timeout)
    return _sh(cmd, cwd=cwd, inp=inp, timeout=timeout, env=env, cpu=cpu)
E.sh = qsh

rd = os.path.join(E.EV, 'arm-ref'); shutil.rmtree(rd, ignore_errors=True); os.makedirs(rd); rp = E.private_work(rd)
ref = {w: E.sh([os.path.join(E.O, 's6-cv8b-32'), os.path.join(E.O, 's6-cv8b-s32.img')], cwd=rp, inp=E.program(w), timeout=120, cpu=30).stdout
       for w in ('fib', 'apps')}
shutil.rmtree(rd, ignore_errors=True)
recs = [json.loads(l) for l in open(A[0]) if l.startswith('{"bin"')]
ex = lambda r: E.express(E.canon(r['genome']))
if gcc or NATIVE:
    pick = [{'id': k, 'genome': v, 'speed': 0} for k, v in sorted(E.HUMAN.items()) if not ex({'genome': v}).get('jit')] + [
            r for r in recs if not ex(r).get('compiler') and not ex(r).get('jit')]
else:
    pick = [r for r in recs if r['genome'].get('enc', 'cv8') == 'cv8' and ex(r).get('compiler') and not ex(r).get('jit')]
pick.sort(key=lambda r: r.get('speed') or 0)
if ids: pick = [r for r in pick if r['id'] in ids]
if n and len(pick) > n: pick = [pick[int(j * (len(pick) - 1) / max(1, n - 1))] for j in range(n)]
how = 'the host\'s cc, natively' if NATIVE else 'GCC, by %s, under qemu-arm' % gcc if gcc else 'cv8, clang, no JIT, under qemu-arm'
print('arm-cross-check: %d designs of %d (%s); the reference build/s6-cv8b-32 (the C library)' % (len(pick), len(recs), how), flush=True)
tot = dict(built=0, alive=0, same=0); sizes = []; known = []
for k, r in enumerate(pick, 1):
    g = E.canon(r['genome']); i = r['id']; da = os.path.join(E.EV, 'arm-' + i)
    if not gcc and not NATIVE: os.environ['EVOLVE_TARGET'] = 'armv7'
    try: ea, ia = E.build(g, da)
    except Exception as ex_:
        if i in KNOWN: known.append(i); print('%3d %s - %s (known)' % (k, i, KNOWN[i]), flush=True); continue
        print('%3d %s ARM build: %s' % (k, i, str(ex_)[:100]), flush=True); continue
    finally: os.environ.pop('EVOLVE_TARGET', None)
    tot['built'] += 1; pa = E.private_work(da); sizes.append(os.path.getsize(ea))
    try: E.alive(ea, ia, pa); tot['alive'] += 1; v = 'alive'
    except Exception as ex_: v = 'DEAD (%s)' % str(ex_)[:60]
    same = [w for w in ('fib', 'apps') if E.sh([ea, ia], cwd=pa, inp=E.program(w), timeout=120).stdout == ref[w]]
    if len(same) < 2 and i in KNOWN and v == 'alive': known.append(i); tot['built'] -= 1; tot['alive'] -= 1; sizes.pop()
    else: tot['same'] += len(same) == 2
    print('%3d %s %-5s speed %.3f: ARM %d bytes, %s, fib+apps %s' % (k, i, g['enc'], r.get('speed') or 0, os.path.getsize(ea), v,
          'IDENTICAL' if len(same) == 2 else ('DIFFER (%s same)' % (','.join(same) or 'none')) + (' - known: %s' % KNOWN[i] if i in KNOWN else '')), flush=True)
    shutil.rmtree(da, ignore_errors=True)
m = len(pick) - len(known)
print('arm-cross-check: %d built for ARM, %d alive, %d identical on fib and apps, of %d%s; ARM engines %s bytes' % (
    tot['built'], tot['alive'], tot['same'], m, ' (and %d known: %s)' % (len(known), ', '.join(known)) if known else '',
    '%d-%d' % (min(sizes), max(sizes)) if sizes else '-'), flush=True)
sys.exit(0 if m and tot['built'] == tot['alive'] == tot['same'] == m else 1)
