# Prior work for an article: automatic design-space exploration of a small Forth virtual machine

I am preparing an article (for Habr and ForthHub) about a project that searches automatically for small, fast designs of
a Forth system. Before writing I need to know what has been done before, so that the article claims only what is new and
credits what is not. Please give references with links (papers, theses, projects, articles), say how close each is to
what is described below, and say "unsure" where unsure - I will check every reference.

## What the project does

- **A family of Forth systems** built from one kernel source: a cross-compiler (Python) writes the kernel's image in one
  of four encodings - cell-sized threaded code, a 16-bit token code with direct calls, a compact 16-bit token code with
  scaled addresses, and a byte code whose calls and operations share a two-bit tag (one-byte operations, two- to
  four-byte calls); the engine is C (computed-goto dispatch, linked without the C library, raw system calls).
- **About seventy genes** choose the design: the encoding, which primitives get folded or fused into
  superinstructions (static ones and ones made at run time), top-of-stack caching and register pinning, header formats,
  how variables are reached, compiler flags, and a copy-and-patch JIT (stencils compiled by GCC or Clang, holes patched
  at run time) with genes of its own (loops, the return stack, multiplication and division, EXECUTE, DOES>, fused pairs,
  a register-cache variant).
- **The search**: a multi-objective evolutionary algorithm (NSGA-II) over three equal objectives - binary + image bytes,
  speed (a geometric mean of seven workloads, including small applications, as a ratio to a hand-made reference design),
  and peak memory - and a fourth, the speed with 32-bit cells; a surrogate model screens children before they are
  built; every output is checked against the reference; held-out workloads and applications, and two other machines (an
  x86-64 desktop and a 32-bit ARM board), check that the winners generalise.
- **Findings so far**: the smallest designs are about 14 KB (engine and image together); the fastest run its workloads in
  about 0.13-0.15 of the reference's time, mostly through the JIT; a long list of mechanisms the search kept and the
  ones it consistently refused.

## The questions

1. **Automatic design-space exploration of interpreters or virtual machines** - by evolutionary or genetic search, by
   autotuning, by any search: who has explored a VM's or interpreter's design choices (dispatch, encodings,
   superinstructions, caching) automatically, rather than by hand?
2. **The techniques we combine** - superinstructions (static and dynamic), stack caching, threaded-code and token
   encodings, interpreter size/speed trade-offs, copy-and-patch compilation - the papers that introduced or measured
   them, especially for Forth (I know of Ertl's and Gregg's work, Gforth and vmgen; what else, and what in them is
   closest to a search over the same choices?).
3. **Multi-objective optimisation of program size against speed** - compiler-flag and phase-ordering search,
   superoptimisation for size, embedded VM design (e.g. for microcontrollers): what is close in method?
4. **What would be new**, judging from the above: the combination, the scale of the design space, the equal size and
   speed objectives, the JIT among the genes, the measurement discipline - or nothing, if it has been done.
5. **The two venues**: what Habr's and ForthHub's readers would find most interesting or familiar in this, and what they
   would expect to see (code, numbers, reproducibility).

## The answer I'd like

For each question: references with links and a sentence on how close each is; for question 4 a frank assessment; for
question 5 concrete suggestions. Mark what you are unsure of; a reference you are not sure exists is worse than none.
