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

**After the follow-up** (Iteration 616; the owner: fixed before seed 88's follow-up returns, and checked to lose no good
design). Another portable run - seed 89, 21 hours, seed 88's setup with every earlier portable front carried - when the
follow-up confirms that seed 88's search found something: one of its designs, re-measured, beats the best of those found
before by the stopping rule's thresholds - the laptop alone at either width, a class (x86-64, x86-32, ARMv7) or the mean
of the three by 2% with the paired difference 2 SE or more, binary + image by 1% or memory by 4 KB (exact) - or takes a
portable role of the handoff (the processing's decision, the owner's trades). Else the portable search stops, and the next
work is the article's final pass. `lab/evolve/followup-roles.py --gain` prints the figures and the verdict
(process-followup.sh's OUT/gain.txt); on 611's readings it gives 611's outcome - seed 87's gain confirmed (the mean -4.2%
against 8cc7f60d6b), so another run (results/drafts/followup-rehearsal-615.sh checks it).
The check (616) - the rule loses no good design: it decides only whether to search again, and no design is dropped
either way - seed 88's front stays recorded (its 469 genomes in results/evolve-amd-ryzen-7-pro-8840hs-seed88.md, its ledger
line in results/stopping-series.md), its re-measured best kept by role in results/followup-pick-seed88.md with each
class's fastest and the best means added (final-pick.py step 5), and a role changes only where a design beats its holder.
Its first form keyed on one design, one machine and one width (c7814def6d against 9f8811f7f4, the laptop alone at 4-byte
cells): a gain in another class or a role would have stopped the search - widened to every class, extreme and role. As
before 616: the follow-up re-measures 30 of seed 88's 405 designs on the union's front (select(), by in-run numbers); the
rest are not re-measured across machines - kept, recorded, for a later need.
