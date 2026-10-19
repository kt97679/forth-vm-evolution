# The checks of seed 58's front during seed 59 - four machines, the first on the new remote path, with its probes (Iteration 398)

Seed 58's front - the first with plain-CV8 designs - on three hosts, and seed 58's rejected designs. Spearman against the laptop's 64-bit speeds: dream 0.959 (default build) and 0.963 (64-bit), at 32 bits 0.651, the Tegra 0.709 - the 32-bit hosts low because a two-encoding front ranks differently at 32 bits (seed 58's speed against its 32-bit speed, 0.573): the comparison should use the laptop's 32-bit speeds for them (HANDOFF open item 0g). No rejected design faster than the front's fastest on any host. The probes: copies of 8.2-8.6 MB in 0-1 s; the Tegra's 36 minutes its own start (the build), not the copy.

## dream.lan-prebuilt

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-18 15:42 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.959** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 4 3 5 2 11.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 094966e293 | 0.403 | 0.470 | 1.17 |
| 777933c13b | 0.252 | 0.318 | 1.26 |
| 08483c965c | 0.181 | 0.230 | 1.27 |
| cf3543fb49 | 0.125 | 0.217 | 1.73 |
| 1a3e559904 | 0.127 | 0.221 | 1.74 |
| fa5bfa2d2b | 0.123 | 0.220 | 1.79 |

Copied there: 8.6 MB in 0m 00s (68724 KB/s); mkdir 353 ms, start 175511 ms; the connection 281 ms
12 ms
9 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.36 on average, 1.74 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.17, the busiest then: ps 300%, sshd 20.8%, sshd 7.5%.

## dream.lan-prebuilt32

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-18 15:45 UTC, 3 round(s) a design.


**22 designs measured on both: Spearman 0.651** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 22): 12 5 8 10 11 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| b966d06523 | 0.467 | 0.564 | 1.21 |
| fd88248e34 (rejected) | 0.392 | 0.594 | 1.51 |
| 83ee8ab55b (rejected) | 0.427 | 0.656 | 1.54 |
| d55f05136f | 0.272 | 0.566 | 2.08 |
| ce937eca6d | 0.270 | 0.564 | 2.09 |
| fb73c9be4a (rejected) | 0.267 | 0.588 | 2.20 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (4007310884); than its fastest: 0.

Copied there: 8.6 MB in 0m 00s (87740 KB/s); mkdir 9 ms, start 165251 ms; the connection 281 ms
12 ms
9 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.14 on average, 1.33 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.33, the busiest then: zfs 100%, ps 100%, syncoid 28.5%.

## dream.lan-prebuilt64

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-18 15:48 UTC, 3 round(s) a design.


**22 designs measured on both: Spearman 0.963** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 22): 4 2 1 5 3 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 83ee8ab55b (rejected) | 0.427 | 0.395 | 0.92 |
| fd88248e34 (rejected) | 0.392 | 0.404 | 1.03 |
| ad56a8e0fd | 0.469 | 0.523 | 1.11 |
| 27c40503e0 | 0.297 | 0.389 | 1.31 |
| 4007310884 (rejected) | 0.331 | 0.434 | 1.31 |
| fb73c9be4a (rejected) | 0.267 | 0.360 | 1.35 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (fb73c9be4a); than its fastest: 0.

Copied there: 8.5 MB in 0m 00s (76721 KB/s); mkdir 9 ms, start 159555 ms; the connection 281 ms
12 ms
9 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.19 on average, 1.44 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 1.06, the busiest then: chrome 2.0%, chrome 1.4%, mysqld 0.8%.

## rage.lan-native

### rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.2.11-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-18 15:53 UTC, 2 round(s) a design.

- ce937eca6d not measured: failed here: died: engine did not compile (collect2: error: ld returned 1 exit status)
- d55f05136f not measured: failed here: died: engine did not compile (collect2: error: ld returned 1 exit status)
- 2ad3508c5e not measured: failed here: died: engine did not compile (collect2: error: ld returned 1 exit status)
- c47b567e8e not measured: failed here: died: engine did not compile (collect2: error: ld returned 1 exit status)
- fb73c9be4a not measured: failed here: died: engine did not compile (collect2: error: ld returned 1 exit status)

**11 designs measured on both: Spearman 0.709** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 11): 3 2 1 7 4 9.

| design | laptop | here | here / laptop |
|---|---|---|---|
| a1c67c0049 (rejected) | 0.403 | 0.349 | 0.86 |
| ad56a8e0fd | 0.469 | 0.464 | 0.99 |
| 11e5884401 | 0.465 | 0.462 | 0.99 |
| 30b5c561ec | 0.435 | 0.484 | 1.11 |
| 3f3e7b6891 (rejected) | 0.469 | 0.613 | 1.31 |
| 6542016144 (rejected) | 0.351 | 0.470 | 1.34 |

**Rejected by the laptop's selection, measured here: 3** - faster here than the front's median: 1 (a1c67c0049); than its fastest: 0.

Copied there: 8.2 MB in 0m 01s (7219 KB/s); mkdir 231 ms, start 2158189 ms; the connection 244 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.44 on average, 1.85 at most, over 72 samples 30 s apart, on 4 CPUs; at its start 0.40, the busiest then: ps 400%, sshd-session 83.8%, byobu-status 40.9%.

