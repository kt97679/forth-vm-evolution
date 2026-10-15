# The gene pool: what is in, and what other VMs could add

## Adding a gene - one row (Iteration 276, prompts/17)

A new gene is one call in lab/evolve/evolve.py: `gene(name, values, show, family,
late, needs, convert)` - its values (off first, 0 for a late gene), how a mutation
names a value, the family that expresses it, whether it came after runs were
recorded (so it stays out of a design's identity while off), the rule for when it
is expressed, and the converter's options when it is. mutate() and
random_genome() draw from the row's values; express() applies its rule; the
converter gets its options. A gene that changes the engine still needs its build
code (engine flags, generators). lab/evolve/gene-table-test.py registers a
fictional gene and requires it to work with no code change.

Touch points, before and after: factor (a converter gene) took seven - its
values' constant, LATE, EXPRESSED, an express() rule, a mutate() branch, a
random_genome() branch, the converter's option; it is one row now (with its
shares' constant, which the converter's option reads). The thirteen older genes
with more than two values keep their rules and build code, but their values sit
once in GENE_VALUES, read by both mutate() and random_genome() - the two copies
before. Converting them changed nothing: 2,876 recorded genomes keep their ids
and expressions; 3,000 mutations, 1,000 random genomes and 1,000 crossovers, each
seeded, came out identical before and after (lab/evolve/gene-equiv.py REV checks any
later conversion the same way).

**Iteration 278: 31 older genes are rows too** - their express() rules, their
values where they have more than two, and five converter flags (bss, thinhdr,
opbody, abortif, lean): rtfuse, rtimm, rtloop, rtloopall, kfast, tfind, kinput,
klookup, jit, rtiplus, swapi, tag2 (registered before the six rules that read it),
hotcalls, t2hot, hotinl, t2wide, rtempty, kstack, jitx, opbody, bss, thinhdr,
abortif, lean, jitloop, jitinl, jitos, jittail, jitk, and factor. Still code, each
for a reason: the dispatch cluster (varcall, sharedcall, doesfar, msc, tail, d256 -
rules that pop one another), the compiler's switch-off of GCC's own genes, the
list genes (spec, folds, supers, ops10, opcall), two value rewrites (rtimm and
rtloop 2 to 1 where the build is the same), the dormant sysc (in no family: a row
would switch it on), every engine flag, and the converter options several genes
build together (the tag's, the JIT's, the headerless and rebind lists). gene()
refuses an already-listed gene whose late-ness its row misstates: rtfuse, older
than LATE, was put into it by default, and gene-equiv.py caught 875 recorded
designs changing id - every one rtfuse=0 leaving the identity.

## In the genome now

