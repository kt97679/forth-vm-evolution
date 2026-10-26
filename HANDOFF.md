# HANDOFF - start here in a new chat

The state card: read it whole. Its background - the owner's decisions in full, the state through Iteration 544, the
open items' history, the lessons - is HANDOFF-REFERENCE.md, read on demand; its lessons before changing the evolver or a
measurement.

## What this is

**The aim is simplicity and minimalism** (GOALS.md; the owner, Iteration 72): the smallest, simplest system that does
the job - small images, a small and plain engine, few mechanisms, each easy to read and to remove; speed where it costs
little, never as a reason for complexity. A mechanism is kept only if it earns its place by measurement.

An evolutionary search over the design of a Forth system: the engine (`engine/vm-lab.c`, computed-goto C), the kernel
(`forth/kernel.4`, cross-compiled by `forth/cross.4`), the converter (`tools/layout.py`, `tools/sod16.py`: into the
byte-coded CV8 / tag-2 image), and the evolver (`lab/evolve/evolve.py`: NSGA-II over genes; objectives - speed against
the hand-made s6 over the selection workloads, engine plus image bytes, memory, and the speed at 32-bit cells). The
owner, Kirill Timofeev, runs the seeds on his laptop (AMD Ryzen 7 PRO 8840HS, "fury") per `lab/evolve/NEXT-RUN` and
sends back one chain archive per run (`forth-vm-evolution-chain-<commit>-fury-<time>_tar.gz`). Commits are authored
`Kirill Timofeev <kt97679@gmail.com>`; deliveries are git bundles.

## The environment

- Work as user `claude` - every git, build and tool command as `runuser -u
  claude -- ...` (git refuses root on the tree) - in
  `/home/claude/forth-vm-evolution`; scratch in /tmp. Uploads arrive in
  `/mnt/user-data/uploads`; deliveries go to `/mnt/user-data/outputs`, presented.
- A tool call ends near 300 s and kills what it started in the background:
  start anything long with `setsid nohup ... &` and poll it. Times on the VM:
  a build about a minute, run-tests about six, validate two to four. Tool calls
  run /bin/sh (dash): no bash-only syntax there.
- **A turn has a budget of tool calls (about fifty).** Commit and make a
  `--checkpoint` bundle before long work: twice a turn ended with work only in
  /tmp (Iterations 267-268).
- A scratch tree for a batch in progress: clone master, apply the pending
  patches committing each, build there. Files for a pending patch are written
  there, never in master. Never two evolver processes on one tree at once.
  After changing forth/ or engine/, rebuild the stages.

## The state now

- master: Iteration 549.
- **Seed 75 is next** - 10 hours, the method's: the stopping count's second run, after seed 74. Its line ends with the
  clock test - now with the chain's perf hold: **next-run.sh asks for sudo once, at the start** - and truefronts.py,
  every seed pack's true front. The after-seed-74 batch is applied (results/applied-after-seed74/ORDER.md).
- **Seed 74 processed (549)** - results/evolve-amd-ryzen-7-pro-8840hs-seed74.md: the reported front is the true one
  (238; the old staircase 144 - 527 holds); the fixed-box hypervolume 0.35667, the stopping series' first on the
  method; one round first holds (529); adaptive operators (526) and jitos (534) fail; the clock test: the offset does
  not follow the clock. Its chain came back "failed" - the experiments failed at their packing, their reports whole
  (Iteration 541's cleanup; fixed by the batch's chain-logs patch).
- **jitrp is a freeze candidate** (12 of 12 over 72-74, no keep vote). A freeze changes the method and restarts the
  stopping count: the owner's to decide - not frozen.
- **Predictions due** (results/predictions.md): seed 75 - no gain over seed 74 by the stopping rule (549).
- **Before 549**: seeds 70-74 processed (498, 516, 520, 544, 549); every front reported until seed 74 was the
  shortcut's (results/drafts/front-recheck-528.md) - figures recomputed from the records. History: HANDOFF-REFERENCE.md.
