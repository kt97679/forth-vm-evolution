pinned to cpu 8 (it and its sibling 7% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 6% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.345 | 0.339 | 0.983 | 0.346 | 0.361 | 0.349 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.305 | 0.292 | 0.958 | 0.309 | 0.326 | 0.314 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.334 | 0.326 | 0.975 | 0.322 | 0.340 | 0.333 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.330 | 0.320 | 0.970 | 0.377 | 0.380 | 0.365 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.383 | 0.375 | 0.979 | 0.405 | 0.410 | 0.409 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.829 | 0.829 | 1.000 | 0.767 | 0.768 | 0.764 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.579 | 1.573 | 0.996 | 1.624 | 1.623 | 1.624 |

{"id": "11a56ff9e4", "idle": 0.34488032482446285, "idle32": 0.3612328797164089, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3391367953373025, "loaded32": 0.3486543028454392}
{"id": "782f3ad7ff", "idle": 0.3052983239977103, "idle32": 0.32587698568608897, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.2923529204327258, "loaded32": 0.31401000680402635}
{"id": "3eb59b271d", "idle": 0.33410488835523905, "idle32": 0.33998146697331283, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3258367755037493, "loaded32": 0.33330959079442074}
{"id": "c2ef9488ff", "idle": 0.3296787296879001, "idle32": 0.37953382259397445, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3199482286266366, "loaded32": 0.3647391518603716}
{"id": "ae99617f06", "idle": 0.3825446851097928, "idle32": 0.4103352346927584, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.37461858291868183, "loaded32": 0.40857097612553445}
{"id": "fb0d57c8a2", "idle": 0.828741173344926, "idle32": 0.7675270507380535, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8289227159243644, "loaded32": 0.7635489590488926}
{"id": "64a7345393", "idle": 1.5785662147290582, "idle32": 1.6226010535497137, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5726177315081795, "loaded32": 1.62384657817637}
- the asked group: loaded / idle, median 0.979 over 7 (range 0.958-1.000)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
