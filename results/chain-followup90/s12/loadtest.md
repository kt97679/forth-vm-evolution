pinned to cpu 2 (it and its sibling 6% busy; BENCH_CPU=N to choose)
pinned to cpu 8 (it and its sibling 6% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 8 (setup()'s), the load on 0, 2, 4: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.342 | 0.339 | 0.992 | 0.346 | 0.358 | 0.352 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.299 | 0.297 | 0.994 | 0.309 | 0.316 | 0.312 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.330 | 0.326 | 0.988 | 0.322 | 0.337 | 0.326 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.325 | 0.324 | 0.997 | 0.377 | 0.369 | 0.362 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.374 | 0.375 | 1.002 | 0.405 | 0.401 | 0.411 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.822 | 0.829 | 1.009 | 0.767 | 0.760 | 0.776 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.571 | 1.582 | 1.007 | 1.624 | 1.593 | 1.623 |

{"id": "11a56ff9e4", "idle": 0.3417156271938603, "idle32": 0.3579356265621888, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3389039419276724, "loaded32": 0.3520427764882008}
{"id": "782f3ad7ff", "idle": 0.29876308603363866, "idle32": 0.3157612420964159, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29684122260504814, "loaded32": 0.3123811771764855}
{"id": "3eb59b271d", "idle": 0.3297231516744818, "idle32": 0.3366453808102777, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.32574434357936205, "loaded32": 0.3259784815470675}
{"id": "c2ef9488ff", "idle": 0.32464296113894253, "idle32": 0.3692494560260319, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.32378825830198893, "loaded32": 0.3620012533815993}
{"id": "ae99617f06", "idle": 0.3744158501017786, "idle32": 0.4009283335753599, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.37504217119621874, "loaded32": 0.4108523263850023}
{"id": "fb0d57c8a2", "idle": 0.8216623799687545, "idle32": 0.7596012638859138, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8289962633769532, "loaded32": 0.775654832007787}
{"id": "64a7345393", "idle": 1.5712979544569166, "idle32": 1.5925025059093103, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.582200347517673, "loaded32": 1.6226075844021943}
- the asked group: loaded / idle, median 0.997 over 7 (range 0.988-1.009)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