- **Files a new chat needs**: the newest bundle, and seed 75's chain archive (`forth-vm-evolution-chain-<its
  commit>-fury-<time>_tar.gz`). appbench.zip stays on the laptop.

## Processing a returned seed

1. `sh lab/evolve/process-seed.sh <the chain archive>` as claude (Iteration 395): every output in a file under
   /tmp/process, about a screen in /tmp/process/summary.md - read that, the files only where it points. It covers
   the pack's own checks (tests PASS, validate 7 IDENTICAL, jail PASS; its results-measured-here.patch is the
   laptop's own re-measures, not applied), the verdict as printed and from both CPUs, seed-facts.py, heldout.py,
   review-checks.py progress, curse (the fast end's optimism) and fail32 (the 32-bit failures by cause - Iteration 427)
   and the remote checks' agreement.
2. Judge it. The verdict by GOALS.md's "Judging a run", read from both CPUs (the owner, 389) - for a session printed
   by older code (seed 59's), the summary's "both CPUs" line; its per-CPU lines show how far noise moves it; a
   positive figure is the run ahead. heldout: the top-end lines and the regret beside the whole front's Spearman
   (about 0.94 on seeds 49-57). progress: say if diversity falls or the gains stop early. Replicates (seeds 61-62):
   `python3 lab/evolve/review-checks.py spread <db> <db> <db>`, one generation for all - seed 62's chain runs it on
   the laptop over seeds 58-62 (its review-checks pack, Iteration 415); here, about 8 minutes for three databases, in
   the background (results/drafts/preflight-414.md).
3. Score the predictions, write the next (`results/predictions.md`).
4. `results/evolve-amd-ryzen-7-pro-8840hs-seedN.md`: the verdict and facts, a `---`, then report.md - the gate and
   ans-check read genomes from it; results/xcheck-seedN.md from the remote reports.
5. A batch due now (its ORDER.md says when): `tools/batch-check.sh` first (one line), then apply it (reseed with
   `tools/reseed.sh` only when a patch changes `forth/kernel.4`). Then ONE background chain on master, logs to
   files: build (`env LAYOUTS=1 bash tools/build-stages.sh`), `bash tools/run-tests.sh` (PASS), `python3
   lab/evolve/evolve.py --validate` (7 of 7 IDENTICAL), `python3 lab/evolve/test-jail.py` (PASS - run it last, after the gate and ans-check, and alone: here
   it takes the same user's other processes with it - the chain after it at 433 and 441, and at 449 a gate running beside
   a batch-check's own jail test; nothing may run beside it), `python3
   lab/evolve/gate.py <results file> <compare pack>/compare-fronts.md` (all alive; a run with no comparison step: COMPARE left
   out, the run's front alone - Iteration 427), `python3 lab/evolve/ans-check.py
   --ids <every fourth of the front by size, and its extremes>` (0 differ, its negative control caught) - about 20
   minutes.
6. The records. A batch applied: `git mv results/pending results/applied-after-seedN` and its citations follow
   (Iteration 372: 62 had been left behind):
   `git grep -lz 'results/pending/' -- '*.md' | xargs -0 sed -i 's|results/pending/\([A-Za-z0-9._-]*-after-seedN\.patch\)|results/applied-after-seedN/\1|g; s|results/pending/ORDER\.md|results/applied-after-seedN/ORDER.md|g'`
   (N the seed); and results/README.md's `pending/ORDER.md` line goes, unless a new batch waits (Iteration 414's dry
   run: handoff-check names it). A batch queued behind it moves into results/pending/ the same way - its folder
   renamed, its paths followed (done at 433: the after-seed-63 batch) - and `sh tools/batch-check.sh` runs against the new
   master. The session appended to `results/compare-fronts-amd-ryzen-7-pro-8840hs.md` ("## Session K -
   Iteration I: seed N and seeds ...", the verdict line, then the pack's compare-fronts.md); `python3
   lab/evolve/progress-table.py > results/progress-by-run.md`; the gene votes, from seed 63 on (Iteration 432): `python3
   lab/evolve/review-checks.py votes results/evolve-<machine>-seedN.md --ledger results/gene-votes.md --append`; NEXT-RUN; this file; a PROGRESS entry; then "Before a
   chat's turn ends".

## The owner's standing decisions - the ones every session uses

The full list, with the reasons: HANDOFF-REFERENCE.md.
- Every patch tested, then verified to apply in order on a fresh clone; batches wait in results/pending/ with ORDER.md;
  `tools/batch-check.sh` runs that test.
- Run lengths are the owner's - ask for each run's hours.
- Noisy timing questions go to the laptop; here decide by deterministic counts (the profiler's dispatches, cachegrind).
- Offer trade-offs to evolution as genes rather than deciding; size savings are exact - take them.
- Every iteration has a PROGRESS entry, naming every file it adds under results/ (the article is written from it).
- A generic Forth first: nothing is selected by relf's shell profile.
- One command, one archive: the laptop runs one script and sends one archive back.
- The gene rules (results/seed63-rules.md): a gene leaves FROZEN only when a selection workload can see its benefit
  (rule 11); its votes count from its second run back (rule 12).

## Open items

1. Seed 75's processing, then a new chat: the prediction (549); the clock test with cycles - check that sudo was asked
   at the start and the setting held only while it measured (runs/perf-hold.log); truefronts.md - every seed's true
   front: check the seed names, then rebuild results/progress-by-run.md and the charts on the true fronts; the chain's
   status done (the chain-logs patch).
2. The end of the improvement phase - GOALS.md, "When the improvements are done": runs on an unchanged method from seed
   74 (10 hours; its hypervolume 0.35667), then the confirmation run, the final set, the random-search baseline (its mode
   drafted and tested: results/drafts/random-mode-548.patch, applied at consolidation).
3. The fast end's 7% offset (rule 3; seeds 73-74 1.070, 1.066): seed 74's clock test - the time against the run 1.079
   alone, 1.056 beside compiles, while the core's clock moved 2,000-4,600 MHz: not the clock. Seed 75's cycles confirm;
   then the winner's curse or the run's hours of load (results/drafts/ask-noise-answers-513.md,
   ask-cpu-state-answers-526.md).
4. Rule 9 (the rtimm=2 / rtfuse overlap): PROPOSE every run - "rtfuse governs" waits on the owner (seed 74: 2 designs
   rely on it).
5. The JIT genes' place: their votes count (rule 12). Seed 74: JIT designs 50 of 238, all of the fastest tenth; jitmul
   25, jitfuse 5, jitexec 1; jitos none (534 fails); jitrp a freeze candidate (above).
6. Deferred: the JIT on ARMv7, for the Tegra session (results/drafts/ask-arm-jit-answers-512.md); an uncertainty-aware
   screen tested offline (results/drafts/ask-search-answers-525.md, proposal 2).
7. The article, after consolidation: the claim is the integration, not any technique
   (results/drafts/ask-related-work-answers-539.md); every figure recomputed on the true fronts; across machines the
   fast end as a band, the fastest named per machine (results/drafts/xcheck-agreement-546.md). The method section
   drafted (results/drafts/article-method-548.md).

## Conventions - tokens (the owner, Iteration 542)

- Write each fact once: the detail in its own document; a PROGRESS entry of about three lines - what, the numbers, the
  files; an index line of one sentence. This file stays a card: history goes to HANDOFF-REFERENCE.md.
- Replies: the answer first, few sections; detail when asked.
- Tool output: aggregates and the lines that matter, never whole files or listings. Ask the owner for summaries
  (`du -sh runs/* build/* | sort -h | tail -30`), not dumps.
- Other models (prompts/20-ask-other-models.md): the owner pastes the answers one at a time; each is assessed on
  arrival - what is new, what is wrong, what checks out - and logged in results/model-usefulness.md; stop when the
  question is answered.
- A new chat after each seed's processing.

## Where things are

Every document: README.md's "Documents" section. Every measurement, analysis
and per-run record: results/README.md. Every tool of the evolver:
lab/evolve/README.md's "Tools". The prompts: prompts/INDEX.md. The leftovers of
the chats of Iterations 213-265: results/drafts/chat-to-iter265/README.md (left the tree at Iteration 541 -
`git show cb05abe20:results/drafts/chat-to-iter265/README.md`).
GOALS.md before Iteration 275: results/drafts/goals-snapshots.md. This file's background: HANDOFF-REFERENCE.md.

## Before a chat's turn ends - every turn that changed the repository

1. Commit everything that should survive. A script that produced a figure
   recorded in PROGRESS.md goes into the repository (lab/evolve/ or
   results/drafts/); every other file you wrote in /tmp is deleted or listed in
   `/tmp/handoff-disposable.txt` (a path, then a reason, per line).
2. Bring this file up to date: "master: Iteration N", the state, the open
   items - a card: history goes to HANDOFF-REFERENCE.md; write the PROGRESS
   entry - about three lines: what, the numbers, the files.
3. `runuser -u claude -- sh tools/make-bundle.sh /mnt/user-data/outputs` - it
   runs `tools/handoff-check.py` and refuses a bundle a new chat could not
   start from. Mid-work, `--checkpoint` makes a bundle that is not a handoff
   point (its name ends in -checkpoint).
4. Present the bundle.
