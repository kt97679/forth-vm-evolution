# The checks of seed 67's front during seed 68 - dream at three builds and the Tegra (Iteration 464)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-23 06:18 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.966** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 3 2 4 5 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| a5213d8de3 | 0.385 | 0.426 | 1.11 |
| a71f0bcfc7 | 0.225 | 0.313 | 1.39 |
| c34219918d | 0.157 | 0.226 | 1.44 |
| 0ba1c3f26c | 0.124 | 0.218 | 1.76 |
| 9736a78e7d | 0.126 | 0.223 | 1.77 |
| d383f3f0aa | 0.126 | 0.227 | 1.80 |

Copied there: 9.7 MB in 0m 00s (73994 KB/s); mkdir 349 ms, start 143250 ms; the connection 370 ms
15 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.77 on average, 1.09 at most, over 5 samples 30 s apart, on 8 CPUs; at its start 0.21, the busiest then: sshd 30.0%, sshd 10.2%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-23 06:21 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.946** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 1 12 3 6 2 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| a55a293d22 | 0.418 | 0.425 | 1.02 |
| 87b43caa6c | 0.333 | 0.359 | 1.08 |
| d60771ec29 | 0.338 | 0.368 | 1.09 |
| 90fd01ecb3 | 1.617 | 2.456 | 1.52 |
| dc40a63044 | 0.646 | 0.986 | 1.53 |
| f0c116a3a1 | 0.916 | 1.469 | 1.60 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (09388bfb96); than its fastest: 0.

Copied there: 9.7 MB in 0m 00s (88395 KB/s); mkdir 9 ms, start 175315 ms; the connection 370 ms
15 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.08 on average, 1.22 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.04, the busiest then: ps 200%, chrome 2.0%, chrome 1.3%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-23 06:24 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.963** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 1 8 4 2 3 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 87b43caa6c | 0.333 | 0.360 | 1.08 |
| 5a47c41db3 | 0.330 | 0.358 | 1.09 |
| bc9e354c89 | 0.328 | 0.361 | 1.10 |
| f0c116a3a1 | 0.916 | 1.542 | 1.68 |
| c7531480ab | 1.674 | 2.830 | 1.69 |
| dc40a63044 | 0.646 | 1.103 | 1.71 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (09388bfb96); than its fastest: 0.

Copied there: 9.6 MB in 0m 00s (86205 KB/s); mkdir 9 ms, start 170485 ms; the connection 370 ms
15 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.86 on average, 2.65 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.98, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.9%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.9; measured 2026-10-23 06:29 UTC, 2 round(s) a design.


Too few measured to rank (0).

Copied there: 9.3 MB in 0m 01s (7577 KB/s); mkdir 250 ms, start 1082624 ms; the connection 232 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.47 on average, 2.15 at most, over 37 samples 30 s apart, on 4 CPUs; at its start 0.12, the busiest then: ps 300%, sshd-session 88.9%, sh 40.0%.

