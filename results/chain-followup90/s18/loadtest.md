pinned to cpu 1 (it and its sibling 0% busy; BENCH_CPU=N to choose)
pinned to cpu 4 (it and its sibling 2% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 4 (setup()'s), the load on 0, 2, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.342 | 0.341 | 0.999 | 0.346 | 0.359 | 0.349 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.302 | 0.295 | 0.979 | 0.309 | 0.323 | 0.315 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.336 | 0.323 | 0.963 | 0.322 | 0.341 | 0.324 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.335 | 0.322 | 0.961 | 0.377 | 0.382 | 0.364 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.382 | 0.375 | 0.981 | 0.405 | 0.411 | 0.405 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.818 | 0.825 | 1.008 | 0.767 | 0.763 | 0.767 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.557 | 1.575 | 1.012 | 1.624 | 1.616 | 1.615 |

{"id": "11a56ff9e4", "idle": 0.34158986476426345, "idle32": 0.35907704545571506, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.34135038458244465, "loaded32": 0.34939682772560476}
{"id": "782f3ad7ff", "idle": 0.30158853265907204, "idle32": 0.3229462757893973, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29531825611632817, "loaded32": 0.3146593965124349}
{"id": "3eb59b271d", "idle": 0.335809452391851, "idle32": 0.3408996290953179, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3232463996829143, "loaded32": 0.323901523326255}
{"id": "c2ef9488ff", "idle": 0.3354408471475877, "idle32": 0.38182918697555074, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3223116760237052, "loaded32": 0.3643254022452163}
{"id": "ae99617f06", "idle": 0.3820578867366338, "idle32": 0.41078678878937924, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3748725378180782, "loaded32": 0.4052796769254195}
{"id": "fb0d57c8a2", "idle": 0.8180787913676704, "idle32": 0.7630613527651487, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8246079839023815, "loaded32": 0.7670087308486883}
{"id": "64a7345393", "idle": 1.5571092070683814, "idle32": 1.615530747362304, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5751742381125966, "loaded32": 1.6149522010465867}
- the asked group: loaded / idle, median 0.981 over 7 (range 0.961-1.012)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
