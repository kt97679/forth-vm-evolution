## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-05 11:49 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 37 of 37 built and measured here.

- a2df4ef183 speed 0.426 here
- 62abdb2c64 speed 2.681 here
- 3d006a078e speed 1.084 here
- 9f8811f7f4 speed 0.424 here
- a627b954c6 speed 0.529 here
- 72dd720079 speed 0.412 here
- 58479dda0a speed 0.768 here
- 51ad64b5f0 speed 0.431 here
- 775c8d1e6d speed 0.471 here
- ce5bbc5dc2 speed 1.338 here
- 782f3ad7ff speed 0.386 here
- b04102ac63 speed 0.619 here
- 12c66adc50 speed 0.411 here
- bdfd4fb056 speed 0.976 here
- 213415ff71 speed 0.376 here
- bb247456e7 speed 0.993 here
- 2cf10b13df speed 1.570 here
- 716b31e9e2 speed 0.660 here
- 5f97d3e05d speed 0.489 here
- 350f21ecd0 speed 0.399 here
- 1f79736cf1 speed 0.417 here
- 79d85c8425 speed 0.828 here
- 17abb91f1f speed 0.969 here
- 64a7345393 speed 2.357 here
- 16df2da615 speed 0.519 here
- 05dfa902ed speed 0.376 here
- b35ae710e6 speed 0.427 here
- 7abedb242d speed 1.278 here
- 0d66d2e102 speed 0.397 here
- ac202587ad speed 0.434 here
- 8cc7f60d6b speed 0.386 here
- fb0d57c8a2 speed 1.010 here
- 1f2e71902c speed 0.368 here
- dea923f5a8 speed 0.454 here
- 7aa49309c5 speed 0.470 here
- f55cec5849 speed 0.405 here
- 3452cb633b speed 0.471 here

**14 designs measured on both: Spearman 0.996** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 14): 1 2 4 3 5 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| d64ea63dcc (rejected) | 0.316 | 0.398 | 1.26 |
| c2ef9488ff | 0.307 | 0.390 | 1.27 |
| 5c0e405cec | 0.306 | 0.394 | 1.29 |
| 2a8401f193 | 0.912 | 1.414 | 1.55 |
| cea114f47e | 1.570 | 2.476 | 1.58 |
| 15ecc6a232 (rejected) | 0.133 | 0.228 | 1.72 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 4 (15ecc6a232, e671547ec7, d64ea63dcc, 57b65bfd06); than its fastest: 2 (15ecc6a232, e671547ec7).

Copied there: 16.9 MB in 0m 00s (100357 KB/s); mkdir 8 ms, start 7 ms; the connection 286 ms
18 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.40 on average, 4.76 at most, over 1573 samples 30 s apart, on 8 CPUs; at its start 0.25, the busiest then: git 105%, sshd 41.0%, python3 25.0%.
