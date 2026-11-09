pinned to cpu 1 (it and its sibling 6% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 7% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.344 | 0.339 | 0.987 | 0.346 | 0.360 | 0.351 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.303 | 0.293 | 0.967 | 0.309 | 0.316 | 0.310 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.324 | 0.325 | 1.001 | 0.322 | 0.331 | 0.330 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.327 | 0.323 | 0.988 | 0.377 | 0.375 | 0.364 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.386 | 0.374 | 0.968 | 0.405 | 0.412 | 0.408 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.826 | 0.827 | 1.001 | 0.767 | 0.764 | 0.753 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.575 | 1.573 | 0.998 | 1.624 | 1.592 | 1.621 |

{"id": "11a56ff9e4", "idle": 0.34359495868722695, "idle32": 0.3595580484213088, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.33905596132078075, "loaded32": 0.3507805407386772}
{"id": "782f3ad7ff", "idle": 0.302994560989945, "idle32": 0.3159080971498327, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.2930421144051475, "loaded32": 0.3101520021196708}
{"id": "3eb59b271d", "idle": 0.32433016183965563, "idle32": 0.3308674651907731, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3248014659528995, "loaded32": 0.329525070750254}
{"id": "c2ef9488ff", "idle": 0.3270441026977794, "idle32": 0.37545204594969367, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3232048117468554, "loaded32": 0.3641080816876934}
{"id": "ae99617f06", "idle": 0.385956848685053, "idle32": 0.4124333750645179, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.37379557087682536, "loaded32": 0.4083244727844992}
{"id": "fb0d57c8a2", "idle": 0.8261592119797198, "idle32": 0.7637358253411745, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8273045728196432, "loaded32": 0.7534302849525082}
{"id": "64a7345393", "idle": 1.5752439380597179, "idle32": 1.5921265254923018, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5725722076892, "loaded32": 1.6205430375540801}
- the asked group: loaded / idle, median 0.988 over 7 (range 0.967-1.001)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
