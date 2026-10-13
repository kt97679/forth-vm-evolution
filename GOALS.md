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
  extension uses belongs in that extension (results/word-audit.md).
- **speed**: median CPU time against the hand-made s6, the geometric mean over
  the selection workloads - kernel, fib, corpus, loop, bubble (300 cells),
  ackermann (A(3,5)); parse and sieve held out (Iterations 100, 127-128). The
  gate before any timing: the corpus (661 cases) and the kernel workload
  byte-identical to the reference.
- **memory**: the pages a run touches (cputime's MINFLT times the page size),
  each workload's median over the rounds, the largest the design's. **Within
  8 KB is a tie** (Iteration 77): designs differ by a few pages; a JIT's buffer
  or a leak, tens of KB, still decides.

**Judging a run, and when to stop** (Iterations 78, 188-189): each run against
all the others, measured again in one session - its fastest, smallest and
least-memory designs, the hypervolume in log space, and the best Q (binary +
image x run time x memory). A run is small only if all five are: fastest
under 5%, smallest under 2%, memory under 8 KB, hypervolume under 2%, best Q
under 2%. Two small runs in a row: stop - the gene set has converged - until
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

## Later - the owner's plans

1. **The Tegra session - once the improvements are done** (the owner).
   SPN on 32-bit ARM is correct under qemu (Iterations 30-31). Before the
   Tegra can time it: the build makes s8 only from 8-byte images
   (mk-spn-cv8-image.sh; s8-*-32 on an ARM host), and bench-laptop.sh
   skips SPN off x86-64. Then one sitting: tools/arm-qemu-check.sh
   natively, the stage ladder timed, SPN against the interpreter.
2. **The article - on the backburner** (the owner, Iteration 48):
   `article/`; prompts/14-audience-research before drafting for Habr and
   ForthHub, 04 and 05 before publishing.

## Rejected or deferred - look here first

Prototype code for some of these may exist only in the scratch trees of the
chats of Iterations 213-265: results/drafts/chat-to-iter265/trees/SORTED.md lists
the ten whose work never reached master.

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
| Dropping the engine's stack-permissions header (PT_GNU_STACK) | captured, left (the owner, Iteration 251): the smallest engine's file is code and data but 176 bytes of ELF headers; without the second program header the kernel makes the stack - and with READ_IMPLIES_EXEC every mapping - executable: 56 bytes (0.35% of the smallest design) for a weaker process | Iteration 250's summary; `readelf -l` on 3456ac1e5e's engine |
| A compressed image and engine (decompressed at start-up) | priced, captured, not built (the owner, Iteration 236): on disk only - the code must be decompressed to run, so memory does not shrink (it grows by the compressed copy while it unpacks) and every start pays the decompression. A tiny LZSS (12-bit offsets, a ~150-300-byte decompressor) on the smallest of all runs: image 8,704 -> 6,659 bytes, engine 7,680 -> 4,605 - about -4.5 KB of 16.4 KB after the decompressor; deflate or xz pack tighter (image 5,639 / 5,456) but their decompressors (KBs) eat the gain. The question before building: should the size objective count bytes on disk at all if they are not the bytes that run - it would reward a packing trick over a smaller VM | this register |
| Packed names (6 bits a character) | priced, plan written, deferred by the owner (Iterations 222, 231-233): the image's names take ~300-380 bytes fewer (-311 on the smallest, -292 middle, -384 fastest) before ~100-150 bytes of pack/unpack code - about 1-1.5% of binary + image at the small end, as a gene. Plan: a fixed 63-character alphabet (A-Z, 0-9 and the 22 punctuation characters the front uses, a few spares); a name packs only if every byte is in it, else stays raw (lowercase, UTF-8) - one stored form per name, so lookups compare stored forms; the hash on the plain name (threads unchanged); NAME>STRING unpacks into two alternating buffers; the converter packs the image. UTF-8 names gain nothing under it; a second, Cyrillic table chosen per name would store a letter in 6 bits instead of 16 (an 8-letter name 16 -> 6 bytes, ~60% less; 31 letters fit) - in a program's own dictionary, not the evolved image; CJK has no small table. The count byte after the name (Iteration 232) means >NAME no longer cares what name bytes hold | `results/price-names.md` |
| The next keeping forms (OVER C@, DUP C@, ...) | priced again, not built (Iteration 222): the largest, DUP before ?BRANCH (5-6% of the small end's image dispatches), already has its form, listed by 121 of seed 43's front and realised by 28 - the small end is short of one-byte codes, and new forms would queue for them | `results/price-keepforms-next.md` |
| Packed names, six bits a character | priced, not built (Iteration 222): -292 to -384 bytes before the code to pack and unpack, a kernel change and a reseed; hiding the internal words' names saves more for less | `results/price-names.md` |
| A name-lookup cache beside the threads gene | priced, not built (Iteration 221): at 16 chains a 16-entry cache cuts the walk 22% (corpus) and 48% (parse); doubling the chains halves it, for bytes evolution already declined at the small end; half the walk is names not found, which a cache cannot serve | `results/price-lookup-cache.md` |
| Native code calling byte code (SPN's st_interp, GENES.md candidate 5) | priced again, not built (Iteration 220): since jitx the words it would free hold 9.3% of the kernel workload's dispatches, 4.1% of the corpus's, ~0 elsewhere, and they would cross back to byte code every 3-4 operations | `results/price-jit-interp.md` |
| Stack state in the JIT's translator (cells in registers across stencils) | priced, deferred (Iterations 218-219): -27% instructions with free renames, but the fixed-register form (+1.4 KB at K=2) saves few, and on the VM neither is reliably faster at eight code placements - only the loop index in registers is (-40%, the loop workload alone); the laptop's `jitstack-inner-sweep.sh` decides | `results/price-jit-stack.md` |
| fsys 5 copying lines out a cell at a time (FS-MOVE) | priced, not built (Iteration 214): where CMOVE has no opcode, kernel -28% and corpus -17% of fsys 5's dispatches; where it has one, +2.2% to +11.7% and +0.8% to +6.5% - evolution can give CMOVE its opcode instead | `results/drafts/fsys/single-syscall.md` |
| Variables and constants compiled as literals in code compiled at run time (`rtlit`) | built and measured, rejected (Iteration 59): correct, and the held-out sieve 0.811 of its dispatches - but kernel 0.984 and corpus 1.016, because a COMPILE,8 link that checks every compiled word costs a compiling workload more than it saves; 132 bytes more; selected geomean 1.000 | PROGRESS.md, Iteration 59 |
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

**Judging a run (Iteration 188, the owner: weigh, do not lock out).** A run is
small only if all five are: fastest under 5%, smallest under 2%, memory under
8 KB, and the two front-wide measures - the hypervolume in log space under 2%
and the best Q (binary + image x run time x memory) under 2%. A run that moves
the front's middle - +1% size for -25% time - is not small.
compare-fronts.py prints the five per run ("Judging the runs") and names the
Q-best design of all runs; evolve.py's report names its own.
