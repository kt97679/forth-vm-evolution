# RELF.md - this lab and RelF

**The immediate goal of this project is to be the base of RelF** (the owner, Iteration 356):
<https://github.com/kt97679/relf> - Relative Forth, a self-hosting Forth and a POSIX shell written in
it. RelF runs one byte-coded image on two engines: CV8 (engine/cv8.c, portable C) and relfasm64
(x86-64, assembled by relf itself); `cross.4` compiles `kernel.4` into the images byte for byte, and
gforth must agree; every change is built and tested at both cell widths. Its real workload is the
shell (relfsh). It also has a native back end (Forth to x86-64), whose CV8 counterpart is this lab's.

## What relf asks of this lab

relf's Iteration 716 (vendor/relf/tree/docs/CV8-LEDGER.md), from CV8's profile of the realistic shell
script (18.4 million dispatches, 10.2 % calls and returns): not done in CV8 - **XF@ and XV@ (4.9 %
of dispatches), DEFER (2.5), (+LOOP) (1.7), PICK (1.5), fused pairs (some 8 %)** - "all of them new
instructions, so forth-vm-evolution's to inform"; and, outside the instruction set, the cross
compiler's constants and inlining for the kernel's own words.

## How a result reaches relf - the adoption criteria

- **Measured on relf's workloads**, with relf's tool: vendor/relf/tree/tools/bench-vm.py (paired,
  interleaved CPU time, bootstrap intervals) on tests/bench-vm - loop, fn, str, arith, realistic
  (shell scripts) and start (the shell's startup). On this VM, relf master's CV8 shell (SCALE=1):
  realistic 84 ms, loop 91, fn 51, str 49, arith 70, a start about 1 ms (Iteration 356).
- **Producible by relf**: an image format must come from relf's own cross.4 (not this lab's
  tools/layout.py), and run on both engines - so a format change costs relf cross.4, opcodes.tab
  and relfasm64.4 together; a C-engine-only change costs cv8.c alone.
- **Portable**: both cell widths (relf builds the 32-bit engine -fno-pie -no-pie), and AArch64 and
  RISC-V under qemu, as relf checks them; nothing x86-only for CV8 (the JIT stays this lab's research).
- **Passing relf's gates** before it is proposed: `make verify` - CORE on both engines and both
  widths, the shell suites, `make check-images`, the gforth build.

## The plan (Iteration 356; status kept here)

1. **Done**: vendor/relf follows relf master (tools/update-relf.sh, default origin/master; the
   sources under vendor/relf/tree, building and running there); LICENCE.md GPLv2 only.
2. **Done (Iteration 357): tools/relf-ab.sh** - A, vendor/relf/tree as vendored; B, with candidate
   patches (images rebuilt when the instruction map, kernel.4 or cross.4 change); B must fail nothing
   in relf's own `make test` that A passes (A's failures recorded once per vendored commit - here,
   none: relf passes its whole suite on this VM); then relf's bench-vm.py on loop, fn, str, arith,
   realistic, start. vendor/relf/tree now carries relf's tests and examples (what make test needs).
   **The noise floor here** (A against A, 12 rounds, SCALE=2): medians 0.98-1.06, 95 % intervals
   about +-10 % (start +-30 %) - this VM gates correctness and shows large effects; the ledger's
   candidates (1.5-5 % of dispatches each) are the laptop's to measure (relf's own reports are).
3. **Done (Iteration 358): tools/relf-pairs.py** - the realistic script by instruction and by adjacent
   pair (results/relf-pairs-realistic.md): VAR@ 15.2 % of all dispatches; pairs VAR@ VAR@ 4.2 %, VAR@ +
   3.1 %, 0= ?BRANCH 2.3 %, + @ 1.8 % - the top ten about 18 %. **The constraint** (relf's QUESTIONS.md
   A15): 64 one-byte opcodes, kept for the two-bit tag; fused pairs went at 536 for it. A new fused
   instruction displaces an operation to the escape band (a dispatch more where it runs); one in the
   escape band saves nothing. **The budget (Iteration 359; --all, the five scripts)**: VAR@ VAR@ 4.45 % for
   LIT64's slot (0.03 %), VAR@ + 2.85 % for ?BRANCH8's (0.04 %), 0= ?BRANCH 2.31 % for R@'s (0.13 %) - the
   top three net about 9.4 % of dispatches (chains overlapping, less). **Next**: those three as one patch
   to relf - opcodes.tab (the three displaced to the escape band, their slots reused), cv8.c's handlers
   (VAR@ VAR@ two slot operands; VAR@ + one), the compilers' peephole (cross.4's PEEP-VAR, kernel.4's
   run-time compiler), relfasm64.4's handlers - through relf-ab.sh's gate here, measured on the laptop.
   **Iteration 360, the first: `0= ?BRANCH`** (results/relf-patches/): one opcode 0=?BRANCH, fused by
   kernel.4's IF and WHILE - **relf's whole make test passes**; the realistic script **2.10 % fewer
   dispatches**; its time within this VM's noise - for the laptop (`sh tools/relf-ab.sh -r 30 -s 4
   results/relf-patches/zeq-qbranch.patch`). Next: VAR@ + and VAR@ VAR@; UNTIL's branch.
4. Classify this lab's genes by what relf would pay to adopt one (C engine only; image format;
   kernel words; x86-only) - a relf profile for the search; and relf's shell workloads in it.
5. This lab's 32-bit engines built -fno-pie -no-pie, as relf's are (its two-width measurements
   otherwise pessimistic: a register spent on the PIC base, Iteration 353).
6. A port list from knockouts on the best relf-profile design, each item measured on relf's
   workloads, ported as a patch passing relf's gates.
