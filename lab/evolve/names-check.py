#!/usr/bin/env python3
"""names-check.py [IDS...] - word names in UTF-8, defined and then compiled
into other words, on every kind of design (Iteration 232).

The fault it pins: >NAME finds a word's header by scanning back from its body
for the first byte with bit 7 set - the count byte. With the name between the
count byte and the body, a UTF-8 name's own bytes (bit 7 set) stopped the scan
first, and one with bit 5 set read as a primitive's count byte: COMPILE,
inlined garbage - `: суп 5 . ;` ran, `: обед суп суп ;` printed nothing.
Since Iteration 232 byte headers carry the count byte after the name.

Each design runs one program and must print the numbers it should: names
that end in bytes with bit 5 set (BF, A9, A0), a B0 one byte before the end,
CJK, 31 ASCII bytes, 15 Cyrillic letters (30 bytes), IMMEDIATE, a
redefinition, and ' with EXECUTE - on the evolved designs given (byte
headers) and on every hand-made stage, cell headers included (Iteration 233:
the count byte after the name there too; the kernel's own COMPILE, asked
>NAME the same way).
"""
import os, sys, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
args = [a for a in sys.argv[1:]]; sys.argv = [sys.argv[0]]
import evolve as E
E.setup()
PROG = '\n'.join([
    ': суп 5 . ;  : обед суп суп ;  обед CR',
    ': café 9 . ;  : menu café ;  menu CR',
    ': voilà 3 . ;  : w2 voilà voilà ;  w2 CR',
    ': a°b 4 . ;  : w3 a°b ;  w3 CR',
    ': 名前 6 . ;  : w4 名前 名前 ;  w4 CR',
    ': x123456789012345678901234567890 1 . ;  : w5 x123456789012345678901234567890 ;  w5 CR',
    ': ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ 2 . ;  : w6 ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ ;  w6 CR',
    ': ёж 11 . ; IMMEDIATE  : w7 ёж ;  CR',
    ': суп 8 . ;  обед суп CR',
    "' café EXECUTE CR",
    "' обед EXECUTE ' voilà EXECUTE CR",
    'BYE', '']).encode()
WANT = ['5 5', '9', '3 3', '4', '6 6', '1', '2', '11', '5 5 8', '9', '5 5 3']
def run(eng, img, pw):
    r = subprocess.run([eng, img], cwd=pw, input=PROG, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    out = r.stdout.replace(b'\r', b'').decode(errors='replace')
    nums = [l.strip() for l in out.split('\n') if l.strip() and all(t.lstrip('-').isdigit() for t in l.split())]
    return r.returncode, nums, out
fails = 0
cell = '--cell' in args; args = [a for a in args if a != '--cell']
ids = args or ['s6-cv8b', 'add5ec8937', 'cc6d168e0a', 'f20de05a64', '4a351e360a', 'dde890d478']
print('Expected, line by line: %s\n' % ' | '.join(WANT))
for did in ids:
    g = E.canon(E.HUMAN[did] if did in E.HUMAN else E.recorded_genome(did)); d = os.path.join(E.EV, 'names')
    eng, img = E.build(g, d); rc, nums, out = run(eng, img, E.private_work(d))
    ok = rc == 0 and nums == WANT
    fails += not ok
    print('- %s (%s): %s' % (did, ', '.join('%s=%s' % (k, g.get(k)) for k in ('tag2', 'bytehdr', 'kfast', 'klookup', 'msc', 'tail', 'jit', 'fsys') if k in g),
          'right' if ok else 'WRONG - status %d, got %s' % (rc, ' | '.join(nums))))
STAGES = ['s0-cell', 's1-sod16', 's2-cpt16', 's3-cpt16f', 's4-cv8', 's5-cv8spec', 's6-cv8b', 'p4-pack4', 'p8-pack8',
          's7-spn', 's7-full', 's8-spncv8', 's8-full', 's8-lazy']
if cell or not args:  # Iteration 233: the cell headers carry the count byte after the name too - every stage judged
    for st in STAGES:
        eng = os.path.join(E.O, st + '-64'); img = os.path.join(E.O, st + '-s64.img')
        if not (os.path.exists(eng) and os.path.exists(img)): print('- %s: not built here' % st); continue
        dd = os.path.join(E.EV, 'names-' + st); shutil.rmtree(dd, ignore_errors=True)
        rc, nums, out = run(eng, img, E.private_work(dd))
        ok = rc == 0 and nums == WANT
        fails += not ok
        print('- %s (hand-made stage): %s' % (st, 'right' if ok else 'WRONG - status %d, got %s' % (rc, ' | '.join(nums))))
print('\n%s' % ('PASS' if not fails else 'FAIL - %d' % fails))
sys.exit(1 if fails else 0)
