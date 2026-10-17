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

- master: Iteration 376.
- The after-seed-47 batch is applied (Iteration 269, six patches -
  `results/applied-after-seed47/ORDER.md`). The after-seed-50 batch is applied too (Iteration 296,
  results/applied-after-seed50/ORDER.md), and the after-seed-51 batch (Iteration
  300); `results/pending` holds the after-seed-52 batch (Iteration 312): the JIT fix.
- **Seed 48 has no record of its own, by the owner's choice** (Iteration 289): a run
  went from Oct 13 21:01 UTC to about 03:00, its database archived as
  runs/archived-20261014-052835 - in seed 49's comparison, which credits it with the
  Q-best of all runs (4599c1f454); its front's genomes are in seed 49's database
  as carried records (gate.py --db). Its packs were never sent, the owner unsure
  which seed it ran; nothing re-runs it. Its predictions stay unscored.
- **Seeds 53-54 processed** (Iteration 333): 53 small (+0.3%, 80 minutes of evolution), 54 small
  (+1.1%, fastest +3.6%, 6 h 47 min) - two small in a row: the stopping rule's end of these genes.
  bfind on 67 of seed 54's 195 (17 in seed 53) - kept by the laptop's selection; no corpus deaths;
  heldout 0.953; dream.lan Spearman 0.941 (seed 53: 0.959). Predictions 5 of 5. One converter
  death, a new kind (open item 0c). The after-seed-54 batch applied: the 32-bit checks.
- **Seed 55 processed** (Iteration 334): small (+0.4%) - the third small run of these genes: the
  stopping rule's end. bfind on 80 of 168; heldout 0.959. **The first checks at both widths**:
  dream.lan 64-bit Spearman 0.940; **32-bit x86 at 4-byte cells 0.694** - the laptop's six fastest
  interpreted designs 8th-13th there, their lead over s6 about halved (results/xcheck-dream-seed55.md).
  The Tegra failed again - four hand-made engines kept x86's sysc guard: the after-seed-55 batch
  (results/applied-after-seed57/ORDER.md).
- **Seed 56 processed** (Iteration 354): small (+1.3%; fastest -4.1%) - the fourth of these genes.
  **The first run checked on four machines**: the Tegra's first native run (ARMv7) - Spearman 0.944;
  dream.lan 64-bit 0.917, 32-bit 0.833, the same designs at 64 bits 0.977 - on one machine 64 against
  32 bits 0.854: the skew is the width's. On real hardware fsys 3 keeps its place at 32 bits (r 1.00) -
  the VM's 2x was its own slow 32-bit system calls; the five fastest at 64 bits lose most (r 1.7), one
  lineage (klookup, kinput, rtimm 2, swapi; no regpin). **The after-seed-56 batch applied**: selecting
  at both widths, jitimg and jitvar, the comparison at 32 bits - the gate 268 of 268.
- **This lab is RelF's base - as a generic Forth first** (the owner, Iterations 356 and 365; RELF.md;
  the relf patches of 360-362 parked as phase-3 reference, their laptop timing optional): vendor/relf follows relf master with
  its sources (vendor/relf/tree); relf's ledger asks this lab about XF@/XV@, DEFER, (+LOOP), PICK and
  fused pairs for CV8, measured on relf's shell workloads (bench-vm.py). tools/relf-ab.sh, the A/B harness,
  done (Iteration 357): relf's make test as a regression gate, then bench-vm.py; this VM's noise floor
  +-10 % - the candidates' small effects are the laptop's to measure. tools/relf-pairs.py (Iteration
  358): VAR@ 15.2 %, its pairs lead; relf's 64 one-byte opcodes (A15) make each candidate a trade. The
  budget (359): VAR@ VAR@, VAR@ +, 0= ?BRANCH net ~9.4 % of dispatches for the coldest three slots.
  **The first patch for relf** (360, results/relf-patches/zeq-qbranch.patch): 0= ?BRANCH fused - relf's
  whole make test passes, 2.10 % fewer dispatches; its time for the laptop: tools/relf-ab.sh there.
  The second (361, var-fetch-plus.patch): `var @ +` fused, the inliner taught it; both pass, 4.74 % fewer
  dispatches; this VM leaning faster (fn 0.933). The third (362, two-var-fetch.patch): `a @ b @` fused
  (2VAR@; CALL, keeps the last VAR@); all three pass, 6.41 % fewer dispatches; this VM realistic 0.944,
  arith 0.947 (both significant). All three for the laptop to time (results/relf-patches/README.md).
  Iteration 363: no more fusions until the laptop times these (the rest ~1 % each, each a slot of A15's
  64); this lab's genes classed for relf (results/drafts/relf-gene-classes.md); 32-bit engines not PIE,
  pending after seed 57 (results/applied-after-seed57/ORDER.md).
  Iteration 367: the supers gene's pool misnamed for every tag-2 design since Iteration 66, and the
  gene inert in ~97% of the fronts (its slots taken by ops10): the fix pending after seed 57
  (results/drafts/supers-tag2.md; results/applied-after-seed57/ORDER.md, patch 2). Decided at 368: no new slot
  mechanism; after seed 58, if superinstructions still buy nothing, the gene comes out of tag-2 designs.
  Iteration 364: the cheap class measured on relf's shell - clang, -Os, pinned registers: none faster
  (results/relf-patches/README.md); relf-ab.sh takes RELF_AB_MAKE_B and measures the shells it built.
