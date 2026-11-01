# The checks of seed 83's front during seed 84 (Iteration 575)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-31 15:14 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.969** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 3 2 1 5 6 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 2146796c30 | 0.362 | 0.435 | 1.20 |
| 22b6f67cfd | 2.032 | 2.705 | 1.33 |
| e144638ec0 | 1.758 | 2.437 | 1.39 |
| 0709e03303 | 0.168 | 0.286 | 1.70 |
| 196d3cad36 | 0.161 | 0.275 | 1.71 |
| bce73d10ad | 0.146 | 0.250 | 1.71 |

Copied there: 12.3 MB in 0m 00s (80835 KB/s); mkdir 303 ms, start 158391 ms; the connection 258 ms
15 ms
15 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.72 on average, 1.01 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.15, the busiest then: sshd 30.4%, sshd 8.6%, mysqld 0.8%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-31 15:17 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.962** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 4 1 3 5 7 2.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 0fa744b1d5 (rejected) | 0.478 | 0.467 | 0.98 |
| 22b6f67cfd | 2.032 | 2.205 | 1.09 |
| 2146796c30 | 0.362 | 0.395 | 1.09 |
| 196d3cad36 | 0.161 | 0.634 | 3.94 |
| 0709e03303 | 0.168 | 0.685 | 4.08 |
| 93312d192e | 0.164 | 0.673 | 4.10 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 3 (c8c5c0f2f9, 73c34399b9, 0fa744b1d5); than its fastest: 0.

Copied there: 12.5 MB in 0m 00s (93096 KB/s); mkdir 9 ms, start 182071 ms; the connection 258 ms
15 ms
15 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.09 on average, 1.21 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.00, the busiest then: mysqld 0.8%, tmux: 0.6%, z_wr_iss 0.1%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-31 15:20 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.984** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 2 4 3 1 6 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| eafa905dfc (rejected) | 0.735 | 0.766 | 1.04 |
| 0fa744b1d5 (rejected) | 0.478 | 0.532 | 1.11 |
| 2146796c30 | 0.362 | 0.432 | 1.19 |
| 2b298b50fd | 0.148 | 0.251 | 1.69 |
| c8c5c0f2f9 (rejected) | 0.146 | 0.249 | 1.71 |
| bce73d10ad | 0.146 | 0.252 | 1.72 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (c8c5c0f2f9); than its fastest: 0.

Copied there: 12.4 MB in 0m 00s (90753 KB/s); mkdir 9 ms, start 175856 ms; the connection 258 ms
15 ms
15 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 2.14 on average, 2.75 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.14, the busiest then: mysqld 0.8%, tmux: 0.6%, z_wr_iss 0.1%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-10-31 15:29 UTC, 2 round(s) a design.

Built where: 15 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 1 built here.


**16 designs measured on both: Spearman 0.935** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 1 6 5 3 2 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 279f05cd30 (rejected) | 1.003 | 1.010 | 1.01 |
| 18c919b869 (rejected) | 0.657 | 0.666 | 1.01 |
| f3814ae606 (rejected) | 2.029 | 2.109 | 1.04 |
| 57d2827955 | 0.379 | 0.517 | 1.36 |
| dee5caf86d | 0.353 | 0.482 | 1.36 |
| 3b5e1162dd | 0.342 | 0.484 | 1.42 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (c18b204a6a); than its fastest: 1 (c18b204a6a).

Copied there: 12.1 MB in 0m 01s (8533 KB/s); mkdir 5973 ms, start 2411746 ms; the connection 231 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 4.33 on average, 6.89 at most, over 81 samples 30 s apart, on 4 CPUs; at its start 4.29, the busiest then: ps 200%, sshd-session 84.3%, sh 25.0%.
