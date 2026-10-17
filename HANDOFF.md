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

- master: Iteration 364.
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
  (results/pending/ORDER.md).
- **Seed 56 processed** (Iteration 354): small (+1.3%; fastest -4.1%) - the fourth of these genes.
  **The first run checked on four machines**: the Tegra's first native run (ARMv7) - Spearman 0.944;
  dream.lan 64-bit 0.917, 32-bit 0.833, the same designs at 64 bits 0.977 - on one machine 64 against
  32 bits 0.854: the skew is the width's. On real hardware fsys 3 keeps its place at 32 bits (r 1.00) -
  the VM's 2x was its own slow 32-bit system calls; the five fastest at 64 bits lose most (r 1.7), one
  lineage (klookup, kinput, rtimm 2, swapi; no regpin). **The after-seed-56 batch applied**: selecting
  at both widths, jitimg and jitvar, the comparison at 32 bits - the gate 268 of 268.
- **This lab is RelF's base** (the owner, Iteration 356; RELF.md): vendor/relf follows relf master with
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
  pending after seed 57 (results/pending/ORDER.md).
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
7. `git mv results/pending results/applied-after-seedN`; append the session to
   `results/compare-fronts-amd-ryzen-7-pro-8840hs.md` ("## Session K -
   Iteration I: seed N and seeds ...", the verdict line, then the pack's
   compare-fronts.md); `python3 lab/evolve/progress-table.py >
   results/progress-by-run.md`; NEXT-RUN (the owner's hours, and a comment for
   the iteration); this file; a PROGRESS entry; then "Before a chat's turn ends".

## The owner's standing decisions

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

0. The protocol above, built to results/drafts/runner-protocol.md - its commands
   (start, status, monitor, stop), the start's recovery, the end's trap and one archive, root
   that chowns and watches the chain - and tried here as it says (a miniature chain;
   stop in mid-run; a kill -9 as a crash) before the laptop relies on it. Each step's
   own pack kept in runs/ for the first real use. Fix with it: perf-hold.py creates
   runs/perf-hold.log as root today.
   Done of it: lab/evolve/xcheck.py (Iteration 307) - sample, the host's run and the
   report, tried here; the hosts (dream, rage) idle, GCC only, no clang or perf. dream
   measures the laptop's own binaries (--bundle, --prebuilt; Iteration 308); rage builds
   natively first. To do:
   the runner, and its ssh side for the remote checks.
