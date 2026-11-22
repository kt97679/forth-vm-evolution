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
sends back one chain archive per run (`forth-vm-evolution-chain-<commit>-fury-<time>_tar.gz`, or `.tar.gz` - 699). Commits are authored
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

- master: Iteration 736.
- **Generic application code (the owner, 674: step 1 after relf's report; relf's shell stays out of the
  objectives)** - results/generic-apps-674.md. Seven programs (the selection's four apps, wordfreq, minif, brainless)
  on the ten designs, s6, relf's CV8 (relf64, relfasm64, relf32 at vendor/relf e6e7d46) and gforth-fast:
  lab/evolve/genapps.py, genapps-report.py, genapps-dispatch.py, genapps-constructs.py. The gap: application code
  +7-10 % on the portable designs, +18-28 % on the JIT designs (a 5-byte JIT header per definition, 4-byte calls
  past 16 KB); 1.3-1.9 times CV8's dispatches (calls, DOVAR, constants - what relf's run-time compiler folds); the
  JIT leaves 86-90 % of brainless to the interpreter (DODOES has no stencil). The size score does not see
  application code (Spearman -0.21). **Step 2 - the search reopened (the owner, 677)**:
  results/drafts/search-reopen-plan-677.md. The size: engine + kernel image + the code the selection's four apps lay
  (one total, three objectives); wordfreq, minif, brainless held out (then relf's shell and rill3, step 3). The
  order: 0 the measure in evolve.py, checked against genapps.py; 1 the pure savings (unaligned strings, VALUE's kind
  cell); 2 relf's mechanisms priced on the four (rtlit, rejected at 59, among them); 3 the batch; 4 the rehearsal;
  5 the laptop. **Step 0 done (678)**: `rec['total'] = bin + size + app` (rec['app'], at 4-byte cells app32, tracked) by
  lab/evolve/appsize.py, genapps.py's count; lab/evolve/appsize-check.py PASS - the same binaries equal at both widths,
  the translator's ten 674's table, planted changes, a database of the old size refused a resume; run-tests runs
  `--quick` (results/app-size-measure-678.md); compare-fronts, stopping.py and final-pick refuse to pool the two sizes
  (679; the first new run's processing opens a series: NEXT_METHOD). **Step 1 (680)**: VALUE without its kind cell
  taken (coreext.4; brainless -696 B, the four 0 - no VALUE in them, no image moves); the unaligned strings priced
  (lab/evolve/string-price.py: the four -103 to -203 B at 8-byte cells, the held-out three about -300) - results/pure-savings-680.md.
  **The strings built (681)**: CV8's inline strings unpadded - cv8.4/cv8t.4's (S")8 (.")8 (ABORT")8 STRING,8, sod16.py's
  op_bytes, cross-cv8.4, jit.c, the spn decoders; the cell and cpt16 families, kernel.4 and the frozen stages
  untouched; every design and s6 smaller, total -152 to -266 B at 8-byte cells, -51 to -93 at 4
  (lab/evolve/design-sizes.py; results/unaligned-strings-681.md). designs/ unchanged (the shipped roles).
  681's self-hosting failures resolved (683): not the lab - selfhost-check ran designs/'s shipped engine source
  (676's jit.c, rounding a string's end) and genes (676's tag-2 map; ALIGNED's rank moved) against today's cross
  compiler. **tools/selfhost-lab.sh NAME ...** checks the lab's state: each design exported from the lab, its genes
  from the export, designs/ untouched - all ten PASS at 8-byte cells (three checked at 4).
  **Step 2 done (684)**: results/mech-prices-684.md (lab/evolve/mech-census.py, mech-price.py, mech-dispatch.py). On
  the four: a data word's @/! as one op 188-359 B and 3.5-24.9 % of dispatches (the knee) - the most; constants as
  literals where not longer 34 B, 0-2.5 %; small-word inlining 0.1-9.4 % for bytes; the JIT header 745 B. Invisible to
  the four: address literals (brainless 1,220 B), the DODOES stencil, `n -`/`=`; DOES> @ pays nowhere (GOALS.md's
  register). 680's VALUE: 3.9 % of brainless's dispatches.
  **relf's answers (685)**: results/relf-reply-685.md (the reply: results/drafts/relf-reply-953.md). relf's code has
  no TO/VALUE/['] (mechanism 8: drop), but DOES> hooks and buffers; VAR@ saves dispatches, not bytes (3.2 B); its
  constant test, inlining rule (3 instructions, 6 bytes) and the peepholes 684 missed. Its shellmix.fth is in
  lab/evolve/apps (held out): the JIT designs 1.11-1.49 of relf64's time on it; the knee 22.3 % of dispatches from
  VAR@/VAR!, 3.0 % from DOES> @. relf will measure the new roles - tell it when they exist and how to fetch them.
  **The owner decided (686)**: shellmix the fifth selection program - the apps workload runs `150 SHELLMIX` after
  the four, the size counts its code, appsize.size_key() keeps 0-, 4- and 5-program measures apart (evolve.py
  resumes only five); mechanism 8 deferred, not dropped - no word goes, the lab's 9-byte literal is the general form
  (GOALS.md's register). results/shellmix-686.md.
  **Step 3 begun (687): the gene rtvar** - forth/cv8-fuse-var.4 (a data word's @ and ! as vf/vs at run time, never
  across a branch target), layout.py's VAR-OPS, the gene and its -var dumps; the byte header only (tag 2 next).
  lab/evolve/rtvar-check.py on the knee: alive both ways, the fusion fires (T1 = vf slot EXIT), the values the same;
  the five apps' code 8,365 -> 8,278 B. **688: it pays, with varslot** - each program alone 0.733 (scan) to 0.980
  (gc16), shellmix 0.750; the apps workload 0.902 with varslot, 1.038 without (16-bit slots reach 64 KB; scan starts
  at 388 KB in it) - so rtvar needs varslot. results/rtvar-688.md. 689: the tag too (one overlay, VAR-OPS in its
  one-byte codes, vf/vs pinned) - but on fastest-x86-64 the JIT refused run-time words holding vf (the apps workload
  1.999, interpreted). **690: found and fixed** - engine/jit.c took jitvar's slot kinds 8 and 9 for branches and
  refused every word holding vf or vs, the kernel's HERE too (JIT_BROPND); since, rtvar's words translate, the JIT
  design 1.022 (the JIT already compiles call and @ natively) - rtvar under the JIT needs jitvar.
  **691: the gene rtconst** (forth/cv8-fuse-const.4: a constant compiled as its value, relf's rule and test): the apps
  workload 0.975 on the knee, **0.770 on fastest-x86-64** (its constants no longer called through the interpreter);
  lab/evolve/rtconst-check.py PASS on both. results/rtconst-691.md.
  **692: the JIT designs on shellmix** - nearly all its words refused (JITLOG): DOES> children without jitdoes, and
  the parsing words PARSE WORD FIND >NUMBER (no stencils) cascading up through >NUM; jitdoes about even (0.950,
  1.046); cold-calling the four slower (1.15, 1.11: GOALS.md's register). Native parsing operations would help - a
  JIT project of its own. results/jit-shellmix-692.md.
  **693: step 4's rehearsal for rtvar and rtconst** (a scratch clone): the front 10 of 10 alive with them; the search's
  speed 0.999 at the size end to 0.960 (portable-fastest), at about 350 bytes (overlay code, and rtconst's wide
  literals); a short run clean but for s1-sod16, which shellmix takes past sod16's 128 KB DOES> reach (a founder, not
  a candidate). results/rehearsal-693.md. The owner (694): **more genes before the run**.
  **694: the gene rtinline** (forth/cv8-fuse-inline.4: a body of at most 3 instructions in 6 bytes copied for its
  call, layout.py's INL-OPS a whitelist of position-blind operations): the programs alone 5-15 % faster on four roles
  (gc16 0.825 on fastest-x86-64), the apps workload about even; lab/evolve/rtinline-check.py PASS on four. **The dumps
  are made when first asked for** (evolve.py's dump_file, build/dumps-HASH): setup 63 s -> 1.6 s, the run-time genes no
  longer doubling it; boot_files() the one list (export-genes.py's copy had missed -var and -const).
  results/rtinline-694.md.
  **695: DOES> @ in rtvar** (cv8-fuse-var.4's DOES-@: the tail decoded from the child's call, `R> @` and EXIT in its
  three forms): shellmix alone 0.606 on fastest-x86-64 (the JIT translates the hooks' and buffers' callers now), 0.783
  on portable-fastest; rtvar-check.py PASS on three. results/does-at-695.md.
  **696: the rehearsal of the three together** (a scratch clone): the front alive with them; per workload the programs
  gain (bubble, ackermann ~0.9) and the corpus pays 1.11-1.22 (the compile layer - rtinline's scan most); rtinline's
  fold search behind a bitmap halved its share (1.125 -> ~1.07); the score nets 0.94-1.01, at 0.8-1.6 KB of image.
  results/rehearsal-696.md.
  **697: the laptop's run set - `seed 92 14h widths`** (lab/evolve/NEXT-RUN; the owner: 14 hours): every design, the
  JIT's too, at both widths, the newest four fronts carried. The new series' method line is in
  results/stopping-series.md already ("from seed 92", matched by generation) - **process seed 92 without
  NEXT_METHOD**. A search now makes and checks every dump before its workers fork (evolve.py's prebuild_dumps: 10,198
  at two widths, 246 s here; ~1.1 GB in build/dumps-HASH), and a dump that fails in a worker is an error there, not an
  exit (which would have left its design's result never coming). Self-hosting (cross-cv8.4) fills neither VAR-OPS nor
  INL-OPS yet (zeros: the fusions off in self-built images - phase 6's).
  **698: seed 92 processed** (results/evolve-amd-ryzen-7-pro-8840hs-seed92.md): 49,601 designs, 166 generations, the
  checks clean; it opens the series (hypervolume 0.31386; fastest 0.1245, smallest 22,417 B with the five programs'
  code, 108 KB, 32-bit 0.1542). Step 3's genes each below their children's share on the front (rtinline 32 of 386, 8 in
  the fastest tenth; rtconst 17, rtvar 2): speed-for-bytes trades (pairs: rtinline 0.959 for +673 B) - newgenes-seed92.
  The held-out code (lab/evolve/heldout-code.py, new): Spearman 0.813 with the selection's, the small end's regret 0 B.
  Found and fixed: since 678 the report's records begin `{"app"`, and eleven readers keyed on `{"bin"` saw no front
  (seed-facts.py, gate.py among them) - fixed before the gate ran. **699: seed 93 processed**
  (results/evolve-amd-ryzen-7-pro-8840hs-seed93.md): 49,137 designs, 160 generations, the checks clean; it **gains** by
  the fastest (0.1218, -2.2 %) and the fastest at 32 bits (0.1506, -2.3 %), both in-run and just past 2 % (the curse
  1.085; the front re-measured, its fastest 0.130 against seed 92's 0.1277); the hypervolume 0.31632 (+0.8 %), the
  smallest 22,411 B. Step 3's genes on 67 of 401 (rtinline 53, 11 in the fastest tenth; lab/evolve/newgenes.py, seed
  92's draft made a tool); the held-out code's regret 0 B again. **700: seed 94 processed**
  (results/evolve-amd-ryzen-7-pro-8840hs-seed94.md): 43,109 designs, 136 generations - a stall at generation 44 (93
  minutes; 18 runs timed out, 4 compiles past cc's 60 s CPU limit, one 32-bit build) cost 24; nothing new found. Its
  fastest at 32 bits (2806f89619, 0.1426) a wrong kernel reading in the stall (0.119 against its parent's 0.362; built
  here, 1.019 of the parent's time) - struck from the stopping line (results/drafts/stall-seed94.py, ktime-seed94.py;
  the owner: "ensure we don't lose any good designs"), the hypervolume then flat (0.31733); it gains by the least memory
  alone (104 KB: one page, designs carried from seeds 84-90 - one page the re-measure's noise: the threshold 8 KB from
  seed 95, 702).
  **701 (while seed 95 runs; the owner: "proceed in this chat")**: lab/evolve/outliers.py - a fast-end reading one
  workload 2x off its parent's and 1.5x off the fast end's median, the rest within 10 % (seed 94: 2806f89619 alone; in
  summary.md, run-tests' self-test) - and stopping.py --strike ID --why TEXT (the ledger's line and the curve file say
  which; process-records.sh's STRIKE; process-finish.sh stops without a stopping line). The after-seed-95 batch
  (batch-check PASS): why32's end kept, fail32 naming a time limit; --remeasure's 32-bit fastest tenth measured again
  into remeasure32.json (it measured the 64-bit front only); the ticker's machine line (load, memory, swap, clock, heat,
  AC) and a late tick - no gene or measure in the run changed, the method stands. **702 (the owner)**: the least
  memory's threshold 8 KB from seed 95 (stopping.py's mem_kb; GOALS.md) - of 2,769 designs read in two or more results
  files 416 differ, 334 by one page (results/drafts/memory-noise-702.py); seeds before 95 keep 4 KB, so seed 94's gain
  and the earliest stop after seed 96 stand; seed 95's memory bar 96 KB.
  (batch-check.sh tests results/pending's patches only - not direct commits.) **703: seed 95 processed**
  (results/evolve-amd-ryzen-7-pro-8840hs-seed95.md): 60,264 designs, 205 generations, the checks clean (the gate 462 of
  462, ans-check 0 of 101, the deaths all expected); **it gains nothing** - the fastest 0.1199 (-1.4 %), at 32 bits
  0.1485 (-0.7 %), each about 1.3 % in-run; the hypervolume 0.31512 (-0.7 %; 0.3148-0.3192 all run); the smallest
  22,409 B unmoved from generation 0; the memory 108 KB (seed 94's 104 KB designs re-read 108-112 here: 702's noise).
  2806f89619's strike confirmed (0.1733 at 32 bits). The after-seed-95 batch applied (dc3dcac). Predictions 5 of 5.
  **704: seed 96 processed** (results/evolve-amd-ryzen-7-pro-8840hs-seed96.md): 79,690 designs, 279 generations (21 h),
  the checks clean (the gate 504 of 504, ans-check 0 of 115, deaths-check 16 of 16 right here); **it gains nothing** -
  the fastest 0.1190 (-0.8 %), at 32 bits 0.1470 (-1.0 %), neither moving after generation 84; the hypervolume 0.31378
  (-1.1 %); the smallest 22,409 B, the memory 108 KB. **The stopping rule stops: the reopened search's series ends at
  seed 96** (seeds 92-96; the fastest 0.1245 to 0.1190, 4.4 % over five runs). A stall in generation 0 (the ticker's
  first catch: load 27-32, 21:56-22:25) killed 16 carried designs, each right here, one on seed 95's front
  (b25c984a48) - restored, nothing moves (results/drafts/stall-seed96.py). Predictions 5 of 6. NEXT-RUN none.
  **705: the plan's step 6 begun - the new roles** (the owner: "let's go straight to the new designs" - no confirmation
  run; the 573 rule's 5 % band in two chains; the first 21 hours, dream and the Tegra): results/drafts/new-roles-plan-705.md.
  The series' pool (46,971 alive: seed 96's database and seeds 92-95's fronts; results/drafts/new-roles-705.py) gives
  **the screen's lists** - results/followup-seed96-roles.md, 944 for the laptop and dream (the whole pool and its JIT-free
  designs by final-set.py, within 5 % of the fastest at either width, the JIT-free front, the holders), and its -arm
  list, 437 for the Tegra; the ten holders under today's measure in results/roles-holders-705.md (none of the eight the
  pool lacks on its fronts; the smallest holder 22,837 B against the pool's 22,409). lab/evolve/measure-ids.py (new):
  the chain's first step measures the holders on the laptop (this sandbox's memory reads 12-16 KB high). The ARMv7
  pre-flight (results/drafts/arm-preflight-705.md): clang's new-gene builds alive under qemu; GCC's tos=1 designs die
  there on the corpus's misaligned 2@ - a qemu artifact (7fb40ff7ba, measured on the Tegra in the final check, dies the
  same). **Chain A is NEXT-RUN and REMOTES** (about 21.5 hours).
  **706 (while chain A runs; the owner: "use whatever is useful from TRIZ, proceed")**: results/drafts/triz-706.md - TRIZ
  proposes, measurement decides; the contradiction inventory's method (a gene's pairs, the element's physical
  contradiction, the separations, the register, the price) and seed 96's five. **Mechanism 9 (the JIT header) priced**:
  its 4-byte field's two jobs elsewhere - the length at an end-EXIT, the offset in a side table (V1: +95-152 engine
  bytes, up to +8 KB) or in the translated word's dead bytecode (V1': separation in time, no table) - -700 B of the five
  programs' code, about -1.8 % on the smallest JIT design; the trigger byte stays; not built (after the roles, the
  owner's call; GOALS.md's register). **The after-seed-96 batch** (results/applied-after-seed96/ORDER.md; batch-check PASS): arm2at -
  2@ and 2! through a byte-aligned cell, so GCC no longer joins a tos=1 design's two loads into ARMv7's LDRD (x86
  engines byte-identical, 48 of 48; the GCC ARMv7 builds alive under qemu - results/drafts/arm2at-706.md); armcheck -
  arm-cross-check.py compares as evolve.py does ("Redefining:" lines out; s0-cell's false DIFFER).
  **707 (the owner: "use anything that can help think out of the box and find new nontrivial designs")**:
  results/drafts/ideation-707.md - each method run, its result. **The pre-mortem** of the new roles (prompt 16, late;
  results/drafts/premortem-roles-707.md): chain A's laptop sessions carry no load record (the ticker ran for seed runs
  only - ticker-after-seed96.patch for chain B; chain A's sessions checked against each other on the holders), and the
  self-built images ship without the run-time fusions - **a gate**: a role ships when its self-built image's speed is
  the translator's, else its translator-built image, named. **lab/evolve/fuzz-designs.py** (new): x86 clean at both
  widths (2,240 runs); ARMv7 under qemu found the misaligned 2@ and 2! in clang's builds too (3 tos=1 designs; 0 with
  the batch's arm2at). **The engine read by symbol size**: the variadic syscall, 241 bytes - rtsc-after-seed96.patch,
  -192 to -304 bytes on every x86-64 design (results/drafts/rtsc-707.md). **Priced, not built**: the image's names in
  their chains by use - zero bytes, the lookup's walk 43-49 % shorter on parse (results/drafts/chain-order-707.txt); with
  706's mechanism 9, the two candidate genes for a next search (the owner's call, after the roles). **Closed**: a size
  superoptimizer (at most 11 bytes), gene-interaction mining (no synergy), a perfect hash of names (too many bytes).
  **708 (the owner)**: the roles' memory rule 8 KB, not 4 (followup-roles.py; HANDOFF-REFERENCE.md's standing decisions
  give the data); **the search reopens after the roles** - chainorder and mechanism 9's V1' built as genes, then a new
  series.
  **709 (the owner: "proceed" - the sweep with the evaluator in the loop)**: results/drafts/sweep-709.md. Two patches
  into the batch: sysstubs (the runtime's system calls as unified stubs; clang's x86-64 engines -176 to -400 bytes, GCC's
  unchanged - its LTO inlines the C wrappers) and imagemsg (the image's refusals as `not a RelF image (N)`, a check
  digit; -226 to -458 bytes on every design, both widths; user-visible, the owner told). The smallest engine 4,768 to
  4,230. Not reached: the profiler's top dispatches (speed) - after chain A, on the shortlist's fastest.
  **710 (the owner: "yes" - the genes built while chain A runs)**: results/drafts/jitdead-710.md. **Chainorder
  mispriced** at 707 (byte headers' links point backward only: signed links, +19-73 B, five places to change) - the
  owner told; a converter-and-engine prototype, instructions counted, before the full build. **Mechanism 9's V1' built:
  the gene jitdead** (results/applied-genes-727 - its own queue, applied after the roles ship, after the after-seed-96
  batch; batch-check with BASE=results/pending until that is applied): -700 B of the programs' code, the total -0.3 to
  -2.9 % on ten JIT designs, instructions the same or fewer; not yet in the self-hosting compiler (G-NOT-YET).
  **wends16** into the after-seed-96 batch: -1.1 KB on every jitx engine.
  **711 (the owner: "reuse whatever you think is reasonable" from Architect Labs' Frostbite)**: results/drafts/
  frostbite-711.md. The counters patch into the batch - mispredictions and last-level misses beside instructions and
  cycles, kept per workload, chain B's lines carrying them, lab/evolve/countfit.py to fit the time to them after
  chain B (a screen without rounds, if it holds). The held-out check on the screen's pool: the interpreted end's
  search-set advantage carries about a fifth to the held-out pair - proposed: the roles' held-out pair reported, more
  held out by group in the reopened search (the owner's call).
  **712 (the owner: a deep dive for more that can help)**: results/drafts/literature-712.md. The register's stack-header
  premise is wrong on x86-64 since Linux 5.8 (exec-none: the stack stays rw-) - -48 bytes on every 8-byte engine with
  a one-segment link, the owner's call reopened; proposed, not built: countfit with shared penalties, counters.py
  --topdown (Zen 4), the roles' build-level spread, Gforth 1.0 in the comparisons.
  **713: chain A processed** (results/followup-roles-seed96-roles.md): the laptop 5 sessions (a sixth ended by hand),
  dream 8 a width, the Tegra 3, none died; predictions 6 of 6. The after-seed-96 batch applied first (7081f96 -
  results/applied-after-seed96; every engine 482-2,224 bytes smaller, the small end's order unchanged: sizes-713.py).
  followup-roles.py fixed (the list had no "jit" mark: the portable roles had taken JIT designs - now the JIT expressed).
  On the screen seven of ten holders beaten by the rule - the smallest to one of six at 21,679 B (25-29 % faster), least
  memory tied at 108 KB (five reads in chain B), small-and-fast-on-ARMv7 kept, the smallest JIT design's contenders all
  trades (the owner's). Chain B (the owner's 19 hours, restarted for "not losing good designs"): the 99 of results/followup-seed96-roles-b.md.
  **714: chain B processed** (results/followup-roles-seed96-roles-b.md): the laptop 18 sessions, dream 34 a width, the
  Tegra 5 at 10 rounds, none died, no stall (the ticker's one load spike, session 6, inside the noise); no PMU counts
  (paranoid not set); predictions 7 of 8 ((1b) wrong, (7) void). Settled: the fastest on ARMv7 a8d35bdccc (-2.63 % +/-
  0.39 %), the knee 48a012411a (bytes -1.38 %, speed within 1 %), the fastest on x86-64 9b15ba26f7 (-10.65 %), best
  all-round df097ba2e2 (-7.53 %); least memory the holder fb0d57c8a2 (four at 112 KB, every contender an ARMv7 trade - the
  laptop reads the lean end 4 KB above chain A). Led, not settled - **the owner (714): "our goal is not to lose any
  potentially good designs"**, so a tie keeps both: the fastest portable d727605472 (-7.46 %) with 5f7e66b12d (+0.24 % +/-
  0.16 %, 4.2 % smaller), the fastest on x86-32 ea782c6094 (-5.49 %) with five within 2 SE (11f956db93 3.8 % smaller,
  16 KB leaner - assumed: broken by size if still tied after chain C). The smallest: 219878ec89 21,673 B, the four at
  21,679 B 11 % faster on x86-64 (a trade), and **pool-sizes.py found 23 designs at 21,666-21,670 B, never timed**; small
  and fast on ARMv7 and the smallest JIT design kept, their long shots in chain C. results/drafts/chainB-714.py (the
  near-ties, the smallest's contenders, the stalls, the ticker).
  Chain C (the owner: 6 hours): results/followup-seed96-roles-c.md, 66 (results/drafts/chainC-list-714.py); -c-arm 34.
  **714, while chain C runs (the owner: "yes")**: self-hosting phase 6's first part - forth/cross-cv8.4 fills VAR-OPS
  and INL-OPS as layout.py does (VAR-OPS!, INL-OPS!), and does FILL outside a definition and ?DO, which
  cv8-fuse-inline.4 needed: every rtinline design failed to self-host before. results/selfhost-fusions-714.md: the
  tables the translator's to the byte in five designs (both headers, the JIT, rtvar on two variants made for it), the
  probes the same, the programs' code differing only by A's smaller layout (results/drafts/selfhost-ids-714.sh,
  fusetab-714.py). **Then (the owner: "yes" again) --guard-abort**: the cross compiler guards ABORT" as guard_aborts
  does (G-GUARD-ABORT in the genes; 0 for the shipped ten's) - 9b15ba26f7 and df097ba2e2 self-host, and ca04ccb8ec, the
  first real rtvar design to (VAR-OPS the translator's); 11 designs PASS. Still not done (G-NOT-YET): --factor (done at 715, below) and the
  fused =I?BRANCH / DUP?NBRANCH - d727605472 and 5f7e66b12d, the fastest portable's pair; before the roles ship, or the
  gate ships those two translator-built. Chain C's processing rehearsed (results/drafts/chainC-rehearsal-714.sh: PASS
  after the ROLES fix below). **The ship step's fallback** (the owner: "yes"): tools/selfhost-ship.sh no longer stops at a
  design the cross compiler cannot build - it keeps the converter's images, named in TRANSLATOR-BUILT with the reason;
  `make selfhost`, run-tests and freeze-build-645.sh follow it; rehearsed with chain B's leaders
  (results/drafts/ship-rehearsal-714.sh: nine shipped, portable-fastest named - PASS).
  Offered for the time between runs, not started (none is needed before chain C's processing or the roles step): the
  gate's speed half - an experiment timing each design's self-built image against its translator-built one on the
  laptop, for the first laptop run after the roles (so far the gate is the deterministic half: results/selfhost-fusions-714.md);
  the fused =I?BRANCH / DUP?NBRANCH in the cross compiler. The lean end's 4 KB between chains A and B: the
  after-seed-96 batch's layout, one page up or down by design (results/drafts/memshift-714.md) - pre-batch memory records
  do not compare page for page with chain B's.
  **715 (the owner: "start --factor now")**: the gene factor in the cross compiler - forth/cross-cv8.4 finds and
  chooses the runs itself by layout.py's rules (pass 2 keeps the cold words' operations, the search between passes 2
  and 3, pass 3 the uses as chained calls checked against pass 2, the bodies after the last word); the genes G-FACTOR,
  G-FACTOR-ANY, G-FACTOR-COLD, G-FACTOR-NOT (export-genes.py), --factor out of G-NOT-YET. The fastest portable pair
  without the fused branches and one at factor=3 self-host at both widths, the gate passed; the runs considered the
  translator's exactly, the choice a body short, the net bytes within 1 (factor=3: 182 against 197) -
  results/selfhost-factor-715.md. Left for the pair: the fused =I?BRANCH / DUP?NBRANCH.
  **716: chain C processed** (results/followup-roles-seed96-roles-c.md): the laptop 6 sessions, dream 11 a width, the
  Tegra 2 (a session's length barely follows the list's: dream ~900 s with 66 as with 99), none died, no stall, no PMU
  counts; predictions 4 of 8. Settled: small and fast on ARMv7 the holder ae99617f06; **the smallest JIT design
  15eda54ebd** (36,344 B, -1.25 %; x86-64 -0.69 %, x86-32 +0.27 %, -4 KB; fa38596098 and 13a2b38e1b beat c6f1c1331b too).
  pool-sizes.py's 1,054 JIT finds (32,044-34,714 B) all trades, none within 20 % in in-run terms
  (results/drafts/jitmiddle-716.py); the band up to ~38,600 B before the batch not reached. **Waiting for the owner**:
  the smallest - 3456fc28b2 (21,666 B, the fewest: x86-64 -11.3 %, x86-32 +5.5 %, ARMv7 +3.6 % against 219878ec89),
  219878ec89 (21,673 B, the rule's: none smaller beats it) or 90273721a1 (21,679 B: -11.3 %, -2.1 %, -0.2 %, pooled over
  chains B and C); the fastest portable still tied (5f7e66b12d +0.21 % +/- 0.14 % pooled, 4.2 % smaller, x86-32 +2.7 %);
  the x86-32 tie by size - 11f956db93 (714's assumption) to confirm; whether the unreached JIT band is screened (in-run
  speed first, then a build). The ten then: fastest portable (the tie), fastest on ARMv7 a8d35bdccc, the knee
  48a012411a, small and fast on ARMv7 ae99617f06, least memory fb0d57c8a2, smallest (the trade), fastest on x86-64
  9b15ba26f7, fastest on x86-32 (the tie), best all-round df097ba2e2, the smallest JIT design 15eda54ebd.
  results/drafts/chainC-716.py: the open pairs in chains B and C and pooled.
  **717 (the owner: a deep dive into the esoteric languages, then the next run as I think most reasonable)**:
  results/drafts/esolangs-717.md - FALSE, the Brainfuck optimisers, Befunge-93/Funge-98 (befunjit, ff3, bef2c), the
  golfing languages, Joy, sectorforth and milliForth against the genes and the register: most here. New: **literals
  converted before the lookup** (FALSE's first-character dispatch; results/drafts/esolangs-717.py): literals 28.6 % of
  the corpus's tokens and 93 % of its misses, 50 % of parse's - about half their dictionary walk for a few tens of bytes;
  the gene numfirst proposed for the reopened search (the owner's call). **Chain D is NEXT-RUN and REMOTES** (about 4
  hours, the laptop and dream; the owner left the run to me): the smallest JIT design's band chain C's 40 minutes did not
  reach - pool-sizes.py --jit-speed 0.2116 --jit-speed32 0.2354 (15eda54ebd's seed 96 readings + 10 %, the records
  screened before building) --below-jit 35980 --write build/evolve/jitband-list.md --anchors all --cap 30; the results
  files alone gave 23 (results/followup-seed96-jitband.md, with the role's 5 anchors - dream measures these 28);
  measure-ids.py and loadtest.py at 10 rounds on the written list. **The PMU's counts (719, the owner: the sudo commands in
  the run, every setting restored at its end)**: loadtest.py takes the chain's perf hold as clockcheck.py does (545) -
  next-run.sh asks sudo once at the start (from a terminal), root's perf-hold.py sets kernel.perf_event_paranoid to 2 only
  while loadtest.py measures, restores it after each session, at a crash and at the chain's end; the pack carries
  perf-hold.log and perf.txt - the processing checks the value at the pack is the starting one, then countfit.py on the
  "cnt" lines (711). Tested here as root: 4 -> 2 while measuring -> 4 after, the hold gone at the chain's end (this VM has
  no PMU, so no "cnt" here). **720 (the owner: "include all the runs you need into next run")**: chain D carries the
  roles' machine work too, about 5 hours - first `experiment rage-designs.py` (647: the Tegra's GCC 16 on designs/' GCC
  designs' forth-arm, a8d35bdccc new - its rage-designs.md must say PASS), then the screen, then **lab/evolve/selfhost-speed.py**
  (new: the gate's speed half - each self-built role on its own engine against the translator's build, 5 alternations of
  10 rounds, both widths; at most 1.02 keeps it self-built, else the processing ships its translator-built images and
  names it in designs/TRANSLATOR-BUILT with the ratio; here on the VM, 2 rounds: small-jit's 4-byte image 1.07-1.09 - the
  laptop decides), then loadtest.py's repeats (dream 150 + 150 minutes). **721 (while chain D runs)**: the VM's 1.07-1.09
  is no defect - cachegrind's instructions (results/drafts/selfspeed-counts-721.py; the 4-byte engines under `setarch -L`,
  their legacy-layout re-exec otherwise lands on valgrind's tool) self / translator 0.998-0.999 for small-jit and smallest
  at both widths, every workload within 1 %; a gate FAIL ships translator-built by `TRANSLATOR='NAME:REASON' sh
  tools/selfhost-ship.sh` (new) in roles-build-718.sh's phase 2; relf's handoff drafted
  (results/drafts/handoff-relf-draft-721.md - [chain D] marks what is left). **Its processing** (rehearsed at 721:
  results/drafts/chainD-rehearsal-721.sh PASS - it found and fixed followup-roles.py's crash on a chain without the Tegra;
  process-followup.sh merges the pool-sizes --write list into the list itself, lab/evolve/written-list.py): the Tegra's
  rage-designs.md PASS, selfhost-speed.md's gate, then
  `HANDOFF=results/handoff-relf-657.md PRED=717 sh lab/evolve/process-followup.sh 96-jitband ITERATION
  smalljit=15eda54ebd` (the laptop and dream only: the JIT designs' two classes), results/drafts/chainB-714.py and
  chainC-716.py's pairing on its readings; a beater by the rule replaces 15eda54ebd.
  **722 (while chain D runs)**: the fused =I?BRANCH / DUP?NBRANCH in forth/cross-cv8.4 (EQI-PASS, KEEP-PASS; G-NOT-YET
  empty) - portable-fastest d727605472 self-hosts at both widths, instructions self / translator 0.9988
  (results/drafts/selfspeed-pf-722.txt), **shipped self-built: all ten, designs/TRANSLATOR-BUILT gone**; run-tests PASS.
  Chain D's selfhost-speed.md has no reading for it (named translator-built in the laptop's tree, so skipped): its
  timing is the next laptop run's, the counts the gate meanwhile - do not ship it translator-built on chain D's gate.
  **numfirst priced** (results/drafts/numfirst-722.md; prototype numfirst-722.4, .py): smallest's dispatches corpus
  0.748, parse 0.672, kernel and apps 0.99, +148 B; with FIND and NUMBER? in C (portable-fastest) the Forth test adds
  dispatches (corpus 1.095; instructions 0.984) - a gene in two forms for the reopened search (the owner's call).
  **723 (while chain D runs; the owner: "go ahead")**: the fused branches checked on variants that use them all - every
  form fires self-built, both widths (results/drafts/branches-723.md); **after chain D, rehearse the one-design rebuild
  with `sh results/drafts/rebuild-rehearsal-723.sh NAME`** (PASS for small-jit; read its check, not roles-build's own
  "differ" line, which counts untracked binaries and the genes' path comment). numfirst's C form priced
  (numfirst-722.md's 723 section): on the nine klookup roles no dispatch, corpus instructions 0.905-0.990, kernel up to
  +0.37 % - the Forth form for smallest, the C one for the rest.
  **724 (while chain D runs)**: **the queued genes rebased** - 713's patches no longer applied to master; made again
  (one conflict), and **jitdead in the cross compiler queued** after them (results/applied-genes-727/jitdead-cross-after-
  seed96.patch; ORDER.md's order now four) - four JIT records with jitdead self-host at both widths
  (results/drafts/jitdead-cross-723.md); the shipped designs' genes need no export for it. The 723 =I?BRANCH gap left
  open (a per-word map needed).
  **725: chain D processed** (results/followup-roles-seed96-jitband.md; results/drafts/chainD-725.py): **small-jit stays
  15eda54ebd** - pool-sizes.py built 1,048 JIT records, 1,000 below 35,980 B; none of the 54 smaller JIT designs measured
  beats it (every one at least 4 % slower on x86-64 on the laptop alone - dream had only the 28 named at the start, so the
  30 new finds had no pooled class). **The gate: 6 of 9 self-built pass; fastest-x86-32 (4-byte 1.021), fastest-x86-64
  (8-byte 1.046) and small-jit (4-byte 1.036) ship translator-built** (the owner: the rule as written) - roles-build-718.sh
  with TRANSLATOR= for the three, designs/TRANSLATOR-BUILT names them; the JIT designs swing ~5 % either way, the
  instructions the same (721). **The rage check failed on export-arm.py's own check** (a self-built image32.img asked to be
  the translator's; designs/ self-built since 676) before the GCC designs' bytes - fixed: a `selfhost32` design's image not
  asked, forth-arm runs the shipped image (the clang three PASS here under qemu-arm, a planted byte still caught on a
  translator-built export). **dream runs the GCC JIT designs ~3.2 times slower at 4-byte cells** (11 of 11; clang 1.17; the
  same binaries normal at 8 bytes and on the laptop) - nothing shipped (the JIT roles are clang), cause not found (perf on
  dream would tell); the roles' pooled x86-32 class carries it. The PMU's counts arrived (countfit.py: ~3 % error, not a
  2 % screen). NEXT-RUN: rage-designs.py again, then selfhost-speed.py portable-fastest.
  **726: both PASS** (results/rage-designs-726.md, selfhost-speed-726.md; results/drafts/chain-pack-726.py on the archive):
  the chain 586 s, not the 40 minutes guessed (654's 17 were the whole chain; the Tegra's step 206 s against 654's ~12
  minutes, a fresh clone both times - not explained, the bytes decide); the GCC three's forth-arm the lab's bytes running
  their self-built image32.img (11,158, 13,014, 16,782 B - least-memory and portable-small 426 B under 654's); portable-
  fastest 0.9974 / 0.9867, stays self-built - seven self-built, three translator-built. Predictions 3 of 3. **The roles
  shipped**: results/handoff-relf-726.md (results/drafts/relf-handoff-726.py: the draft made final - 8 of the ten changed
  since 657, not the draft's seven; the tag now on portable-fastest too) and the package
  forth-vm-evolution-designs-iter726.tar.gz (pack-designs.py on results/relf-designs-718.md: 20 of 20 builds 9 of 9 right,
  the 40 checksums designs-sha256-718.txt's; the lab's build - the converter's images). NEXT-RUN none.
  **727 (the owner: "finalize design evolution and ensure we found best designs, handoff to relf project after that")**:
  **relf's handoff held** - handoff-relf-726.md and the iter726 package not sent; both made again from the reopened
  search's roles (results/drafts/relf-handoff-726.py adapted, pack-designs.py), one handoff at the end. The reopened
  search's preparation now: the queued genes (jitdead = V1', fixenv, jitfew) applied; chainorder's prototype, numfirst
  (a gene in its two forms - 'offer trade-offs as genes'), the fixed data layout's step 1 (GOALS.md's register, 713)
  each built as a gene where its prototype pays; the rehearsal of them together; then the series' first seed (the
  owner's hours), the stopping rule, the roles' follow-up chains, the handoff.
  **728 (the owner: the demoscene's and the IOCCC's implementations)**: results/drafts/demoscene-ioccc-727.md - all
  covered or not for an interpreter but one: **hashk**, the chain hash's seed searched per image (crinkler's per-program
  brute force; results/drafts/hashseed-727.py, .txt): out of sample alone -5 to -15 % of the corpus's walk, -4 to -47 %
  of parse's; with chainorder up to three fifths - built with chainorder's prototype (both place names in chains).
  Names stored as hashes rejected (FIND must be exact).
  **hashk measured (728)** on a prototype (results/drafts/hashk-727.py, .txt; the survey document's last sections): the
  smallest -9.0 % of the corpus's instructions, -17.5 % of parse's (image -16 B); portable-fastest -3.6 %, -3.2 % (+8 B);
  outputs the same. **One K for all**: h = ((v * 18835) >> 8) & (chains - 1) (hashk-table-728.txt: the ten roles
  -11 to -24 % of the corpus's visits). chainorder priced from it (chainorder-est-727.py): parse -21.6 % / -7.4 %, above
  hashk - but the model misreads the corpus; its build (signed links) after hashk's. **Next: hashk built as a gene**
  (a scratch clone, a patch, batch-check): an always-compiled HASHK swapped into HASH when on, dropped when off (the 718
  checksums prove the off-images), -DHASHK for the engine's two hashes (and gen-msc's), the cross compilers' THASH.
  **730: hashk built and applied** (results/pending/hashk.patch, now results/applied-hashk-730/; batch-check PASS):
  off, every byte as before (the 718 checksums, the stage images, run-tests, validate, engines-check 113 of 113); on, the
  ten roles' outputs the same at 8-byte cells, three at 4 (results/drafts/hashk-gene-729.py, .txt) - corpus 0.914-0.994
  of the instructions, parse 0.833-1.000, most at 16 chains. Found on the way: the hash had five copies, not three -
  gen-msc.py's and gen-tos.py's too (the JIT designs died until gen-tos.py had CHAIN). **Next: hashk in the cross
  compiler**, then chainorder's build.
  **731: hashk in the self-hosting compiler** (results/applied-hashk-cross-731/; batch-check PASS): the word HASH8 (the
  converter's own swap; the cross compiler's X8 rule), G-HASHK in genes.4 and THASH, cv8-hashk.4 among the overlays
  where HASH is no engine op; stages/s6-genes.4 written again (it lagged since 714: G-JITDEAD, G-FACTOR... all 0 for
  s6). smallest, portable-fastest and small-jit with hashk self-built at both widths, A = B and the gate
  (results/drafts/hashk-cross-731.sh, .txt). **Next: chainorder's build** (signed links), then numfirst as a gene.
  chainorder's margin over hashk as built (results/drafts/chainorder-margin-731.py, .txt - the ten roles, entries
  visited): corpus -6 to -10 %, parse -26 to -41 %, the five programs -18 to -34 % - worth its build. The plan: zigzag
  links (2|d| + sign) when on; the readers C's PREVNFA (both forms) and Forth's NEXT-NFA8 (cv8b.4, cv8bt.4), the
  writers LINK-LEN and LINK, (both), layout.py's linklen/linkbytes and its chain order by a committed use file (the
  held-out three's lookups by name - deterministic), the cross compiler's LINK-LEN-T, LINK,-T, LINK@-T and order;
  the Forth words as hashk's were: alternatives in every dump, swapped in with the gene, dropped without; a name's
  duplicates newest first (the use count is the name's), a run-time definition at its chain's front as now.
  **732: chainorder built as a converter-only gene and applied** (results/applied-chainorder-732/; batch-check PASS) -
  the owner chose "full, with self-hosting", then, shown the measurements, "gene now, self-host later": the
  self-hosting part is built only if a final role takes the gene (export-genes refuses it until then - G-NOT-YET).
  The zigzag encoding first (every link signed) lost: each step of a walk paid the decode, the smallest's corpus +13 %.
  As applied, backward links as before and a forward link its own three-byte form (tag F0-FF; tag 2's E0-FF); the
  names looked up 64 times or more in the held-out programs first. The ten roles (results/drafts/chainorder-732.txt):
  outputs the same; the corpus's instructions 0.987-1.031 of off, parse 0.79-0.99, the images +56-120 B; with hashk
  the smallest's corpus 0.903. Found on the way: bfind's bf_prev, a sixth link reader (the JIT roles crashed until it
  read the forward form); lab/evolve/test-resume.py's noise 1.0 (the gene moved its draws - the control stopped
  forking at 0.6; at 1.0 it forks with and without). The self-hosting part, when needed: forward links laid as three-
  byte placeholders and patched at the end - one pass.
  **733: numfirst built as a gene and applied** (results/applied-numfirst-733/; batch-check PASS) - while no name of
  the form -?[0-9]+ is defined, a token of that form goes to NUMBER? without FIND's walk; the flag the prologue's last
  padding byte (SAVE-SYSTEM keeps it), set by HEADER8. Two forms: with klookup the engine's (FIND) answers at once
  (-DNUMFIRST), without it forth/cv8-numfirst.4's INTERPRET8 skips FIND. The ten roles (results/drafts/numfirst-733.txt):
  outputs the same; the corpus's instructions 0.756-0.999 of off, parse 0.683-0.994 (the smallest with hashk 0.725,
  0.587); +55-106 B of image; off, every byte as before. Not yet in the self-hosting compiler (G-NOT-YET): HEADER8 as
  the last X8 and INTERPRET8 for the Forth form - built if a final role takes the gene, as chainorder's.
  **734: the fixed data layout's step 1 built and applied** (results/applied-data-layout-734/; batch-check PASS) -
  engine/data-layout.ld, an augmenting linker script: the small variables on one page of their own, the tables a run
  touches after them (then t_obuf and heads, used from their start), the big buffers after those. The ten roles
  (results/drafts/data-layout-734.txt): no byte of engine, output or instruction moved; the memory 8-36 KB less on
  nine, least-memory the same; start-up 2-8 faults fewer. Every run's memory reads lower from here: records of the
  runs before (and the ten roles' 718 records) are on the old layout - the series' pooled picks measure again, as
  727's fixed environment already asks. The designs shipped carry it when exported again (export-designs.py copies
  the script into src/). Step 2 (the stack tops on one page) open, priced apart.
  **735: the rehearsal** (results/rehearsal-735.md): the ten roles off and on, every evaluation ok; by instructions the
  selection 0.944-1.004 (the corpus 0.71-0.99, parse 0.46-0.98, the kernel workload +0.5-3.8 %), the JIT roles' memory
  30-72 KB less, the totals +38-567 B. Its short run found and the iteration fixed a death of the new genes - a design
  of no other part with hashk on had no HASH8 in build-stages.sh's plain dump; now such a design with hashk, chainorder
  or numfirst on takes a dump of its own (results/applied-plain-dump-735/; batch-check PASS). **NEXT-RUN: `seed 97 16h
  widths`** (the owner: "let's do next run 16 hours") - the new series' first run (its method line in
  results/stopping-series.md: the genes, the environment, the layout); predictions 5. **Next: process seed 97** - its
  results file, the stopping rule's first line of the series, then the next seed or the roles' follow-up chains, and
  relf's handoff once at the end (results/handoff-relf-726.md and the iter726 package held, not sent).
  **736 (seed 97 running; the owner: "start with 1 and 2")**: seed 97's processing rehearsed on a stand-in made by
  the laptop's path (results/drafts/process-rehearsal-736.md: every step and check PASS, the stopping rule reading the
  new series; review-checks.py curse guarded for a front under ten), and **numfirst and chainorder self-hosted**
  (results/applied-selfhost-736/): cross-cv8.4's G-SKIP, G-TRIM8, G-ONCE and chainorder's walk across the passes;
  export-genes.py refuses neither. Five designs shipped self-built at both widths with them; small-jit's first try found
  ITEM-START misreading a forward link (fixed). Nothing here changes what the search builds or measures - seed 98 on the
  same method. NEXT-RUN none in this bundle (seed 97 runs from iter735's). **Next: process seed 97**
  (process-rehearsal-736.sh shows the steps).
  **718 (the owner, on the three choices: "no strong opinions - the most reasonable way, not losing any good designs")**:
  each decided by the chains' own rule (1 % smaller, no class 2 % slower, memory within 8 KB; 649's precedent for the
  smallest) - results/new-roles-718.md: **smallest 219878ec89** (the 23 smaller all trades), **portable-fastest
  d727605472** (5f7e66b12d: x86-32 +2.7 %), **fastest-x86-32 11f956db93** (3.8 % smaller, 16 KB leaner, tied); every
  near one kept on record there (3456fc28b2, 90273721a1, 5f7e66b12d, 69cebcaed9, 262a51bc6c, 13a2b38e1b, ...). **The ten
  built into designs/** (results/drafts/roles-build-718.sh - 645's build-out in two phases around the cross GCC, which
  removes gcc-multilib; records results/relf-designs-718.md): validate 7 of 7, the export, the clang and the GCC ARM
  rules the lab's bytes, nine self-built (portable-fastest translator-built, TRANSLATOR-BUILT: the fused branches), make
  test, selfhost, 32 and libc, pack-designs 20 of 20 right (results/drafts/designs-sha256-718.txt), run-tests PASS;
  designs/README.md's table from chains B and C (results/drafts/designs-table-718.py). small-jit 15eda54ebd provisional
  until chain D. **The owner, beside chain D**: `RAGECHECK_CMD='sh tools/rage-designs-check.sh' sh tools/rage-check.sh`
  - the Tegra's GCC 16 on the GCC designs' forth-arm (a8d35bdccc new; 17 minutes at 654) - since 720 chain D's first step.
  **After chain D** (725): small-jit unchanged; the gate's three rebuilt translator-built (done). After the rage check's
  rerun: the package and relf's handoff (made, 726; held, 727 - sent after the reopened search's roles). Then the rest
  of the plan (the roles were step 6 - results/drafts/new-roles-plan-705.md): designs/ and the
  package made again (`sh results/drafts/freeze-build-645.sh . RECORDS NAME=ID,...`), self-hosting phase 6 on them (the
  gate: a design the cross compiler cannot build ships translator-built, named - since 722 every role self-builds), relf
  told how to fetch them. From the early games (results/drafts/early-games-713.md): a fixed
  layout of the engine's writable data, a prototype for the reopened search; queued genes (results/applied-genes-727:
  jitdead, fixenv - results/drafts/fixenv-713.md -, jitfew - results/drafts/early-computers-713.md) applied after the
  roles, chainorder if its prototype pays, then the reopened search's series; the article.
- **Next: the ten designs self-hosting, relf's way (the owner, 666)** - a CV8 cross compiler in Forth, run by each
  design, writing its own image from source; new images, measured again; all ten, both widths. The plan, its six
  phases and the checks: results/drafts/selfhost-plan-666.md. Phase 1 done (667-668): forth/cross-cv8.4 self-hosts
  s6-cv8b with its specialisations (small, imm, var, tiny, the folds; loc needs locals, s6 has none) and the X8
  names dropped - the translator-built s6 writes image A, A rebuilds itself byte for byte (9,077 bytes; the
  translator's 9,265), A passes the evolver's gate. Phase 2 begun (669): each design's genes as Forth
  (lab/evolve/export-genes.py: designs/NAME/genes.4, stages/s6-genes.4), the translator's rewrites done while
  compiling, three passes (dead words, call counts, one-byte calls). **All ten designs self-host at both widths**
  (the six portable: phase 2, 670, and phase 4, 671; the four JIT designs: phase 3, 672): every image smaller than
  the translator's (8-byte 208-304 bytes, 4-byte 16-224), A = B on its own engine, the gate passed, the 64-bit build
  making the same 32-bit image, speed the same: `sh tools/selfhost-check.sh [--self-test] [--32] NAME` (s6: no name;
  the tables in the plan). A JIT engine knows its image's layout (src/vm-jit-ops.h's jit_wends and JIT_W_ lines):
  the cross compiler writes them for its image (cv8-self-jit.h) and the check builds the engine with them - phase 5
  ships them with the images. Found at 672: the translator's fastest-x86-32 and small-jit compile a run-time call of
  (PARSE) as the JIT's opcode (layout.py's _jitimg_pick gives the JIT's header to an --op-inline word) - the
  self-built images do not. **Phase 5 done (676)**: designs/ ships the self-built images (both widths, the JIT
  designs' layout lines) and their source, designs/forth/; `make selfhost` in a design rebuilds its image by its own
  engine, byte for byte (at the top: all ten), run by run-tests with two planted faults; tools/selfhost-ship.sh makes
  them, last in the build-out (after export-designs.py and export-arm.py). Next: phase 6 - measured again (the
  laptop, the i7, the Tegra; the GCC three on ARM), the roles, the relf handoff and package (still the translator's
  images), the article - after the reopened search (677, above).
- For relf (673): its report (its Iteration 942) fixed in the engine - on the jitexec designs a THROW from a nested
  interpreter unwinds the C stack to its CATCH's interpreter (RP!), a sentinel leaves to its own; designs/test.sh has
  the cases; results/jit-throw-unwind-673.md. relf takes the three designs' new src/vm.c and src32/vm.c (the
  other seven designs' engines are the recorded bytes).
- For relf (665): its questions answered as far as the search can - results/relf-questions-665.md; a patch for its
  shell tests' /tmp leak - results/relf-patches/tests-tmp-cleanup.patch.
- **The search is over; the freeze done - its batch applied (656), the relf handoff final (657), the article's portable figures (658); reopened by the owner for self-hosting (666), then the article.** The improvement phase ended by the stopping rule (seed 83, 572); the final set,
  21 (598: results/final-set-chainsBCD-seed86.md, results/final-pick-chainCD-seed86.md); consolidation's retirements done
  (599: results/applied-after-seed86/ORDER.md); the method section's figures (600: results/article-figures-600.md). Then
  the portable runs (seeds 87, 88, 91) and the last JIT runs (89, 90), each with a follow-up chain on the three machines
  (results/followup-roles-seed87.md to -seed91.md; every run: results/progress-by-run.md) - the x86 roles final at 630, the
  portable search stopped at 640 - and the final check (641-649, below): no further gain. Each step's bullet as it stood:
  HANDOFF-HISTORY.md, "The card's state at Iteration 650" (before it, the states at 597, 598 and 647).
- **relf's next handoff: after the reopened search's roles (the owner, 727)** - results/handoff-relf-726.md and the package
  forth-vm-evolution-designs-iter726.tar.gz (726) held, not sent; made again then. The bullet below is 657's, history.
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
  above; 650's suggestion). Its last item, the article's portable figures recomputed from the runs' records: done (658).
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
  process, not result - it cancels in every comparison). Section 17 finished in both drafts (658: seeds 88-91, the final check, the ten roles'
  table; results/article-figures-658.md, 22 of 22 figures as the chains' documents have them). `python3 tools/article-check.py --self-test`, exit 0
  after every edit of the drafts (659): the same numbers in both, section by section; 195 of the English 197 distinctive
  figures in the records, the other two from the build at a105e59 - where part one's sizes regenerate, not at master (the
  run-only images grew 6-12% since; results/article-check-659.md): both drafts cite a105e59 for part one (660). Read as a ForthHub member would (661): the
  diagrams aligned, every abbreviation explained before use; eight suggestions for him in
  results/drafts/forthhub-read-661.md, 1-7 done (662-664), and how to get each design (663); 8, the length, is his. Waiting: his review; a Russian reader's pass
  (AUDIENCE.md: a translation-shaped text is a named failure on Habr); prompts 04 and 05 before publishing; the KDPV image.
  The method draft (results/drafts/article-method-548.md): no [check] left (659); the follow-up chain's tool
  ready (lab/evolve/portable-followup.py).
- **Across machines - the owner's terms (576; GOALS.md)**: lose no good design or gene. final-pick.py step 5: the three
  classes' geometric mean; the 25% veto removes nothing, only names the generic pick; the three best means and each
  class's fastest ADDED to the set; a design missing a class ranked on the rest, kept. Consolidation (578, the owner): a
  gene or code path is retired only when no design on the pooled true front uses it - not the final set.
- **Predictions due** (results/predictions.md): seed 97's five (Iteration 735) - scored when it is processed. Scored: the rage check again and portable-fastest's
  gate (725) 3 of 3; chain D's (717-720) 4 of 7, one void; chain C's (714) 4 of 8; chain B's (714) 7 of 8; chain A's (713) 6 of 6; the rage
  check's (654) 1 of 1; the final check's (648-649) 2 of 4 (wrong: the Tegra 2 of 3; a role changed - the smallest, 649).
- **History**: HANDOFF-HISTORY.md - the card's states at 597, 598, 647 and 650 (seeds 70-91, chains A-D, the final pick, the
  portable runs and their follow-ups, the final check's plan) and its forth-arm bullet at 653 and its freeze's-batch bullet at 655 (the rage check's first
  run); remote hosts cleaned after every chain (628: `sh lab/evolve/remote-checks.sh clean runs/chain-...`).
- **Files a new chat needs**: the newest bundle and the next chain's archive (forth-vm-evolution-chain-*_tar.gz). appbench.zip stays on the laptop.

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
   (the owner's hours), this card, the PROGRESS entry; at DONE /tmp/process-checks/heldout-code.txt (the held-out programs'
   code on the front, 698) for the results file. Run nothing as claude while the status's last line says "jail".
   A detached job dies when the turn ends (the sandbox suspends; /tmp stays - 561): start it early, see it to DONE in
   the same turn; cut off, `FROM=checks` resumes it at the checks.
3. At DONE: `sh lab/evolve/process-finish.sh N ITERATION` - it stops naming anything wrong or missing (a check, a TODO, a
   record); fixed, run it again. A reading shown wrong (outliers.py in summary.md - 701): its curve again, detached,
   `stopping.py DB --seed N --strike ID --why TEXT --curve /tmp/process/curve.json`, then `STRIKE=ID STRIKE_WHY='...'`
   before process-finish.sh. It writes the chain line, runs process-records.sh (`NEXT_METHOD='why'` when the next
   run changes the method), commits and makes the bundle: present it.

## The owner's standing decisions - the ones every session uses

The full list, with the reasons: HANDOFF-REFERENCE.md.
- Every patch tested, then verified to apply in order on a fresh clone; batches wait in results/pending/ with ORDER.md;
  `tools/batch-check.sh` runs that test.
- Run lengths are the owner's - ask for each run's hours.
- The roles' memory rule 8 KB (708; 4 before - one page is a design's own noise).
- The search reopens after the new roles: chainorder and mechanism 9's V1' built as genes, then a new series (708).
- relf's handoff once, after the reopened search's roles - "ensure we found best designs" first (727).
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
