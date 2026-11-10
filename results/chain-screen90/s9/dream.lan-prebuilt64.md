## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-10 18:23 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 32 of 32 built and measured here.

- 7fb40ff7ba speed 0.375 here
- 2a0e020033 speed 0.388 here
- c00b89387c speed 0.444 here
- 2ca099a850 speed 0.435 here
- 0c34db4318 speed 0.420 here
- a88c57d744 speed 0.400 here
- c1daef30d7 speed 0.420 here
- d2ced1eeb2 speed 0.414 here
- 094b4f4220 speed 0.520 here
- 4b003ada88 speed 0.516 here
- 0d9a909f1a speed 0.477 here
- 8abee9e480 speed 0.494 here
- c181fa46f1 speed 0.523 here
- f8beff72c9 speed 0.751 here
- 78f5dcfa21 speed 0.731 here
- 2d9da6e2a3 speed 1.044 here
- 236f438f62 speed 0.920 here
- 6d7a78ae47 speed 1.299 here
- a2a2b12cb9 speed 1.307 here
- d1eb81c577 speed 2.257 here
- c59afb99b9 speed 2.267 here
- 7cc76c82e3 speed 2.234 here
- b63c2031e1 speed 2.250 here
- b1ec80afdf speed 2.368 here
- 834db54e0b speed 2.358 here
- 782f3ad7ff speed 0.383 here
- 3eb59b271d speed 0.418 here
- c2ef9488ff speed 0.394 here
- ae99617f06 speed 0.529 here
- fb0d57c8a2 speed 1.006 here
- 64a7345393 speed 2.363 here
- 11a56ff9e4 speed 0.381 here

**240 designs measured on both: Spearman 0.986** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 240): 1 2 3 9 5 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| b3b4951ed2 (rejected) | 0.323 | 0.356 | 1.10 |
| e2746a2dc0 | 0.343 | 0.388 | 1.13 |
| eac560744d | 0.458 | 0.535 | 1.17 |
| 757a32d750 | 0.621 | 1.054 | 1.70 |
| 69b4c7efbd | 0.761 | 1.293 | 1.70 |
| e365635532 (rejected) | 0.132 | 0.231 | 1.75 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 5 (e365635532, ba2d2f350d, b3b4951ed2, 4023705df2, ceeaacf723); than its fastest: 3 (e365635532, ba2d2f350d, b3b4951ed2).
