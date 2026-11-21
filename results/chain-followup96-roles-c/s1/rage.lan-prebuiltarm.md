## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.5-gentoo-r1; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-21 15:10 UTC, 10 round(s) a design.

Built where: 36 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 2 built here.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 34 of 34 built and measured here.

- e51c01ba10 speed 0.551 here
- 4acee9a48e speed 0.445 here
- 340c985752 speed 1.155 here
- b4f9afac29 speed 1.039 here
- 6e5c5bfe12 speed 0.894 here
- 0f11f28236 speed 1.313 here
- 3456fc28b2 speed 1.288 here
- 3a63ab4b58 speed 1.293 here
- 7086a9627c speed 1.300 here
- 0ce98ba0a7 speed 1.285 here
- 18415c8452 speed 1.282 here
- 19561ac49d speed 1.279 here
- 209f3df898 speed 1.282 here
- 29f34f8751 speed 1.283 here
- 2fa2a5db34 speed 1.289 here
- 3e0688d84d speed 1.286 here
- 54c559718f speed 1.274 here
- 55ef62d73f speed 1.283 here
- ba968f6f20 speed 1.273 here
- c6754d245d speed 1.291 here
- c8a7029bd7 speed 1.294 here
- ce43e57393 speed 1.287 here
- e48fe3eb29 speed 1.283 here
- e4f7158bb1 speed 1.277 here
- eb25ec3600 speed 1.281 here
- fbcb67ab0c speed 1.280 here
- fe15118862 speed 1.283 here
- ff4c4ebcdf speed 1.278 here
- d727605472 speed 0.328 here
- 5f7e66b12d speed 0.325 here
- 219878ec89 speed 1.241 here
- 90273721a1 speed 1.237 here
- ae99617f06 speed 0.325 here
- d180351903 speed 1.734 here

**4 designs measured on both: Spearman 1.000** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 2 3 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 7e3d034731 (rejected) | 1.234 | 1.220 | 0.99 |
| 1463ab134c (rejected) | 0.266 | 0.339 | 1.28 |
| 9839870263 (rejected) | 0.698 | 0.898 | 1.29 |
| 1463ab134c (rejected) | 0.266 | 0.339 | 1.28 |
| 9839870263 (rejected) | 0.698 | 0.898 | 1.29 |
| 542f0327e5 (rejected) | 0.382 | 0.501 | 1.31 |

Copied there: 31.1 MB in 0m 02s (15358 KB/s); mkdir 290 ms, start 25 ms; the connection 401 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.69 on average, 8.09 at most, over 626 samples 30 s apart, on 4 CPUs; at its start 1.50, the busiest then: ps 150%, sshd-session 85.5%, bash 74.4%.
