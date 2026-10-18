# A review of the methodology, the workflows and the logic (Iteration 386)

The owner asked for a review of all results for flaws in method, workflow and logic. Each suspicion here
was checked against the code or the data before it was written down; every figure is reproduced by
`lab/evolve/review-checks.py` (pedigree, curse, cpus, screen) from the files named. One suspicion did not
survive its check and is reported as cleared. The proposals at the end are the owner's calls.

## 1. Act now: the anchoring test is not from scratch

`nocarry` carries no archived front, but every run that is not `fromzero` puts **two evolved designs** into
generation 0 (evolve.py, Iterations 155 and 178): seed 37's fastest (38446e6c09, with jitloop and jitinl - in
seed 58 it started at speed 0.174, five times s6) and seed 40's small-end knee (d99e3d9ed9). Only `fromzero`
leaves them out. Seed 58's front, by each design's expected share of its generation-0 ancestors (every listed
parent weighted equally - an approximation; `review-checks.py pedigree`):

| front, by 64-bit speed | seed 37's fastest | seed 40's knee | founders from s4/s6 | hand-made | random or seeded |
|---|---|---|---|---|---|
| fastest third (57) | 55.0% | 11.3% | 3.8% | 1.1% | 28.8% |
| middle third (57) | 49.4% | 12.3% | 7.4% | 1.4% | 29.4% |
| slowest third (57) | 48.7% | 17.0% | 5.6% | 1.4% | 27.3% |

