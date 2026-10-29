#!/usr/bin/env python3
"""results/drafts/jitscan-test-567.py [8|4] - the after-seed-81 batch's JIT designs built and run (Iteration 567): the minimal
design (the newest regression), engines-check's "the JIT with jitexec, aligned to 64" and the older regressions - each on
the corpus, jit-diff.fth (as engines-check runs it) and sim16's line (the apps workload's), against s6. From a built
tree with the batch applied. 567: at JIT_SCAN_MAX 512 all right at 8- and 4-byte cells; with 160 put back by hand, the
first two wrong on jit-diff and sim16, the corpus right.
"""
import os, sys, json, shutil, contextlib
T = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); W = int(sys.argv[1]) if len(sys.argv) > 1 else 8; sys.argv = ['x']; sys.path.insert(0, T + '/lab/evolve'); import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths(); E.TWO_WIDTHS[0] = False
S6 = dict(E.HUMAN['s6-cv8b']); JIT = dict(tag2=1, jit=1, jitx=1, jitloop=1, jitinl=1, jittail=1)
_JD = T + '/tests/jit'
JDIFF = (open(_JD + '/jit-diff.fth', 'rb').read() + open(_JD + '/jit-ops.fth', 'rb').read()).replace(b'\nBYE\n', b'\n') \
    + b''.join(open(T + '/forth/' + f, 'rb').read() + b'\n' for f in ('extend.4', 'coreext.4')) + open(_JD + '/jit-marker.fth', 'rb').read()
SIM = open(T + '/lab/evolve/apps/sim16.fth', 'rb').read() + b'\n700 ORG 15 LIT, FIB CALL, HALT,  0 STEPS !  700 RUN DPOP . STEPS @ . CR\nBYE\n'
def out(eng, img, pw, inp): r = E.sh([eng, img], inp=inp, timeout=120, cpu=60, cwd=pw); return r.stdout.decode('latin-1').replace('\r', '').split('\n')
regs = json.load(open(T + '/lab/evolve/regressions.json'))
CASES = [('minimal (regression %s)' % regs[-1]['id'], regs[-1]['genome']), ('variant: JIT, jitexec, aligned to 64', E.canon(dict(S6, **dict(JIT, jitexec=1, alignhot=3))))] \
      + [('regression %s' % r['id'], r['genome']) for r in regs[:-1]]
with (E.at_width(E.WIDTH4) if W == 4 else contextlib.nullcontext()):
    dr = os.path.join(E.EV, 'vt-ref'); shutil.rmtree(dr, ignore_errors=True)
    er, ir = E.build(E.canon(dict(S6)), dr); pr = E.private_work(dr); RJ = out(er, ir, pr, JDIFF); RS = out(er, ir, pr, SIM)
    for name, g in CASES:
        d = os.path.join(E.EV, 'vt'); shutil.rmtree(d, ignore_errors=True)
        try:
            eng, img = E.build(E.canon(g), d); pw = E.private_work(d)
            try: E.alive(eng, img, pw); c = 'right'
            except Exception as x: c = 'DIES ' + str(x)[:40]
            j = 'right' if out(eng, img, pw, JDIFF) == RJ else 'WRONG'; s = 'right' if out(eng, img, pw, SIM) == RS else 'WRONG'
            print('%d-byte cells, %-40s corpus %s, jit-diff %s, sim16 %s' % (W, name, c, j, s), flush=True)
        except Exception as x: print('%d-byte cells, %-40s DIED %s' % (W, name, str(x)[:90]), flush=True)