| genes | from | what they change |
|---|---|---|
| family: `cell`, `sod16`, `cpt16`, `cv8` | this ladder (RelF, SOD16, CPT16, CV8) | the encoding; dormant genes switch on when a lineage changes family |
| CV8: top of stack in a register, call-target scale, byte headers, specialisation families, shared call path, far DOES>, variable opcodes, 256-entry dispatch, guard pages | the engine lab, relf | dispatch and image format |
| folds: which of the 23 foldable primitives get prim;EXIT opcodes, in what order | the engine lab | opcode map |
| superinstructions: primitive pairs as single opcodes, drawn from the parent's own hottest pairs (`design_pairs`, profiled per design), in the slots folds and specialisations leave free | gforth's prims2x, relf S3, this lab's pair profile | one dispatch instead of two, and one byte instead of two; folds, specialisations and pairs compete for the same opcodes |
| format-10 opcodes (`ops10`): `EXECUTE`, `I`, `(DO)`, `+!`, `?DUP`, `UNLOOP`, `J`, and the loop words with an operand, `(LOOP)`, `(?DO)`, `(+LOOP)`, `(LEAVE)` - kernel colon words - and the short branches `?BRANCH8`, `BRANCH8` as opcodes, from the free slots before the pairs, each only where its compiled body is exactly the definition the engine implements | relf's format 10 | a call and a return become one dispatch; the words compete with pairs and folds for slots |
| 2@ and 2! in `ops10`, and in `opbody`'s list (Iteration 290): the double-cell fetch and store, six dispatches a call each as kernel colon words, one as an opcode - bubble's inner loop calls them at run time (2@ three times, 2! once), the corpus's tester too: 16-42% of bubble's dispatches inside them (results/source-audit-2.md). Code compiled at run time calls the words, so opbody's [opcode EXIT] bodies carry the saving there | this lab: word-cost.py | bubble -11% to -28% of its dispatches, priced |
| > and 0= in `ops10`, and in `opbody`'s list (Iteration 299): the compare and the test as opcodes - > is `SWAP <` (the engine's L_gt is <, its name historical), 0= is `0 =`; code compiled at run time calls them: bubble's compare 11.7% of its dispatches, ackermann's test 7.7%, on seed 50's fastest design without the JIT (results/source-audit-3.md). The JIT translates both (GT; LIT and EQ) | this lab: hotwords.py, word-cost.py | 658ed9b9f8 with them first, opbody and opinline: bubble -11.7%, ackermann -7.7% - and, its slots full, the kernel +5.5% and the corpus +8.7% for the words they displaced: evolution places them |
| the [opcode EXIT] words among the primitives (`opinline`: 0, 1; Iteration 292): placed before (PRIMITIVES-END), where PRIMITIVE? asks by address, so the run-time compiler copies their opcode in place of a call - code compiled at run time (bubble's 2@ and 2!) saves the call and the EXIT. A word defined once only; a design with no [opcode EXIT] word does not express it. For a JIT design it can cost: an inlined opcode with no stencil leaves its word to the interpreter | this lab: word-cost.py | c9369657e4 with 2@ 2! and opbody: bubble 9,572,364 -> 7,448,901 dispatches (-22.2%; -41.6% from 12,759,474 before 2@ 2!) |
| the tail-call engine with preserve_none and musttail (`tailpn`: 0, 1; Iteration 293): clang 19+'s calling convention that saves no register on every handler, and musttail on every handler-to-handler call (tools/gen-tail.py --preserve-none) - CPython 3.14's tail-call interpreter. Built with the newest clang here that takes them (clang_pn(): clang-20 on the owner's laptop); expressed only on a clang tail engine, only where such a clang is installed | CPython 3.14; this lab: engines-check | s6's engine 14,232 bytes, 14,680 without (no register saved) - speed for the laptop's runs to judge |
| NUMBER? as one opcode (`knumber`: 0, 1; Iteration 295): forth/cv8b-knumber.4, after klookup's overlay - (NUMBER?), the kernel's NUMBER? with BASE @ and DPL given (its failures 0 0 0: only INTERPRET calls it, and aborts or throws), and NUMBER?8, whose body NUMBER? takes; the opcode's C (numberq, vm-lab.c) is the same steps. Put first in the design's format-10 list, so it takes a slot from the last word there. Expressed only with klookup | this lab: word-cost.py | c9369657e4's corpus 4,529,779 -> 4,067,754 dispatches (-10.2%, NUMBER? 10.1% -> 0.9%); 927064f127, its slots full: the corpus -4.9%, the kernel +5.3% - the word it displaced |
| handler entries aligned (`alignhot`: off, 32:11, 32, 64; Iteration 298): GCC's -falign-jumps, -falign-labels and -falign-functions - a computed goto's target, or a tail engine's function, on a fetch window's start; 32:11 only where it costs at most 10 bytes. The laptop's counters put the evolved interpreted designs' front end at half their cycles on compute work, and align1 only takes alignment away. GCC only; not with align1 or alignfn | this lab: counters.py --extra | the engine: s6 +1,280 bytes at 32:11, +5,216 at 32, +12,192 at 64; 658ed9b9f8 +1,216, +4,448, +10,976 - speed for the laptop's runs to judge |
| the escape (`escape`): primitives 36-67 behind one byte (125 + selector), their 32 opcodes joining the free slots | relf's format 10 | rare primitives a byte bigger; the slots go to words and pairs - what lets a design with specialisations hold more than two |
| an operation and the call after it (`opcall`: a list, Iteration 121; the tag, computed goto): `X;CALL` opcodes of their own (0xFE00 + k), X's handler then a direct jump into the call | results/docs-reuse.md (Koopman) | fastest: parse -3.8%, corpus -3.4%, kernel -1.6% of dispatches for +768 bytes of engine (16 ops); results/opcall.md |
| ABORT" guarded (`abortif`: 0, 1; Iteration 117): the converter puts every (ABORT") call behind ?BRANCH and -1, as gforth and lbForth compile ABORT" | results/forth-sources.md | parse -5.6%, corpus -3.0%, kernel -1.0% of dispatches on the fastest design for 56 bytes; errors unchanged |
| the stack check guarded (`kstack`: 0, 1; Iteration 116; the tag, without kinput): kinput's own ?STACK8 on its own - DEPTH 10000 U> IF ... ABORT" ... THEN | results/forth-sources.md | parse and corpus -0.7% of dispatches on the smallest design, the image the same size |
| the file read-ahead buffer (`fbuf`: 0, 1, 2 = 4096, 1024, 512 bytes; Iteration 115) | results/deep-dive-2.md: memory had no lever | the kernel workload's memory 200 -> 172 -> 168 KB (smallest), 216 -> 180 -> 176 (fastest); more read(2) calls |
| function alignment off (`alignfn`: 0, 1; Iteration 113): -falign-functions=1 -falign-loops=1 | the deep dive's 15, a flag pool for the binary | -O2 engines ~1.1 KB smaller, -Os ones nothing (results/flags-gcsections.md) |
| no inlining of small functions (`noinls`: 0, 1; Iteration 113): -fno-inline-small-functions | the same | -O2 engines ~1.3 KB smaller, maybe slower |
| the JIT reaches further (`jitx`: 0, 1; Iteration 108; on the JIT): variables as literals, words without the JIT header translated once each, >R/R>/R@ in balanced words, a FILL stencil | results/jit-kernel-words.md (priced) | kernel workload 10% fewer bytecode dispatches, the sieve 99.9% (3.4x faster on the VM); +368 bytes of code (results/jitx.md) |
| (+LOOP) and (?DO) native (`jitloop`: 0, 1; Iteration 130; on the JIT; **dormant** - in LATE, not in EXPRESSED, until seed 39 has run): SPN's stencils for both, the scanner reading 160 bytes (its 64 cut both stencils: (+LOOP)'s 87 before either exit, (?DO)'s 76 after its fall-through), both exits required or the word stays bytecode. On the fastest design bubble's dispatches -98.5%, its long run 13.2 -> 7.9 ms (VM), the corpus -1.1%; gate, answers, the Forth 2012 suite as s6 on five JIT designs; off, ids, images and engines identical. D+ priced and left out: -ack native, no faster - the call is the cost |  |  |
| one SYSCALL (`sysc`: 0, 1; Iteration 136; CV8 designs - vm-lab.c's; **dormant** - in LATE, not in EXPRESSED, until seed 39 has run): the engine keeps one system call in FORK's slot and drops the shell's other seventeen process and environment primitives and the runtime's environment and getpwnam - none of which a design's image (the kernel) calls; the shell gets them back in Forth from forth/shell-sysc.4 (tests/shell, all 554 assertions, on a SYSC s5 shell: tools/test-sysc-shell.sh, removed in Iteration 169 - run-tests.sh's shell suite runs every SYSC shell since). Engines: five JIT designs -3,392 to -3,808 bytes, the smallest of seed 37 -2,880 (its total -14%), tail-call threading -6,568, msc -3,728; every one through the gate; off, ids, images and engines identical |  |  |
| the JIT's translator compiled for size (`jitos`: 0, 1; Iteration 239; JIT designs not built -Os): engine/jit.c under GCC's optimize ("Os") - it runs once per word translated; the stencils are compiled apart | results/price-stencils-bloom.md: a JIT engine's extra bytes are the translator, jit_body 3.5 KB | -416 to -800 bytes off JIT engines built -O2/-O3; translation speed is the trade |
| tail calls as jumps on the JIT (`jittail`: 0, 1; Iteration 246; JIT designs): engine/jit.c - a call to a native word whose next operation is EXIT, or a BRANCH chain to one, is translated as a jump to it, so its ret returns to the caller and tail recursion runs in place (no native stack growth). Return addresses are on the machine stack, so >R, R> and loop parameters are untouched. Measured on 28677d13b1 (VM, alternating runs): ackermann 15-18% faster, the other selection workloads within noise; +256 engine bytes. Off: the engine byte-identical (results/price-jit-calls.md) |
| the JIT's stack cache (`jitk`: 0, 2, 3; Iteration 259; JIT designs): the top K cells stay in fixed registers across the copied code - tools/gen-jitk.py writes a variant of 16 hot data stencils (literal, DUP DROP SWAP OVER, + and immediate +, = > <, AND XOR, @ ! C@, I) for each cache state 0..K and a canonicaliser per state; control, calls, loops, exits and branch targets run in state 1, so every join and call agrees. Static stack caching as Ertl & Gregg's (up to 58% in their interpreter) and CPython's JIT; on the VM's Intel core mixed: loop -9%, bubble -5%, corpus -4%, fib +16% at K=2, flat at K=3 - the laptop decides. +2.3 KB (K=2), +2.8 KB (K=3) on the fastest design's engine |
| link-time optimisation (`lto`: 0, 1; Iteration 260; CV8 designs): the engine and its runtime compiled as one (-flto), so GCC inlines and drops across them; the JIT's stencils are compiled outside it - LTO changed their code and the JIT stopped translating (fib 2.5x, loop 3.9x slower). Engines -32 (smallest) to -160 bytes (fastest) on top of Iteration 257's runtime savings; speed the laptop's |
| GCC's computed-goto unfactoring (`gotodup`: 0, 1, 2 - its default 8, 32, 128 instructions; Iteration 260; CV8 designs): `--param max-goto-duplication-insns`. GCC factors computed gotos early and copies the dispatch back into handlers whose block ends in no more than this many instructions; larger values copy more - interpreted engines +704 to +800 bytes at 32-128 (3456ac1e5e, 697f12fecc); JIT engines unchanged. A dispatch per handler predicts better on some cores, a shared one is smaller - the laptop's |
| the compiler (`compiler`: 0 GCC, 1 clang; Iteration 262; CV8 designs, offered only where clang is installed): every engine compile through clang - -Oz for -Os, only the flags clang knows; GCC's own genes (nogcse, nocrossjump, align1, noreorder, peel, ipaclone, tracer, noinls, gotodup, jitos, regpin, lto) not expressed under it. No source change but a bcmp in the runtime. clang 18 on the VM: engines larger at the small end (3456ac1e5e 7,112 -> 10,256; -Oz 8,624), 4% smaller at the fast end at -Oz (3bb2087f9d 21,276 -> 20,396); the JIT's stencils hold. The way to preserve_none (clang 19+) for the tail engine |
| repeated code in shared bodies (`factor`: 0, 1, 2, 3; Iteration 267; tag-2 designs): the converter moves runs of whole operations that recur in the image - no branch or branch target, inline operand, string, EXIT, return-stack or loop word, call to a word reading its caller's return address - into headerless bodies past the image's end, each use a 2-byte call; a use keeps the run's old cells as a GAP, so no offset in the word moves. Which words: those below 0.1% (1) or 1% (2) of the reference dispatches (lab/evolve/hotwords-v1.json, lab/evolve/hotwords.py), or every word (3). Counted on 3456ac1e5e: -41 image bytes for +0.007% dispatches, -95 for +0.17%, -127 for +1.98% (kernel and loop +4.3%). No engine change; off, every design converts byte for byte as before |
| one-operation words inline on the JIT (`jitinl`: 0, 1; Iteration 137; JIT with jitx; **dormant** until seed 39 has run): a call to a word of one operation and EXIT - 1+, 0=, 1- - is that operation in the caller (not one that branches, ends the word, or touches the return stack or the interpreter), and D+ gets its stencil back. Native call and return were a quarter of a small recursive word's time (2.92 -> 2.21 ns a call); D+ alone (Iteration 130) made -ack native and no faster - with the inlining, ackermann's long run 10.1 -> 5.0 ms (VM), its 12.7 M dispatches native. Gate, answers, the Forth 2012 suite as s6 on five JIT designs with jitloop; off, identical |  |  |
| compile nothing for a word that does nothing (`rtempty`: 0, 1; Iteration 101; in the tag): forth/cv8t-empty.4, an outermost COMPILE,8 - a word whose body is EXIT alone (CHARS) compiles to nothing | Iteration 89: CHARS, 12.6% of the kernel workload's calls | kernel workload 2.3-4.0% fewer dispatches, +32-40 bytes of image |
| the tag without its 3-byte call (`t2wide`: 0, 1; Iteration 95; in the tag, not multi-state): `10xxxxxx` 64 more one-byte codes (127), calls of 2 bytes (16 KB) and 4 (1 GB) | the owner's question on continuation-byte calls; the deep dive's 6 | escapes (4-8% of the dispatches of kernel, parse, corpus) gone, images 121-302 bytes smaller (results/t2wide.md) |
| inlined at the hottest call sites (`hotinl`: 0, 10, 20, 40; Iteration 92; in the tag): the converter splices the first K safe sites of lab/evolve/hotsites-v1.json - the image's call sites by the fastest design's profile, named by caller, callee and ordinal - before every rewrite | Iteration 91's deep dive: short words found nothing, hot sites did | fast designs 9-10% fewer dispatches on parse and corpus, 4-5% on kernel, +40-160 bytes (results/hotinl-opbody.md) |
| words an opcode replaced, [opcode EXIT] (`opbody`: 0, 1; Iteration 92): (FIND), (>NUMBER), THREAD-FIND, +!, ?DUP, as FILL and CMOVE (Iterations 50, 54) | Iteration 91: a quarter of the fastest image never runs | 128-144 bytes off the fast designs' images; run-time calls take the opcode (results/hotinl-opbody.md) |
| the data stack's start skewed (`dskew`: 0, 1; Iteration 183, the owner's question - the stacks' place): 2 KB lower, so its top cells and the return stack's stop sharing page offsets (4K aliasing: with both stacks at the block's top they met whenever the return stack was one cell deeper) | the engine's layout (vm-lab.c DSKEW) | not measurable on the development VM (rounds differ by up to 9%): the laptop's to judge |
| SWAP+I sure of a slot (`swapi`: 0, 1; Iteration 61; with 'imm'): SWAP+I first among the format-10 names | seed 13's front: SWAP+I on none of it | fib 0.944, selected geomean 0.987, 16 bytes less (PROGRESS.md, Iteration 61) |
| the keeping forms (`ops10` names DUP+I, DUP<I; Iteration 176): DUP n + and DUP n < in one dispatch, the top kept - in the image (the converter) and at run time (cv8t-fuse-imm.4's IMM+), pinned to one-byte codes where IMM-OPS is | results/price-hybrid.md: the hybrid's keeping forms | seed 40's smallest with rtimm=2: fib -36.3% of its dispatches (the price: 36.4), +726 bytes |
| I + fused in run-time code (`rtiplus`: 0, 1; Iteration 60; with rtloopall): a format-10 opcode I+, SUPER-TABLE's (I, +) -> I+, and forth/cv8-fuse-iplus.4 pointing LAST-OP at I's byte | the run-time code's opcodes, named | loop 0.801, sieve 0.967, kernel/parse/corpus +0.7-1.2% compile cost; selected geomean 0.962; 37 bytes (PROGRESS.md, Iteration 60) |
| one thread head in the header (`thinhdr`: 0, 1; Iteration 58; CV8): the header's 32 thread heads - read by the CV8 loader and never used, only SOD16 numbers calls - as a count of 1 and a zero head | this lab: an audit of the header | 248 bytes off every CV8 design, dispatches identical (results/bss.md) |
| the whole lookup and numbers (`klookup`: 0, 1; Iteration 57; with kinput): forth/cv8b-klookup.4 ((FIND) and FIND8, (>NUMBER) and >NUMBER8, WORD8) and (FIND), (>NUMBER) first among the format-10 names | the dispatch attribution on seed 13's fastest | parse 0.53-0.57, corpus 0.60-0.65, kernel 0.80-0.81 counted; differential tests identical (results/kfast.md) |
| the input side (`kinput`: 0, 1; Iterations 54-55; with kfast): forth/cv8b-kinput.4 (REFILL's tab loop as TABS>BL; (PARSE) and PARSE8; ?STACK8) and SCAN, SKIP, TABS>BL, FILL, (PARSE), HASH, PLACE first among the format-10 names | the dispatch attribution on seed 12's fastest | kernel 0.62, parse 0.65, corpus 0.61, sieve 0.84 counted; 63 bytes less (results/kfast.md) |
| THREAD-FIND first (`tfind`: 0, 1; Iteration 52; with kfast): THREAD-FIND first among the format-10 names - seed 11 drew it from the pool 7 times in 1,425 designs | seed 11's records | kernel 0.82, parse 0.49-0.51, corpus 0.63-0.65 counted on seed 11's best (results/evolve-...-seed11.md) |
| THREAD-FIND as an opcode (in `ops10`, with kfast; Iteration 51): the byte-header dictionary's walk along one thread in one dispatch | this lab: the dispatch attribution | parse 0.489, corpus 0.631, kernel 0.799 more on 96f2d8bfd7 (results/kfast.md) |
| FILL and CMOVE as opcodes (in `ops10`; Iteration 50): the kernel's byte loops as format-10 opcodes, and their colon bodies the opcode and EXIT for code compiled at run time | this lab: the dispatch attribution | kernel 0.865, corpus 0.917, sieve 0.848 more on 96f2d8bfd7 with kfast, 32 bytes less (results/kfast.md) |
| kernel words faster (`kfast`: 0, 1; Iteration 49; byte headers): NAME>BUF without its 32-byte zero fill, which the byte compare never reads (forth/cv8b-kfast.4) | this lab: every dispatch attributed to its word | 24-29% fewer dispatches on kernel, parse and corpus (results/kfast.md) |
| scratch buffers out of the file (`bss`: 0, 1; Iteration 44): TIB, POCKET and INCLUDE-BUFFER live past the image's end, DP after them | this lab: an audit of a small image | 1,056-1,064 bytes (11-13%), no dispatch more (results/bss.md) |
| rtloop compact (`rtloopall`: 0, 1; Iteration 43): with rtloop and all eight loop opcodes, a run-time loop compiler without fallbacks - one chain, one 12-byte table (forth/cv8-fuse-loopall.4) | this lab: rtloop's own bytes, priced word by word | 380-488 bytes of rtloop's ~470 on seed 8's front, the same speed (results/rtloopall.md) |
| run-time loops (`rtloop`: 0, 1; Iteration 41): the compiler the image carries emits the design's loop opcodes - (DO) (LOOP) (+LOOP) (?DO) (LEAVE), I J UNLOOP - each where it has one, 16-bit operands, no padding (forth/cv8-fuse-loop.4) | this lab: loop.fth's INNER, dumped | loop 2-4x faster, for about 6% of the image (results/rtloop.md); loop is selected since |
| build artifacts left out (`lean`: 0, 1; Iterations 38-39): the compiler's X8 copies (calls and (POSTPONE)s to them go to X), the dump tool's words, dead shadowed words | this lab: the converter's own comment called the copies harmless | 12-16% of every CV8 image, 1,267-1,896 bytes on seed 6's front, no slower (results/lean.md) |
| run-time immediates (`rtimm`: 0, 1, 2; Iteration 37; 2 - Iteration 175: without pairs, the overlay alone): with run-time fusion and spec imm, the compiler the image carries makes `n +` an ADDI and `SWAP n +` a SWAP+I in the code it writes (forth/cv8-fuse-imm.4) | this lab: fib's own code, dumped from a front design | fib 15% fewer dispatches, 17-27% faster, for 408-472 bytes (results/rtimm.md) |
| one-byte calls (`hotcalls`: 0, 8, 16, 32): the far-call prefixes 0xE0-0xFF call the image's own words with the most call sites, through a table in the image's header; chosen per design by the converter, no profile | this lab's search (SEARCH-SPACE.md: a stranger), priced at Iteration 13 | a call one byte instead of two; the far form keeps 21 bits - 2 MB at scale 0 |
| tail-call threading (`tail`): every handler a function of (ip, dsp, rp, tos, t), dispatching by a tail call through a 256-entry table of functions; made from the cached engine | Wasm3, CPython 3.14, WasmKit | each handler's registers allocated for it alone; handlers that keep a frame are split so their dispatch stays a jump |
| multi-state stack caching (`msc`): 0, 1 or 2 top items in registers, a dispatch table per state, each handler variant dispatching by the table of the state it ends in; generated from stack effects for 72 operations, the rest normalised to the one-register state | Ertl and Gregg; gforth's vmgen | no memory traffic where the state absorbs it; three times the code for the specified operations |
| compiler: `-O2/-O3/-Os`, `-fno-gcse`, `-fno-crossjumping`, `-fcf-protection=none`, minimal label alignment, `-fno-reorder-blocks` | gforth's and CPython's builds, this lab's endbr64 finding | how the C compiler lays out the interpreter: computed goto only pays if every handler keeps its own indirect jump, which GCSE and cross-jumping undo |

## Not yet - each needs engine work first

Ordered by how much diversity they add for the work.

1. **Translation to direct threading at load** - gforth's
   primitive-centric hybrid direct/indirect threading, Wasm3's M3. The image
   stays compact; at start the engine expands it into handler addresses with
   operands, so each dispatch skips the decode. A gene any family could
   carry: compact on disk, fast in memory, at a start-up cost - exactly the
   trade the fitness weighs.
4. **relf's format 10** - in the genome: the words, the loop words, the
   short branches and the escape. Not taken: @XT, a fused @ EXECUTE -
   relf's kernel calls through vectors, and this one has no `@ EXECUTE`
   anywhere in the image's code, so it would have nothing to fuse.
5. **Indirect threading** - gforth-itc, fig-Forth, eForth, JonesForth: a
   code field per word. Slower, classic, and a distinct ancestor. *Priced
   at Iteration 29 (lab/dispatch/README.md): dispatch in token and direct
   threading's band, code a cell a reference - beside s0-cell, never near a
   front. Not built.*
7. **Dynamic superinstructions** - gforth copies primitives' machine code;
   this lab's SPN copies C stencils. SPN's genes - fusions, recipes or lazy
   translation, inlining - are phase 3.
8. **A register machine** - Lua, Dalvik. Shi and Gregg found a register
   JVM executing 46% fewer VM instructions for 26% more code: the far end
   of the speed-for-size trade. Needs a stack-to-register translator; the
   largest item here. *Priced at Iteration 29
   (results/price-register-machine.md): up to 38-50% of dispatches on the
   front designs are moves or lone literals - the largest prize left.
   Its first stage priced exactly at Iteration 32
   (results/price-register-stage1.md): 19-24%, most of it in five
   operand-carrying patterns the pairs cannot reach.*

Sources: gforth manual, "Direct or Indirect Threaded?" and "Dynamic
Superinstructions" (complang.tuwien.ac.at/forth/gforth/Docs-html/);
CPython Python/ceval_macros.h; Wasm3 (github.com/wasm3/wasm3); WasmKit
PR 145 (github.com/swiftwasm/WasmKit); Shi, Gregg, Beatty, "Virtual
Machine Showdown: Stack versus Registers", VEE 2005.

## Iteration 7: profile-guided optimisation measured - and three flags from inside it

**PGO is not a gene.** On s6's engine (VM, paired, CPU time), against plain
-O2: trained on the four measured workloads, 0.903 on them and 0.877 on
held-out loop - but that is the benchmark tuning itself. Trained on
`pgo-train.fth`, a program with the same ingredients and none of the
measured text, 0.980 on the four: exactly what -fprofile-use's flags give
with no profile at all (0.980), and fib slower (1.012). Two extra compiles
and a training run per design, for what the flags give anyway.

**The flags inside it.** One at a time on s6, with four layout-only builds
(-falign-functions/-loops 16, 32, 64; -fno-align-jumps) as the control,
same session:

| build | selection | fib | parse | loop (held out) |
|---|---|---|---|---|
| layout only, four builds | 0.972-0.994 | 0.971-1.028 | 0.954-0.978 | 0.899-0.990 |
| -fpeel-loops | 0.956 | 0.936 | 0.947 | 0.911 |
| -fipa-cp-clone | 0.961 | 0.930 | 0.957 | 0.926 |
| -ftracer | 0.977 | 0.934 | 0.979 | 0.924 |
| -funroll-loops | 1.015 | 1.001 | 0.980 | 1.062 |

Held-out loop's 7-9% is layout: moving code alone gives it 10%. fib's 6-7%
is beyond the layout band, for all three flags, in two sessions; on the
selection mean the best flag beats the best layout by under 2%. Added as
genes `peel`, `ipaclone`, `tracer`, because they are cheap and selection
on the real machine decides - but on the VM they do not help the front:
seed 2's fastest design (multi-state) + peel -1.0%, + ipaclone -0.3%,
+ tracer +2.9% (slower), where s6 gains 2-4%. Left out of a design's
identity when off (`LATE` in evolve.py): every recorded id is unchanged -
1,308 of 1,308 in seed 2's database, 1,306 of 1,306 in the VM rehearsal's.

## Iteration 8: triples priced, not built - tests before branches are the larger prize

`lab/evolve/price.py ID --db FILE` profiles a design's own dispatched
stream (its pairs, words and specialisations already fused) and prices
fusions before any is built (prompts/10). On seed 2's front, from its
database, on the VM:

## 9cd791dd84 - 21 pairs, 13 format-10 words

| workload | dispatches | pairs save | best 8 triples | best 16 | next 16 pairs | test -> branch | calls | EXIT |
|---|---|---|---|---|---|---|---|---|
| kernel | 7208480 | 14.7% | 2.7% | 3.3% | 5.2% | 8.1% | 7.2% | 2.5% |
| fib | 29672789 | 0.0% | 0.0% | 0.0% | 0.0% | 9.1% | 9.1% | 9.1% |
| parse | 28791219 | 14.2% | 4.3% | 4.9% | 9.5% | 8.3% | 3.7% | 1.6% |
| corpus | 5246072 | 15.0% | 3.7% | 4.5% | 6.4% | 7.9% | 4.5% | 2.0% |

the tests before a conditional branch, by workload:
  kernel  zeq 4.2%, eqi 1.3%, sub 1.1%, = 0.8%, < 0.4%
  fib     < 9.1%, zeq 0.0%, eqi 0.0%, sub 0.0%, = 0.0%
  parse   zeq 4.1%, eqi 1.7%, = 1.6%, sub 0.4%, sgt 0.4%
  corpus  zeq 4.3%, = 1.3%, eqi 1.2%, sub 0.6%, sgt 0.4%
the best triples, mean share: ROT+ROT++ 0.6%, DUP+ROT+ROT 0.6%, >R+C!+R> 0.4%, ROT+DUP+C@ 0.3%, >R+OVER+R> 0.3%, >R+OVER+C@ 0.2%

## 0ebf0445e0 - 22 pairs, 12 format-10 words

| workload | dispatches | pairs save | best 8 triples | best 16 | next 16 pairs | test -> branch | calls | EXIT |
|---|---|---|---|---|---|---|---|---|
| kernel | 7727583 | 15.4% | 2.1% | 2.4% | 3.2% | 7.3% | 8.9% | 2.1% |
| fib | 29679019 | 0.0% | 0.0% | 0.0% | 0.0% | 9.1% | 9.1% | 9.1% |
| parse | 33932578 | 15.7% | 1.6% | 1.9% | 2.1% | 6.6% | 7.3% | 2.1% |
| corpus | 5937204 | 16.1% | 2.2% | 2.6% | 2.4% | 6.7% | 7.4% | 1.9% |

the tests before a conditional branch, by workload:
  kernel  zeq 4.1%, sub 1.0%, eqi 0.9%, U< 0.5%, < 0.4%
  fib     < 9.1%, zeq 0.0%, sub 0.0%, eqi 0.0%, U< 0.0%
  parse   zeq 3.7%, U< 1.8%, sub 0.3%, eqi 0.3%, sgt 0.3%
  corpus  zeq 4.1%, U< 1.1%, sub 0.6%, eqi 0.5%, sgt 0.3%
the best triples, mean share: >R+C!+R> 0.3%, C@+>R+OVER 0.3%, OVER+R>+= 0.2%, >R+OVER+C@ 0.2%, ROT+ROT+SWAP 0.2%, R>+SWAP+>R 0.1%

Triples would remove 0-4.9% of dispatches - none on fib - an upper bound,
before overlaps and the slots they would take from pairs: not built. A
test fused with the conditional branch after it would remove 6.6-8.3% on
kernel, parse and corpus and 9.1% on fib. Most of it is `0= IF` (about 4%
on three workloads: a branch with its sense inverted) and, on fib, `< IF`
- in code compiled at run time, which only the image's own compiler can
fuse; the converter reaches the kernel's code alone.

### Built: `0= IF` as one branch (Iteration 8)

Two format-10 opcodes, `?NBRANCH` and `?NBRANCH8` (in OPS10_POOL): a
branch that jumps when the top is NOT zero, long and short. The converter
fuses `0= ?BRANCH` into it wherever nothing jumps to the ?BRANCH
(`tools/sod16.py`, testbranch) - `0=` an opcode where the tiny words are,
a call otherwise; the short form where the offset fits and the design has
a slot for it. Handlers in the plain engine, the cached one (gen-tos.py)
and multi-state caching (gen-msc.py).

**Measured on one engine binary**: the design's image converted with the
fusion and without (`SOD16_NO_TESTBR=1`), both through the gate, timed
paired - s6 with the escape (so all three opcodes have slots), VM:

| fused / unfused | kernel | parse | corpus | fib | loop (held out) | selection |
|---|---|---|---|---|---|---|
| 16 sites, all short | 0.969 | 0.972 | 0.966 | 1.003 | 0.997 | 0.977 |

What the price said: about 4% of the dispatches on the three, none on fib
and loop - their tests are in code compiled at run time, which the
converter never sees. The image is 16 bytes smaller.

**How it was first measured wrongly.** Two builds of s6 - with and without
the opcodes - compared as designs: the fused one 5% SLOWER, fib 12% - a
workload that never runs `0= IF`. The engines differed (two more
handlers), and that was layout. And the size had not moved: s6 has two
free slots (126, 127), so `?NBRANCH8` got none and every fused branch
stayed long - 3 bytes, as `0=` and a short branch were. For a change to
the image alone, compare two images on one engine.

**Still open**: the other tests (=, U<, = with an immediate, -) - about
half the price - each a pair of opcodes for slots; and `< IF` in fib (9%
of its dispatches), only reachable by the image's own compiler fusing as
it compiles.

## Iteration 9: tests fused at run time too, and = and U<

**At run time.** fib's `< IF` is compiled from fib.fth, by the image's own
compiler: the converter never sees it. The compiler overlay
(`forth/cv8-fuse.4`) gains `?BRANCH,`: IF, UNTIL and WHILE call it, and
straight after a test it overwrites the test's byte with the fused branch,
when SUPER-TABLE has (test, ?BRANCH, fused). LAST-OP gives it COMPILE,8's
safety: an operand byte is never taken for a test, and nothing branching
to HERE is fused across. The converter writes the test entries first
(`tools/layout.py`). So `rtfuse` now means something without pairs: the
overlay is built for a design with run-time fused tests. Changing the
overlay changes the image of designs that already had it (rtfuse with
pairs - none on any front).

**= and U<** join 0= and < (`TESTBR` in `tools/sod16.py`: one line per
test, plus its two handlers in the three engine forms).

**Measured on one engine per design** (image with and without,
`SOD16_NO_TESTBR=1`, both through the gate), s6 with the escape, VM:

| fused / unfused | kernel | fib | parse | corpus | loop (held out) | selection | image |
|---|---|---|---|---|---|---|---|
| 0= and <, kernel code | 0.959 | 1.004 | 0.960 | 0.957 | 0.998 | 0.970 | 9,937 |
| all four, kernel code | 0.948 | 1.003 | 0.945 | 0.945 | 0.949 | 0.960 | 9,929 |
| all four, and run time | 0.962 | 0.903 | 0.930 | 0.945 | 0.950 | 0.935 | 10,553 |

The overlay costs about 620 bytes for fib's 10%: a trade the two
objectives decide. The corpus - compiled at run time, so with fused
branches throughout under the overlay - gives identical output; held-out
loop gains 5% from tests in the kernel words it calls.

## Iteration 11: a second escape level - built, and it does not pay

Seed 3's front uses all 34 slots (21 format-10 opcodes, 13 pairs). The
nine rarest primitives in no fold or pair - UM* UM/MOD D+ WRITE READ SP@
SP! RP@ RP!: 0.36% of the fastest design's dispatches - are the tail of
the compacted band (27-35), so escaping them moves no other opcode and
the compiler's opcode constants hold. `escape=2` puts them behind ESC too:
41 escaped, 27-67 free, nine slots more (engine/vm-lab.c; `--escape2`).
It lives in every engine form; designs with the existing level compile to
identical machine code (two front designs and a tail-call one, checked).

**But it does not pay.** Filled with the fastest design's own hottest
pairs (22 with slots instead of 13), dispatches fell 0.2% (kernel), 2.4%
(parse), 1.1% (corpus), 0 (fib, loop) - counted, so free of layout.
`price.py` had said 6.4-12.9%: its pair and triple columns count
overlapping pairs, each operation many times (now flagged in the tool).
Timed on the VM, both front designs at level 2 were 5-6% slower, mostly
fib and loop, which use neither: layout, at a cost the counts cannot
recover. Kept as a gene, like rtfuse - selection decides.

## Iteration 12: the rest of the tests before a branch

`-` and `<>` (one pair: both fall through when a != b), `>`, `0<`, and
`=` with an immediate - EQI n then ?BRANCH, fused in place: the EQI
emits the fused opcode and n, the ?BRANCH only its offset, so positions,
cell sizes and targets stay the converter's own (`tools/sod16.py`,
eqibranch). Eight more format-10 opcodes (29 in the pool). Each new pair
of handlers is compiled only in a design that has it (`-DX_NEBR` ...): the
handlers of Iterations 8-9 sit in every format-10 engine, and unused code
moves GCC's layout - so these leave every other engine byte-identical
(seed 3's front, checked). `SOD16_TESTBR_SKIP=-,<>,EQI` leaves chosen tests
unfused, for measuring on one engine.

**Measured, one engine (multi-state, escape 2), image with and without
the five new**: 48 sites fused, 48 bytes smaller, both through the gate.
Counted dispatches (layout-free):

| | kernel | parse | corpus | fib | loop |
|---|---|---|---|---|---|
| 0= < = U< fused (8-9) | -5.0% | -5.9% | -5.6% | 0 | -4.4% |
| the five new, further | -2.3% | -1.1% | -1.6% | 0 | 0 |

Timed: 1.001 over the selection workloads - the first four's 5-6% bought
4-5%; these 1-2% should buy about 1%, inside one session's noise. A small
gain in speed, 48 bytes in size: for selection.

(A first count said +1117%: the profiler appends to its file, and the
script reused one name. price.py uses a fresh file per run.)

## Iteration 13: one-byte calls priced - and four format-10 words that were never there

**Priced** (`lab/evolve/callsites.py`, `results/price-hotcalls-seed3-front.md`):
the converter writes every call site of a design's image (CALLMAP in
tools/layout.py) and, with `--hotcalls-file`, lays the image out again
with chosen targets as one-byte calls - image side only, exact. On seed
3's front, the top 32 targets by bytes, the table charged at 2 bytes an
entry: 136 bytes net on 8dd8a7a146 (1.0% - bodies padded to 8 swallow
single bytes), 221-320 on the three 9.6 KB designs (2.3-3.3% - byte
headers make it better than the raw count: links shorten too). No
dispatch is removed: a call through a table is still a call.

Where the opcodes come from decides whether it pays. All 34 free slots
are taken, and the pairs with the fewest static sites are among the
hottest - taking four pairs' slots costs 3-8% of the dispatches for
24-120 bytes. The top of the far-call prefixes (0xE0-0xFF) costs no slot:
32 one-byte calls there, the far reach at scale 0 from 4 MB to 2 MB, which
cv8.4's compiler does not check today. So: a size gene, in that band,
targets chosen per design from its own census (no profile), table in the
image's header - next to build.

**The body check.** A kernel word becomes its format-10 or tiny opcode only
where its body is exactly the definition the engine implements. The
check (tools/sod16.py, ops10_at, tiny_at) cleared specialisations and
folds but not what came later - pairs, short branches (Phase 3d), fused
tests (Iterations 8-12) - so it compared rewritten bodies: `?DUP` read
`DUP ?BRANCH8 ...`, `(LOOP)` `... =?BRANCH8 ...`. A design carrying a short
branch lost `(LOOP)`, `(+LOOP)`, `(?DO)` and `?DUP`; one whose pairs fell
inside `(DO)`, `(LEAVE)`, `+!`, `J` or tiny `COUNT` lost those. The converter
printed a line; nothing read it; the design lived without the opcode.
`lab/evolve/scan-bodycheck.py --old`: 1,032 of seed 3's 1,145 living CV8
designs lost at least one word - every front design four. Every earlier
statement that these words were measured in combination with the short
branches is about designs that did not have them; each was measured alone
(Phases 3a-3d), where the check held.

Fixed: every rewrite off while checking (`SOD16_OLD_BODYCHECK=1` restores
the fault, to measure it); 0 of 1,145 now; and build() kills a design whose
check fails, so it cannot be silent again. The hand-made stages are
byte-identical. On the front (`lab/evolve/image-ab.py`, one engine): 99-112
bytes smaller, the selection workloads' dispatches unchanged (cold words
there), all through the gate.

**Two measurement faults found by the audit.** The profiler counts an
escaped primitive twice, and with the 256-entry dispatch every call twice
- price.py overstated such designs' dispatches by their calls (8%) and
doubled their calls column; corrected. And the held-out loop moves with
the image's size mod 8: before a call with an inline operand the compiler
pads with NOOPs, executed on every pass - 60753a0eb0's loop made 1,200,000
more NOOP dispatches (+14%) because its image shrank by 99 bytes.

## Iteration 14: one-byte calls, built

`hotcalls` (0, 8, 16, 32; in LATE, so every recorded id is unchanged): the
converter counts the call sites in the design's own code and gives the
bytes 0xE0-0xFF to the targets with the most (a site before an inline
operand counted last; three sites at least - two only pay for the entry);
the table, a count byte and 2-byte image offsets, ends the image's header
(flag 0x20), so the size measure sees it. The engine: `L_hcall` - RPUSH,
`ip = cbase + hot_tab[t & 0x1F]` - reached by the 256-entry table, or by
one compare in `do_call` where there is none; a copy per state under
multi-state caching (gen-msc.py), a function under tail calls. Engines
without the gene compile through `HCALL(i)` to `&&do_call` as before:
nine designs across every engine form, machine code and image identical
to Iteration 13's.

Every engine form lives with it - cached, plain, 256-entry, tail calls,
multi-state - through the gate. Predicted against achieved (32 targets):

| design | priced (Iteration 13) | built | image |
|---|---|---|---|
| s6-cv8b | - | 255 | 10,065 -> 9,810 |
| 8dd8a7a146 | 136 | 143 | 13,352 -> 13,209 |
| 60753a0eb0 | 221 | 212 | 9,686 -> 9,474 |
| f4a6dd9a13 | 320 | 319 | 9,662 -> 9,343 |
| 550df563ee | 304 | 303 | 9,646 -> 9,343 |

One engine, image without and with (`image-ab.py --set hotcalls=32 --env
SOD16_NO_HOTCALLS=1`): dispatches unchanged on kernel, fib and corpus,
0.2% fewer on parse; loop -12% on 60753a0eb0, the alignment artefact of
Iteration 13 (212 bytes, 4 mod 8). Time on this VM, selection 0.963-1.016,
inside its own noise: the same run with two identical images gave
0.976-1.005, single workloads 0.917-1.085. A size gene, for selection.

Open: the far form's reach - 2 MB at scale 0 with the gene, 4 MB without -
is not checked by cv8.4's compiler, and how far the workloads' dictionary
grows was not measured here.

## Seed 4: what selection made of Iterations 11-14

`results/evolve-amd-ryzen-7-pro-8840hs-seed4.md`, re-measured front of seven:
one-byte calls on six (five with 32 targets; 56% of the living); Iteration
12's tests, seven or eight on every one; the words restored at Iteration 13
on every one. The second escape level - built and found not to pay alone
at Iteration 11 - is on the fastest design and one small one, holding 17
and 18 pairs where the others hold 7-8: format-10 opcodes take 26-28 slots
now, and the nine more are what pairs need. Selection weighed it with the
rest and kept it.

## Candidates (Iterations 82-86) - the owner asked for more genes

Each to be priced before it is built, behind a gene, in this order (the
owner agreed, Iteration 83):

1. **Inlining short colon words.** A call (2-4 bytes, and a call and an
   EXIT dispatch every time it runs) to a word whose body is one or two
   one-byte opcodes becomes those opcodes - in the image (the converter)
   and in code compiled at run time (COMPILE,). Excluded: bodies touching
   the return stack (I, J, R>, >R, R@ - inside a callee they see the
   return address), inline operands, recursion. Never built: an early plan
   called it "phase 3". The tool to price it: lab/evolve/callsites.py
   (the call-site census by target, and per-target dynamic counts from
   the profiler) - to be ported first: its audit rebuilds with the
   pre-Iteration-13 body check, which today's designs fail.
   *Priced (Iterations 88-89, results/price-inline-tailcalls.md): in the
   image 0-15 sites and 0-11 bytes on every front design - the short words
   are opcodes already; at run time 6.1-7.6% of the kernel workload's
   dispatches on the faster designs, mostly the empty word CHARS. Not
   built: compiling nothing for a call to an empty word is the cheap
   part.*
2. **Forth tail calls.** A call followed by EXIT becomes a BRANCH to the
   callee (no new opcode: a 16-bit branch reaches any target in today's
   images): no return address pushed, no EXIT dispatch. Excluded: callees
   that read their return address - the inline-operand words ((S"),
   (POSTPONE) and the like), and words doing R> tricks. "Tail calls" in
   this catalog so far meant only the engine's dispatch form.
   *Priced (Iteration 89): 48-55 sites, -4 to +9 bytes, at most 1.8% of
   any workload's dispatches - not worth building.*
3. **Rewrite rules found by random testing** - a small superoptimizer:
   the profile's most frequent 2-3 operation sequences, searched for
   shorter sequences of the design's own operations (SWAP DROP -> NIP,
   OVER OVER -> 2DUP, 1 + -> 1+...), kept only if they agree on thousands
   of random stacks and edge values; each verified rule a gene the
   converter and the run-time compiler apply. The engine unchanged.
   Randomness finds the rules; evolution decides which to use.
4. **Image compression** with a small decompressor in the engine: the
   7-9 KB image is repetitive (bytecode, names); a few hundred bytes of
   decompressor against perhaps 2-3 KB of image - startup microseconds,
   memory unchanged (decompressed into RAM as now).
5. **The JIT's calls into bytecode words** (SPN's st_interp): most words
   compiled at run time stay bytecode because they call kernel words -
   the largest JIT lever left; then ?DO, +LOOP, >R/R>, kernel words
   translated lazily too. *Priced (Iteration 90,
   results/price-inline-tailcalls.md): on the five JIT designs of the
   front, every call translatable frees 9.8-10.2% of the kernel workload's
   dispatches, 1.4-1.6% of the corpus's and 78.8-80.1% of the held-out
   sieve's; >R without stencils is first in words holding 30.1% of the
   kernel's. Inlining short words alone: 0%.*
6. **A wider pool of compiler flags**, sampled at random (an autotuner)
   beyond today's nine (opt, nogcse, nocrossjump, nocet, align1,
   noreorder, peel, ipaclone, tracer). Caution: many flags win by a code
   layout that suits one CPU and not the next - check on the held-out
   workload and on the second machine.

