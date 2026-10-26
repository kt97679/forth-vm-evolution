# The checks of seed 72's front during seed 73 - dream at three builds and the Tegra (Iteration 544)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-25 16:15 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.870** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 8 2 4 1 13 12.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 8db6ab33ae | 0.354 | 0.437 | 1.23 |
| 6d463f3d0e | 1.798 | 2.409 | 1.34 |
| 87d27bfc21 | 1.794 | 2.438 | 1.36 |
| c3a18bd60b | 0.148 | 0.253 | 1.71 |
| e057f6d356 | 0.151 | 0.259 | 1.71 |
| 84329899c3 | 0.150 | 0.259 | 1.73 |

Copied there: 10.4 MB in 0m 00s (67989 KB/s); mkdir 231 ms, start 155743 ms; the connection 392 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.21 on average, 1.64 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.28, the busiest then: sanoid 53.3%, syncoid 10.9%, sshd 9.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-25 16:18 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.931** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 6 4 2 1 3 9.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 854295ff0a (rejected) | 0.431 | 0.412 | 0.96 |
| 8057fcbd1a (rejected) | 0.807 | 0.795 | 0.98 |
| 35c940238d (rejected) | 1.798 | 1.850 | 1.03 |
| 214bd58881 | 0.152 | 0.266 | 1.75 |
| 8db6ab33ae | 0.354 | 0.654 | 1.85 |
| 4ebbe7de3b | 0.238 | 0.634 | 2.66 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (e1b2bc4b6a); than its fastest: 0.

Copied there: 10.5 MB in 0m 00s (93919 KB/s); mkdir 10 ms, start 179082 ms; the connection 392 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 2.09 on average, 2.79 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.46, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-25 16:21 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.893** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 9 7 2 1 8 14.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 854295ff0a (rejected) | 0.431 | 0.463 | 1.08 |
| 8057fcbd1a (rejected) | 0.807 | 1.001 | 1.24 |
| 8db6ab33ae | 0.354 | 0.447 | 1.26 |
| e057f6d356 | 0.151 | 0.258 | 1.71 |
| c3a18bd60b | 0.148 | 0.252 | 1.71 |
| 84329899c3 | 0.150 | 0.260 | 1.74 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (e1b2bc4b6a); than its fastest: 0.

Copied there: 10.5 MB in 0m 00s (89646 KB/s); mkdir 8 ms, start 173178 ms; the connection 392 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.29 on average, 1.68 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.68, the busiest then: ps 200%, chrome 2.0%, chrome 1.3%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.9; measured 2026-10-25 16:26 UTC, 2 round(s) a design.


**16 designs measured on both: Spearman 0.882** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 3 7 1 5 4 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| a825898fa1 | 0.719 | 0.486 | 0.68 |
| c3be728635 | 0.708 | 0.503 | 0.71 |
| db5b11366a | 0.743 | 0.545 | 0.73 |
| c61ef587e9 | 0.334 | 0.346 | 1.04 |
| f1909fb956 | 0.387 | 0.407 | 1.05 |
| 330089c50a | 0.335 | 0.354 | 1.06 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (861a7db793); than its fastest: 1 (861a7db793).

Copied there: 10.1 MB in 0m 01s (7598 KB/s); mkdir 236 ms, start 1814610 ms; the connection 229 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.41 on average, 2.15 at most, over 61 samples 30 s apart, on 4 CPUs; at its start 0.19, the busiest then: ps 300%, sshd-session 86.4%, sh 28.5%.
