## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-09 21:47 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 5 of 5 built and measured here.

- 782f3ad7ff speed 0.379 here
- c2ef9488ff speed 0.387 here
- ae99617f06 speed 0.519 here
- fb0d57c8a2 speed 1.003 here
- 64a7345393 speed 2.378 here

**8 designs measured on both: Spearman 0.905** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 8): 1 2 5 4 3 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 11a56ff9e4 | 0.333 | 0.378 | 1.14 |
| 3e13bd3c58 (rejected) | 0.451 | 0.521 | 1.15 |
| e11b4cbd12 (rejected) | 0.319 | 0.396 | 1.24 |
| 11658227de (rejected) | 1.869 | 2.563 | 1.37 |
| 0a0e767d85 (rejected) | 0.203 | 0.281 | 1.38 |
| 15ecc6a232 (rejected) | 0.131 | 0.221 | 1.69 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 3 (15ecc6a232, 0a0e767d85, e11b4cbd12); than its fastest: 2 (15ecc6a232, 0a0e767d85).

Copied there: 21.6 MB in 0m 00s (100366 KB/s); mkdir 11 ms, start 7 ms; the connection 548 ms
16 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 4.78 on average, 19.93 at most, over 125 samples 30 s apart, on 8 CPUs; at its start 1.93, the busiest then: sshd 40.2%, rsync 8.5%, chrome 8.2%.