**Where randomness does not belong**: mutating the Forth or C sources
themselves - the space is vast, and the 616-case ANS corpus is not a full
specification, so a random rewrite can pass every test and still be
wrong. Rules verified by random testing (3) are the safe form.
Triples were priced in Iteration 8 (~0.6% each at best) - not built.


## Ranked (Iteration 91) - a deep dive, what else could make it smaller and faster

The owner asked for imagination, not templates, then a ranking. Five facts
measured for it on the VM (one-off scripts, the front's genomes from
results/; dispatches counted, CPU times rough):

- **The binary is most of the size, and much of it is not the interpreter.**
  Smallest design (faf72cef8e, 18,032 bytes stripped): .text 14,686, of
  which virtual_machine 8,147 and 62 other functions 6,252 - vsnprintf
  1,162 (through snprintf), load_image 570, __udivmodti4 430 (UM/MOD),
  getpwnam 319, setenv 316, malloc 289, execvp 230, sigaction 188, syscall
  168, take_env 131, unsetenv 128, freel 128; static tables 1.5 KB
  (dispatch 1,024, esc_ 512). Fastest (2cbcf427f6, 34,936): virtual_machine
  11,997, 106 others 12,644 (jit_word 2,541, vsnprintf 1,909).
- **The workloads are now short, so starting counts.** On the fastest design
  kernel 3.9 ms, fib 7.4, parse 4.8, corpus 1.5, loop 0.55, sieve 4.7 (CPU
  per run); a bare start (BYE) 0.077-0.097 ms - 18% of loop, 7% of corpus -
  against 0.042 for an empty static process: half of it is ours.
