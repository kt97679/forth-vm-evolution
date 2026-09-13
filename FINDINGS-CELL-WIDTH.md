# Where the 64-bit image is still bigger

`s6-cv8b` run-only: 7,609 bytes at 8-byte cells, 6,749 at 4-byte. The
token stream is the same program either way, so the 860-byte difference
is worth accounting for exactly. Measured, not estimated - the numbers
below come from instrumenting `layout.py` and they sum to the total.

| component | 8-byte | 4-byte | diff | what it is |
|---|---|---|---|---|
| data word bodies | 1,696 | 1,288 | +408 | parameter fields |
| image header | 320 | 164 | +156 | 33 wordlist cells + locals |
| code token stream | 3,300 | 3,148 | +152 | cell-sized inline operands |
| padding before bodies | 224 | 103 | +121 | alignment for those operands |
| image prologue | 40 | 20 | +20 | five boot cells |
| dictionary links | 458 | 455 | +3 | byte-granular already |
| name text | 1,571 | 1,571 | 0 | |
| **total** | **7,609** | **6,749** | **+860** | |

Before the byte-granular header the same difference was 2,980 bytes, of
which 1,088 was link cells, 496 name padding and 660 end-of-body
padding. All of that is gone. What is left divides into three kinds.

## Irreducible: 408 bytes, the data words

A `VARIABLE` holds a cell because that is what a cell is for. 102 cells
across 39 data words, four bytes wider each. Nothing to do here short of
changing what the language means.

## Structural but addressable: 156 bytes, the image header

The header publishes the hashed word list into the image: a thread count
and 32 chain heads, one cell each. They are OFFSETS into an image of
7.3 KB. Sixteen bits would hold any of them with room to spare, and
32-bit offsets are trivially safe; either would save 132 bytes at 8-byte
cells and change nothing a Forth program can observe.

## The interesting 273: seventeen operands and their alignment

Only seventeen places in the whole kernel carry a cell-sized operand
inside a code body - five `OPD` (the `(DO)`/`(LOOP)` byte offsets) and
twelve `XT` (`(POSTPONE)`, `[']`) - plus fourteen inline strings. Each
costs a whole cell, and forces the body that contains it to start on a
cell boundary, which is the 121 bytes of padding.

Per-word, the growth is entirely in the words one would predict:

    +16  SORTNFA, DUMP        +12  COLD
    +8   DO ?DO LOOP LEAVE WHILE DOES> POSTPONE S" ." ABORT" COLLECT

That is 273 bytes spent so that `(LOOP)` can read its operand with a
single aligned cell load. `(LOOP)`'s operand is a BYTE offset into the
same word, never more than a couple of hundred; an `XT` is an offset
into the image, under 16 bits. Both could be two or three bytes in the
token stream like everything else, and then nothing in a code body would
need cell alignment at all.

## If all three were done

408 irreducible, 452 addressable. The 8-byte image would land near 7,150
- about 0.29x of cell threading, against 0.31x today - and, more to the
point, the 8-byte and 4-byte images would differ by only the width of
the data they actually store.

Not done. Recorded because the question "why is the 64-bit image bigger"
has an exact answer, and because the answer says the remaining
difference is no longer about the ENCODING at all: it is seventeen
operands, a header table and the parameter fields.
