# The checks of seed 71's front during seed 72 - dream at three builds and the Tegra (Iteration 520)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-25 06:05 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.958** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 3 2 5 8 7 1.

| design | laptop | here | here / laptop |
|---|---|---|---|
| d0739d5e95 | 0.221 | 0.298 | 1.35 |
| 365c304c59 | 0.317 | 0.444 | 1.40 |
| 995c41c0a3 | 1.733 | 2.430 | 1.40 |
| b0116306e3 | 0.143 | 0.250 | 1.75 |
| e116f28fdc | 0.143 | 0.250 | 1.75 |
| b5f7ea1727 | 0.157 | 0.282 | 1.79 |

Copied there: 10.3 MB in 0m 00s (43399 KB/s); mkdir 334 ms, start 153869 ms; the connection 321 ms
17 ms
15 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.67 on average, 2.31 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.17, the busiest then: sshd 56.2%, sshd 6.7%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-25 06:08 UTC, 3 round(s) a design.

- 7c97d9819e not measured: failed here: wrong output: apps

**29 designs measured on both: Spearman 0.956** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 29): 3 6 2 1 4 11.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 80a92f00da (rejected) | 1.733 | 1.815 | 1.05 |
| 9ecc4ef241 (rejected) | 1.059 | 1.150 | 1.09 |
| 7baf77008a (rejected) | 0.561 | 0.697 | 1.24 |
| f04abcceb5 | 0.141 | 0.261 | 1.85 |
| b0116306e3 | 0.143 | 0.265 | 1.85 |
| 365c304c59 | 0.317 | 0.963 | 3.04 |

**Rejected by the laptop's selection, measured here: 5** - faster here than the front's median: 1 (56f894d4d1); than its fastest: 0.

Copied there: 10.5 MB in 0m 00s (90045 KB/s); mkdir 9 ms, start 182257 ms; the connection 321 ms
17 ms
15 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.32 on average, 1.66 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.66, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-25 06:11 UTC, 3 round(s) a design.

- 7c97d9819e not measured: failed here: wrong output: apps

**29 designs measured on both: Spearman 0.955** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 29): 4 2 3 7 10 9.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 252d068e97 (rejected) | 0.331 | 0.393 | 1.19 |
| 7baf77008a (rejected) | 0.561 | 0.710 | 1.27 |
| 9ecc4ef241 (rejected) | 1.059 | 1.387 | 1.31 |
| f83a64a706 | 0.140 | 0.244 | 1.74 |
| e116f28fdc | 0.143 | 0.253 | 1.77 |
| b5f7ea1727 | 0.157 | 0.282 | 1.79 |

**Rejected by the laptop's selection, measured here: 5** - faster here than the front's median: 1 (56f894d4d1); than its fastest: 0.

Copied there: 10.4 MB in 0m 00s (82139 KB/s); mkdir 10 ms, start 174666 ms; the connection 321 ms
17 ms
15 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.30 on average, 1.65 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.15, the busiest then: sshd 23.5%, zfs 11.1%, z_metaslab 7.6%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.9; measured 2026-10-25 06:16 UTC, 2 round(s) a design.

- 074ff7a7af not measured: failed here: wrong output: apps
- 6dd20c052c not measured: failed here: wrong output: apps

**14 designs measured on both: Spearman 0.916** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 14): 4 3 5 2 1 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| ae67c6822a (rejected) | 0.556 | 0.432 | 0.78 |
| 327ccef340 | 0.486 | 0.391 | 0.81 |
| 4dd1bcd479 | 0.520 | 0.421 | 0.81 |
| 58094b8938 | 0.365 | 0.368 | 1.01 |
| 0c5e11160a | 0.348 | 0.356 | 1.02 |
| 4b07cbbe27 | 0.399 | 0.414 | 1.04 |

**Rejected by the laptop's selection, measured here: 3** - faster here than the front's median: 1 (4145d6e39c); than its fastest: 1 (4145d6e39c).

Copied there: 9.9 MB in 0m 01s (7776 KB/s); mkdir 227 ms, start 1806831 ms; the connection 232 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.40 on average, 1.90 at most, over 61 samples 30 s apart, on 4 CPUs; at its start 0.28, the busiest then: sshd-session 88.7%, sh 33.3%, sshd-session 2.4%.

---
