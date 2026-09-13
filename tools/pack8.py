#!/usr/bin/env python3
"""pack8.py DUMP CELL IMAGE OUT - rewrite a RelF image's runs of
primitives into tagged-byte packs, for engine/pack8.c.

WHAT IT DOES. Every maximal run of consecutive plain primitives in a
compiled word body is replaced by a pack: one cell holding a tag byte
and up to CELL-1 opcode bytes. The run's remaining cells are left
exactly as they were and are never executed, because the engine steps
`ip` over the whole run when it meets the pack.

WHY THE DEAD CELLS ARE LEFT IN PLACE. Because that keeps every address
in the image unchanged, so this tool needs no relocation pass at all -
no link fields to fix, no branch offsets to recompute, no DOES> tails to
chase. The cost is that the image does not get SMALLER, and this tool
therefore measures the scheme's DISPATCH honestly while saying nothing
about its density by the size of the file it writes.

That is the right trade for the question being asked. The tagged-byte
scheme was rejected on dispatch cost, from a synthetic benchmark, in
Iteration 157. Density was never the doubt: the census put it at 0.76x
and nobody disputed that. So the number worth paying for is the one the
rejection rested on, and the density is reported here as an exact count
of cells saved rather than as a smaller file.

WHAT IS NOT PACKED, and why each one would be wrong:

  operand carriers   LIT, BRANCH and ?BRANCH read a following cell.
                     Inside a pack there is no well-defined "following
                     cell", because `ip` has already stepped past the
                     whole run.
  calls              a call IS its own cell - the offset is the
                     instruction - so there is nothing to pack.
  branch targets     a pack can only be entered at its first opcode.
                     Landing in the middle would silently re-run the
                     opcodes before the target, so any operation that
                     something branches to ends the preceding run.
  DOES> tails        the same argument: a tail is an entry point into
                     the middle of a word.
"""
import re
import sys

DUMP, CELL, IMG, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]

# Reuse the dump parser and body decoder that the token translator uses,
# the same way layout.py does, so there is one definition of "what the
# operations in this word are".
_argv = list(sys.argv)
sys.argv = ['sod16.py', DUMP, str(CELL)]
_src = open(__file__.replace('pack8.py', 'sod16.py')).read()
_lib = _src[:_src.index('# ---- decode tokens back')]
G = {'__name__': 'sod16lib'}
exec(compile(_lib, 'sod16lib', 'exec'), G)
sys.argv = _argv

words, read_ops, op_cells = G['words'], G['read_ops'], G['op_cells']
PRIMS = set(G['prims'])
idx_of, cells = G['idx_of'], G['cells']

START = None
for line in open(DUMP, errors='replace'):
    m = re.match(r'^S (\d+) (\d+)', line)
    if m:
        START, HERE = int(m.group(1)), int(m.group(2))
        break
if START is None:
    sys.exit("no S anchor line in %s" % DUMP)

blob = bytearray(open(IMG, 'rb').read())
# A RelF image is an 8-byte magic followed by the dictionary, so an
# address maps to a file offset by a fixed shift. The dump is taken from
# a session with the dumper itself loaded, which appends words ABOVE the
# image's own HERE; those are skipped rather than the dump being made to
# match, because making it match needs locals.4 and save-system.4 loaded
# too and that changes the very image being measured.
HDR = 8
IMG_END = START + len(blob) - HDR


def put_cell(addr, value):
    off = HDR + (addr - START)
    blob[off:off + CELL] = value.to_bytes(CELL, 'little')


MAXOPS = CELL - 1          # opcode bytes that fit beside the tag byte

# DOES> tails: a body whose first cell is a call to a mid-word address.
tails = set()
starts = {w['s'] for w in words}
for w in words:
    v = cells.get(w['s'])
    if v is not None and not (v & 1):
        t = w['s'] + CELL + v
        if t not in starts:
            tails.add(t)

packs = runs = saved = total_ops = 0

for w in words:
    if w['e'] > IMG_END:
        continue               # defined by the dumper, not in the image
    if w['n'] in PRIMS:
        # A PRIMITIVE's body is not code that runs - it is the token the
        # compiler COPIES when it compiles a call to that primitive.
        # Packing it made every newly compiled DUP come out as a
        # two-opcode pack of DUP and EXIT, so the first runtime
        # definition returned its own argument.
        continue
    ops = read_ops(w)
    if ops is None:
        continue
    # Byte offset of each operation within the body.
    at, off = [], 0
    for k, pl in ops:
        at.append(off)
        off += op_cells(k, pl)

    # Everything that must remain reachable as an entry point.
    breaks = set()
    for j, (k, pl) in enumerate(ops):
        if k in ('BR', 'QBR'):
            breaks.add(at[j] + CELL + pl)
        elif k == 'OPD':
            breaks.add(at[j] + pl)
    for t in tails:
        if w['s'] < t < w['e']:
            breaks.add(t - w['s'])

    # Maximal runs of plain primitives, split at entry points.
    run = []
    def flush():
        global packs, runs, saved
        if len(run) < 2:
            del run[:]
            return
        runs += 1
        i = 0
        while i < len(run):
            chunk = run[i:i + MAXOPS]
            if len(chunk) < 2:
                break          # a lone trailing opcode stays a cell
            tag = 3 | ((len(chunk) - 1) << 2)
            value = tag
            for n, o in enumerate(chunk):
                value |= o[1] << (8 * (n + 1))
            put_cell(w['s'] + chunk[0][0], value)
            packs += 1
            saved += len(chunk) - 1
            i += len(chunk)
        del run[:]

    for j, (k, pl) in enumerate(ops):
        if k == 'P' and idx_of[pl] < 256 and (j == 0 or at[j] not in breaks):
            run.append((at[j], idx_of[pl]))
            total_ops += 1
        else:
            flush()
            if k == 'P' and idx_of[pl] < 256:
                run.append((at[j], idx_of[pl]))
                total_ops += 1
    flush()

open(OUT, 'wb').write(bytes(blob))
old = len(blob) - HDR
print("packs %d in %d runs; %d cells of %d primitive cells folded away"
      % (packs, runs, saved, total_ops))
print("image %d bytes; %d bytes would be saved by a relocating build "
      "(%.3fx)" % (old, saved * CELL, (old - saved * CELL) / old))
