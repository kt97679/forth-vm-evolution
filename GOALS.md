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
- **Iteration 13: four format-10 words were never there.** The converter's
  exact-body check compared bodies already rewritten by pairs, short
  branches and fused tests: 1,032 of seed 3's 1,145 living designs lost at
  least one word silently - every front design `(LOOP)`, `(+LOOP)`, `(?DO)`
  and `?DUP` (`lab/evolve/scan-bodycheck.py`). Fixed, and the evolver now
  kills a design the check fails. The front's images, converted again:
  99-112 bytes smaller, the selection workloads' dispatches unchanged.
  Seed 3's recorded sizes stand as what that converter made.
- **The held-out loop moves with the image's size mod 8**: code compiled at
  run time pads `(LOOP)`'s operand with 0-7 NOOPs, run on every pass (about
  4% each) - compare designs on loop only at equal size mod 8.
- **Seed 4** (`results/evolve-amd-ryzen-7-pro-8840hs-seed4.md`), with the
  fix, the second escape level, Iteration 12's tests and one-byte calls,
  re-measured: 0.589 at 13,352 bytes (seed 3: 0.595 at 13,464); the small
  end 262-410 bytes smaller, 0.669 at 9,523 to 0.727 at 9,335 (seed 3: 0.622
  at 9,785). One-byte calls on six of the seven front designs.
- **All runs' fronts, by the median, on two CPUs** (Iteration 26,
  `results/compare-fronts-amd-ryzen-7-pro-8840hs.md`): the CPUs agree per
  design within 1.7% (10-90%), rank agreement 0.98. Seven of the eight
  designs on the front of all runs are seed 4's; at the fast end its
  replicate's e99da68667 is 3% faster than seed 3's best and 151 bytes
  smaller; at the small end the speeds tie and seed 4 is 163-311 bytes
  smaller. The two best-of-N sessions before (Iterations 21, 23)
  disagreed by a lucky fib run.
- **The best of N was the fault** (Iteration 25): a rare fib run is 20-38%
  fast - 0.4-2.3% of runs for some designs - and the best of the rounds
  reported it when drawn. The evolver now takes the median of the rounds;
  every speed recorded before is a best of N. The lucky run is not a place
  - no stack offset, randomisation on or off alike (Iteration 27,
  `results/lucky-amd-ryzen-7-pro-8840hs.md`): a lead closed.
