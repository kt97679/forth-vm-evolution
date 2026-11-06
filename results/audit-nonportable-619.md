# The audit: another run with non-portable (JIT) designs? (Iteration 619)

The owner asked for a deep audit of the results so far and whether another run with non-portable engines is worth it.

## The results so far, checked

- **Correctness**: none open (576). Seed 88's checks on master: the gate 469 of 469 alive, ans-check 0 of 106 differ from
  s6, its two deaths values retired at 599 and refused the same here (615).
- **Measurement**: the fast end's in-run numbers run lucky (seed 88: the fastest tenth 1.028 re-measured / in-run, its
  fastest 1.08); the stopping rule compares in-run with in-run, and roles are decided on re-measures paired by session
  (the follow-ups: 2% at 5 SE or more on every line).
- **Across machines**: one systematic effect, explained (614; results/dream32-experiment-seed88.md): GCC's 4-byte-cell
  builds run 1.6-2.2 times the laptop's time on dream (Skylake), clang's 1.1-1.2 times, so the laptop's selection keeps GCC
  at 32 bits; the class picks (x86-32: the laptop and dream) absorb it. The four JIT roles are clang builds - untouched.

## The non-portable (JIT) search

- **The series**, seeds 77-83 from scratch, 9-12 hours, 126-178 generations: the stopping rule stopped at 83 (572); the
  fastest in-run 0.1377-0.1477 a run (results/stopping-series.md).
- **The confirmation runs from the pool**, 12 hours each: seed 84 gained at the fast end only, by a hair and on the laptop
  alone (dream disagreed - 582), fastest 0.1325; seed 86 gained nothing from its search - not confirmed only by a carried
  design's 4 KB of memory, fastest 0.1330.
- **Nothing new since**: no gene's definition names an iteration after 540 (44 genes, lab/evolve/evolve.py); the
  consolidation (599) only removed values. A JIT run now searches the space seed 86 searched.

## Could the portable runs' gains carry over to the JIT?

- **The JIT needs the two-bit tag and the top-of-stack register**: evolve.py's founder note (441: the JIT needs the tag);
  c7c35f9c97 with tos=0 expresses no JIT (checked here).
- **No portable front design has both**: seed 88's 469 - no tag and tos 0 353, no tag and tos 1 112, the tag and tos 0
  4, both 0; seed 87's 377 - 274, 99, 4, 0. Without the JIT that base loses, so the portable search never improves it.
- **The portable winners' interpreter genes**: the run-time immediates (rtimm) fit a JIT design (expressed with it) and
  none of the four JIT roles has them - but the gene was there through the whole JIT series; rtfuse is dropped with the
  JIT, regpin and lto with clang.
- **The JIT designs' own interpreter, JIT off** (their ARMv7 readings, results/final-pick-chainCD-seed86.md): 0.456-0.540
  against 690981ca5b's 0.327 - weaker, but on the Tegra, where these roles do not run.
- **How much a JIT design still interprets on x86 today is not known**: JIT.md's 44.5-46.6% of the kernel's dispatches is
  Iteration 90's; lab/evolve/callsites.py, which measured it, stops on today's designs (c7c35f9c97: its census audit).

## The prize

The JIT roles against the best portable design, re-measured (in different chains, each against s6 in its sessions):
x86-64 c7c35f9c97 0.1848 against 782f3ad7ff 0.3428 (1.85 times as fast), x86-32 4ef851fd8e 0.1989 against 0.3387 (1.70).

## The one lever never tested: the length

The JIT runs never passed 178 generations; the portable search found seed 87's winners at generations 171 and 258 and
seed 88's 32-bit fastest at 157, in 21-hour runs from the pool.

## Verdict

No sign of progress to be had from a JIT run now: the search converged by its own rule, nothing new reached it since, and
the portable runs' gains lie where the JIT cannot go. By the owner's rule (618: evolve while there is progress), not now.
If the length is to be settled before the freeze: one 21-hour JIT run from the JIT pool, judged by the confirmation rule
(GOALS.md step 2), its follow-up re-measuring its best beside the four x86 roles - the last step before the freeze, and
continued only on confirmed progress (the 618 rule).
