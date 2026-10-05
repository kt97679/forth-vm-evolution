# n + and SWAP n + in code compiled at run time: the gene `rtimm`

Iteration 37. Seed 6's front gained nothing on fib and loop from the fused
opcodes of Iterations 33-34: their hot words are compiled at run time, by
the image's own compiler, which the converter's fusions never reach.

## What fib compiles to (seed 6's cd943ed219, dumped from its own image)

```
before                                   with rtimm
06          DUP                          06          DUP
47 02       LIT8 2                       47 02       LIT8 2
29 08 00    <?BRANCH (run-time fused)    29 08 00    <?BRANCH
05          DROP                         05          DROP
47 01       LIT8 1                       47 01       LIT8 1
03 15 00    BRANCH                       03 0c 00    BRANCH
06          DUP                          06          DUP
44 ff ff ff ff  LIT32 -1                 78 ff       ADDI -1
17          +
b5 b0       call FIB                     b7 88       call FIB
07          SWAP                         25 fe       SWAP+I -2
44 fe ff ff ff  LIT32 -2
17          +
b5 b0       call FIB                     b7 88       call FIB
17 01       + EXIT                       17 01       + EXIT
```

32 bytes become 23; a recursive call's 13 dispatches, 10.

## How

`forth/cv8-fuse-imm.4`, loaded after cv8-fuse.4: LITERAL8 leaves LAST-OP
on a literal ADDI's signed byte holds; a + compiled straight after takes
its place - ADDI n, or SWAP+I n where a plain SWAP came straight before
the literal. Every branch target clears LAST-OP, as for the pairs. The
converter writes the design's ADDI, SWAP+I, + and SWAP opcodes into the
overlay's IMM-OPS (tools/layout.py).

**A gene, not a change to cv8-fuse.4**: the code costs image bytes - the
converter keeps each replaced word's X8 copy - so folding it into
cv8-fuse.4 made every design with run-time fusion 3.4% bigger, seed 6's
fastest among them, and no longer its recorded size. As `rtimm` (in
LATE: all 1,309 of seed 6's ids unchanged; expressed only with run-time
fusion and spec imm) the recorded designs build byte for byte as
recorded, and only a design that chooses it pays.

## Measured: image against image, one engine (development VM)

`lab/evolve/image-ab.py c61857fc89 b06a4cf784 af5e8dc29f cd943ed219
--set rtimm=1 --env SOD16_NO_RTIMM=1 --rounds 10` - seed 6's front
designs that have run-time fusion; A with the overlay's table zeroed (the
code there, unused), B as built:

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| c61857fc89 | 10442 | 10442 | +0 | 1.000, 0.850, 1.000, 1.001, 1.000 | 1.012, 0.801, 0.995, 0.989, 1.060 | 0.945 |
| b06a4cf784 | 10670 | 10670 | +0 | 1.000, 0.850, 1.000, 1.001, 1.000 | 1.038, 0.826, 0.983, 0.993, 1.035 | 0.956 |
| af5e8dc29f | 10678 | 10678 | +0 | 1.000, 0.850, 1.000, 1.001, 1.000 | 0.967, 0.810, 1.009, 0.977, 1.002 | 0.937 |
| cd943ed219 | 14553 | 14553 | +0 | 1.000, 0.850, 1.000, 1.002, 1.000 | 0.912, 0.730, 1.071, 0.994, 1.053 | 0.918 |

**fib: 15% fewer dispatches, 17-27% faster; selection 5-8% faster.** The
others do not move. The bytes: 408-472 (+3.4-4.1%) - the designs without
the gene are 10,034, 10,246, 10,254 and 14,081 bytes. A trade, and so a
gene: selection weighs it design by design.
