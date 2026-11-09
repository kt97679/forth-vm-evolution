pinned to cpu 2 (it and its sibling 4% busy; BENCH_CPU=N to choose)
pinned to cpu 1 (it and its sibling 5% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 1 (setup()'s), the load on 2, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.345 | 0.342 | 0.993 | 0.346 | 0.356 | 0.358 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.299 | 0.303 | 1.010 | 0.309 | 0.317 | 0.313 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.332 | 0.331 | 0.998 | 0.322 | 0.329 | 0.330 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.330 | 0.325 | 0.985 | 0.377 | 0.389 | 0.366 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.382 | 0.377 | 0.987 | 0.405 | 0.404 | 0.419 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.823 | 0.830 | 1.009 | 0.767 | 0.779 | 0.771 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.583 | 1.574 | 0.994 | 1.624 | 1.596 | 1.608 |

{"id": "11a56ff9e4", "idle": 0.3446919532753306, "idle32": 0.35598855157425435, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3424152952093927, "loaded32": 0.35754282763626016}
{"id": "782f3ad7ff", "idle": 0.2994776289975835, "idle32": 0.3172494477890637, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.3026074269295979, "loaded32": 0.3134839401665157}
{"id": "3eb59b271d", "idle": 0.33180536394868176, "idle32": 0.32944438198152887, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.33118973057920975, "loaded32": 0.3296002835379643}
{"id": "c2ef9488ff", "idle": 0.33018463349557386, "idle32": 0.38875917322189624, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.325276380583244, "loaded32": 0.3655685888984104}
{"id": "ae99617f06", "idle": 0.3824911153292282, "idle32": 0.4039946010905087, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3774001548520296, "loaded32": 0.418996780423444}
{"id": "fb0d57c8a2", "idle": 0.8226038380598704, "idle32": 0.7788316012204307, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8299356630230813, "loaded32": 0.7712123059512869}
{"id": "64a7345393", "idle": 1.5826733978385872, "idle32": 1.5956748840373265, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5738143697606597, "loaded32": 1.608199019924933}
- the asked group: loaded / idle, median 0.994 over 7 (range 0.985-1.010)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