- **Seed 57 next** (the owner, Iteration 355: one 12-hour run, not two of 6 - each run's fixed part
  with two widths about 3 h 40 min): the first run selecting at both widths, with jitimg and jitvar;
  the comparison at both widths. The reserve knows --widths now (164 min; the evolution ~8 h 20 min).
- Seeds 49-52 processed: 49 not small (+4.0%), 50 small (+0.4%), 51 small (+1.7%), 52
  small (Iteration 310: +0.5%; 2@ on 77 of the front, > on 3, alignhot on none; heldout
  0.937). Seed 52's database: two designs dead on the corpus - a JIT fault (open item 0a).
- **The after-seed-51 batch is applied** (Iteration 300 - results/applied-after-seed51/
  ORDER.md): alignhot; > and 0= as opcodes. New genes: the stopping rule counts afresh.
- **Seed 52 is the laptop's next run** (Iteration 300): `seed 52 tag2 6h then
  experiment compare-fronts.py --rounds 6 --frontier --cpus 2,8` - 6 hours, the
  owner's (Iteration 301). Before it, between runs: missmap.py, and counters.py with
  Zen 4's cache events (item 5), each its own command. Its predictions: the end of
  `results/predictions.md`.
- Seed 47 was small by all five measures (Iteration 269). The Q-best design of
  all runs (session 42): seed 43's 19510c7689.

## Processing a returned seed (as done for seed 47, Iteration 269)

About 20 minutes of machine time for build, tests and gates.

1. Unpack both packs into /tmp; `tests.log` PASS, `validate.log` 7 IDENTICAL,
   `jail.log` PASS, `next-run.log` times; `git apply -R --check` the pack's
   `results-measured-here.patch` (the laptop's stash, already on master).
2. The comparison's "Judging the runs": fastest, smallest, memory (+-8 KB),
   hypervolume, best Q - small only if all five are. The Q-best of all runs.
3. `python3 lab/evolve/seed-facts.py <pack>/db.jsonl <pack>/report.md` - every late gene
   on the front, and the format-10 words, since Iteration 299.
   Then `python3 lab/evolve/heldout.py results/evolve-...-seedN.md` - the held-out
   check (Iteration 305): Spearman about 0.94 on seeds 49-51; say if it falls.
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
7. `git mv results/pending results/applied-after-seedN`, and the documents citing the moved files
   follow them (Iteration 372: 62 citations had been left at results/pending/):
   `git grep -lz 'results/pending/' -- '*.md' | xargs -0 sed -i 's|results/pending/\([A-Za-z0-9._-]*-after-seedN\.patch\)|results/applied-after-seedN/\1|g; s|results/pending/ORDER\.md|results/applied-after-seedN/ORDER.md|g'`
   (N the seed: the current pending/ is the next batch's and keeps its name); append the session to
   `results/compare-fronts-amd-ryzen-7-pro-8840hs.md` ("## Session K -
   Iteration I: seed N and seeds ...", the verdict line, then the pack's
   compare-fronts.md); `python3 lab/evolve/progress-table.py >
   results/progress-by-run.md`; NEXT-RUN (the owner's hours, and a comment for
   the iteration); this file; a PROGRESS entry; then "Before a chat's turn ends".

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
  reproduce the tested files; batches wait in `results/pending/` with ORDER.md.
- Run lengths are the owner's - ask for each run's hours (seed 48: 6).

## Open items (roughly by value)

Rewritten at Iteration 369 to the state now (the list before it: git, the commit before Iteration 369);
under GOALS.md's aim - simplicity and minimalism - and the owner's order (RELF.md): a generic Forth first.

0. **Seed 57** - the first run selected at both widths (--widths 8,4): process when its archive comes,
   with its cross-machine checks. Its batch is applied already (Iteration 374: results/applied-after-seed57/
   - 32-bit engines not PIE, superinstruction pairs named right), so **seed 58 starts when seed 57's chain
   ends**: NEXT-RUN's `seed 58 12h widths nocarry then experiment compare-fronts.py ...` - the test of
   item 4c. This bundle into ~/Downloads only after seed 57's chain has finished (each step pulls the newest).
   Seed 57's verdict: its comparison runs on its own commit, before the verdict at both widths (Iteration
   375) - apply it by hand from its "At 32 bits" table: small only if the five are and its fastest at 32
   bits moved under 5%. From seed 58 the comparison prints it.
1. **Superinstructions after seed 58** (results/drafts/supers-tag2.md; decided at 368): with the pool
   named right, do front designs build real pairs, and do they buy anything? If not, the gene comes out
   of tag-2 designs - a mechanism that buys nothing comes out (GOALS.md).
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
3. **The JIT genes** (results/drafts/next-genes.md): jitimg and jitvar applied; helper calls and
   re-entry parked (results/drafts/jithelp-wip.patch, jitre-wip.patch) - the kernel still 54.6% left to
   the interpreter, INTERPRET stopping at (FIND) and PARSE-WORD at +!, operations re-entry cannot help.
   The owner's call: on, or park for good.
4. **Fewer dispatches - the front end's lever** (Iterations 297, 301): the evolved interpreted designs
   stall on the dispatch's indirect jump, not the caches. Superinstructions were that lever on paper,
   and in tag-2 designs never in fact (item 1). Calls and returns are 15-25% of mispredictions; the
   JIT's ackermann misses past the return predictor's depth - a candidate gene, not built
   (results/missmap-amd-ryzen-7-pro-8840hs.md). The IP-update loop form set aside
   (results/drafts/iploop-plan.md).
4b. **The simplicity review, after seed 57** (results/drafts/gene-usage-53-56.md, Iteration 372): over
   seeds 53-56's 722 front designs, msc, scale and tail never on; eight genes under 10% of every front;
   ten on in every design by choice - tag2 and bytehdr too, but imposed (--require tag2, every run since
   Iteration 71), not chosen. Seed 57's two widths first, and the anchoring and constraint tests
   (item 4c) before any gene is frozen - freezing would make an anchoring permanent. Then each
   never-chosen mechanism out or kept, each always-on gene frozen or kept: the owner's call.
4c. **Is the search anchored?** (the owner's question, Iteration 373). Two tests for the owner's
   hours, after seed 57: the anchoring test again with today's genes - `seed 58 tag2 12h widths
   nocarry` (or fromzero), its front against the carried ones by compare-fronts.py; seed 36 (Iteration
   123, 2 h 40 min) found no anchoring with the genes of then. And the constraint test - a run without
   `tag2`, so the search may choose the encoding; tag2 costs 36% at 32 bits (results/drafts/skew-32.md).
   **Seed 58 is both at once** (the owner, Iteration 374): from scratch and without the requirement, at
   both widths. Back in the carried region with tag2 chosen: neither concern holds. Elsewhere: a
   follow-up run separates them (nocarry with tag2, or carried without).
   Reading it in genes: `python3 lab/evolve/gene-usage.py <seed 58's db> --vs results/evolve-*-seed5[3-7].md`
   - two consecutive carried runs (seeds 55, 56) differ by up to 17 points a gene: the scale to read it by.
4d. **Weighing results across machines** (the owner's question, Iteration 376;
   results/drafts/cross-machine-weighing.md - proposed): selection on the laptop, other machines as the
   generalization test; a disagreement diagnosed (noise, width, gene) before it is weighed; the final
   generic choice by the geometric mean over machine classes with a veto; and the blind spot tested -
   xcheck samples only the laptop's front, so a design good on the Tegra and rejected by the laptop is
   never seen: a sample of rejected designs measured elsewhere. Classes, weights, margin: the owner's.
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