- **Inlining at the hottest call sites pays where short words did not**: the
  10 hottest sites, any callee, +26 bytes for 9.3% of parse's dispatches,
  8.8% of corpus's, 3.4% of kernel's (fastest design; 50 sites +164 bytes,
  10.6/10.7/4.9%). On the smallest design 1-1.5%: evolution would choose.
- **A quarter of the fastest image never runs** in any of the six
  workloads: 104 of 329 words, 1,977 bytes - first the Forth bodies of
  words opcodes replaced ((FIND) 66, (>NUMBER) 57, THREAD-FIND 46) and what
  only they call (DIGIT? 56, NEXT-NFA8 53, NAME=? 36), and the old format's
  compiler variables (CV8-DOES-RESERVE 40, CV8-DOES-FAR? 39, CV8-SHIFT-V
  33). Smallest: 69 words, 896 bytes (13%). Names are 27-28% of the words'
  bytes.
- **Factoring repeated code (outlining) does not pay**: 62-78 bytes (~1%)
  for 0.2-4% more dispatches.

Ranked, most promising first - by what it should buy on the three
objectives, how sure the number is, and what it costs in mechanism:

1. **Inline the hottest call sites in the image** (converter only, a gene
   with K, sites from a reference profile like tag2-rank): measured above.
2. **Dead bodies behind opcodes, and the old format's leftovers, out** (a
   lean-like gene): words an opcode replaced get [opcode EXIT] as FILL and
   CMOVE did (Iteration 50) - the loop words excepted, they read their
   caller's return stack - their helpers go where nothing else reaches
   them, and the compiler variables tag 2 never reads go. Estimated 300-600
   bytes of the fast designs' images (4-8%).
