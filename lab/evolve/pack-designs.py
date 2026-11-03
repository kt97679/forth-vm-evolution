#!/usr/bin/env python3
"""lab/evolve/pack-designs.py OUT DB ID[,ID...] - designs packed for another project (Iteration 601: the handoff to
relf, RELF.md). DB: a file of records, one a line (results/final-set-chainsBCD-seed86.md). For each design and each
cell width (8 and 4 bytes), built by evolve.py's own build() - the bytes the lab measured - into OUT/ID/cell8, cell4:
  engine, image.img   the stripped engine and its image: `./engine image.img < program` (names in upper case);
  src/                the engine's C source as compiled (vm.c, a copy of engine/vm-lab.c or vm-lab-tos.c, and every file
                      generated beside it - fused pairs, superinstructions, the JIT's tables);
  build.txt           every command build() ran, in order, as run - the generators, the compiler line, layout.py;
  check.txt           each workload (the nine the lab measures: kernel fib corpus loop bubble ackermann apps sieve parse)
                      run on this engine and on the hand-made s6-cv8b at the same width: right, WRONG or DIES.
OUT/ID/record.json: the design's record (its genome, expression, the lab's numbers). OUT/SHA256SUMS: every engine and
image. Prints one line a design and width; exit 1 when any check is not right. As the build user, in a built tree
(tools/build-stages.sh, then evolve.py --validate). About a minute a design and width, the s6 references once."""
import json, os, shutil, subprocess, sys, hashlib
if len(sys.argv) != 4: sys.exit(__doc__)
OUT, DB, IDS = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3].split(',')
WORK = ('kernel', 'fib', 'corpus', 'loop', 'bubble', 'ackermann', 'apps', 'sieve', 'parse')
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import evolve as E
R = {}
for l in open(DB):
    if l.startswith('{'): r = json.loads(l); R[r['id']] = r
miss = [i for i in IDS if i not in R]
if miss: sys.exit('pack-designs: not in %s: %s' % (DB, ', '.join(miss)))
LOG = []
_sh = E.sh
def sh(cmd, *a, **k):                                   # every command build() runs, recorded
    LOG.append(' '.join(str(c) for c in cmd)); return _sh(cmd, *a, **k)
E.sh = sh
E.setup(); E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
def run(eng, img, pw, inp):
    try: r = _sh([eng, img], inp=inp, cwd=pw, timeout=300, cpu=120)
    except Exception as x: return None, [], 'timeout (%s)' % str(x)[:60]
    return r.returncode, r.stdout.decode('latin-1').replace('\r', '').split('\n'), r.stderr.decode('latin-1').strip()[-160:]
os.makedirs(OUT, exist_ok=True); bad = 0; sums = []
ref = {}
for cell in (8, 4):
    ctx = E.at_width(E.WIDTH4) if cell == 4 else __import__('contextlib').nullcontext()
    with ctx:
        if cell == 4:
            dr = os.path.join(E.EV, 'pack-ref4'); shutil.rmtree(dr, ignore_errors=True); ref[cell] = E.build(E.canon(dict(E.HUMAN['s6-cv8b'])), dr) + (E.private_work(dr),)
        else: dr = os.path.join(E.EV, 'pack-ref8'); shutil.rmtree(dr, ignore_errors=True); ref[cell] = (E.REF[0], E.REF[1], E.private_work(dr))
        for i in IDS:
            d = os.path.join(OUT, i, 'cell%d' % cell); b = os.path.join(E.EV, 'pack-%s-%d' % (i, cell))
            shutil.rmtree(d, ignore_errors=True); shutil.rmtree(b, ignore_errors=True); os.makedirs(os.path.join(d, 'src'))
            json.dump(R[i], open(os.path.join(OUT, i, 'record.json'), 'w'), indent=1, sort_keys=True)
            del LOG[:]
            try: eng, img = E.build(E.canon(R[i]['genome']), b)
            except Exception as x: print('%s cell%d: the build DIED - %s' % (i, cell, str(x)[:160])); bad += 1; continue
            shutil.copy(eng, os.path.join(d, 'engine')); shutil.copy(img, os.path.join(d, 'image.img'))
            for f in sorted(os.listdir(b)):
                p = os.path.join(b, f)
                if os.path.isfile(p) and f.endswith(('.c', '.h', '.json', '.S', '.s')): shutil.copy(p, os.path.join(d, 'src', f))
            open(os.path.join(d, 'build.txt'), 'w').write('# %s at %d-byte cells: build()\'s commands, in order, as run (build dir %s)\n' % (i, cell, b)
                                                          + '\n'.join(LOG) + '\n')
            pw = E.private_work(b); re_, ri, rw = ref[cell]; lines = []
            for w in WORK:
                inp = E.program(w); (c0, o0, _), (c1, o1, e1) = run(re_, ri, rw, inp), run(eng, img, pw, inp)
                if c1 == c0 and o1 == o0: lines.append('%-10s right' % w); continue
                bad += 1
                lines.append('%-10s %s' % (w, 'DIES - exit %s (s6 %s) %s' % (c1, c0, e1) if c1 != c0 else 'WRONG'))
            open(os.path.join(d, 'check.txt'), 'w').write('# %s at %d-byte cells against s6-cv8b at the same width, the lab\'s inputs\n' % (i, cell) + '\n'.join(lines) + '\n')
            for f in ('engine', 'image.img'):
                p = os.path.join(d, f); sums.append('%s  %s' % (hashlib.sha256(open(p, 'rb').read()).hexdigest(), os.path.relpath(p, OUT)))
            print('%s cell%d: engine %d + image %d = %d bytes; %d of %d right' % (i, cell, os.path.getsize(os.path.join(d, 'engine')),
                  os.path.getsize(os.path.join(d, 'image.img')), os.path.getsize(os.path.join(d, 'engine')) + os.path.getsize(os.path.join(d, 'image.img')),
                  sum(l.endswith('right') for l in lines), len(WORK)), flush=True)
            shutil.rmtree(b, ignore_errors=True)
for c in (8, 4): shutil.rmtree(os.path.join(E.EV, 'pack-ref%d' % c), ignore_errors=True)
open(os.path.join(OUT, 'SHA256SUMS'), 'w').write('\n'.join(sums) + '\n')
sys.exit(1 if bad else 0)
