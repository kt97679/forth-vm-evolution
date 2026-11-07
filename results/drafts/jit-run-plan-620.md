# The last JIT run before the freeze (Iteration 620; the owner: "yes, let's do 21 hour jit run" - results/audit-nonportable-619.md)

**Why**: the one lever the JIT search never tried, the length. Its runs stopped at 126-178 generations (9-12 hours); the
portable search found winners at generations 157-258 in 21-hour runs from the pool. Nothing else new reaches it (619).

**When**: after the portable search ends (results/drafts/portable-plan-602.md, "The search goes on") - the last step
before the freeze.

**The run**: `seed N 21h widths carryall` - N the next seed number then; the JIT allowed (no nojit); every archived
database carried as founders, as seed 86's (the portable runs' fronts among them); no experiment. Its remote lines screen
the last portable run's rest (results/screen-seedK.md, K that run; 617's lines - seed 88's: results/screen-seed88.md),
which no next portable run will screen: the last rest at no laptop time.

**The judge, in-run** (process-seed.sh runs confirm.py for a carryall run): the run's true front against the pooled true
front by the stopping rule's thresholds - the hypervolume 1%, speed 2%, binary + image 1%, memory 4 KB, the 32-bit speed
2%. Its pool widened with --pool to every earlier front (seeds 84-88's results files and the later portable runs'), and
only what the run bred counted - confirm.py's "what the run added", carried against bred (seed 86: not confirmed by a
carried design alone). No gain: the four x86 roles are final.

**The follow-up** (when it gains): its best - the bred designs on the union's front, select()'s 30, the JIT kept - beside
the four x86 roles (c7c35f9c97 fastest x86-64, 4ef851fd8e fastest x86-32, 06b188f45b best all-round, bac37f35a2 the
smallest JIT design) on the laptop, dream at both widths and the Tegra (a JIT design's ARMv7 reading its JIT-off build, for
the mean); with them the screen's flagged and the portable holders beside them. Then the 618 rule: another JIT run while a
follow-up confirms progress, else the JIT roles are final; a screened design that takes a portable role reopens the portable
search the same way. No follow-up due for the JIT and the screen flagged some: a short follow-up for them alone
(portable-followup.py --also).

**To prepare while the run goes** (today's follow-up tools are portable only): portable-followup.py keeping JIT designs (it
drops them - a --jit option); followup-roles.py's roles for the x86 classes (the fastest on x86-64 and on x86-32 - it has
ARMv7's) and the smallest JIT design; rehearsed as 615's. The run's predictions written when it is set. **Done (622)**: portable-followup.py --jit --seed N,
followup-roles.py's fast64, fast32, allround and smalljit, confirm.py's pool with the portable runs (results/drafts/jit-rehearsal-622.py).