3. **The OS layer out of the engine**: the shell's primitives (FORK EXECVE
   WAITPID PIPE DUP2 GETENV SETENV UNSETENV CHDIR GETCWD GETPWHOME SYSTEM
   ALLOCATE...) carry ~3-4 KB of the smallest engine; no workload uses them.
   Either a design without them, or one SYSCALL primitive with the wrappers
   in Forth outside the image (the shell loads them). 12-16% of the smallest
   total. The owner decides whether the shell is part of the job.
4. **A cheaper start**: dispatch tables built by the compiler, not filled at
   each start; fewer pages touched; guard pages and COLD's Forth set-up
   looked at - up to ~10% of loop and ~4% of corpus on the fastest design.
   And a question for the owner: should starting count in speed (longer
   workloads, or a bare-start baseline subtracted)?
5. **The JIT's calls into bytecode** (candidate 5 above, priced in Iteration
   90): with data words and constants as literals, 10% of the kernel
   workload's dispatches and 80% of the sieve's would run native.
6. **Drop the 3-byte call form - 64 one-byte codes free**: image calls are 2
   bytes (4 before an operand); run-time calls of 16 KB-4 MB would take 4.
   The codes: one-byte calls to the most-called words (the hot calls the
   tag gave up, ~200-300 bytes), no escapes, short branches with the offset
   in the opcode. A format decision (FORMAT-TAG2.md).
