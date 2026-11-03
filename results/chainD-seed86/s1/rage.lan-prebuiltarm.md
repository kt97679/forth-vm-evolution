## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.1-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-03 02:28 UTC, 10 round(s) a design.

Built where: 43 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 9 built here.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 48 of 48 built and measured here.

- 6d321be1cc speed 0.392 here
- 9920e9af07 speed 0.464 here
- 01efebca24 speed 0.400 here
- 97a4e37ab4 speed 0.469 here
- c67e6b5336 speed 0.404 here
- 8bddf3a5e4 speed 0.477 here
- 629b7e96ec speed 0.447 here
- 75acca89a6 speed 0.519 here
- 2af9192e1d speed 0.548 here
- bee0b97bb5 speed 1.966 here
- fb0d57c8a2 speed 0.524 here
- df890d7385 speed 0.543 here
- c2ef9488ff speed 0.474 here
- bac37f35a2 speed 0.546 here
- 22420b3b61 speed 0.365 here
- 9f70a06b4d speed 0.495 here
- bf25d58303 speed 0.555 here
- 690981ca5b speed 0.331 here
- 8ef0975d7c speed 0.531 here
- cea114f47e speed 1.981 here
- 5050960bac speed 0.530 here
- 4df5b46d00 speed 0.523 here
- c7c35f9c97 speed 0.538 here
- 89d296ffed speed 0.545 here
- 4ef851fd8e speed 0.512 here
- c13353f8cf speed 0.456 here
- e42b9f69e3 speed 0.542 here
- d6805a8b0a speed 0.545 here
- 6064084bb3 speed 0.532 here
- e7b598f793 speed 0.571 here
- 1e08254a4c speed 0.542 here
- be42bd8ea4 speed 0.461 here
- 45efec9d25 speed 0.544 here
- 6c6717b20a speed 0.461 here
- 51e6d4c661 speed 0.530 here
- 06b188f45b speed 0.465 here
- 5c1f5316db speed 0.527 here
- d9c6d38ce6 speed 0.483 here
- 66252391bb speed 0.529 here
- 3ee67e7d34 speed 0.459 here
- 4f39f9f341 speed 0.564 here
- d6b42c335a speed 0.536 here
- f4365761df speed 0.516 here
- 9a460d7122 speed 0.455 here
- 78e45e08f0 speed 0.542 here
- b0120bca4c speed 0.549 here
- bdfcf57297 speed 0.562 here
- 2c80490dc2 speed 0.554 here

**4 designs measured on both: Spearman 0.800** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 3 2 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| d7fa747b17 (rejected) | 1.204 | 1.058 | 0.88 |
| 609f90b24a (rejected) | 1.923 | 1.695 | 0.88 |
| ceab169be8 (rejected) | 0.448 | 0.517 | 1.15 |
| 609f90b24a (rejected) | 1.923 | 1.695 | 0.88 |
| ceab169be8 (rejected) | 0.448 | 0.517 | 1.15 |
| f80f9b3012 (rejected) | 0.965 | 1.367 | 1.42 |

Copied there: 13.9 MB in 0m 01s (10292 KB/s); mkdir 228 ms, start 20 ms; the connection 246 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.41 on average, 3.13 at most, over 1286 samples 30 s apart, on 4 CPUs; at its start 0.83, the busiest then: ps 300%, sshd-session 87.2%, sh 33.3%.
