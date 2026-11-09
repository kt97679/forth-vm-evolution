pinned to cpu 4 (it and its sibling 6% busy; BENCH_CPU=N to choose)
pinned to cpu 8 (it and its sibling 4% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 8 (setup()'s), the load on 0, 2, 4: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.339 | 0.339 | 1.000 | 0.346 | 0.359 | 0.351 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.308 | 0.298 | 0.967 | 0.309 | 0.325 | 0.309 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.340 | 0.328 | 0.966 | 0.322 | 0.335 | 0.331 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.334 | 0.320 | 0.959 | 0.377 | 0.379 | 0.378 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.381 | 0.373 | 0.978 | 0.405 | 0.405 | 0.409 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.825 | 0.826 | 1.001 | 0.767 | 0.767 | 0.773 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.560 | 1.580 | 1.013 | 1.624 | 1.598 | 1.620 |

{"id": "11a56ff9e4", "idle": 0.33934754473974743, "idle32": 0.35869169324683897, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3392235089475918, "loaded32": 0.35140901671813213}
{"id": "782f3ad7ff", "idle": 0.30759996448622906, "idle32": 0.32478004978363273, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.2975762755442652, "loaded32": 0.30928075357848844}
{"id": "3eb59b271d", "idle": 0.3398309867641346, "idle32": 0.3351980133673487, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3282933602908838, "loaded32": 0.3309318580352293}
{"id": "c2ef9488ff", "idle": 0.33351706449822294, "idle32": 0.37911071850572436, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.31975908069682807, "loaded32": 0.3781400474636172}
{"id": "ae99617f06", "idle": 0.3812576593587112, "idle32": 0.4046070553993488, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3728415659045802, "loaded32": 0.4088858651762876}
{"id": "fb0d57c8a2", "idle": 0.824725282611507, "idle32": 0.7670261733230307, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8255352064778426, "loaded32": 0.7733839711021266}
{"id": "64a7345393", "idle": 1.5598326454217213, "idle32": 1.597908542840665, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5804436274833131, "loaded32": 1.6196636615211086}
- the asked group: loaded / idle, median 0.978 over 7 (range 0.959-1.013)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
