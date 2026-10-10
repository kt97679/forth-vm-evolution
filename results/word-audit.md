# Every word, audited - the sources and the weights (Iteration 131)

The first step of results/word-audit-plan.md: the other Forths' sources, newer online where they
exist (the owner: check online; else the collection), their licences; and every kernel word weighed
by what it costs under the selection, so the comparison starts where the cost is.

## The sources

Fetched to the VM, not into the repository (their licences differ; the commits are the record).

| Forth | where | commit, date | licence | use here | in the collection |
|---|---|---|---|---|---|
| pForth | github.com/philburk/pforth | e561763 2026-07-28 | 0BSD-style | code | PFTHPC19 (v19, 1990s) |
| FICL | github.com/jwsadler58/ficl (its author) | 50c54d6 2026-06-12 | BSD-3-Clause | code | ficl202 (2.02) |
| ueForth / ESP32forth | github.com/flagxor/ueforth (eForth's successor) | d8376db 2026-09-26 | Apache-2.0 | code | eForth 1.0 (1990), lx-eforth, e4a |
| jonesforth | github.com/nornagon/jonesforth | d97a25b 2022-03-10 | public domain | code | - |
| zForth | github.com/zevv/zForth | 41db72d 2025-08-15 | MIT | code | - |
| Retro | github.com/crcx/retroforth | 7d23972 2026-09-11 | ISC | code (not a standard Forth) | - |
| lbForth | github.com/larsbrinkhoff/lbForth | 912433b 2023-02-11 | GPL-3 | ideas only | - |
| the Forth 2012 standard | github.com/Forth-Standard/forth-standard | 79bd531 2026-09-05 | none stated | ideas (reference implementations) | - |
| F83 (Laxen, Perry) | the owner's collection | - | public domain | code | Open Source - 8086 Forth 83 2.1.0 (no newer) |
| cmFORTH, FIRST/THIRD, Itsy, 3ins4th | the owner's collection | - | not stated | ideas | - |
| gforth, SP-Forth, bigFORTH, ciforth, SOD32 | the owner's collection | - | GPL | ideas only | - |
| RelF | github.com/kt97679/relf, the collection | - | the owner's | code | RelF 0.1-0.3, relf_dev |

Newer online: pForth, FICL (4.x from its author, against 2.02), eForth (ueForth), and three
not in the collection - jonesforth, zForth, Retro. Nothing newer for F83; the rest from the collection.

## The weights

Profiling builds (VMPROF, exact) of hand-made s6, the front's fastest (38446e6c09, seed 37, the JIT)
and its smallest (cd6c94b30d), on the six selected workloads; each dispatch counted to the kernel
word whose bytes hold it (the converter's map), a word's weight the mean of its shares of the six -
the equal weighting of the speed score. Kernel words carry 60% of s6's dispatches (the rest is code
compiled at run time), 60% of the smallest's, 70% of what the fastest still interprets (its JIT runs
fib, loop and its translated words natively - not counted, so its weights are the interpreter's).
**17 words carry 90% of the kernel words' share on s6 and on the smallest, 41 on the fastest; the
three sets together are 51 words** - the audit's order:

| word | bytes | s6 | fastest | smallest |
|---|---|---|---|---|
| INTERPRET | 93 |  | 11.36% |  |
| FILL | 24 | 10.42% |  | 10.00% |
| (LOOP) | 23 | 9.50% |  | 9.10% |
| (+LOOP) | 36 | 7.54% |  | 7.42% |
| PARSE-WORD | 47 | 0.91% | 7.10% | 1.00% |
| 2@ | 5 | 2.03% | 6.04% | 2.00% |
| NEXT-NFA8 | 65 | 3.41% |  | 5.34% |
| I | 4 | 5.08% |  | 4.93% |
| ?STACK | 33 |  | 3.72% |  |
| REFILL | 105 | 1.77% | 3.58% | 1.90% |
| SEARCH-WORDLIST | 71 | 3.35% |  | 3.30% |
| CMOVE | 30 | 2.50% |  |  |
| NUMBER? | 115 |  | 2.25% |  |
| 2! | 6 | 0.79% | 1.96% | 0.78% |
| HERE | 4 |  | 1.96% |  |
| COLD | 85 |  | 1.87% |  |
| SCAN | 27 | 1.42% |  | 1.48% |
| NAME=? | 32 | 1.45% |  | 1.48% |
| CMOVE> | 32 |  | 1.47% |  |
| 0= | 2 | 1.29% | 1.36% | 1.29% |
| > | 2 |  | 1.36% | 0.81% |
| WORD | 30 |  | 1.34% |  |
| >NAME | 8 |  | 1.31% |  |
| 1- | 2 | 1.27% | 1.29% | 1.27% |
| COMPILE, | 66 |  | 1.14% |  |
| FIND | 63 | 0.86% |  | 0.94% |
| HEADER | 169 |  | 0.92% |  |
| 1+ | 2 | 0.68% | 0.92% | 0.69% |
| COMPILE,8 | 73 |  | 0.86% |  |
| SUPER-OP | 51 |  | 0.76% |  |
| C, | 9 |  | 0.74% |  |
| INCLUDE-FILE | 64 |  | 0.72% |  |
| CALL, | 62 |  | 0.69% |  |
| SMALL-LIT? | 84 |  | 0.65% |  |
| * | 2 |  | 0.63% |  |
| >IN | 16 |  | 0.62% |  |
| ; | 55 |  | 0.61% |  |
| ALLOT | 4 |  | 0.60% |  |
| BL | 2 |  | 0.55% |  |
| IMM+ | 102 |  | 0.49% |  |
| OP, | 7 |  | 0.49% |  |
| PARSE | 29 |  | 0.42% |  |
| PICK | 7 |  | 0.41% |  |
| LITERAL | 35 |  | 0.40% |  |
| W, | 23 |  | 0.40% |  |
| CONTEXT | 48 |  | 0.40% |  |
| W@ | 9 |  | 0.40% |  |
| NAMEBUF | 48 |  | 0.39% |  |
| (POSTPONE) | 23 |  | 0.34% |  |
| LIT, | 90 |  | 0.33% |  |
| DP | 16 |  | 0.33% |  |

## Seen already

- **FILL through NAME>BUF.** `NAMEBUF 32 0 FILL 32 MIN NAMEBUF PLACE`: every dictionary lookup
  zero-fills 32 bytes, a byte at a time in a Forth loop - on s6, FILL is 35% of the kernel workload's
  dispatches and 27% of the corpus's (cross.4 also clears its 64 KB target image with it, once a
  run). kfast replaces this path, which is why the fastest design does not show it - 240 of seed
  37's 242 front designs have kfast - but s6, the yardstick, and every design without it pay it.
  pForth, FICL and F83 have FILL in C or assembler; eForth's is a FOR NEXT byte loop.
- **(LOOP), (+LOOP), I** - 22% of s6's share: user loops on designs without the loop opcodes
  (ops10); evolved designs mostly have them; s6 does not.
- **The dictionary search** - NEXT-NFA8, SEARCH-WORDLIST, NAME=?, FIND: ~9% on s6 and the smallest.
- **The interpreter** - INTERPRET, PARSE-WORD, ?STACK, REFILL, NUMBER?, WORD, HERE: the fastest
  design's bytecode. **COLD**, 1.9% of the fastest's: start-up, in every timed run.

A kernel change moves s6, the yardstick, and every design without the matching k-gene; as an overlay
gene, s6 and the recorded designs stay as they are - the plan's rule (4).

**Next**: each of the 51 against pForth, FICL, F83, ueForth, jonesforth, zForth and RelF - ours,
theirs, the candidate - priced in dispatches and bytes, the heaviest first.
