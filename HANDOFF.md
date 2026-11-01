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

- master: Iteration 580.
- **The next chain - seed 86, 12 hours (the owner): the second confirmation run** (GOALS.md step 2): NEXT-RUN `seed 86 12h
  widths carryall then experiment review-checks.py spread then experiment appbench.py ...` - seed 84's chain. Its founders:
  the series' and seed 84's fronts; seed 85's random run not carried (576: next-run.sh skips a run whose WANT says random).
  confirm.py pools seeds 77-83 and 84 (the {"confirmation": 84} line). REMOTES: dream re-measures the fast-end file's 41 at
  both widths alongside (`--also @results/fastend-remeasure-575.md`, 110 minutes a line; out at seed 86's processing).
- **The re-measure STANDS (576)**: seed 84's best bred 5.9% ahead of the best of the rest idle, 6.8% loaded (the bar 2%), the
  stricter test +1.25% (the bar 1%) - results/evolve-amd-ryzen-7-pro-8840hs-seed85.md. Unexplained: the bred lead 0.8%
  in-run (group medians), 4.5% re-measured; dream's 41 test whether it is the laptop's.
- **Seed 85, the random baseline (GOALS.md step 4), done (576)**: at generation 140 the hypervolume 0.553 of the series'
  median, the fastest 2.23 and the 32-bit 2.19 times slower, the smallest 1.16 times larger; none of its front on the
  final front. A new death, 55 "body size drift": the scale-0 call reach, no fault (results/drafts/body-size-drift-576.md).
- **Processing the next chain**: the same three commands; a confirmation run - process-seed.sh runs final-set.py and
  confirm.py (as seed 84). Judge: confirm.py's verdict; dream's 41 (xcheck-seed86.md: does the bred lead hold at 64
  bits? results/drafts/fastend-icount-579.md: 1.4% of the 4.5% is fewer instructions - expect 1.4-4.5% there).
  Drafted for both outcomes (579):
  - CONFIRMED - the final pick, **two chains (the owner, 579; 580)**, neither with a seed step:
    **Chain A**: NEXT-RUN `experiment loadtest.py --ids results/candidates-final-seed86.md` (242 candidates, about 1.5
    hours on the laptop alone); REMOTES with no `--also` (take 576's out) - no host asked. Its processing:
    process-seed.sh runs final-pick.py --shortlist - results/shortlist-seed86.md, about 40: the set alone and loaded,
    the additions, each width's 5 fastest alone and loaded, the next by hypervolume, the near-misses (each record's
    why). **Chain B**: NEXT-RUN `experiment loadtest.py --ids results/shortlist-seed86.md --rounds 5`; REMOTES `--also
    @results/shortlist-seed86.md` on dream's prebuilt32 (prebuilt64 pairs it; designs 4, minutes 150 each) and rage's
    line (designs 4, minutes 900 - about 38 minutes a design there: the shortlist's first 20 or so, in its order, the set
    first), only after the owner's rage-check.sh PASS (open item 1, on fury between the chains). next-run.sh starts the
    remote checks in a chain with no seed step when a REMOTES line asks by id, each line's minutes from its start; the
    pack waits for them (580). Its processing: final-pick.py with every host - step 5 across machines, the final set.
    process-run.sh's later stages (draft-results, the checks) expect a seed pack: if it stops, process-seed.sh's
    summary has the final pick. Consolidation's retirement: results/drafts/retire-report-579.py (578's rule).
  - NOT CONFIRMED by bred designs again - per 573 another confirmation run, `seed 87 12h widths carryall ...` as seed 86's
    line (the owner's hours); by carried designs only - the pool widened, the final pick as above.
- **Across machines - the owner's terms (576; GOALS.md)**: lose no good design or gene. final-pick.py step 5: the three
  classes' geometric mean; the 25% veto removes nothing, only names the generic pick; the three best means and each
  class's fastest ADDED to the set; a design missing a class ranked on the rest, kept. Self-test passes. Consolidation
  (578, the owner): a gene or code path is retired only when no design on the pooled true front uses it - not the final set.
- **Predictions due** (results/predictions.md): seed 86 confirmed (55/45); dream - the bred lead under 2% (60/40).
- **Before 576**: seeds 70-84 processed (498-575); history: HANDOFF-HISTORY.md.
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

1. The Tegra's check (the owner, 570: clang) - the after-seed-83 batch **applied** (572, 9664214: armrt, prebuiltarm,
   ragecheck): ARM engines without the C library; rage's check of the front's clang designs, cross-built on fury. Nothing
   changes on x86. Seed 84's failed chain cross-built 15 for rage on fury (Spearman 0.953 on 16, seed 83's 0.143 on 6) -
   the packages are in. Seed 84's chain: 15 cross-built again, Spearman 0.935 on 16 - but rage busy while it measured
   (load average 4.3 on 4 CPUs). rage-check.sh's PASS is still not in an archive: **the owner runs `sh
   tools/rage-check.sh` on fury, no chain running, before the chain that re-measures the candidates on the Tegra** (575:
   not the next one). Rage's numbers from then: no-C-library engines, mostly
   clang's - not comparable with its checks before.
2. The end of the improvement phase - GOALS.md, "When the improvements are done": **step 1 done** - the rule stopped at
   seed 83 (572; seeds 77-83 on one method). Step 2: seed 84 NOT CONFIRMED at the fast end; the re-measure STANDS (576) -
   seed 86 the second confirmation run. Step 3, the final set - lab/evolve/final-set.py, final-pick.py (its first run on
   the 41 at 576: not the pick). **Step 4, the random baseline, done (576)**: results/evolve-amd-ryzen-7-pro-8840hs-seed85.md.
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
7b. Consolidation's retire candidates read before seed 84 returned (results/drafts/retire-candidates-573.md): the old
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
