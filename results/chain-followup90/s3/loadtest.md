pinned to cpu 12 (it and its sibling 1% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 6% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.348 | 0.340 | 0.975 | 0.346 | 0.364 | 0.352 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.309 | 0.299 | 0.969 | 0.309 | 0.332 | 0.316 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.345 | 0.327 | 0.948 | 0.322 | 0.347 | 0.326 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.335 | 0.330 | 0.983 | 0.377 | 0.384 | 0.364 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.383 | 0.377 | 0.982 | 0.405 | 0.418 | 0.416 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.827 | 0.824 | 0.997 | 0.767 | 0.770 | 0.769 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.563 | 1.576 | 1.009 | 1.624 | 1.598 | 1.603 |

{"id": "11a56ff9e4", "idle": 0.34843783256043703, "idle32": 0.36392600440422945, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3396210390566115, "loaded32": 0.3518363891539689}
{"id": "782f3ad7ff", "idle": 0.3091083410278855, "idle32": 0.3317771926521066, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29942439214052696, "loaded32": 0.31604370497752504}
{"id": "3eb59b271d", "idle": 0.3451489492971566, "idle32": 0.3467899709643905, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3271488975037524, "loaded32": 0.3259733819464142}
{"id": "c2ef9488ff", "idle": 0.33548510291426104, "idle32": 0.3837636818806751, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3298945844281322, "loaded32": 0.36359824180140604}
{"id": "ae99617f06", "idle": 0.3834903657935335, "idle32": 0.4176434775197825, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3765634703160255, "loaded32": 0.41576349683841357}
{"id": "fb0d57c8a2", "idle": 0.8265389397501643, "idle32": 0.7699757754516465, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8243849312344157, "loaded32": 0.769094495050818}
{"id": "64a7345393", "idle": 1.5625813773441906, "idle32": 1.5980496311079957, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5758763999392484, "loaded32": 1.6030255137631324}
- the asked group: loaded / idle, median 0.982 over 7 (range 0.948-1.009)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
