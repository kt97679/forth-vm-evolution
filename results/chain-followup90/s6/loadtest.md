pinned to cpu 4 (it and its sibling 6% busy; BENCH_CPU=N to choose)
pinned to cpu 2 (it and its sibling 4% busy; BENCH_CPU=N to choose)
# The measuring load (lab/evolve/loadtest.py, Iteration 455)

Front: results/followup-seed90.md, the candidates (7 designs); the 8 fastest and 4 slowest. Measured on core 2 (setup()'s), the load on 0, 4, 6: s6 on the kernel workload over and over. 10 rounds a measure; idle, loaded, idle, loaded - the geometric mean of each pair.

| design | group | in-run | re-measured | idle | loaded | loaded / idle | in-run 32 | idle 32 | loaded 32 |
|---|---|---|---|---|---|---|---|---|---|
| 11a56ff9e4 | asked | 0.334 | 0.334 | 0.351 | 0.342 | 0.975 | 0.346 | 0.361 | 0.351 |
| 782f3ad7ff | asked | 0.292 | 0.292 | 0.303 | 0.294 | 0.971 | 0.309 | 0.313 | 0.313 |
| 3eb59b271d | asked | 0.319 | 0.319 | 0.331 | 0.323 | 0.975 | 0.322 | 0.330 | 0.325 |
| c2ef9488ff | asked | 0.332 | 0.332 | 0.330 | 0.321 | 0.972 | 0.377 | 0.368 | 0.364 |
| ae99617f06 | asked | 0.375 | 0.375 | 0.385 | 0.374 | 0.972 | 0.405 | 0.417 | 0.404 |
| fb0d57c8a2 | asked | 0.824 | 0.824 | 0.826 | 0.830 | 1.005 | 0.767 | 0.768 | 0.775 |
| 64a7345393 | asked | 1.581 | 1.581 | 1.577 | 1.582 | 1.003 | 1.624 | 1.599 | 1.609 |

{"id": "11a56ff9e4", "idle": 0.3508292970686262, "idle32": 0.36063082673976155, "inrun": 0.3344649957403834, "inrun32": 0.3463796096823302, "loaded": 0.3421566823028563, "loaded32": 0.3514481703145057}
{"id": "782f3ad7ff", "idle": 0.30259371710375227, "idle32": 0.3134821452379389, "inrun": 0.2921257883130746, "inrun32": 0.3086628152471835, "loaded": 0.29368858039954815, "loaded32": 0.31264639032902286}
{"id": "3eb59b271d", "idle": 0.331178457739304, "idle32": 0.32951279282738916, "inrun": 0.31876421182711784, "inrun32": 0.32200121574494256, "loaded": 0.3227928021790708, "loaded32": 0.32476267190136143}
{"id": "c2ef9488ff", "idle": 0.3302705185584395, "idle32": 0.36822738305490715, "inrun": 0.332386829251106, "inrun32": 0.3766817076039704, "loaded": 0.3209929380245457, "loaded32": 0.363859045966067}
{"id": "ae99617f06", "idle": 0.38468670952637374, "idle32": 0.41748714987145025, "inrun": 0.3751574012075074, "inrun32": 0.4045153959416717, "loaded": 0.374094802159929, "loaded32": 0.40413792684787486}
{"id": "fb0d57c8a2", "idle": 0.8259703648596822, "idle32": 0.7679032616863656, "inrun": 0.8244482774406747, "inrun32": 0.7666540585673541, "loaded": 0.829876667255569, "loaded32": 0.7745784547353031}
{"id": "64a7345393", "idle": 1.5769758459943697, "idle32": 1.5987417833403943, "inrun": 1.5809972333832245, "inrun32": 1.6240304411411217, "loaded": 1.5818716460745283, "loaded32": 1.608685884431619}
- the asked group: loaded / idle, median 0.975 over 7 (range 0.971-1.005)

The load explains the fast end's optimism if the fast group's median is near 0.90 and the slow group's near 1.00.
