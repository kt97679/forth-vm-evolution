# The checks of seed 65's front during seed 66 - dream at three builds and the Tegra (Iteration 454)

Seed 65's front, sampled, and its rejected designs. Spearman against the laptop's 64-bit speeds: dream 0.963 (default
build, 24), 0.977 (64-bit, 30), at 32 bits 0.809 (30); the Tegra 0.818 (16). Against the laptop's own 32-bit speeds:
dream 0.818 (24). Rejected by the laptop's selection and faster than the front's median on every host: ad0975a72e.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-22 03:39 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.963** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 2 3 5 7 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| fa8d99dfab | 0.226 | 0.284 | 1.26 |
| 4ec1bef260 | 0.397 | 0.532 | 1.34 |
| 9403761024 | 1.713 | 2.647 | 1.55 |
| 3fa7829f6d | 0.118 | 0.214 | 1.81 |
| 00092dc6b0 | 0.117 | 0.213 | 1.82 |
| 85f5d1ae5e | 0.123 | 0.226 | 1.84 |

Copied there: 9.5 MB in 0m 00s (42807 KB/s); mkdir 380 ms, start 185743 ms; the connection 336 ms
17 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.40 on average, 1.70 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.48, the busiest then: sshd 53.3%, sshd 9.8%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-22 03:42 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.809** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 10 11 12 14 9 1.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 20f080d2f2 (rejected) | 0.686 | 0.666 | 0.97 |
| 5559074a8f (rejected) | 0.509 | 0.586 | 1.15 |
| f64c664738 (rejected) | 0.920 | 1.129 | 1.23 |
| d794e25ca6 | 0.309 | 0.650 | 2.10 |
| f403a4d547 | 0.305 | 0.644 | 2.11 |
| ad0975a72e (rejected) | 0.305 | 0.645 | 2.11 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 2 (ad0975a72e, 5559074a8f); than its fastest: 0.

Copied there: 9.6 MB in 0m 00s (85799 KB/s); mkdir 9 ms, start 218108 ms; the connection 336 ms
17 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.11 on average, 1.31 at most, over 8 samples 30 s apart, on 8 CPUs; at its start 1.14, the busiest then: ps 200%, chrome 2.0%, chrome 1.3%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-22 03:46 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.977** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 3 2 6 5 4 1.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 20f080d2f2 (rejected) | 0.686 | 0.630 | 0.92 |
| 5559074a8f (rejected) | 0.509 | 0.509 | 1.00 |
| 71328b8032 | 0.486 | 0.573 | 1.18 |
| 3721443712 | 1.679 | 2.723 | 1.62 |
| 69a41b2a93 | 1.645 | 2.709 | 1.65 |
| fa100c2257 | 0.609 | 1.011 | 1.66 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (ad0975a72e); than its fastest: 0.

Copied there: 9.5 MB in 0m 00s (88881 KB/s); mkdir 9 ms, start 212614 ms; the connection 336 ms
17 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.34 on average, 2.54 at most, over 8 samples 30 s apart, on 8 CPUs; at its start 0.96, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.8%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-22 03:52 UTC, 2 round(s) a design.


**16 designs measured on both: Spearman 0.818** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 6 4 7 1 3 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| f900823eb3 (rejected) | 0.820 | 0.530 | 0.65 |
| 71328b8032 | 0.486 | 0.371 | 0.76 |
| 269c05f27e | 0.820 | 0.650 | 0.79 |
| ad0975a72e (rejected) | 0.305 | 0.354 | 1.16 |
| ab16f60a0c | 0.304 | 0.353 | 1.16 |
| 550404fd3a (rejected) | 0.591 | 0.852 | 1.44 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (ad0975a72e); than its fastest: 0.

Copied there: 9.2 MB in 0m 01s (8362 KB/s); mkdir 234 ms, start 2387360 ms; the connection 237 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.43 on average, 2.04 at most, over 80 samples 30 s apart, on 4 CPUs; at its start 0.11, the busiest then: ps 300%, sshd-session 87.0%, sh 33.3%.

