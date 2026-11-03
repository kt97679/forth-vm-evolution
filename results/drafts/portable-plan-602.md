# The portable run - planned (Iteration 602)

**The question** (the owner, 601-602): the best portable design - without the JIT, which is x86 only - for relf's CV8,
which must stay portable; and whether a search for it alone finds better than what the lab already has.

**What the lab already has, and a correction.** 601 said the JIT crowds portable designs off the front; it does not -
memory keeps them (the JIT designs 208-244 KB, the portable 104-148): 279 of the pooled true front's 444 designs are
portable, the same 279 as the portable designs' own front. The gap is the final pick's: its 232 candidates were chosen
by their contribution to the whole front, whose fast end the JIT owns, so only 5 of the 279 were candidates, and the
fastest of them in-run - 8cc7f60d6b 0.298, f55cec5849 0.304, 0d2912ef80 0.306, against c2ef9488ff's 0.3125 - were
never re-measured, nor measured on dream or the Tegra, whose order on portable designs is its own.
results/portable-front-seed86.md: the 279 and the final set's 3 other portable designs, 282.

**The carry**: the default, the last four archives' fronts (CARRY_LAST=4, the random baseline excluded) - seeds 83, 84 and
86, the confirmation runs' fronts holding the pool's; `carryall` would also mark it a confirmation run in process-seed.sh.

**The chain** (NEXT-RUN, REMOTES; 21 hours - 603, the owner's 9 or 21): `seed 87 nojit 21h widths` - every design without
the JIT (evolve.py --require nojit: require() sets jit=0, mutation leaves the JIT's genes), the earlier fronts carried in
as their JIT-off builds, selected at both widths; then `experiment loadtest.py --ids results/portable-front-seed86.md
--rounds 5` on the laptop; during the run the Tegra (3 rounds, up to 4 sessions) and dream (10 rounds, up to 12
sessions a width) measure the 282. Rehearsed in a scratch clone (602): 6 carried, 29 records, none with the JIT.

**The rule, fixed before the run** (lab/evolve/portable.py): BETTER when the run's true front's hypervolume beats the
portable pool's - the pool's portable designs and the final set's 7, in-run - by 1% or more, or an extreme does by its
threshold (speed 2%, binary + image 1%, memory 4 KB, 32-bit speed 2%): the stopping rule's effect sizes. In-run against
in-run; the run's designs on the union's true front named either way.

**Then** (its processing): final-pick.py on the 282 with the chain's readings - the best portable designs found before,
by role, on the three machines; `lab/evolve/portable-followup.py DB portablepick.json OUT --hours H` (604) writes a short chain's
list and lines: re-measuring, in one session a machine, the run's designs on the union's
front beside the best of the 282 by role (laptop, dream, the Tegra); the portable roles of results/handoff-relf-601.md
replaced where a design beats the one there by the thresholds after re-measure, and the package rebuilt
(lab/evolve/pack-designs.py). The run is no series run: no stopping line, no gene votes (its own ledger line).
