# c4 and its family - what they hold for this project (Iteration 459)

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

**5. For Fern** (results/drafts/fern-design-457.md, its own chat):
- **c4's frames are Fern's locals**: ENT (a frame set up), LEA (a slot's address), LEV (the frame torn down) - FRAME,
  L@ / L!, UNFRAME - proven in a self-hosting compiler.
- **c4's structure is Fern's**: a tokenizer, precedence climbing in one expression function emitting code as it parses,
  a statement parser; write-a-C-interpreter walks through each step.
- **c4's -s listing** (each source line with the code generated for it) - worth copying: Fern's listing of the Forth it
  generates shows its overhead plainly.
- A sibling for that chat: a C front end in c4's style emitting Forth words - c4's VM maps almost one to one onto Forth
  (IMM a literal, LI and SI @ and !, LC and SC C@ and C!, BZ 0BRANCH, JSR a call) - C programs as workloads, and a
  second language.
