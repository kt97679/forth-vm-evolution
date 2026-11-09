pinned to cpu 1 (it and its sibling 5% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 8% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.346 | 0.339 | 0.980 | 0.346 | 0.355 | 0.350 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.300 | 0.293 | 0.978 | 0.309 | 0.328 | 0.309 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.328 | 0.323 | 0.985 | 0.322 | 0.336 | 0.329 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.335 | 0.320 | 0.955 | 0.377 | 0.372 | 0.363 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.374 | 0.373 | 0.997 | 0.405 | 0.412 | 0.405 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.830 | 0.827 | 0.996 | 0.767 | 0.762 | 0.764 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.568 | 1.586 | 1.012 | 1.624 | 1.618 | 1.619 |

{"id": "11a56ff9e4", "idle": 0.3460935209284478, "idle32": 0.355300204842935, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.33906150749852626, "loaded32": 0.3500287800784849}
{"id": "782f3ad7ff", "idle": 0.3000593052573788, "idle32": 0.32752044212745623, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29337234311766075, "loaded32": 0.3090476368786547}
{"id": "3eb59b271d", "idle": 0.3283176520582322, "idle32": 0.3362544150916611, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3233716403858123, "loaded32": 0.3287517697974442}
{"id": "c2ef9488ff", "idle": 0.33456139962718234, "idle32": 0.3720975181694577, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3195455690821, "loaded32": 0.36270506714428674}
{"id": "ae99617f06", "idle": 0.3744682138451623, "idle32": 0.4118821986146501, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.3731801251356335, "loaded32": 0.40549343218482986}
{"id": "fb0d57c8a2", "idle": 0.8298831636470329, "idle32": 0.7622126757171294, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.82684378027597, "loaded32": 0.7644178530620176}
{"id": "64a7345393", "idle": 1.567988404524777, "idle32": 1.6182056402590523, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5864719416639612, "loaded32": 1.6185520899965922}
- the asked group: loaded / idle, median 0.985 over 7 (range 0.955-1.012)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