0. The 32-bit checks - their first run (seed 55): dream.lan 32-bit x86 Spearman 0.694 against the
   laptop, 64-bit 0.940 - the skew, measured. Two follow-ups: (a) the Tegra - the pending batch
   ports the sysc guard to pack4.c, pack8.c, spn.c, spn-cv8.c (build-stages.sh compiles them; it
   stopped at pack4.c); (b) the width alone - a 64-bit check on dream from the same pool as the
   32-bit one (no JIT, GCC only, the same designs), so 64 against 32 bits on one machine; seed 55's
   two samples shared 8 designs, nearly all slow and within 5%. Then: what in the evolved designs
   costs at 32 bits (register pressure on i386's 8 registers, 4-byte cells) - genes for both.
0c. Selecting at both widths - **pending, the after-seed-56 batch** (results/pending/ORDER.md,
   Iterations 336-338): evolve.py --widths 8,4 (NEXT-RUN's word: widths) - speed32, each design's
   interpreter as a 32-bit x86 engine at 4-byte cells, a fourth objective; 20 of 20 designs with
   speed32 in the scratch run; 64 bits unchanged (byte-identical, gene-equiv PASS, the gate). The
   converter's alignment fixed with it (seed 54's converter death lives). After seed 56: apply, and
   NEXT-RUN with widths - the owner's hours.
   Patch 3 (Iteration 352): the comparison at 32 bits too (--widths 8,4). And why designs lose at
   32 bits (results/drafts/skew-32.md): knockouts name tag2 and fsys 3 (engine-side, to read as bugs)
   and the compiler gene's 64-bit-only gain.
   Iteration 353: tag2's 32-bit cost confirmed (36%), in dispatch, not the cell type nor the PIC
   register; selecting at both widths costs x1.86 the evaluation time - nearly twice the hours.
   And a correction: this VM's 32-bit system calls cost 140x its 64-bit ones (12.49 against 0.09 us) -
   fsys 3's 32-bit penalty measured here is mostly the VM; tag2's (in a loop without calls) stands.
0b. The next genes (results/drafts/next-genes.md, Iterations 323, 339): lab/evolve/jitleft.py
   measured it - the JIT leaves kernel 56% and corpus 99.7% to the interpreter (fib, loop,
   ackermann translated whole): the outer interpreter - INTERPRET, PARSE-WORD, REFILL, WORD, ?STACK -
   and the corpus's run-once words. Next: a JITLOG build naming the operation that keeps each word
   out - done, Iteration 340: --why. 62.6% of what is left is never tried - the image's words have no JIT
   header; the gene jitimg designed (results/drafts/next-genes.md): the converter writes the header
   run-time words get - built (results/drafts/jitimg-wip.patch, Iteration 341): level 1 alive, little
   gained yet - PARSE-WORD tried and refused for vf (getstatic); INTERPRET excluded (aligned data).
   jitimg (0/1) and jitvar pending as patch 2 of the after-seed-56 batch (Iteration 343: forced 16 of
   16 JIT designs alive, 66 engine paths). INTERPRET now tried, refused for PLACE; PARSE-WORD, WORD for
   (PARSE) - C primitives: **helper calls next** (the owner approved; the design in the draft).
   Iteration 345: pending patch 2's latent jitvar bug fixed and re-verified (byte-identical off; 66
   paths; forced 16/16; gate 248/248) - the pending patch replaced. Helper calls (results/drafts/
   jithelp-wip.patch): PLACE, (PARSE), COUNT - INTERPRET now at (FIND), PARSE-WORD at +!. (FIND) needs
   the engine's internals: the hard step.
   Interpreter re-entry built (Iteration 346, the owner approved; results/drafts/jitre-wip.patch):
   links, crashes on its first run. Bisected (Iteration 347): helper calls and COUNT right natively;
   (PARSE)'s image header breaks the compiler's inlining (fix: no header on one-operation words);
   **Re-entry works** (Iteration 349): JIT_L_INTERP had been 0xFFFE, the translator's "call resolved"
   marker - fixed; jit_rtouch keeps (S")'s inline data from being decoded. Snippets identical to the
   JIT off; the helper words verified translated. Iteration 350: all four JIT genes alive together
   (jit_rtouch conservative; callee addresses bounded) - but kernel 54.6% left (55.9%): INTERPRET at
   (FIND), PARSE-WORD at +! - operations, which re-entry cannot help. The owner's call: on, or park.
1. Seed 52: process when its packs come; and the two measurements' packs. seed-facts.py now reports every late gene and the format-10 words on the front
   (Iteration 299) - seed 51's predictions are scored from it.
2. What the batches applied after seeds 50 and 51 do (Iteration 300): seed 51 took
   opinline on 64 of 162; 2@ on the JIT designs - five of the six fastest - but on 8 of
   the 69 without the JIT; knumber on 8 of 69 klookup designs; tailpn brought no tail
   engine back. A new opcode costs an interpreted design a slot of its full format-10
   list. Seed 52 shows > and 0=, and alignhot (which only 20 of seed 50's 187 could
   take).
3. The interpreter's mispredictions (results/missmap-amd-ryzen-7-pro-8840hs.md, Iteration
   301): (FIND) in C the largest single source on kernel and corpus, 9-13% - its chain
   walk; the fast designs all took 16 threads, the fewest. A gene for its walk made
   branch-light (a name's length and first characters compared as one word) is the next
   to try. Calls and returns 15-25% - one shared jump predicting where the program goes.
   The JIT's ackermann misses: native ret past the return predictor's depth - a
   candidate gene, not built.
4. The front end (Iterations 297, 301): the evolved interpreted designs stall there half
   their cycles on compute work - not the caches (under 0.2 misses a thousand
   instructions): the dispatch's taken indirect jump itself. The lever is fewer
   dispatches (superinstructions, opcodes, the JIT); alignhot, applied after seed 51, is
   unlikely to pay. The IP-update loop form set aside (results/drafts/iploop-plan.md).
5. ?STACK as an opcode - deferred (Iteration 299, results/source-audit-3.md): 7.4% of the
   corpus's dispatches on seed 50's fastest design without the JIT, about a dozen a check
   - INTERPRET checks after every word it executes. Twice worked on already, in Forth:
   kinput's ?STACK8 (Iteration 54) and kstack's (116), one unsigned compare on DEPTH. One
   opcode, given S0 @ by an overlay's wrapper, would save most of it - about 1% of the
   geometric mean - but: a new overlay tag for every design doubles the stage dumps each
   build makes, and it must reproduce DEPTH exactly (SP@ is PUSH(dsp + CELL_BYTES): the
   macro moves dsp first, so the value is dsp as it was; an off-by-one misses a one-cell
   underflow). Worth it if seed 51 shows the corpus still weighs.
5b. Generalization (results/generalization.md, Iteration 305): the selection measured on
   one CPU, with small programs. Two checks to build: a held-out workload whose code
   footprint grows (generated programs of N words, hot and run once, and a
   compile-heavy one) - each front design's time per dispatch against N; and the joint
   front measured on a second CPU - now planned: the remote checks on dream.lan and
   rage.lan, part of item 0 (results/drafts/runner-protocol.md).
6. The genes still code (GENES.md, "Adding a gene": the dispatch cluster, the
   compiler's switch-off, the list genes, engine flags, shared converter
   options) - into rows only as each is next touched, each conversion checked
   with `python3 lab/evolve/gene-equiv.py <the commit before>`. A new gene is
   one row.

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
