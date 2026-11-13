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
  a build under a minute (17 s since the freeze, 599), run-tests about six, validate two to four. Tool calls
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

- master: Iteration 657.
- **The search is over; the freeze done - its batch applied (656), the relf handoff final (657); the article next, the last.** The improvement phase ended by the stopping rule (seed 83, 572); the final set,
  21 (598: results/final-set-chainsBCD-seed86.md, results/final-pick-chainCD-seed86.md); consolidation's retirements done
  (599: results/applied-after-seed86/ORDER.md); the method section's figures (600: results/article-figures-600.md). Then
  the portable runs (seeds 87, 88, 91) and the last JIT runs (89, 90), each with a follow-up chain on the three machines
  (results/followup-roles-seed87.md to -seed91.md; every run: results/progress-by-run.md) - the x86 roles final at 630, the
  portable search stopped at 640 - and the final check (641-649, below): no further gain. Each step's bullet as it stood:
  HANDOFF-HISTORY.md, "The card's state at Iteration 650" (before it, the states at 597, 598 and 647).
- **The ten roles - the relf handoff, final (657)** (results/handoff-relf-657.md - one document for 611 and its four updates
  628, 631, 636 and 649, which stay as history: the roles by `make` target, how to build, run and check a design, what
  relf takes; the records results/relf-designs-649.md; the package forth-vm-evolution-designs-iter649.tar.gz): fastest-x86-64 c7c35f9c97, fastest-x86-32 ee34931cd7, best-all-round
  06b188f45b, small-jit c6f1c1331b (these four x86 only, the JIT); portable-fastest 782f3ad7ff, portable-arm 3eb59b271d,
  portable-knee 11a56ff9e4, portable-small ae99617f06, least-memory fb0d57c8a2, smallest d180351903 - each at both widths 9
  of 9 right against s6. `make` builds them from designs/ (608; designs/README.md), each its engine's real source and a
  Makefile: `make test`, `make 32`, `make libc` and `make arm` (the six without the JIT; forth-arm, 646);
  lab/evolve/export-designs.py then export-arm.py write them and check the lab's bytes - rerun when a role changes. Phase 2
  (RELF.md): relf takes mechanisms and measures them with relf-ab.sh.
