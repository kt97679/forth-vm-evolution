# The checks of seed 84's front during seed 85 (Iteration 576)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-01 04:44 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.983** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 3 2 1 4 5 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 1bf867d374 | 0.773 | 0.999 | 1.29 |
| 3a412db1fc | 0.257 | 0.344 | 1.34 |
| 52f2a1481d | 0.473 | 0.651 | 1.38 |
| 5d04dbe696 | 0.156 | 0.273 | 1.75 |
| 89d296ffed | 0.133 | 0.236 | 1.77 |
| bf92c7003b | 0.142 | 0.253 | 1.78 |

Copied there: 12.6 MB in 0m 00s (83821 KB/s); mkdir 333 ms, start 156203 ms; the connection 345 ms
10 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 2.00 on average, 2.47 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.22, the busiest then: sshd 37.5%, sshd 7.8%, mysqld 0.8%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-01 04:46 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.938** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 3 4 2 1 5 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 439d9bbf9d (rejected) | 0.441 | 0.487 | 1.10 |
| 1bf867d374 | 0.773 | 0.870 | 1.13 |
| 8e0d21182b (rejected) | 0.201 | 0.257 | 1.28 |
| d105d778e2 | 0.145 | 0.272 | 1.87 |
| 7f1a388261 | 0.159 | 0.781 | 4.91 |
| 5d04dbe696 | 0.156 | 0.825 | 5.29 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 4 (15ecc6a232, 8e0d21182b, d31e410642, 439d9bbf9d); than its fastest: 0.

Copied there: 12.7 MB in 0m 00s (94561 KB/s); mkdir 10 ms, start 180348 ms; the connection 345 ms
10 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.37 on average, 1.66 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.66, the busiest then: ps 100%, mysqld 0.8%, tmux: 0.6%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-01 04:49 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.972** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 2 4 3 1 5 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 439d9bbf9d (rejected) | 0.441 | 0.499 | 1.13 |
| d31e410642 (rejected) | 0.317 | 0.380 | 1.20 |
| 1bf867d374 | 0.773 | 1.002 | 1.30 |
| 7f1a388261 | 0.159 | 0.283 | 1.78 |
| 89d296ffed | 0.133 | 0.237 | 1.79 |
| d105d778e2 | 0.145 | 0.261 | 1.80 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 2 (15ecc6a232, 8e0d21182b); than its fastest: 0.

Copied there: 12.7 MB in 0m 00s (95659 KB/s); mkdir 10 ms, start 173121 ms; the connection 345 ms
10 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.16 on average, 1.27 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.09, the busiest then: mysqld 0.8%, tmux: 0.6%, z_wr_iss 0.1%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-01 04:55 UTC, 2 round(s) a design.

Built where: 14 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 2 built here.

- 810e0f39a3 not measured: failed here: died: engine did not compile ((.text+0x8): undefined reference to `raise')
- 276d62fa7e not measured: failed here: died: engine did not compile ((.text+0x8): undefined reference to `raise')

**14 designs measured on both: Spearman 0.956** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 14): 1 3 2 5 4 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 607be5872f | 0.836 | 0.912 | 1.09 |
| 286c581e7e | 1.719 | 1.910 | 1.11 |
| 925948723f | 1.735 | 1.992 | 1.15 |
| a4aae22a83 | 0.314 | 0.477 | 1.52 |
| 0d2deace92 | 0.314 | 0.478 | 1.52 |
| 2a1e278348 | 0.312 | 0.484 | 1.55 |

**Rejected by the laptop's selection, measured here: 2** - faster here than the front's median: 1 (e22fc1afc8); than its fastest: 0.

Copied there: 12.4 MB in 0m 01s (8646 KB/s); mkdir 229 ms, start 1711227 ms; the connection 238 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.42 on average, 2.18 at most, over 57 samples 30 s apart, on 4 CPUs; at its start 0.30, the busiest then: ps 100%, sshd-session 88.0%, sh 28.5%.
