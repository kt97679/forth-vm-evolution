## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.1-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-09 21:15 UTC, 10 round(s) a design.

Built where: 6 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 5 built here.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 7 of 7 built and measured here.

- 11a56ff9e4 speed 0.482 here
- 782f3ad7ff speed 0.372 here
- 3eb59b271d speed 0.318 here
- c2ef9488ff speed 0.475 here
- ae99617f06 speed 0.351 here
- fb0d57c8a2 speed 0.521 here
- 64a7345393 speed 1.844 here

**4 designs measured on both: Spearman 1.000** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 2 3 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 02d689d8db (rejected) | 0.450 | 0.368 | 0.82 |
| 11658227de (rejected) | 1.869 | 1.967 | 1.05 |
| bf580f095d (rejected) | 0.843 | 0.933 | 1.11 |
| 11658227de (rejected) | 1.869 | 1.967 | 1.05 |
| bf580f095d (rejected) | 0.843 | 0.933 | 1.11 |
| 1ce4882d06 (rejected) | 0.277 | 0.319 | 1.15 |

Copied there: 21.5 MB in 0m 01s (13982 KB/s); mkdir 215 ms, start 24 ms; the connection 237 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.46 on average, 3.18 at most, over 175 samples 30 s apart, on 4 CPUs; at its start 0.51, the busiest then: ps 200%, sshd-session 61.9%, sh 2.6%.
