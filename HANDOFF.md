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

- master: Iteration 623.
- **Consolidation's retirements, done (599)** - the after-seed-86 batch applied at 1b53e88
  (results/applied-after-seed86/ORDER.md): fsys 4-5 retired; s2-s5 frozen as built artefacts (stages/frozen/, checked by
  hash in --validate; s4 and s5 refused by build() from source); lean 1, varcall 1 (sharedcall with it), doesfar 1,
  bytehdr 1 fixed; scale 0 for CV8 (SCALE stays for cpt16 and sod16; the cell, sod16 and cpt16 families stay - the owner,
  590); rtloop 2 gone (canon reads 2 as 1). 53 files, 219 lines in, 358 out. batch-check PASS on 4bb5eff (its record
  commit 0c83123 says 598); on master run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS; the final set's 21 the
  same engine and image bytes before and after at both widths, none died (results/drafts/consolidate-599.sh). Of the 17
  values on no pooled-front design (results/drafts/retire-report-583.md, rerun the same): 10 retired; kept jitdoes 1 (2
  of the 21: 3ee67e7d34, be42bd8ea4), msc 1 (the Tegra: msc=0 18% slower, 598) and alignhot 1, fsys 1, jit 0, jitinl
  0, jitos 0 (no code to remove - retire-plan-583.md).
