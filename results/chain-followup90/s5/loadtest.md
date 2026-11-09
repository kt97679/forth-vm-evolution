pinned to cpu 1 (it and its sibling 0% busy; BENCH_CPU=N to choose)
pinned to cpu 1 (it and its sibling 0% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 1 (setup()'s), the load on 2, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.353 | 0.346 | 0.980 | 0.346 | 0.370 | 0.357 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.308 | 0.302 | 0.980 | 0.309 | 0.336 | 0.315 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.339 | 0.331 | 0.978 | 0.322 | 0.342 | 0.329 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.335 | 0.329 | 0.982 | 0.377 | 0.384 | 0.370 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.389 | 0.380 | 0.979 | 0.405 | 0.421 | 0.409 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.824 | 0.827 | 1.004 | 0.767 | 0.761 | 0.763 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.571 | 1.580 | 1.005 | 1.624 | 1.616 | 1.628 |

{"id": "11a56ff9e4", "idle": 0.3531691593718711, "idle32": 0.3696668108681255, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3459649666006025, "loaded32": 0.3573892715808915}
{"id": "782f3ad7ff", "idle": 0.3079743801739454, "idle32": 0.33629076581267053, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.3018188355423728, "loaded32": 0.3154510126559279}
{"id": "3eb59b271d", "idle": 0.33870377447629413, "idle32": 0.34186359631744045, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.33125992752491645, "loaded32": 0.32870754147011483}
{"id": "c2ef9488ff", "idle": 0.33478428476097005, "idle32": 0.38431014891503035, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3288576136179356, "loaded32": 0.3697914354415273}
{"id": "ae99617f06", "idle": 0.3887064681700617, "idle32": 0.4205320503056824, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.380488957972943, "loaded32": 0.4090642858753517}
{"id": "fb0d57c8a2", "idle": 0.8239629393682952, "idle32": 0.761303960212114, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8271288913560836, "loaded32": 0.7627325817554873}
{"id": "64a7345393", "idle": 1.5714652519194996, "idle32": 1.6160347151833943, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5800864029061863, "loaded32": 1.6276831867594759}
- the asked group: loaded / idle, median 0.980 over 7 (range 0.978-1.005)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
