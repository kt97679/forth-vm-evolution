# The checks of seed 66's front during seed 67 - dream at three builds and the Tegra (Iteration 458)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-22 17:04 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.962** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 4 6 1 5 7 2.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 8f6d709709 | 0.395 | 0.453 | 1.15 |
| 25e8558784 | 0.275 | 0.363 | 1.32 |
| f2b5a02cdf | 0.167 | 0.235 | 1.41 |
| 8fcb6946e6 | 0.130 | 0.234 | 1.80 |
| 3531fb98c3 | 0.123 | 0.222 | 1.81 |
| 1a0e42d971 | 0.129 | 0.236 | 1.83 |

Copied there: 9.6 MB in 0m 00s (43100 KB/s); mkdir 288 ms, start 185627 ms; the connection 374 ms
17 ms
16 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.21 on average, 1.73 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 0.72, the busiest then: sshd 53.3%, sshd 7.6%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-22 17:07 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.833** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 9 11 10 7 13 3.

| design | laptop | here | here / laptop |
|---|---|---|---|
| da81f90540 (rejected) | 0.949 | 0.783 | 0.83 |
| ad742ac4b6 (rejected) | 0.697 | 0.669 | 0.96 |
| bc9e8dd5db | 0.389 | 0.473 | 1.22 |
| 25e8558784 | 0.275 | 0.592 | 2.15 |
| 5522733b46 | 0.267 | 0.588 | 2.20 |
| c98072e9a4 (rejected) | 0.268 | 0.593 | 2.21 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (c98072e9a4); than its fastest: 0.

Copied there: 9.7 MB in 0m 00s (83181 KB/s); mkdir 9 ms, start 220004 ms; the connection 374 ms
17 ms
16 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.19 on average, 1.31 at most, over 8 samples 30 s apart, on 8 CPUs; at its start 1.12, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-22 17:10 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.987** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 2 1 5 4 3 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| ad742ac4b6 (rejected) | 0.697 | 0.619 | 0.89 |
| da81f90540 (rejected) | 0.949 | 0.879 | 0.93 |
| df22df9c5d (rejected) | 0.492 | 0.529 | 1.08 |
| 5b13ea9a75 | 0.527 | 0.857 | 1.63 |
| 7020490a00 | 0.806 | 1.318 | 1.64 |
| 909df0d397 (rejected) | 1.174 | 2.009 | 1.71 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (c98072e9a4); than its fastest: 1 (c98072e9a4).

Copied there: 9.6 MB in 0m 00s (89048 KB/s); mkdir 9 ms, start 213228 ms; the connection 374 ms
17 ms
16 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.99 on average, 2.70 at most, over 8 samples 30 s apart, on 8 CPUs; at its start 1.10, the busiest then: ps 200%, chrome 2.0%, chrome 1.3%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.9; measured 2026-10-22 17:16 UTC, 2 round(s) a design.


**16 designs measured on both: Spearman 0.618** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 1 2 8 10 13 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| c3dbe10ac8 | 0.435 | 0.320 | 0.73 |
| 504e39f9e6 | 0.402 | 0.317 | 0.79 |
| 97a08041a1 | 0.411 | 0.326 | 0.79 |
| 25e8558784 | 0.275 | 0.320 | 1.16 |
| 3118e5a3a7 | 0.285 | 0.335 | 1.17 |
| 57a7b8ea11 | 0.276 | 0.326 | 1.18 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (c98072e9a4); than its fastest: 0.

Copied there: 9.3 MB in 0m 01s (7828 KB/s); mkdir 234 ms, start 2376246 ms; the connection 236 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.44 on average, 2.04 at most, over 80 samples 30 s apart, on 4 CPUs; at its start 0.28, the busiest then: ps 150%, sshd-session 86.5%, sh 28.5%.

