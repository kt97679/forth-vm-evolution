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
- Seed 2 on the Ryzen (`results/evolve-amd-ryzen-7-pro-8840hs-seed2.md`)
  found the same front as seed 1, re-measured: 0.619 at 13,472 bytes
  (seed 1: 0.609), 0.667 at 9,761 (0.649 at 9,801) - the same genes. The
  Ryzen sample of 128: the run's best beats every random design. The
  generator fix left s6's speed unchanged on the Ryzen too (pinned, each
  row calibrated: fib 0.977, parse 0.997, corpus 0.994).
- Seed 3, with fused tests and the flag genes
  (`results/evolve-amd-ryzen-7-pro-8840hs-seed3.md`), re-measured: 0.595
  at 13,464 bytes, 0.622 at 9,785 - 2-4% and 4-7% past seeds 1 and 2;
  every front design keeps all eight fused-test opcodes, at the pairs'
  cost (13 left). The jail and the scale-0 rule held: 129 declined unrun.

## Next, in order

1. **One-byte calls through a table of hot words** - priced first: mostly
   size (a call is 2-3 bytes), so count the static call sites by target.
2. **A fourth run on the Ryzen** with what has been added since seed 3:
   the second escape level (works, does not pay alone), the five further
   fused tests (Iteration 12: 1-2% fewer dispatches, 48 bytes smaller) -
   selection weighs them together.
3. Remaining planned gene: indirect threading; then a register machine.
4. The article (`article/`): prompts/14-audience-research before drafting
   for Habr and ForthHub; 04 and 05 before publishing.
5. ARM port of SPN. Push master to GitHub (the owner's step).

## Rejected or deferred - look here first

| approach | what decided it | where |
|---|---|---|
| Native code in the genome: relf's native compiler as a family of its own, or our SPN with relf's rules as genes | deferred by the user (Iteration 4) after measuring it (Iteration 3): our corpus byte for byte, our kernel workload a segmentation fault in cross.4's RESOLVE, 3-10 times faster than s6 on the VM | PROGRESS.md, Iterations 3 and 4 |
| Profile-guided optimisation of the engine as a gene | measured, not built (Iteration 7): 0.903 on s6 only when trained on the measured workloads; trained on a separate program, 0.980 - what -fprofile-use's flags give without a profile; three of those flags became genes instead | `lab/evolve/GENES.md`; `lab/evolve/pgo-train.fth` |
| A second escape level - nine more primitives behind ESC for nine slots | built, measured, does not pay (Iteration 11): with the design's own best pairs in the slots, 0.2-2.4% fewer dispatches - price.py's 6.4-12.9% counted overlapping pairs; kept as a gene for selection | `lab/evolve/GENES.md` |
| Triples - three operations as one opcode | priced, not built (Iteration 8): at most 0-4.9% of dispatches on the front, none on fib, before overlaps and slots - tests before branches came out larger | `lab/evolve/GENES.md`; `lab/evolve/price.py` |
| Load-time direct threading (a decode cache invalidated on every store) | deferred, not built: the dispatch lab gave direct over token threading -5% fib, -12% sieve, but +9% loop; relf S8 found dispatch already at the indirect-jump rate | `lab/evolve/GENES.md` 1; `lab/dispatch/README.md` |
| Run-time fusion of pairs (`rtfuse`) | built, kept as a gene, selection rejects it: +560-576 bytes, s6 with two pairs 0.956 -> 0.970 (VM) | 53017b4; `lab/evolve/README.md` phase 2b |
| READ/WRITE stencils making the system call themselves | not built: they would bypass the engine's buffers (`t_obuf`, `t_ibuf`) | 973435c; `FINDINGS-SPN.md` |
| ACCEPT with READ stopping only at LF and CR, every byte examined in Forth | built, 3-11% SLOWER, replaced by READ stopping at every special character | e223d8e; `FINDINGS-OUTER-INTERPRETER.md` |
| @XT, a fused @ EXECUTE | not built: no `@ EXECUTE` in the image's code | 93849f3 |
| Multi-state caching with 25 operations specified | built, lost (s6 1.049, s5 1.110, VM): the normaliser's second dispatch; kept with 72 operations and composed pairs | 28dc163, 4512665 |
| A retry for "transient" conversion failures | added on a wrong diagnosis, removed: the cause was the raw genome built under the canonical identity | 9d46ba3 -> 679e6f3 |
| "Multi-state caching buys less on Zen 4" | an inference from 8 re-measured designs, retracted: every design on the Ryzen's front has it | 679e6f3; `lab/evolve/REHEARSAL.md` |
| Two top-of-stack registers always; real calls and returns for dispatch | lost in the dispatch lab (before this register) | `lab/dispatch/README.md` |
