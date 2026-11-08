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
