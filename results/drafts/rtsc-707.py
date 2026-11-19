#!/usr/bin/env python3
"""results/drafts/rtsc-707.py TREE LIST N OUT - the rtsc patch's check (Iteration 707): N designs of LIST (the 8 smallest
first - the bytes matter most there - then spread by speed with tos, GCC and clang, the JIT among them) built by TREE's
evolve.py at the width of EVOLVE_CELL (with EVOLVE_CC as arm-cross-check.py sets it for 32-bit x86), each: its binary's
bytes, evolve.alive (the corpus, the kernel, far, full), and fib and apps against TREE's s6 at that width. OUT: a line a
design. Run on master and on the patched tree, then compare: the bytes saved, nothing else changed. As the build user."""
import json, os, re, sys

tree, lst, n, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab', 'evolve'))
import evolve as E
E.TWO_WIDTHS[0] = True; E.setup_widths()
recs = [json.loads(l) for l in open(lst) if l.startswith('{"') and '"genome": {' in l]
small = sorted(recs, key=lambda r: r.get('total') or 1e9)[:8]
rest = sorted((r for r in recs if r not in small), key=lambda r: r.get('speed') or 9)
pick = small + rest[::max(1, len(rest) // max(1, n - 8))][:max(0, n - 8)]
clean = lambda b: re.sub(rb'(?m)^Redefining:[^\n]*\n', b'', b.replace(b'\r', b''))
d = os.path.join(E.EV, 'rtsc-s6'); se, si = E.build(E.canon(dict(E.HUMAN['s6-cv8b'])), d); sp = E.private_work(d)
ref = {w: clean(E.sh([se, si], cwd=sp, inp=E.program(w), timeout=120, cpu=60).stdout) for w in ('fib', 'apps')}
with open(out, 'w') as o:
    for r in pick:
        g = dict(r['genome'])
        if os.environ.get('EVOLVE_CELL') == '4' and (g.get('scale') or 0) > 2: g['scale'] = 2
        dd = os.path.join(E.EV, 'rtsc-' + r['id'])
        try:
            eng, img = E.build(E.canon(g), dd); pw = E.private_work(dd)
            try: E.alive(eng, img, pw); al = 'alive'
            except Exception as e: al = 'DEAD ' + str(e)[:40]
            same = ','.join(w for w in ('fib', 'apps') if clean(E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=120, cpu=60).stdout) == ref[w])
            line = '%s bin %d %s fib+apps=%s' % (r['id'], E.bin_size(eng), al, same or 'none')
        except Exception as e:
            line = '%s FAILED %s' % (r['id'], str(e)[:80])
        o.write(line + '\n'); print(line, flush=True)
