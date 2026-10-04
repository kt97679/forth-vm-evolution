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
   code field per word. Slower, classic, and a distinct ancestor.
7. **Dynamic superinstructions** - gforth copies primitives' machine code;
   this lab's SPN copies C stencils. SPN's genes - fusions, recipes or lazy
   translation, inlining - are phase 3.
8. **A register machine** - Lua, Dalvik. Shi and Gregg found a register
   JVM executing 46% fewer VM instructions for 26% more code: the far end
   of the speed-for-size trade. Needs a stack-to-register translator; the
   largest item here.

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
