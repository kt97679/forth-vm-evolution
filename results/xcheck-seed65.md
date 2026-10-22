# The checks of seed 64's front during seed 65 - dream at three builds and the Tegra (Iteration 449)

Seed 64's front, sampled, and its rejected designs. Spearman against the laptop's 64-bit speeds: dream 0.959 (default
build, 24), 0.937 (64-bit, 30), at 32 bits 0.837 (30); the Tegra 0.857 - over 7 only: of seed 64's front just 3 designs
are GCC without the JIT, the only kind the Tegra builds as itself (the owner, 429: it compiles for itself, GCC only).
Against the laptop's own 32-bit speeds: dream 0.912 (24). Across the machine classes, 2 designs on all three:
fff5759c3a (mean 0.420), d88784231e (0.447).

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-21 14:05 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.959** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 3 2 5 8 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 8af60764d5 | 0.381 | 0.408 | 1.07 |
| 7d8e645eab | 2.013 | 2.741 | 1.36 |
| 136fac9f05 | 1.907 | 2.602 | 1.36 |
| 9c51381240 | 0.130 | 0.221 | 1.70 |
| b8fa465fce | 0.145 | 0.250 | 1.72 |
| b69c45bae0 | 0.129 | 0.226 | 1.75 |

Copied there: 9.4 MB in 0m 00s (86817 KB/s); mkdir 287 ms, start 184776 ms; the connection 340 ms
18 ms
16 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.94 on average, 1.19 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 0.19, the busiest then: sshd 22.2%, sshd 9.7%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-21 14:09 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.837** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 9 10 12 11 1 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 92359aba70 | 0.507 | 0.499 | 0.98 |
| a70a6795c8 | 0.420 | 0.436 | 1.04 |
| d3b633c063 | 0.362 | 0.378 | 1.04 |
| a89c2863b8 | 1.674 | 2.656 | 1.59 |
| fff5759c3a | 0.339 | 0.609 | 1.80 |
| d88784231e | 0.340 | 0.634 | 1.87 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (313a1229e3); than its fastest: 0.

Copied there: 9.4 MB in 0m 00s (87719 KB/s); mkdir 9 ms, start 216876 ms; the connection 340 ms
18 ms
16 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.31 on average, 1.61 at most, over 8 samples 30 s apart, on 8 CPUs; at its start 0.94, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.8%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-21 14:12 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.937** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 1 2 3 5 4 12.

| design | laptop | here | here / laptop |
|---|---|---|---|
| d3b633c063 | 0.362 | 0.372 | 1.03 |
| 91d27b78ac | 0.355 | 0.372 | 1.05 |
| 92359aba70 | 0.507 | 0.534 | 1.05 |
| 3f59bdf05c | 1.681 | 2.763 | 1.64 |
| 2f8d0b04ea | 1.664 | 2.785 | 1.67 |
| 48c3bae5e6 | 0.870 | 1.596 | 1.83 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (313a1229e3); than its fastest: 0.

Copied there: 9.4 MB in 0m 00s (92067 KB/s); mkdir 8 ms, start 210033 ms; the connection 340 ms
18 ms
16 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 2.02 on average, 2.64 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.66, the busiest then: chrome 2.0%, chrome 1.3%, mysqld 0.8%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-21 14:18 UTC, 2 round(s) a design.


**7 designs measured on both: Spearman 0.857** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 7): 2 1 3 4 6 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| fff5759c3a | 0.339 | 0.292 | 0.86 |
| 0f0fda5c59 (rejected) | 0.337 | 0.296 | 0.88 |
| 2dda74437d | 0.360 | 0.333 | 0.92 |
| 1f15317ed6 (rejected) | 0.360 | 0.343 | 0.95 |
| 986ed6200f (rejected) | 0.356 | 0.341 | 0.96 |
| d88784231e | 0.340 | 0.332 | 0.98 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (0f0fda5c59); than its fastest: 0.

Copied there: 9.1 MB in 0m 01s (7805 KB/s); mkdir 237 ms, start 2003149 ms; the connection 233 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.39 on average, 1.91 at most, over 67 samples 30 s apart, on 4 CPUs; at its start 0.44, the busiest then: ps 100%, sshd-session 87.0%, sh 25.0%.

