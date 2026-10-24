# c4 and its family - what they hold for this project (Iterations 459, 462)

The owner asked (while seed 68 runs) for a deep dive into EarlGray/c4 and AoiKuiyuyou/AoikC4x86Study, a search for
derived and similar projects, and which of their ideas apply here. Reusable facts first, then what applies.

## The projects (October 2026)

| project | what it is | size | licence | link |
|---|---|---|---|---|
| rswier/c4 | the root: a self-hosting C subset (int, char, pointers, if/while, enums) compiled in one pass to a stack VM that runs at once; four functions - next (tokens), expr (precedence climbing), stmt, main (declarations and the VM) | ~500 lines | GPL-2.0 | github.com/rswier/c4 |
| EarlGray/c4 (c4x86.c) | an x86 (i386) JIT for c4's VM by Dmytro Sirenko, 2014: one machine-code template per opcode, the working value in eax, operands popped into ecx; two passes - the first stores each opcode's native address in its own cell, the second patches jump offsets; i386 only, not self-hosted, no register allocation | 86 lines (550 with c4) | GPL-2.0 | github.com/EarlGray/c4 (JIT.md) |
| AoiKuiyuyou/AoikC4x86Study | the same two files with line-by-line comments - the easiest reading of both | - | GPL-2.0 | github.com/AoiKuiyuyou/AoikC4x86Study |
| lotabout/write-a-C-interpreter (xc) | c4 rewritten for clarity, with a step-by-step tutorial (English and Chinese) | ~4.4k stars | GPL-2.0 | github.com/lotabout/write-a-C-interpreter |
| jserv/amacc | c4's infrastructure grown into an ARMv7 compiler: JIT or ELF executables, C89 statements but typedef, structs, unions; about 70% of gcc -O0 | ~2,400 lines | (check) | github.com/jserv/amacc |
| HPCguy/Squint | AMaCC's follow-on (mc.c) with a peephole optimiser over its ARMv7 output: about half the instructions executed, sieve 6x faster, at gcc -O1 on several benchmarks; floats, ELF, dynamic linking; the optimiser itself warned as buggy | 4,150 + 5,300 lines | (check) | github.com/HPCguy/Squint |
| jserv/shecc (similar, not derived) | a self-hosting C subset for ARMv7-A and RV32IM, its own code generator, SSA middle-end, register allocation | - | BSD-2 | github.com/jserv/shecc |
| Marc Feeley's tinyc | tokens, syntax tree, bytecode, VM | 284 lines | - | github.com/HPCguy/MarcFeeleyTinyc |

Also: Thorsten Ball's walk through c4 ("Exploring the c4 compiler", 2024); HPCguy's curated list of tiny C compilers
(github.com/HPCguy). Classics outside the family: Bellard's OTCC and TCC, chibicc, SectorC, "A Compiler Writing
Journey". A name clash: ForthHub's list of Forth systems has an unrelated "c4", a Forth inspired by Tachyon and ColorForth.

**Licences**: c4 and what copies its code are GPL-2.0 - their ideas are free to use here, their code is not without the
GPL; shecc is BSD-2.

## What applies here

**1. Our JIT already has what c4x86 and Squint teach - checked in engine/jit.c.** c4x86 keeps the working value in a
register and expands each opcode from a template: our JIT does that with the cached top of stack and stencils compiled
from C. Squint's gains come from removing a stack VM's memory traffic and fusing patterns; ours has jitk (the top two
or three cells kept in registers across stencils, gen-jitk.py), immediate forms (S_ADDI, S_ADDI32 - a literal folded
into the add) and a fused compare-and-branch (S_DUP_GTI_BR). Nothing there to add without measuring first.

