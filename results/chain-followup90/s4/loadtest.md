pinned to cpu 8 (it and its sibling 2% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 0% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.352 | 0.341 | 0.969 | 0.346 | 0.371 | 0.359 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.307 | 0.298 | 0.969 | 0.309 | 0.328 | 0.314 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.340 | 0.326 | 0.959 | 0.322 | 0.349 | 0.336 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.336 | 0.320 | 0.952 | 0.377 | 0.387 | 0.365 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.388 | 0.379 | 0.977 | 0.405 | 0.415 | 0.421 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.827 | 0.826 | 0.999 | 0.767 | 0.769 | 0.772 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.561 | 1.571 | 1.007 | 1.624 | 1.603 | 1.613 |

{"id": "11a56ff9e4", "idle": 0.35215703774804025, "idle32": 0.3712635488136534, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3413741797848482, "loaded32": 0.3591182369579249}
{"id": "782f3ad7ff", "idle": 0.307062739449382, "idle32": 0.32816618918656365, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.2975055523520799, "loaded32": 0.31402992192844753}
{"id": "3eb59b271d", "idle": 0.34011924076972777, "idle32": 0.34858461356538556, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.32611335063238467, "loaded32": 0.3358237248596696}
{"id": "c2ef9488ff", "idle": 0.3361030870800388, "idle32": 0.3865271066993201, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3198226027001379, "loaded32": 0.36480108434046843}
{"id": "ae99617f06", "idle": 0.38833893616353066, "idle32": 0.4148768136753257, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.37943300556995285, "loaded32": 0.42089065630331324}
{"id": "fb0d57c8a2", "idle": 0.8269538774173679, "idle32": 0.769458962084485, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8262534776858954, "loaded32": 0.7720210964292287}
{"id": "64a7345393", "idle": 1.5611654056984443, "idle32": 1.6026706126019439, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5714202080443762, "loaded32": 1.6129763101219323}
- the asked group: loaded / idle, median 0.969 over 7 (range 0.952-1.007)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
