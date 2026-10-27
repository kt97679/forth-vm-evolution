# The stopping series - GOALS.md's stopping rule, run by run (lab/evolve/stopping.py, Iteration 554)

Each run on the method: its true front's fixed-box hypervolume (lab/evolve/hv.py, the box lab/evolve/hv-bounds.json)
and four extremes, from its own database at its processing; stopping.py judges a run against the best of the method's
earlier runs, criterion by criterion, and appends its line (HANDOFF.md, "Processing a returned seed", step 6). A method
change opens a new series with a "method" line - the count restarts there. Seed 74's line: its hypervolume from its
processing (Iteration 549), its extremes from its records (results/truefronts-seed75.md; its database stays on the
laptop); from seed 75 on, each from its pack's database.

{"method": "from seed 74", "why": "the after-seed-73 batch (Iteration 544): adaptive operators, the true front, one round first, the evolver self-test, the JIT table's bounds, jitos unfrozen - the count starts (GOALS.md)"}
{"seed": 74, "front": 238, "hv": 0.35667, "fastest": 0.14023, "smallest": 14079, "memory": 112, "fastest32": 0.17395}
{"seed": 75, "front": 266, "hv": 0.348506, "fastest": 0.136349, "smallest": 14095, "memory": 112, "fastest32": 0.172292}
{"seed": 76, "front": 262, "hv": 0.350361, "fastest": 0.145013, "smallest": 14109, "memory": 112, "fastest32": 0.177819}
{"method": "from seed 77", "why": "12 hours, the owner (Iteration 555) - the hours are the method (GOALS.md): the count restarts; the measure as before unless the owner decides (seed 76: the dominance chain)"}
