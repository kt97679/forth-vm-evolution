# The checks of seed 60's front during seed 61 - dream at three builds and the Tegra (Iteration 425)

Seed 60's front, sampled, and its rejected designs. Spearman against the laptop's 64-bit speeds: dream 0.863 (default
build, 24 designs), 0.910 (64-bit, 20), at 32 bits 0.929 (20); the Tegra (rage.lan) 0.991 (16). Against the laptop's
own 32-bit speeds (`--laptop32`): dream 0.890 (14), the Tegra 0.881 (12). **The Tegra built all 16** - seed 60's
chain had six failures there, every one alignhot 32 or 64 (results/xcheck-seed60.md); none of seed 60's front carries
alignhot above 1, so this chain could not repeat them (Iteration 406's prediction 1: consistent, its failure half
untested). Rejected by the laptop's selection and faster here than the front's median: dream 4, the Tegra 3;
bf439eb307 faster than the front's fastest on both.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-19 16:37 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.863** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 6 9 2 8 10 12.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 503f4e44ea | 1.402 | 1.294 | 0.92 |
| 1a9b008ad1 | 1.377 | 1.289 | 0.94 |
| bf24feed43 | 0.828 | 0.792 | 0.96 |
| 4343c5771c | 0.116 | 0.213 | 1.84 |
| 5ee5c38165 | 0.111 | 0.211 | 1.90 |
| 1146d9fa20 | 0.112 | 0.213 | 1.91 |

Copied there: 8.9 MB in 0m 00s (34967 KB/s); mkdir 245 ms, start 168495 ms; the connection 254 ms
9 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.62 on average, 2.62 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.01, the busiest then: sshd 57.5%, sshd 3.9%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-19 16:40 UTC, 3 round(s) a design.


**20 designs measured on both: Spearman 0.929** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 20): 1 4 3 2 5 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 307a8f8ecd (rejected) | 1.197 | 0.969 | 0.81 |
| c185f742fd (rejected) | 1.099 | 1.004 | 0.91 |
| 8102d6d283 (rejected) | 1.426 | 1.363 | 0.96 |
| 16c7e1b047 | 0.612 | 0.708 | 1.16 |
| eb834617db | 0.611 | 0.715 | 1.17 |
| bf439eb307 (rejected) | 0.334 | 0.620 | 1.86 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 4 (bf439eb307, f6185cd2a7, c185f742fd, 307a8f8ecd); than its fastest: 1 (bf439eb307).

Copied there: 8.8 MB in 0m 00s (84315 KB/s); mkdir 10 ms, start 175300 ms; the connection 254 ms
9 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.41 on average, 1.97 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.97, the busiest then: ps 200%, chrome 2.0%, chrome 1.4%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-19 16:43 UTC, 3 round(s) a design.


**20 designs measured on both: Spearman 0.910** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 20): 1 2 3 4 5 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 307a8f8ecd (rejected) | 1.197 | 0.991 | 0.83 |
| cb2e5910e7 | 1.093 | 1.023 | 0.94 |
| 1a9b008ad1 | 1.377 | 1.296 | 0.94 |
| c185f742fd (rejected) | 1.099 | 1.221 | 1.11 |
| 99939e8917 (rejected) | 1.316 | 1.476 | 1.12 |
| 8102d6d283 (rejected) | 1.426 | 1.665 | 1.17 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 4 (bf439eb307, f6185cd2a7, c185f742fd, 307a8f8ecd); than its fastest: 1 (bf439eb307).

Copied there: 8.7 MB in 0m 00s (86032 KB/s); mkdir 8 ms, start 174090 ms; the connection 254 ms
9 ms
8 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.14 on average, 1.22 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.14, the busiest then: ps 100%, chrome 2.0%, chrome 1.4%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.2.11-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-19 16:49 UTC, 2 round(s) a design.


**16 designs measured on both: Spearman 0.991** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 1 2 3 4 6 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| cb2e5910e7 | 1.093 | 1.175 | 1.07 |
| 98d43300c7 (rejected) | 1.229 | 1.422 | 1.16 |
| 0381e89958 | 1.242 | 1.465 | 1.18 |
| 16c7e1b047 | 0.612 | 1.014 | 1.66 |
| eb834617db | 0.611 | 1.014 | 1.66 |
| 488a87d5e6 | 0.614 | 1.046 | 1.70 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 3 (bf439eb307, 2e98f5b7f4, 98d43300c7); than its fastest: 1 (bf439eb307).

Copied there: 8.6 MB in 0m 01s (7691 KB/s); mkdir 239 ms, start 2556394 ms; the connection 229 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.44 on average, 1.95 at most, over 86 samples 30 s apart, on 4 CPUs; at its start 0.23, the busiest then: ps 200%, sshd-session 86.5%, sh 33.3%.

