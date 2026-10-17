# The after-seed-57 batch - apply in this order (against master after Iteration 363)

| # | patch | what it does |
|---|---|---|
| 1 | nopie-after-seed57.patch | This lab's 32-bit engines built `-fno-pie -no-pie`, as relf builds its own (its Makefile: relf32). Position-independent code on i386 spends one of its seven registers on a base for every table address - the dispatch's `add %ebp,%eax` (Iteration 353) - so this lab's 32-bit measurements (speed32, the selection at both widths, xcheck's 32-bit sample shipped to dream.lan) were pessimistic against relf's own 32-bit engine. evolve.py's W4_ENV (gcc) and CCV() (clang at -m32). After seed 57, which measured its speed32 as before - its numbers comparable with themselves. |

    git apply results/pending/nopie-after-seed57.patch

Tested at Iteration 363: three of seed 55's designs (the fastest, the middle, the slowest), each built
as a 32-bit engine at 4-byte cells and through alive() (the corpus, the kernel): alive, and `file`
says "ELF 32-bit LSB executable" - not PIE. 64 bits untouched (only the 4-byte settings change).
