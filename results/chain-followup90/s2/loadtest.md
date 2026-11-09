pinned to cpu 1 (it and its sibling 7% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 9% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.346 | 0.343 | 0.992 | 0.346 | 0.355 | 0.350 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.302 | 0.296 | 0.980 | 0.309 | 0.320 | 0.311 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.330 | 0.326 | 0.987 | 0.322 | 0.333 | 0.326 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.330 | 0.326 | 0.986 | 0.377 | 0.371 | 0.363 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.384 | 0.377 | 0.980 | 0.405 | 0.404 | 0.399 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.826 | 0.831 | 1.006 | 0.767 | 0.767 | 0.762 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.572 | 1.577 | 1.003 | 1.624 | 1.600 | 1.605 |

{"id": "11a56ff9e4", "idle": 0.3458293088963148, "idle32": 0.3554856925643446, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3430039889796912, "loaded32": 0.35003405442744395}
{"id": "782f3ad7ff", "idle": 0.3019668118557364, "idle32": 0.320344047913714, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.2959506489890081, "loaded32": 0.3113541798230958}
{"id": "3eb59b271d", "idle": 0.33027878359025165, "idle32": 0.3327024209734714, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.32589550368448367, "loaded32": 0.3261643187677419}
{"id": "c2ef9488ff", "idle": 0.3304698384669848, "idle32": 0.3707290126845293, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3260083008188696, "loaded32": 0.36316063697448714}
{"id": "ae99617f06", "idle": 0.38426133777047633, "idle32": 0.40384344301113395, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3766247281958016, "loaded32": 0.399212451593999}
{"id": "fb0d57c8a2", "idle": 0.8263396697108518, "idle32": 0.7668569983369571, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8309105853321668, "loaded32": 0.7618630498273998}
{"id": "64a7345393", "idle": 1.5721556102268774, "idle32": 1.6002956922014862, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5767423188238152, "loaded32": 1.6053656807406638}
- the asked group: loaded / idle, median 0.987 over 7 (range 0.980-1.006)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
