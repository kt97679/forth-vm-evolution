# Prompt for other models: find projects and ideas we can reuse

You are helping a research project find external projects, papers and techniques whose ideas it can reuse. Read the
context below, then answer in the format at the end. Only suggest what you can point to: a URL to a repository, a paper
or a page. If you are unsure that something exists or says what you remember, say so. Do not re-suggest anything under
"Already reviewed" unless you bring a specific new angle.

## The project

- An evolutionary search over Forth virtual-machine designs. Each design is a genome of about a hundred genes: the
  bytecode encoding, dispatch, stack caching, superinstructions, compiler flags, a JIT and its options. Every design is
  built (a C engine compiled for it, and a Forth image made by a converter), checked for correctness (a Forth test
  corpus) and measured.
- Objectives, as a Pareto front: the smallest binary plus image in bytes, the highest speed relative to a hand-made
  reference design, the lowest memory; simplicity preferred when the numbers are close.
- Platform: Linux user space, little-endian only. x86-64 is the main machine (an AMD Ryzen 7 PRO 8840HS laptop); 32-bit
  x86 and 32-bit ARM (ARMv7, a Tegra board that compiles natively with GCC only) are checked too. Engines link no C
  library. Images are 5-30 KB; the smallest whole design is about 14 KB.
- The current design family (CV8): a byte-coded VM. One-byte operations assigned by frequency, plus an escape page;
  calls of 2-4 bytes with a 2-bit tag encoding; literals of 1, 2, 4 or 8 bytes; byte-granular headers; one-byte calls
  to the hottest words; top-of-stack caching; static and run-time-fused superinstructions; loop opcodes.
- A copy-and-patch JIT: stencils compiled from C, copied and patched at run time (x86-64; an i386 port tested), with
  options: return-stack operations, a register cache of the top 2-3 stack cells across stencils, inlining of
  one-operation words, tail calls, loops, native UM* and UM/MOD (with a throw path back to the interpreter on a zero
  divisor), DOES>-defined words, EXECUTE through a helper. Every stencil is checked to be relocatable.
- Selection workloads: six small kernels (compiling Forth source, fib, a test corpus, a counting loop, bubble sort,
  Ackermann); sieve is held out.

## What we learned recently - why we are asking

- On real applications (Appbench's two chess programs and a CPU simulator, plus our own CPU simulator, mark-sweep
  collector, scanner generator and genetic algorithm), the fastest evolved designs kept only about 1.3 times speed over
  the reference, against about 7 times on the selection's kernels. The JIT translates a word whole or not at all, and
  one operation without a stencil kept whole words, and every caller of them, interpreted.
- With more of the language covered (multiply and divide, DOES>, EXECUTE), the applications reached about 2.9 times.
  What remains: EXECUTE of a word that cannot be translated now costs an expensive trip into the interpreter and back
  (one application got a third slower); long words exceed the JIT's size limit; and the selection's kernels never use
  these features, so the search cannot weigh them.

## What we are looking for

Projects, papers or techniques with concrete, reusable ideas for any of:

1. **JIT coverage for stack-machine or Forth code**: translating part of a word, with native and interpreted code mixed
   and cheap transitions between them; indirect calls (EXECUTE, deferred words) - inline caches, call-target
   speculation; long words - splitting, or on-stack replacement.
2. **Cheap transitions between interpreter and native code** in a C VM without a C library (we use GCC's
   __builtin_setjmp and __builtin_longjmp).
3. **Register allocation for stack code** in a template or copy-and-patch JIT, beyond caching the top 2-3 cells.
4. **Copy-and-patch or template JITs on 32-bit ARM (ARMv7, Thumb-2) and i386**: stencils extracted by their relocations,
   literal pools, branch ranges, cache flushing.
5. **Code density**: whole-program factoring of bytecode into shared words, fast-decoding variable-length opcodes,
   dictionary and header compression, compressed bytecode with cheap decompression.
6. **Workloads**: permissively licensed, deterministic, self-checking Forth applications - or kernels that behave like
   applications: deep stacks, frequent calls, DOES>, EXECUTE, CATCH - for selection or held-out tests.
7. **Method**: automatic or evolutionary exploration of interpreter and VM designs, automatic superinstruction
   selection, measuring under noise and machine load, multi-objective search (island models, hypervolume), avoiding
   overfitting to benchmarks.

## Already reviewed - skip unless you have a specific new angle

c4 and its family (c4x86, AMaCC, Squint, shecc, write-a-C-interpreter); Gforth's papers (dynamic superinstructions,
code copying, stack caching, instruction-pointer updates; Ertl and Paysan's 2025 code-copying experience report);
copy-and-patch (Xu and Kjolstad 2021), CPython's JIT, Deegen and LuaJIT Remake; RPyForth (2026); Appbench;
nibbleforth, tokthr, zForth, paraforth, astil_forth, romforth, bee, milliForth, sectorforth; VFX Forth and SwiftForth as
references; sljit, GNU lightning, MIR. Since the first round (results/drafts/scout-answers-480.md): copapy and pelfy,
buxn-jit, interp, ccforth, frth, WAMR, Uxn, MicroPython, STOKE, V8 Sparkplug, WebKit's LLInt, Android ART and Dalvik;
Dave Mason's threaded and native dual execution; Brunthaler's inline caching with quickening; OSR (Mosaner et al.,
D'Elia and Demetrescu); Gregg et al.'s code-copying JIT, Ertl and Gregg's retargeting; Prokopski and Verbrugge;
Shannon and Bailey; LaTTe, linear scan, trace register allocation, virtual register machines; Clausen et al., Evans and
Fraser, Latendresse and Feeley, Hu, Zhao and Scholz; the copy-and-patch JIT for R; robust benchmarking (Chen et al.).

## Answer format

- At most 15 items, ranked by their expected value to us.
- For each: its name and URL; what exactly the idea is (two or three sentences); which of areas 1-7 it serves; why it
  fits our constraints (a C engine, no C library, Linux user space, x86-64, i386 and ARMv7, small images) or what would
  block it; the gain and cost you expect, if you can estimate them; its licence (code we may reuse, or the idea only);
  and your confidence that the source exists and says this (high, medium or low).
- Then the three you would try first, and why.
- Do not invent repositories, papers or numbers. If you remember something only vaguely, mark it low confidence and
  say how to find it.
