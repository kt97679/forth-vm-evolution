# The gene pool: what is in, and what other VMs could add

## In the genome now

| genes | from | what they change |
|---|---|---|
| family: `cell`, `sod16`, `cpt16`, `cv8` | this ladder (RelF, SOD16, CPT16, CV8) | the encoding; dormant genes switch on when a lineage changes family |
| CV8: top of stack in a register, call-target scale, byte headers, specialisation families, shared call path, far DOES>, variable opcodes, 256-entry dispatch, guard pages | the engine lab, relf | dispatch and image format |
| folds: which of the 23 foldable primitives get prim;EXIT opcodes, in what order | the engine lab | opcode map |
| superinstructions: primitive pairs as single opcodes, chosen from the 24 pairs the CV8 interpreter dispatches most, in the slots folds and specialisations leave free | gforth's prims2x, relf S3, this lab's pair profile | one dispatch instead of two, and one byte instead of two; folds, specialisations and pairs compete for the same opcodes |
| format-10 opcodes (`ops10`): `EXECUTE`, `I`, `(DO)`, `+!`, `?DUP`, `UNLOOP`, `J`, and the loop words with an operand, `(LOOP)`, `(?DO)`, `(+LOOP)`, `(LEAVE)` - kernel colon words - and the short branches `?BRANCH8`, `BRANCH8` as opcodes, from the free slots before the pairs, each only where its compiled body is exactly the definition the engine implements | relf's format 10 | a call and a return become one dispatch; the words compete with pairs and folds for slots |
| the escape (`escape`): primitives 36-67 behind one byte (125 + selector), their 32 opcodes joining the free slots | relf's format 10 | rare primitives a byte bigger; the slots go to words and pairs - what lets a design with specialisations hold more than two |
| compiler: `-O2/-O3/-Os`, `-fno-gcse`, `-fno-crossjumping`, `-fcf-protection=none`, minimal label alignment, `-fno-reorder-blocks` | gforth's and CPython's builds, this lab's endbr64 finding | how the C compiler lays out the interpreter: computed goto only pays if every handler keeps its own indirect jump, which GCSE and cross-jumping undo |

## Not yet - each needs engine work first

Ordered by how much diversity they add for the work.

1. **Translation to direct threading at load** - gforth's
   primitive-centric hybrid direct/indirect threading, Wasm3's M3. The image
   stays compact; at start the engine expands it into handler addresses with
   operands, so each dispatch skips the decode. A gene any family could
   carry: compact on disk, fast in memory, at a start-up cost - exactly the
   trade the fitness weighs.
2. **Tail-call threading** - Wasm3, CPython 3.14, WasmKit (which tried
   labels-as-values and tail calls and kept tail calls: one big function
   spills sp and pc). `lab/dispatch` has the C prototype; it needs the
   CV8 handler set rewritten as functions.
4. **relf's format 10** - in the genome: the words, the loop words, the
   short branches and the escape. Not taken: @XT, a fused @ EXECUTE -
   relf's kernel calls through vectors, and this one has no `@ EXECUTE`
   anywhere in the image's code, so it would have nothing to fuse.
5. **Indirect threading** - gforth-itc, fig-Forth, eForth, JonesForth: a
   code field per word. Slower, classic, and a distinct ancestor.
6. **Stack caching with several states** - Ertl's work behind gforth:
   handlers per cache state, generated like gen-tos. A single fixed
   two-register state lost in lab/dispatch; several states should not.
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
