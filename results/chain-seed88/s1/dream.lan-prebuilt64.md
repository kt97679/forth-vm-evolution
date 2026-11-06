## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-05 22:01 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 18 of 18 built and measured here.

- 690981ca5b speed 0.468 here
- f8b8fed677 speed 0.428 here
- 1d73264c94 speed 0.433 here
- 49859ccf95 speed 0.423 here
- 2ac7d6b132 speed 0.436 here
- 969d4ff708 speed 0.431 here
- 3965a85446 speed 0.424 here
- b0042fce56 speed 0.424 here
- 22aa39921b speed 0.432 here
- 6835b2e3d5 speed 0.426 here
- 0701dd4670 speed 0.437 here
- 64c534c502 speed 0.468 here
- 5b415caff7 speed 0.467 here
- 04ab053102 speed 0.462 here
- 41afedb8d0 speed 0.468 here
- 8e8d3b5f88 speed 0.472 here
- a91930f793 speed 0.467 here
- 8d0543a069 speed 0.480 here

**8 designs measured on both: Spearman 1.000** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 8): 1 2 3 4 5 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 137a7ddf4b (rejected) | 0.489 | 0.558 | 1.14 |
| ccb53f42aa (rejected) | 0.382 | 0.491 | 1.28 |
| 782f3ad7ff | 0.292 | 0.379 | 1.30 |
| a354dafbb6 (rejected) | 0.689 | 0.975 | 1.41 |
| 9f8811f7f4 | 0.296 | 0.424 | 1.43 |
| 534610b3e8 (rejected) | 1.002 | 1.529 | 1.53 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (f2974c1a03); than its fastest: 1 (f2974c1a03).

Copied there: 17.5 MB in 0m 00s (96847 KB/s); mkdir 14 ms, start 8 ms; the connection 285 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.40 on average, 2.96 at most, over 561 samples 30 s apart, on 8 CPUs; at its start 0.00, the busiest then: git 106%, sshd 31.9%, sshd 6.7%.
