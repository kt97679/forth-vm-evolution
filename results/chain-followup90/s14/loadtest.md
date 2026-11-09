pinned to cpu 2 (it and its sibling 4% busy; BENCH_CPU=N to choose)
pinned to cpu 8 (it and its sibling 5% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 8 (setup()'s), the load on 0, 2, 4: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.346 | 0.334 | 0.967 | 0.346 | 0.353 | 0.345 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.304 | 0.297 | 0.979 | 0.309 | 0.308 | 0.310 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.335 | 0.329 | 0.982 | 0.322 | 0.338 | 0.328 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.334 | 0.319 | 0.955 | 0.377 | 0.369 | 0.360 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.379 | 0.373 | 0.985 | 0.405 | 0.406 | 0.404 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.830 | 0.830 | 1.000 | 0.767 | 0.758 | 0.777 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.574 | 1.583 | 1.006 | 1.624 | 1.575 | 1.600 |

{"id": "11a56ff9e4", "idle": 0.3458974186652374, "idle32": 0.35333609552154627, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.33437728287061175, "loaded32": 0.3451286270265478}
{"id": "782f3ad7ff", "idle": 0.30371360977047435, "idle32": 0.3083751081770472, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29745173495075233, "loaded32": 0.30964891767134084}
{"id": "3eb59b271d", "idle": 0.3350490048185282, "idle32": 0.33821076838140957, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3291805406119307, "loaded32": 0.3284786257987556}
{"id": "c2ef9488ff", "idle": 0.33419954658366563, "idle32": 0.36927956002134427, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.31922216386103264, "loaded32": 0.3601187254269726}
{"id": "ae99617f06", "idle": 0.3789253620126165, "idle32": 0.4058601738738057, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.37330068162249863, "loaded32": 0.40373348719905294}
{"id": "fb0d57c8a2", "idle": 0.8299837031548661, "idle32": 0.7577661792727127, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8298851679435674, "loaded32": 0.7767155378732895}
{"id": "64a7345393", "idle": 1.5742037728867055, "idle32": 1.575080554100761, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5834687490367703, "loaded32": 1.5995142792815011}
- the asked group: loaded / idle, median 0.982 over 7 (range 0.955-1.006)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
