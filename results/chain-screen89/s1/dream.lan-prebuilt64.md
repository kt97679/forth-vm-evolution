## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-09 09:24 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 17 of 17 built and measured here.

- 3c5d6c64d8 speed 0.269 here
- 68a476fe49 speed 1.676 here
- bd0a0a725b speed 1.649 here
- d02a90b0dc speed 1.660 here
- bc7366289f speed 1.643 here
- ef92ebcbcd speed 1.647 here
- e2f3732d3f speed 1.662 here
- c7c35f9c97 speed 0.233 here
- ee34931cd7 speed 0.222 here
- 06b188f45b speed 0.225 here
- 782f3ad7ff speed 0.383 here
- c2ef9488ff speed 0.388 here
- a627b954c6 speed 0.533 here
- fb0d57c8a2 speed 1.052 here
- 64a7345393 speed 2.488 here
- 8164d3858f speed 0.527 here
- ae99617f06 speed 0.525 here

**280 designs measured on both: Spearman 0.992** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 280): 2 5 6 11 12 10.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 2ba58b1e45 | 0.316 | 0.334 | 1.06 |
| 59f4ae6aeb | 0.379 | 0.436 | 1.15 |
| 3e13bd3c58 (rejected) | 0.451 | 0.520 | 1.15 |
| 23a8ba850d | 0.143 | 0.250 | 1.75 |
| 15ecc6a232 (rejected) | 0.131 | 0.229 | 1.75 |
| a19dbb567c | 0.142 | 0.249 | 1.76 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 5 (15ecc6a232, 0a0e767d85, e11b4cbd12, 3e13bd3c58, 71e51f89f1); than its fastest: 0.

Copied there: 23.6 MB in 0m 00s (102951 KB/s); mkdir 13 ms, start 8 ms; the connection 417 ms
9 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 5.63 on average, 95.12 at most, over 2188 samples 30 s apart, on 8 CPUs; at its start 3.53, the busiest then: git 100%, sshd 33.3%, sshd 4.3%.
