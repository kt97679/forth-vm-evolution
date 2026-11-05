# The resume that forked - seed 87 (Iteration 610)

**What happened.** The laptop crashed 10.5 hours into seed 87, at generation 136. The owner restarted next-run.sh (03:35
UTC, 11-04); it resumed from the database, as designed: evolve.py replays a run from its records, deciding from the
designs this run asked for, never the whole database. The replay forked at once - after generation 2 the first attempt's
attic held 115 designs and 35 lost gene values, the replay's 118 and 36 - and from generation 3 it measured children of
its own: 262 generations in the 20.5 hours left, a second search beside the first, not its continuation. The database
holds both (A: 38,912 records; B: from line 39,331 of 104,522); the run's front is their union.

**The cause.** The fast gate's second reading (Iteration 446): a child faster than the gate is measured again in the
next generation's batch and its record written again - a second line with speed1, speed2 and their geometric mean as
its speed. load() keeps the last line, so the replay ranked every gated design on the mean from its first generation,
where the first attempt had ranked it on its first reading until the batch after. Other survivors, another attic,
other children. Seed 87 had 616 such designs (422 in A); one in generations 1-2 is enough.

**The fix** (lab/evolve/evolve.py). load() keeps, for each design whose second reading follows a gated first, the first
record and the generation of the batch that measured it again (that of the records after the second reading); the
run's loop starts from the first readings and flush() puts each second reading back in its generation's batch,
"(replayed)" in the log. A second reading the first attempt never took is measured at the first batch with children,
as it would have been. A run stopped inside its replay reports the records as they end. EVOLVE_REPLAY=0: off.

**The test** (lab/evolve/test-resume.py, in tools/run-tests.sh): 12 designs, 9 generations, a stand-in measurement
(nothing built), the database cut at generation 6 after its second readings, the run started again on it - generations
1-6 as the first attempt's; with EVOLVE_REPLAY=0 it forks by generation 3 - seed 87's failure in small.

**Not covered.** After the crash point a resumed run decides on its own (its screen fitted at the crash, not at its
cadence) - no reference to match there. The laptop's crash itself is the owner's machine; next-run.sh's resume worked.

**The two attempts** (results/drafts/attempts-610.py - each one's hypervolume in the stopping rule's fixed box; the true
front's tolerances make it move both ways by about 1%):

records: A 38912 (generations 0-136), B 69829 (0-262); B starts at line 39331 of 104522
| generation | A hypervolume | B hypervolume |
|---|---|---|
| 20 | 0.285146 | 0.287270 |
| 40 | 0.286347 | 0.287390 |
| 60 | 0.286874 | 0.285154 |
| 80 | 0.286734 | 0.287609 |
| 100 | 0.284937 | 0.285863 |
| 120 | 0.289422 | 0.287200 |
| 140 | - | 0.289904 |
| 160 | - | 0.291537 |
| 180 | - | 0.292079 |
| 200 | - | 0.292224 |
| 220 | - | 0.288140 |
| 240 | - | 0.287441 |
| 260 | - | 0.287062 |
| 136 | 0.291862 | 0.289843 |
| 262 | - | 0.287073 |
A at its end: fastest 0.2847, smallest 13861, memory 108, fastest32 0.2888
B at its end: fastest 0.2921, smallest 13803, memory 108, fastest32 0.3053

At the same generation the two are within about 1%. The longer one did not gain: B peaked at 0.2922 near generation 200
and ended at 0.2871, below A's 0.2919 at 136; A, the shorter, found the run's fastest at both widths. Their union -
0.2958, the run's verdict - is above either: two searches of the same seed pooled beat one twice as long.
