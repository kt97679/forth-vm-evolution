#!/usr/bin/env python3
"""names-check.py [IDS...] - word names in UTF-8, defined and then compiled
into other words, on every kind of design (Iteration 232).

The fault it pins: >NAME finds a word's header by scanning back from its body
for the first byte with bit 7 set - the count byte. With the name between the
count byte and the body, a UTF-8 name's own bytes (bit 7 set) stopped the scan
first, and one with bit 5 set read as a primitive's count byte: COMPILE,
inlined garbage - `: суп 5 . ;` ran, `: обед суп суп ;` printed nothing.
Since Iteration 232 byte headers carry the count byte after the name.

Each design runs one program and must print what the cell system (s0) prints
- its compiler never asks >NAME - byte for byte: names that end in bytes with
bit 5 set (BF, A9, A0), a C2 three bytes from the end, CJK, 31 ASCII bytes,
15 Cyrillic letters (30 bytes), IMMEDIATE, a redefinition, a lookup by
SEARCH-WORDLIST, and ' and EXECUTE.
"""
import os, sys, subprocess
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
    'S" café" FORTH-WORDLIST SEARCH-WORDLIST . EXECUTE CR',
    "' обед EXECUTE ' voilà EXECUTE CR",
    'BYE', '']).encode()
def run(eng, img, pw):
    r = subprocess.run([eng, img], cwd=pw, input=PROG, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    return r.returncode, r.stdout.replace(b'\r', b'')
ref = run(os.path.join(E.O, 's0-cell-64'), os.path.join(E.O, 's0-cell-s64.img'), E.private_work(os.path.join(E.EV, 'names-s0')))
print('## the cell system (s0), the reference: status %d\n\n```\n%s```\n' % (ref[0], ref[1].decode(errors='replace')))
want = [b'5 5', b'9', b'3 3', b'4', b'6 6', b'1', b'2', b'11', b'5 5 8', b'-1 9', b'5 5 3']
lines = [l.strip() for l in ref[1].split(b'\n')]
missing = [w for w in want if w not in lines]
fails = int(bool(missing) or ref[0] != 0)
if missing: print('THE REFERENCE ITSELF lacks %s' % missing)
ids = args or ['s6-cv8b', 's5-cv8spec', 'add5ec8937', 'cc6d168e0a', 'f20de05a64', '4a351e360a']
for did in ids:
    g = E.canon(E.HUMAN[did] if did in E.HUMAN else E.recorded_genome(did)); d = os.path.join(E.EV, 'names')
    eng, img = E.build(g, d); got = run(eng, img, E.private_work(d))
    same = got == ref
    fails += not same
    print('- %s (%s): %s' % (did, ', '.join('%s=%s' % (k, g.get(k)) for k in ('tag2', 'bytehdr', 'kfast', 'klookup', 'msc', 'tail', 'jit', 'fsys') if k in g),
          'as the cell system' if same else 'DIFFERS - status %d, %r' % (got[0], got[1][-300:])))
print('\n%s' % ('PASS' if not fails else 'FAIL - %d' % fails))
sys.exit(1 if fails else 0)
