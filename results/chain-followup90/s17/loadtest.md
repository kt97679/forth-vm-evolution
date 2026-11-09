pinned to cpu 2 (it and its sibling 2% busy; BENCH_CPU=N to choose)
pinned to cpu 8 (it and its sibling 2% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 8 (setup()'s), the load on 0, 2, 4: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.346 | 0.339 | 0.980 | 0.346 | 0.363 | 0.351 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.302 | 0.297 | 0.984 | 0.309 | 0.323 | 0.310 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.340 | 0.324 | 0.954 | 0.322 | 0.331 | 0.334 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.336 | 0.321 | 0.956 | 0.377 | 0.376 | 0.365 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.384 | 0.374 | 0.973 | 0.405 | 0.420 | 0.404 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.824 | 0.832 | 1.009 | 0.767 | 0.769 | 0.775 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.574 | 1.587 | 1.008 | 1.624 | 1.616 | 1.607 |

{"id": "11a56ff9e4", "idle": 0.34632891573862673, "idle32": 0.36337666819530945, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.33946526501669677, "loaded32": 0.3506735330291405}
{"id": "782f3ad7ff", "idle": 0.3023179705697715, "idle32": 0.3234534930071795, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.2974876617401781, "loaded32": 0.3096891570765423}
{"id": "3eb59b271d", "idle": 0.3397608254385228, "idle32": 0.33050912335827504, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3240812382168536, "loaded32": 0.3339206869784872}
{"id": "c2ef9488ff", "idle": 0.3361145878020625, "idle32": 0.3763659193406912, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.32119616791989275, "loaded32": 0.36452489613305356}
{"id": "ae99617f06", "idle": 0.38407669645866754, "idle32": 0.4199359702437872, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3737244138076927, "loaded32": 0.4036587671429987}
{"id": "fb0d57c8a2", "idle": 0.8241136333162289, "idle32": 0.7690563984186463, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8317812229790579, "loaded32": 0.7754914466170868}
{"id": "64a7345393", "idle": 1.5739649340129573, "idle32": 1.6155212852874377, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.587185896589439, "loaded32": 1.607061150389974}
- the asked group: loaded / idle, median 0.980 over 7 (range 0.954-1.009)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