One design in 140 is half the front's ancestry; the two evolved founders about two thirds. So seed 58's
"within 3.4% of the carried fast end, from scratch" is largely inherited, and **seed 59** - nocarry with the
same founders - **cannot answer the anchoring question it was set for**: if it finds nothing new, the founders
may have steered it into the carried basin. (Seed 36's test, Iteration 123, predates both founders.) The
constraint finding of seed 58 stands, and is if anything strengthened: both evolved founders are tag-2 designs
(their runs required it), so the plain encoding that took the small end came from the hand-made and random
side, against the founders' pull.

A second confound for the seed 58/59 pair: seed 59 is the first chain on Iteration 379's remote path, so it
evolves ~55 minutes longer than seed 58 did (8 h 01 min of a 12-hour chain) - about 11% more search.

**`fromzero` is no answer as it stands** - tested here in miniature (`evolve.py --pop 8 --gens 1 --rounds 1
--fromzero --require tag2 --widths 8,4`): it runs (exit 0, both widths measured, no hand-made design or founder
in generation 0), but only 2 of its 16 designs were tag-2 - require() puts the tag only on designs already CV8,
and random genomes mostly draw other encodings (cell, sod16, cpt16: sizes 27,264 and ~16,000), at 1.2-2.0 times
s6. A start that far below the carried runs makes "behind after 12 hours" uninformative (3c).

**The clean test** is what seed 36 was before Iteration 155: the hand-made designs and the founders built from
them, without the two evolved ones - an opt-in switch for evolve.py and next-run.sh, not yet built.

**Options** (the owner's): keep seed 59 running - with the same founders as seed 58 and the requirement as the
designed difference, it is a replicate of the constraint finding, worth its hours - and make the anchoring
test the run after, once the switch is built and tested; or stop seed 59 now and wait for the switch.

## 2. Measurement and statistics

**2a. The in-run speeds of the fast end are about 10% optimistic - selection on noise (winner's curse).**
Seed 58's front, re-measured after the run against its in-run speed (`curse`): the fastest tenth median
1.112 (all 17 between 1.073 and 1.142), the fastest third 1.081, the middle 1.032, the slowest third 0.991.
A uniform bias would be flat; a gradient that vanishes at the slow end is designs admitted for lucky
draws. Selection counts speeds within 2% as tied, inside a noise of ~10% at the fast end: there, fine
speed selection is mostly chance, and so are the front's gene shares at that end. The comparison's
re-measure (6 rounds, two CPUs) is the number to quote, never the in-run one.

**2b. The verdict's thresholds sit inside the measurement noise.** Session 52's measures, computed from
each CPU alone on the same designs (`cpus ... 52`): "fastest against the others" moves by up to 5.4 points
between the two CPUs (seed 58: -3.8% / +1.6%), "best Q" by up to 6.2 (the run archived 2026-10-17 02:48: -5.8% / +0.4%), and
**seed 57's best Q is +3.5% on cpu 2 and -0.4% on cpu 8** - over the 2% bar on one, under it on the other.
The stopping rule (two small runs in a row) stands on these bars; they were set without a noise estimate.
**Audited at Iteration 388** (results/verdict-audit-388.md): all 16 sessions since the rule, rebuilt and
recomputed per CPU - the two CPUs agree in 14; the two that do not (seeds 50 and 51) were each followed at
once by new genes, so no decision turned on them, and the rule's recent end (seeds 53-55) holds on both. The
noise is real, the past verdicts mostly clear of it. And the verdict reads cpu 2 alone: compare-fronts takes
the session's speed from the first CPU, cpu 8's half of the session feeding only the agreement section.

**2c. Which designs are "on the front of all runs" is largely noise now.** The fronts computed from the two
CPUs of one session share 80-100% of their members while fronts held under 20 designs, and only 46-65% in
the last ten sessions (120-150 designs): the fronts grew dense, many designs within noise of each other.
"On the front of all", the joint front and "the Q-best design of all runs" inherit this.

**2d. Spearman over a whole front overstates agreement.** Held out, seed 58: sieve 0.883 over the front, 0.866
over its fastest third, **0.529 over its fastest tenth** - where selection chooses. A front spanning speeds
0.12 to 1.5 (JIT and not, two encodings) ranks well on anything; the same holds for the remote checks'
headline Spearman (0.96-0.97). Their line "the laptop's six fastest, their rank here" is the informative one
(dream at 32 bits, seed 57's front: 1 2 3 10 15 14).

**2e. 32-bit numbers do not compare across sessions.** The non-PIE patch (applied at 374) rebuilt every 32-bit
engine and s6's between sessions 51 and 52: seed 57's 32-bit fastest, 1a3cfe3e03, was 0.337 in session 51 and
0.400 in session 52 (built and measured both times; compare-fronts.log) - 19%, far beyond three rounds' noise,
and consistent with that rebuild, which made s6's 32-bit engine faster too. Same-session verdicts are sound; seed 58's prediction 4 was
written against session 51's number and "met" only as written.

## 3. Logic of the conclusions

**3a. "Converged" was said of a constrained space.** Every run since Iteration 71 required tag2, and with it
bytehdr (require() sets both); the stopping rule's verdicts - "the gene set has converged" (seeds 19-20, 22-23,
34-35, 53-56) - meant converged inside that subspace. Seed 58, outside it, found the small end 10.5% smaller
and the 32-bit end 21.5% faster. A requirement is part of an experiment's definition and belongs in every
verdict that rests on it; other standing restrictions deserve the same audit (the founders of section 1 are
one).

**3b. One run per configuration.** Carried against fresh, tag-2 against free: each arm is a single run, and
the run-to-run spread under one configuration is unmeasured (the one replicate, seed 4b, is from the first
days; two consecutive carried runs differ by up to 17 points a gene). Seed 58's constraint effect is large and
mechanistic (the plain encoding is smaller; tag-2 costs ~36% at 32 bits) and survives that; the anchoring
question, a matter of degree, does not - it needs replicates, shorter runs with different seeds if the hours
are scarce.

**3c. The anchoring test is asymmetric - seed 59's prediction 1 overclaims.** A fresh run finding territory the
carried runs missed shows anchoring; a fresh run finding nothing shows little, since 12 fresh hours may simply
reach less than the carried runs' hundreds. "Small, so not anchored" (results/predictions.md) should read
"small: no evidence of anchoring at this search budget".

**3d. Superinstructions "stay" by the letter of Iteration 368's rule.** The knockout (Iteration 385) found 0.9%
fewer dispatches at the median - measured at 64 bits with the JIT on only - which is under 1% of time: below
the 2% speed tie and far below the fast end's ~10% in-run noise (2a). Selection cannot see that gain; the gene
persists on its bytes (smaller in 6 of 19) and by drift. Whether a mechanism selection cannot see earns its
place is the owner's question, not answered by "it buys something". **Measured at Iteration 388 with the JIT
off** (the interpreter, as at 32 bits): 0.27% at the median, and a byte cost in every design (+24 to +735) -
the JIT build's savings were layout. The evidence now leans to "buys nothing selection can see".

## 4. Workflow

**4a. A signed verdict, read backwards.** This chat's first summary of seed 58 (Iteration 384) read "smallest
+10.51%" as a loss; it is the run ahead. Caught by checking the per-run minimum before committing; the
table's header does not say which sign is ahead. Labelling it is one line in compare-fronts.py.

**4b. One reader, no second.** The same chat writes the code, reads the outputs, writes and scores the
predictions. Three errors of this kind in Iterations 384-385, each caught by a check rather than a reviewer:
the sign (by the data), a wrong cause for the `L_t2call4` deaths (by the genomes), and a regression in the
first draft of why() (by its before/after test). The routine's checks catch what they test; the readings
between them have none.

**4c. HANDOFF's state goes stale, and the handoff check cannot tell.** "Seed 52 is the laptop's next run
(Iteration 300)" stood twenty lines below "Seed 59 is running"; results/README.md said "seeds 1-47" through
seed 58. tools/handoff-check.py checks the "master: Iteration N" line, not whether the state is current.
(The stale bullet is removed at Iteration 386.)

**4d. The front's thinning keeps the 64-bit bests, not the 32-bit one.** compare-fronts.py --frontier keeps
each run's fastest, smallest and least-memory design, and since Iteration 352 reads the verdict at 32 bits
from what it kept - a 32-bit specialist dominated at 64 bits would be dropped, flattering the newer run.
Latent: in session 52 seed 57's 32-bit fastest was kept. One line.

## 5. Checked and sound

- **The surrogate screen** (`screen`): fitted only on the run's own earlier generations, no prior from older
  runs; it predicts two of the four objectives, but of 968 screened children measured by its audit none
  reached the final front, against 6.9 expected at the 0.71% rate of the measured; tag-2 share 48.0% screened
  against 46.7% not. No sign of the blind spot suspected.
- Every design timed paired with s6 on the same CPU; fronts re-measured together in one session; verdicts
  same-session; decisions on this VM by deterministic dispatch counts, never its timing; negative controls
  (ans-check, the knockout's control, the size check against the records); predictions written before runs.

## 6. Proposals, the owner's calls, by value

1. Seed 59: keep it as a replicate of seed 58, and build the switch that leaves out the evolved founders for
   the anchoring test after it - or stop it and wait for the switch (section 1).
2. The session's speed from both CPUs (each design's two speeds combined), and the verdict per CPU printed
   beside it - a disagreement called undecided (2b; the audit of 388). Until then the processing routine runs
   `review-checks.py verdicts` on each new session.
3. Re-measure before admitting to the fast end: a design entering the front's fastest tenth measured again
   (more rounds) before it counts - or more rounds in-run there (2a).
4. Top-end agreement beside every Spearman: the fastest tenth's Spearman, or the regret - how much slower
   on held out the selection's pick is than the held-out best (2d).
5. One-line fixes: the verdict table's sign labelled (4a); the 32-bit fastest kept by --frontier (4d).
6. Replicates for configuration questions (3b); "converged within the requirement" in verdicts (3a).
