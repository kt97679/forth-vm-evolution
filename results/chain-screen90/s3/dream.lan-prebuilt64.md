## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-10 12:16 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 32 of 32 built and measured here.

- 7fb40ff7ba speed 0.378 here
- 2a0e020033 speed 0.388 here
- c00b89387c speed 0.441 here
- 2ca099a850 speed 0.435 here
- 0c34db4318 speed 0.421 here
- a88c57d744 speed 0.396 here
- c1daef30d7 speed 0.422 here
- d2ced1eeb2 speed 0.412 here
- 094b4f4220 speed 0.522 here
- 4b003ada88 speed 0.519 here
- 0d9a909f1a speed 0.471 here
- 8abee9e480 speed 0.492 here
- c181fa46f1 speed 0.525 here
- f8beff72c9 speed 0.747 here
- 78f5dcfa21 speed 0.736 here
- 2d9da6e2a3 speed 1.037 here
- 236f438f62 speed 0.931 here
- 6d7a78ae47 speed 1.315 here
- a2a2b12cb9 speed 1.300 here
- d1eb81c577 speed 2.234 here
- c59afb99b9 speed 2.273 here
- 7cc76c82e3 speed 2.233 here
- b63c2031e1 speed 2.328 here
- b1ec80afdf speed 2.426 here
- 834db54e0b speed 2.443 here
- 782f3ad7ff speed 0.389 here
- 3eb59b271d speed 0.424 here
- c2ef9488ff speed 0.389 here
- ae99617f06 speed 0.524 here
- fb0d57c8a2 speed 1.048 here
- 64a7345393 speed 2.490 here
- 11a56ff9e4 speed 0.388 here

**240 designs measured on both: Spearman 0.987** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 240): 1 2 3 9 5 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| b3b4951ed2 (rejected) | 0.323 | 0.350 | 1.08 |
| e2746a2dc0 | 0.343 | 0.387 | 1.13 |
| 1993148bc2 | 0.378 | 0.439 | 1.16 |
| c1e58ce43a | 0.757 | 1.290 | 1.70 |
| 757a32d750 | 0.621 | 1.060 | 1.71 |
| e365635532 (rejected) | 0.132 | 0.233 | 1.76 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 5 (e365635532, ba2d2f350d, b3b4951ed2, 4023705df2, ceeaacf723); than its fastest: 3 (e365635532, ba2d2f350d, b3b4951ed2).
