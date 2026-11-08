## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-07 14:30 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 6 of 6 built and measured here.

- 782f3ad7ff speed 0.383 here
- 690981ca5b speed 0.468 here
- c2ef9488ff speed 0.387 here
- a627b954c6 speed 0.532 here
- fb0d57c8a2 speed 1.010 here
- 64a7345393 speed 2.363 here

**381 designs measured on both: Spearman 0.984** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 381): 2 1 4 3 6 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| c71dc8f0dc (rejected) | 0.467 | 0.538 | 1.15 |
| 907732f4cb | 0.419 | 0.485 | 1.16 |
| 4023705df2 | 0.458 | 0.532 | 1.16 |
| 48d076b4eb | 0.838 | 1.444 | 1.72 |
| 7623a4732c | 0.838 | 1.468 | 1.75 |
| 4434bc9c71 | 0.762 | 1.362 | 1.79 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 4 (8d636f5a9c, f238ccb5e2, c71dc8f0dc, 3360c35d4f); than its fastest: 0.

Copied there: 21.6 MB in 0m 00s (101629 KB/s); mkdir 9 ms, start 7 ms; the connection 387 ms
18 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.39 on average, 3.39 at most, over 2160 samples 30 s apart, on 8 CPUs; at its start 1.56, the busiest then: git 100%, sshd 40.5%, sshd 5.2%.
