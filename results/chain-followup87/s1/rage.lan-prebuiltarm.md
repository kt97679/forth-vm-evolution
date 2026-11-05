## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.1-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-05 05:13 UTC, 10 round(s) a design.

Built where: 30 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 19 built here.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 45 of 45 built and measured here.

- a2df4ef183 speed 0.337 here
- 62abdb2c64 speed 2.008 here
- 3d006a078e speed 0.508 here
- 9f8811f7f4 speed 0.334 here
- a627b954c6 speed 0.364 here
- 72dd720079 speed 0.415 here
- 58479dda0a speed 0.496 here
- 51ad64b5f0 speed 0.353 here
- 775c8d1e6d speed 0.500 here
- ce5bbc5dc2 speed 0.905 here
- 782f3ad7ff speed 0.370 here
- b04102ac63 speed 0.453 here
- 12c66adc50 speed 0.522 here
- bdfd4fb056 speed 0.531 here
- 213415ff71 speed 0.468 here
- bb247456e7 speed 0.833 here
- 2cf10b13df speed 1.205 here
- 716b31e9e2 speed 0.456 here
- 5f97d3e05d speed 0.506 here
- 350f21ecd0 speed 0.376 here
- 1f79736cf1 speed 0.471 here
- 79d85c8425 speed 0.509 here
- 17abb91f1f speed 0.796 here
- 64a7345393 speed 1.833 here
- 16df2da615 speed 0.580 here
- 05dfa902ed speed 0.467 here
- b35ae710e6 speed 0.341 here
- 7abedb242d speed 0.910 here
- 0d66d2e102 speed 0.482 here
- ac202587ad speed 0.527 here
- 8cc7f60d6b speed 0.391 here
- cea114f47e speed 1.974 here
- fb0d57c8a2 speed 0.517 here
- 1f2e71902c speed 0.456 here
- 22420b3b61 speed 0.360 here
- e6ca8a928f speed 0.500 here
- dea923f5a8 speed 0.348 here
- 2a8401f193 speed 1.005 here
- 7aa49309c5 speed 0.504 here
- 491139cdbc speed 0.521 here
- f55cec5849 speed 0.391 here
- 5c0e405cec speed 0.402 here
- 3452cb633b speed 0.328 here
- 690981ca5b speed 0.330 here
- c2ef9488ff speed 0.476 here

**4 designs measured on both: Spearman 1.000** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 2 3 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 53ad3af969 (rejected) | 0.457 | 0.458 | 1.00 |
| f575d014d6 (rejected) | 0.797 | 0.866 | 1.09 |
| 6913bb131f (rejected) | 1.696 | 1.959 | 1.16 |
| f575d014d6 (rejected) | 0.797 | 0.866 | 1.09 |
| 6913bb131f (rejected) | 1.696 | 1.959 | 1.16 |
| 77b0a0d48d (rejected) | 0.295 | 0.382 | 1.29 |

Copied there: 16.6 MB in 0m 01s (12173 KB/s); mkdir 227 ms, start 23 ms; the connection 227 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.41 on average, 2.87 at most, over 1511 samples 30 s apart, on 4 CPUs; at its start 0.25, the busiest then: ps 200%, sshd-session 88.7%, sh 16.6%.
