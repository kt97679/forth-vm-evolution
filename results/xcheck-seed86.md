# The checks of seed 85's front during seed 86 (Iteration 582)

**The fast-end file's 41 on dream** (asked for by id at both widths, 576; results/drafts/dream41-582.py): seed 84's best bred design against the best of the rest - **-0.6% at 64 bits** (229dc9804a 0.2245, the pool's 0cc1db4424 0.2231), **+0.2% at 32 bits** (c7c35f9c97 0.2244, the pool's 52648fcf2f 0.2250), the bar 2%; the group medians 0.2349 bred, 0.2367 the rest at 64 bits. The laptop's re-measure had the bred lead at 5.9% idle (576): the lead is the laptop's, not the designs' - on dream the fast end is a band, as across machines before (results/drafts/xcheck-agreement-546.md).

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-01 16:10 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.983** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 3 2 5 4 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| be09b611aa | 0.943 | 0.839 | 0.89 |
| c927e10de3 | 1.060 | 0.951 | 0.90 |
| a4a66eb6b5 | 0.790 | 0.724 | 0.92 |
| 399956162e | 1.018 | 1.491 | 1.46 |
| 2fa8591306 | 0.838 | 1.227 | 1.46 |
| a4c51f9ae4 | 1.380 | 2.049 | 1.48 |

Copied there: 12.6 MB in 0m 00s (93025 KB/s); mkdir 280 ms, start 152418 ms; the connection 331 ms
15 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.97 on average, 1.22 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.06, the busiest then: sshd 23.8%, sshd 6.9%, mysqld 0.8%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-01 16:12 UTC, 3 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 41 of 41 built and measured here.

- d701cad70b speed 0.232 here
- 15ecc6a232 speed 0.230 here
- c7c35f9c97 speed 0.224 here
- 4df5b46d00 speed 0.229 here
- 45efec9d25 speed 0.228 here
- a52904d3eb speed 0.231 here
- 332d4a8da1 speed 0.234 here
- 8ef0975d7c speed 0.234 here
- 89d296ffed speed 0.229 here
- c653192faf speed 0.236 here
- 984e656c7e speed 0.232 here
- 89c05507c1 speed 0.229 here
- 23b6a752aa speed 0.233 here
- ab224f77a3 speed 0.232 here
- 2a4a5fd55a speed 0.232 here
- b27ca531b3 speed 0.235 here
- 4b679ef996 speed 0.230 here
- 89928b821a speed 0.233 here
- 2af9192e1d speed 0.228 here
- c5c93faf29 speed 0.232 here
- c121b4629d speed 0.232 here
- 9880e6f1ee speed 0.231 here
- 3152d3d441 speed 0.232 here
- 4c9c2d9075 speed 0.235 here
- ce8e9435b9 speed 0.228 here
- 70198fcef7 speed 0.230 here
- 96acd4dd94 speed 0.230 here
- 82f4ff7a02 speed 0.248 here
- 82bbc95daa speed 0.245 here
- 3d703cac0d speed 0.231 here
- 0cc2c03ff7 speed 0.231 here
- a4ee4a4d91 speed 0.244 here
- 1c4e3d9311 speed 0.251 here
- 457ba3e340 speed 0.245 here
- 0cc1db4424 speed 0.229 here
- 9a26b5a98d speed 0.230 here
- 8ad960343e speed 0.228 here
- e7b598f793 speed 0.230 here
- 229dc9804a speed 0.229 here
- caf5e5fa4d speed 0.227 here
- 52648fcf2f speed 0.225 here

**27 designs measured on both: Spearman 0.836** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 27): 1 14 15 2 3 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| c927e10de3 | 1.060 | 0.846 | 0.80 |
| a4a66eb6b5 | 0.790 | 0.662 | 0.84 |
| bc69973522 (rejected) | 1.343 | 1.132 | 0.84 |
| 0ac9d47ce7 | 0.587 | 0.932 | 1.59 |
| 13a5f33784 (rejected) | 0.386 | 0.864 | 2.24 |
| 173c99baa6 | 0.359 | 0.859 | 2.39 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 0; than its fastest: 0.

Copied there: 13.7 MB in 0m 00s (92706 KB/s); mkdir 10 ms, start 259235 ms; the connection 331 ms
15 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.73 on average, 2.71 at most, over 9 samples 30 s apart, on 8 CPUs; at its start 1.07, the busiest then: mysqld 0.8%, tmux: 0.6%, z_wr_iss 0.1%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-01 16:16 UTC, 3 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 41 of 41 built and measured here.

