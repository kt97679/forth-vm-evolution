# The checks of seed 80's front during seed 81 (Iteration 568)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-29 18:34 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.891** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 4 5 7 8 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 100f13302e | 0.490 | 0.529 | 1.08 |
| 16315839c5 | 0.280 | 0.356 | 1.27 |
| 49ad8077a5 | 1.953 | 2.531 | 1.30 |
| 6f41a7ebc2 | 0.164 | 0.274 | 1.67 |
| a892ab68f1 | 0.161 | 0.270 | 1.68 |
| f9f7fd4b37 | 0.148 | 0.250 | 1.69 |

Copied there: 11.8 MB in 0m 00s (88151 KB/s); mkdir 244 ms, start 156484 ms; the connection 304 ms
9 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.73 on average, 2.39 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.70, the busiest then: sshd 30.0%, sshd 5.1%, mysqld 0.8%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-29 18:37 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.919** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 4 3 8 5 6 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 100f13302e | 0.490 | 0.488 | 1.00 |
| 49ad8077a5 | 1.953 | 1.950 | 1.00 |
| 19d543299b (rejected) | 0.436 | 0.451 | 1.03 |
| 9b71afe6d3 (rejected) | 0.143 | 0.247 | 1.73 |
| f9f7fd4b37 | 0.148 | 0.260 | 1.76 |
| 65a6fdd750 (rejected) | 0.249 | 0.680 | 2.73 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (9b71afe6d3); than its fastest: 0.

Copied there: 11.9 MB in 0m 00s (91192 KB/s); mkdir 9 ms, start 180036 ms; the connection 304 ms
9 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.26 on average, 1.58 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.58, the busiest then: mysqld 0.8%, tmux: 0.6%, z_wr_iss 0.1%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-29 18:40 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.928** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 3 1 4 6 7 9.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 19d543299b (rejected) | 0.436 | 0.450 | 1.03 |
| 4f47ac20a0 (rejected) | 0.660 | 0.692 | 1.05 |
| 100f13302e | 0.490 | 0.533 | 1.09 |
| f9f7fd4b37 | 0.148 | 0.249 | 1.68 |
| a892ab68f1 | 0.161 | 0.272 | 1.69 |
| 9b71afe6d3 (rejected) | 0.143 | 0.249 | 1.75 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (9b71afe6d3); than its fastest: 0.

Copied there: 11.9 MB in 0m 00s (90808 KB/s); mkdir 9 ms, start 174976 ms; the connection 304 ms
9 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.97 on average, 1.08 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.03, the busiest then: mysqld 0.8%, tmux: 0.6%, z_wr_iss 0.1%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-10-29 18:45 UTC, 2 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 16 of 16 built and measured here.

- 87d744cf61 speed 0.324 here
- b0ae9df364 speed 0.324 here
- 62a3270cb8 speed 0.377 here
- b5297e165e speed 0.388 here
- 0dc639bb04 speed 0.391 here
- d48399e6a6 speed 0.382 here
- 953bf22f85 speed 0.427 here
- d95af0f227 speed 0.390 here
- c125251bc4 speed 0.427 here
- 6d0cdfcfab speed 0.485 here
- d21be6bd69 speed 0.559 here
- 25e62c1eae speed 0.561 here
- 0a316ae645 speed 0.701 here
- fada1c70f9 speed 0.652 here
- 16b1c59b88 speed 0.714 here
- dc9608f0ff speed 0.699 here

Too few measured to rank (0).

Copied there: 11.5 MB in 0m 01s (9105 KB/s); mkdir 225 ms, start 1829816 ms; the connection 228 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.40 on average, 2.26 at most, over 61 samples 30 s apart, on 4 CPUs; at its start 0.34, the busiest then: ps 200%, sshd-session 87.8%, sh 33.3%.
