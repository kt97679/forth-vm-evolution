# Seed 89's 32-bit gain, off the front (Iteration 624)

confirm.py counts the extremes from every alive design (the stopping rule's measure, 556); portable-followup.py narrows
the union's true front to the follow-up's 30, and that front is an ε-front - evolve.py's dominates() takes speeds within
SPEED_TOL (2%) as ties, so a smaller design within 2% removes a faster one. Seed 89's 32-bit gain lies there: ee34931cd7
(0.1580 at 32 bits, 0.1515 at 64, 41,990 B, 224 KB, generation 147, JIT) is dominated so by d8471f1b16 (0.1583, 40,230 B)
and six others, d8471f1b16 by 31f5d0a494 and 3609920444 (results/drafts/gain-designs-624.py). None of the seven bred designs past the bar (0.1610: seed 79's
0.1643 less 2%) is on it - 0.1580-0.1605, generations 123-167, all JIT. The follow-up drafted before the fix listed none
of them: its "fastest at 32 bits" was 88233c0551, 0.1715. The fix: portable-followup.py --jit --seed N lists each design
the run bred past a criterion's bar, from every alive design (here the seven); results/drafts/jit-rehearsal-622.py PASS,
the portable path byte for byte.

Drift (results/drafts/drift-624.py): the 2,398 carried designs measured again in seed 89 read, against their pool
readings, median 1.0009 at 64 bits (quartiles 0.992-1.009) and 1.0056 at 32 (0.995-1.017); seed 79's 147 at 32 bits
1.0057 - seed 89's readings no faster, so the gain is not drift. Its risk is the fast end's optimism: the fastest tenth
re-measured at 1.096 of in-run (curse.txt), and each of the seven has one in-run reading - the follow-up decides.

**The fast end's optimism by run** (Iteration 625; each results file's curse line - the fastest tenth re-measured at the
run's end over its in-run speed, at 64 bits): the JIT runs 1.048-1.096 (seeds 78-86: 1.061, 1.094, 1.070, 1.060, 1.048,
1.089, 1.066, 1.080; seed 89 1.096), the portable runs 1.023 and 1.028 (seeds 87 and 88, 21 hours and more designs) - a
trait of the JIT designs' readings, not of a run's length. Seed 79, whose 0.1643 is the 32-bit bar's base, read 1.094: seed
89's lead is not measured against a less optimistic run; the follow-up re-measures the seven beside the 32-bit holder.
