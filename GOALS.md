# Goals - where things stand, and what is next

The present. It shrinks as things are done; the past is in `PROGRESS.md`
(append-only) and the git log. Check the register at the bottom before
trying anything again (prompts/12-progress-log).

## The aim - simplicity and minimalism

**Simplicity and minimalism are this project's main goal** (the owner,
2026-10-06, Iteration 72): the smallest, simplest system that does the
job - small images, a small and plain engine, few mechanisms, each one
easy to read and to remove. Speed is welcome where it costs little; it
does not justify complexity on its own.

How it decides things:
- **A mechanism earns its place by measurement**, and goes behind a gene
  so that evolution - and the reader - can see what it buys. If it buys
  nothing, it comes out (`rtlit`, Iteration 59).
- **Of two ways to the same result, the simpler one**, even at a small
  cost in speed or bytes; of two designs equally fast and small, the one
  with fewer mechanisms.
- **Complexity is a cost to count, not only to avoid.** The fitness is CPU
  time and IMAGE size; since Iteration 73 every design's ENGINE code
  (its binary's .text) and peak memory (resident, per workload) are
  recorded and reported beside them - tracked, not scored. Anything that
  grows either must show it: the tag added 5.6 KB of engine code to the
  fastest design (39.9 -> 45.5 KB), its peak memory unchanged (1.44 MB).

## Resuming in a new chat (Iteration 85)

Everything a new session needs is in the repository. Upload the newest
bundle (`forth-vm-evolution-claude-iterN-*.bundle`) and any packs not yet
analysed (`runs/forth-vm-evolution-*.tar.gz`), and say: "continue from
GOALS.md". **The fronts' genomes are in results/ (Iteration 87)**: every
run's report ends with "The front's genomes", one JSON line per front
design (its database record without the raw timings), and a tool that
takes `--db` reads a report as a database - so no database needs
uploading to rebuild a design of any front. Seeds 19-23 were filled in
from the owner's databases (158 designs, every one on the front of all
runs); from seed 24 on, `evolve.py --report` writes the section, and the
report goes to results/ as always. Read first: this file (the aim, the objectives, where things
stand, the register), `lab/evolve/NEXT-RUN`, `JIT.md`, the newest
`PROGRESS.md` entries, `lab/evolve/GENES.md`. The owner's standing
preferences are written here: simplicity and minimalism first; three
equal objectives (memory within 8 KB a tie); each mechanism priced before
it is built, behind a gene; laptop runs via next-run.sh, packs in runs/.

