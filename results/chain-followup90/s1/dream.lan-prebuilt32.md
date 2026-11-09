## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-09 21:14 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 7 of 7 built and measured here.

- 11a56ff9e4 speed 0.398 here
- 782f3ad7ff speed 0.339 here
- 3eb59b271d speed 0.549 here
- c2ef9488ff speed 0.402 here
- ae99617f06 speed 0.452 here
- fb0d57c8a2 speed 1.001 here
- 64a7345393 speed 2.118 here

**6 designs measured on both: Spearman 0.771** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 6): 1 4 3 2 5 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 3e13bd3c58 (rejected) | 0.451 | 0.438 | 0.97 |
| 71e51f89f1 (rejected) | 0.843 | 0.970 | 1.15 |
| 11658227de (rejected) | 1.869 | 2.356 | 1.26 |
| e11b4cbd12 (rejected) | 0.319 | 0.450 | 1.41 |
| 15ecc6a232 (rejected) | 0.131 | 0.227 | 1.74 |
| 0a0e767d85 (rejected) | 0.203 | 0.776 | 3.81 |

Copied there: 21.6 MB in 0m 00s (64886 KB/s); mkdir 338 ms, start 17 ms; the connection 548 ms
16 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 5.52 on average, 19.93 at most, over 66 samples 30 s apart, on 8 CPUs; at its start 1.93, the busiest then: ps 200%, sshd 46.6%, rsync 8.5%.