- **The final set: 21 (598)** - results/final-set-chainsBCD-seed86.md, results/final-pick-chainCD-seed86.md: the pick
  pooled over every session of chains B, C and D gives 15, chain B's and chain C's own sets add 6 (lose no good design).
  No generic pick within 25% (the best mean 06b188f45b; each class's fastest c7c35f9c97, 4ef851fd8e, 690981ca5b).
  Readings kept: results/chainB-seed86/, results/chainC-seed86/, results/chainD-seed86/sK.
- **The method section's figures, recomputed (600)** - results/article-figures-600.md
  (results/drafts/article-figures-600.py, from the ledger, the results files, the final set and the chains' readings);
  results/drafts/article-method-548.md's [74+] markers all filled. New in them: the screen loses a few front designs (2
  of 421 audited children that ran in full reached the true front, seeds 77-83); one round first none (0 of 6,934); seed
  77's clock test - not the clock (cycles 1.002); the random baseline 0.55 of the series' median hypervolume.
- **The handoff to relf (611; the smallest 612)** - results/handoff-relf-611.md, the package
  forth-vm-evolution-designs-iter612.tar.gz (outputs; lab/evolve/pack-designs.py on results/relf-designs-611.md): ten
  designs by role - c7c35f9c97 fastest x86-64, 4ef851fd8e fastest x86-32, 06b188f45b best all-round, bac37f35a2 the
  smallest JIT design (these four x86 only); 782f3ad7ff fastest portable, 690981ca5b fastest on ARMv7, c2ef9488ff the
  knee, a627b954c6 small and fast on ARMv7, fb0d57c8a2 least memory, 64a7345393 smallest (612, for cea114f47e: smaller
  at both widths, 3-7% faster in each class, as simple - the owner asked for Claude's view). Each at both widths 9 of 9
  right against s6. Phase 2 (RELF.md): relf takes mechanisms and measures them with relf-ab.sh.
- **Seed 87 processed (610)** - the portable run: portable.py BETTER than the portable designs found before
  (hypervolume +2.4%, fastest 0.2847 against 0.2978, at 32 bits 0.2888 against 0.3059) -
  results/evolve-amd-ryzen-7-pro-8840hs-seed87.md. The 282 found before, every complete session of both chains pooled
  (results/portable-pick-seed87.md; readings results/chain-seed87/, results/chain-seed87-interrupted/ - the crashed
  chain's dream 8-byte session and the Tegra's second were cut short, left out): x86-64 8cc7f60d6b, x86-32 1f2e71902c,
  ARMv7 3452cb633b and 690981ca5b tied (0.3%), the generic pick f55cec5849. Its follow-up: 611.
- **The resume fixed (610)** - seed 87's restart forked at generation 3: the replay saw each gated design's second
  reading from the start (results/drafts/resume-610.md). evolve.py replays first readings until their batch;
  lab/evolve/test-resume.py in run-tests (a crash at generation 6: the replay as the first attempt; EVOLVE_REPLAY=0
  forks - the control). The two attempts (results/drafts/attempts-610.py): the crashed one's 136 generations found the
  run's fastest at both widths; the resumed one's 262 ended below it (0.2871 against 0.2919); their union 0.2958.
- **The follow-up chain processed (611)** - results/followup-roles-seed87.md: the 45 side by side, every session complete
  (results/chain-followup87/, pooled: results/followup-pick-seed87.md). 782f3ad7ff the fastest portable design (mean
  -11.6% against 690981ca5b, -4.2% against the best found before, 8cc7f60d6b); 690981ca5b kept on ARMv7 (3452cb633b a
  tie); a627b954c6 for 22420b3b61 (the owner: 4 KB traded); 64a7345393 the smallest (612). The noise half the sizing's
  (the Tegra 0.44% a session). A GCC lineage runs about twice the laptop's time on dream at 32 bits - not factor 3 as 611
  wrote (factor needs tag2: expressed in none of them, 612); its expressed genes confounded - seed 88's chain tests them.
- **Seed 88 processed (614; deaths-check's 2 open were values retired at 599, refused the same here - expected from 615)**
  - the second portable run: portable.py BETTER than every portable design found before it,
  seed 87's included, by one extreme - the fastest at 32 bits, c7814def6d (a GCC build) 0.2803 against 0.2888; the
  hypervolume (0.2936 against 0.2979), the fastest, the smallest and memory short of their bars
  (results/evolve-amd-ryzen-7-pro-8840hs-seed88.md). The dream 32-bit experiment: the compiler
  (results/dream32-experiment-seed88.md) - clang brings both GCC bases to the control's dream/laptop ratio at 4-byte cells
  (2.13 and 1.82 to 1.17; the control 1.105): dream 25-38% faster, the laptop 14-18% slower, so the laptop's selection
  keeps GCC at 32 bits; no other single gene. General: seed 87's follow-up's 45, GCC median 1.57, clang 1.13
  (results/drafts/gcc-clang-614.py). The front-end question (623, results/drafts/jcc-count-623.md): in 614's variants the dispatch jumps' share on 32-byte
  boundaries ranks with dream's slowdown (+0.79) and alignment-only genes move it 10-24% - Intel's JCC erratum on the
  Skylake the likely cause; padding indirect jumps too clears every one (+0.4-5.2% bytes); untimed - the test needs dream.
- **Seed 88's follow-up processed (621)** - results/followup-roles-seed88.md: the 46, every session complete (the laptop 18,
  dream 28 and 25, the Tegra 3), the incumbents within 0.1% of 611's. No role changes: the smallest's candidates
  4dd4e3e7e2 (1.31% smaller, x86-32 +27.9%) and 422e922f9c (0.29%) turned down by the owner's 611 trade, which he
  confirmed (621: "performance drop is too significant and size gain is too small"); no extreme gained - seed 88's in-run 32-bit lead,
  c7814def6d, 2.1% behind 9f8811f7f4 re-measured. By the 616/618 rule the **portable search stops** after two runs.
- **Seed 89 running (started from 621's bundle at eca15d5; 622: NEXT-RUN none, so a pull of this bundle cannot start
  it again)** - the last JIT run (620, the owner's 21 hours) - `seed 89 21h widths carryall`, no experiment;
  REMOTES 617's lines screening results/screen-seed88.md (the Tegra 1255 minutes, 3 sessions at 3 rounds; dream 625 a
  width, 8 sessions). **Its processing** (prepared 622): process-run.sh as a seed - confirm.py's pool takes the portable runs'
  fronts by default now (seed 89's: 11 files, front 620, hv 0.38110; the smallest's bar 13,572 B, not 13,800); the screen
  read by followup-roles.py --screen --flagged on the remote lines' readings; when it gains, its follow-up -
  `portable-followup.py <seed 89's db> - results/followup-seed89.md --jit --seed 89 --holders results/relf-designs-611.md
  --also <the screen's flagged>`, then followup-roles.py with the six portable roles and
  fast64=c7c35f9c97,fast32=4ef851fd8e,allround=06b188f45b,smalljit=bac37f35a2 (results/drafts/jit-rehearsal-622.py PASS).
- **Before the freeze** (618; GOALS.md step 3 - results/drafts/portable-plan-602.md, "Then the freeze"): the portable search
  ended (621); seed 88's rest screened during seed 89 (620); the retire report on the final pooled
  front, every value no design on it uses retired, the winners' bytes unchanged (599's way) - previewed on today's pool (623,
  results/drafts/retire-report-623.md): 8 values on no front design, msc=1 the one with code (the owner's: 578's rule or
  598's Tegra 18%), thinhdr=0 kept for s6; the roles packed and exported
  from the final code, make test, the handoff final; the portable figures recomputed from the records. **The last JIT run (620, the owner)**: one 21-hour JIT run after the portable
  search ends, the last step before the freeze - `seed N 21h widths carryall`, its remote lines screening the last portable
  run's rest, judged by confirm.py (only what it bred counted), a follow-up when it gains, continued only on confirmed
  progress (results/drafts/jit-run-plan-620.md; the audit: results/audit-nonportable-619.md).
- **`make` builds the winners (608; ten at 611)** - the top Makefile and designs/ (designs/README.md): the ten of the
  relf handoff by role name (611: portable-fastest 782f3ad7ff, portable-arm 690981ca5b, portable-small a627b954c6; 612:
  smallest 64a7345393), each its engine's real source and a Makefile, built from source; `make test`, `make libc` (the six
  portable ones), `make 32`. lab/evolve/export-designs.py writes them and checks each engine byte for byte the lab's (20
  of 20) and each C-library build running (6 of 6). Rerun it when a role changes.
