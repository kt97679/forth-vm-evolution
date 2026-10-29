# Seed 80's processing - the checklist (Iteration 565)

HANDOFF.md's routine (process-run.sh, then process-finish.sh); nothing waits in results/pending/.

- **The stopping rule** (matched by generation): seed 80 is the method's fourth run; the last two must gain nothing
  for a stop, so the earliest stop is after seed 81 - unless the owner reads seed 79 at equal effort (565: no gain at
  generation 161), when the confirmation run would have come now. stopping.py prints the bar at seed 80's generation;
  where seed 80 goes past every earlier run, read it at the longest earlier run's end too (565's way: the curve).
- **Prediction 565**: the fastest at generation 126 above 0.1389 (the curve, or the spread); no gain.
- **The Tegra**: 565's check disagreed (-0.103) - does seed 80's chain's check agree again?
- **The deaths**: a cv8 kernel death at scale 1 with doesfar=0 and varcall=1 is the reach limit (deaths-check names it).
