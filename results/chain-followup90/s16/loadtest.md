pinned to cpu 1 (it and its sibling 2% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 0% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.351 | 0.338 | 0.963 | 0.346 | 0.364 | 0.357 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.303 | 0.297 | 0.980 | 0.309 | 0.326 | 0.311 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.337 | 0.324 | 0.961 | 0.322 | 0.344 | 0.323 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.335 | 0.319 | 0.954 | 0.377 | 0.381 | 0.370 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.383 | 0.376 | 0.982 | 0.405 | 0.411 | 0.416 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.825 | 0.829 | 1.004 | 0.767 | 0.759 | 0.766 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.575 | 1.572 | 0.998 | 1.624 | 1.608 | 1.613 |

{"id": "11a56ff9e4", "idle": 0.3511728852510092, "idle32": 0.3636675066692253, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.33817952909945465, "loaded32": 0.3572501557154195}
{"id": "782f3ad7ff", "idle": 0.3031288803642087, "idle32": 0.3263356945884932, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.2970307792144108, "loaded32": 0.3113339632065189}
{"id": "3eb59b271d", "idle": 0.33741503099181774, "idle32": 0.34392413116046744, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3243066785520582, "loaded32": 0.32306849710529434}
{"id": "c2ef9488ff", "idle": 0.335013464994986, "idle32": 0.38103549064886927, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3194380553134174, "loaded32": 0.3699360222486324}
{"id": "ae99617f06", "idle": 0.38320487171256473, "idle32": 0.4107228409257647, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3763248696286891, "loaded32": 0.4162240884796751}
{"id": "fb0d57c8a2", "idle": 0.8251169269276221, "idle32": 0.7593814774830115, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8287675474441156, "loaded32": 0.7658218539783788}
{"id": "64a7345393", "idle": 1.57537280104707, "idle32": 1.6078378965507796, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5716026104581842, "loaded32": 1.6134388919041343}
- the asked group: loaded / idle, median 0.980 over 7 (range 0.954-1.004)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