- d701cad70b speed 0.235 here
- 15ecc6a232 speed 0.229 here
- c7c35f9c97 speed 0.235 here
- 4df5b46d00 speed 0.236 here
- 45efec9d25 speed 0.235 here
- a52904d3eb speed 0.234 here
- 332d4a8da1 speed 0.231 here
- 8ef0975d7c speed 0.239 here
- 89d296ffed speed 0.236 here
- c653192faf speed 0.236 here
- 984e656c7e speed 0.236 here
- 89c05507c1 speed 0.235 here
- 23b6a752aa speed 0.233 here
- ab224f77a3 speed 0.237 here
- 2a4a5fd55a speed 0.232 here
- b27ca531b3 speed 0.238 here
- 4b679ef996 speed 0.234 here
- 89928b821a speed 0.236 here
- 2af9192e1d speed 0.235 here
- c5c93faf29 speed 0.232 here
- c121b4629d speed 0.237 here
- 9880e6f1ee speed 0.229 here
- 3152d3d441 speed 0.235 here
- 4c9c2d9075 speed 0.240 here
- ce8e9435b9 speed 0.236 here
- 70198fcef7 speed 0.236 here
- 96acd4dd94 speed 0.235 here
- 82f4ff7a02 speed 0.256 here
- 82bbc95daa speed 0.252 here
- 3d703cac0d speed 0.235 here
- 0cc2c03ff7 speed 0.237 here
- a4ee4a4d91 speed 0.245 here
- 1c4e3d9311 speed 0.254 here
- 457ba3e340 speed 0.240 here
- 0cc1db4424 speed 0.223 here
- 9a26b5a98d speed 0.229 here
- 8ad960343e speed 0.228 here
- e7b598f793 speed 0.235 here
- 229dc9804a speed 0.224 here
- caf5e5fa4d speed 0.229 here
- 52648fcf2f speed 0.237 here

**27 designs measured on both: Spearman 0.983** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 27): 1 3 6 2 5 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| be09b611aa | 0.943 | 0.816 | 0.86 |
| c927e10de3 | 1.060 | 0.955 | 0.90 |
| a4a66eb6b5 | 0.790 | 0.732 | 0.93 |
| 2fa8591306 | 0.838 | 1.200 | 1.43 |
| 399956162e | 1.018 | 1.473 | 1.45 |
| a4c51f9ae4 | 1.380 | 2.036 | 1.48 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (13a5f33784); than its fastest: 0.

Copied there: 13.7 MB in 0m 00s (91591 KB/s); mkdir 11 ms, start 243402 ms; the connection 331 ms
15 ms
13 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.33 on average, 1.74 at most, over 9 samples 30 s apart, on 8 CPUs; at its start 1.74, the busiest then: mysqld 0.8%, tmux: 0.6%, z_wr_iss 0.1%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.3.0-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.10; measured 2026-11-01 16:23 UTC, 2 round(s) a design.

Built where: 10 designs cross-built on the laptop (clang, ARMv7, no C library), shipped; s6 and the other 5 built here.

- 9e99fa8a5a not measured: failed here: died: engine did not compile ((.text+0x8): undefined reference to `raise')
- 129b78be56 not measured: failed here: died: engine did not compile ((.text+0x8): undefined reference to `raise')
- 0ac9d47ce7 not measured: failed here: died: engine did not compile ((.text+0x8): undefined reference to `raise')
- ceab169be8 not measured: failed here: died: engine did not compile ((.text+0x8): undefined reference to `raise')

**11 designs measured on both: Spearman 0.918** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 11): 1 2 3 5 6 7.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 9a89364262 | 1.982 | 1.507 | 0.76 |
| d7fa747b17 (rejected) | 1.204 | 1.076 | 0.89 |
| 609f90b24a (rejected) | 1.923 | 1.724 | 0.90 |
| 5530c31254 | 0.685 | 0.878 | 1.28 |
| f80f9b3012 (rejected) | 0.965 | 1.355 | 1.40 |
| be09b611aa | 0.943 | 1.324 | 1.40 |

**Rejected by the laptop's selection, measured here: 3** - faster here than the front's median: 2 (f80f9b3012, d7fa747b17); than its fastest: 0.

Copied there: 12.4 MB in 0m 01s (9046 KB/s); mkdir 224 ms, start 1654683 ms; the connection 219 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.44 on average, 1.95 at most, over 56 samples 30 s apart, on 4 CPUs; at its start 0.34, the busiest then: ps 200%, sshd-session 82.6%, sh 13.3%.
