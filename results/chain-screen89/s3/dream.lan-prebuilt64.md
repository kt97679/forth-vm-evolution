## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-09 11:26 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 17 of 17 built and measured here.

- 3c5d6c64d8 speed 0.270 here
- 68a476fe49 speed 1.660 here
- bd0a0a725b speed 1.654 here
- d02a90b0dc speed 1.659 here
- bc7366289f speed 1.647 here
- ef92ebcbcd speed 1.647 here
- e2f3732d3f speed 1.660 here
- c7c35f9c97 speed 0.233 here
- ee34931cd7 speed 0.218 here
- 06b188f45b speed 0.226 here
- 782f3ad7ff speed 0.383 here
- c2ef9488ff speed 0.389 here
- a627b954c6 speed 0.532 here
- fb0d57c8a2 speed 1.008 here
- 64a7345393 speed 2.359 here
- 8164d3858f speed 0.526 here
- ae99617f06 speed 0.526 here

**280 designs measured on both: Spearman 0.992** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 280): 1 5 8 11 12 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 2ba58b1e45 | 0.316 | 0.330 | 1.04 |
| 3e13bd3c58 (rejected) | 0.451 | 0.519 | 1.15 |
| 11a56ff9e4 | 0.333 | 0.383 | 1.15 |
| 01869da41b | 0.618 | 1.073 | 1.74 |
| a19dbb567c | 0.142 | 0.248 | 1.75 |
| 23a8ba850d | 0.143 | 0.251 | 1.75 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 5 (15ecc6a232, 0a0e767d85, e11b4cbd12, 3e13bd3c58, 71e51f89f1); than its fastest: 1 (15ecc6a232).
