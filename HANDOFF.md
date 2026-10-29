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

- master: Iteration 565.
- **Seed 80 is next - 12 hours from scratch** (the owner), the freezes lifted, the stopping rule matched by generation.
  NEXT-RUN carries the line - and, commented, the confirmation run's (`seed 80 12h widths carryall`) should the owner
  read seed 79 at equal effort (below).
- **Seed 79 processed (565)** - results/evolve-amd-ryzen-7-pro-8840hs-seed79.md: 12 hours, 177 generations, the true
  front 257. **It gains by the rule** (the fastest -2.0%, 32-bit -3.5%, against seed 77's end) - three runs, the earliest
  stop after seed 81 - **but not at equal effort**: at generation 161 (seed 77's end) no gain; the rule's lean decided it.
  The three lifted runs slower at the fast end at generation 126 than 74-76 (3 against 3 apart). The founders'
  pre-flight: 6,252 designs (seeds 75-79), 40 of 40 right. The Tegra disagreed (-0.103), unexplained. Prediction 563
  failed by the rule; 556 holds as built. Deaths: 4, the scale-1 reach limit. No correctness issue open.
- **The after-seed-79 batch applied (565)** - results/applied-after-seed79/ORDER.md: deaths-check names the scale-1
  reach limit, gene-narrow.py, the random-search baseline ("random"), lifted.py as built. Nothing waits.
- **Predictions due** (results/predictions.md): seed 80 - slow at generation 126, no gain (565).
- **Before 565**: seeds 70-78 processed (498-563); history: HANDOFF-REFERENCE.md.
- **Files a new chat needs**: the newest bundle, and seed 80's chain archive. appbench.zip stays on the laptop.

## Processing a returned seed

Three commands, the judgment between them (Iteration 560; each step's detail and what it judges: HANDOFF-REFERENCE.md,
"Processing a returned seed - the steps in detail"):

1. As root, a fresh sandbox: `git clone -q /mnt/user-data/uploads/<bundle> /tmp/s && sh /tmp/s/tools/setup-sandbox.sh
   && rm -rf /tmp/s` - the compilers, the clone as claude, the identity.
2. As claude, in the clone: `setsid nohup sh lab/evolve/process-run.sh ITERATION > /dev/null 2>&1 &`, polled with `sh
   tools/wait-for.sh /tmp/process-run/status 'summary|DONE|STOP'` - the archive unpacked and checked, the results
   drafted, the batch checked and applied, the checks on master, the control. At "summary" read /tmp/process/summary.md
   and judge while the rest runs: the stopping rule (stopping.py; GOALS.md), the verdict from both CPUs, the predictions
   scored and the next written (results/predictions.md), the results file's TODO lines, the spread's session; NEXT-RUN
   (the owner's hours), this card, the PROGRESS entry. Run nothing as claude while the status's last line says "jail".
   A detached job dies when the turn ends (the sandbox suspends; /tmp stays - 561): start it early, see it to DONE in
   the same turn; cut off, `FROM=checks` resumes it at the checks.
3. At DONE: `sh lab/evolve/process-finish.sh N ITERATION` - it stops naming anything wrong or missing (a check, a TODO, a
   record); fixed, run it again. It writes the chain line, runs process-records.sh (`NEXT_METHOD='why'` when the next
   run changes the method), commits and makes the bundle: present it.

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
   process-run.sh and process-finish.sh; the stopping rule matched by generation (562).
2. The end of the improvement phase - GOALS.md, "When the improvements are done": the 10-hour series (74-76) closed
   without a stop; from seed 77 one series matched by generation, the hours free (562), the earliest stop after seed 79; then the confirmation run, the final set, the random-search baseline (ready: random-mode-after-seed79.patch, NEXT-RUN's "random" - 564).
   The confirmation run's founders built carefully (the owner, 559: no good design missed) -
   results/drafts/confirmation-pool-559.md - prepared (562, carry-after-seed78.patch: the strict front, the named
   designs, carryall, carry-check.py): --carry to take each run's strict front (today's tolerance front drops
   chain-hidden designs - seed 76's 105 fastest), every archived run, designs named elsewhere, the pool pre-flighted.
3. **Correctness - none open (564)**: seed 78's kernel deaths are the scale-1 reach limit (Iteration 10), not a fault.
   The JIT's value holes fixed and applied (560: corpus-deaths-555.md, jit-sweep-558.md).
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
