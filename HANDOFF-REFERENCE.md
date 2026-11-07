# HANDOFF-REFERENCE - background to HANDOFF.md, read on demand (Iteration 542)

HANDOFF.md is the state card a new chat reads whole; this is what it points to: the owner's standing decisions in
full, the processing steps in detail, and the lessons - read the lessons before changing the evolver or a measurement.
The history - the state through Iteration 562, the open items' lists of 505 and 369 - is HANDOFF-HISTORY.md (568). Moved here verbatim
at Iteration 542 (the owner: fewer tokens at every chat's start).

## The owner's standing decisions - in full

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
- Role picks between designs (611, 621): no small gain in one criterion for a
  large loss in the others - 62abdb2c64 (0.98% smaller, 12.5% and 24.0% slower
  on x86) and 4dd4e3e7e2 (1.31% smaller, 27.9% slower at x86-32: "performance drop is too significant and size gain is too small")
  kept out of the smallest role. "Size savings are exact - take them" (above)
  is about changes to the system, not a choice between designs.
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

## Processing a returned seed - the steps in detail (HANDOFF.md's routine runs them, Iteration 560)

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

## Lessons - how faults got in, and the checks that catch them now

- Branches of one chat share its sandbox (622): a second branch's edits landed in this tree mid-turn and `git commit -a`
  swept three of them into eca15d5 (reverted at 997d945). Stage named paths; read `git status` before a commit; a file
  changed that this session did not write is another session's.
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
- A test that reads the results files changes with every seed: engines-check's donor took each list gene's value from the
  newest recorded design, and seed 80's opcall ['PLACE'] (offered only with PLACE a format-10 word) made the op;CALL
  variant NOT EXPRESSED - run-tests failed on master once the drafted results file was in the tree, and the laptop's
  next chain would have stopped at its tests (Iteration 566: the donor now takes the newest value the variant
  expresses). process-checks on master, before the bundle, is what catches it.
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
