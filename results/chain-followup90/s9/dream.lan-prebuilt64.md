## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-09 22:10 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 5 of 5 built and measured here.

- 782f3ad7ff speed 0.380 here
- c2ef9488ff speed 0.385 here
- ae99617f06 speed 0.520 here
- fb0d57c8a2 speed 1.014 here
- 64a7345393 speed 2.373 here

**8 designs measured on both: Spearman 0.905** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 8): 1 2 5 4 3 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 3e13bd3c58 (rejected) | 0.451 | 0.515 | 1.14 |
| 11a56ff9e4 | 0.333 | 0.385 | 1.16 |
| e11b4cbd12 (rejected) | 0.319 | 0.397 | 1.25 |
| 11658227de (rejected) | 1.869 | 2.529 | 1.35 |
| 0a0e767d85 (rejected) | 0.203 | 0.283 | 1.39 |
| 15ecc6a232 (rejected) | 0.131 | 0.220 | 1.68 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 3 (15ecc6a232, 0a0e767d85, e11b4cbd12); than its fastest: 2 (15ecc6a232, 0a0e767d85).
