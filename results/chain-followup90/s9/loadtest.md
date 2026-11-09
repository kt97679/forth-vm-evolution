pinned to cpu 2 (it and its sibling 4% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 4% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.345 | 0.341 | 0.987 | 0.346 | 0.359 | 0.348 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.304 | 0.296 | 0.975 | 0.309 | 0.313 | 0.310 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.332 | 0.324 | 0.975 | 0.322 | 0.332 | 0.326 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.325 | 0.323 | 0.995 | 0.377 | 0.370 | 0.364 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.379 | 0.375 | 0.990 | 0.405 | 0.412 | 0.399 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.835 | 0.829 | 0.993 | 0.767 | 0.760 | 0.767 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.568 | 1.580 | 1.007 | 1.624 | 1.592 | 1.627 |

{"id": "11a56ff9e4", "idle": 0.3451797400904393, "idle32": 0.3590119313530441, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3405567757243144, "loaded32": 0.3477354399883958}
{"id": "782f3ad7ff", "idle": 0.30389578496639497, "idle32": 0.31344857871899495, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29631743842620045, "loaded32": 0.3100284028746625}
{"id": "3eb59b271d", "idle": 0.33222294431901106, "idle32": 0.3319052254912328, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3239830790125577, "loaded32": 0.32631862734828526}
{"id": "c2ef9488ff", "idle": 0.32455927254014694, "idle32": 0.37038814813019805, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.32284505082972836, "loaded32": 0.3641970587819588}
{"id": "ae99617f06", "idle": 0.37907229668535397, "idle32": 0.41157676578326496, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.37517418475348907, "loaded32": 0.39878435591134975}
{"id": "fb0d57c8a2", "idle": 0.8346164496470042, "idle32": 0.7598352777075913, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.8285827836966502, "loaded32": 0.7667718393707431}
{"id": "64a7345393", "idle": 1.5682995130903152, "idle32": 1.5916511162332836, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5797153159940793, "loaded32": 1.6272966759525336}
- the asked group: loaded / idle, median 0.990 over 7 (range 0.975-1.007)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