7. **Compile nothing for a call to an empty word**: CHARS, 5.2 of the
   kernel workload's 6.1 points (Iteration 89), ~10 bytes of Forth.
8. **Engine trims**: escaped operations as one cold -Os function, not
   handlers each with a dispatch; dispatch tables as 16-bit offsets; UM/MOD
   by the CPU's divide, not libgcc's 430 bytes. ~1-2.5 KB.
9. **Names in 6 bits a character**, FIND comparing packed keys: ~25% of the
   names, ~500 bytes.
10. **Shipped compressed** (engine and image behind a small self-extracting
    stub; candidate 4 widened to the engine, most of the size): perhaps a
    third off binary + image, paid in start time (4) and memory - it shrinks
    the file, not the system; against the aim unless the owner reads the
    objective so.
11. **The interpreter's handlers as the JIT's stencils**, one copy of each
    operation's machine code: the JIT's ~3 KB of engine.
12. **Native code for the hottest kernel words at build time**: the
    converter writing a C handler from a word's Forth body, what the k-genes
    did by hand (Iterations 49-57).
13. **Operand-carrying superinstructions from each design's profile** (a
    literal and an operation, as ADDI and EQI).
14. **Rewrite rules by random testing** (candidate 3): the folds, pairs and
    fused tests took the common sequences already.
