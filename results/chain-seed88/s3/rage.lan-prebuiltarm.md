## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.1-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-05 21:57 UTC, 10 round(s) a design.

Built where: 5 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 19 built here.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 20 of 20 built and measured here.

- 9f8811f7f4 speed 0.336 here
- 690981ca5b speed 0.326 here
- 782f3ad7ff speed 0.369 here
- f8b8fed677 speed 0.332 here
- 1d73264c94 speed 0.342 here
- 49859ccf95 speed 0.344 here
- 2ac7d6b132 speed 0.329 here
- 969d4ff708 speed 0.335 here
- 3965a85446 speed 0.339 here
- b0042fce56 speed 0.335 here
- 22aa39921b speed 0.328 here
- 6835b2e3d5 speed 0.331 here
- 0701dd4670 speed 0.329 here
- 64c534c502 speed 0.330 here
- 5b415caff7 speed 0.329 here
- 04ab053102 speed 0.345 here
- 41afedb8d0 speed 0.332 here
- 8e8d3b5f88 speed 0.333 here
- a91930f793 speed 0.333 here
- 8d0543a069 speed 0.338 here

**4 designs measured on both: Spearman 0.800** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 3 2 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 23c779dbee (rejected) | 0.806 | 0.511 | 0.63 |
| 4aae5e2eb3 (rejected) | 1.888 | 1.850 | 0.98 |
| c84a70f5df (rejected) | 0.436 | 0.516 | 1.18 |
| 4aae5e2eb3 (rejected) | 1.888 | 1.850 | 0.98 |
| c84a70f5df (rejected) | 0.436 | 0.516 | 1.18 |
| f2974c1a03 (rejected) | 0.283 | 0.354 | 1.25 |