**2. The gap these projects point at: no JIT at 32 bits.** The JIT is built only on x86-64 (jit_on(): the machine must
be x86_64). The evidence that it is the 32-bit gap: the 64-bit fronts' fastest without the JIT (seed 65's ab16f60a0c,
0.304) is where the 32-bit fastest sit (seeds 66-67: 0.33), and the JIT's designs run at 0.115-0.12 - about 2.6 times
faster. c4x86 shows how small a template JIT for i386 can be; AMaCC and Squint generate ARMv7 code from stack-machine
code - our two non-JIT targets, x86-32 (dream's 32-bit build) and 32-bit ARM (the Tegra). **Proposed, the owner's
call**: the stencil JIT ported to i386 first (the nearest: the same stencil method, fewer registers, R_386 relocations,
cdecl), measured on dream's 32-bit build; ARMv7 later, with AMaCC, Squint and shecc as references (shecc's code usable
under BSD-2; the others' ideas only).

**3. A cheap probe before any peephole pass.** Squint's yardstick is instructions per source line. A JITDUMP hook (the
JIT's buffer written out at exit; JITLOG today logs only refusals) and objdump on fib's and loop's code would count
what jitk leaves - register-to-register moves, stores reloaded at once, jumps to the next instruction. Above ~10% of the
emitted instructions, a Squint-style pass over stencil boundaries could pay; below, it would not.

**4. A workload: an interpreter written in Forth.** c4's VM - one loop dispatching some forty opcodes - written in
Forth and running a fixed bytecode program is a classic nested-interpretation workload: dispatch inside Forth code,
which none of the six selection workloads is. A candidate held-out workload, or a footprint-style check (optional).

**5. For Fern** (results/drafts/fern-design-457.md, its own chat) - *obsolete here (Iteration 510): Fern is its own
project now, which has this section; kept for the history only*:
- **c4's frames are Fern's locals**: ENT (a frame set up), LEA (a slot's address), LEV (the frame torn down) - FRAME,
  L@ / L!, UNFRAME - proven in a self-hosting compiler.
- **c4's structure is Fern's**: a tokenizer, precedence climbing in one expression function emitting code as it parses,
  a statement parser; write-a-C-interpreter walks through each step.
- **c4's -s listing** (each source line with the code generated for it) - worth copying: Fern's listing of the Forth it
  generates shows its overhead plainly.
- A sibling for that chat: a C front end in c4's style emitting Forth words - c4's VM maps almost one to one onto Forth
  (IMM a literal, LI and SI @ and !, LC and SC C@ and C!, BZ 0BRANCH, JSR a call) - C programs as workloads, and a
  second language.

## The second pass (Iteration 462): who cites c4, and the literature behind our JIT

The owner asked for a deeper search - pages, posts and projects referencing c4, c4x86 and the rest.

**More of c4's circle.** The Hacker News thread of November 2014 ("C4 - C in 4 functions"); Thorsten Ball's walk-through
(2024); srhuang's HackMD trace of c4 (2019), which lists comzyh/c4's commented branch, EarlGray's JIT, **rswier's own c5 -
c4 with a syntax tree and a code generator, in one commit of rswier/c4** (d8e61a8), write-a-C-interpreter and AMaCC; a
self-hosting compiler to WebAssembly that names c4 as its model (minizig, on Codeberg); Kray-G/kcs, scripting in C with a
JIT (x86-64) and a VM - prior art for Fern.

**The literature our JIT belongs to** - the most useful find:
- **Ertl and Paysan, "Code-Copying Compilation in Production" (EuroForth 2025)** - Gforth has copied GCC-made code
  snippets since 2003, on Alpha, ARM A32/T32 and A64, IA-32, AMD64, PowerPC, RISC-V and more, and with all its
  optimisations it runs about as fast as SwiftForth's hand-written compiler; VFX Forth, with register allocation within
  basic blocks and aggressive inlining, about twice as fast. It records the hurdles: code reordering, alignment padding,
  deduplication and duplication by newer GCCs, register allocation, cache flushing, control-flow protection, clang.
- Ertl and Paysan, "The Performance Effects of Virtual-Machine Instruction Pointer Updates" (ECOOP 2024); Ertl and
  Gregg, "Retargeting JIT compilers by using C-compiler generated executable code" (PACT 2004) - the copy-and-patch
  prototype for Gforth; stack caching with dynamic superinstructions (IVME 2004).
- Xu and Kjolstad, "Copy-and-Patch Compilation" (OOPSLA 2021) - stencils as functions with holes, extracted from object
  files by their relocations at build time; **CPython's JIT** (PEP 744, Python 3.13) - stencils compiled from one
  template per micro-op, their holes the relocations llvm-readobj reports, chained by musttail; and **Deegen / LuaJIT
  Remake** (Apache-2.0) - a copy-and-patch baseline JIT generated automatically, with register pinning, the GHC calling
  convention and hot-cold splitting.

**JIT back ends that reach our 32-bit targets**: abdimoallim/jit (a header-only C library for i386, x86-64, ARM32,
ARM64, RISC-V 64); sljit and GNU lightning (from memory, not this search: both cover 32-bit x86 and ARM). MIR does not
go below 64 bits.

## Ideas for this project, from the second pass

Checked against the code: **already ours** - the copy-and-patch JIT itself (its holes found by magic values, as in
Ertl and Gregg 2004), stack caching across stencils (jitk), dropping the jump when the next stencil follows (tailnext),
genes for -fcf-protection=none (nocet: Ertl and Paysan measured endbr64 at 1.45 times the instructions, 1.04 the cycles)
and -falign-labels=1 -falign-jumps=1 (align1). **Not for us**: the IP-update optimisation - the JIT keeps no IP, and an
interpreter needs code copying for it.

New, proposed (the owner's calls):
1. **A relocatability check for stencils** (Gforth's way: the snippets built twice, once padded; any byte that differs
   outside the known holes is a reference out of the stencil). Today a stencil that GCC gives a call (memset, a stack
   check) or a PC-relative constant is copied as if it were safe. Most useful now, with the i386 port, and for any future
   compiler.
2. **Stencils from the object file's relocations** (CPython, Xu and Kjolstad, Gforth's own suggestion): the clean way to
   32-bit ARM - movw/movt and branch relocations name every hole, compile the stencils -marm (no Thumb), and flush the
   cache (__builtin___clear_cache - check it emits code there, as Ertl advises).
3. **The return-stack pointer pinned in a register** across stencils (Deegen's register pinning; Ertl's global register
   variables - 12 general registers on AMD64): today jit_rp lives in memory, so every >R, R>, I and loop step touches it.
   A gene, "jitrp".
4. **Inlining beyond one operation** (VFX Forth's lead): jitinl inlines only one-operation words; calls and returns are
   idiomatic Forth's most frequent block boundaries. A level for jitinl - words of up to 4 or 8 operations.
5. **-fno-tree-vectorize** as a gene (Ertl: it removed GCC's register shuffling at Gforth's dispatch) - none today.
6. **The Forth application benchmarks** Gforth is measured on - benchgc, brainless, cd16sim, lexex, fcp, and siev,
   bubble, matrix, fib - as held-out workloads beside sieve: real programs, the question the footprint check asks.
