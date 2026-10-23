# Five answers to the scouting prompt - verified, merged, weighed (Iteration 480)

The owner sent results/drafts/scout-prompt-479.md to other models and shared five answers. Their sources were checked
here (GitHub for the repositories, searches for the papers); the items are merged across answers and weighed against
what this project has and what it measured this session.

## Checked

- **Exist, as described**: copapy and pelfy (MIT; copapy's README lists x86_64, ARM32 Cortex-A and Cortex-M, ARM64,
  RISC-V; stencils taken from ELF relocations, a stencil's final jump dropped - our method), buxn-jit (MIT) and its
  blog post on JIT-ing a stack machine with SLJIT, vshymanskyy/interp (MIT), ncw/ccforth (MIT; a Forth-to-C compiler
  with a benchmark set), frno7/frth (GPL-3), WAMR, STOKE. Dave Mason's "Threaded Execution as a Dual to Native Code"
  (MoreVMs 2023: threaded and native code kept as parallel implementations, seamless transitions) and his IWST 2023
  paper (threaded code and CPS native code interleaved even within a method, native about 4 times faster) - and on his
  profile a 2026 paper, "A Copy-and-Patch JIT for Threaded Interpreters", newer than any answer. Gregg et al.,
  "Optimizing code-copying JIT compilers for virtual stack machines" (a DSL and tool generating stack-optimized code for
  VM instruction sequences, choosing the most useful for a code-copying compiler). The copy-and-patch JIT for R
  (Kocourek, Krikava, Vitek, VMIL 2025) and its MPLR 2026 sequel. Shannon and Bailey's EuroForth 2006 paper.
- **Not as claimed**: Shannon and Bailey allocate a stack machine's local variables to stack positions - a compiler for
  stack machines, not register allocation for a JIT's stack cells. Wasmtime and Cranelift have no interpreter tier to
  replace on the stack, so "OSR in Wasmtime" is doubtful. No EuroForth "benchmark corpus" exists - the proceedings are
  papers. The MOEA Framework's author is David Hadka. Uxn is not on GitHub (it lives on sourcehut). RPyForth and Gforth's
  instruction-pointer paper were on the reviewed list already.
- **Found on the way**: Prokopski and Verbrugge, "Compiler-guaranteed safety in code-copying virtual machines" (CC 2008)
  and "Analyzing the performance of code-copying virtual machines" (OOPSLA 2008) - GCC made to guarantee what our
  stencil-check verifies after the fact.

## Weighed - what to do with them

**First - the problems measured here:**

1. **An inline cache for EXECUTE** (Brunthaler, "Inline Caching Meets Quickening", ECOOP 2010; the monomorphic caches
   of HotSpot; Gforth's hybrid threading for tokens). jitexec's stencil compares the token with the one it last saw at
   that site and calls its native code directly; a miss takes the helper. And a caller whose tokens lead to words that
   cannot be translated stays interpreted, rather than paying the trip - fcp's third.
2. **Partial translation: native regions with exits** (Mason's dual execution and his copy-and-patch JIT for threaded
   interpreters; WebKit's LLInt sharing frames with its JIT; Dalvik's chaining cells; for loop entry, Mosaner et al.'s
   OSR by loop reconstruction and D'Elia and Demetrescu's OSR distilled). Our interpreter and native code already share
   the data stack in memory and the return stack through jit_rp, so leaving native code at a bytecode boundary needs
   only the stack pointer, the top and the instruction pointer: a region ends in an exit stencil that hands those back,
   and the interpreter goes on at that ip. One operation without a stencil then costs a region boundary, not the word
   and every caller; and a long word becomes several regions - JIT_MAXOPS no longer refuses it.
3. **What the selection sees** (one answer's design change): the JIT's coverage counted in each measurement - the
   share of dispatches native, transitions, refusals by cause (jitapps.py has the means); feature kernels the six lack:
   EXECUTE with one target and with several, a long word with one unsupported operation, a loop mixing both. ccforth's
   benchmarks (MIT) are workloads we may copy; Chen, Revels and Edelman's robust benchmarking for the noise.

**For the ports (i386, ARMv7):** copapy's ARM32 relocation handling (MIT - code we may read and adapt), CPython's
stencil trampolines, Android ART's Thumb-2 fixups (Apache-2.0), ARM's cache-maintenance guidance - and GCC's
__builtin___clear_cache, which may call a libgcc helper: to be checked against our engines' no-C-library rule.

**Later:** register allocation beyond the cached top (Ertl's thesis, LaTTe, linear scan, trace register allocation,
Titzer's baseline-compiler comparison); Gregg et al.'s sequence selection for stencils; Prokopski's compiler-guaranteed
safety beside stencil-check. **For the factoring gene** (results/drafts/more-projects-478.md): Clausen et al.'s Java
bytecode factoring (about 15% smaller), Evans and Fraser's grammar rewriting, Hu, Zhao and Scholz's Re-Pair
superinstruction synthesis (VMIL 2024), Latendresse and Feeley's Huffman bytecode with fast decoding.

**Not for us**: Uxn, MicroPython's varints (CV8 has them), STOKE, V8's Sparkplug, Wasmtime, frth (GPL-3), WAMR and the
MOEA Framework as code (ideas noted), ret2spec (a caution only).

**The answers**: the two that cited papers with their claims (code copying, inline caching, Mason, OSR, compression)
were the most accurate; one contributed the best idea about method; one repeated two reviewed items; one made two
claims that do not hold.
