# HANDOFF - start here in a new chat

This file is the handoff, kept current: it says where things stand now, and
every chat updates it before it presents a bundle (`tools/handoff-check.py`
fails when it is behind the state). PROGRESS.md is the history - read its
entries after the iteration named below. Everything needed is in the
repository; nothing from an earlier chat's machine or transcript is.

## What this is

**The aim is simplicity and minimalism** (GOALS.md; the owner, Iteration 72): the smallest,
simplest system that does the job - small images, a small and plain engine, few mechanisms, each easy
to read and to remove; speed where it costs little, never as a reason for complexity. The size
objective (engine plus image bytes) measures part of it; the rest - a mechanism kept only if it earns
its place by measurement - is how every change is judged. Restated here at Iteration 368, the owner
asking that it be explicit: a summary written from this file had left it out.

An evolutionary search over the design of a Forth system: the engine
(`engine/vm-lab.c`, computed-goto C), the kernel (`forth/kernel.4`,
cross-compiled by `forth/cross.4` in the cell system), the converter
(`tools/layout.py` with `tools/sod16.py`: the cell-threaded dump into the
byte-coded CV8 / tag-2 image), and the evolver (`lab/evolve/evolve.py`: NSGA-II
over genes; three objectives - speed: the geometric mean of median cpu time
over the selection workloads against the hand-made s6; size: engine plus image
bytes; memory: rss). The owner, Kirill Timofeev, runs the seeds on his laptop
(AMD Ryzen 7 PRO 8840HS, "fury") per `lab/evolve/NEXT-RUN` and sends back two
packs: the run (`forth-vm-evolution-seedN-<commit>-fury-<time>_tar.gz`) and the
comparison (`forth-vm-evolution-compare-fronts-..._tar.gz`). Commits are
authored `Kirill Timofeev <kt97679@gmail.com>`; deliveries are git bundles.

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