- **The article (604; open item 8)** - one article, the ladder by hand then the genetic algorithm (the owner: English
  for ForthHub, Russian for Habr): article/article-en-draft.md (19 KB) and article/article-ru-draft.md, beside the ladder
  article until he approves. Part one condensed from article/article-en.md (its paraphrases checked against it), part two
  from results/article-figures-600.md and the final pick. His reason for the switch in (605: randomising had found the
  interesting things in other projects - designs no project or paper covers); the credits (Ertl and Gregg, COLE) and the
  ending asking readers whether the designs are new (results/drafts/originality-605.md; 607: the two details have
  fixed-length precedents - Rose's ART-FORTH, Rochester 1986, uxForth, Enforth - only their variable-length forms not
  found, and the question now asks about those). Two ASCII diagrams (607, results/drafts/ascii-figures-607.py, no
  pictures - the owner): each run's hypervolume, the pooled front as speed against size. The fast end's 5-7% out of both (606, the owner:
  process, not result - it cancels in every comparison). Waiting: his review; section 17, the portable run and its follow-up, written in both drafts (612); a Russian reader's pass
  (AUDIENCE.md: a translation-shaped text is a named failure on Habr); prompts 04 and 05 before publishing; the KDPV image.
  The method draft (results/drafts/article-method-548.md): one [check] left, the offset; the follow-up chain's tool
  ready (lab/evolve/portable-followup.py).
- **Across machines - the owner's terms (576; GOALS.md)**: lose no good design or gene. final-pick.py step 5: the three
  classes' geometric mean; the 25% veto removes nothing, only names the generic pick; the three best means and each
  class's fastest ADDED to the set; a design missing a class ranked on the rest, kept. Consolidation (578, the owner): a
  gene or code path is retired only when no design on the pooled true front uses it - not the final set.
- **Predictions due** (results/predictions.md): seed 89, the last JIT run - 4 (621).
- **Before 599**: chains C and D's processing (598) - HANDOFF-HISTORY.md, "The card's state at Iteration 598"; chains
  A-D, seed 86 and the final pick's planning (582-597) - "at Iteration 597"; seeds 70-86 processed (498-582).
- **Files a new chat needs**: the newest bundle; seed 89's chain archive when it returns. appbench.zip stays on the laptop.

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
   NOT CONFIRMED by carried designs only - the pool widened, no new search. **Step 3, the final set: 21 (598)** -
   results/final-pick-chainCD-seed86.md, from chains B, C and D; consolidation's retirements done (599); the figures next. **Step 4, the random baseline, done (576)**:
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
7b. (Done, 599: results/applied-after-seed86/ORDER.md; planned at 583 - results/drafts/retire-plan-583.md.) Consolidation's retire candidates read before seed 84 returned (results/drafts/retire-candidates-573.md): the old
   values' code builds the stages s2-s5; msc kept by the Tegra's check (598).
8. The article, after consolidation: the claim is the integration, not any technique
   (results/drafts/ask-related-work-answers-539.md); every figure recomputed on the true fronts (seeds 53-75:
   results/truefronts-seed75.md, results/progress-true-fronts.md; the method section's: results/article-figures-600.md, 600); across machines the fast end as a band, the fastest
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
