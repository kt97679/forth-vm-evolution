# The checks of seed 68's front during seed 69 - dream at three builds and the Tegra (Iteration 487)

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-23 15:03 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.963** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 4 5 2 1 8 3.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 7004d07819 | 0.326 | 0.368 | 1.13 |
| 4a9adab62b | 1.411 | 1.869 | 1.32 |
| f60c2153d6 | 0.187 | 0.250 | 1.34 |
| bf214b65e1 | 0.132 | 0.221 | 1.68 |
| 7aff831e61 | 0.134 | 0.226 | 1.69 |
| f2fc53c206 | 0.143 | 0.243 | 1.70 |

Copied there: 9.7 MB in 0m 00s (40081 KB/s); mkdir 351 ms, start 142254 ms; the connection 372 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.75 on average, 0.98 at most, over 5 samples 30 s apart, on 8 CPUs; at its start 0.05, the busiest then: sshd 57.5%, sshd 6.5%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-23 15:05 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.862** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 9 6 8 12 13 15.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 4c3d3d38b8 (rejected) | 1.076 | 0.930 | 0.86 |
| 8bc012b954 (rejected) | 0.855 | 0.750 | 0.88 |
| 9eabd766b5 | 0.355 | 0.366 | 1.03 |
| 7fab9d311d | 1.062 | 1.736 | 1.63 |
| bccdee5462 | 0.341 | 0.643 | 1.89 |
| fc12506f33 | 0.348 | 0.678 | 1.95 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 2 (3fb01e86c0, 8e364f42dd); than its fastest: 0.

Copied there: 9.8 MB in 0m 00s (90118 KB/s); mkdir 9 ms, start 169341 ms; the connection 372 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.39 on average, 2.27 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.99, the busiest then: ps 200%, chrome 2.0%, chrome 1.3%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-23 15:08 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.863** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 14 10 12 9 6 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 4c3d3d38b8 (rejected) | 1.076 | 1.020 | 0.95 |
| 8bc012b954 (rejected) | 0.855 | 0.821 | 0.96 |
| 9584abd328 | 0.368 | 0.401 | 1.09 |
| 00f0b92df6 | 1.569 | 2.522 | 1.61 |
| d2a947b73f | 1.077 | 1.750 | 1.63 |
| 7fab9d311d | 1.062 | 1.764 | 1.66 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (3fb01e86c0); than its fastest: 0.

Copied there: 9.7 MB in 0m 00s (88632 KB/s); mkdir 9 ms, start 163473 ms; the connection 372 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.99 on average, 2.76 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 2.76, the busiest then: ps 200%, chrome 2.0%, chrome 1.3%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.9; measured 2026-10-23 15:13 UTC, 2 round(s) a design.


**16 designs measured on both: Spearman 0.965** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 3 1 4 2 5 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 3f618e5bcf | 0.804 | 0.507 | 0.63 |
| 615615eb9e | 0.853 | 0.550 | 0.65 |
| 49392a2fb3 | 0.788 | 0.514 | 0.65 |
| bccdee5462 | 0.341 | 0.337 | 0.99 |
| 2784d8e2fc (rejected) | 0.338 | 0.360 | 1.06 |
| fc12506f33 | 0.348 | 0.372 | 1.07 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (2784d8e2fc); than its fastest: 0.

Copied there: 9.4 MB in 0m 01s (7795 KB/s); mkdir 234 ms, start 1728680 ms; the connection 250 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.37 on average, 1.82 at most, over 58 samples 30 s apart, on 4 CPUs; at its start 0.27, the busiest then: ps 400%, sshd-session 86.7%, sh 14.2%.

---
