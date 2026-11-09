pinned to cpu 2 (it and its sibling 3% busy; BENCH_CPU=N to choose)
pinned to cpu 8 (it and its sibling 2% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 8 (setup()'s), the load on 0, 2, 4: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.344 | 0.338 | 0.983 | 0.346 | 0.364 | 0.352 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.307 | 0.297 | 0.965 | 0.309 | 0.324 | 0.309 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.337 | 0.329 | 0.974 | 0.322 | 0.340 | 0.323 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.332 | 0.320 | 0.963 | 0.377 | 0.380 | 0.363 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.386 | 0.380 | 0.985 | 0.405 | 0.416 | 0.408 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.822 | 0.827 | 1.007 | 0.767 | 0.766 | 0.764 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.565 | 1.574 | 1.006 | 1.624 | 1.608 | 1.618 |

{"id": "11a56ff9e4", "idle": 0.3442074902776681, "idle32": 0.36397768166329847, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.33829066688311754, "loaded32": 0.35156214648100487}
{"id": "782f3ad7ff", "idle": 0.3074508149882594, "idle32": 0.32391117956474325, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.2965374104003029, "loaded32": 0.30917052350397295}
{"id": "3eb59b271d", "idle": 0.3373291781810223, "idle32": 0.3397680578644515, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.32859767392258177, "loaded32": 0.323391747420066}
{"id": "c2ef9488ff", "idle": 0.3320713905592195, "idle32": 0.3798039028793641, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3198113025660609, "loaded32": 0.3632305095831225}
{"id": "ae99617f06", "idle": 0.3858367583556423, "idle32": 0.4160685307237034, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3799300004741115, "loaded32": 0.408263430099574}
{"id": "fb0d57c8a2", "idle": 0.8215709584808467, "idle32": 0.7664441527852492, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8271325736283041, "loaded32": 0.7644016808323404}
{"id": "64a7345393", "idle": 1.5651833882132151, "idle32": 1.607917113270501, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.574174685335962, "loaded32": 1.6176456793630203}
- the asked group: loaded / idle, median 0.983 over 7 (range 0.963-1.007)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
