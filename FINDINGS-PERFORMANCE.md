# Where a kernel compile actually spends its time

The article compares encodings - how much each VM instruction costs to
dispatch. This asks a different question: how MANY instructions does
the system dispatch, and in which Forth words?

## Method: count, do not time

The engine built with `-DPROFILE=1` records how many times the VM
instruction at every address executed. `tools/layout.py` with
`SYMMAP=file` writes every word's body range in the image.
`tools/attribute.py` joins the two and charges each dispatch to the word
it happened in.

Dispatch counts are exact and machine-independent. This project spent a
great deal of effort fighting timing noise - layout variants, error
bars, discarded benchmarks. For changes made in Forth, a dispatch count
is a noise-free proxy that needs none of that. Time still has to be
checked, since dispatches do not all cost the same, but it is no longer
the only instrument.

## What it found

Kernel compilation on the specialised CV8 engine, 8-byte cells:
8,402,938 dispatches, and

    FILL              36.8%
    SEARCH-WORDLIST    8.9%
    CMOVE              8.8%
    REFILL             7.6%
    SCAN               4.8%
    PARSE, FIND, HASH, SKIP, PLACE ...

FILL, CMOVE, SCAN and SKIP - four generic byte-at-a-time loops - were
52% of all the work. And almost every FILL call came from one line:

    : NAME>BUF  NAMEBUF 32 0 FILL  32 MIN NAMEBUF PLACE ;

Every dictionary lookup blank-fills a 32-byte name buffer, one byte at a
time, at about ten dispatches per byte. 6,674 lookups made that line
roughly 30% of an entire kernel compile.

The buffer only has to be zeroed in cell-sized pieces, because
SEARCH-WORDLIST compares names a cell at a time. So the fix is to zero it
by cells - still pure Forth, no new primitive:

    : NAME>BUF
      NAMEBUF 32 OVER + SWAP
      BEGIN 0 OVER ! CELL+ 2DUP = UNTIL 2DROP
      32 MIN NAMEBUF PLACE ;

## Result

    dispatches     8,402,938 -> 6,015,283     -28.4%
    s0-cell        21.07 ms  -> 16.28 ms      -22.8%
    s5-cv8spec     11.06 ms  -> 8.37 ms       -24.4%

All ten systems pass the 616-case corpus; the kernel compile is still
byte-identical to its reference; and the new kernel reaches a fixed
point - it compiles itself to itself.

For scale, the whole encoding ladder bought about the same on this
workload. The two are orthogonal: CV8+spec against the cell engine is
0.525 before the fix and 0.514 after, so the encoding comparison is
essentially unchanged and the speed-ups multiply.

## A trap worth knowing

The first attempt showed no effect at all. `tools/build-stages.sh`
builds every host image from the committed `forth/kernel-seed.img` - a
prebuilt binary of the OLD kernel - so editing `kernel.4` changes what
gets compiled, not the compiler that does the compiling. A kernel change
has to be bootstrapped: compile the new source with the old seed, check
the result compiles itself to itself, and install it as the new seed.

## What is left, ranked by measured share after the fix

    SEARCH-WORDLIST   12.5%   the chain walk and cell compare
    CMOVE             12.3%   14,162 calls, about 5 bytes each
    REFILL            10.6%   line input
    FILL               8.2%   cross.4 clearing its 40 KB image, once
    SCAN               6.7%   text scanning
    NAME>BUF           4.3%
    PARSE, FIND, HASH, SKIP, PLACE ...

Two different kinds of fix apply.

Where the data is cell-aligned - FILL of the target image, the name
buffer - a cell-wise loop in Forth gets most of the gain without a new
primitive, which is what NAME>BUF shows.

Where the data is short and unaligned - CMOVE of five-byte names, SCAN
and SKIP over source text - no Forth loop avoids paying per byte. Only a
primitive does: memmove, memchr and memset would each turn a
fifty-dispatch call into one.

That second kind conflicts directly with this system's design. SOD32's
appeal, and the subject of the author's earlier article, is how few
primitives a Forth needs. The data says three more would remove most of
what is left. Whether that is worth it is a question about what the
system is for, and the measurements cannot answer it.

## Status

Recorded, not applied. When the branches were consolidated into master,
the VM designs were declared final - so these findings, tools/attribute.py
and the layout tool's SYMMAP option came in, but the kernel change did
not: changing the kernel changes the seed, and so every image and every
published figure in the article. The patch - NAME>BUF zeroing its buffer
a cell at a time, and the bootstrapped seed - is commit c91b008, reachable
from master as the second parent of the merge that brought this file in.
Applying it is a decision about the article as well as about speed.
