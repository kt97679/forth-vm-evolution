# The checks of seed 70's front during seed 71 - dream at three builds and the Tegra (Iteration 516)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-24 17:28 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.804** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 10 13 12 6 11.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 03f1f207e1 | 0.385 | 0.511 | 1.33 |
| d7fa0896db | 0.245 | 0.335 | 1.37 |
| ac976c9ad7 | 1.600 | 2.302 | 1.44 |
| 6bba82eff5 | 0.125 | 0.263 | 2.11 |
| 50c96dc10c | 0.125 | 0.266 | 2.13 |
| bf50a0e91f | 0.121 | 0.263 | 2.17 |

Copied there: 10.1 MB in 0m 00s (82693 KB/s); mkdir 345 ms, start 175075 ms; the connection 13 ms
8 ms
10 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.82 on average, 0.97 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.42, the busiest then: sshd 19.0%, sshd 10.4%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-24 17:31 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.969** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 2 1 3 4 7 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| b6e5f97c6f (rejected) | 1.021 | 0.931 | 0.91 |
| f5d32a48d7 (rejected) | 0.463 | 0.517 | 1.12 |
| 03f1f207e1 | 0.385 | 0.457 | 1.19 |
| bf50a0e91f | 0.121 | 0.195 | 1.62 |
| d7fa0896db | 0.245 | 0.756 | 3.09 |
| fcac7ef570 (rejected) | 0.259 | 0.965 | 3.73 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (f7670b67a3); than its fastest: 1 (f7670b67a3).

Copied there: 10.2 MB in 0m 00s (91010 KB/s); mkdir 8 ms, start 198714 ms; the connection 13 ms
8 ms
10 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.04 on average, 1.09 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 0.98, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-24 17:35 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.966** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 1 3 2 4 6 11.

| design | laptop | here | here / laptop |
|---|---|---|---|
| b6e5f97c6f (rejected) | 1.021 | 0.920 | 0.90 |
| f5d32a48d7 (rejected) | 0.463 | 0.560 | 1.21 |
| 03f1f207e1 | 0.385 | 0.507 | 1.32 |
| 77d42fd7da | 0.120 | 0.252 | 2.10 |
| bf50a0e91f | 0.121 | 0.255 | 2.10 |
| f7670b67a3 (rejected) | 0.121 | 0.255 | 2.11 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (f7670b67a3); than its fastest: 0.

Copied there: 10.2 MB in 0m 00s (91375 KB/s); mkdir 10 ms, start 192586 ms; the connection 13 ms
8 ms
10 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.62 on average, 2.08 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.03, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.9; measured 2026-10-24 17:40 UTC, 2 round(s) a design.


**7 designs measured on both: Spearman 0.607** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 7): 3 1 5 2 7 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 6625e6219e (rejected) | 0.336 | 0.328 | 0.98 |
| 32f5be4a31 | 0.323 | 0.323 | 1.00 |
| 51f42c1445 (rejected) | 0.327 | 0.328 | 1.00 |
| a3c7b9bffd | 0.336 | 0.354 | 1.05 |
| 555840b5cd | 0.325 | 0.345 | 1.06 |
| 12749c44e8 (rejected) | 0.331 | 0.369 | 1.11 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 3 (ff02daf2b5, 51f42c1445, 6625e6219e); than its fastest: 0.

Copied there: 9.7 MB in 0m 01s (7999 KB/s); mkdir 222 ms, start 1739458 ms; the connection 19 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.39 on average, 1.96 at most, over 58 samples 30 s apart, on 4 CPUs; at its start 0.22, the busiest then: ps 300%, sshd-session 84.7%, byobu-status 50.0%.

---
