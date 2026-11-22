## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-22 00:10 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 13 of 13 built and measured here.

- 15eda54ebd speed 0.253 here
- fa38596098 speed 0.247 here
- c6f1c1331b speed 0.249 here
- 08578f5e3d speed 0.259 here
- 59a1461f03 speed 0.265 here
- 50e56fd555 speed 0.288 here
- 26f776db8a speed 0.267 here
- 4c0bcc453e speed 0.268 here
- d7e6b28bb7 speed 0.269 here
- 3a5d7735b0 speed 0.267 here
- 893d4cb050 speed 0.260 here
- 70124be7f5 speed 0.262 here
- f13b982631 speed 0.259 here

**21 designs measured on both: Spearman 0.858** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 21): 1 2 3 8 4 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 3725269582 (rejected) | 0.374 | 0.430 | 1.15 |
| 9ee2cb3eb9 (rejected) | 0.174 | 0.205 | 1.18 |
| f1c42d8039 (rejected) | 0.277 | 0.350 | 1.27 |
| 13a2b38e1b | 0.179 | 0.251 | 1.40 |
| cee5764284 (rejected) | 0.679 | 1.072 | 1.58 |
| 792d7976b8 (rejected) | 0.120 | 0.202 | 1.69 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 2 (792d7976b8, 9ee2cb3eb9); than its fastest: 2 (792d7976b8, 9ee2cb3eb9).

Copied there: 31.9 MB in 0m 00s (82155 KB/s); mkdir 9 ms, start 12 ms; the connection 265 ms
9 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.66 on average, 5.13 at most, over 199 samples 30 s apart, on 8 CPUs; at its start 0.55, the busiest then: git 102%, chrome 50.0%, sshd 42.0%.
