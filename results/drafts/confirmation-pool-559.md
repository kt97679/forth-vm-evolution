# The confirmation run's founders - no good design missed (Iteration 559)

The owner (559): "no rush, let's proceed carefully to ensure we are not missing good designs". The run seeded with the
best designs seen comes as GOALS.md's confirmation run, after the 12-hour series stops (seed 79 at the earliest), and its
pool is built so that no good design is left out.

**What --carry does today** (evolve.py, Iteration 45): each database's own front by first_front - the evolver's
dominance, speeds within 2% and memory within 8 KB as ties - carried into generation 0, every carried design timed again
with the run's own; no cap. Its filter (status ok, a speed, a size) keeps every alive design of modern records (seed 76:
22,758 of 22,758).

**The gap**: the tolerance front loses designs to a dominance chain - seed 76's 105 designs faster than its front's
fastest, down to 0.1383; its strict front 1,296 designs against 262. Carried as it is, the confirmation run would leave
them out.

**Prepared (Iteration 562)**: steps 1, 3 and 4 in the after-seed-78 batch (carry-after-seed78.patch); step 2 is the
confirmation run's NEXT-RUN line - `seed N HOURS widths carryall` (no noevolved), with `then experiment carry-check.py
--all` in the line of the run before it, so the pool is pre-flighted on the laptop's every archive; step 5 is its
processing.

**The plan, before the confirmation run:**
1. --carry takes each database's strict front (no tolerance) - a patch. The series runs with noevolved and never
   carries, so it waits until then without touching the count.
2. The databases: every archived run from seed 71 on (the seven workloads with apps) through the 12-hour series' last,
   and the older runs' fronts too - every carried design is timed again, so an old measure only chooses. The cost is
   about a second of the run a design (seed 76: 36,200 records in 10 hours).
3. Designs named elsewhere, carried as well where no front has them: each machine's fastest from the cross-machine
   checks (seed 76's: 3d4e860a9f on dream), the held-out and application bests.
4. A pre-flight here: every pooled genome built with the current code, its outputs against s6's - a genome the code has
   moved under (the JIT fix, the lifted freezes) caught before the run, not during it.
5. The run's front read as the series reads it - the extremes from every alive design - and the final set chosen from
   the strict front.
