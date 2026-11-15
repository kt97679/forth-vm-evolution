# The pure savings - VALUE taken, the strings priced (Iteration 680; step 1 of results/drafts/search-reopen-plan-677.md)

## Item 7 - VALUE without its kind cell: taken (forth/coreext.4)

A VALUE is `CREATE , DOES> @` - its cell alone, relf's way: 8 bytes (4 at 4-byte cells) and a CELL+ a fetch less. TO
tells a 2VALUE by a list: each 2VALUE's first cell, where its kind was, links to the one before (2VALUES), walked only
by TO - a 2VALUE the same size as before. Measured by genapps.py --sizes before and after, s6 and the ten designs:

- brainless: -696 bytes at 8-byte cells on all eleven (its 87 VALUEs; 674 predicted 696), -348 to -352 at 4;
- minif, wordfreq and the selection's four: 0 - none of them makes a VALUE (gc16's two matches are comments). **The
  selection cannot see this saving** (the plan's first risk, as it named): no image moves either - coreext.4 is a
  library, in no image. It is taken as a size saving that is exact and costs no speed (one CELL+ a fetch fewer), the
  standing rule - not as a gene.

## Item 6 - inline strings without cell alignment: priced, not built

lab/evolve/string-price.py: S" and ." redefined before each program, laying the string as kernel.4's STRING, does
(count, characters, ALIGN; the run-time word's ALIGNED) and again without both; HERE's advance, the first less the
second (bytes of code saved):

| system | the four, 8-byte cells | held-out three, 8 | the four, 4-byte | held-out three, 4 |
|---|---:|---:|---:|---:|
| s6 | 147 | 354 | 28 | 146 |
| smallest | 155 | 338 | 32 | 142 |
| least-memory | 174 | 326 | 32 | 136 |
| portable-small | 166 | 316 | 40 | 134 |
| portable-knee | 162 | 319 | 40 | 141 |
| portable-arm | 163 | 301 | 37 | 131 |
| portable-fastest | 173 | 300 | 31 | 129 |
| best-all-round | 137 | 293 | 46 | 129 |
| small-jit | 150 | 302 | 37 | 138 |
| fastest-x86-64 | 105 | 305 | 33 | 143 |
| fastest-x86-32 | 131 | 287 | 40 | 139 |

Per program at 8-byte cells, s6: sim16 7, gc16 6, scan 125, evo 9; wordfreq 23, minif 70, brainless 261 (scan's
27 strings carry the four's share). Against the four's code (6,948-8,368 bytes) that is 1.0-2.3 %; against the
total (about 21-51 KB) under 1 %. The kernel image's own inline strings shrink with it - every design's image -
measured only once it is built.

What building it takes (why it is not done in the same step): sod16.py keeps inline strings cell-aligned on purpose
("no kernel change at all"), so the alignment is a contract across kernel.4's (S") (.") (ABORT") and STRING,, the
converters (tools/sod16.py's STR operands, tools/layout.py's SQ/DQ), cross.4 and the self-hosting cross compiler
(forth/cross-cv8.4's STR+). The cell family's threaded code must stay cell-aligned after a string - so the
alignment becomes the family's code alignment (1 for CV8's byte code), not none; the frozen stages validate
compares (s3-s5) must not move. Next: that change, then every image and s6 measured before and after.
