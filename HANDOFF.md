# HANDOFF - start here in a new chat

The state card: read it whole. Its background - the owner's decisions in full, the processing steps, the lessons - is
HANDOFF-REFERENCE.md, read on demand (its lessons before changing the evolver or a measurement); its history is
HANDOFF-HISTORY.md, grepped.

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
- A scratch tree for a batch in progress: `SCRATCH=/tmp/x sh tools/setup-sandbox.sh` as root - master cloned, the
  pending patches applied committing each, the build started (/tmp/x.status). Files for a pending patch are written
  there, never in master. Never two evolver processes on one tree at once.
  After changing forth/ or engine/, rebuild the stages.
- **The environment is tools/setup-sandbox.sh** (the owner, 567; prompts/22): idempotent - run it again rather than
  mend by hand (a second run changes nothing; 573: "still installing - run this again" is apt-get detached past 240 s); a requirement a session finds missing goes into it in that turn, never
  as a manual step in a document (gcc-multilib, Iteration 553, was one).

## The state now

- master: Iteration 588.
- **Chain B, processed (587)** - results/final-pick-chainB-seed86.md: the final set 14 (results/final-set-seed86.md) -
  the laptop's 10 and 4 added across machines (06b188f45b, 6c6717b20a, c13353f8cf the best means; d6b42c335a x86-32's
  fastest); no generic pick within 25% (ARMv7's best, 690981ca5b, a GCC design without the JIT, 130% behind on x86).
  Every host measured all it was given (rage 237 of 237 at 2 rounds in 154 of its 540 minutes; dream 44 of 44 a width):
  the chain took 2.9 hours of the owner's 12, nothing cut - 585 read seed 86's rage time, its 16-minute stages build in
  it, as a per-design rate (measured: 35 s a design at 2 rounds). Its readings kept in results/chainB-seed86/ (chain A's
  were not - its dream session cannot be compared). Rage's GCC built 9 lto=1 designs with -u raise, alive: open items 1
  and 1b closed. The 7 msc designs 585 never asked for: chain C. The swaps against chain A's set are ties (the fastest
  0.9%, the smallest the same bytes): chain A's members and additions not in this set stay on the shortlist, re-measured.
- **Chain C, next (NEXT-RUN; the owner's 8 hours)** - the shortlist's 40 again on the three machines at 10 rounds (the
  laptop alone and loaded at both widths, dream at both widths, the Tegra), the 8 msc designs on the Tegra first. About
  3 hours of work, rage's line the longest; the 8 hours its window (rage's deadline 450 minutes) - an end near hour 3 is
  expected. An experiment chain ends when its work is done: quote its length from measured rates, a one-time build apart.
- **Chain A, done (585)** - results/final-pick-chainA-seed86.md: 232 of 232 re-measured at both widths and on dream; the
  generic pick 4df5b46d00 across x86-64 and x86-32, four added; the shortlist 40. The laptop's 64-bit fast-band order its
  own (0.889 against itself, -0.357 against dream). Fixed: final-pick.py's host Spearman at its width; gather's silently
  dropped line; xcheck --also from the archived databases (the msc pairs' records are only in seed 86's).
