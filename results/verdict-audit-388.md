# The verdicts audited: does "small" depend on which CPU is asked? (Iteration 388)

The methodology review (results/review-methodology-386.md, 2b) found the verdict's measures moving by several
points between the two CPUs of one session. This audit asks what that did to the verdicts themselves. Every
session since the five-measure rule (Iteration 188) - 16 of them - rebuilt from its own tables by
`lab/evolve/review-checks.py verdicts` (compare-fronts' hypervolume, its numpy path, copied verbatim), checked
against the printed verdict, then computed from cpu 2's measurements alone and from cpu 8's alone.

**The verdict reads one CPU.** compare-fronts.py measures every design on both CPUs but takes the session's
speed from the first alone (`c0 = cpus[0]; t, speed = T[c0], S[c0]`): the verdict, the fronts, the Q-best and
the gate's joint front all rest on cpu 2; cpu 8's six rounds a design - half of every session - feed only the
section comparing the two. The rebuild "from cpu 2 alone" equals the printed verdict in every session.

**What the noise did: 2 of 16 verdicts depend on the CPU, and no decision rested on either.**

- 15 of 16 printed verdicts rebuilt exactly; the 16th, session 45 (seed 51), printed "fastest +4.9%" against
  the 5% bar, rebuilt +5.1% from speeds printed to three decimals - a knife edge, the bar inside the rounding.
- The two CPUs agree in 14. Session 44 (seed 50): small on cpu 2, not on cpu 8 (best Q +0.2% / +2.1%).
  Session 45 (seed 51): small as printed by 0.1 points of cpu 2's fastest; cpu 8 +0.7%.
- Both were followed at once by new genes (the after-seed-50 and after-seed-51 batches), which restart the
  stopping rule's count: no stop or continue turned on them. The rule's one recent end - seeds 53, 54 and 55
  small (sessions 47-49) - holds on both CPUs, as do the other twelve.

So the measures are noisy (review 2b stands: the fastest moves up to 5.4 points, best Q up to 6.2), but past
verdicts were mostly decided by margins well clear of the bars - a hypervolume of +22% or an extreme of
+12%, or every measure inside them. The risk is the knife edge, two in sixteen so far.

**Proposals** (the owner's calls): the session's speed from both CPUs - each design's two per-CPU speeds
combined (their geometric mean), the second CPU's half of the session no longer idle; and the per-CPU verdicts
printed beside it, a disagreement called undecided. Until then the processing routine runs this check on each
new session (HANDOFF, "Processing a returned seed", step 2).

---

session 37 (Iteration 209), 422 designs, 422 on both CPUs
  printed      -7.0%  +0.18%  +6 KB  +4.8%  +0.5%  not small
  rebuilt      -6.9% +0.18% +6 KB +4.8% +0.5%  not small
  cpu 2 alone  -6.9% +0.18% +6 KB +4.8% +0.5%  not small
  cpu 8 alone  -5.8% +0.18% +6 KB +5.0% -1.9%  not small
session 38 (Iteration 215), 406 designs, 406 on both CPUs
  printed      -1.9%  +12.26%  +4 KB  +22.4%  +9.3%  not small
  rebuilt      -1.6% +12.26% +4 KB +22.4% +9.4%  not small
  cpu 2 alone  -1.6% +12.26% +4 KB +22.4% +9.4%  not small
  cpu 8 alone  -2.2% +12.26% +4 KB +22.6% +9.6%  not small
session 39 (Iteration 230), 364 designs, 364 on both CPUs
  printed      -0.6%  +0.00%  +0 KB  +0.9%  -0.2%  small
  rebuilt      -0.5% +0.00% +0 KB +0.9% -0.0%  small
  cpu 2 alone  -0.5% +0.00% +0 KB +0.9% -0.0%  small
  cpu 8 alone  +2.3% +0.00% +0 KB +1.0% -2.7%  small
session 40 (Iteration 240), 331 designs, 331 on both CPUs
  printed      +0.9%  +0.54%  +4 KB  +6.2%  -1.6%  not small
  rebuilt      +1.1% +0.54% +4 KB +6.2% -1.3%  not small
  cpu 2 alone  +1.1% +0.54% +4 KB +6.2% -1.3%  not small
  cpu 8 alone  +0.0% +0.54% +4 KB +5.8% -2.1%  not small
session 41 (Iteration 248), 314 designs, 314 on both CPUs
  printed      -1.1%  +0.15%  +2 KB  +6.4%  -3.4%  not small
  rebuilt      -1.1% +0.15% +2 KB +6.4% -3.2%  not small
  cpu 2 alone  -1.1% +0.15% +2 KB +6.4% -3.2%  not small
  cpu 8 alone  -2.2% +0.15% +2 KB +6.2% -5.4%  not small
session 42 (Iteration 269), 300 designs, 300 on both CPUs
  printed      +2.5%  +0.05%  -2 KB  +1.4%  -2.1%  small
  rebuilt      +2.3% +0.05% -2 KB +1.4% -2.1%  small
  cpu 2 alone  +2.3% +0.05% -2 KB +1.4% -2.1%  small
  cpu 8 alone  +2.8% +0.05% -2 KB +1.4% +0.4%  small
session 43 (Iteration 288), 356 designs, 356 on both CPUs
  printed      -4.1%  +0.00%  -4 KB  +4.0%  -3.9%  not small
  rebuilt      -4.0% +0.00% -4 KB +3.9% -3.5%  not small
  cpu 2 alone  -4.0% +0.00% -4 KB +3.9% -3.5%  not small
  cpu 8 alone  -0.7% +0.00% -4 KB +4.6% -4.3%  not small
session 44 (Iteration 296), 380 designs, 380 on both CPUs
  printed      -0.1%  +0.16%  -2 KB  +0.4%  +0.2%  small
  rebuilt      +0.0% +0.16% -2 KB +0.4% +0.2%  small
  cpu 2 alone  +0.0% +0.16% -2 KB +0.4% +0.2%  small
  cpu 8 alone  -0.7% +0.16% -2 KB +0.4% +2.1%  not small
session 45 (Iteration 300), 397 designs, 397 on both CPUs
  printed      +4.9%  +0.00%  +0 KB  +1.7%  +0.8%  small
  rebuilt      +5.1% +0.00% +0 KB +1.7% +0.6%  not small
  cpu 2 alone  +5.1% +0.00% +0 KB +1.7% +0.6%  not small
  cpu 8 alone  +0.7% +0.00% +0 KB +1.4% -4.3%  small
session 46 (Iteration 310), 407 designs, 407 on both CPUs
  printed      +1.8%  +0.00%  +0 KB  +0.5%  -1.9%  small
  rebuilt      +2.2% +0.00% +0 KB +0.5% -1.6%  small
  cpu 2 alone  +2.2% +0.00% +0 KB +0.5% -1.6%  small
  cpu 8 alone  +3.0% +0.00% +0 KB +0.7% -3.8%  small
session 47 (Iteration 320), 367 designs, 367 on both CPUs
  printed      -5.8%  +0.00%  -4 KB  +0.3%  -5.3%  small
  rebuilt      -5.6% +0.00% -4 KB +0.2% -5.3%  small
  cpu 2 alone  -5.6% +0.00% -4 KB +0.2% -5.3%  small
  cpu 8 alone  -6.5% +0.00% -4 KB +0.2% -0.8%  small
session 48 (Iteration 333), 368 designs, 368 on both CPUs
  printed      +3.6%  +0.05%  -2 KB  +1.1%  +0.9%  small
  rebuilt      +3.7% +0.05% -2 KB +1.1% +0.6%  small
  cpu 2 alone  +3.7% +0.05% -2 KB +1.1% +0.6%  small
  cpu 8 alone  -0.7% +0.05% -2 KB +1.0% -0.3%  small
session 49 (Iteration 334), 370 designs, 370 on both CPUs
  printed      +3.1%  +0.00%  +0 KB  +0.4%  -2.5%  small
  rebuilt      +3.0% +0.00% +0 KB +0.4% -2.5%  small
  cpu 2 alone  +3.0% +0.00% +0 KB +0.4% -2.5%  small
  cpu 8 alone  +2.3% +0.00% +0 KB +0.5% -1.3%  small
session 50 (Iteration 354), 383 designs, 383 on both CPUs
  printed      -4.1%  +0.04%  +0 KB  +1.3%  -0.9%  small
  rebuilt      -4.3% +0.04% +0 KB +1.3% -0.7%  small
  cpu 2 alone  -4.3% +0.04% +0 KB +1.3% -0.7%  small
  cpu 8 alone  -5.8% +0.04% +0 KB +1.3% +0.6%  small
session 51 (Iteration 378), 417 designs, 417 on both CPUs
  printed      +3.9%  +0.00%  +0 KB  +2.0%  +1.2%  small
  rebuilt      +3.9% +0.00% +0 KB +2.0% +1.3%  small
  cpu 2 alone  +3.9% +0.00% +0 KB +2.0% +1.3%  small
  cpu 8 alone  -0.8% +0.00% +0 KB +1.8% +0.3%  small
session 52 (Iteration 384), 433 designs, 433 on both CPUs
  printed      -3.4%  +10.51%  +4 KB  +11.1%  -5.3%  not small
  rebuilt      -3.8% +10.51% +4 KB +11.1% -5.1%  not small
  cpu 2 alone  -3.8% +10.51% +4 KB +11.1% -5.1%  not small
  cpu 8 alone  +1.6% +10.51% +4 KB +11.1% -4.0%  not small

| session | iteration | printed | rebuilt | cpu 2 alone | cpu 8 alone | the CPUs agree |
|---|---|---|---|---|---|---|
| 37 | 209 | not small | not small | not small | not small | yes |
| 38 | 215 | not small | not small | not small | not small | yes |
| 39 | 230 | small | small | small | small | yes |
| 40 | 240 | not small | not small | not small | not small | yes |
| 41 | 248 | not small | not small | not small | not small | yes |
| 42 | 269 | small | small | small | small | yes |
| 43 | 288 | not small | not small | not small | not small | yes |
| 44 | 296 | small | small | small | not small | **no** |
| 45 | 300 | small | not small | not small | small | **no** |
| 46 | 310 | small | small | small | small | yes |
| 47 | 320 | small | small | small | small | yes |
| 48 | 333 | small | small | small | small | yes |
| 49 | 334 | small | small | small | small | yes |
| 50 | 354 | small | small | small | small | yes |
| 51 | 378 | small | small | small | small | yes |
| 52 | 384 | not small | not small | not small | not small | yes |

16 sessions: the printed verdict rebuilt in 15; the two CPUs alone agree in 14.

## Under the owner's rule of Iteration 389 - the speed from both CPUs

The owner chose to judge by both CPUs (each design's speed the geometric mean of its two; applied in
compare-fronts.py at 389). The same 16 sessions by that rule (`review-checks.py verdicts`, its "both CPUs"
line): **15 give the printed verdict**. The one that changes is session 44, seed 50 - small as printed (cpu 2),
not small from both: best Q +2.7%, more than either CPU alone (+0.2% and +2.1%), as a minimum over designs
need not lie between its per-CPU values - a different design can become each side's best. No decision turned
on it: the after-seed-50 batch's new genes followed at once. Seed 51's knife edge reads small. Seed 58's
fastest, from both CPUs, is 0.4% behind the others', not 3.4%.

| session | iteration | printed | rebuilt | cpu 2 alone | cpu 8 alone | the CPUs agree | both CPUs (the rule from 389) |
|---|---|---|---|---|---|---|---|
| 37 | 209 | not small | not small | not small | not small | yes | not small |
| 38 | 215 | not small | not small | not small | not small | yes | not small |
| 39 | 230 | small | small | small | small | yes | small |
| 40 | 240 | not small | not small | not small | not small | yes | not small |
| 41 | 248 | not small | not small | not small | not small | yes | not small |
| 42 | 269 | small | small | small | small | yes | small |
| 43 | 288 | not small | not small | not small | not small | yes | not small |
| 44 | 296 | small | small | small | not small | **no** | not small |
| 45 | 300 | small | not small | not small | small | **no** | small |
| 46 | 310 | small | small | small | small | yes | small |
| 47 | 320 | small | small | small | small | yes | small |
| 48 | 333 | small | small | small | small | yes | small |
| 49 | 334 | small | small | small | small | yes | small |
| 50 | 354 | small | small | small | small | yes | small |
| 51 | 378 | small | small | small | small | yes | small |
| 52 | 384 | not small | not small | not small | not small | yes | not small |

16 sessions: the printed verdict rebuilt in 15; the two CPUs alone agree in 14; both CPUs give the printed verdict in 15.