15. **A wider compiler-flag pool** (candidate 6), now for the binary as well.
16. **A better dictionary hash or thread count**, priced offline from a
    trace of FIND's keys.
17. **The offset in the opcode, nibble-packed hot pairs** - need 6's codes.
    *(6 built as the gene t2wide, Iteration 95: results/t2wide.md.)*

*Iterations 100-103 (the owner's answers): **Q** (size x time x memory)
for information, never selection; **3** - one SYSCALL primitive (the
shell's OS words in Forth on it) agreed in principle, to plan; **4** -
longer workloads (Iteration 100); **7** built as the gene rtempty
(Iteration 101); **8** - the CPU's divide for UM/MOD done in every x86-64
engine (Iteration 102: libgcc's 430 bytes gone), the cold escaped
operations and 16-bit dispatch tables next; **9** - later; **the JIT** -
kernel words made native, priced (Iteration 103, results/jit-kernel-
words.md): with data words as literals, 8.2% of the kernel workload's
dispatches; FILL's stencil, the sieve's 79%.*

*Iteration 104 - an engineering item, not a gene: the genes as data
(prompts/17-variants-as-data). Each gene of Iterations 92-101 touched six to
eight places in evolve.py (LATE, EXPRESSED, BLOCKS, express, mutate,
random_genome, build, setup's dumps), and one addition's global name
replaced another gene's pool; one record per gene - values, condition,
converter options, engine flags, overlay, dump suffix - would make the next
gene a row, checked by a fictional gene in the tests.*
18. **Handlers ordered by the profile** (I-cache): no size; layout noise.
19. **Factoring repeated code**: measured above - no.
20. **Tail calls, or the fall-through layout**: measured (Iteration 89) - no.

*Built (Iteration 92, results/hotinl-opbody.md): 1 as the gene `hotinl`, 2 as
`opbody` - together on the fast designs about size-neutral (-16 to +16
bytes) for 9-10% fewer dispatches on parse and corpus, 5% on kernel.*
*Seed 24 (Iteration 94): opbody on 23 of the front's 37 designs, its clean
pairs -105 bytes and neutral in time; hotinl tried 33 times, on none - its 8
clean pairs parse 0.970, the rest within a pair's noise (+-5%). If seeds 25
and 26 do not take it up, it comes out.*
*Seeds 25-26 (Iterations 96-97): hotinl taken up after all - 3 of seed 25's
front, 11 of the night run's, and the two fastest designs of all runs (20
sites); opbody on every front design of the night run. t2wide (Iteration
95) on all 35 of the night run's front and 29 of the 30 of all runs.*

## Ranked (Iteration 115) - results/deep-dive-2.md

1. **kstack** - *corrected in Iteration 116 (results/forth-sources.md)*: kinput
   already has a guarded ?STACK; (ABORT")'s calls come from INTERPRET and
   REFILL. Built as kinput's ?STACK8 alone (-0.7% on designs without it); the
   real fix is a guarded ABORT" (parse -4.3%) - a source change, the owner's.
2. **knum** - NUMBER?'s plain cases in C: 19.1% of parse, 7.8% of corpus.
3. **Promotion by synthesis** - opcodes composed from the core's handlers
   for any straight-line word or hot sequence (gen-super.py generalized):
   evolution building instructions, the ceiling of an instruction set.
4. **The primitive-set gene** (the owner) - demotion to a minimal core:
   priced, no single demotion pays (OVER, ROT: larger and slower; UM*: kernel
   2x slower) - the floor of 3, built with it.
5. Process: immigrants, macro-mutations, islands, success-led mutation
   rates, a knock-in sweep - against anchoring.
6. hotinl's list from today's fastest design; more JIT stencils (COUNT,
   DODOES, PICK, (?DO), (+LOOP)).
7. 16-bit dispatch tables (~768 bytes); one SYSCALL primitive (~1.3 KB and
   the handlers); packed names (~500 bytes).
8. INTERPRET's loop in C (34% of parse) - large, re-entrant: later.

Built in Iteration 115: **fbuf** (memory: -28 to -40 KB) and the run start
**fromzero** (random genomes only).

*Iteration 120 (results/docs-reuse.md, Koopman's Table 6.3): **opcall** - an
operation and the call after it as one opcode, the call's width decided by a
direct jump, no table dispatch between: priced at 2.7-6.6% of dispatches on
the fastest design (LIT8, ?BRANCH8, (PARSE), PLACE, DROP and 0= before calls:
the top ten 95% of the pairs), 2.7-3.8% on the smallest. The one combination
of the RTX 32P's that no gene has. A slot a pair, competing with supers.*
