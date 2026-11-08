## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-07 15:57 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 6 of 6 built and measured here.

- 782f3ad7ff speed 0.384 here
- 690981ca5b speed 0.469 here
- c2ef9488ff speed 0.385 here
- a627b954c6 speed 0.529 here
- fb0d57c8a2 speed 1.008 here
- 64a7345393 speed 2.421 here

**381 designs measured on both: Spearman 0.986** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 381): 1 2 4 3 8 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 1ea016c0ff | 0.456 | 0.528 | 1.16 |
| c71dc8f0dc (rejected) | 0.467 | 0.541 | 1.16 |
| 4023705df2 | 0.458 | 0.533 | 1.16 |
| a7943ccff0 | 0.802 | 1.375 | 1.71 |
| 642f8fdad2 | 0.775 | 1.363 | 1.76 |
| 6165016d29 | 0.804 | 1.415 | 1.76 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 4 (8d636f5a9c, f238ccb5e2, c71dc8f0dc, 3360c35d4f); than its fastest: 1 (8d636f5a9c).