**Where it stands (Iteration 86)**: evolution has STOPPED - seeds 22 and
23 both small, the gene set with the JIT converged (front of all runs: 35
designs, fastest 2cbcf427f6 0.195 at 42,816 bytes). `lab/evolve/NEXT-RUN`
says `none`: the laptop rests until there are new genes.
**Since (Iteration 92)**: two new genes built, `hotinl` and `opbody`
(results/hotinl-opbody.md: on the fast designs about size-neutral for
9-10% fewer dispatches on parse and corpus); NEXT-RUN says `seed 24 tag2`
(then the comparison) - the stopping rule counts afresh. **Iteration 93**:
`night` after the seed in next-run.sh - population 96, 80 generations, ~3
hours (lab/evolve/RUNNING.md): the front (38-46 designs) had outgrown the
population of 32. **Seed 24** (Iteration 94,
results/evolve-amd-ryzen-7-pro-8840hs-seed24.md, no comparison - run before
93): opbody on 23 of the front's 37; hotinl tried 33 times, on none (its
clean pairs: parse 0.970, the rest within the noise); the run's fastest
e22d91cd94 0.175 re-measured, without either. The owner: a couple more
short runs, then a night run when he says. **Iteration 95: the gene
`t2wide`** (results/t2wide.md) - the tag without its 3-byte call, 127
one-byte codes; on the front escapes (4-8% of kernel's, parse's and
corpus's dispatches) go and images shrink 121-302 bytes. Found on the way:
the engine's file moves in 4 KB steps when the code's end crosses a page
(the page-aligned memory area) - a fix for the owner to decide. NEXT-RUN:
seed 26 tag2, then the comparison (which also judges seed 24, and 25 if
run). Every pack now
carries `repo-files.txt` (the owner's clone, listed) - look at it first.

**Next steps, as agreed (Iteration 83-86):**
1. (Done: seed 23 was small too - stopped.)
2. (Done, Iterations 88-89: `results/price-inline-tailcalls.md`.)
   callsites.py ported to the tag; **inlining short words** and **Forth
   tail calls** priced on the 35 designs of the front of all runs. In the
   image neither pays: inlining 0-11 bytes (the converter's tiny words,
   folds and format-10 words took the short words already), tail calls -4
   to +9 bytes (a 16-bit BRANCH is as long as a call and its EXIT). At run
   time inlining saves 6.1-7.6% of the kernel workload's dispatches on the
   faster designs - 85% of it one empty word, CHARS, which the cross-
   compiler calls for 12.6% of its calls; tail calls 1.8% at most anywhere.
   Nothing built. **For the JIT (Iteration 90): nothing** - alone it frees
   no run-time word; the JIT leaves 45-47% of the kernel workload's
   dispatches and 79-80% of the sieve's in bytecode, held there by calls
   into the image, calls to data words and constants, and >R without
   stencils. Native code calling bytecode (SPN's st_interp, step 3's "the
   JIT's calls into bytecode words") would free 10% of the kernel's and
   80% of the sieve's: the largest lever measured. The owner decides.
3. (Iteration 91: a deep dive ranked twenty candidates - lab/evolve/GENES.md,
   "Ranked (Iteration 91)"; the owner picks, and decides three questions:
   is the shell part of the job, should process start count in speed, and
   may the tag drop its 3-byte call.) Before it: each priced first: the rewrite-rule search (shorter equivalent
   sequences of a design's own operations, verified by random testing);
   image compression with a small decompressor; the JIT's calls into
   bytecode words; a wider pool of compiler flags. The reasoning for each,
   and where randomness helps and where it does not: lab/evolve/GENES.md,
   "Candidates (Iterations 82-86)".
4. When a batch of new genes is built: laptop runs again (seed 24 on),
   the stopping rule counting afresh. **Iteration 92: the first batch -
   hotinl and opbody (the deep dive's 1 and 2); NEXT-RUN seed 24 tag2.**

**Longer term**: the Tegra session (32-bit ARM) needs 32-bit cells under
the tag (FORMAT-TAG2.md, T5 - the DOES> body's 4-byte call does not fit
a 4-byte first cell), an ARM version of the libc-free runtime
(engine/rt-linux-x86_64.c is x86-64 only), and the JIT's ARM patching
(SPN's stencils run there already). The Forth sources' remaining
candidates (results/kfast.md): number conversion, FIND's search-order
loop. The article stays on the backburner. Pushing to GitHub is the
owner's step.

**Working on the development VM** (how every session has done it): clone
the bundle to /home/claude/forth-vm-evolution, owned by the user claude;
run everything as that user (`runuser -u claude -- ...`: the evolver
refuses root, and git refuses a repository owned by another user). Build:
`LAYOUTS=1 bash tools/build-stages.sh`; then `bash tools/run-tests.sh` and
`python3 lab/evolve/evolve.py --validate` (seven hand-made stages
IDENTICAL). Commit as the owner (`git -c user.name='Kirill Timofeev' -c
user.email='kt97679@gmail.com' commit`), the handoff's last commit titled
`Iteration N: ...`; record in PROGRESS.md (append) and here; bundle with
`sh tools/make-bundle.sh DIR` into /mnt/user-data/outputs/. Processes do
not survive between turns on the VM (Iteration 79): long runs belong on
the laptop.

## Success: three objectives, equal (the owner, Iteration 75)

**The smallest binary + image, the highest speed, the lowest memory** -
treated equally: selection keeps the Pareto front over all three, no
weights. To be changed to priorities if equal treatment does not work;
watched in every comparison (below). The motivation: logic moved from
the image into the engine must show - the image shrinks, the binary and
memory grow.

How each is measured:
- **binary**: the engine, stripped. Every engine - the evolved ones and
  the reference s6 - is linked WITHOUT the C library (raw system calls,
  engine/rt-linux-x86_64.c) and without unwind tables, so the binary is
  all there is: a dynamic binary hides the library's code, and with the
  library 1.1 MB of an engine's 1.47 MB resident was the library and its
  loader. (x86-64 Linux; the Tegra's 32-bit ARM needs its own runtime.)
- **speed**: CPU time against s6, as before.
- **memory**: the pages a run touches - cputime's MINFLT, page faults
  counted one by one, times the page size; each workload's median over
  the rounds, the largest the design's. Not ru_maxrss: on Linux 6.x it
  reads 0 KB for a small static run, and a cputime linked with the
  library set a 388 KB floor (now linked without it too).

First readings: s6 39,521 bytes (29,456 binary); seed 15's fastest,
multi-state cached, 65,982 (58,024 binary: the cached states' handler
copies cost 20 KB), the same with tail calls 45,526; 200-216 KB touched.

**Watched, to tell whether equal treatment works**: the front's size; the
designs on it by memory alone (the comparison counts them: dominated on
speed and binary + image together, kept by a page or a few); and each
objective's best - fastest, smallest total, least memory - run to run.

**Seed 18's answer (Iteration 77)**: binary + image works - it reshaped
the front at once; memory as measured did not - 18 of 39 front designs
by memory alone, every one a page or less from a design faster and
smaller. **Memory within 8 KB is now a tie** (EVOLVE_MEM_TOL; speed and
binary + image exact): the three stay equal, at a resolution the
measurement supports - designs today differ by a few pages; a JIT's
buffer or a leak, tens of KB, still decides.

**The stopping rule for three objectives (adopted by the owner, Iteration
78)**: a run is SMALL when, against the earlier runs measured in the same
session, the fastest improves < ~5%, the smallest binary + image < ~2%
and the least memory < 8 KB. Two small runs in a row: stop - the gene set
has converged; new genes (the JIT) before more runs. **Seed 19: small, the
first** (+2.5%, +0.1%, none). **Seed 20: small, the second - STOPPED
(Iteration 79).** The gene set has converged under the three objectives;
the laptop rests until new genes exist.

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
- **Seed 13 - the input side taken up** (Iteration 56,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed13.md`; session 11,
  calibration 0.994): **all 10 front designs its own: the fastest yet,
  0.284 at 7,799 bytes - 3.5x s6; 0.297 at 7,246; the smallest, 6,903 at
  0.436** - 17-34% faster than anything earlier at every size. kinput on
  all ten from generation 1; no design above 7,799 bytes on the front.
- **Seed 14 - the whole lookup taken up** (Iteration 62,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed14.md`; session 12,
  calibration 1.000): **11 of the 12 front designs its own - the fastest
  yet, 0.240 at 8,320 bytes, 4.2x s6; 0.244 at 7,286; 0.245 at 7,172** -
  15-20% faster than anything earlier from 7.0 to 8.3 KB; the small end
  held at 6,903. klookup on 8 of the 11; parse at 0.09-0.12 of s6.
- **Seed 15 - thinhdr everywhere** (Iteration 63,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed15.md`; session 13, the
  newest four runs and this one, calibration 0.994): **13 of the 14 front
  designs its own - the smallest yet, 6,654 bytes; 0.239 at 6,940 (the
  best that small before: 0.375); the fastest yet, 0.230 at 7,958.**
  thinhdr on all 13; rtiplus on none, swapi on one - the run-time code
  genes did not pay in time. Stopping rule: go on (smallest 3.6%).
- **Seed 16 - the first run in the two-bit tag** (Iteration 72,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed16.md`; session 14,
  calibration 1.001): **its front is the old one moved ~370 bytes right
  at about its speed** - 7,009 bytes (0.424) to 7,708 (0.243); 1.03-1.08
  of the best old design no larger from 7.2 KB up. The front of all runs
  stays the old format's. From here the tag-2 front is the one to beat.
- **Seed 17 - the first designs in the tag on the front of all runs**
  (Iteration 76, `results/evolve-amd-ryzen-7-pro-8840hs-seed17.md`;
  session 15, calibration 0.993): a36dc45e12 0.233 at 7,283 bytes, 4.5%
  faster than the best old design no larger; the tag's own front 4.1%
  faster at its fast end than seed 16's, 425 bytes smaller. From 7.2 KB up
  the tag's price is won back. Both: no multi-state caching, swapi taken
  up for the first time. The last run under the old rules.
- **Iteration 75: the objectives change** - three, equal (above).
- **Seed 18 - the first run under them** (Iteration 77,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed18.md`; session 16,
  calibration 1.004): binary + image reshapes the front - 35 of 39 seed
  18's, engines down to 25,280 bytes; bbab8560dd 0.258 at 40,786 total
  against the old fastest's 0.249 at 65,982. Memory selected on noise -
  now a tie within 8 KB. Two converter bugs fixed.
- **Seed 19 - small, the first of two** (Iteration 78,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed19.md`; session 17,
  calibration 1.009): fastest +2.5%, smallest total +0.1%, memory none.
  The fastest of all runs at 42.5 KB total, no large engine (cc0b1e2aeb,
  0.238). 0 of the front's 18 by memory alone.
- **Seed 20 - small, the second: evolution stops** (Iteration 79,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed20.md`; session 18,
  calibration 1.000): fastest none, smallest total 0.0%, memory none.
  The front of all runs, 32 designs, is the converged front. Next:
  development - the JIT (JIT.md) first - then runs again with new genes.
  On running faster: processes here do not survive between Claude's
  turns, so a run here only advances during a reply; and runs keep
  finding front designs to generation 40 (25% by 20, 50% by 30).
- **Seed 21 - the JIT's first run** (Iteration 82,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed21.md`; session 19,
  calibration 0.995): taken up in generation 6; the four fastest designs
  of all runs carry it (6fd52398b1 0.204); on the laptop it costs the
  bytecode workloads nothing (0.98). Not small (fastest +19.6%): the
  stopping rule starts again. Engines now linked without page padding:
  the binary objective counts bytes, not 4 KB pages.
- **Seed 22 - small, the first of two** (Iteration 83,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed22.md`; session 20): fastest
  +4.5% (0.199), smallest total +0.5%, memory none. 12 of the front's 39
  by memory alone, but by 16-20 KB - real pages, not noise. next-run.sh
  now cleans the runs directory before every run (tools/clean-runs.sh).
- **Seed 23 - small, the second: evolution stops** (Iteration 86,
  `results/evolve-amd-ryzen-7-pro-8840hs-seed23.md`; session 21,
  calibration 0.996): fastest none (0.212 against 0.195), smallest total
  +0.2%, memory none. The gene set with the JIT has converged; the front
  of all runs, 35 designs, fastest 2cbcf427f6 0.195 at 42,816 bytes. Runs
  resume with new genes.
- **The runs directory is runs/ in the clone** (Iteration 84, the owner):
  ignored by git; next-run.sh moved what was needed from
  ~/forth-vm-evolution-runs, once. The packs to send back are there.
- **Next, priced before built (the owner's questions, Iteration 82)**:
  inlining short colon words - never built (GENES.md had it as "phase
  3"): a call (2-4 bytes, and an EXIT at run time) where the callee's body
  is one or two one-byte opcodes; and the Forth sources' remaining
  candidates from the kfast review (results/kfast.md): number conversion,
  FIND's search-order loop. Runs
  from seed 18 on are judged by them; the earlier fronts are carried in
  and measured again under them.
- **One-byte calls, built (Iteration 14)**: the gene `hotcalls` - the
  far-call prefixes 0xE0-0xFF call the image's own most-called words
  through a table in its header. 143-319 bytes on seed 3's front (1.1-3.3%;
  priced 136-320), no dispatch removed; every engine form lives; engines
  without it are byte-identical.

## Next, in order

**The current plan is in "Resuming in a new chat" above (Iteration 86);
what follows is how it came about.** Two figures below were later
corrected: the JIT costs the bytecode workloads nothing on the laptop
(the VM's 10-17% was the VM's, Iteration 82), and its engine cost is 3.4
KB, not 8.3 (page padding, Iteration 82).

Iteration 48, the owner: the improvements first, the Tegra session once
they are done, the article on the backburner.

**A JIT as a gene? (the owner, Iteration 72) - the question open.**
Possible: SPN (FINDINGS-SPN.md) proved copy-and-patch here - stencils,
C functions the C compiler builds into the engine, copied and patched by
a translator in Forth, on x86-64 and 32-bit ARM - and ran fib ~5.7x faster
than the evolved interpreter. But SPN is not minimal: a 1,861-line engine
copy, ~2,600 lines of Forth translator. The minimal version: at `;`, a
colon word whose every operation has a stencil (a small set - the stack
ops, arithmetic, literals, @ !, branches, the loop opcodes, calls, EXIT)
is copied and patched into executable memory, and the word pointed at
it; any other stays bytecode - no decoder, no fallback. Its translator is
Forth in the image, so the image size counts it; its stencils are in the
engine, so their machine code should count too (the aim, above). Waits
for the owner's word. **The owner's word (Iteration 73): lazy, and no
significant growth in code or memory - tracked.** The plan, with budgets,
is `JIT.md`; phase 1 a prototype on the VM, its numbers decide.
**Phase 1 done (Iteration 80)**: on seed 19's fastest design fib 2.7x and
loop 2.5x faster, kernel/parse/corpus 10-13% slower, speed 0.229 -> 0.166;
binary +8.3 KB, image +136 bytes, memory +4 KB - within the budgets. The
gene `jit` is wired; seed 21 lets evolution weigh it.

**First, the format (Iteration 64, the owner): `FORMAT-TAG2.md`.** The
code space was 2 MB; the owner wants relf's design - 64 opcodes and
escapes - and a 1 GB code space: relf's two-bit tag, `00` an opcode,
calls of 14, 22 and 30 bits; codes ranked by each design's profile; no
hot calls; variable length everywhere. Its plan, T1-T6, comes before the
improvements below and before the Tegra, which should measure the
format the designs will keep.

**The work left, and when to stop** (Iteration 60, with the owner): about
4-6 more laptop runs of improvements - the code compiled at run time (fib
and loop run in it entirely: I + fused, Iteration 60; next a compare
with a small literal fused into its branch, run-time tail calls), the
opcode budget (seed 13's fastest had 6 pair slots left: the k-genes'
format-10 opcodes take the rest; 2 with klookup, rtiplus and swapi - and
five 'put X first' switches say evolution needs a way to order the
format-10 names itself), size (fewer dictionary threads, cheap
now the lookup is an opcode; the names), and capping the comparison
session (done, Iteration 62: the newest four runs - eight minutes, not
twenty; the carry too, Iteration 63; tools/clean-runs.sh packs the older
runs' directories). Then the
Tegra: 32-bit builds of the evolved designs' overlays and opcodes, SPN's
32-bit path, one sitting. **Stopping rule: the improvement phase ends
when two runs in a row each improve the fastest design by under ~5% and
the smallest by under ~2%.**

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
      0.65, corpus 0.61 counted. Seed 13 (Iteration 56): taken up from
      generation 1 - the fastest yet, 0.284 at 7,799. The whole lookup
      and the numbers (Iteration 57): the gene `klookup` - parse
      0.53-0.57, corpus 0.60-0.65 counted. Seed 14 (Iteration 62): the
      fastest yet, 0.240 at 8,320. Seed 15 (Iteration 63): 0.230 at
      7,958; the smallest 6,654 (thinhdr).
      Next in the sources: number conversion (NUMBER?, >NUMBER, DIGIT?:
      17% of parse), FIND's search-order loop, then what is left
      (REFILL, SCAN, PARSE: a quarter of kernel); the cell-header
      NAME>BUF (open).
   b. **The image's remaining fixed costs** (Iteration 44's audit) -
      begun: the header's 32 thread heads, read by no CV8 engine, as one
      (`thinhdr`, Iteration 58): 248 bytes off every design. Left: the
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
| Variables and constants compiled as literals in code compiled at run time (`rtlit`) | built and measured, rejected (Iteration 59): correct, and the held-out sieve 0.811 of its dispatches - but kernel 0.984 and corpus 1.016, because a COMPILE,8 link that checks every compiled word costs a compiling workload more than it saves; 132 bytes more; selected geomean 1.000 | PROGRESS.md, Iteration 59 |
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
