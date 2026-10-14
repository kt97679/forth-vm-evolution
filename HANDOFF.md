# HANDOFF - start here in a new chat

This file is the handoff, kept current: it says where things stand now, and
every chat updates it before it presents a bundle (`tools/handoff-check.py`
fails when it is behind the state). PROGRESS.md is the history - read its
entries after the iteration named below. Everything needed is in the
repository; nothing from an earlier chat's machine or transcript is.

## What this is

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

- master: Iteration 292.
- The after-seed-47 batch is applied (Iteration 269, six patches -
  `results/applied-after-seed47/ORDER.md`). `results/pending` holds the
  after-seed-50 batch: 2@ and 2! as opcodes (Iteration 290-291), and the gene
  opinline (Iteration 292).
- **Seed 48 has no record of its own, by the owner's choice** (Iteration 289): a run
  went from Oct 13 21:01 UTC to about 03:00, its database archived as
  runs/archived-20261014-052835 - in seed 49's comparison, which credits it with the
  Q-best of all runs (4599c1f454); its front's genomes are in seed 49's database
  as carried records (gate.py --db). Its packs were never sent, the owner unsure
  which seed it ran; nothing re-runs it. Its predictions stay unscored.
- Seed 49 processed (Iteration 288): not small, hypervolume +4.0%.
- **Seed 50 is running** (started 13:49 UTC Oct 14; the evolution stops 23:55 UTC): `seed 50 tag2 12h then experiment
  compare-fronts.py --rounds 6 --frontier --cpus 2,8` - 12 hours, the owner's; the
  same genes a third time. Its predictions: the end of `results/predictions.md`.
- Seed 47 was small by all five measures (Iteration 269). The Q-best design of
  all runs (session 42): seed 43's 19510c7689.

## Processing a returned seed (as done for seed 47, Iteration 269)

About 20 minutes of machine time for build, tests and gates.

1. Unpack both packs into /tmp; `tests.log` PASS, `validate.log` 7 IDENTICAL,
   `jail.log` PASS, `next-run.log` times; `git apply -R --check` the pack's
   `results-measured-here.patch` (the laptop's stash, already on master).
2. The comparison's "Judging the runs": fastest, smallest, memory (+-8 KB),
   hypervolume, best Q - small only if all five are. The Q-best of all runs.
3. `python3 lab/evolve/seed-facts.py <pack>/db.jsonl <pack>/report.md`.
4. Score the predictions, write the next (`results/predictions.md`).
5. `results/evolve-amd-ryzen-7-pro-8840hs-seedN.md`: the verdict and facts, a
   `---`, then report.md - the gate and ans-check read genomes from it.
6. Apply the pending batch per its ORDER.md (reseed with `tools/reseed.sh` only
   when a patch changes `forth/kernel.4`), then ONE background chain: build
   (`env LAYOUTS=1 bash tools/build-stages.sh`), `bash tools/run-tests.sh`
   (PASS; 31 generator paths), `python3 lab/evolve/evolve.py --validate` (7 of 7
   IDENTICAL), `python3 lab/evolve/test-jail.py` (PASS - the laptop's fourth
   check; the VM runs all four before a bundle goes to the laptop, Iteration
   129), `python3 lab/evolve/gate.py <results file> <compare
   pack>/compare-fronts.md` (152 of 152 for seed 47), `python3
   lab/evolve/ans-check.py --ids <every fourth of the front by size, and its
   extremes>` (33 designs, 2.5 minutes; 0 differ, its negative control caught).
7. `git mv results/pending results/applied-after-seedN`; append the session to
   `results/compare-fronts-amd-ryzen-7-pro-8840hs.md` ("## Session K -
   Iteration I: seed N and seeds ...", the verdict line, then the pack's
   compare-fronts.md); `python3 lab/evolve/progress-table.py >
   results/progress-by-run.md`; NEXT-RUN (the owner's hours, and a comment for
   the iteration); this file; a PROGRESS entry; then "Before a chat's turn ends".

## The owner's standing decisions

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
  reproduce the tested files; batches wait in `results/pending/` with ORDER.md.
- Run lengths are the owner's - ask for each run's hours (seed 48: 6).

## Open items (roughly by value)

1. Seed 50: process when its packs come. No batch is pending.
2. Pending, to apply after seed 50 (results/pending/ORDER.md): 2@ and 2! as
   opcodes, and the gene opinline - their call gone from code compiled at run time;
   bubble -41.6% of its dispatches on c9369657e4 with both. Next on that line:
   NUMBER?'s digit table as a gene.
3. A tail engine with preserve_none + musttail (clang 19+), once seed 48 shows
   what clang engines do on the laptop.
4. The interpreter's mispredictions (results/counters-amd-ryzen-7-pro-8840hs.md): on
   kernel and corpus the evolved designs lose an estimated 9-24% of their cycles to
   branch misses, s6 1-3%. Next: which handlers - perf record on branch-misses:u
   against the unstripped engine (engine.full), a laptop measurement like counters.py
   - then make them branch-light. Also there: the JIT mispredicts 1.5% of ackermann's
   branches (returns, probably - jittail).
5. The IP-update loop form (deferred in Iteration 260): the counters leave it open -
   dispatch predicted on compute work, yet the evolved interpreted designs run at a
   lower IPC than s6. A gene to build when its turn comes.
6. The genes still code (GENES.md, "Adding a gene": the dispatch cluster, the
   compiler's switch-off, the list genes, engine flags, shared converter
   options) - into rows only as each is next touched, each conversion checked
   with `python3 lab/evolve/gene-equiv.py <the commit before>`. A new gene is
   one row.
## Lessons - how faults got in, and the checks that catch them now

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
