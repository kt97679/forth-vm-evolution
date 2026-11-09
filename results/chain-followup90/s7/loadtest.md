pinned to cpu 1 (it and its sibling 8% busy; BENCH_CPU=N to choose)
pinned to cpu 1 (it and its sibling 8% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 1 (setup()'s), the load on 2, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.350 | 0.346 | 0.990 | 0.346 | 0.370 | 0.353 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.310 | 0.303 | 0.978 | 0.309 | 0.334 | 0.331 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.344 | 0.334 | 0.971 | 0.322 | 0.341 | 0.342 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.340 | 0.329 | 0.969 | 0.377 | 0.384 | 0.374 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.389 | 0.382 | 0.983 | 0.405 | 0.419 | 0.415 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.822 | 0.826 | 1.005 | 0.767 | 0.775 | 0.775 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.563 | 1.570 | 1.004 | 1.624 | 1.599 | 1.609 |

{"id": "11a56ff9e4", "idle": 0.34958087360050766, "idle32": 0.36997495217028525, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3461475306514827, "loaded32": 0.3529165128093504}
{"id": "782f3ad7ff", "idle": 0.3095613188126505, "idle32": 0.33390091087829354, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.30270723676788897, "loaded32": 0.33081115018709023}
{"id": "3eb59b271d", "idle": 0.34439227215271695, "idle32": 0.34081621763387077, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.33431900599687253, "loaded32": 0.3423019016587276}
{"id": "c2ef9488ff", "idle": 0.33958287815872074, "idle32": 0.38387410211825934, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3291166995137677, "loaded32": 0.3741488626301235}
{"id": "ae99617f06", "idle": 0.3886593452365288, "idle32": 0.41925123084011306, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.38216149142274747, "loaded32": 0.41463201898733776}
{"id": "fb0d57c8a2", "idle": 0.822277600769848, "idle32": 0.7749725642632602, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8261252610149269, "loaded32": 0.7747335145615801}
{"id": "64a7345393", "idle": 1.56332695486032, "idle32": 1.599076891932804, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5701532953153168, "loaded32": 1.6091960892211783}
- the asked group: loaded / idle, median 0.983 over 7 (range 0.969-1.005)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
