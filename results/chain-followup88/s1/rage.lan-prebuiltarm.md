## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.1-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-06 18:23 UTC, 10 round(s) a design.

Built where: 30 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 20 built here.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 46 of 46 built and measured here.

- c7814def6d speed 0.328 here
- 4dd4e3e7e2 speed 1.984 here
- 640feb6013 speed 0.554 here
- f3e832ef82 speed 0.361 here
- d47ab67a90 speed 0.408 here
- 0e192e15fc speed 0.511 here
- 8642898a7d speed 0.515 here
- 7055894eea speed 0.418 here
- 256d40aa3e speed 1.080 here
- a5d1c4e20f speed 0.547 here
- 328cec9957 speed 0.403 here
- f4f18ea197 speed 0.597 here
- a8ea0ad5b7 speed 0.465 here
- c7f47a0ca3 speed 0.593 here
- 8084d198fe speed 0.851 here
- 2eb106d7d7 speed 1.279 here
- a96deba5f8 speed 0.484 here
- 7d7de7c7dd speed 0.460 here
- 7a248231e7 speed 0.904 here
- 44ab9ee1b5 speed 0.483 here
- 2a14ceedec speed 0.801 here
- 291b405067 speed 0.458 here
- 142011c5b9 speed 0.546 here
- 2801917a1c speed 0.494 here
- 3d7fc45587 speed 0.576 here
- 422e922f9c speed 1.933 here
- baabf8b7f7 speed 0.557 here
- 196b735a2f speed 0.433 here
- 5508843670 speed 0.495 here
- 2511cc959e speed 0.516 here
- 782f3ad7ff speed 0.369 here
- 62abdb2c64 speed 2.028 here
- fb0d57c8a2 speed 0.524 here
- 9f8811f7f4 speed 0.333 here
- a627b954c6 speed 0.359 here
- 58479dda0a speed 0.496 here
- 12c66adc50 speed 0.520 here
- ce5bbc5dc2 speed 0.903 here
- bdfd4fb056 speed 0.529 here
- 51ad64b5f0 speed 0.346 here
- 350f21ecd0 speed 0.377 here
- 8cc7f60d6b speed 0.392 here
- 3452cb633b speed 0.328 here
- 690981ca5b speed 0.327 here
- c2ef9488ff speed 0.472 here
- 64a7345393 speed 1.837 here

**4 designs measured on both: Spearman 0.800** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 3 2 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 23c779dbee (rejected) | 0.806 | 0.511 | 0.63 |
| 4aae5e2eb3 (rejected) | 1.888 | 1.852 | 0.98 |
| c84a70f5df (rejected) | 0.436 | 0.516 | 1.18 |
| 4aae5e2eb3 (rejected) | 1.888 | 1.852 | 0.98 |
| c84a70f5df (rejected) | 0.436 | 0.516 | 1.18 |
| f2974c1a03 (rejected) | 0.283 | 0.355 | 1.26 |

Copied there: 18.1 MB in 0m 01s (12548 KB/s); mkdir 230 ms, start 21 ms; the connection 238 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.40 on average, 2.18 at most, over 950 samples 30 s apart, on 4 CPUs; at its start 0.21, the busiest then: ps 300%, sshd-session 88.0%, sh 16.6%.
