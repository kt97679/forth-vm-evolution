## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-07 18:51 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 6 of 6 built and measured here.

- 782f3ad7ff speed 0.384 here
- 690981ca5b speed 0.467 here
- c2ef9488ff speed 0.385 here
- a627b954c6 speed 0.533 here
- fb0d57c8a2 speed 1.012 here
- 64a7345393 speed 2.486 here

**381 designs measured on both: Spearman 0.985** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 381): 2 1 4 3 7 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| c71dc8f0dc (rejected) | 0.467 | 0.537 | 1.15 |
| 1ea016c0ff | 0.456 | 0.530 | 1.16 |
| 4023705df2 | 0.458 | 0.534 | 1.17 |
| af5e7cb18d | 0.792 | 1.394 | 1.76 |
| 125f34a2b3 | 0.791 | 1.406 | 1.78 |
| 4434bc9c71 | 0.762 | 1.364 | 1.79 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 4 (8d636f5a9c, f238ccb5e2, c71dc8f0dc, 3360c35d4f); than its fastest: 0.
