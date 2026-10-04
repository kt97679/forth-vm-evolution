# Goals - where things stand, and what is next

The present. It shrinks as things are done; the past is in `PROGRESS.md`
(append-only) and the git log. Check the register at the bottom before
trying anything again (prompts/12-progress-log).

## Conventions

- **Each handoff's last commit is titled `Iteration N: ...`**, N counting
  handoffs, not commits - from Iteration 1 (the handoffs before it were
  not numbered).
- **The bundle**: `tools/make-bundle.sh DIR` names it
  `forth-vm-evolution-claude-iterN-YYYYMMDD-HHMMSS.bundle` (UTC, N from
  HEAD's subject), with HEAD and master, and checks that it clones to the
  same HEAD. Example: `forth-vm-evolution-claude-iter1-20261003-180000.bundle`.
- **Every commit builds and passes `tools/run-tests.sh`.**

## Where things stand

- 15 systems, two cell widths, pass the 616-case ANS CORE corpus; every
  image is reproducible (`tools/check-reproducible.sh`).
- The evolution lab (`lab/evolve`) searches CV8-family designs: encodings,
  switches, folds, specialisations, superinstructions from each design's
  own profile, relf's format-10 opcodes, the escape, short branches, tail
  calls, multi-state stack caching, compiler flags. Fitness: the engine
  process's CPU time over hand-made s6's, paired run by run; and size.
- First run on the Ryzen 7 PRO 8840HS
  (`results/evolve-amd-ryzen-7-pro-8840hs-seed1.md`): measured again,
  0.609 of s6's CPU time at 13,480 bytes; 0.649 at 9,801 - smaller than
  s6. The VM rehearsal's front, re-measured there, reached 0.605.
- What carries it (`results/evolve-knockout-amd-ryzen-7-pro-8840hs.md`):
  the escape and the pairs it makes room for (+28-37% when undone),
  superinstructions (+17-35%), guard pages (+9-19%), format-10 opcodes
  (+6-14%), no endbr64 (+6-13%); multi-state caching only 2-9%.
- The gene pool searched, not recited (`lab/evolve/SEARCH-SPACE.md`): 11
  axes, 66 values, 31 left out - each decided. A uniform sample of 32
  (VM): median 1.59 times s6's time, 1 in 30 faster than s6; the run's
  best beats all of them - the front is a peak, not a plateau.

## Next, in order

1. **On the Ryzen** (the owner's runs, `lab/evolve/RUNNING.md`): the
   second run, `--seed 2`, the first database moved aside; then
   `--sample 128 --rounds 3` - the uniform sample at a size that can say
   where the front stands (`lab/evolve/SEARCH-SPACE.md`, step 5).
2. **The next genes, from `lab/evolve/SEARCH-SPACE.md`**: of its 14
   candidates and 4 deliberate strangers, first those cheap to try and
   likely to matter - profile-guided optimisation of the engine; triples;
   two escape levels; one-byte calls through a table of hot words (a
   stranger).
3. Remaining planned gene: indirect threading; then a register machine.
4. The article (`article/`): prompts/14-audience-research before drafting
   for Habr and ForthHub; 04 and 05 before publishing.
5. ARM port of SPN. Push master to GitHub (the owner's step).

## Rejected or deferred - look here first

| approach | what decided it | where |
|---|---|---|
| Native code in the genome: relf's native compiler as a family of its own, or our SPN with relf's rules as genes | deferred by the user (Iteration 4) after measuring it (Iteration 3): our corpus byte for byte, our kernel workload a segmentation fault in cross.4's RESOLVE, 3-10 times faster than s6 on the VM | PROGRESS.md, Iterations 3 and 4 |
| Load-time direct threading (a decode cache invalidated on every store) | deferred, not built: the dispatch lab gave direct over token threading -5% fib, -12% sieve, but +9% loop; relf S8 found dispatch already at the indirect-jump rate | `lab/evolve/GENES.md` 1; `lab/dispatch/README.md` |
| Run-time fusion of pairs (`rtfuse`) | built, kept as a gene, selection rejects it: +560-576 bytes, s6 with two pairs 0.956 -> 0.970 (VM) | 53017b4; `lab/evolve/README.md` phase 2b |
| READ/WRITE stencils making the system call themselves | not built: they would bypass the engine's buffers (`t_obuf`, `t_ibuf`) | 973435c; `FINDINGS-SPN.md` |
| ACCEPT with READ stopping only at LF and CR, every byte examined in Forth | built, 3-11% SLOWER, replaced by READ stopping at every special character | e223d8e; `FINDINGS-OUTER-INTERPRETER.md` |
| @XT, a fused @ EXECUTE | not built: no `@ EXECUTE` in the image's code | 93849f3 |
| Multi-state caching with 25 operations specified | built, lost (s6 1.049, s5 1.110, VM): the normaliser's second dispatch; kept with 72 operations and composed pairs | 28dc163, 4512665 |
| A retry for "transient" conversion failures | added on a wrong diagnosis, removed: the cause was the raw genome built under the canonical identity | 9d46ba3 -> 679e6f3 |
| "Multi-state caching buys less on Zen 4" | an inference from 8 re-measured designs, retracted: every design on the Ryzen's front has it | 679e6f3; `lab/evolve/REHEARSAL.md` |
| Two top-of-stack registers always; real calls and returns for dispatch | lost in the dispatch lab (before this register) | `lab/dispatch/README.md` |
