# This lab's genes, by what relf would pay to adopt one (Iteration 363; RELF.md item 4)

relf's CV8 is one byte-coded image on two engines - cv8.c (portable C) and relfasm64 (x86-64, by relf
itself) - its images made by its own cross.4, and its opcode set held at 64 one-byte opcodes for the
two-bit tag (QUESTIONS.md A15). So a gene costs relf according to what it touches:

| class | what adopting one touches | genes |
|---|---|---|
| **C engine only** - cheap | cv8.c and its build; no image, no opcode, the asm engine untouched | opt, compiler, regpin, d256, sharedcall, alignhot, guard, tailpn, bss, lean |
| **opcode set or image format** - dear | opcodes.tab, cv8.c AND relfasm64.4, cross.4 and kernel.4, relf's image tools (the lesson of Iterations 361-362: the inliner and image-audit know opcodes and formats by number); within the 64 one-byte opcodes, each new one a trade | enc, tag2, t2hot, t2wide, bytehdr, thinhdr, scale, varcall, doesfar, spec, supers, folds, ops10, opbody, opcall, opinline, rtimm, rtloop, rtloopall, rtiplus, rtfuse, rtempty, swapi, kfast, tfind, kinput, klookup, knumber, kstack, bfind, factor |
| **kernel words only** | kernel.4 (and cross.4 for the kernel's own code) | fsys, fbuf, abortif, hotinl |
| **x86-64 JIT - not for CV8** | a translator CV8 has no place for; relf's native back end is its own | jit, jitx, jitloop, jitinl, jitos, jittail, jitk, jitvar, jitimg (and the parked jithelp, jitre) |

Notes:
- **folds and fused pairs are what relf gave up in A15** - their return is through the budget's trades
  (results/relf-pairs-realistic.md), as the three patches of Iterations 360-362 are.
- relf already has a part of several: the top of stack in a register (tos), variable slots (varslot),
  an inliner with swept limits (hotinl's ground), CTABLE-FIND (klookup's ground).
- **Measured (Iteration 364; results/relf-patches/README.md): the cheap class does not transfer** -
  clang, -Os and pinned registers are each no faster for relf's cv8.c on its shell; d256 and guard
  pages it has already. Its genes belong to this lab's designs' whole combinations.
- Was: **the cheap class is where to look first**: each a change to cv8.c's build or code alone, testable at
  once on relf's own shell with tools/relf-ab.sh - compiler (clang against gcc: Iteration 352's knockouts
  found its 35 % 64-bit-only on this lab's fastest design), regpin, alignhot (hot handlers aligned), d256
  (one 256-entry table, no opcode-or-call test), sharedcall. A relf profile for the search: these and
  the kernel class free, the dear class priced by its trade, the JIT class off.
