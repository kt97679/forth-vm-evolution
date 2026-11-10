## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-10 10:13 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 32 of 32 built and measured here.

- 7fb40ff7ba speed 0.379 here
- 2a0e020033 speed 0.390 here
- c00b89387c speed 0.436 here
- 2ca099a850 speed 0.439 here
- 0c34db4318 speed 0.417 here
- a88c57d744 speed 0.398 here
- c1daef30d7 speed 0.424 here
- d2ced1eeb2 speed 0.411 here
- 094b4f4220 speed 0.521 here
- 4b003ada88 speed 0.519 here
- 0d9a909f1a speed 0.476 here
- 8abee9e480 speed 0.495 here
- c181fa46f1 speed 0.527 here
- f8beff72c9 speed 0.739 here
- 78f5dcfa21 speed 0.732 here
- 2d9da6e2a3 speed 1.036 here
- 236f438f62 speed 0.925 here
- 6d7a78ae47 speed 1.291 here
- a2a2b12cb9 speed 1.299 here
- d1eb81c577 speed 2.238 here
- c59afb99b9 speed 2.255 here
- 7cc76c82e3 speed 2.248 here
- b63c2031e1 speed 2.260 here
- b1ec80afdf speed 2.373 here
- 834db54e0b speed 2.366 here
- 782f3ad7ff speed 0.384 here
- 3eb59b271d speed 0.421 here
- c2ef9488ff speed 0.387 here
- ae99617f06 speed 0.527 here
- fb0d57c8a2 speed 0.997 here
- 64a7345393 speed 2.366 here
- 11a56ff9e4 speed 0.382 here

**240 designs measured on both: Spearman 0.986** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 240): 1 2 3 8 4 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| b3b4951ed2 (rejected) | 0.323 | 0.350 | 1.08 |
| e2746a2dc0 | 0.343 | 0.393 | 1.14 |
| 1993148bc2 | 0.378 | 0.439 | 1.16 |
| e5b7633b9d | 0.623 | 1.055 | 1.69 |
| cf9922a3ba | 0.631 | 1.071 | 1.70 |
| e365635532 (rejected) | 0.132 | 0.231 | 1.75 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 5 (e365635532, ba2d2f350d, b3b4951ed2, 4023705df2, ceeaacf723); than its fastest: 3 (e365635532, ba2d2f350d, b3b4951ed2).

Copied there: 23.9 MB in 0m 00s (103755 KB/s); mkdir 8 ms, start 8 ms; the connection 240 ms
10 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 3.08 on average, 110.53 at most, over 2295 samples 30 s apart, on 8 CPUs; at its start 10.77, the busiest then: ps 100%, sshd 25.4%, rsync 14.6%.