- **Seed 4 again - same seed, same code, other noise** (Iteration 22,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed4b.md`): the runs part after
  the 35 starting designs and share 2 more of 1,310, yet reach the same
  kind of front - one-byte calls on all six, the same smallest size
  (9,335) - leaning more on the second escape level. Calibrated well (s6
  1.004, fib 1.020), its re-measure took 0-7% off (the first: 2-20%).
- **Seed 5, selected by the median** (Iteration 28,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed5.md`): the re-measure agrees
  with selection within 4% (seed 4's first run: 2-24%). Every front design
  carries 32 one-byte calls and the second escape level. Against the
  earlier fronts, across sessions so provisionally: 0.593 at 13,073 bytes,
  5% faster than anything before at that size; a new fastest, 0.579 at
  14,017 (scale 2, run-time fusion); ties at 9.45 KB; slower at 9,335.
  *Settled in one session (Iteration 36): 0.585 at 14,017 - dominated by
  seed 4b's 0.582 at 13,201 - and 0.610 at 13,073. Seed 5 shared the front
  with 4b and 3; it set no record.*
- **Seed 6 - the front of all runs** (Iteration 36,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed6.md`; one session with every
  run, calibration 0.996, two CPUs agreeing: `results/compare-fronts-...`,
  session 4): **0.547 at 14,081 bytes, the fastest yet; 0.685 at 9,327,
  the smallest yet**; 4-7% faster than the fastest earlier design no
  larger at most sizes. The first run that could choose Iterations 33-34's
  opcodes: from 3 designs of 29 at the start to 58-80% of the living, and
  on every design of the front - where they remove 9-10% of the
  dispatches on kernel, parse and corpus (counted). fib and loop gain
  nothing from them: their hot code is compiled at run time.
- **Seed 7 - the small end rewritten** (Iteration 40,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed7.md`; session 5, calibration
  1.008): **0.673 at 8,073 bytes - the smallest yet - to 0.550 at 11,777**,
  seven of the eight designs on the front of all runs; seed 6's 0.541 at
  14,081 still the fastest. `lean` on every front design (none had it in
  generation 0); `rtimm` weighed and mostly left - expressed on one, at
  8,957 bytes. Beyond lean's bytes, 2.5-7% faster than seed 6's front with
  lean applied, through the middle.
- **Seed 8 - loop selected** (Iteration 42,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed8.md`; session 6, five
  workloads, calibration 1.003): **0.449 at 13,073 bytes - the fastest yet
  - 0.454 at 9,278, down to 8,034 bytes, the smallest yet**; 14 of the 17
  designs on the front of all runs, 15-27% faster than the fastest earlier
  design no larger from 8.5 KB up. rtloop on every front design from
  8,525 bytes, the loop opcodes taken back (I in 83% of the living): loop
  five times faster than s6. The held-out sieve improved with it
  (0.51-0.66, seed 7's 0.78-0.85): the gains carry over.
- **Seed 9 - the small end, and what does not compound** (Iteration 45,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed9.md`; session 7, calibration
  1.000): **0.794 at 7,019 bytes - the smallest yet - to 0.515 at 7,725**,
  bss on every front design; seed 8 keeps 8,614 bytes and up, the fastest
  0.442. But seed 8's front with bss and rtloopall, built and alive, would
  be 0.508 at 7,178 ... 0.442 at 11,569 - dominating seed 9 from 7,178 up.
  Every run starts from the same founders: progress does not compound.
- **Seed 10 - progress compounds** (Iteration 47,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed10.md`; session 8, calibration
  1.004): the first run to start from the earlier fronts (109 designs
  carried in). **15 of the 16 designs on the front of all runs are its own,
  from 6,977 bytes - the smallest yet - through 0.486 at 7,236 to 0.438
  at 12,145**; 5-26% faster than the fastest earlier design no larger at
  every size, a quarter at 7.1-7.2 KB. Every one descends from carried
  designs. Seed 8's 0.436 at 13,073 is still the fastest.
- **Seed 11 - the Forth sources' batch, timed** (Iteration 52,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed11.md`; session 9,
  calibration 1.007): **all 11 front designs its own: the fastest yet,
  0.413 at 8,030 bytes; the smallest, 6,971; 0.433 at 7,238** - 9-30%
  faster than anything earlier at every size, on kfast and CMOVE alone.
  THREAD-FIND, the largest saving, met kfast once in 1,425 designs: the
  gene `tfind` puts it first.
- **Seed 12 - THREAD-FIND taken up** (Iteration 53,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed12.md`; session 10,
  calibration 0.994): **all 12 front designs its own: the fastest yet,
  0.326 at 9,014 bytes; 0.331 at 7,958; 0.379 at 7,105; the smallest,
  6,941** - 17-32% faster than anything earlier at every size. THREAD-FIND
  on 11 of the 12 (tfind from generation 7); parse at 0.21-0.28 of s6.
- **One-byte calls, built (Iteration 14)**: the gene `hotcalls` - the
  far-call prefixes 0xE0-0xFF call the image's own most-called words
  through a table in its header. 143-319 bytes on seed 3's front (1.1-3.3%;
  priced 136-320), no dispatch removed; every engine form lives; engines
  without it are byte-identical.

## Next, in order

Iteration 48, the owner: the improvements first, the Tegra session once
they are done, the article on the backburner.

1. **Improvements, on the development VM** - each priced before it is
   built; a change that would alter a recorded design's image goes behind
   a gene, as lean and bss did. Between batches, a seed run carrying the
   earlier fronts (one laptop sitting, run then comparison).
   a. **The Forth sources** (the owner, Iteration 48): look through
      forth/kernel.4, cv8.4, cv8b.4 and the overlays for simplifications
      and optimisations. The image's code is mostly the kernel's - 6,610
      of the 7,881 bytes of words in Iteration 44's audit - and kernel,
      parse and corpus run it: a shorter or faster definition there is a
      gain in every design. Words the converter already rewrites (and the
      hand-made stages, which must stay identical) set the limits.
      **Begun (Iteration 49, `results/kfast.md`)**: every dispatch
      attributed to its word - a quarter of kernel, parse and corpus was
      NAME>BUF's zero fill; without it (the gene `kfast`, byte headers),
      24-29% fewer dispatches there. FILL and CMOVE as opcodes, their
      colon bodies too (Iteration 50): kernel 0.865, corpus 0.917, the
      held-out sieve 0.848 more, 32 bytes less. The thread walk as one
      opcode, THREAD-FIND (Iteration 51): parse 0.489, corpus 0.631,
      kernel 0.799 more - from the design as recorded, parse 0.34, corpus
      0.42, kernel 0.53 of the dispatches. Seed 11 (Iteration 52): the
      fastest yet, 0.413 at 8,030 - without THREAD-FIND, never taken up;
      `tfind` puts it first. Seed 12 (Iteration 53): taken up - the
      fastest yet, 0.326 at 9,014; 17-32% faster at every size. The input
      side (Iterations 54-55): the gene `kinput` - kernel 0.62, parse
      0.65, corpus 0.61 counted. **NEXT-RUN: seed 13, then compare.**
      Next in the sources: number conversion (NUMBER?, >NUMBER, DIGIT?:
      17% of parse), FIND's search-order loop, then what is left
      (REFILL, SCAN, PARSE: a quarter of kernel); the cell-header
      NAME>BUF (open).
   b. **The image's remaining fixed costs** (Iteration 44's audit): the
      353-byte image header (32 thread heads as cells), FORTH-WORDLIST's
      32 cell-sized heads (296 bytes), the names (a third of the image),
      NAMEBUF.
   c. **The register machine's tail**: the return-stack moves (13-16% of
      dispatches) and the long tail of move patterns
      (`results/price-register-stage1.md`).
2. **The Tegra session - once the improvements are done** (the owner).
   SPN on 32-bit ARM is correct under qemu (Iterations 30-31). Before the
   Tegra can time it: the build makes s8 only from 8-byte images
   (mk-spn-cv8-image.sh; s8-*-32 on an ARM host), and bench-laptop.sh
   skips SPN off x86-64. Then one sitting: tools/arm-qemu-check.sh
   natively, the stage ladder timed, SPN against the interpreter.
3. **The article - on the backburner** (the owner, Iteration 48):
   `article/`; prompts/14-audience-research before drafting for Habr and
   ForthHub, 04 and 05 before publishing.

### Built from this list, for the record

- **The fronts carried into every run** - built (Iteration 46, the
   owner's go): `evolve.py --carry DB,...` puts each database's own front
   into the first generation beside the founders, every one timed again;
   next-run.sh passes every archived database. compare-fronts.py credits a
   carried design to the run that found it. Seed 10 (Iteration 47): every
   front design descends from carried ones; 5-26% faster at every size.
- **fib and loop: code compiled at run time** - built (Iteration 37) as the
   gene `rtimm`: the run-time compiler makes `n +` an ADDI and `SWAP n +` a
   SWAP+I, as the converter does in the image (`results/rtimm.md`): fib
   15% fewer dispatches, 17-27% faster, selection 5-8% faster on the
   front's run-time-fusion designs - for 408-472 bytes, so a gene. For a
   seed run to weigh, batched with whatever else needs the laptop next.
   **And the gene `lean` (Iterations 38-39)**: build artifacts left out
   of the image - 12-16% of every CV8 image, no slower
   (`results/lean.md`). Both weighed by seed 7 (Iteration 40): lean taken
   everywhere, rtimm where fib's gain paid.
   **Loops (Iteration 41, the owner's call)**: the gene `rtloop` - the
   run-time compiler emits the design's loop opcodes, each where it has
   one (`results/rtloop.md`): loop 2-4x faster, 57-80% fewer dispatches,
   for about 6% of the image. **And loop is in the selection now**, with
   `bench/sieve.fth` held out in its place. Seed 8 (Iteration 42) took both
   - loop five times faster, the sieve carried along.
   **And `rtloopall` (Iteration 43)**: for a design with all eight loop
   opcodes - most of seed 8's rtloop designs - a compact run-time loop
   compiler, 380-488 bytes less, the same speed (`results/rtloopall.md`):
   fast loops for about 100 bytes. **And `bss` (Iteration 44)**: an audit
   of a small image found three scratch buffers stored in it; out of the
   file, 1,056-1,064 bytes (11-13%), not a dispatch more
   (`results/bss.md`) - seed 8's smallest would be 6,970 bytes. **NEXT-RUN:
   seed 9, then every front compared** - both for evolution to take.
- **A register machine** - priced (Iteration 29,
   `results/price-register-machine.md`): up to 38-50% of the front designs'
   dispatches only move values or push a lone literal - the largest prize
   left, and the largest work: operands in every instruction, a
   stack-to-register translation in the converter, register handlers in
   every engine family, the run-time compiler. Its first stage priced
   exactly (Iteration 32, `results/price-register-stage1.md`): register
   forms within a block would remove 19-24% of the front designs' image
   dispatches - and 5-8 patterns give 80% of that, led on every workload
   by `DUP ?BRANCH` (6%) and `SWAP addi` (4-5%): operand-carrying, so the
   pairs could never fuse them. Built (Iterations 33-34): `DUP ?BRANCH`,
   `OVER ?BRANCH`, `DUP 0= ?BRANCH` kept and `SWAP n +` as opcodes and a
   gene - image against image about 10% fewer dispatches on kernel, parse
   and corpus, 40 bytes, selection 0.951 on the VM; net of the seven pairs
   they displace on 8dc0f97f2c, 6-7% fewer dispatches
   (`results/fused-keep-tests.md`). For evolution to weigh: a seed run
   with them - with the comparison of all fronts, one laptop session.
   Beyond: the run-time compiler could fuse them too (fib's code), and
   the register machine proper is the long tail and the return stack.

## Rejected or deferred - look here first

| approach | what decided it | where |
|---|---|---|
| The loop opcodes in code compiled at run time | priced, not built (Iteration 28): 0.1% of kernel's dispatches, 0.8-1% of corpus's, none on fib or parse; 68-70% of the held-out loop's, which building it for would spoil | `results/price-runtime-loops.md` |
| A reach check for far calls in cv8.4 | measured, not built (Iteration 28): the workloads run code up to 68 KB, the far form reaches 2 MB (one-byte calls) to 4 MB; a check costs every image bytes | `results/price-runtime-loops.md` |
| Indirect threading as a gene | priced, not built (Iteration 29): in the dispatch lab its dispatch lands in token and direct threading's band; its code is a cell a reference, beside s0-cell's 25 KB - dominated | `lab/dispatch/README.md` |
| One-byte calls in the pairs' slots | priced, not built (Iteration 13): the pairs with the fewest static sites are among the hottest - four of them carry 3-8% of the dispatches, for 24-120 bytes; the far-call prefix band costs no slot | `results/price-hotcalls-seed3-front.md` |
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
