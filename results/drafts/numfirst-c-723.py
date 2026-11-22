#!/usr/bin/env python3
"""results/drafts/numfirst-c-723.py [NAME ...] - numfirst's C form priced (Iteration 723, after
results/drafts/numfirst-722.md: where FIND is the C (FIND), klookup, the Forth digit test costs more dispatches than the
lookup it skips). The C form: (FIND) answers c-addr 0 at once for a token of the form -?[0-9]+ - what its walk would
answer while no name of that form is defined (the flag the header word would keep, assumed clear: none of the workloads
defines one, and the outputs are compared) - and INTERPRET's NUMBER? converts it as before, so BASE does not enter. Built
by wrapping evolve.sh in a process of its own: the engine's copy (vm.c) patched at L_x_find under #if NUMFIRST_C and
compiled with -DNUMFIRST_C=1, the image the same. For each design of designs/ with klookup (its (FIND); default all such):
the lab's build of its record and the C form's, each workload (kernel, corpus, parse - held out - apps) under cachegrind
(instructions) and on each build's profiling engine (dispatches - the same by construction, checked), outputs compared.
8-byte cells. Run from the top as the build user; about fifteen minutes."""
import json, os, re, shutil, subprocess, sys
ROOT = os.getcwd(); HERE = os.path.join(ROOT, 'lab', 'evolve'); DS = os.path.join(ROOT, 'designs')
PHASE = os.environ.get('NF_PHASE')
OUT = os.path.join(ROOT, 'build', 'numfirst-c'); os.makedirs(OUT, exist_ok=True)
WORK = ['kernel', 'corpus', 'parse', 'apps']
AT = re.compile(r'(L_x_find: \{ UNS64 n_ = [^;]*, c_ = [^;]*, r_ = 0;)')   # vm-lab.c's and gen-tos.py's (tos)
PATCH = ('\n#if NUMFIRST_C\n'
         '            { UNS64 e_ = c_ + 1 + BYTE(c_), q_ = c_ + 1; if (q_ < e_ && BYTE(q_) == 45) q_++;   /* numfirst: -?[0-9]+ */\n'
         '              if (q_ < e_) { while (q_ < e_ && (UNS8)(BYTE(q_) - 48) < 10) q_++; if (q_ == e_) n_ = 0; } }\n'
         '#endif\n')

if PHASE:
    names = sys.argv[1:]; sys.argv = ['x']; sys.path.insert(0, HERE)
    import evolve as E
    E.setup()
    if PHASE == 'cform':
        orig = E.sh
        def sh(cmd, *a, **kw):
            src = [x for x in cmd if isinstance(x, str) and x.endswith(os.sep + 'vm.c')] if isinstance(cmd, list) else []
            if src and '-o' in cmd:
                t = open(src[0]).read()
                if PATCH not in t:
                    t, k = AT.subn(lambda m: m.group(1) + PATCH, t, count=1)
                    if k != 1: raise RuntimeError('numfirst-c: no L_x_find to patch in ' + src[0])
                    open(src[0], 'w').write(t)
                cmd = cmd + ['-DNUMFIRST_C=1']
            return orig(cmd, *a, **kw)
        E.sh = sh
    res = {}
    for n in names:
        rec = json.load(open(os.path.join(DS, n, 'record.json'))); g = E.canon(dict(rec['genome']))
        d = os.path.join(E.EV, 'numfirst-c-%s-%s' % (PHASE, n)); shutil.rmtree(d, ignore_errors=True)
        et, it = E.build(g, d)
        E.PROFILING[0] = 1; pe, pi = E.build(g, d + '-prof'); E.PROFILING[0] = 0
        res[n] = {'eng': et, 'img': it, 'peng': pe, 'pimg': pi, 'work': E.private_work(d), 'id': rec['id'],
                  'prog': {w: E.program(w).decode('latin-1') for w in WORK}}
    json.dump(res, open(os.path.join(OUT, PHASE + '.json'), 'w'))
    sys.exit(0)

names = sys.argv[1:] or sorted(n for n in os.listdir(DS) if os.path.exists(os.path.join(DS, n, 'record.json'))
                               and json.load(open(os.path.join(DS, n, 'record.json')))['genome'].get('klookup'))
for ph in ('base', 'cform'):
    subprocess.run([sys.executable, os.path.abspath(__file__)] + names, env=dict(os.environ, NF_PHASE=ph), check=True,
                   stdout=subprocess.DEVNULL)
B, C = (json.load(open(os.path.join(OUT, ph + '.json'))) for ph in ('base', 'cform'))

def dispatches(eng, img, prog, cwd):
    f = os.path.join(OUT, 'vmprof.txt')
    if os.path.exists(f): os.remove(f)
    p = subprocess.run([eng, img], cwd=cwd, input=prog.encode('latin-1'), capture_output=True, timeout=600,
                       env=dict(os.environ, VMPROF=f))
    return sum(int(l.split()[2]) for l in open(f) if l.startswith('I ')), p.stdout
def ir(eng, img, prog, cwd):
    p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null', eng, img],
                       input=prog.encode('latin-1'), cwd=cwd, capture_output=True, timeout=1800)
    n = re.findall(rb'I\s+refs:\s+([\d,]+)', p.stderr)
    return (int(n[-1].replace(b',', b'')) if n else 0), p.stdout

print('# numfirst\'s C form: instructions and dispatches, C form / base (results/drafts/numfirst-c-723.py)\n')
bad = 0
for n in names:
    b, c = B[n], C[n]
    print('%s (%s), 8-byte cells - engines %d / %d B, images %d / %d B (C form / base)' % (
        n, b['id'], os.path.getsize(c['eng']), os.path.getsize(b['eng']), os.path.getsize(c['img']), os.path.getsize(b['img'])))
    for w in WORK:
        db, _ = dispatches(b['peng'], b['pimg'], b['prog'][w], b['work'])
        dc, _ = dispatches(c['peng'], c['pimg'], b['prog'][w], b['work'])
        (ib, ob), (ic, oc) = ir(b['eng'], b['img'], b['prog'][w], b['work']), ir(c['eng'], c['img'], b['prog'][w], b['work'])
        bad += ob != oc
        print('  %-7s instructions %14s -> %14s  %.4f   dispatches %.4f   output %s' % (
            w, '{:,}'.format(ib), '{:,}'.format(ic), ic / ib if ib else 0, dc / db if db else 0, 'same' if ob == oc else 'DIFFERS'),
              flush=True)
    print()
print('numfirst-c: %s' % ('FAIL - an output differs' if bad else 'every output the same'))
