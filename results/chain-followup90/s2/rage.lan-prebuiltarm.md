## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.1-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-09 21:58 UTC, 10 round(s) a design.

Built where: 6 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 5 built here.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 7 of 7 built and measured here.

- 11a56ff9e4 speed 0.473 here
- 782f3ad7ff speed 0.370 here
- 3eb59b271d speed 0.323 here
- c2ef9488ff speed 0.476 here
- ae99617f06 speed 0.353 here
- fb0d57c8a2 speed 0.520 here
- 64a7345393 speed 1.833 here

**4 designs measured on both: Spearman 1.000** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 2 3 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 02d689d8db (rejected) | 0.450 | 0.372 | 0.83 |
| 11658227de (rejected) | 1.869 | 1.954 | 1.05 |
| bf580f095d (rejected) | 0.843 | 0.926 | 1.10 |
| 11658227de (rejected) | 1.869 | 1.954 | 1.05 |
| bf580f095d (rejected) | 0.843 | 0.926 | 1.10 |
| 1ce4882d06 (rejected) | 0.277 | 0.321 | 1.16 |
