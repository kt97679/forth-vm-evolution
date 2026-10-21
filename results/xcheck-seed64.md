# The checks of seed 63's front during seed 64 - dream at three builds and the Tegra (Iteration 443)

Seed 63's front, sampled, and its rejected designs. Spearman against the laptop's 64-bit speeds: dream 0.707 (default
build, 24), 0.946 (64-bit, 30), at 32 bits 0.753 (30); the Tegra 0.771 (16). Against the laptop's own 32-bit speeds:
dream 0.612 (24), the Tegra 0.629 (12). Rejected by the laptop's selection and faster than the front's median on every
host: cf524f4c20 - first across the machine classes too (review-checks.py generic: mean 0.409, then seed 63's front's
e2faacbf03 0.412 and ec53b0ae91 0.413; six designs on all three).

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-21 03:22 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.707** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 2 15 5 14 12 9.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 542bcf7b64 | 0.393 | 0.405 | 1.03 |
| 1d7672eddb | 0.754 | 0.795 | 1.05 |
| 6377fc5ff3 | 0.325 | 0.371 | 1.14 |
| b7bf01702c | 1.514 | 2.464 | 1.63 |
| 68d140aa3f | 1.614 | 2.630 | 1.63 |
| 53608880ce | 0.266 | 0.436 | 1.64 |

Copied there: 9.3 MB in 0m 00s (78358 KB/s); mkdir 370 ms, start 185534 ms; the connection 312 ms
13 ms
10 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.45 on average, 2.00 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.61, the busiest then: sshd 30.0%, sshd 10.0%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-21 03:25 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.753** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 10 12 9 11 13 14.

| design | laptop | here | here / laptop |
|---|---|---|---|
| be61b8af8b (rejected) | 1.067 | 0.937 | 0.88 |
| 8b026536c2 | 0.441 | 0.461 | 1.05 |
| 6c1eff34d6 (rejected) | 1.306 | 1.420 | 1.09 |
| cf524f4c20 (rejected) | 0.263 | 0.610 | 2.32 |
| ec53b0ae91 | 0.263 | 0.616 | 2.34 |
| 28149c3629 (rejected) | 0.496 | 1.221 | 2.46 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (cf524f4c20); than its fastest: 0.

Copied there: 9.4 MB in 0m 00s (88563 KB/s); mkdir 8 ms, start 210760 ms; the connection 312 ms
13 ms
10 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.02 on average, 1.10 at most, over 8 samples 30 s apart, on 8 CPUs; at its start 1.10, the busiest then: ps 200%, chrome 2.0%, chrome 1.3%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-21 03:28 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.946** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 2 4 3 6 8 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| be61b8af8b (rejected) | 1.067 | 0.917 | 0.86 |
| 83bf1f7ae4 (rejected) | 0.802 | 0.816 | 1.02 |
| 28149c3629 (rejected) | 0.496 | 0.529 | 1.07 |
| b7bf01702c | 1.514 | 2.364 | 1.56 |
| 3a2fbb384d | 0.583 | 0.941 | 1.61 |
| b36fe5f8dc | 0.274 | 0.445 | 1.62 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (cf524f4c20); than its fastest: 0.

Copied there: 9.3 MB in 0m 00s (87728 KB/s); mkdir 11 ms, start 203780 ms; the connection 312 ms
13 ms
10 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.11 on average, 1.40 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.00, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.8%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-21 03:34 UTC, 2 round(s) a design.


**16 designs measured on both: Spearman 0.771** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 4 6 8 2 5 3.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 8eac059d5f | 0.814 | 0.501 | 0.61 |
| c6240cbcf9 | 0.887 | 0.621 | 0.70 |
| af5040cd66 (rejected) | 0.429 | 0.349 | 0.81 |
| ec53b0ae91 | 0.263 | 0.303 | 1.15 |
| 1dcd3dbf4f (rejected) | 0.600 | 0.704 | 1.17 |
| 53608880ce | 0.266 | 0.318 | 1.19 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (cf524f4c20); than its fastest: 0.

Copied there: 9.0 MB in 0m 01s (7080 KB/s); mkdir 227 ms, start 2409028 ms; the connection 234 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.40 on average, 2.05 at most, over 81 samples 30 s apart, on 4 CPUs; at its start 0.71, the busiest then: ps 300%, sshd-session 86.0%, sh 28.5%.

