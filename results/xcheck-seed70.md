# The checks of seed 69's front during seed 70 - dream at three builds and the Tegra (Iteration 498)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-24 04:59 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.941** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 4 7 3 6 8 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| e4ce0affef | 0.573 | 0.586 | 1.02 |
| ce7223f3f2 | 0.314 | 0.384 | 1.22 |
| 831928544e | 0.223 | 0.278 | 1.25 |
| 81432d1877 | 0.116 | 0.212 | 1.83 |
| b7165de9ed | 0.113 | 0.208 | 1.84 |
| 1164a898ce | 0.115 | 0.213 | 1.85 |

Copied there: 10.0 MB in 0m 00s (42727 KB/s); mkdir 333 ms, start 143926 ms; the connection 359 ms
14 ms
11 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.62 on average, 0.92 at most, over 5 samples 30 s apart, on 8 CPUs; at its start 0.10, the busiest then: sshd 54.8%, sshd 7.0%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-24 05:02 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.935** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 3 6 4 7 1 10.

| design | laptop | here | here / laptop |
|---|---|---|---|
| e4ce0affef | 0.573 | 0.546 | 0.95 |
| bfb0c55a2c (rejected) | 1.820 | 2.033 | 1.12 |
| de278336ba (rejected) | 0.457 | 0.524 | 1.15 |
| 831928544e | 0.223 | 0.688 | 3.08 |
| 85a1dd71f7 | 0.179 | 0.612 | 3.42 |
| 67ef18152b | 0.137 | 0.636 | 4.64 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 2 (fe5c5498fd, de278336ba); than its fastest: 0.

Copied there: 10.1 MB in 0m 00s (87698 KB/s); mkdir 9 ms, start 169283 ms; the connection 359 ms
14 ms
11 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.73 on average, 2.35 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.95, the busiest then: ps 300%, chrome 2.0%, chrome 1.3%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-24 05:05 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.959** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 5 6 4 2 7 9.

| design | laptop | here | here / laptop |
|---|---|---|---|
| e4ce0affef | 0.573 | 0.597 | 1.04 |
| ce7223f3f2 | 0.314 | 0.383 | 1.22 |
| 831928544e | 0.223 | 0.278 | 1.25 |
| 22ec9bacda | 0.118 | 0.216 | 1.83 |
| fe5c5498fd (rejected) | 0.114 | 0.210 | 1.85 |
| b7165de9ed | 0.113 | 0.210 | 1.86 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (fe5c5498fd); than its fastest: 0.

Copied there: 10.1 MB in 0m 00s (86487 KB/s); mkdir 9 ms, start 161604 ms; the connection 359 ms
14 ms
11 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.59 on average, 1.93 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.93, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.9; measured 2026-10-24 05:10 UTC, 2 round(s) a design.


**8 designs measured on both: Spearman 0.929** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 8): 1 2 3 4 7 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 6a35579cb5 (rejected) | 0.384 | 0.316 | 0.82 |
| e778c57c15 (rejected) | 0.413 | 0.365 | 0.89 |
| 8400e812e1 | 0.309 | 0.285 | 0.92 |
| 48accb308a | 0.298 | 0.284 | 0.95 |
| 0cb9091ae7 (rejected) | 0.354 | 0.410 | 1.16 |
| b51f6881b0 | 0.413 | 0.512 | 1.24 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (a3d8d12c3a); than its fastest: 1 (a3d8d12c3a).

Copied there: 9.6 MB in 0m 01s (7886 KB/s); mkdir 242 ms, start 1408306 ms; the connection 228 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.41 on average, 2.01 at most, over 47 samples 30 s apart, on 4 CPUs; at its start 0.40, the busiest then: ps 200%, sshd-session 88.1%, sh 16.6%.

---
