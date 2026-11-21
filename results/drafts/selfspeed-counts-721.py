#!/usr/bin/env python3
"""results/drafts/selfspeed-counts-721.py [NAME ...] - a self-built role against its translator's build by instruction
count (Iteration 721): the VM's 2-round selfhost-speed.py read small-jit's 4-byte self-built image 7-9 % slower on both
alternations; timing here is noise, a count is not. For each design (default small-jit and smallest, a JIT-free control),
at 8- and 4-byte cells: designs/NAME's engine and self-built image, and the lab's build of its record (evolve.build: the
translator's), each workload of the selection run once under cachegrind (instructions retired, the JIT's code included -
--smc-check=all) in the design's own work directory. Prints Ir per workload and self / translator. Run from the top."""
import json, os, re, shutil, subprocess, sys
HERE = os.path.join(os.getcwd(), 'lab', 'evolve'); D = os.path.join(os.getcwd(), 'designs')
names = sys.argv[1:] or ['small-jit', 'smallest']
sys.argv = ['x']; sys.path.insert(0, HERE)
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.setup()
def ir(eng, img, pw, w, legacy=False):
    # 4-byte cells: the engine re-execs itself into Linux's legacy layout unless it is set already (vm-lab.c, Iteration 326)
    # - under valgrind /proc/self/exe is the tool, so the layout is set first (setarch -L) and no re-exec happens
    p = subprocess.run((['setarch', 'x86_64', '-L'] if legacy else []) + ['valgrind', '--tool=cachegrind', '--cache-sim=no', '--smc-check=all', '--trace-children=yes',
                        '--cachegrind-out-file=/dev/null', eng, img], input=E.program(w), cwd=pw,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=1800)
    n = [int(x.replace(b',', b'')) for x in re.findall(rb'I\s+refs:\s+([\d,]+)', p.stderr)]
    return sum(n) if n else None
print('# Self-built against the translator\'s build, instructions (results/drafts/selfspeed-counts-721.py)\n')
for n in names:
    rec = json.load(open(os.path.join(D, n, 'record.json')))
    for w, eng, img in (('8', 'forth', 'image.img'), ('4', 'forth32', 'image32.img')):
        d = os.path.join(E.EV, 'selfcount-%s-%s' % (n, w)); shutil.rmtree(d, ignore_errors=True)
        g = dict(rec['genome'])
        if w == '4' and (g.get('scale') or 0) > 2: g['scale'] = 2
        ctx = E.at_width(E.WIDTH4) if w == '4' else None
        if ctx: ctx.__enter__()
        try:
            et, it = E.build(E.canon(g), d); pw = E.private_work(d)
            es, is_ = os.path.join(D, n, eng), os.path.join(D, n, img)
            print('%s (%s), %s-byte cells - engines %d / %d B, images %d / %d B (self / translator)'
                  % (n, rec['id'], w, os.path.getsize(es), os.path.getsize(et), os.path.getsize(is_), os.path.getsize(it)))
            tot = [0, 0]
            for wl in E.WORK_SEL:
                a, b = ir(es, is_, pw, wl, w == '4'), ir(et, it, pw, wl, w == '4')
                if a and b: tot[0] += a; tot[1] += b
                print('  %-10s self %14s  translator %14s  %s' % (wl, '{:,}'.format(a) if a else '-', '{:,}'.format(b) if b else '-',
                      '%.4f' % (a / b) if a and b else '-'), flush=True)
            print('  %-10s self %14s  translator %14s  %.4f\n' % ('all', '{:,}'.format(tot[0]), '{:,}'.format(tot[1]), tot[0] / tot[1] if tot[1] else 0), flush=True)
        finally:
            if ctx: ctx.__exit__(None, None, None)
            shutil.rmtree(d, ignore_errors=True)
