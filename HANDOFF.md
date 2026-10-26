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

- master: Iteration 547.
- **Seed 74 is running** on the laptop - 10 hours (the owner), the first run of the after-seed-73 batch
  (results/applied-after-seed73/ORDER.md). The method changed, so GOALS.md's stopping count starts at seed 74 - its
  hours, 10, are the method's: seeds 75 on at 10 too, or the count restarts. Its clock test runs without cycles unless
  the owner set kernel.perf_event_paranoid to 2 by hand - and only after the evolution's re-measurement: tools/cputime.c
  opens the counters for every run once it may (545). Its processing: results/drafts/seed74-checklist-545.md, then
  "Processing a returned seed".
- **The after-seed-74 batch**, four patches (results/pending/ORDER.md): fail32 learns cpt16's reach; the clock test
  takes the chain's perf hold - from seed 75, next-run.sh asks for sudo once at the start; the progress table's header;
  truefronts.py - every run's true front from the laptop's records, seed 75's last step. batch-check again before
  applying.
- **Seed 73 processed (544)** - results/evolve-amd-ryzen-7-pro-8840hs-seed73.md: the true front 222 (reported 174); no
  comparison in its chain, the spread level with 71-72; the fixed-box hypervolume 0.34915, the series' first; jitexec on 6
  of 65 JIT designs (518 fails); no freeze candidate - rtimm not (533's question closed), rtfuse not before 75.
- **Predictions due** (results/predictions.md): seed 74 - adaptive operators, the reported fronts, one round first (526,
  527, 529), jitos back on the front (534).
- **Before 544**: seeds 70-73 processed (498, 516, 520, 544). Every front reported until seed 74 was the shortcut's, not the
  true one (results/drafts/front-recheck-528.md): figures are recomputed from the runs' records. The decisions of
  532-543: HANDOFF-REFERENCE.md.
- **Files a new chat needs**: the newest bundle, and seed 74's chain archive (`forth-vm-evolution-chain-<its
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

1. Seed 74's processing, then a new chat: predictions 526, 527, 529, 534; its reported front is the true one now - check
   it against `review-checks.py votes --db`; the clock test's reading (item 3); its hypervolume, the stopping series' first
   run on the method; clean-runs.sh's first tidy of the laptop's runs/ (only copies gone: repo.bundle, bins.tar.gz, chain
   tarballs past the newest two); the archive about 13 MB, without the bundle and the binaries.
2. The end of the improvement phase - GOALS.md, "When the improvements are done": runs on an unchanged method from seed
   74 (10 hours), then the confirmation run, the final set, the random-search baseline (a random mode in evolve.py,
   written at consolidation).
3. The fast end's 7% offset (rule 3; seed 73 1.070): the clock test - seed 74's on the time and the clock (cycles only if
   set by hand), seed 75's with the chain's hold (results/drafts/ask-noise-answers-513.md, ask-cpu-state-answers-526.md).
4. Rule 9 (the rtimm=2 / rtfuse overlap): PROPOSE every run - "rtfuse governs" waits on the owner (seed 73: 1 design relies
   on it).
5. The JIT genes' place: their votes count (rule 12). Seed 73: jitexec on 6 and jitfuse on 7 of 65 JIT designs; jitrp 8
   votes of 8 over 72-73 - a freeze candidate if seed 74 gives it three or four (11 of 12) with no keep vote.
6. Rule 5's ATTENTION for cpt16's reach at 4-byte cells (517; seeds 72-73: 67 and 61 designs) is in name only until
   the after-seed-74 batch's fail32 patch is applied.
7. Deferred: the JIT on ARMv7, for the Tegra session (results/drafts/ask-arm-jit-answers-512.md); an uncertainty-aware
   screen tested offline (results/drafts/ask-search-answers-525.md, proposal 2).
8. The article, after consolidation: the claim is the integration, not any technique
   (results/drafts/ask-related-work-answers-539.md); every figure recomputed on the true fronts; across machines the
   fast end as a band, the fastest named per machine (results/drafts/xcheck-agreement-546.md).

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
