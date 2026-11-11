## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.3-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-10 23:07 UTC, 10 round(s) a design.

Built where: 25 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 16 built here.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 37 of 37 built and measured here.

- 3060f04651 speed 0.327 here
- 01712a2639 speed 1.886 here
- 22f7ad33b4 speed 0.512 here
- 6dbd01752e speed 0.367 here
- 88cdf38fbd speed 0.386 here
- c6d37f5da7 speed 0.476 here
- b311f84693 speed 0.354 here
- e92b45e100 speed 1.051 here
- 9f68e71820 speed 0.460 here
- d99a498d26 speed 0.325 here
- 782eff599d speed 0.776 here
- 65de387971 speed 0.495 here
- 5dcf9f7656 speed 0.445 here
- ac0c7e5cb3 speed 0.343 here
- bee66ec75c speed 0.496 here
- 965f48c803 speed 0.306 here
- a1c2fb2f99 speed 0.881 here
- 2e78669dc6 speed 0.562 here
- 66efe94609 speed 1.143 here
- 3da7de0a41 speed 0.474 here
- 444a9c62f5 speed 0.390 here
- 1cc775c214 speed 0.501 here
- 733b0afc1e speed 0.522 here
- 575263bf0e speed 1.722 here
- 8470be6ce5 speed 0.445 here
- b9bd589dd9 speed 0.464 here
- 60e1cba304 speed 0.797 here
- 2eb063e5fb speed 0.777 here
- 5adbc963d0 speed 0.489 here
- 012f4a0515 speed 0.437 here
- 782f3ad7ff speed 0.355 here
- 64a7345393 speed 1.783 here
- fb0d57c8a2 speed 0.503 here
- ae99617f06 speed 0.346 here
- 3eb59b271d speed 0.311 here
- 11a56ff9e4 speed 0.469 here
- c2ef9488ff speed 0.457 here

**4 designs measured on both: Spearman 0.800** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 3 2 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| c7e83c8b8f (rejected) | 0.806 | 0.527 | 0.65 |
| 062bb8e4ed (rejected) | 1.714 | 1.907 | 1.11 |
| 7fb40ff7ba (rejected) | 0.272 | 0.308 | 1.13 |
| 062bb8e4ed (rejected) | 1.714 | 1.907 | 1.11 |
| 7fb40ff7ba (rejected) | 0.272 | 0.308 | 1.13 |
| 1c0ce661f0 (rejected) | 0.441 | 0.611 | 1.38 |

Copied there: 22.9 MB in 0m 01s (13267 KB/s); mkdir 218 ms, start 26 ms; the connection 220 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.40 on average, 2.16 at most, over 1350 samples 30 s apart, on 4 CPUs; at its start 0.34, the busiest then: ps 300%, sshd-session 85.7%, byobu-status 64.2%.
