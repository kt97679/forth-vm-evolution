## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-147-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-11-22 00:42 UTC, 10 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 13 of 13 built and measured here.

- 15eda54ebd speed 0.255 here
- fa38596098 speed 0.248 here
- c6f1c1331b speed 0.251 here
- 08578f5e3d speed 0.258 here
- 59a1461f03 speed 0.267 here
- 50e56fd555 speed 0.287 here
- 26f776db8a speed 0.269 here
- 4c0bcc453e speed 0.272 here
- d7e6b28bb7 speed 0.269 here
- 3a5d7735b0 speed 0.267 here
- 893d4cb050 speed 0.259 here
- 70124be7f5 speed 0.263 here
- f13b982631 speed 0.261 here

**21 designs measured on both: Spearman 0.879** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 21): 1 2 3 6 4 5.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 3725269582 (rejected) | 0.374 | 0.431 | 1.15 |
| f1c42d8039 (rejected) | 0.277 | 0.346 | 1.25 |
| 1949ffd0cd | 0.205 | 0.267 | 1.30 |
| 13a2b38e1b | 0.179 | 0.251 | 1.40 |
| cee5764284 (rejected) | 0.679 | 1.064 | 1.57 |
| 792d7976b8 (rejected) | 0.120 | 0.204 | 1.70 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 2 (792d7976b8, 9ee2cb3eb9); than its fastest: 2 (792d7976b8, 9ee2cb3eb9).
