# The checks of seed 61's front during seed 62 - dream at three builds and the Tegra (Iteration 433)

Seed 61's front, sampled, and its rejected designs. Spearman against the laptop's 64-bit speeds: dream 0.943 (default
build, 24 designs), 0.958 (64-bit, 26), at 32 bits 0.945 (26); the Tegra (rage.lan) 0.847 (16, all built). Against the
laptop's own 32-bit speeds (`--laptop32`): dream 0.874 (21), the Tegra 0.867 (12). Rejected by the laptop's selection and
faster than the front's fastest on the Tegra: 2 (9019323181, 4d5b3d0e53); on dream none. Designs measured on all three
classes (review-checks.py generic): 5, all from the small end (means 1.455-1.548) - this chain ran from Iteration 425's
bundle, before the head to head (430) was asked for.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-20 04:03 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.943** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 8 2 3 4 1 9.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 37d5da9011 | 1.395 | 1.352 | 0.97 |
| 407c5aa793 | 1.376 | 1.341 | 0.97 |
| 510a838c68 | 1.353 | 1.329 | 0.98 |
| 3b63f32bb0 | 0.111 | 0.199 | 1.79 |
| 5c948b32f7 | 0.118 | 0.212 | 1.80 |
| 3cee75bc70 | 0.110 | 0.204 | 1.86 |

Copied there: 9.1 MB in 0m 00s (78175 KB/s); mkdir 241 ms, start 168851 ms; the connection 293 ms
20 ms
17 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.45 on average, 2.05 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.12, the busiest then: sshd 26.3%, sshd 5.2%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-20 04:06 UTC, 3 round(s) a design.


**26 designs measured on both: Spearman 0.945** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 26): 1 2 9 8 7 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 7d590862f8 (rejected) | 1.155 | 0.899 | 0.78 |
| 9be1148f72 (rejected) | 0.490 | 0.400 | 0.82 |
| 96237bd474 | 1.110 | 0.930 | 0.84 |
| 3a245e6d9d | 0.354 | 0.392 | 1.11 |
| 6970b60a7c | 0.339 | 0.377 | 1.11 |
| 2d6b4f3591 | 0.320 | 0.364 | 1.14 |

**Rejected by the laptop's selection, measured here: 5** - faster here than the front's median: 0; than its fastest: 0.

Copied there: 9.0 MB in 0m 00s (84797 KB/s); mkdir 9 ms, start 186245 ms; the connection 293 ms
20 ms
17 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.11 on average, 1.19 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.12, the busiest then: chrome 2.0%, chrome 1.4%, mysqld 0.8%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-20 04:09 UTC, 3 round(s) a design.


**26 designs measured on both: Spearman 0.958** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 26): 1 2 6 5 7 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 7d590862f8 (rejected) | 1.155 | 0.975 | 0.84 |
| 256c7757f0 (rejected) | 0.924 | 0.830 | 0.90 |
| 96237bd474 | 1.110 | 1.013 | 0.91 |
| a8824eeac3 | 0.323 | 0.364 | 1.13 |
| 2d6b4f3591 | 0.320 | 0.364 | 1.14 |
| 3a245e6d9d | 0.354 | 0.464 | 1.31 |

**Rejected by the laptop's selection, measured here: 5** - faster here than the front's median: 0; than its fastest: 0.

Copied there: 9.0 MB in 0m 00s (92647 KB/s); mkdir 9 ms, start 182332 ms; the connection 293 ms
20 ms
17 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.31 on average, 1.99 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.00, the busiest then: chrome 2.0%, chrome 1.4%, mysqld 0.8%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.2.11-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-20 04:15 UTC, 2 round(s) a design.


**16 designs measured on both: Spearman 0.847** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 1 2 8 3 7 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 5ef4f5b0b4 | 1.258 | 1.445 | 1.15 |
| e267052e86 (rejected) | 1.200 | 1.383 | 1.15 |
| 5d1868db2e | 1.157 | 1.398 | 1.21 |
| 407c5aa793 | 1.376 | 1.834 | 1.33 |
| 510a838c68 | 1.353 | 1.817 | 1.34 |
| 82cc7452f0 | 1.306 | 1.772 | 1.36 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 3 (9019323181, 4d5b3d0e53, e267052e86); than its fastest: 2 (9019323181, 4d5b3d0e53).

Copied there: 8.7 MB in 0m 01s (7390 KB/s); mkdir 238 ms, start 2540825 ms; the connection 233 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.46 on average, 2.13 at most, over 85 samples 30 s apart, on 4 CPUs; at its start 0.47, the busiest then: ps 300%, sshd-session 88.5%, sh 40.0%.

