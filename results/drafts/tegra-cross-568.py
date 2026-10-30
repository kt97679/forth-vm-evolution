#!/usr/bin/env python3
"""results/drafts/tegra-cross-568.py - can the laptop build the Tegra's clang designs? (Iteration 568)

Seed 81's fastest front design that rage could measure with clang - no JIT, not cpt16 - built twice by evolve.py's own
build: as a 32-bit x86 engine (4-byte cells, the laptop's widths build) and cross-built for ARMv7 by clang
(--target=arm-linux-gnueabihf, linked by lld against Ubuntu's armhf C library, static - the runtime evolve.py uses on
ARM hosts); the ARM engine run under qemu-arm, not under evolve.py's process limit (qemu starts a thread). Needs
`CROSS=1 sh tools/setup-sandbox.sh` (lld, qemu-user, libc6-dev-armhf-cross, libgcc-13-dev-armhf-cross) and a seed-81
db.jsonl as its argument. Iteration 568: corpus, fib and apps IDENTICAL; the two images identical; the ARM engine
347,688 bytes (static glibc) against 12,916 (x86, no C library).
"""
import json, os, shutil, subprocess, sys
db = sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
front = {json.loads(l)['id'] for l in open(os.path.join(ROOT, 'results', 'evolve-amd-ryzen-7-pro-8840hs-seed81.md')) if l.startswith('{"bin"')}
R = [json.loads(l) for l in open(db) if l.startswith('{')]
pick = min((r for r in R if r['id'] in front and r.get('speed') and r.get('speed32') and r['genome'].get('compiler')
            and not r['genome'].get('jit') and r['genome'].get('enc') != 'cpt16'), key=lambda r: r['speed'])
g = E.canon(pick['genome']); print('design', pick['id'], 'speed %.3f' % pick['speed'])
E.setup(); E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
with E.at_width(E.WIDTH4):
    dx = os.path.join(E.EV, 'cross-x86-32'); shutil.rmtree(dx, ignore_errors=True); ex, ix = E.build(g, dx); px = E.private_work(dx)
    E.ARM32 = True; E.rt = lambda: ['-fno-asynchronous-unwind-tables']
    E.CCV = lambda g: ['clang', '--target=arm-linux-gnueabihf', '-march=armv7-a', '-static', '-fuse-ld=lld']
    da = os.path.join(E.EV, 'cross-arm'); shutil.rmtree(da, ignore_errors=True); ea, ia = E.build(g, da); pa = E.private_work(da)
    for w in ('corpus', 'fib', 'apps'):
        inp = E.program(w)
        rx = subprocess.run([ex, ix], input=inp, capture_output=True, cwd=px, timeout=280)
        ra = subprocess.run(['qemu-arm', ea, ia], input=inp, capture_output=True, cwd=pa, timeout=280)
        print('%-7s x86 exit %d, ARM exit %d - %s' % (w, rx.returncode, ra.returncode, 'IDENTICAL' if ra.stdout == rx.stdout else 'DIFFER'))
print('images identical: %s; engines: x86 %d, ARM %d bytes' % (open(ia, 'rb').read() == open(ix, 'rb').read(), os.path.getsize(ex), os.path.getsize(ea)))