- master: Iteration 507.
- **The runs**: **seed 70 processed (Iteration 498)** - inside the replicates' spread (at generation 109 fastest 0.1259,
  smallest 14,143); **the four JIT genes on no front design** - tried on thousands, dominated: the six workloads do not pay
  for them and they cost bytes; the applications 0.756 of s6 on its fastest. **906 32-bit failures, all JIT designs** -
  CELL+/CELLS (fixed in the batch). **The after-seed-70 batch applied** (six patches, batch-check PASS): the applications
  the seventh selection workload, jitrp enabled, jitos frozen, nocase staged frozen - results/applied-after-seed70/.
  **Seed 71 next: 10 hours (the owner)** - the speed column breaks at it (seven workloads). **499: nocase's acceptance
  passed** - coreext.4's [ELSE] matches [IF], [ELSE], [THEN] without case (on master directly - a run-time library the
  search does not load; seed 71's bundle is unchanged): lexex and benchgc then run unmodified, as fcp and cd16sim did -
  all four Appbench programs that stopped on case. **501: the owner retired nocase** (the after-seed-71 batch); the
  process review (results/drafts/process-review-501.md): engines-check now runs the JIT at 32 bits and a differential
  JIT test on every JIT variant; batch-check refuses conflict markers; four proposals for the owner. **502-503 (the
  owner): rules 11 (a gene paid for before it is enabled) and 12 (votes' grace period - from seed 72 for the four JIT
  genes and jitrp); the fast gate takes the slower of its two readings (the after-seed-71 batch's second patch).**
  **504**: the footprint experiment dropped from seed 72's line (the owner; the 4 MB check stays in engines-check);
  jithelp and jitre retired - the after-seed-71 batch's third patch. **500: two more held-out
  applications from scratch** (apps/wordfreq.fth, apps/minif.fth; appbench.py's default) - seed 70's fastest at 0.537
  of s6 on them, 0.204 with the four JIT genes, every output right.
  Before - **seed 69 processed (Iteration 487)** - islands ran (700 island lines) and **failed their prediction**:
  at generation 109 fastest 0.1274 against the replicates' 0.1197-0.1298, smallest 14,199 against 14,039-14,207 - inside
  the spread (its end, generation 175: 0.1125 and 14,043). By 464's rule islands are not kept. **The after-seed-68 batch
  applied** (the JIT at 32 bits, the stencil check; batch-check PASS) - results/applied-after-seed68/. **Seed 70 next:
  11 hours (the owner), no islands, the four JIT genes enabled, the applications held out after the spread** - a break
  in the 32-bit column from it. The gene votes count only the genes a run's code had (487: seed 69's would have voted
  against jitmul, jitdoes, jitexec and jitcfa, which it never had). **For the owner**: jitos a freeze candidate (12 of
  12 over seeds 67-69); rtfuse no longer. **The after-seed-70 batch waits** (488, results/applied-after-seed70/ORDER.md): native
  (ABORT"), JIT_MAXOPS 1024; **489-490**: image words' ends from the converter, depth 16 with depth refusals not
  cached (fcp's DABS, nine calls deep, had stayed bytecode with its eight callers), 2>R/2R>/2R@ compiled in place -
  **the JIT leaves 0.1% of fcp's, brainless's and cd16sim's work; the fast design at 0.234 of s6 on the applications**.
  Master stays what seed 70's bundle tests. **493: the batch's third patch - the new genes at 32 bits**, and a bug of
  the applied 32-bit batch found (and **494: jitrp, the 465 prototype made a gene, the batch's fourth patch, staged
  frozen** - loop -19% of instructions on a GCC JIT design; **495, the owner's decisions as the fifth patch: the
  applications the seventh selection workload (a speed-column break), jitos frozen, jitrp enabled**; **497: the gene
  nocase, the sixth patch, staged frozen** - fcp and cd16sim run unshimmed with it): the JIT's CELL+ and CELLS assumed eight-byte cells - **seed 70's 32-bit JIT
  designs may compute wrong addresses where those are translated**: look at its 32-bit failures at processing. **491: the applications in the selection priced** (results/drafts/
  apps-selection-491.md): as a seventh workload the four genes show threefold (0.573 to 0.193 of s6) - a draft patch;
  the owner's decision.
  Before - seed 68 processed (Iteration 464) - **and islands never ran**: seeds 65-68 asked for them, but next-run.sh
  lost the word in its detach (no NEXT_RUN_ISLANDS beside NEXT_RUN_NOEVOLVED and NEXT_RUN_WIDTHS) - their logs hold no
  ", island " line. **Fixed (464)**: carried through the detach, shown in the chain's lines, and seed-facts.py reports
  "islands: on/off" from the log. The islands "trial" of seeds 65-67 voided: **seeds 64-68 are five plain replicates** -
  at generation 109 fastest 0.1197-0.1298, smallest 14,039-14,207. **Seed 69: the real islands trial, 12 hours** (the
  owner's hours; NEXT-RUN). **The after-seed-68 batch deferred to seed 69's processing** (the 32-bit JIT changes what
  "widths" selects for, so it waits a run - one change at a time). **For the owner, later**: the votes' new candidates
  rtfuse and jitos (12 of 12 over seeds 66-68).
- **Application workloads** (the owner, 466-467; results/drafts/appbench-466.md, -467.md): Appbench is the suite to
  hold out (applications run deep stacks and many calls - RPyForth 2026); **the owner's appbench.zip runs: fcp, brainless
  and cd16sim on s6, their own checks PASS** (results/drafts/appbench/run.py ZIP PROGRAM; the zip outside the repository -
  terms differ); lexex and benchgc stop on case-sensitive lookups. **The held-out tier built (468): lab/evolve/appbench.py**
  - a chain step once the zip has a path on the laptop. **First reading (results/drafts/appbench-468.md): the evolved lead
  does not travel** - seed 68's design at 0.140 runs the applications at 1.03 of s6. The owner (468): a case-insensitive
  gene, with concerns - planned, not built; coreext's words stay out of the image (the size measured is the base image;
  the applications load extend.4 and coreext.4 themselves, in 0.01-0.06 s). **Seed 70's line gets `then experiment
  appbench.py --zip ~/Downloads/appbench.zip --sample 16`** (the owner: the zip in ~/Downloads). **Our own applications
  (469)**: lab/evolve/apps/sim16.fth, written from scratch - a CPU simulator checking itself; appbench.py runs it
  without the zip; **and three more (470, the owner: all three): gc16 (a collector), scan (a scanner generator), evo (a
  genetic algorithm)** - appbench.py's default is all four of ours with the three of Appbench; on seed 68's fast design
  ours run at 0.566 of s6 (Appbench's at 1.03, the selection's workloads at 0.140). brainless, public domain, may be
  copied in as it is. **Why the lead does not travel (471, results/drafts/jitapps-471.md)**: on seed 68's fast design
  the JIT leaves 37-94% of the applications' dispatches interpreted - operations without stencils (the multiply and
  divide under *, CELLS, MOD, /) and EXECUTE sink whole words; proposed: those stencils, EXECUTE native. **The owner
  (472): genes for them.** Named: UM*, UM/MOD, DODOES, EXECUTE the four largest. **jitmul built and tested, frozen off
  (staged)**: UM* and COUNT native; UM/MOD written but unmapped until a zero divisor can THROW -10 from native code.
  **jitdoes built and tested, frozen off (473)**. Measured on seed 68's fast design with both: **scan's interpreted
  work 93% to 4%**; gc16 37% to 33%, evo 83% to 68% (UM/MOD next); fcp, brainless, cd16sim unchanged - their DOES>
  children are reached as callees (no JIT header); next: a DOES> child at its call, UM/MOD's throw path, EXECUTE.
  **Later in 473**: children taken at their call - fcp 72% to 54%, brainless 94% to 57%, cd16sim 87% to 66% left -
  **but jitdoes gives those three wrong results** (appbench.py's checks; the corpus and a DOES> test pass): frozen,
  NOT to be unfrozen until found. **jitmul is right on all seven applications; scan at 0.150 of s6** (was 0.687).
  **474: the fault found and fixed** (the return-stack check read the operation table at the literal's code) - with
  both genes every output right, the fast design 2.0 times s6 on the applications (1.3 before). **The owner: jitmul
  enabled** (out of FROZEN) - **seed 70 then carries it with the 32-bit JIT batch** (two changes, the owner's choice;
  the batch still applies on top, checked). jitdoes frozen until the owner says. Next: UM/MOD's throw path, jitexec.
  **475 (the owner): jitdoes enabled; UM/MOD native** (its throw path: -10 THROW from native code, as the interpreter)
  - **the fast design at 2.4 times s6 on the applications**, every output right. The pending 32-bit batch rebased onto
  it. Seed 70 carries the batch, jitmul and jitdoes (the owner's choice), and the appbench step. Next: jitexec.
  **476: jitexec built, tested, staged frozen** - EXECUTE through a helper (native, translated now, else interpreted):
  with all three the fast design at 2.9 times s6 on the applications (sim16 2.7x faster, brainless 40%), but fcp a
  third slower (an untranslatable token's trip through the interpreter). **477: the owner enabled it** - seed 70
  carries jitmul, jitdoes and jitexec with the 32-bit batch. Next for jitexec: a cheaper trip, or a caller left
  interpreted when its tokens lead to untranslatable words (fcp). **481-483**: EXECUTE's inline cache (small - 0.9% of
  sim16's instructions); fcp's real cause found - evalLP and evalDP refused by a return-stack check that read down the
  page; **jitcfa** checks along the paths: fcp 0.646 to 0.392 of s6, the fast design at 0.344 on the applications (2.9
  times s6). **The owner enabled jitcfa** - seed 70 carries jitmul, jitdoes, jitexec and jitcfa. Pending batch rebased.
  **484 (measured before partial translation)**: SP@ and ALIGNED stencils (jitmul; PICK stands on SP@), jitdoes takes
  fused DOES> code - the fast design at **0.301 of s6 on the applications (3.3 times)**. Open: gc16 refused at DODOES
  with no DOES> in it; partial translation for return-address words, words over 256 operations, nested JIT opcodes.
  **485-486**: gc16's puzzle was `." HEAP FULL"`'s count byte decoded as DODOES; inline strings and cold calls (I/O,
  ABORT, THROW through EXECUTE's helper) in jitexec - gc16 0.434 to 0.219, the applications at **0.272 of s6 (3.7x)**.
  jitre tried: fewer dispatches, slower where hot - transitions too dear. **The pending engine patch had an unresolved
  vm-lab.c conflict since 475** (my rebases); repaired from the original, engines-check PASS at both widths on top.
  The pending batch rebased again (applies to 8c2731a). Gforth's siev, bubble, matrix run on s6 with case folding and a prelude (no NIP, no .( in
  our kernel). Proposed: a held-out tier of applications; NIP, .( and [IF] by prelude or in the kernel.
- **jitrp - a prototype** (the owner, 465; results/drafts/jitrp-465.md and .patch): the JIT's return-stack pointer in
  r15; seed 68's fastest GCC JIT design runs loop with 19.9% fewer instructions (cachegrind, exact), ackermann 2.1% more.
  Five steps to a gene (GCC only; a register clear of regpin's; with jitk; engines-check; the laptop's timing) - after
  the 32-bit JIT batch's run. valgrind is installed here: exact instruction counts where this machine's timing is noise.
- **The JIT at 32-bit x86 - a working prototype** (the owner, 460; results/drafts/jit-i386-460.md and .patch): s6 with
  the JIT built at 32 bits passes the corpus, speed 0.956 to 0.767; a variable-alignment bug fixed on the way. **Made
  real as the after-seed-68 batch (461, the owner; results/applied-after-seed68/ORDER.md)**: eval32 keeps the JIT, jitk off at 32 bits,
  dream's prebuilt 32-bit sample takes JIT designs, engines-check 81 paths; seed 67's front JIT designs 1.9-2.9x faster
  at 32 bits. **A break in the 32-bit column from seed 70** (applied at 487).
- **The second pass over c4's circle** (the owner, 462; results/drafts/c4-family-459.md): the code-copying literature
  (Ertl and Paysan 2025, copy-and-patch, CPython's JIT, Deegen); **six ideas for the owner** - a stencil relocatability
  check, stencils from relocations (the way to ARM), jitrp (the return stack in a register), wider jitinl, a no-vectorise
  gene, Forth application benchmarks held out. **The first done (463): the stencil safety check - patch 3 of the
  after-seed-68 batch** (stencil-check.py, objdump-exact, in engines-check at 64 and 32 bits; a runtime guard in jit.c):
  today's stencils all safe; a stack protector would make all 43 unsafe, latently.
- **c4's family looked at** (the owner, 459; results/drafts/c4-family-459.md): our JIT already has its lessons; **proposed
  for the owner: the stencil JIT ported to i386** (the 32-bit builds have no JIT - about 2.6x behind; ARMv7 after, AMaCC,
  Squint and shecc as references), a JIT-redundancy probe, an interpreter-in-Forth workload; for Fern, c4's frames and
  structure.
- **Fern, a scripting language on this Forth** (the owner, 457): designed - results/drafts/fern-design-457.md - and to
  be built in a chat of its own, from this bundle; the evolution's chats carry on as before.
- **Files a new chat needs** (Iteration 415), beyond the newest bundle: the chain archive of every seed not yet
  processed - seed 71's, named from the bundle it starts from (seed 70's, `forth-vm-evolution-chain-b4c0b9c69d-fury-
  20261024-161913_tar.gz`, processed at 498). Seed 70's chain carries its own spread (every run's database on the
  laptop) and the applications (appbench.zip in ~/Downloads). For seed 66's islands reading seed 64's database is kept here too
  (build/evolve/keep/seed64-db.jsonl); if gone, seed 64's archive. Every processed run's facts and front are in results/evolve-*-seedN.md; its database stays on the laptop
  (runs/archived-*).
- **The code**: the after-seed-59 batch applied (Iteration 389, results/applied-after-seed59/ORDER.md: opcall only
  where the tag is built; a failed tool's first error; `noevolved`; compare-fronts' sign labelled, its 32-bit fastest
  kept, its speed from both CPUs). Pending: the after-seed-62 batch - the fast gate, and the genes jithelp and
  jitre (the owner, 397: try them), and the bfind fix at 4-byte cells (399, item 0f) the tail engines' (400), musttail on every clang tail engine (401) bfind built in TOS designs (402), the gene jitret (404), GCC's 32-bit t2call tail call (405; the batch rehearsed,
  results/rehearsal-405.md) the simplicity review's freeze (409) I+ on the two-bit tag (412) programs past 4 MB on plain CV8 (416) and the stage build's overlay check (417) - apply it only at seed 62's processing, so seeds 60-62 run one evolver.
- **The latest processed: seed 59** (Iteration 398): small at both widths - seed 58's start with the tag-2
  requirement, its cost replicated (the small end +12.5%, 32 bits +11%, the 64-bit fast end alike); within the
  requirement the gains stopped at generation 88 of 143. Seed 58 (384), free: plain CV8 took the small end and 32
  bits. Every run's extremes: results/progress-by-run.md.
- **The remote checks**: on Iteration 379's path since seed 59 - the evolution six minutes after the checks (seed
  58: 55), and the probes answered the owner's question of 379-381: the copies take a second (the Tegra 7,219 KB/s);
  the Tegra's long wait is its own build, about 36 minutes, now in the background.
- **The method since Iteration 386** (results/review-methodology-386.md, its proposals all done or queued; the
  follow-ups verdict-audit-388.md, convergence-seed58.md, tools-audit-394.md): the verdict from both CPUs, the fast
  gate, heldout's top-end lines, review-checks.py's progress and spread, process-seed.sh and batch-check.sh.

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
   lab/evolve/evolve.py --validate` (7 of 7 IDENTICAL), `python3 lab/evolve/test-jail.py` (PASS - last, and alone: here
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

## The owner's standing decisions

- **The Tegra compiles for itself, in parallel, never slowing a run** (Iteration 429). No cross-compiling on the laptop
  (its ARM cross-compilers would displace gcc-multilib, which the 32-bit selection needs), and no phone (Termux) host:
  too much effort for the result (428). The Tegra builds natively with its GCC - so it checks GCC designs without the
  JIT - with REMOTES' minutes "run": the whole of the evolution's time, never past it; every check's deadline is capped
  at the evolution's end (remote-checks.sh, RUN_UNTIL), so the chain never waits on a host. Its only cost to the
  laptop: its sample, made before the evolution - about 2 minutes (20 designs, each built and alive at 32 bits here).
- **An article from the findings - a goal, deprioritized (Iteration 366).** Revisited when the
  best designs are found, and written from PROGRESS.md: so every iteration has its entry, with its
  numbers, and **names every file it adds** under results/ (PROGRESS.md, Iteration 366: the audit and
  the index of what no entry had named).
- **A generic Forth first (Iteration 365).** This lab builds a generic Forth, with no optimization
  for relf's shell: (1) the best generic designs, found here on this lab's own workloads; (2) then how
  they fit relf and its shell; (3) only then relf tuned for its shell - and relf too kept as generic
  as possible. Nothing is selected by relf's shell profile (RELF.md, the order of the work).
- **One command, one archive (Iteration 302).** The laptop runs one script and gets
  one archive to send back: every step's results and every log, so a failure is
  diagnosable without a second round; made at the end even when a step failed, and a
  failed step does not cost the others. Privileges are asked at the start, while the
  owner is there; anything needing them later goes to a root helper forked at the
  start that polls for its condition, and chowns every file it creates - no
  root-owned files in the owner's home. The code is pulled once, at the start; the
  checks (build, tests, validate, jail) run once per chain. Measurements run at the
  chain's start, on the front that just finished. `next-run.sh status`, `monitor` (a
  read-only follower of the chain's one log, with progress lines in the seed run) and
  `stop` (Iterations 303-304); cleanup on every exit, and at every start a repair of
  what a crashed or killed run left (Iteration 303). Remote checks on dream.lan (Intel
  i7-6700, Skylake) and rage.lan (Tegra, ARMv7, 32-bit), by ssh from the laptop,
  alongside each seed run on the front that just finished - adding no hours
  (Iteration 306). (prompts/08 items 11-16; the specification:
  results/drafts/runner-protocol.md.)
- What each objective measures, how a run is judged and when evolution stops,
  and that the size is the kernel's (Iterations 75, 127, 138, 188-189):
  GOALS.md, "Success" - not repeated here.
- Demote, don't delete: the attic (a tenth of parents); the 8 best by Q always
  survive. The surrogate screen: pure Python, 30%/5%, one screened child in ten
  audited.
- Offer trade-offs to evolution as genes rather than deciding (factor's levels,
  Iteration 267). Small gains count: size savings are exact - take them; speed
  ones go in as genes (261).
- Noisy timing questions go to the laptop; on the VM (+-10%) decide by the
  profiler's dispatch counts, which are deterministic; to time two engines,
  alternate them over many rounds.
- I/O (202-211): keep both families - native I/O primitives (fsys 0) and the
  single SYSCALL primitive (fsys 1-5). No buffering of input from stdin, pipes
  or anything that cannot seek; output buffers on the heap, never in the
  dictionary; terminal output unbuffered; read-ahead only where a file can
  seek, given back before any other use.
- No limits a developer could hit (237): 32-bit dispatch offsets; opcode maps
  not narrowed to 8 bits. Developer friendly (227): core words in the kernel,
  helpers where convenient in balance with size, reusable non-standard words
  keep their names.
- Primitives together at the start of the dictionary; headers link-name-code;
  bit 7 of the count byte free; >NAME in coreext.4 (242-244). UTF-8 names must
  work (231-242). A zero divisor is -10 THROW; an uncaught THROW names its code
  (229). A fault handler in every engine (252). GNU_STACK kept (251).
- The kernel workload (cross.4) is a yardstick, not a design: left as it is
  (257). Clang is a gene (262); an assembly engine not now (262).
- From the Forth collection (`reference/forth-archive/`): code only from
  public-domain, permissive or the owner's own sources; GPL ones (SOD32,
  gforth, SP-Forth, bigFORTH) for ideas only.
- Deferred, the owner's call (GOALS.md's register): packed names, hidden
  internal names, a compressed image, the stack header, cross.4's fast path.
- Every patch: tested, then verified to apply in order on a fresh clone and to
  reproduce the tested files; batches wait in `results/pending/` with ORDER.md. `tools/batch-check.sh` runs that test (Iteration 394).
- Run lengths are the owner's - ask for each run's hours (seed 48: 6).

- **Superinstructions kept for now** (Iteration 389), though they buy nearly nothing: 0.27% of dispatches with the
  JIT off, 0.9% with it on, bytes either way (results/supers-knockout-seed58.md).

## Open items (Iteration 505 - the list now; Iteration 369's below it, much of it done, kept for its history)

0. **Seed 71's processing** - by results/drafts/seed71-checklist-505.md, written before its results: the first run with
   the applications in the selection (a speed break - the progress table and the spread mark it, 505); the
   after-seed-71 batch (results/pending/ORDER.md: nocase retired, the fast gate's slower reading, jithelp and jitre
   retired) batch-checked, then applied; seed 72's line without the footprint experiment (the owner, 504).
1. **Do the JIT genes earn their place now?** Seeds 71-72: jitmul, jitdoes, jitexec, jitcfa on the front, the
   applications' speed (predictions at 495); their votes count from seed 72 (rule 12). If not even with the
   applications paying, they are rule 11's case for freezing.
2. **The JIT on ARMv7, for the Tegra** - SPN's stencils have ARM holes already (movw/movt pairs, Iteration 30); jit.c's
   copying and patching are x86's (rel32 calls and jumps, the trampolines, the helpers' calls); copapy (MIT) shows the
   ARM relocations (results/drafts/scout-answers-480.md). Several sessions; after item 1.
3. **Partial translation with cheap transitions** (results/drafts/jitapps-471.md) - since 490 the JIT leaves 0.1% of
   the applications' dispatches to the interpreter: little left for it.
4. **Rule 9** (the rtimm=2 / rtfuse overlap) - PROPOSE every run: "rtfuse governs" waits on the owner.
5. **The fast end's optimism** (rule 3) - the slower reading from seed 72; predicted to pass (503).

## Open items (Iteration 369's list)

Rewritten at Iteration 369 to the state now (the list before it: git, the commit before Iteration 369);
under GOALS.md's aim - simplicity and minimalism - and the owner's order (RELF.md): a generic Forth first.

0. **Seeds 60-62** (the state, above), each by the routine. Seed 60 answered the anchoring question (Iteration 406; results/review-methodology-386.md,
   3c): small at both widths, no gain past a bar - no evidence of anchoring at 12 hours; seeds 61-62 how far
   runs of one start spread. Then the after-seed-62 batch: seed 63 its first run, free of the tag-2 requirement (the owner, 409: seeds
   59-60 ended 11-12% above seed 58's free small end; free, it is like-for-like with seed 58's curse figure - and
   seed 60's own, 1.066, is already below seed 58's 1.112). **Planned: 10 hours (the owner, Iteration 434; 11 at 426)** - seed 60's shape without the
   requirement, NEXT-RUN's line at seed 62's processing:
   `seed 63 10h widths noevolved then experiment compare-fronts.py --rounds 6 --widths 8,4 --frontier --cpus 2,8`,
   a verdict against seeds 59-62. The comparison is reserved from the 10 hours (next-run.sh's reserve()): about 6 3/4
   hours of evolution (seed 60, 12 hours with the same step: 8 h 50). **Its decisions by results/seed63-rules.md**,
   written before its results (the owner, 430), checked against losing good designs and adopted (431), measured by
   review-checks.py rules in process-seed.sh's summary (438); genes by
   votes, not by rule (432: results/gene-votes.md, appended from seed 63's processing on) - `review-checks.py curse` on its report
   shows whether the fast end's optimism falls from seed 58's 1.112, and jithelp's, jitre's and jitret's share of its front
   whether they stay (the owner: out again if useless).
0f. **Why designs fail at 32 bits** (Iterations 399-401; results/bfind32-fault-399.md, results/fail32-400.md): every
   32-bit failure of seeds 58 and 59 classified - none a design that cannot exist there. Bugs, fixed in the after-seed-62
   batch: bfind's walk (418 + 2,057, patch 4); the tail engine built for x86-64 and compiled for i386 (patch 5). A
   missing guarantee: clang's tail engine without musttail, whose i386 dispatches clang made no jumps (74 + 86) -
   musttail on every clang tail engine (401, patch 6; the owner asked for a view). The owner (400): understand why each
   fails before ruling. Proposed: no design dead for a machine class - a bug fixed, a mechanism impossible there left out
   of that class's build (as the JIT, 336); until a class is classified, the slowest there (336). At 64 bits (402) seed 59's one death class, the reach limit (188), is the designs' own -
   dead on every machine. Open: the Tegra's link
   failures (item 0d - seed 60's chain records their first error).
0g. **The 32-bit hosts against the laptop's 32-bit speeds** - done (Iteration 402, results/xcheck32-402.md):
   `xcheck.py --report OUT.json --laptop32 <the checked run's results/evolve-*.md>`; process-seed.sh runs it for every 4-byte
   host (Iteration 403). Seed 59's checks of seed 58's front: the Tegra 0.709 against the 64-bit speeds, 0.857 against the 32-bit; dream
   at 32 bits 0.651 and 0.650 - for dream the machine, not the width (item 4d).
   Its sample was small because a 4-byte sample took GCC's designs only: prebuilt32's takes clang's too (Iteration 408) -
   seed 60's front, 109 eligible where seed 59's gave 6.
0d. **The Tegra's build failures - closed** (Iteration 441): its rebuild test in seed 63's chain built all seven asked
   for, the four that had failed (alignhot 32 and 64) among them - alignhot left out of 32-bit ARM builds (407) was the
   whole cause. The history below.
   Before: **The Tegra's build failures - named** (Iteration 406, results/xcheck-seed60.md): not the linker but the
   assembler, `bad immediate value for offset (5224)`. Every one of the 14 that failed in seeds 58-60's chains has
   alignhot 32 or 64, every one of the 28 that built 0 or 1 - most likely GCC's ARM literal pools placed without the
   padding that alignment adds, a load then past its 4 KB reach (the fsys lead was a correlate). Built (Iteration 407, the
   owner): alignhot left out of a 32-bit ARM build (evolve.py's ccflags, ARM32), as the JIT is of a 32-bit one - in master,
   the laptop's and dream's builds unchanged; seed 62's chain is the first to check it on the Tegra - **but it cannot**
   (425): seed 60's and 61's fronts carry alignhot 0 on every design, and the chains check the front before - so
   nothing they sample fails that way. **The directed check is set (the owner, 428): seed 63's chain** (seed 62's ran from
   Iteration 425's bundle, before it) - REMOTES' rage
   line asks for four of the 14 by id (xcheck --also): two alignhot 32 that failed at the link, two alignhot 64 that
   failed in the assembler. At seed 63's processing: the report's "Asked for by id" line (process-seed.sh's summary
   shows it) - all four built closes the item; then --also out of REMOTES (its minutes stay "run", 429). 429 fixed the
   lookup: 428's --also looked for genomes beside the sampled report - in a chain the archived run's report.md, where
   no results file lies - and would have left all four out; it reads the repository's results now.
0h. **Programs past 4 MB** (the owner, Iterations 415-416, results/bigprog-416.md): supported by every design from the
   after-seed-62 batch (patch 12) - plain CV8's call, link and DOES> reaches extended, the two-bit tag's already 1 GB;
   engines-check runs two such programs. Cost: +104 bytes a plain-CV8 image (417: the far call by (FAR)). The stage build now
   stops on an overlay that does not load (417, patch 13). The batch rehearsed on plain CV8: results/rehearsal-417.md.
2. **Generalization** (results/generalization.md, Iteration 305): selection is measured on small
   programs. The second CPU is done (the remote checks: dream.lan at both widths, the Tegra); still to
   build: a held-out workload whose code footprint grows - generated programs of N words, hot and run
   once, and a compile-heavy one - each front design's time per dispatch against N.
   **The generator is built** (Iteration 370: lab/evolve/footprint-gen.py - N words in levels, a
   table of their tokens, a checksum; --defs-only for the compile phase): checksums agree on s6 and
   seed 56's fastest (its JIT on) at N = 100, 1,000, 10,000, 30,000. **footprint.py ran** (433, seed 62's chain,
   12 of its front): the selection's order holds, weakening - Spearman 0.951 at N = 100, 0.783 at 10,000 and 30,000 -
   but each design's time per call against s6 moves 1.6-3.8 times across N: the fast designs about 4x s6's speed at
   100-1,000 words, 1.1-1.5x at 10,000 (s6 itself falls off a cliff at 30,000: 154 to 464 ns a call). The selection's
   small programs flatter the fast end at large footprints; a footprint workload in the selection, or this as a
   held-out check each run - **answered by seed 64's check (443): the 16 fastest keep their order at 10,000 words
   (Spearman 0.888) - no gate, no workload; the check stays in each line.** Priced before (435, results/drafts/footprint-gate-435.md) - a held-out check
   about 10 minutes a run (recommended first), a fast-end gate 1-2% of a run, a selection workload some 30% of its
   generations. **The held-out check in the chain (the owner, 435-437)**: footprint.py --fastest (the front's 16 fastest,
   at 100 and 10,000 words, 3 rounds, about 15 minutes) - from seed 64's line on, every seed line: seed 63's processing
   writes `then experiment footprint.py --fastest --sample 16 --sizes 100,10000 --rounds 3` into it. Not in seed 63 -
   its 10 hours as set (437; 436 had put it there). (Before it: next, the experiment step for the
   laptop - a sample of the front, each N full and --defs-only, repeated; time per call (run phase)
   and per word (compile phase), each against s6 - with --calls at least 40 N, as below 30,000's
   definitions (41 s on s6 here) swamp a fixed 200,000 calls.
   **The experiment is built** (Iteration 371: lab/evolve/footprint.py - the chain's `experiment
   footprint.py`; defaults --sample 12 --sizes 100,1000,10000,30000 --rounds 5, about 20 minutes on the
   laptop by this VM's scale). Proposed for the chain after seed 57's processing, the owner's hours:
   `seed 58 tag2 12h widths then experiment footprint.py then experiment compare-fronts.py ...`.
   **Scheduled** (the owner, Iteration 397): after seed 62, in its command (NEXT-RUN's comment).
   Run end to end here at Iteration 403 on seed 59's database (2 designs, N = 100 and 1,000, a round): it works.
3. **The JIT genes** (results/drafts/next-genes.md): jitimg and jitvar applied; **jithelp and jitre to be tried**
   (the owner, Iteration 397) - in the after-seed-62 batch. jitleft.py's counts say they buy little (the kernel's
   share left to the interpreter 53.7% to 53.6%, bubble's 2.0% to 1.7%; 4.5 KB more): out if the fronts do not use
   them (results/applied-after-seed62/ORDER.md has the evidence) - by results/seed63-rules.md's gene rule (431): three runs
   (seeds 63-65), a dependence test, frozen off for a run before the code goes.
4. **Fewer dispatches - the front end's lever** (Iterations 297, 301): the evolved interpreted designs
   stall on the dispatch's indirect jump, not the caches. Superinstructions were that lever on paper,
   and in tag-2 designs never in fact (the standing decisions: superinstructions). Calls and returns are 15-25% of mispredictions; the
   JIT's ackermann misses past the return predictor's depth - a candidate gene, not built
   (results/missmap-amd-ryzen-7-pro-8840hs.md). The IP-update loop form set aside
   (results/drafts/iploop-plan.md). The return candidate sized (Iteration 403): the JIT's EXIT is a stencil ending at its
   first ret (jit.c reads 0xC3); built (the owner, Iteration 404): the gene jitret, EXIT's ret made pop %rcx; jmp *%rcx
   (patch 8, results/jitret-404.md) - here ackermann -26%, bubble and loop +6-9%; seed 63's fronts decide.
4b. **The simplicity review** (results/drafts/gene-usage-53-56.md, Iteration 372): never-chosen mechanisms - msc,
   scale, tail, on no front of seeds 53-58 - out or kept; always-on genes frozen or kept: the owner's call - seed 60's
   anchoring answer is in (406: none found at 12 hours). Approved and built (the owner, 409; results/drafts/simplicity-proposal-408.md):
   bytehdr, doesfar, thinhdr, varcall, bss and lean frozen on, msc and scale at 0 - pending patch 10; tail by results/seed63-rules.md's gene rule (seeds 63-65);
   with it the overlap 423 found: rtimm=2 passes --rtfuse, so a design's built pairs and fused tests fuse at run time
   with rtfuse off (five of seed 60's front rely on it) - document it, or let rtfuse govern: the owner's call;
   jitos and nogcse watched. Not tag2 or bytehdr: free, the search chooses
   by objective (seed 58). And bfind, inert in every TOS design (Iteration 399): built there from
   the after-seed-62 batch (402, patch 7). And tail, on no front of seeds 53-58: since seed 57 every tail design was
   the slowest at 32 bits for a fault (Iteration 400) - judge it again after seed 63. Seed 59's front: msc, scale and tail 0% too
   (Iteration 403, results/drafts/gene-usage-53-59.md).
4b2. **Reachability - the audit's finding** (Iteration 439, results/audit-genes-designs-439.md): rtloopall needs all eight
   loop words in the format-10 list; in seed 62 only 92 of the 5,819 genomes that set it could express it (J, UNLOOP,
   (LEAVE) missing), its front share 1-65% run to run, rtiplus blocked behind it. Proposed: a repair - rtloopall turned
   on puts the missing loop words first in the list - **built (440, the owner): patch 4 of results/pending/** (with
   rtloop on, and escape where a tag-2 design has 2-4 slots), applied with the batch at seed 63's processing; it makes
   rtloopall express in 4,370 of seed 62's 4,462 blocked genomes. Seed 64 the first run with it. The audit's other
   checks found the pipeline sound: the screen costs about 9 front-quality designs a run; the tail kinds build at 32 bits.
4c. **A local minimum?** (the owner, Iterations 373 and 392; results/convergence-seed58.md maps five sources to their
   tests): a constraint - real (seed 58); the carry - none found (seed 60, 406); one start for every run - seeds 58-62; collapse inside
   a run - none in seed 58; the gene set's edge - only new mechanisms pass it (item 4). Gene usage against seeds 53-57
   by gene-usage.py; two consecutive carried runs differ by up to 17 points a gene. Seeds 59 and 60, two starts on the tag, 13.6 points apart on average at generation
   133 while within 6% in speed and 0.2% in size - many settings, one performance (414). Seed 59 (Iteration 403): no collapse - the tag-2 family's diversity 0.45-0.52 to
   the end - but no gain in its last third (smallest last at generation 88 of 143, speed's last 2% at 81); its front's
   genes against seeds 53-58's differ by up to 56 points (rtloopall, escape, supers, guard on; tos off).
   **The replicates, answered** (433; seed 62's chain's review-checks.py spread at generation 133): seeds 60, 61 and
   62 - one start - smallest 15,938, 15,939 and 15,929 bytes (0.06%), hypervolume within 0.7%, fastest 0.1111, 0.1108
   and 0.1164 (5.05%); gene usage 7.5-11.8 points apart a pair. One basin at the small end; at the fast end runs of one
   start stop about 5% apart by chance - Iteration 393's prediction 4's condition: the case for an escape mechanism
   (islands or immigrants, item 4e) at the fast end. The owner's call - **options priced (435,
   results/drafts/escape-mechanism-435.md): islands recommended**, an evolver option off by default, one run against
   seeds 63-64. **Built (436, the owner): patch 3 of results/pending/** - evolve.py --islands 4 from the word "islands" in
   a seed line; applied with the batch at seed 63's processing, so the first run that can use it is seed 64. Not in
   seed 63: its batch and its rules are judged without it.
4d. **Weighing across machines** (the owner, Iterations 376-377; results/drafts/cross-machine-weighing.md): three
   machine classes, equal (GOALS.md); the blind spot tested by xcheck --rejected - of seed 57's rejected designs,
   none faster on any host than the front's fastest (results/xcheck-seed58.md).
   **The best design across the classes - measured** (seed 63's chain, Iteration 441): of 10 designs on all three,
   seed 62's front's 5f512a3017 first (x86-64 0.368, x86-32 0.509, ARMv7 0.391 - mean 0.419, 25,105 bytes), then its
   83716d5eaf (0.437), bf439eb307 (0.467); ad56a8e0fd and 11e5884401 vetoed at x86. The plan (Iteration 430): bf439eb307 (seed 60, rejected by its selection - its record in results/candidates-generic.md), 11e5884401 and
   ad56a8e0fd (seed 58's front) asked for by id on dream at 32 and 64 bits and on the Tegra (REMOTES); review-checks.py
   generic - now in process-seed.sh's summary - ranks every design measured on all three classes by the geometric mean
   of its speeds, vetoing one more than 25% behind a class's best. On seed 61's chain: bf439eb307 0.455, every front
   design measured on all three vetoed (0.780 and slower). At seed 63's processing: read it, then the --also lists out
   of REMOTES (the Tegra's rebuild test's with them).
4e. **Mechanisms not yet genes** (Iteration 407: lab/evolve/GENES.md's "Not yet" and the open items). **The register
   machine - parked** (418-424, results/wip-regmachine/README.md): priced at Iterations 29 and 32 as the largest prize;
   re-priced on code as it runs, on plain CV8 a fifth to a third of most workloads' dispatches could be taken in as
   operands (`+` and `<` the most), on the tag little beyond I+ - but the forms that take them largely exist as genes
   (rtimm's immediates, the loop compiler, I+), and what keeps the small end from them is their bytes, not their reach.
   No general stage unless a later workload shows move-heavy code these miss; two of the forms made cheaper instead -
   the after-seed-63 batch (results/applied-after-seed63/ORDER.md). Its bound on the front: 7-46% a workload (410-411,
   results/drafts/price-410.md). I, the loop index, fused on the tag since patch 11 (412-413: I+ pinned to one byte;
   every run-time table entry kept). Translation to direct threading at load (gforth's hybrid, Wasm3's M3): the compact
   image expanded at start. The interpreter's returns predicted - priced (410): handler replication at most 0.4-1.6% of
   the geometric mean, no dispatch fewer - not built; the JIT's is built (jitret). Direct threading at load priced
   (440, results/drafts/price-dthread-440.md): about 3% faster at best, about +58 KB - a third of the memory objective -
   and a new engine path: not built. The search's own escape - islands or
   immigrants - after the replicates (Iteration 393's prediction 4). Priced out: indirect threading (Iteration 29);
   deferred: ?STACK (item 5).
5. **?STACK as an opcode - deferred** (Iteration 299, results/source-audit-3.md): about 1% of the
   geometric mean, for a new overlay tag in every design and DEPTH reproduced exactly - more mechanism
   than it buys, by GOALS.md's measure, unless the corpus comes to weigh more.
6. **relf, phases 2 and 3** (RELF.md): after the best generic designs - how they fit relf and its shell;
   the shell-profile patches (results/relf-patches/) parked for then, their laptop timing optional.
7. **The article** - deprioritized (the owner's standing decision): written from PROGRESS.md when the
   best designs are found.
8. **The genes still code** (lab/evolve/GENES.md, "Adding a gene") - into table rows only as each is
   next touched, each conversion checked with `python3 lab/evolve/gene-equiv.py <the commit before>`.

Done since the list before (pointers, not repeats): the runner protocol and its remote checks
(Iterations 302-315: lab/evolve/chainctl.py, lab/evolve/xcheck.py); the 32-bit checks and their
follow-ups (seeds 55-56, Iterations 334-354: the Tegra, the width alone on dream); selection at both
widths (applied at 354; seed 57 runs it); (FIND)'s branch-light walk (bfind, Iteration 316); seeds
52-56 processed.

Not an item - **dormant list genes are by design** (checked at 369): about half of the front's
format-10 words (ops10) are listed past their slots and not built, as are nearly all superinstruction
pairs; express() keeps only what is built - a design's identity, and what lab/evolve/seed-facts.py
counts - so dormant entries are a neutral reservoir a mutation can promote, not a fault in the reports.

## Lessons - how faults got in, and the checks that catch them now

- A rehearsal reaches what a test of variants does not: the tail variants were built on s6, not on the two-bit tag, and
  t2call's path, which only a tag2 design has, kept its tail call a call at 32 bits under GCC (Iteration 405). Before the
  laptop runs a batch, evaluate a run's front with its genes on, and evolve a short run, in a scratch clone.
- Two steps of one build must target one machine: build_tail preprocessed with cc and compiled with gcc -m32, so every
  tail design failed at 32 bits from Iteration 336 to 400, read as a design that does not build there; and a machine-
  code reader written for x86-64 (tail_offenders) saw nothing at i386. A generator path is checked at each machine
  class it is selected on (engines-check's 4-byte section, Iterations 399-400).
- A gene's check must build the gene's code: engines-check's bfind variants sat on s6, whose TOS engine never takes
  the bfind walk, and passed from Iteration 316 to 399 while the walk was wrong at 4-byte cells (seed 59: 34 of the
  front dead at 32 bits). And UNS64 is the cell, not 64 bits: a fixed-width value takes uint64_t (Iteration 399).
- On Ubuntu gcc-arm-linux-gnueabihf and gcc-multilib cannot both be installed: the first removes the second,
  and /usr/include/asm with it - every 32-bit build fails until gcc-multilib is back (Iteration 391, the ARM
  compiler installed at 390 for a cross build). After any apt install, build before trusting the tree.
- A shortened output must still say pass or fail in so many words, and its exit status must agree: batch-check.sh
  at first exited 0 on a failed test (Iteration 395, results/tools-audit-394.md). And two traps of this VM: git run
  as root in a tree claude owns refuses it as unsafe; `pkill -f PATTERN` kills the calling shell when PATTERN is in
  its own command line.
- **Context economy** (Iteration 394; the owner asked how a chat lasts longer): what tools print stays in the
  chat. Logs to files and one line printed (`| tail -1`, a summary file); a recurring cycle as a script -
  `tools/batch-check.sh` tests the pending batch as it will be applied (fresh clone, ORDER.md's patches, build,
  run-tests, validate, jail) in one line, three calls where it took eight; after the first reading, grep or a
  view range, not whole files; one wait loop per background job; replies short - the files hold the detail.
- Read what a configuration does before naming the experiment: `nocarry` was called "from scratch" for seeds
  58 and 59, and evolve.py puts two evolved designs in every generation 0 but fromzero's (Iteration 386: two
  thirds of seed 58's ancestry). Likewise a requirement (tag2, and bytehdr with it) belongs in every verdict
  it shaped - "converged" was said of the constrained space.
- In "Judging the runs" a positive figure is the run AHEAD of all the others: seed 58's smallest +10.51%
  is its design 10.5% smaller, not larger - Iteration 384 first read it backwards, and caught it by the
  per-run minimum (14,146 against 15,633). Check a verdict's direction against the table before writing it.
- Edit a numbered item by its own text, never by `index('\n4. ')`: this file's
  routine is numbered too, and comes first - Iterations 293-299 wrote open items over
  the routine's steps 3-5, and left the open items themselves stale (found and
  restored from Iteration 292's text at 300). Now prompts/19-address-by-name, with
  the three other faults of the same week.
- A passing gate does not prove the intended code ran (a fallback of the same
  name answered twice): profile and look for the new words; the dump guard
  stops a run whose libraries do not load whole.
- The dump lists words newest first; Forth remarks must be in comments; the
  cell system has no NIP or TUCK; the kernel never uses ?DO; a colon word
  shaped like a stub is read as a stub. In cross-compiled kernel code `[']`
  compiles a START-relative number - use a variable's address. The converter
  swaps every X8 body into X (a new X collides with an overlay's X8). New
  dump-tool words go in layout.py's DUMPTOOL.
- After a header or lookup change, count dispatches: a "correct" fix cost the
  small designs 6-8% unseen by the gate. Engine size changes hide in code:
  measure the file, not the table.
- An engine change is checked on every generator's engine (engines-check, in
  run-tests): seed 46 lost every tail design to one that was not. When a family
  is fixed, check that its designs live, not only compile (seed 47: 626 alive).
- A compiler gene is offered only where the compiler exists, and the jail must
  know it as a build tool (BUILD_TOOLS).
- Judge an old scratch tree against what was applied, not against today's master:
  later batches rewrite what it held (277: ten trees "not in master" were all
  applied). "Never failed" means "never recorded failing" - record the run.
- next-run.sh's chain runs detached (nohup, stdin /dev/null): anything that needs
  a terminal - sudo's password - happens before it detaches (282: the first
  counters.py run failed so, after a claim, never read in the code, that the
  tools ran in the foreground). Read how a thing runs before saying how it runs.
- A failure report carries the failing program's own words, not only its exit
  code: counters.py said "exited 2" and kept perf's message to itself (283).
  Try an outside program once, where someone can still fix it, before the work
  goes to the background.
- Forcing a list gene for a check puts its members first: ops10_in hands a
  design's opcode slots out in its list's order, and members appended to a full list
  get none - a check of them that builds nothing (290: the gate's first try).
- A background job still running when the turn ends is lost: start it early and
  read it in the same turn (290: a gate's log came back empty).
- `pkill -f PATTERN` kills the shell running it when PATTERN is in its command
  line - anchor the pattern, or kill by pid (282). Tests sharing one global
  setting run one at a time: run alongside, they made each other's results (282).
- A check that never failed is made to fail before it is trusted (266:
  engines-check against 248's fault). Measure the artifact, not a tool's
  estimate of it (267). A first number far below its price: lift one
  restriction at a time before concluding (267).
- Look in lab/evolve/ before writing a script (image-ab.py measures an image
  change on one engine). A script that produces a recorded figure is tracked.
  An old chat can still be asked for its files while its machine lasts (273-274
  recovered 263's factor.py and 174 more so) - but ask the whole range of
  iterations it ran, and early. Transcripts of earlier chats may sit in
  /mnt/transcripts on one machine (that chat had two) and not on the next (empty
  here): the repository is the only record that carries over.
- A "where things stand" written anywhere but here goes stale: GOALS.md held
  770 lines of them, the newest seed 28's (Iteration 275 moved them out).
- Information is lost only outside the repository: the handoff check (below)
  fails on uncommitted work, untracked scripts, scratch trees with changes, a
  stale HANDOFF.md.

## Where things are

Every document: README.md's "Documents" section. Every measurement, analysis
and per-run record: results/README.md. Every tool of the evolver:
lab/evolve/README.md's "Tools". The prompts: prompts/INDEX.md. The leftovers of
the chats of Iterations 213-265: results/drafts/chat-to-iter265/README.md.
GOALS.md before Iteration 275: results/drafts/goals-snapshots.md.

## Before a chat's turn ends - every turn that changed the repository

1. Commit everything that should survive. A script that produced a figure
   recorded in PROGRESS.md goes into the repository (lab/evolve/ or
   results/drafts/); every other file you wrote in /tmp is deleted or listed in
   `/tmp/handoff-disposable.txt` (a path, then a reason, per line).
2. Bring this file up to date: "master: Iteration N", the state, the open
   items; write the PROGRESS entry.
3. `runuser -u claude -- sh tools/make-bundle.sh /mnt/user-data/outputs` - it
   runs `tools/handoff-check.py` and refuses a bundle a new chat could not
   start from. Mid-work, `--checkpoint` makes a bundle that is not a handoff
   point (its name ends in -checkpoint).
4. Present the bundle.
