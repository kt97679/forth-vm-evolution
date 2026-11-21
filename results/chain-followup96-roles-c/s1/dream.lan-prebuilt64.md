## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-21 17:54 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 62 of 62 built and measured here.

- e51c01ba10 speed 0.522 here
- 4acee9a48e speed 0.674 here
- 340c985752 speed 1.521 here
- 6e5c5bfe12 speed 1.260 here
- 08578f5e3d speed 0.259 here
- 15eda54ebd speed 0.253 here
- fa38596098 speed 0.250 here
- 0f11f28236 speed 1.651 here
- 3456fc28b2 speed 1.658 here
- 3a63ab4b58 speed 1.721 here
- 7086a9627c speed 1.645 here
- 0ce98ba0a7 speed 1.764 here
- 18415c8452 speed 1.758 here
- 19561ac49d speed 1.805 here
- 209f3df898 speed 1.758 here
- 29f34f8751 speed 1.770 here
- 2fa2a5db34 speed 1.752 here
- 3e0688d84d speed 1.760 here
- 54c559718f speed 1.774 here
- 55ef62d73f speed 1.847 here
- ba968f6f20 speed 1.754 here
- c6754d245d speed 1.788 here
- c8a7029bd7 speed 1.764 here
- ce43e57393 speed 1.754 here
- e48fe3eb29 speed 1.801 here
- e4f7158bb1 speed 1.758 here
- eb25ec3600 speed 1.756 here
- fbcb67ab0c speed 1.761 here
- fe15118862 speed 1.780 here
- ff4c4ebcdf speed 1.767 here
- d727605472 speed 0.352 here
- 5f7e66b12d speed 0.354 here
- a8d35bdccc speed 0.388 here
- 48a012411a speed 0.391 here
- 9b15ba26f7 speed 0.199 here
- 262a51bc6c speed 0.199 here
- df097ba2e2 speed 0.199 here
- ea782c6094 speed 0.207 here
- b5c79bff7e speed 0.204 here
- 69cebcaed9 speed 0.208 here
- 11f956db93 speed 0.208 here
- b525180392 speed 0.208 here
- 163935642a speed 0.218 here
- 219878ec89 speed 1.697 here
- 5cd995716d speed 1.599 here
- cdea6ab042 speed 1.657 here
- 71005d8a0d speed 0.685 here
- 16560cb51f speed 0.685 here
- 2c841d55e3 speed 0.895 here
- 5ff17f9000 speed 0.269 here
- 4ba25fac6c speed 0.258 here
- a6e8c448f0 speed 0.263 here
- 782f3ad7ff speed 0.365 here
- 3eb59b271d speed 0.402 here
- 11a56ff9e4 speed 0.381 here
- ae99617f06 speed 0.497 here
- fb0d57c8a2 speed 0.931 here
- d180351903 speed 2.232 here
- c7c35f9c97 speed 0.223 here
- ee34931cd7 speed 0.212 here
- 06b188f45b speed 0.218 here
- c6f1c1331b speed 0.250 here

**10 designs measured on both: Spearman 0.964** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 10): 1 2 3 4 5 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 3725269582 (rejected) | 0.374 | 0.435 | 1.16 |
| 90273721a1 | 1.234 | 1.586 | 1.28 |
| f1c42d8039 (rejected) | 0.277 | 0.357 | 1.29 |
| b4f9afac29 | 0.905 | 1.380 | 1.53 |
| cee5764284 (rejected) | 0.679 | 1.064 | 1.57 |
| 792d7976b8 (rejected) | 0.120 | 0.203 | 1.70 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 5 (792d7976b8, 9ee2cb3eb9, f1c42d8039, 3725269582, cee5764284); than its fastest: 2 (792d7976b8, 9ee2cb3eb9).

Copied there: 31.7 MB in 0m 00s (105881 KB/s); mkdir 8 ms, start 8 ms; the connection 256 ms
10 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.51 on average, 4.55 at most, over 654 samples 30 s apart, on 8 CPUs; at its start 0.53, the busiest then: git 106%, sshd 41.1%, chrome 2.5%.
