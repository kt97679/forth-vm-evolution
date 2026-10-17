# The after-seed-57 batch - apply in this order (against master after Iteration 363)

**Applied at Iteration 374** - before seed 57's processing, as the owner chose seed 58 to start when
seed 57's chain ends (the anchoring and constraint test): the batch's one condition, that seed 57 run on
the code before it, holds. run-tests.sh PASS with both applied.

| # | patch | what it does |
|---|---|---|
| 1 | nopie-after-seed57.patch | This lab's 32-bit engines built `-fno-pie -no-pie`, as relf builds its own (its Makefile: relf32). Position-independent code on i386 spends one of its seven registers on a base for every table address - the dispatch's `add %ebp,%eax` (Iteration 353) - so this lab's 32-bit measurements (speed32, the selection at both widths, xcheck's 32-bit sample shipped to dream.lan) were pessimistic against relf's own 32-bit engine. evolve.py's W4_ENV (gcc) and CCV() (clang at -m32). After seed 57, which measured its speed32 as before - its numbers comparable with themselves. |

| 2 | tag2-pairs-after-seed57.patch | design_pairs names a tag-2 design's profiled codes through its own table (vm-tag2-one.h), and keeps wide codes 128-191: until now every tag-2 design's pool for the supers gene was its codes misread as plain opcodes (results/drafts/supers-tag2.md). A run resumed across the patch keeps its cached pools (build/evolve/pairs.json); a new run starts clean. |

    git apply results/applied-after-seed57/nopie-after-seed57.patch
    git apply results/applied-after-seed57/tag2-pairs-after-seed57.patch

Tested at Iteration 363: three of seed 55's designs (the fastest, the middle, the slowest), each built
as a 32-bit engine at 4-byte cells and through alive() (the corpus, the kernel): alive, and `file`
says "ELF 32-bit LSB executable" - not PIE. 64 bits untouched (only the 4-byte settings change).

The second, tested at Iteration 367: seed 56's fastest design (a0a0277bf2, tag2 wide) - its pool now
+ XOR, SWAP OVER, OVER !, OVER R@, + C!, OVER C@, >R OVER, DUP >R, DUP C@, @ < - as counted by hand
through its table; and the same genome without the tag (always named right) gives the same ten, two
adjacent swapped. Non-tag-2 designs: the same code path as before (the identity, codes below 128).
