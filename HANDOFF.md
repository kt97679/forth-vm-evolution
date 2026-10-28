# HANDOFF - start here in a new chat

The state card: read it whole. Its background - the owner's decisions in full, the state through Iteration 555, the
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
- The 32-bit stages need gcc-multilib, which a fresh sandbox may lack (Iteration 553: the stages then build at 8-byte
  cells only and run-tests' generators test fails): `apt-get install -y gcc-multilib` as root, first.

## The state now

- master: Iteration 561.
- **Seed 78 is next - 9 hours from scratch, every freeze still lifted (the owner, 560): a new series again** - the hours
  are the method's (GOALS.md), so the count restarts; the earliest stop after seed 80. Its chain: the spread and
  appbench; no clock test (item 4 answered), so no perf hold and no sudo. NEXT-RUN carries the line.
- **Seed 77 processed (560)** - results/evolve-amd-ryzen-7-pro-8840hs-seed77.md: 12 hours, 161 generations, the true
  front 370; the hypervolume 0.35010, the fastest 0.1421 (alive 0.1406), the smallest 14,015, the least memory 108 KB -
  inside seeds 73-76's spread at generation 128 (session 64). The 12-hour series' only run (stopping-series.md).
  Prediction 555 fails by the memory alone (108 KB, one 4 KB page, reached by seed 76's alive designs already);
  prediction 556 holds (every lifted gene at its old frozen value on 100% of the front).
- **The after-seed-77 batch applied (560)** - results/applied-after-seed77/ORDER.md: the JIT patches every copy of a value
  hole; seed 77's one corpus death (0b17df4e1c: jit, tracer, nocrossjump - the 557 hole) wrong on the tree before
  the fix, right on the fixed one (deaths-check.py): no correctness issue open. The chain on master all PASS - run-tests,
  validate 7 of 7, the gate 417 of 417, ans-check 0 of 96 differ, deaths 1 of 1, the jail.
- **The after-seed-78 batch** (results/pending/ORDER.md, Iteration 561): a processing in three commands -
  process-run.sh, process-finish.sh, setup-sandbox.sh, draft-results.py drafting the facts; and **every run judged at
  generation 100** (the owner's hours vary - GOALS.md's rule counted them, so it could never stop): **the owner's yes
  needed**. Seed 78's processing applies it by hand once: results/drafts/seed78-checklist-561.md. Tested whole on
  seed 77's archive (561): every check passed, the control reproduced 560's by itself (ORDER.md).
- **Predictions due** (results/predictions.md): seed 78 - nine hours lose nothing at the fast end, lose at the small end (560).
- **Scripts added (560)**: lab/evolve/process-records.sh (step 6 in one command); lab/evolve/deaths-check.py (a
  process-checks step: the seed's deaths rebuilt on the tree); draft-results.py reads the spread's generation.
- **Before 560**: seeds 70-76 processed (498-555); history: HANDOFF-REFERENCE.md.
- **Files a new chat needs**: the newest bundle, and seed 78's chain archive (`forth-vm-evolution-chain-<its
  commit>-fury-<time>_tar.gz`). appbench.zip stays on the laptop.

## Processing a returned seed

**The tools** (Iteration 551, first used at seed 75's processing - 553): `sh
lab/evolve/process-seed.sh ARCHIVE`, then `python3 lab/evolve/draft-results.py --iteration N` - the results file, the
xcheck file and the spread's session drafted, the facts filled in, TODO lines for the verdict, the predictions, the votes
and the rules (none may be committed); judge and edit; a batch if one waits; then `setsid nohup sh
lab/evolve/process-checks.sh RESULTS [COMPARE] > /dev/null 2>&1 &` - build, run-tests, validate, the gate, ans-check, the
jail last - polled until /tmp/process-checks/status says DONE; the records; the bundle. The steps below say what each
judges.

1. `sh lab/evolve/process-seed.sh <the chain archive>` as claude (Iteration 395): every output in a file under
   /tmp/process, about a screen in /tmp/process/summary.md - read that, the files only where it points. It covers
   the pack's own checks (tests PASS, validate 7 IDENTICAL, jail PASS; its results-measured-here.patch is the
   laptop's own re-measures, not applied), the verdict as printed and from both CPUs, seed-facts.py, heldout.py,
   review-checks.py progress, curse (the fast end's optimism) and fail32 (the 32-bit failures by cause - Iteration 427)
   and the remote checks' agreement.
2. Judge it. On the stopping series (seed 74 on), GOALS.md's stopping rule first - the hypervolume by 1% and each
   extreme by its threshold, against the best of the method's earlier runs: any one is a gain (553: seed 75's fastest
   alone) - summary.md's stopping.py section prints it, from the after-seed-76 batch on. Then the verdict by GOALS.md's "Judging a run", read from both CPUs (the owner, 389) - for a session printed
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
   minutes. process-checks.sh runs them all, and deaths-check.py (the seed's deaths rebuilt) before the jail.
6. The records - `sh lab/evolve/process-records.sh N ITERATION` (Iteration 560; `NEXT_METHOD='why'` when the
   next run changes the method) does the mechanical part below: the batch's move and citations, the progress table, the
   votes, the stopping line; then the predictions, NEXT-RUN, this file, PROGRESS by hand. By hand, for reference: a batch applied: `git mv results/pending results/applied-after-seedN` and its citations follow
   (Iteration 372: 62 had been left behind):
   `git grep -lz 'results/pending/' -- '*.md' | xargs -0 sed -i 's|results/pending/\([A-Za-z0-9._-]*-after-seedN\.patch\)|results/applied-after-seedN/\1|g; s|results/pending/ORDER\.md|results/applied-after-seedN/ORDER.md|g'`
   (N the seed); and results/README.md's `pending/ORDER.md` line goes, unless a new batch waits (Iteration 414's dry
   run: handoff-check names it). A batch queued behind it moves into results/pending/ the same way - its folder
   renamed, its paths followed (done at 433: the after-seed-63 batch) - and `sh tools/batch-check.sh` runs against the new
   master. The session appended to `results/compare-fronts-amd-ryzen-7-pro-8840hs.md` ("## Session K -
   Iteration I: seed N and seeds ...", the verdict line, then the pack's compare-fronts.md); `python3
   lab/evolve/progress-table.py > results/progress-by-run.md`; the gene votes, from seed 63 on (Iteration 432): `python3
   lab/evolve/review-checks.py votes results/evolve-<machine>-seedN.md --ledger results/gene-votes.md --append`; the stopping series (the after-seed-76 batch on): `python3 lab/evolve/stopping.py <the pack's db.jsonl> --seed N --append`; NEXT-RUN; this file; a PROGRESS entry; then "Before a
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

1. Seed 78's processing - results/drafts/seed78-checklist-561.md: the after-seed-78 batch by hand once, then
   process-run.sh and process-finish.sh; the stopping rule at generation 100 if the owner said yes.
2. The end of the improvement phase - GOALS.md, "When the improvements are done": the 10-hour series (74-76) closed
   without a stop; the 12-hour series seed 77 alone (560); the 9-hour series from seed 78, the earliest stop after seed 80; then the confirmation run, the final set, the random-search baseline (its mode drafted and tested: results/drafts/random-mode-548.patch, applied at consolidation).
   The confirmation run's founders built carefully (the owner, 559: no good design missed) -
   results/drafts/confirmation-pool-559.md: --carry to take each run's strict front (today's tolerance front drops
   chain-hidden designs - seed 76's 105 fastest), every archived run, designs named elsewhere, the pool pre-flighted.
3. **Correctness - the JIT's value holes fixed, applied (560)**: the after-seed-77 batch (results/drafts/corpus-deaths-555.md,
   jit-sweep-558.md); seed 77's one corpus death the same fault - wrong before the fix, right after (deaths-check.py's control).
3b. The stopping rule's measure - decided (the owner, 556): from seed 77 the extremes from every alive design, the
   hypervolume on the true front as before (stopping.py; seed 76's dominance chain).
4. The fast end's offset (rule 3; seeds 73-76 1.070, 1.066, 1.047, 1.063) - results/drafts/fast-end-offset-554.md: a cost
   every workload's run pays, a design and s6 alike, outside user space - not the JIT; seed 76's re-measure agrees (the
   non-JIT designs 0.988, below 1 as predicted). Seed 77's clock test measures the cost both pay, by workload.
5. Rule 9 (the rtimm=2 / rtfuse overlap): PROPOSE when no design relies on it - seed 76: 2 do, no change.
6. The JIT genes' place: their votes count (rule 12). Seed 76: JIT designs 73 of 262, all 26 of the fastest tenth;
   jitmul 43, jitfuse 10, jitexec 1, jitos 19, jitrp 22; jitdoes the one freeze candidate.
7. Deferred: the JIT on ARMv7, for the Tegra session (results/drafts/ask-arm-jit-answers-512.md); an uncertainty-aware
   screen tested offline (results/drafts/ask-search-answers-525.md, proposal 2).
8. The article, after consolidation: the claim is the integration, not any technique
   (results/drafts/ask-related-work-answers-539.md); every figure recomputed on the true fronts (seeds 53-75:
   results/truefronts-seed75.md, results/progress-true-fronts.md); across machines the fast end as a band, the fastest
   named per machine (results/drafts/xcheck-agreement-546.md; seed 76's checks: 3d4e860a9f the fastest on dream). The
   method section drafted (results/drafts/article-method-548.md).

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
- **A detached job dies when the turn ends** (561: the sandbox suspends between turns; /tmp and the clone stay, the
  processes go). Start a long job early in a turn and see it to its end in that turn; cut off, rerun it from its step.

**Efficiency** (the owner, Iteration 551 - seeds 73 and 74 in one chat cost several times two fresh chats):

- One chat per returned archive: a fresh chat with the newest bundle and the archive, ending with a bundle. A long
  chat re-reads all of itself every turn.
- Work while a run goes: only what must be ready before the next run - in its own short chat, bundle in and out, or
  folded into the next processing. Not an iteration per question.
- Charts drawn by a script into a file and shown as the file - never data points typed into a chart call.
- Replies: the answer first, short; nothing a tool output already showed, restated.
- Effort: xhigh for the routine; max for the unexpected - a failed chain, an odd result, a design decision.
- Recurring steps become scripts; the judgment stays in the chat - prompts/21, item 9 (Iteration 552).
- Tool calls: never `pkill -f` a pattern in your own command line (it kills your shell); a file written after an `&&`
  step that can fail is lost with it - check what was written; remove a background job's old output before polling it
  (a stale file reads as done); a sandbox restart kills background jobs and keeps /tmp - the status file says where to
  resume; no quadratic loop over a run's records (a call's 300 s).

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
