# The gene pool: what is in, and what other VMs could add

## In the genome now

| genes | from | what they change |
|---|---|---|
| family: `cell`, `sod16`, `cpt16`, `cv8` | this ladder (RelF, SOD16, CPT16, CV8) | the encoding; dormant genes switch on when a lineage changes family |
| CV8: top of stack in a register, call-target scale, byte headers, specialisation families, shared call path, far DOES>, variable opcodes, 256-entry dispatch, guard pages | the engine lab, relf | dispatch and image format |
| folds: which of the 23 foldable primitives get prim;EXIT opcodes, in what order | the engine lab | opcode map |
| superinstructions: primitive pairs as single opcodes, drawn from the parent's own hottest pairs (`design_pairs`, profiled per design), in the slots folds and specialisations leave free | gforth's prims2x, relf S3, this lab's pair profile | one dispatch instead of two, and one byte instead of two; folds, specialisations and pairs compete for the same opcodes |
| format-10 opcodes (`ops10`): `EXECUTE`, `I`, `(DO)`, `+!`, `?DUP`, `UNLOOP`, `J`, and the loop words with an operand, `(LOOP)`, `(?DO)`, `(+LOOP)`, `(LEAVE)` - kernel colon words - and the short branches `?BRANCH8`, `BRANCH8` as opcodes, from the free slots before the pairs, each only where its compiled body is exactly the definition the engine implements | relf's format 10 | a call and a return become one dispatch; the words compete with pairs and folds for slots |
| the escape (`escape`): primitives 36-67 behind one byte (125 + selector), their 32 opcodes joining the free slots | relf's format 10 | rare primitives a byte bigger; the slots go to words and pairs - what lets a design with specialisations hold more than two |
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
| run-time immediates (`rtimm`: 0, 1; Iteration 37): with run-time fusion and spec imm, the compiler the image carries makes `n +` an ADDI and `SWAP n +` a SWAP+I in the code it writes (forth/cv8-fuse-imm.4) | this lab: fib's own code, dumped from a front design | fib 15% fewer dispatches, 17-27% faster, for 408-472 bytes (results/rtimm.md) |
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
