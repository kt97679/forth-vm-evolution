# The checks of seed 73's front during seed 74 - dream at three builds and the Tegra (Iteration 549)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-26 04:41 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.977** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 4 2 8 6 3.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 529f78461a | 0.260 | 0.320 | 1.23 |
| 4f741a36aa | 0.205 | 0.281 | 1.37 |
| b7aabd4006 | 0.356 | 0.507 | 1.43 |
| fc680274ba | 0.141 | 0.238 | 1.69 |
| 265d94e623 | 0.144 | 0.245 | 1.70 |
| 7c920bb9eb | 0.141 | 0.242 | 1.71 |

Copied there: 10.7 MB in 0m 00s (44927 KB/s); mkdir 298 ms, start 152600 ms; the connection 363 ms
14 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.35 on average, 2.36 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.07, the busiest then: sshd 53.1%, sshd 9.0%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-26 04:44 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.974** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 4 6 1 2 8 3.

| design | laptop | here | here / laptop |
|---|---|---|---|
| d63920ac9d (rejected) | 0.727 | 0.665 | 0.92 |
| 529f78461a | 0.260 | 0.306 | 1.18 |
| b7aabd4006 | 0.356 | 0.451 | 1.27 |
| 7c920bb9eb | 0.141 | 0.248 | 1.76 |
| ec5696a1d1 (rejected) | 0.500 | 0.884 | 1.77 |
| 4ce16885f4 (rejected) | 0.298 | 0.899 | 3.02 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (33b2e42c13); than its fastest: 0.

Copied there: 10.8 MB in 0m 00s (92178 KB/s); mkdir 9 ms, start 178525 ms; the connection 363 ms
14 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 2.30 on average, 3.02 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.80, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-26 04:47 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.984** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 1 2 8 6 4 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| ec5696a1d1 (rejected) | 0.500 | 0.492 | 0.98 |
| d63920ac9d (rejected) | 0.727 | 0.724 | 1.00 |
| 529f78461a | 0.260 | 0.323 | 1.24 |
| 4bc3da2b09 | 0.140 | 0.237 | 1.70 |
| b9c4407406 | 0.140 | 0.238 | 1.70 |
| 5ec10b8e4c (rejected) | 1.025 | 1.770 | 1.73 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (33b2e42c13); than its fastest: 0.

Copied there: 10.8 MB in 0m 00s (91093 KB/s); mkdir 9 ms, start 171960 ms; the connection 363 ms
14 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.25 on average, 1.47 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.47, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.9; measured 2026-10-26 04:52 UTC, 2 round(s) a design.


**16 designs measured on both: Spearman 0.856** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 1 5 2 4 8 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 3d584272c3 | 0.583 | 0.450 | 0.77 |
| 45ce1eaa22 | 0.624 | 0.495 | 0.79 |
| 611905d5b1 | 0.600 | 0.490 | 0.82 |
| 2422d16b4a | 0.399 | 0.416 | 1.04 |
| 4046c87a6c (rejected) | 0.447 | 0.491 | 1.10 |
| 88a49d2c19 (rejected) | 0.624 | 0.826 | 1.32 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (a66239fcbd); than its fastest: 1 (a66239fcbd).

Copied there: 10.3 MB in 0m 01s (7700 KB/s); mkdir 228 ms, start 1804217 ms; the connection 233 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.42 on average, 1.94 at most, over 61 samples 30 s apart, on 4 CPUs; at its start 0.27, the busiest then: ps 200%, sshd-session 89.7%, sh 40.0%.
