# Goals - the aim, how success is measured, and what was rejected

What changes rarely. The present - the state, the routine, the open items - is
HANDOFF.md; the history is PROGRESS.md; every document is indexed in README.md.

## The aim - simplicity and minimalism

**Simplicity and minimalism are this project's main goal** (the owner,
2026-10-06, Iteration 72): the smallest, simplest system that does the
job - small images, a small and plain engine, few mechanisms, each one
easy to read and to remove. Speed is welcome where it costs little; it
does not justify complexity on its own.

**Words in the kernel, and how long they are** (the owner, 2026-10-12,
Iteration 227): the base kernel holds the core words; helper words are
welcome where they are convenient, in a reasonable balance with size - this
is meant to be developer friendly, so a non-standard word that can be reused
keeps its name and its place. Splitting a long word into several named ones
is a plus in its own right when it makes the code easier to understand, to
test and to extend; count that beside the bytes, not after them.

How it decides things:
- **A mechanism earns its place by measurement**, and goes behind a gene
  so that evolution - and the reader - can see what it buys. If it buys
  nothing, it comes out (`rtlit`, Iteration 59).
- **Of two ways to the same result, the simpler one**, even at a small
  cost in speed or bytes; of two designs equally fast and small, the one
  with fewer mechanisms.
- **Complexity is a cost to count, not only to avoid.** The fitness is CPU
  time and IMAGE size; since Iteration 73 every design's ENGINE code
  (its binary's .text) and peak memory (resident, per workload) are
  recorded and reported beside them - tracked, not scored. Anything that
  grows either must show it: the tag added 5.6 KB of engine code to the
  fastest design (39.9 -> 45.5 KB), its peak memory unchanged (1.44 MB).


## Success: three objectives, equal (the owner, Iteration 75)

**The smallest binary + image, the highest speed, the lowest memory** -
treated equally: selection keeps the Pareto front over all three, no weights.
The motivation: logic moved from the image into the engine must show - the
image shrinks, the binary and memory grow.

How each is measured:
- **binary + image**: the engine, stripped, linked WITHOUT the C library (raw
  system calls, engine/rt-linux-x86_64.c) and without unwind tables, so the
  binary is all there is; plus the kernel's image. **The size is the
  kernel's** (the owner, Iteration 138): the kernel holds core words only, the
  base everything else extends; what an extension needs (the shell's OS words,
  its buffers) is the extension's, outside the measure - a kernel word only an
  extension uses belongs in that extension (results/word-audit.md). **Reopened for application code (the
  owner, Iteration 677)**: the size is the engine, the kernel image and the code the selection's
  applications lay (sim16, gc16, scan, evo; relf's shellmix since 686, the owner), bytes equal - one total; an extension's code stays out, wordfreq,
  minif and brainless are held out (results/drafts/search-reopen-plan-677.md; in force since Iteration 678:
  evolve.py's rec['app'], genapps.py's count - results/app-size-measure-678.md).
- **speed**: median CPU time against the hand-made s6, the geometric mean over
  the selection workloads - kernel, fib, corpus, loop, bubble (300 cells),
  ackermann (A(3,5)); parse and sieve held out (Iterations 100, 127-128). The
  gate before any timing: the corpus (661 cases) and the kernel workload
  byte-identical to the reference.
- **memory**: the pages a run touches (cputime's MINFLT times the page size),
  each workload's median over the rounds, the largest the design's. **Within
  8 KB is a tie** (Iteration 77): designs differ by a few pages; a JIT's buffer
  or a leak, tens of KB, still decides.

**Across machines** (the owner, Iteration 377; results/drafts/cross-machine-weighing.md): the best generic
designs are chosen for **three classes of machine, equal** - x86-64, x86 at 32 bits, ARMv7 - by the
geometric mean of their speeds over the classes, each class once, with a veto: none more than a margin
behind the best of its class. **The terms (the owner, Iteration 576: lose no good design or gene - rules not too
strict)**: the veto 25% and it removes nothing - it only decides which design is named the generic pick (the best mean
within the margin everywhere; a vetoed best mean is named beside it); the three best means and each class's fastest
are ADDED to the final set when the laptop's choice lacks them; a JIT design's ARMv7 speed is its own genome with the
JIT off (ARMv7 has no JIT - the design as it builds there; xcheck.py --arm --also, marked); a design missing a class is
ranked on those it has, marked partial, kept. lab/evolve/final-pick.py step 5. Selection stays on the laptop, at both widths; the other
machines test it, designs it rejected included (xcheck --rejected). A disagreement is diagnosed - measured
again, the width separated from the architecture, knockouts on both - before it is weighed; a mechanism
that helps one class and hurts another is a per-architecture build choice only if large and simple.

**Judging a run, and when to stop** (Iterations 78, 188-189): each run against
all the others, measured again in one session - its fastest, smallest and
least-memory designs, the hypervolume in log space, and the best Q (binary +
image x run time x memory). A run is small only if all five are: fastest
under 5%, smallest under 2%, memory under 8 KB, hypervolume under 2%, best Q
under 2%. A run selected at both widths (--widths 8,4) is small only if its fastest at 32 bits
is under 5% too - a gain on a new objective counts, as Iteration 188 meant for any (proposed at
Iteration 375, **confirmed by the owner at 376**; compare-fronts.py's 32-bit section gives the verdict
at both widths; "Judging the runs" prints the five). Weigh, do not lock out (the owner, Iteration 188): a run
that moves the front's middle - +1% size for -25% time - is not small. The comparison measures every design on
two CPUs; since Iteration 389 (the owner) a design's speed there, and so the verdict, is the geometric mean of
the two, where it had been the first CPU's alone (results/verdict-audit-388.md). Two small runs in a row: stop - the gene set has converged - until
new genes exist; new genes start the count afresh. (How the rule came about:
results/weighing.md and PROGRESS.md; the section as it stood before:
results/drafts/goals-snapshots.md.)

## Conventions

- **Each handoff's last commit is titled `Iteration N: ...`**, N counting
  handoffs, not commits - from Iteration 1 (the handoffs before it were not
  numbered).
- **The bundle**: `tools/make-bundle.sh DIR` runs `tools/handoff-check.py`, then
  names the bundle `forth-vm-evolution-claude-iterN-YYYYMMDD-HHMMSS.bundle` (UTC,
  N from HEAD's subject), with HEAD and master, and checks that it clones to the
  same HEAD. `--checkpoint` skips the check and names it `...-checkpoint.bundle`:
  a safety copy mid-work, not a starting point (Iteration 272).
- **Every commit builds and passes `tools/run-tests.sh`.**
- **Where things are written** (Iteration 275): the present - the state, the
  routine, the open items - in HANDOFF.md, kept current; the past in
  PROGRESS.md, append-only; this file holds what changes rarely - the aim, the
  measures, the conventions, the owner's later plans and the register; every
  document is listed in README.md's index, every result in results/README.md.
  A fact lives in one of them; the others point to it.

## When the improvements are done (the owner, Iteration 536)

"Once the improvements are done" (the Tegra session, below) means this - three steps, in order:

1. **The stopping rule** (revised at Iteration 539 by results/drafts/ask-front-stats-answers-538.md). Judged on each
   run's true front by **its fixed-reference hypervolume** - lab/evolve/hv.py, in the box lab/evolve/hv-bounds.json
   fixed before seed 74 (speed and the 32-bit speed on a log scale): one number a run, comparable from run to run
   because the box never moves. With two or three runs no significance test can decide anything (the smallest two-sided
   p of a rank test is 0.100 for three runs against three), so the rule uses **effect sizes decided now**: a run gains
   when its hypervolume beats the best earlier run's on the method by 1% or more, or an extreme does by its threshold -
   speed 2%, binary + image 1%, memory 4 KB (8 KB from seed 95 - the owner, Iteration 702, and for the roles from 708: one page was the noise of a
   design measured again, results/drafts/memory-noise-702.py; the runs before keep 4), the 32-bit speed 2%. **Stop when, after at least three runs on an
   unchanged method** (the same workloads, selection, operators, gates and box; the hours too until Iteration 562), **the last two runs gain
   nothing**, with no open correctness issue. A method change restarts the count. Report each run's values and the
   spread; no p-values. The series starts at seed 73, the first run with memory measured right since 70. **From seed 77**
   (the owner, 555-556) a new series: 12 hours; every freeze that still has code lifted (evolve.py's FROZEN keeps only the
   retired); the four extremes from every alive design, the hypervolume on the true front as before - seed 76's dominance
   chain hid its fastest designs (results/evolve-amd-ryzen-7-pro-8840hs-seed76.md). **From Iteration 562** (the owner: the hours
   vary with his days) the hours are no part of the method: each run ends by its hours and is judged **at its last
   generation, against each earlier run at that same generation** - the thresholds adjusted to the run's length by the
   earlier run's own record (its curve in the ledger, every 5 generations); an earlier run shorter than this one is
   taken at its end. The series from seed 77 (its method as above): seeds 77 (12 h) and 78 (9 h) its first two.
2. **The confirmation run.** One run of the same method and hours **from the final front** - without `noevolved`, the
   earlier runs' true fronts among the founders - with **every frozen gene that still has code re-enabled** (lifted from seed 77 already - 556)
   (alignhot, msc, scale, sharedcall; the frozen-at-1 genes - bytehdr, doesfar, thinhdr, varcall, bss, lean - free to
   take 0). The retired genes (tail, tailpn, kstack, jithelp, jitre, nocase: their code removed) stay retired unless
   this run shows their region matters. **Confirmed** when its true front's hypervolume is not 1% above the pooled true
   front of the method's last runs (the same box) and no extreme gains by its threshold. Each re-enabled gene screened by
   its enrichment - its share of the run's true front over its share of the children that could carry it: a gene well
   above 1 has its freeze revisited before anything is called final. (The top tenths only as a first look: a gene can
   matter inside the front without reaching one.) Not "the same designs" - a random search never repeats them.
3. **Then the designs are frozen** - **the final set**: the extremes, each re-measured, then designs added one at a
   time by their contribution to the hypervolume in the same box, after merging designs within the tolerances, to five
   or ten; a knee as a candidate, not an oracle (four objectives may have several or none). Consolidation: each
   re-measured alone and under load on the laptop, dream and the Tegra (in two chains - the owner, 579: the laptop
   re-measures every candidate, final-pick.py --shortlist narrows them to about 40, then the laptop again beside dream
   and the Tegra; 242 candidates would take dream about 10 hours and the Tegra days); the genes and code paths no design on the pooled
   true front uses retired (the aim: simplicity; the owner, Iteration 578 - not "no final design": the final set is
   10-15 designs, the pooled front hundreds, and a gene good on it is kept - lose no good gene); every figure the
   article quotes recomputed from the runs' records on the true fronts (results/drafts/front-recheck-528.md: until
   Iteration 532 the reported fronts were mostly not the true ones).
4. **The random-search baseline** (the owner, Iteration 540; results/drafts/ask-related-work-answers-539.md). One run
   of the same hours in which every child is a fresh random genome - random_genome(), uniform over the genome's
   space, the generator the random founders already come from - each evaluated exactly as the method's children
   are (build, checks, every workload, both widths), with nothing learned in the loop: no selection, no surrogate
   screen, no one-round stop (both use what earlier designs showed). Its true front's hypervolume in the same box
   and its extremes, set beside the method's runs, are what the article can say the evolutionary search itself
   contributed - as against the design space alone. One run, reported as values, not a test. It needs a random mode
   in evolve.py - drafted and tested at Iteration 548 (results/drafts/random-mode-548.patch: evolve.py --random,
   `random` in a run's line), applied when consolidation starts.

**The owner's decisions before seed 84 returned (Iteration 573)** - one aim: no potentially useful design or gene filtered
out by a threshold or one noisy number; when unsure, keep it and re-measure it. (Their arithmetic: lab/evolve/confirm.py,
final-set.py --candidates, loadtest.py --ids, xcheck.py --also @FILE.)
- **Step 2, a stricter test besides**: not confirmed either when the run's bred designs, added to the pool, raise its
  hypervolume by 1% or more - the pool's numbers are the best of seven runs' in-run measures, the carried designs re-timed
  once, so the run's own front leans to confirmed.
- **Not confirmed - by where the gain came from**: every gaining design joins the final set's candidates either way. Bred
  designs gained: the search had more to find - another confirmation run, its pool the series and this run. Carried designs
  only (earlier fronts outside the pool, under today's code): the pool widened - no new search. An extreme's gain stands
  only after its re-measure.
- **The genes**: REVISIT (an enrichment of 1.5 or more, 5 or more front designs) - the freeze revisited; KEEP - the other
  value on a candidate, an extreme or a fastest tenth; a gene is a retire candidate only when its other value is on no
  true front of the eight runs, seeds 77-84 - never on one run's absence. The retired genes need a separate experiment.
- **Step 3, the re-measures before the extremes are chosen**: a set of 10, not 5; the candidates - the set, every alive
  design within 5% of the fastest at either width, the 5 smallest and the 5 leanest, the designs merged into the set's -
  each re-measured alone and under load at both widths on the laptop (loadtest.py --ids) and on dream and the Tegra
  (xcheck.py --also @FILE); the whole pooled front kept as the record the article draws on.
- **Step 4**: `seed N 12h widths noevolved random` - the series' own generation 0, nothing carried; a random design on the
  final front joins the candidates.
- **575, seed 84's NOT CONFIRMED** (the fastest and the stricter test, both a ~2% gap at the fast end, the size of the
  session spread): re-measured first, in one session - loadtest.py --ids results/fastend-remeasure-575.md, its fast bred
  designs against its re-timed founders and the pool's fastest (results/drafts/fastend-judge-575.py). The gain stands
  (2% at 64 bits in both readings, or the stricter test on the re-measures 1%): a second confirmation run; else seed 84
  confirmed in effect - the candidates re-measured in full, then the final pick. The random baseline meanwhile (10 hours).
- **The Tegra**: tools/rage-check.sh PASS on fury before the chain after seed 84 (open item 1), or its re-measures see
  1 of the designs clang lets it build (135 of seed 81's 256).

## The portable search (Iterations 602-618)

After the improvement phase, runs without the JIT (`nojit`, 21 hours) for designs that run everywhere - relf's portable
roles - each judged in-run against every portable design found before (lab/evolve/portable.py), then re-measured on the
three machines in a follow-up chain. **It goes on while it makes progress** (the owner, 618): another run after every
follow-up that confirms a gain by the stopping rule's thresholds, in any class, extreme or role; it stops at the first
follow-up that confirms none, and the designs are then frozen as step 3 above freezes them. The detail:
results/drafts/portable-plan-602.md ("After the follow-up", "The search goes on", "Then the freeze"). **Stopped at 621**: seed 87's follow-up confirmed a
gain (611), seed 88's none (results/followup-roles-seed88.md).

## The last JIT run (Iteration 620)

After the portable search ends and before the freeze, one 21-hour run with the JIT (the owner, 620): the one lever the JIT
search never tried, its length (results/audit-nonportable-619.md). Judged as a confirmation run (step 2 above) against
every earlier front, only what it bred counted; continued only on confirmed progress, as the portable search. The detail:
results/drafts/jit-run-plan-620.md. Set at 621: seed 89.

## Later - the owner's plans

1. **The Tegra session - once the improvements are done** (the owner).
   SPN on 32-bit ARM is correct under qemu (Iterations 30-31). Before the
   Tegra can time it: the build makes s8 only from 8-byte images
   (mk-spn-cv8-image.sh; s8-*-32 on an ARM host), and bench-laptop.sh
   skips SPN off x86-64. Then one sitting: tools/arm-qemu-check.sh
   natively, the stage ladder timed, SPN against the interpreter.
   (Iteration 306: the remote checks of the protocol - results/drafts/runner-
   protocol.md - make rage.lan a regular measurement host for the front's designs
   without the JIT; this session stays for the stage ladder and SPN.)
2. **The article - on the backburner** (the owner, Iteration 48):
   `article/`; prompts/14-audience-research before drafting for Habr and
   ForthHub, 04 and 05 before publishing.

## Rejected or deferred - look here first

The scratch trees of the chats of Iterations 213-265 hold no prototype of any of
these (results/drafts/chat-to-iter265/trees/SORTED.md, read in Iteration 277; the directory left the tree at Iteration 541 -
`git show cb05abe20:results/drafts/chat-to-iter265/trees/SORTED.md`).

| approach | what decided it | where |
|---|---|---|
| The internal words' names hidden (headerless), or the words inlined | priced, deferred by the owner (Iterations 222-223; and Iteration 227's guidance: reusable helpers keep their names - only words of no use outside their overlay could go): -2.7 to -2.8% of binary + image on two designs, but a list derived from what programs here write fails the standard suite (coreext.4 builds TRAVERSE-WORDLIST from NEXT-NFA8; LEAVE8 alone crashes a JIT design, reached in a way no source shows) - only hand-kept, reviewed lists per overlay, checked on every gene combination, could be safe; inlining instead saves tens of bytes (the bytes are in the headers) | `results/price-names.md` |
| Dropping the JIT stencils a design never uses | priced, not built (Iteration 238): 50-170 bytes of ~1,000 (0.2-0.5%) | `results/price-stencils-bloom.md` |
| A Bloom filter for names not found | priced, not built (Iteration 238): the lookup is 66% of the smallest design's corpus dispatches, misses half of the walk - but 64 chains (the threads gene) cut three quarters of it for about the same bytes, and evolution declines that at the small end | `results/price-stencils-bloom.md` |
| The JIT translator compiled for size (`jitos`) | priced, proposed as a gene (Iteration 238): -416 to -800 bytes on JIT engines built -O2/-O3, alive; translation speed is the trade | `results/price-stencils-bloom.md` |
| Repeated code factored into headerless shared bodies by the converter (the echo's cheaper cousin) | built: the gene factor, after-seed-47 patch 6 (Iterations 267-268) - 0 off; words below 0.1% or 1% of the reference dispatches, or every word; image bytes on 14 of seed 46's front, mean -52, -96, -133; on the smallest -41, -95, -127 for +0.007%, +0.17%, +1.98% dispatches. 263's 16-byte gap to its price was the hot-word filter, not the safety rules (3 bytes) | results/drafts/factor-plan.md, PROGRESS.md Iterations 263, 267-268 |
| The zero-divisor throw path sharing NOOP's dispatch (DROP's with the cached top) | tried, not kept (Iteration 263): engines -64, -32 and +32 bytes (3bb2087f9d, fe3c9c3940, 3456ac1e5e) - layout noise around a 15-byte saving; -10 still caught | PROGRESS.md Iteration 263 |
| An echo instruction (Fraser 2006: replay n bytes from earlier in the code - LZ77 executed) | priced, the owner's call (Iteration 260): in the smallest design's image, whole instructions with no branch, branch target or return-stack word inside, within a word: 283 bytes at a 3-byte echo (4 KB back), 427 at a 2-byte one (256 back) - 3.3-4.9% of the image, before the engine's handler; a byte-level parse promised 714-886. New instruction semantics in every engine generator, a compression pass in the converter, kept off hot code | `results/missed-options-2026-10.md` |
| Mutation weighted by regime (interpreter-only genes rarer on JIT designs) | priced, not built (Iteration 260): the genes with no effect under the JIT (peel, align1, ipaclone) are ~5% of a JIT design's mutations, JIT designs ~28% of the run's - ~1.4% of evaluations | `results/gene-interactions-seed46.md` |
| VM instruction-pointer update optimisations (Ertl & Paysan, ECOOP 2024: combined increments, immediates at [ip+k], the loop start from the return stack) | deferred (Iteration 260): within a superinstruction GCC already combines the increments; the loop form is the open one - its gain is a dependency chain the laptop must time, on interpreted designs only (the JIT's loops are native) | the research report, item 1.1 |
| Clang, or GCC 16, for musttail and preserve_none | the owner's (Iteration 260): GCC 13.3 on the laptop and the VM has neither; GCC 16.1 has preserve_none for x86. CPython 3.14's gain was 1-5% once Clang 19's computed-goto regression is set aside | `results/missed-options-2026-10.md` |
| JIT code and written data in one cache line or page; section headers in the engine | checked, covered (Iteration 260): the JIT's code is its own mmap'd region; the engines carry no section headers already | - |
| A fast path for cross.4's byte loops (@-T and !-T as the host's @ and ! when the cells match, little-endian) | priced, left (the owner agreed, Iteration 257): the kernel workload's dispatches -37% (interpreted), -9% time on the fastest JIT design, a byte-identical kernel - but it changes the yardstick, not the designs: s6 gains most, every design's kernel ratio moves, and in-run speeds would not compare across it. If the tool should be faster, freeze today's cross.4 as the benchmark's own copy first | `results/drafts/crossfast.md`, `.patch` |
| Repeated instruction sequences factored into helper words | priced, not worth it (Iteration 254): in the smallest design's image (3456ac1e5e), sequences that recur byte for byte - operands and inline strings included, no branch, branch target or return-stack word inside - save 12 bytes after the helpers' own headers and the calls (4 helpers). Matching opcodes alone promised 146: the repeats differ in their literals and messages. The kernel and overlays are already tight | /tmp/factor.py's method, PROGRESS.md Iteration 254 (recovered as found in Iteration 273: results/drafts/chat-to-iter265/scripts/factor.py - its exact-bytes version, behind the 12; the opcode-name version behind 146 was overwritten in place) |
| A fault handler in every engine (flush the output, report, status 70) | measured, the owner's call (Iteration 251): 114 of seed 46's 127 front designs have no handler (the guard gene, 13 have it); they die of a bare SIGSEGV and lose output buffered for a pipe or file. guard costs 256-448 bytes away from the fast end; a minimal handler ~100 (estimated); fsys 4-5's Forth-side buffers lost either way | PROGRESS.md Iteration 251 |
| Dropping the engine's stack-permissions header (PT_GNU_STACK) | captured, left (the owner, Iteration 251): the smallest engine's file is code and data but 176 bytes of ELF headers; without the second program header the kernel makes the stack - and with READ_IMPLIES_EXEC every mapping - executable: 56 bytes (0.35% of the smallest design) for a weaker process. **The premise checked (Iteration 712): wrong on x86-64 since Linux 5.8** - a missing header is exec-none there (the stack stays rw-, no READ_IMPLIES_EXEC; measured on 6.18), still exec-all on i386 and 32-bit ARM; the smallest engine relinked with one segment: -48 bytes, the same on every 8-byte engine (a constant, no ranking moves) - the owner's call, reopened | Iteration 250's summary; `results/drafts/literature-712.md`; `readelf -l` on 3456ac1e5e's engine |
| A compressed image and engine (decompressed at start-up) | priced, captured, not built (the owner, Iteration 236): on disk only - the code must be decompressed to run, so memory does not shrink (it grows by the compressed copy while it unpacks) and every start pays the decompression. A tiny LZSS (12-bit offsets, a ~150-300-byte decompressor) on the smallest of all runs: image 8,704 -> 6,659 bytes, engine 7,680 -> 4,605 - about -4.5 KB of 16.4 KB after the decompressor; deflate or xz pack tighter (image 5,639 / 5,456) but their decompressors (KBs) eat the gain. The question before building: should the size objective count bytes on disk at all if they are not the bytes that run - it would reward a packing trick over a smaller VM | this register |
| Packed names (6 bits a character) | priced, plan written, deferred by the owner (Iterations 222, 231-233): the image's names take ~300-380 bytes fewer (-311 on the smallest, -292 middle, -384 fastest) before ~100-150 bytes of pack/unpack code - about 1-1.5% of binary + image at the small end, as a gene. Plan: a fixed 63-character alphabet (A-Z, 0-9 and the 22 punctuation characters the front uses, a few spares); a name packs only if every byte is in it, else stays raw (lowercase, UTF-8) - one stored form per name, so lookups compare stored forms; the hash on the plain name (threads unchanged); NAME>STRING unpacks into two alternating buffers; the converter packs the image. UTF-8 names gain nothing under it; a second, Cyrillic table chosen per name would store a letter in 6 bits instead of 16 (an 8-letter name 16 -> 6 bytes, ~60% less; 31 letters fit) - in a program's own dictionary, not the evolved image; CJK has no small table. The count byte after the name (Iteration 232) means >NAME no longer cares what name bytes hold | `results/price-names.md` |
| The next keeping forms (OVER C@, DUP C@, ...) | priced again, not built (Iteration 222): the largest, DUP before ?BRANCH (5-6% of the small end's image dispatches), already has its form, listed by 121 of seed 43's front and realised by 28 - the small end is short of one-byte codes, and new forms would queue for them | `results/price-keepforms-next.md` |
| Packed names, six bits a character | priced, not built (Iteration 222): -292 to -384 bytes before the code to pack and unpack, a kernel change and a reseed; hiding the internal words' names saves more for less | `results/price-names.md` |
| A name-lookup cache beside the threads gene | priced, not built (Iteration 221): at 16 chains a 16-entry cache cuts the walk 22% (corpus) and 48% (parse); doubling the chains halves it, for bytes evolution already declined at the small end; half the walk is names not found, which a cache cannot serve | `results/price-lookup-cache.md` |
| Native code calling byte code (SPN's st_interp, GENES.md candidate 5) | priced again, not built (Iteration 220): since jitx the words it would free hold 9.3% of the kernel workload's dispatches, 4.1% of the corpus's, ~0 elsewhere, and they would cross back to byte code every 3-4 operations | `results/price-jit-interp.md` |
| Stack state in the JIT's translator (cells in registers across stencils) | priced, deferred (Iterations 218-219): -27% instructions with free renames, but the fixed-register form (+1.4 KB at K=2) saves few, and on the VM neither is reliably faster at eight code placements - only the loop index in registers is (-40%, the loop workload alone); the laptop's `jitstack-inner-sweep.sh` decides | `results/price-jit-stack.md` |
| fsys 5 copying lines out a cell at a time (FS-MOVE) | priced, not built (Iteration 214): where CMOVE has no opcode, kernel -28% and corpus -17% of fsys 5's dispatches; where it has one, +2.2% to +11.7% and +0.8% to +6.5% - evolution can give CMOVE its opcode instead | `results/drafts/fsys/single-syscall.md` |
| Variables and constants compiled as literals in code compiled at run time (`rtlit`) | built and measured, rejected (Iteration 59): correct, and the held-out sieve 0.811 of its dispatches - but kernel 0.984 and corpus 1.016, because a COMPILE,8 link that checks every compiled word costs a compiling workload more than it saves; 132 bytes more; selected geomean 1.000. **To be priced again (677)**: the code it shrinks now counts in the size | PROGRESS.md, Iteration 59; results/drafts/search-reopen-plan-677.md |
| A `DOES> @` word's fetch compiled as one VAR@ (relf's Iteration 260; step 2 of the reopened search, mechanism 3) | priced, not built (Iteration 684): none of the seven programs defines a `DOES> @` word - the four have no DOES> word at all, brainless's 179 uses of DOES> children are other bodies - so 0 bytes and 0 dispatches on the selection and on the held-out three (results/mech-prices-684.md). Iteration 685: relf's own code has 118 such words (BUFFER:), and relf's shellmix.fth takes 3.0 % of its dispatches out with it on the knee - it stands or falls with shellmix in the selection (results/relf-reply-685.md) - in it since 686 (the owner), so **back to step 3's candidates** | results/shellmix-686.md |
| Address literals in 5 bytes instead of 9 at 8-byte cells (relf's, its dictionary below 4 GB; mechanism 8 of the reopened search) | priced, deferred (Iteration 686, the owner: drop nothing that limits a general Forth): **no word is dropped and nothing is limited** - TO, VALUE, 2VALUE, ['] and LITERAL stay, the ANS suite checks them; the lab's 9-byte form reaches any address, so it is the more general one, and only its length is at stake: 4 bytes a literal, 4 B on the selection, 1,220 B on brainless's TO, none in relf's code. Built when a selection program leans on TO or ['] | results/shellmix-686.md |
| The text interpreter's words (PARSE, WORD, FIND, >NUMBER) called from the JIT's native code through the cold-word helper, so their callers stay native (shellmix on the JIT designs) | rejected (Iteration 692): shellmix 1.152 on fastest-x86-64, 1.114 on best-all-round, the apps workload 1.07 and 1.04 - a nested interpreter at every call costs more than the interpreted chain; native code for the parsing operations is what would help | results/jit-shellmix-692.md |
| The loop opcodes in code compiled at run time | priced, not built (Iteration 28): 0.1% of kernel's dispatches, 0.8-1% of corpus's, none on fib or parse; 68-70% of the held-out loop's, which building it for would spoil | `results/price-runtime-loops.md` |
| A reach check for far calls in cv8.4 | measured, not built (Iteration 28): the workloads run code up to 68 KB, the far form reaches 2 MB (one-byte calls) to 4 MB; a check costs every image bytes | `results/price-runtime-loops.md` |
| Indirect threading as a gene | priced, not built (Iteration 29): in the dispatch lab its dispatch lands in token and direct threading's band; its code is a cell a reference, beside s0-cell's 25 KB - dominated | `lab/dispatch/README.md` |
| One-byte calls in the pairs' slots | priced, not built (Iteration 13): the pairs with the fewest static sites are among the hottest - four of them carry 3-8% of the dispatches, for 24-120 bytes; the far-call prefix band costs no slot | `results/price-hotcalls-seed3-front.md` |
| Native code in the genome: relf's native compiler as a family of its own, or our SPN with relf's rules as genes | deferred by the user (Iteration 4) after measuring it (Iteration 3): our corpus byte for byte, our kernel workload a segmentation fault in cross.4's RESOLVE, 3-10 times faster than s6 on the VM | PROGRESS.md, Iterations 3 and 4 |
| Profile-guided optimisation of the engine as a gene | measured, not built (Iteration 7): 0.903 on s6 only when trained on the measured workloads; trained on a separate program, 0.980 - what -fprofile-use's flags give without a profile; three of those flags became genes instead | `lab/evolve/GENES.md`; `lab/evolve/pgo-train.fth` |
| A second escape level - nine more primitives behind ESC for nine slots | built, measured, does not pay (Iteration 11): with the design's own best pairs in the slots, 0.2-2.4% fewer dispatches - price.py's 6.4-12.9% counted overlapping pairs; kept as a gene for selection | `lab/evolve/GENES.md` |
| Triples - three operations as one opcode | priced, not built (Iteration 8): at most 0-4.9% of dispatches on the front, none on fib, before overlaps and slots - tests before branches came out larger | `lab/evolve/GENES.md`; `lab/evolve/price.py` |
| Load-time direct threading (a decode cache invalidated on every store) | deferred, not built: the dispatch lab gave direct over token threading -5% fib, -12% sieve, but +9% loop; relf S8 found dispatch already at the indirect-jump rate | `lab/evolve/GENES.md` 1; `lab/dispatch/README.md` |
| Run-time fusion of pairs (`rtfuse`) | built, kept as a gene, selection rejects it: +560-576 bytes, s6 with two pairs 0.956 -> 0.970 (VM) | 53017b4; `lab/evolve/README.md` phase 2b |
| READ/WRITE stencils making the system call themselves | not built: they would bypass the engine's buffers (`t_obuf`, `t_ibuf`) | 973435c; `FINDINGS-SPN.md` |
| ACCEPT with READ stopping only at LF and CR, every byte examined in Forth | built, 3-11% SLOWER, replaced by READ stopping at every special character | e223d8e; `FINDINGS-OUTER-INTERPRETER.md` |
| @XT, a fused @ EXECUTE | not built: no `@ EXECUTE` in the image's code | 93849f3 |
| Multi-state caching with 25 operations specified | built, lost (s6 1.049, s5 1.110, VM): the normaliser's second dispatch; kept with 72 operations and composed pairs | 28dc163, 4512665 |
| A retry for "transient" conversion failures | added on a wrong diagnosis, removed: the cause was the raw genome built under the canonical identity | 9d46ba3 -> 679e6f3 |
| "Multi-state caching buys less on Zen 4" | an inference from 8 re-measured designs, retracted: every design on the Ryzen's front has it | 679e6f3; `lab/evolve/REHEARSAL.md` |
| Two top-of-stack registers always; real calls and returns for dispatch | lost in the dispatch lab (before this register) | `lab/dispatch/README.md` |
| The JIT header's 4-byte field elsewhere (mechanism 9, from TRIZ's separations: the length found at an end-EXIT `;8` compiles; the offset in a side table beside the JIT's code, or written into the translated word's dead bytecode) | priced, not built (Iteration 706): -700 B of the five programs' code (175 definitions; -2,732 on the held-out three) for +95-152 engine bytes and up to +8 KB (the table) or a second code's handler (the dead body: no table; not where (ABORT")'s resume point lies in the first 4 bytes) - about -1.8 % on the smallest JIT design; **V1' built (Iteration 710) as the gene jitdead** - the length by the converter's end rule, not an end-EXIT; the offset over the dead first four bytes, what is read there copied out; -693 to -741 B of the programs' code, the total -0.3 to -2.9 % on ten JIT designs, instructions the same or fewer; queued for after the roles (results/applied-genes-727) | `results/drafts/triz-706.md`; `results/drafts/jitdead-710.md` |
| No JIT header at all (eager translation at `;`, or a native form at each call site) | rejected by analysis (Iteration 706): a word reached from bytecode needs a trigger - a check on every call, or 5 bytes at every call site | `results/drafts/triz-706.md` |
| The run-time fusers (rtvar, rtconst, rtinline) in the engine's C instead of the overlays | not pursued (Iteration 706, TRIZ's separation by system level): the plan keeps run-time mechanisms in the overlays the translator and the self-hosting compiler share | `results/drafts/search-reopen-plan-677.md` ("What stays") |
| A size superoptimizer on the selection programs' code (peephole rules: runs of 2-3 words, their shortest equivalent of the kernel's words) | measured, not built (Iteration 707): at most 11 bytes of the five programs' code - less than a peephole's own overlay code; the programs are idiomatic | `results/drafts/superopt-707.txt` |
| New mechanisms from the genes' interactions in a run's records | measured (Iteration 707): the raw interactions are the JIT family's trade; the clean quartets (one design, two genes, all four cells) exist for 5 pairs, their medians about 0 - no synergy to fuse | `results/drafts/epistasis-707.txt` |
| A build-time perfect hash of the image's names | not priced (Iteration 707, the morphological box): its table, about 2 bytes a name, costs more than the 64 chains the small end declines | `results/drafts/ideation-707.md` |
| The image's names in their chains by use (most-used first; the use learned from the held-out programs) | priced, not built (Iteration 707): zero bytes - **mispriced** (Iteration 710: every front design has byte headers, whose links are unsigned backward distances; by use needs signed links, +19 to +73 B of links on six designs, and the engine's walk, the Forth walkers, HEADER and the self-hosting compiler change; a prototype to count instructions first); the lookup's walk 43-49 % shorter on parse, 26-35 % on compiling the five programs, 6-9 % on the corpus - **to build as a gene after the roles** (the owner, Iteration 708: the search reopens; the converter relinks, the newer of a twice-defined name first; its speed by the profiler's dispatches) | `results/drafts/chain-order-707.txt` |
| The runtime's system calls as unified stubs (dietlibc: the number in rax, one shared tail) | built (Iteration 709, the sweep): clang's x86-64 engines -176 to -400 bytes; for GCC lost - its LTO inlines the C wrappers, and the stubs' calls grew its large -O2 engines by 64-192 bytes - so GCC keeps them (`#if defined(__clang__)`) | `results/applied-after-seed96/sysstubs-after-seed96.patch`; `results/drafts/sweep-709.md` |
| The engine's refusals of an image as one message with a check digit (`not a RelF image (N)`) | built (Iteration 709, the sweep): -226 to -458 bytes on every design at 8-byte cells, -234 to -336 at 4; the seven texts were 374 of the smallest engine's 1,072 bytes of rodata - a user-visible change, the owner told | `results/applied-after-seed96/imagemsg-after-seed96.patch`; `results/drafts/sweep-709.md` |
| The kernel's largest words shortened by hand (NUMBER?'s three prefix tests as a range test and a table) | priced, not built (Iteration 709): about 18 bytes, the largest found - tens of bytes a word, each through the kernel's seeds and the self-hosting gate | `results/drafts/sweep-709.md` |
| The JIT's image-word ends table two bytes a number (jit_wends: every end under 64 KB) | built (Iteration 710, found building jitdead): -1,096 to -1,176 B on every jitx engine at both widths (2,568 B of 5-6 KB of rodata); the self-hosting compiler writes it so too | `results/applied-after-seed96/wends16-after-seed96.patch`; `results/drafts/jitdead-710.md` |
| A model of the time from the PMU's counters (Architect Labs' Arcmodel: a function over counters fitted to the truth within 5 %) | built as data, not yet fitted (Iteration 711): cputime reads mispredictions and last-level misses beside instructions and cycles; records and chain B's lines keep them; lab/evolve/countfit.py fits and judges - after chain B, whether one run's counts can screen without rounds | `results/applied-after-seed96/counters-after-seed96.patch`; `results/drafts/frostbite-711.md` |
| More held out, by group (Frostbite: five groups, each split into search and held-out sets) | proposed (Iteration 711; the owner's call, for the reopened search): on the screen's pool the interpreted end's top 20 % by the search set sit at the held-out pair's 40th percentile, about a fifth of their advantage carried (the JIT's about half); recursion and programs have no held-out workload | `results/drafts/frostbite-711.md`; `results/drafts/heldout-711.txt` |
| Frostbite's architecture (interaction nets, tiles, work stealing, fine clock gating) for a VM | not taken (Iteration 711): explicit dependencies are a stack VM's code already (the JIT's stack caching: priced, 218-219), single use is Forth's stack; the rest is multicore hardware | `results/drafts/frostbite-711.md` |
| The counters model with the machine's penalties shared (the interval model: Karkhanis and Smith 2004, Eyerman et al. 2009 - time as a base plus miss events at the core's cost) | proposed (Iteration 712): countfit's per-workload fit beside one with the misprediction and miss costs shared across workloads and designs on a machine, the base per workload and regime (JIT or not); a fitted penalty checkable against the core's | `results/drafts/literature-712.md` |
| Zen 4's top-down metrics in counters.py (perf -M PipelineL1,PipelineL2: retiring, bad speculation, frontend, backend, SMT contention) | proposed (Iteration 712): answers counters.py's own question (mispredicted dispatch or the IP chain) in slots; the laptop's | `results/drafts/literature-712.md` |
| The roles' build-level spread before they are named (Kalibera and Jones, ISMM 2013: repeat at the level that carries the variance) | proposed (Iteration 712): each role is one build, and rounds cannot see its layout luck (5-10 % on the stages, layout-noise.sh); within the spread, a band | `results/drafts/literature-712.md` |
| Gforth 1.0 in the comparisons (the IP-update work in a release; on par with SwiftForth) | proposed (Iteration 712): genapps' row and the article use gforth-fast 0.7.3 (apt, 2014); 1.0 built from source on the laptop | `results/drafts/literature-712.md` |
| Pulley's dispatch data, identical code folding, ELF header overlays, Zen 4's branch-target capacity | checked, nothing for us (Iteration 712): match against tail-call dispatch goes either way (the tail gene); our handlers are labels, not functions; overlays save 8 bytes, fragile; our dispatch sites fit | `results/drafts/literature-712.md` |
| The engine's writable data in a fixed layout (the 8-bit games' hand-placed RAM): every small variable a run touches in one block, the big buffers after; the stack tops on one page (the return stack growing up, the 6502 Forths' layout) apart | **step 1 built (Iteration 734; results/drafts/data-layout-734.txt)** - engine/data-layout.ld: the small variables on one page of their own, the tables and the buffers used from their start after them; the ten roles' memory 8-36 KB less on nine, least-memory the same, no byte of engine or instruction moved. **Step 2 built and queued (Iteration 738; results/drafts/data-layout2-738.txt, results/queued-layout2 - applied when the series ends, since it changes the memory reading)**: the stacks' chunk 1 KB longer on the return stack's side, first in .bss.hot, so the return stack's top shares the small variables' page (not the return stack growing up: both floors and the guards stay page-aligned); the record's memory 0-8 KB less on the ten roles (smallest 104 -> 96), about a fault fewer a workload over 31 runs, every trap the same, no x86 byte, +4 B on every 32-bit ARM engine. Measured, proposed (Iteration 713): memory is pages faulted, and the linker's order moves it 1-4 pages either way (-Wl,--sort-section=alignment: c7c35f9c97 32 -> 28 at start-up, 21768033b7 16 -> 14, fb0d57c8a2 15 -> 17; medians of 15) - the 8 KB rule's size; a start-up touches 4 BSS pages where 2-3 would do; a prototype for the reopened search, step 1 (the small variables) the safe half | `results/drafts/early-games-713.md` |
| The JIT's compiled code bounded on the data stack (the interpreter checks dsp against g_dsp_limit; JIT code does not) | found, the owner's call (Iteration 738, the same before and after step 2): on the JIT roles without the guard gene (small-jit, fastest-x86-32, fastest-x86-64) a runaway push runs down through the whole engine - one RWE segment, its code and the fault handler included - and dies 139 with nothing on stderr, buffered output lost (Iteration 151's symptom, for JIT code alone); best-all-round (JIT and guard) reports it. Ways: the guard gene on those roles (256-448 B, Iteration 251), one PROT_NONE page below the data stack for JIT designs, a dsp check on the JIT's loop back-edges, or leave it. **Priced (Iteration 739)**: native recursion in JIT code dies the same way (the handler has no stack); the guard gene on the three fixes both, names each trap, +144-408 B, memory +4-8 KB at 8-byte cells, the interpreted part 6-8 % fewer instructions - challengers 7a6c182638, b7a09aec76, fba7d5be3d for the roles' follow-up after the series; slim (one page, the handler's own stack) +112-208 B, a draft patch; the back-edge check not built (time in JIT code for what guard gives free). The challengers' records ready (740: results/candidates-guard-740.md, their path rehearsed - results/drafts/guard-challengers-740.sh) | `results/drafts/data-layout2-738.txt`, `results/drafts/jit-guard-739.txt` |
| The 32-bit ARM engines in Thumb-2 (-mthumb; embedded toolchains' size practice) | **built as a gene, queued (Iteration 742; results/drafts/thumb-742.txt, results/queued-thumb)**: every ARM engine is A32 - clang's cross build by default and the Tegra's GCC 16 too (its 726 engines 16,782, 13,014, 11,158 B are the A32 builds' sizes, Thumb-2's 12,506, 9,754, 8,410), so the ARMv7 comparisons were never confounded; Thumb-2 makes the six ARM roles' engines 25-31 % smaller (smallest 6,100 -> 4,440 B), every build alive and the reference's under qemu. The gene `thumb` (HELD: never bred; x86 builds and every id unchanged) for the series' end; the Tegra's speed decides - **the owner's**: ship it or not | `results/drafts/thumb-742.txt`, `results/queued-thumb/ORDER.md` |
| LLVM's machine outliner (-mllvm -enable-machine-outliner) | priced (Iteration 742): the clang designs' x86-64 engines 0 to -3.1 % (portable-fastest -512 B, fastest-x86-64 -752, smallest 0), alive; the outlined sequences become calls, so speed likely pays - a compiler-flag gene for a later search, not built | `results/drafts/thumb-742.txt` |
| Small VMs' and interpretable compression's techniques (Java Card's token linking, HP's RPL, PostScript's binary tokens and early binding, MicroPython's frozen bytecode, eLua's rotables and NodeMCU's flash store; Proebsting's superoperators, BRISC, Evans and Fraser's grammar rewriting) | checked (Iteration 742, the owner's idea): each here already, priced, or changing the measure. Two paper candidates for a later search: the tag's t2tab and t2esc as const data (eLua's rotables: ~one written page fewer for 4 KB more in the file - DISPOFF's inverse, for memory-first designs); a learned grammar over the bytecode (Evans and Fraser: the image and the programs' code are ~80 % of the smallest's bytes; xz reaches 62-64 % of the images - a ceiling no interpretable code meets; the echo instruction's family, 260) | `results/drafts/small-vms-742.md` |
| Memory measured with a fixed environment (PATH, padded with the arguments to 1,024 bytes) | built, queued (Iteration 713; the owner: "let's do it"): the reading carried the measuring process's environment, a page per ~4 KB (the sandbox's 17 KB: +3 pages) - a likely reason the sandbox read holders 4-16 KB above the laptop; fixed, fb0d57c8a2 reads 15 / 27 pages whatever the caller's (before 19 / 31, 24 / 36); with the reopened search's series | `results/applied-genes-727/fixenv-after-seed96.patch`; `results/drafts/fixenv-713.md` |
| Short branches (the Z-machine's 1-byte branch form, the 6502's rel8) | priced, not proposed (Iteration 713): IF THEN is 3 bytes; ~150 branch words in kernel.4, ~106 in the five programs; the converter could choose exactly, the one-pass run-time compiler only backward branches (a forward IF's body would move, its relative calls with it) - about 150 bytes (0.7 % of the smallest) for two primary-band opcodes and the encoding in the seven places 681 touched | `results/drafts/early-games-713.md` |
| The early games' techniques (Starflight, Another World, Elite, SWEET16, UCSD p-code, the Z-machine, Pitfall!, Wolfenstein 3D) | checked (Iteration 713, the owner's idea): each one here already - threading, headerless names (deferred), the k genes, short literals, packed names (deferred), DISPOFF, the JIT and fusers, the tail genes, a compressed image (not built); a CASE table has nothing to take (CASE hardly used) | `results/drafts/early-games-713.md` |
| The JIT translator's arrays short first (`jitfew`; the early linkers' shared areas, Denning's working set) | built, queued (Iteration 713): jit_body's arrays 128 operations long, 1,024 only for a longer word - their heads were a page each at every callee depth; eight JIT designs' memory -5 to -16 pages (-11 to -23 %), engines +224 to +544 bytes, outputs alike - a gene, the trade the search's | `results/drafts/early-computers-713.md`, `results/applied-genes-727/jitfew-after-seed96.patch` |
| The JIT's operation cap lowered (JIT_MAXOPS 256 or 128) | priced, not proposed (Iteration 713): memory -9 to -17 pages, engines 0 or -64 bytes, but a word past the cap stays bytecode - Iteration 488 raised it to 1,024 for the apps' long words; jitfew has the pages without that | `results/drafts/early-computers-713.md` |
| FILL 0 by demand-zero pages (madvise DONTNEED; VAX/VMS's demand zeroing) | priced, not proposed (Iteration 713): cross.4's 40,000-byte IMAGE FILL is 2-3 of the kernel workload's pages - the metacompile writes most of IMAGE anyway; FILL is memset, the time in the noise; a system call and a range check for 8-12 KB on one workload | `results/drafts/early-computers-713.md` |
| The image mapped from its file, copied on write (Multics' shared segments) | priced by estimate, not built (Iteration 713): images are three pages; at most 1-2 a design, and a page-aligned image format | `results/drafts/early-computers-713.md` |
| Engines without stack-clash probes (-fno-stack-clash-protection) | priced (Iteration 713): no probe loop in these engines (load_image's frame went static at 228); pages within 2, bytes 0 to -32 - not proposed | `results/drafts/early-computers-713.md` |
| The early computers' techniques (Mesa's statistical byte code, Smalltalk-80's operand groups and special selectors, the Transputer's prefixes, BCPL's INTCODE, the B5000's stack registers, SOAP's placement, the AGC's interpreter, overlays, program restructuring) | checked (Iteration 713, the owner's idea): each here already - short literals, one-byte codes by use, literal and call widths, short branches (priced), the tos and caching genes, alignhot and the handler order, the interpreted trade itself; text order moves few faults (fault-around) - the data's layout is where order counts (fixed layout, proposed) | `results/drafts/early-computers-713.md` |
| Literals converted before the lookup (FALSE's and Brainfuck's first-character dispatch): a token of the form -?[0-9]+ taken by >NUMBER first while no name has that form (the converter checks the image, the header word sets a flag) | **built: the gene numfirst (Iteration 733; results/drafts/numfirst-733.txt)** - two forms, the engine's (FIND) with klookup, INTERPRET8 without; the ten roles' outputs the same, the corpus's instructions 0.756-0.999 of off, parse 0.683-0.994, +55-106 B; not yet self-hosted. Priced (Iteration 717): literals are 28.6 % of the corpus's tokens and 93 % of its misses, 50 % of parse's (all its misses), 7.4 % of the kernel workload's, 10.8 % of the apps' - about half the corpus's and parse's walk, on the order of a third of their dispatches on an interpreted 16-chain design, for a few tens of bytes (238's Bloom filter: ~350 bytes for about as much); for the reopened search, the owner's call | `results/drafts/esolangs-717.md` |
| The demoscene's and the IOCCC's techniques (crinkler's compression, import by hash and transforms, Teensy ELF and smol, sizecoding's tables made at start-up; IOCCC buzzard.2's FIRST/THIRD, 1996 august's compressed byte code, OTCC, SUBLEQ in 366 bytes, ncw3's Forth in the preprocessor) | checked (Iteration 727, the owner's idea): each one here already or not for an interpreter measured by dispatches, bytes and pages - compression (236, 260), headers (251, 712), offset tables (237); one new candidate, the hash seed below | `results/drafts/demoscene-ioccc-727.md` |
| The image's names stored as hashes (crinkler's import by hash) | rejected on paper (Iteration 727): FIND must be exact - at 16 bits a miss matches one of ~314 names once in ~200; at 32 bits little saved over 5-6-character names, and WORDS' and SEE's names lost; packed names (222) are the exact form | `results/drafts/demoscene-ioccc-727.md` |
| The chain hash's seed searched per image (crinkler's per-program brute force): ((v*K) & 0xFFFF) >> (16 - log2 chains), K chosen on the held-out programs | **built: the gene hashk (Iteration 730; the self-hosting compiler 731)** - one K, ((v * 18835) >> 8) & (chains - 1); on, the ten roles' outputs the same, the corpus's instructions 0.914-0.994 of off, parse's 0.833-1.000, the engine +0-32 B (results/drafts/hashk-gene-729.txt); off, every byte as before. Priced first (Iteration 727): entries visited a lookup, out of sample - alone -5 to -15 % on the corpus, -4 to -47 % on parse, -6 to -18 % on the five programs; with chainorder -7 to -34 %, -51 to -61 %, -29 to -40 %; a multiply and a shift, K two bytes; measured on a prototype (728): the smallest (Forth walk, 16 chains) -9.0 % of the corpus's instructions, -17.5 % of parse's, the image -16 B; portable-fastest (C walk) -3.6 %, -3.2 %, +8 B - to be built as a gene with one K for every design - ((v * 18835) >> 8) & (chains - 1), the ten roles -11 to -24 % of the corpus's visits (hashk-table-728.txt); chainorder priced from it at -21.6 % (smallest) and -7.4 % on parse, above hashk, the corpus not readable from the model; over hashk as built (731, chainorder-margin-731.txt) the ten roles' visits corpus -6 to -10 %, parse -26 to -41 %, the five programs -18 to -34 % - **built (Iteration 732), a converter-only gene**: forward links their own three-byte form, the held-out programs' 64-times names first; the ten roles' corpus 0.987-1.031 of the instructions, parse 0.79-0.99, +56-120 B (chainorder-732.txt) - the evolution's to take or leave; its self-hosting part when a role takes it | `results/drafts/demoscene-ioccc-727.md` |
| The kernel's messages as THROW codes (FALSE: no error messages) | priced, the owner's call (Iteration 717): 211 bytes of text in kernel.4 (11 ABORT"s, 6 ."s), 50 in coreext.4 - at most ~200 bytes, 0.9 % of the smallest; user-visible and in the workloads' reference outputs | `results/drafts/esolangs-717.md` |
| The esoteric languages' techniques (FALSE, the Brainfuck optimisers' contraction, clear, copy, multiply and scan loops, offsets and speculative execution; befunjit's static paths and invalidation, ff3's per-direction dispatch, bef2c, Funge-98's fingerprints; the golfing languages' dictionaries; sectorforth's eight primitives; Joy's combinators; Befunge's `#` skip) | checked (Iteration 717, the owner's idea): each here already or priced - folds and rtimm, multi-state caching, the trigger byte, dead words, rtvar's slots, ops10 and escape, packed names; the one-word IF skip a third of 713's short branches (~50 bytes) - except literals before the lookup (above) | `results/drafts/esolangs-717.md` |