- **The freeze - done (657)** (618's list: results/drafts/portable-plan-602.md, "Then the freeze"; GOALS.md step 3): the
  batch applied on master and the build-out run (656, below); the retire report as 639 left it
  (results/drafts/retire-report-639.md; what stays and why: results/drafts/freeze-retire-641.md); the handoff final (657,
  above; 650's suggestion). Its last item goes with the article: the portable figures recomputed from the runs' records.
- **The final check processed (648) - no extreme gained; the smallest to d180351903 (649)** -
  results/followup-roles-seed91-final.md: the 435 (641's list) on the laptop 5, dream 7 a width, the Tegra 2 of 3 (the third
  would end past the deadline); none died. No role changed by speed: five holders kept; small and fast on ARMv7 by 629's
  pooled rule (a627b954c6 -3.21% in this chain, +1.21% +/- 0.84% over all 10 Tegra sessions with both). --gain: no line (the
  pool's in-run fastest, 38100f0280 and 95077030b0, +2.69% and +1.84% behind). **The smallest's one trade-free candidate,
  d180351903** (13,883 B, -8 B; x86-64 -0.59% - the laptop +3.40%, dream -4.43% -, x86-32 -3.85%, ARMv7 -3.30% on 2
  sessions): taken (the owner, 649: smaller at both widths, 13,883 / 13,627 B against 13,891 / 13,675, 9 of 9 right at both) -
  results/handoff-relf-649.md, results/relf-designs-649.md, the package forth-vm-evolution-designs-iter649.tar.gz, designs/smallest
  made again (forth-arm the lab's bytes, running under qemu-arm; make test 10 of 10); 01712a2639 kept (640). The Tegra's readings swing 4-5% a pair between chains (its kernel 7.3.1 -> 7.3.3 on
  2026-11-10; results/drafts/finalcheck-648.py). Next: the article - the freeze done (657); NEXT-RUN none.
- **The freeze's batch, applied (656)** - results/applied-after-seed91/ORDER.md: rtloop-after-seed91 (the partial run-time
  loop compiler, forth/cv8-fuse-loop.4 and its tables; rtloopall at 1) and rtimmlean-after-seed91 (forth/cv8-imm.4, rtimm=2
  alone in a plain design; such a genome's rtimm read as 0) - 186 lines out, 31 in. On master run-tests PASS, validate 7 of
  7, the jail PASS; the 69 designs of results/drafts/freeze-ids-656.py (the 29 winners, d180351903 among them, and 40 front
  designs drawn) the same engine and image bytes before and after at both widths, 0 died. The build-out
  (results/drafts/freeze-build-645.sh, 649's ten roles; rehearsed at 645 and 650): validate 7 of 7, the export the same as
  designs/ for 10 of 10 (the GCC three's forth-arm by export-arm.py --gcc, the cross GCC 13.3; gcc-multilib back after),
  make test 10 ok, make 32, make libc, pack-designs 20 of 20 right, the 40 the bytes of results/drafts/designs-sha256-649.txt
  - no shipped byte changed: designs/ and the package forth-vm-evolution-designs-iter649.tar.gz stand. A role changed later:
  the same command (`sh results/drafts/freeze-build-645.sh . RECORDS NAME=ID,...`, no spaces in the list), its designs/
  directory and the package made again, the handoff's records. The bullet as it stood: HANDOFF-HISTORY.md (656).
- **forth-arm (646; the owner: the engines without the C library everywhere)**: each of the six designs without the
  JIT has `make forth-arm` (srcarm/, the lab's ARM command; top `make arm`), written by lab/evolve/export-arm.py after
  export-designs.py - the clang three (portable-fastest, portable-knee, smallest) cross-built, the lab's bytes, running
  under qemu-arm (646, 649); the GCC three (portable-arm, portable-small, least-memory) by the ARM host's own GCC.
  **The rage check passed (654)** - results/rage-designs-654.md (results/drafts/rage-pack-654.py on the archive): the
  chain at c8c423671f (652's fix; the first run failed, 652), 17 minutes; on the Tegra the GCC three taken by their
  Makefiles, each `make forth-arm` the lab's bytes and running - least-memory 11,584 B, portable-small 13,440 B,
  portable-arm 15,968 B. Rage's compiler (the owner, 655): Gentoo 16.2.1_p20260926, the one all 81 rage sessions naming
  theirs carry (2026-10-17 to the final check) - the bytes the Tegra measured; 652's stray /tmp directory removed. The
  cross GCC's package removes gcc-multilib (the 32-bit x86 builds): export-arm.py --gcc last, gcc-multilib back after.
- **The article (604; open item 8) - next, the last step (the owner, 636: once everything else is done - the search's end,
  the freeze, the designs handed off to relf; the handoff written final at 657)** - one article, the ladder by hand then the genetic algorithm (the owner: English
  for ForthHub, Russian for Habr): article/article-en-draft.md (19 KB) and article/article-ru-draft.md, beside the ladder
  article until he approves. Part one condensed from article/article-en.md (its paraphrases checked against it), part two
  from results/article-figures-600.md and the final pick. His reason for the switch in (605: randomising had found the
  interesting things in other projects - designs no project or paper covers); the credits (Ertl and Gregg, COLE) and the
  ending asking readers whether the designs are new (results/drafts/originality-605.md; 607: the two details have
  fixed-length precedents - Rose's ART-FORTH, Rochester 1986, uxForth, Enforth - only their variable-length forms not
  found, and the question now asks about those). Two ASCII diagrams (607, results/drafts/ascii-figures-607.py, no
  pictures - the owner): each run's hypervolume, the pooled front as speed against size. The fast end's 5-7% out of both (606, the owner:
  process, not result - it cancels in every comparison). Waiting: section 17's smallest row (both drafts: 64a7345393's 13,891) to d180351903's at the figures
  pass (649); his review; section 17, the portable run and its follow-up, written in both drafts (612); a Russian reader's pass
  (AUDIENCE.md: a translation-shaped text is a named failure on Habr); prompts 04 and 05 before publishing; the KDPV image.
  The method draft (results/drafts/article-method-548.md): one [check] left, the offset; the follow-up chain's tool
  ready (lab/evolve/portable-followup.py).
- **Across machines - the owner's terms (576; GOALS.md)**: lose no good design or gene. final-pick.py step 5: the three
  classes' geometric mean; the 25% veto removes nothing, only names the generic pick; the three best means and each
  class's fastest ADDED to the set; a design missing a class ranked on the rest, kept. Consolidation (578, the owner): a
  gene or code path is retired only when no design on the pooled true front uses it - not the final set.
- **Predictions due** (results/predictions.md): none. Scored: the rage check's (654) 1 of 1; the final check's (648-649)
  2 of 4 (wrong: the Tegra 2 of 3; a role changed - the smallest, 649).
- **History**: HANDOFF-HISTORY.md - the card's states at 597, 598, 647 and 650 (seeds 70-91, chains A-D, the final pick, the
  portable runs and their follow-ups, the final check's plan) and its forth-arm bullet at 653 and its freeze's-batch bullet at 655 (the rage check's first
  run); remote hosts cleaned after every chain (628: `sh lab/evolve/remote-checks.sh clean runs/chain-...`).
- **Files a new chat needs**: the newest bundle. appbench.zip stays on the laptop.

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

3. **Correctness - none open (576)**: seed 85's 55 "body size drift" deaths the scale-0 call reach, met where varcall
   and doesfar exempt a design from reach_lethal() - no wrong output (results/drafts/body-size-drift-576.md). seed 82's deaths all expected (cpt16 on apps 36, the scale-1 reach 10). Seed 80's two JIT deaths - jit_scan's 160-byte window cut st_execute under
   -falign-*=64; ccflags() built alignhot where express() drops it (results/drafts/jitexec-alignhot-566.md) - fixed by
   the after-seed-81 batch, applied at 17566c6; seed 81's one such death right after it, wrong before (the control).
   Before: none open (564): seed 78's kernel deaths are the scale-1 reach limit (Iteration 10), not a fault.
   The JIT's value holes fixed and applied (560: corpus-deaths-555.md, jit-sweep-558.md).
4. The fast end's offset (rule 3; seeds 73-76 1.070, 1.066, 1.047, 1.063) - results/drafts/fast-end-offset-554.md: a cost
   every workload's run pays, a design and s6 alike, outside user space - not the JIT; seed 76's re-measure agrees (the
   non-JIT designs 0.988, below 1 as predicted). Seed 77's clock test measures the cost both pay, by workload.
7. Deferred: the JIT on ARMv7, for the Tegra session (results/drafts/ask-arm-jit-answers-512.md); an uncertainty-aware
   screen tested offline (results/drafts/ask-search-answers-525.md, proposal 2).
8. The article, after consolidation: the claim is the integration, not any technique
   (results/drafts/ask-related-work-answers-539.md); every figure recomputed on the true fronts (seeds 53-75:
   results/truefronts-seed75.md, results/progress-true-fronts.md; the method section's: results/article-figures-600.md, 600); across machines the fast end as a band, the fastest
   named per machine (results/drafts/xcheck-agreement-546.md; seed 76's checks: 3d4e860a9f the fastest on dream). The
   method section drafted (results/drafts/article-method-548.md).

Closed or moot: 1, 2, 3b, 5, 6 and 7b - HANDOFF-HISTORY.md, "The card's state at Iteration 650" (651).

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
