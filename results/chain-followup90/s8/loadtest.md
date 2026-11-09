pinned to cpu 1 (it and its sibling 1% busy; BENCH_CPU=N to choose)
pinned to cpu 8 (it and its sibling 2% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 8 (setup()'s), the load on 0, 2, 4: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.350 | 0.341 | 0.976 | 0.346 | 0.365 | 0.346 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.306 | 0.293 | 0.959 | 0.309 | 0.318 | 0.321 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.326 | 0.328 | 1.004 | 0.322 | 0.325 | 0.324 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.329 | 0.322 | 0.979 | 0.377 | 0.367 | 0.364 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.388 | 0.375 | 0.968 | 0.405 | 0.417 | 0.408 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.827 | 0.829 | 1.002 | 0.767 | 0.777 | 0.771 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.570 | 1.578 | 1.005 | 1.624 | 1.613 | 1.622 |

{"id": "11a56ff9e4", "idle": 0.34960965025063423, "idle32": 0.3650793030637946, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.341351034258409, "loaded32": 0.34582282017305105}
{"id": "782f3ad7ff", "idle": 0.305855271261515, "idle32": 0.31841462460059833, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29344032223220345, "loaded32": 0.3211922113312026}
{"id": "3eb59b271d", "idle": 0.3263242093827564, "idle32": 0.325123824379384, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.327747340205427, "loaded32": 0.32369908506880807}
{"id": "c2ef9488ff", "idle": 0.3294240617075231, "idle32": 0.36655792776247426, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3223679457632302, "loaded32": 0.3641356786423035}
{"id": "ae99617f06", "idle": 0.3876995808647291, "idle32": 0.4168601710859924, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3752169398629751, "loaded32": 0.4081581009755588}
{"id": "fb0d57c8a2", "idle": 0.8270734055405574, "idle32": 0.7767216754549708, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8288274973522907, "loaded32": 0.7713169678692562}
{"id": "64a7345393", "idle": 1.5701292475317916, "idle32": 1.6131028231640727, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5779970389822622, "loaded32": 1.6216557074810432}
- the asked group: loaded / idle, median 0.979 over 7 (range 0.959-1.005)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