- **Seed 86, the second confirmation run, done (582)**: NOT CONFIRMED by carried designs only - the least memory 104 KB
  (fb0d57c8a2, seed 76's, carried) at the 4 KB bar under the pool's 108; the search gained nothing (its front -1.0%
  against the pool, its bred designs +0.05%, the fastest 0.1330 against 0.1325): the pool widened, no new search (GOALS.md,
  573) - step 2 ends. results/evolve-amd-ryzen-7-pro-8840hs-seed86.md.
- **The fast-end question answered (582)**: dream's 41 put seed 84's bred lead at -0.6% (64 bits), +0.2% (32) against the
  laptop's 5.9% - the laptop's, not the designs' (results/xcheck-seed86.md; results/drafts/dream41-582.py).
- **The hosts' real rates (582)**: seed 86's chain measured a 68-design line on dream in about 4.3 minutes and 15
  designs on rage in about 28, the stages built there included (load.log; a lock serializes a host's lines) - 579's
  "dream about 10 hours, the Tegra days" was a budget. So dream re-measures every candidate in chain A, and chain B's 900
  minutes on the Tegra hold every candidate it can build, not the shortlist's first 20: chain A's processing writes
  chain B's lists (the shortlist first, then the rest; the Tegra's
  also the msc pairs of retire-plan-583.md).
- **Consolidation's retirement, planned (583)** - results/drafts/retire-plan-583.md: fsys 4-5 retired, the fsys45
  batch queued (results/queued-consolidation/, batch-check PASS) - moved to results/pending/ at consolidation, never
  before (process-run.sh applies pending). Waiting: jitdoes=1 and rtloop=2 for the final set (12 and 1 candidates; the
  fastest, 15ecc6a232, uses jitdoes); msc=1 for the Tegra's 4 msc pairs, in chain B's list; bytehdr, doesfar, lean,
  scale, varcall: the owner said go (584: "if it will not lose good designs") - checked: no front design, no
  candidate, s6 as it is (results/drafts/retire-stages-584.md). Six patches in fresh chats, the freeze of s2-s5 first;
  each passes results/drafts/build-hash-584.py - every design but s2-s5 the same engine and image bytes as master's
  (results/drafts/build-hash-584-8.jsonl, -4.jsonl) - then run-tests, validate, batch-check; queued after fsys45.
- **Processing chain C**: the same three commands - process-run.sh stops after the summary (no seed pack), final-pick.py
  on chain C's readings (process-seed.sh's chain-B mode: the shortlist); then final-pick.py beside chain B's readings
  (results/chainB-seed86/: each host's two out.json - final-pick.py takes a host's mean; the laptop's two loadtest.md
  merged by hand) - a design in either session's set kept (lose no good design). Keep chain C's readings as chain B's;
  the 8 msc records (rage's designs.json) into the repository; msc by retire-plan-583's rule. Then consolidation:
  retire-plan-583.md, retire-report-579.py (578's rule) on the final set.
- **Across machines - the owner's terms (576; GOALS.md)**: lose no good design or gene. final-pick.py step 5: the three
  classes' geometric mean; the 25% veto removes nothing, only names the generic pick; the three best means and each
  class's fastest ADDED to the set; a design missing a class ranked on the rest, kept. Consolidation (578, the owner): a
  gene or code path is retired only when no design on the pooled true front uses it - not the final set.
- **Predictions due** (results/predictions.md): chain C - every line all it is given (90/10), 2.5-4 hours (75/25),
  rage's two sessions 0.8+ (70/30), dream's 0.8+ (75/25), msc retired (65/35), 11 of the 14 kept (65/35), no generic pick
  (85/15).
- **Before 582**: seeds 70-86 processed (498-582); history: HANDOFF-HISTORY.md.
- **Files a new chat needs**: the newest bundle, and the next chain's archive. appbench.zip stays on the laptop.

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

1. The Tegra's check - **closed (587)**: chain B's rage line built 9 GCC lto=1 designs with its own GCC 16 and 585's
   -u raise, and 227 clang designs cross-built without the C library - all alive and measured (1b's link fault fixed);
   rage-check.sh was not run (the owner, 587) and is no longer needed before a chain.
2. The end of the improvement phase - GOALS.md, "When the improvements are done": **step 1 done** - the rule stopped at
   seed 83 (572). **Step 2 done (582)**: seed 84 NOT CONFIRMED at the fast end - the laptop's lead (dream, 582); seed 86
   NOT CONFIRMED by carried designs only - the pool widened, no new search. **Step 3, the final set: chain B's 14 (587)** -
   results/final-pick-chainB-seed86.md; its second session chain C. **Step 4, the random baseline, done (576)**:
   results/evolve-amd-ryzen-7-pro-8840hs-seed85.md.
3. **Correctness - none open (576)**: seed 85's 55 "body size drift" deaths the scale-0 call reach, met where varcall
   and doesfar exempt a design from reach_lethal() - no wrong output (results/drafts/body-size-drift-576.md). seed 82's deaths all expected (cpt16 on apps 36, the scale-1 reach 10). Seed 80's two JIT deaths - jit_scan's 160-byte window cut st_execute under
   -falign-*=64; ccflags() built alignhot where express() drops it (results/drafts/jitexec-alignhot-566.md) - fixed by
   the after-seed-81 batch, applied at 17566c6; seed 81's one such death right after it, wrong before (the control).
   Before: none open (564): seed 78's kernel deaths are the scale-1 reach limit (Iteration 10), not a fault.
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
7b. (583: planned - results/drafts/retire-plan-583.md.) Consolidation's retire candidates read before seed 84 returned (results/drafts/retire-candidates-573.md): the old
   values' code builds the stages s2-s5; msc's Tegra check before retiring it.
8. The article, after consolidation: the claim is the integration, not any technique
   (results/drafts/ask-related-work-answers-539.md); every figure recomputed on the true fronts (seeds 53-75:
   results/truefronts-seed75.md, results/progress-true-fronts.md); across machines the fast end as a band, the fastest
   named per machine (results/drafts/xcheck-agreement-546.md; seed 76's checks: 3d4e860a9f the fastest on dream). The
   method section drafted (results/drafts/article-method-548.md).

## Conventions - tokens (the owner, Iteration 542)

- Write each fact once: the detail in its own document; a PROGRESS entry of about three lines - what, the numbers, the
  files; an index line of one sentence. This file stays a card: history goes to HANDOFF-HISTORY.md.
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
- A batch: its scratch tree by `SCRATCH=` (setup-sandbox.sh), each commit a patch named by its subject's first word, then
  `tools/batch-make.sh N ITERATION SCRATCH` (the patches, ORDER.md's lines and TODOs, the index, the commit); the prose;
  `RECORD=1 tools/batch-check.sh` writes and commits its PASS (567). A design against s6: lab/evolve/design.py (the batch).
- A seed's checklist holds what to judge and read, never state - a batch waiting, the hours, a bar: those print from
  their sources (process-run's summary, ORDER.md, `stopping.py --bar GEN`). Seed 81's restated one went stale (567).
- Replies: the answer first, short; nothing a tool output already showed, restated.
- Effort: xhigh for the routine; max for the unexpected - a failed chain, an odd result, a design decision.
- Recurring steps become scripts; the judgment stays in the chat - prompts/21, item 9 (Iteration 552).
- Tool calls: never `pkill -f` a pattern in your own command line (it kills your shell); a file written after an `&&`
  step that can fail is lost with it - check what was written; remove a background job's old output before polling it
  (a stale file reads as done); a sandbox restart kills background jobs and keeps /tmp - the status file says where to
  resume; no quadratic loop over a run's records (a call's 300 s).

## Where to look - the first place for each question (568)

Grep first, then read the one section it finds; never read whole PROGRESS.md, predictions.md or a HISTORY file.
- The present, the next step, the open decisions: this card.
- A run's results: results/evolve-amd-ryzen-7-pro-8840hs-seedN.md (its title is the run in a phrase); every run at
  once: results/progress-by-run.md; the stopping rule's ledger: results/stopping-series.md; other machines:
  results/xcheck-seedN.md.
- The stopping rule, the measures, the end of the phase: GOALS.md; the next run's bars: `stopping.py --bar GEN`.
- A prediction: results/predictions.md, `grep -n "^## Seed"` - the newest at the end.
- A subject in results/: results/README.md, by subject - its "### " headings (runs, faults, the JIT, machines,
  the search, the end of the phase, other models' answers), then a term.
- A gene: `grep -n "gene('NAME'" lab/evolve/evolve.py`; its history: lab/evolve/HISTORY.md; its votes:
  results/gene-votes.md.
- A tool: lab/evolve/README.md's tools, one line each; its usage: the tool's docstring.
- An owner's decision: HANDOFF-REFERENCE.md's "standing decisions"; when and why: `grep -n TERM PROGRESS.md`.
- A batch: results/applied-after-seed83/ORDER.md while it waits, results/applied-after-seedN/ORDER.md after.
- A past iteration: `grep -n "^## Iteration N" PROGRESS.md`, that entry only; the card's history to 562:
  HANDOFF-HISTORY.md; GOALS.md before 275: results/drafts/goals-snapshots.md.
- Every document: README.md's "Documents"; the prompts: prompts/INDEX.md.

## Before a chat's turn ends - every turn that changed the repository

1. Commit everything that should survive. A script that produced a figure
   recorded in PROGRESS.md goes into the repository (lab/evolve/ or
   results/drafts/); every other file you wrote in /tmp is deleted or listed in
   `/tmp/handoff-disposable.txt` - `sh tools/disposable.sh PATH REASON` writes the line (568). A file the
   iteration adds under results/ is named in its PROGRESS entry (handoff-check 13).
2. Bring this file up to date: "master: Iteration N", the state, the open
   items - a card: history goes to HANDOFF-HISTORY.md; write the PROGRESS
   entry - about three lines: what, the numbers, the files.
3. `runuser -u claude -- sh tools/make-bundle.sh /mnt/user-data/outputs` - it
   runs `tools/handoff-check.py` and refuses a bundle a new chat could not
   start from. Mid-work, `--checkpoint` makes a bundle that is not a handoff
   point (its name ends in -checkpoint). It prints the new chat's message, the bundle's name in it (568).
4. Present the bundle, and give the owner that message.
