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

- master: Iteration 398.
- **The runs**: seed 59 processed (Iteration 398); next seed 60 (NEXT-RUN's line, 12 h, `noevolved` - the clean
  anchoring test), then seeds 61 and 62 (6 h each, seed 60's start - the replicates; their commands in NEXT-RUN's
  comment, seed 62's ending `then experiment footprint.py` - item 2, the owner at 397). Predictions for all: the end of
  results/predictions.md.
- **The code**: the after-seed-59 batch applied (Iteration 389, results/applied-after-seed59/ORDER.md: opcall only
  where the tag is built; a failed tool's first error; `noevolved`; compare-fronts' sign labelled, its 32-bit fastest
  kept, its speed from both CPUs). Pending: the after-seed-62 batch - the fast gate, and the genes jithelp and
  jitre (the owner, 397: try them) - apply it only at seed 62's processing, so seeds 60-62 run one evolver.
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
   review-checks.py progress and the remote checks' agreement.
2. Judge it. The verdict by GOALS.md's "Judging a run", read from both CPUs (the owner, 389) - for a session printed
   by older code (seed 59's), the summary's "both CPUs" line; its per-CPU lines show how far noise moves it; a
   positive figure is the run ahead. heldout: the top-end lines and the regret beside the whole front's Spearman
   (about 0.94 on seeds 49-57). progress: say if diversity falls or the gains stop early. Replicates (seeds 61-62):
   `python3 lab/evolve/review-checks.py spread <db> <db> <db>`, one generation for all.
3. Score the predictions, write the next (`results/predictions.md`).
4. `results/evolve-amd-ryzen-7-pro-8840hs-seedN.md`: the verdict and facts, a `---`, then report.md - the gate and
   ans-check read genomes from it; results/xcheck-seedN.md from the remote reports.
5. A batch due now (its ORDER.md says when): `tools/batch-check.sh` first (one line), then apply it (reseed with
   `tools/reseed.sh` only when a patch changes `forth/kernel.4`). Then ONE background chain on master, logs to
   files: build (`env LAYOUTS=1 bash tools/build-stages.sh`), `bash tools/run-tests.sh` (PASS), `python3
   lab/evolve/evolve.py --validate` (7 of 7 IDENTICAL), `python3 lab/evolve/test-jail.py` (PASS), `python3
   lab/evolve/gate.py <results file> <compare pack>/compare-fronts.md` (all alive), `python3 lab/evolve/ans-check.py
   --ids <every fourth of the front by size, and its extremes>` (0 differ, its negative control caught) - about 20
   minutes.
6. The records. A batch applied: `git mv results/pending results/applied-after-seedN` and its citations follow
   (Iteration 372: 62 had been left behind):
   `git grep -lz 'results/pending/' -- '*.md' | xargs -0 sed -i 's|results/pending/\([A-Za-z0-9._-]*-after-seedN\.patch\)|results/applied-after-seedN/\1|g; s|results/pending/ORDER\.md|results/applied-after-seedN/ORDER.md|g'`
   (N the seed). The session appended to `results/compare-fronts-amd-ryzen-7-pro-8840hs.md` ("## Session K -
   Iteration I: seed N and seeds ...", the verdict line, then the pack's compare-fronts.md); `python3
   lab/evolve/progress-table.py > results/progress-by-run.md`; NEXT-RUN; this file; a PROGRESS entry; then "Before a
   chat's turn ends".

## The owner's standing decisions

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

## Open items (roughly by value)

Rewritten at Iteration 369 to the state now (the list before it: git, the commit before Iteration 369);
under GOALS.md's aim - simplicity and minimalism - and the owner's order (RELF.md): a generic Forth first.

0. **Seeds 60-62** (the state, above), each by the routine. Seed 60 answers the anchoring question (read by
   results/review-methodology-386.md, 3c: a gain anywhere is evidence of anchoring, none is not); seeds 61-62 how far
   runs of one start spread. Then the after-seed-62 batch: seed 63 its first run - `review-checks.py curse` on its report
   shows whether the fast end's optimism falls from seed 58's 1.112, and jithelp's and jitre's share of its front
   whether they stay (the owner: out again if useless).
0f. **A fifth of seed 59's front dies on the corpus at 32 bits** (Iteration 398): 34 of 171, why32 "died: corpus",
   all jit=1, scale=0, tos=0 - 2,057 such in its database, and 326 that did not compile at 32 bits; their 64-bit
   engines sound. Find the fault (a tag-2 design without tos, as a 32-bit engine: which corpus case fails, and why).
   And a question for the owner: a design wrong on one machine class - dead, or (as now, Iteration 336) only the
   slowest there, kept on the front by its 64-bit objectives?
0g. **The 32-bit hosts compared against the laptop's 64-bit speeds** (xcheck.py, its Spearman over 'speed'): for a run
   selected at both widths the laptop's 32-bit speed is the one to compare (seed 59's checks of seed 58's front: 0.651
   and 0.709, a two-encoding front ranking differently at 32 bits). A diagnostic, no run waits for it.
0d. **The Tegra's link failures** (seed 57's 5405c5b1d9 and df0c11fd98, and a rejected design): not regpin (inert on
   ARM), not lto (it built there three times); seed 60's chain checks seed 59's front with the new why() - a
   recurrence will name its cause. Not reproducible here: a cross build needs Iteration 330's qemu harness, untracked.
2. **Generalization** (results/generalization.md, Iteration 305): selection is measured on small
   programs. The second CPU is done (the remote checks: dream.lan at both widths, the Tegra); still to
   build: a held-out workload whose code footprint grows - generated programs of N words, hot and run
   once, and a compile-heavy one - each front design's time per dispatch against N.
   **The generator is built** (Iteration 370: lab/evolve/footprint-gen.py - N words in levels, a
   table of their tokens, a checksum; --defs-only for the compile phase): checksums agree on s6 and
   seed 56's fastest (its JIT on) at N = 100, 1,000, 10,000, 30,000. Next: the experiment step for the
   laptop - a sample of the front, each N full and --defs-only, repeated; time per call (run phase)
   and per word (compile phase), each against s6 - with --calls at least 40 N, as below 30,000's
   definitions (41 s on s6 here) swamp a fixed 200,000 calls.
   **The experiment is built** (Iteration 371: lab/evolve/footprint.py - the chain's `experiment
   footprint.py`; defaults --sample 12 --sizes 100,1000,10000,30000 --rounds 5, about 20 minutes on the
   laptop by this VM's scale). Proposed for the chain after seed 57's processing, the owner's hours:
   `seed 58 tag2 12h widths then experiment footprint.py then experiment compare-fronts.py ...`.
   **Scheduled** (the owner, Iteration 397): after seed 62, in its command (NEXT-RUN's comment).
3. **The JIT genes** (results/drafts/next-genes.md): jitimg and jitvar applied; **jithelp and jitre to be tried**
   (the owner, Iteration 397) - in the after-seed-62 batch. jitleft.py's counts say they buy little (the kernel's
   share left to the interpreter 53.7% to 53.6%, bubble's 2.0% to 1.7%; 4.5 KB more): out if the fronts do not use
   them (results/pending/ORDER.md has the evidence).
4. **Fewer dispatches - the front end's lever** (Iterations 297, 301): the evolved interpreted designs
   stall on the dispatch's indirect jump, not the caches. Superinstructions were that lever on paper,
   and in tag-2 designs never in fact (the standing decisions: superinstructions). Calls and returns are 15-25% of mispredictions; the
   JIT's ackermann misses past the return predictor's depth - a candidate gene, not built
   (results/missmap-amd-ryzen-7-pro-8840hs.md). The IP-update loop form set aside
   (results/drafts/iploop-plan.md).
4b. **The simplicity review** (results/drafts/gene-usage-53-56.md, Iteration 372): never-chosen mechanisms - msc,
   scale, tail, on no front of seeds 53-58 - out or kept; always-on genes frozen or kept: the owner's call, after seed
   60's anchoring answer (freezing would make an anchoring permanent). Not tag2 or bytehdr: free, the search chooses
   by objective (seed 58).
4c. **A local minimum?** (the owner, Iterations 373 and 392; results/convergence-seed58.md maps five sources to their
   tests): a constraint - real (seed 58); the carry - seed 60; one start for every run - seeds 58-62; collapse inside
   a run - none in seed 58; the gene set's edge - only new mechanisms pass it (item 4). Gene usage against seeds 53-57
   by gene-usage.py; two consecutive carried runs differ by up to 17 points a gene.
4d. **Weighing across machines** (the owner, Iterations 376-377; results/drafts/cross-machine-weighing.md): three
   machine classes, equal (GOALS.md); the blind spot tested by xcheck --rejected - of seed 57's rejected designs,
   none faster on any host than the front's fastest (results/xcheck-seed58.md).
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
