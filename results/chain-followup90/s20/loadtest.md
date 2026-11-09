pinned to cpu 2 (it and its sibling 2% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 1% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.354 | 0.342 | 0.967 | 0.346 | 0.361 | 0.352 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.307 | 0.296 | 0.963 | 0.309 | 0.325 | 0.317 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.338 | 0.326 | 0.965 | 0.322 | 0.343 | 0.322 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.334 | 0.322 | 0.963 | 0.377 | 0.380 | 0.366 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.385 | 0.370 | 0.960 | 0.405 | 0.418 | 0.400 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.820 | 0.830 | 1.012 | 0.767 | 0.767 | 0.761 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.564 | 1.583 | 1.012 | 1.624 | 1.609 | 1.600 |

{"id": "11a56ff9e4", "idle": 0.354011710130523, "idle32": 0.36109128942940677, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3422153522013909, "loaded32": 0.3520630185319785}
{"id": "782f3ad7ff", "idle": 0.307457624560395, "idle32": 0.3249905562520474, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29618077202757137, "loaded32": 0.3168604560147884}
{"id": "3eb59b271d", "idle": 0.33769655706371154, "idle32": 0.3433554054686162, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.32580482677820094, "loaded32": 0.32232621036410314}
{"id": "c2ef9488ff", "idle": 0.33420275542822586, "idle32": 0.38037247008356756, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.32190341849733617, "loaded32": 0.3661434880903437}
{"id": "ae99617f06", "idle": 0.38545781715518596, "idle32": 0.4181350155606185, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3698933817033515, "loaded32": 0.3996234727925703}
{"id": "fb0d57c8a2", "idle": 0.8200791907313335, "idle32": 0.7668051169407765, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.82971505273451, "loaded32": 0.7612119544488064}
{"id": "64a7345393", "idle": 1.5639008428078307, "idle32": 1.6092410190247175, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5828945186052426, "loaded32": 1.600126046190751}
- the asked group: loaded / idle, median 0.965 over 7 (range 0.960-1.012)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
