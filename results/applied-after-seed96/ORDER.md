# The after-seed-96 batch - to apply at chain A's processing, before chain B's lists (Iterations 706-709)

Seed 96 is processed (704) and no seed run is planned: process-followup.sh applies no batch, so the chat processing chain
A (the new roles' screen - results/drafts/new-roles-plan-705.md) applies it by hand on master, first: `sh
tools/batch-check.sh` (PASS), the two lines below, a commit, then process-records' move by hand (`git mv results/pending
results/applied-after-seed96`, the citations followed - HANDOFF-REFERENCE.md, step 6). Chain A's x86 readings are not
touched by it (x86 engines byte-identical); chain B and the export measure and ship the ARMv7 engines it builds.

    git apply results/applied-after-seed96/arm2at-after-seed96.patch
    git apply results/applied-after-seed96/armcheck-after-seed96.patch
    git apply results/applied-after-seed96/ticker-after-seed96.patch
    git apply results/applied-after-seed96/rtsc-after-seed96.patch
    git apply results/applied-after-seed96/sysstubs-after-seed96.patch
    git apply results/applied-after-seed96/imagemsg-after-seed96.patch
    git apply results/applied-after-seed96/wends16-after-seed96.patch
    git apply results/applied-after-seed96/counters-after-seed96.patch

batch-check (711, on 1cf8713 - 8 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**arm2at-after-seed96.patch** (engine/vm-lab.c, tools/gen-msc.py, tools/gen-tos.py) - 2@ and 2! read and write the cell
pair through a one-byte-aligned type (CELLU, `aligned(1), may_alias`), in the engine's handlers and in the two stack
rewrites that restate them (gen-tos.py for tos=1, gen-msc.py for msc). Why: at tos=1 the two cell loads are adjacent with
nothing between, and GCC joins them into ARMv7's LDRD (2! into STRD), which traps on an address not word aligned - the
corpus's `HERE 1 ALLOT  HERE 1 ,  ... 1ST 2@` (Forth 2012 leaves an unaligned `,` ambiguous; the Hayes test does it).
Clang does the same (Iteration 707's fuzzer, lab/evolve/fuzz-designs.py --arm: 3 clang tos=1 designs with 2@ and 2!
as primitives - 022d7fd86e, b575c8d1ff, cb03515bc4 - each died on 10 of 30 programs under qemu at a cell pair 2 bytes
past alignment; 0 of 90 with the patch - results/drafts/fuzz-707.md). Linux on the Tegra fixes the access up, so its readings stood (88 such designs measured in the final check); qemu-user
does not, nor a kernel set to signal - the ARMv7 pre-flight's 4 false deaths (results/drafts/arm-preflight-705.md).
Tested (results/drafts/arm2at-706.md): x86 - 24 designs expressing 2@ (tos 0 and 1, GCC and clang, the JIT and not)
built by master and by the patched tree at both widths, every engine and image byte-identical (48 of 48;
results/drafts/arm2at-bytes-706.py); ARMv7 under qemu-arm - the GCC builds (arm-linux-gnueabihf-gcc 13) of the 4 that
died, of 7fb40ff7ba and 58479dda0a (dead before, measured on the Tegra) and 2 more, 8 of 8 alive and identical on fib and
apps, the engines 0-4 bytes larger; 14 more spread by speed with the hand-made stages, 14 of 14 alive; clang's 10 of 10.

**armcheck-after-seed96.patch** (tools/arm-cross-check.py) - fib and apps compared as evolve.py compares them (run()'s
OUT_LAST): the "Redefining: X" lines dropped first. Why: s0-cell DIFFERED on apps by two such warnings and nothing else -
a cell design's kernel has no LIT, or CALL, for shellmix (and sim16) to redefine, which evolve.py already allows for.
Tested: s0-cell IDENTICAL after (DIFFER before, on master too), d3496fcc6c beside it the same.

**ticker-after-seed96.patch** (lab/evolve/chainctl.py, lab/evolve/next-run.sh) - the machine's line (701: load, memory,
swap, clock, heat, AC, a late tick) every 5 minutes beside an experiment step too: next-run.sh starts chainctl.py's ticker
before the step's tool with TICK_LABEL=lab/evolve/TOOL and stops it after (on a failure too); the ticker prints "TOOL
running" in place of the evolution's progress when TICK_LABEL is set. Why (results/drafts/premortem-roles-707.md): only a
seed run had the ticker - next-run.sh's experiment mode exits before it - so a stall like seed 96's generation 0 under a
follow-up chain's laptop sessions would be pooled unseen; chain A has none. Tested: `sh -n`; the ticker beside a
sleeping process, TICK_EVERY=2, with TICK_LABEL ("lab/evolve/loadtest.py running; the machine: ...") and without (the
seed run's line, unchanged); batch-check below.

**rtsc-after-seed96.patch** (engine/rt-linux-x86_64.c, engine/vm-lab.c) - the engine's one system call (the SYSCALL
operation) through SYSCALL6: rt_syscall6, six arguments and the same errors (-1, errno), where the runtime is linked at
x86-64; elsewhere the variadic syscall as before. Why: the runtime's variadic syscall made the compiler save every
argument register - 241 of the smallest engine's 4,784 bytes of code (nm -S); 257 gave open the same fix, not syscall.
Tested (results/drafts/rtsc-707.md, results/drafts/rtsc-707.py): 20 designs - the 8 smallest, 12 spread over tos, GCC,
clang and the JIT - by master and by the patched tree: at 8-byte cells -192 to -304 bytes each, at 4-byte cells
byte-identical, all 40 builds alive with fib and apps as s6. It changes every x86-64 engine's bytes, so chain B's sizes
are 192-304 bytes below chain A's for the same designs; their speeds it should not touch (a system call is rare - the
I/O is buffered).

**sysstubs-after-seed96.patch** (engine/rt-linux-x86_64.c) - at x86-64 with clang, the runtime's 19 system calls whose C
arguments are the kernel's own registers (rdi, rsi, rdx; the fourth moved rcx to r10) are 4-5 byte assembler stubs: the
number into rax, a jump to one shared tail (syscall; -errno to -1 and errno), as dietlibc's unified syscall; rt_syscall6
(rtsc above) shuffles into the same tail. Each stub in its own section, so --gc-sections keeps only those called. GCC
keeps the C wrappers (`#if defined(__clang__)`): its LTO builds - 99 of the front's 103 GCC designs - inline them, an
inline syscall clobbering two registers where a call clobbers every caller-saved one, and the stubs grew its large -O2
engines by 64-192 bytes. Why: Iteration 709's sweep (results/drafts/sweep-709.md) - every wrapper inlined sc() and
ok(), about 300 of the smallest engine's bytes. Tested: 20 designs (the 8 smallest, 12 spread by speed) and 14 GCC ones,
built with the batch before it and after (rtsc-707.py): clang -176 to -400 bytes (the smallest 4,768 to 4,576), every
GCC engine +0 - GCC's preprocessed runtime is byte-identical to before (`gcc -E -P`), and the i386 runtime's too
(RT_PORTABLE_ONLY), so the 4-byte engines are unchanged by construction; all 34 alive, fib and apps as s6.

**imagemsg-after-seed96.patch** (engine/vm-lab.c) - every refusal of an image's contents is one message from one
function, bad_image: `not a RelF image (N)`, N a check digit (1 the magic - another encoding or cell width, 2 a newer
CV8 format, 3 CV8 features not built in, 4 the header truncated, 5 an impossible thread count, 6 too many DOES> tails,
7 the escaped band, 8 and 9 SOD16's byte-granular headers and a DOES> tail outside the chain; the list in the comment
above bad_image). Kept: the file not opened or not read, memory, usage, the stack and fault messages. A user-visible
change: the seven texts become the digit (the owner told, 709). "not a RelF image" starts the message because relf's
crash fuzzer matches the phrase; nothing else in the tree reads these texts. Not `cold`: GCC then moved L_esc's call
in virtual_machine to .text.unlikely and the dispatch table's label differences did not assemble. Why: the sweep - the
seven messages were 374 of the smallest engine's 1,072 bytes of rodata. Tested (results/drafts/sweep-709.md): the 34
designs above at 8-byte cells, -226 to -458 bytes (the smallest 4,576 to 4,230), and the 20 at 4-byte cells (i386),
-234 to -336; all 54 alive, fib and apps as s6; the digits by hand on the smallest's i386 engine (a text file (1), a
cut header (4), the version raised (2), a feature bit set (3), each exit 2; the image itself runs); ARMv7 - 10 of the
ARM list spread by speed, cross-built by clang (tools/arm-cross-check.py, qemu-arm), 10 of 10 alive and identical on fib
and apps. With sysstubs and rtsc, chain B's x86-64 engines are about 400-1,100 bytes below chain A's for the same designs (GCC's the least).

**wends16-after-seed96.patch** (tools/layout.py, forth/cross-cv8.4, tools/selfhost-check.sh) - the JIT's table of the image words' ends (jit_wends, Iteration 489:
the decoder's end for a word reached without its header) written two bytes a number where every end is under 64 KB, as
every image is (8-11 KB): it was 2,568 bytes of a jitx engine's 5-6 KB of rodata, 321 rows of two 4-byte numbers. The C
reads it as before (jit_wends[m][0] == o, cbase + jit_wends[m][1]); an image past 64 KB keeps the 4-byte form. Why: found
while building the gene jitdead (Iteration 710) - the table appeared in a design without jitx. Tested: ten JIT designs
(the four smallest, six spread by speed; results/drafts/jitdead-710.md), each built before and after at both widths: the
six jitx engines -1,120 to -1,152 bytes at 8-byte cells (923951e8ab 33,608 to 32,472), -1,096 to -1,176 at 4-byte, the
four without jitx unchanged (the table unused there); all 20 alive, fib and apps as s6. The self-hosting compiler
writes its image's table the same way (SAVE-JIT-LAYOUT, by the largest end: JW-MAX), and selfhost-check.sh puts either
form in the engine for A: small-jit's self-hosting check PASS at both widths, its engine for A with the two-byte table.

**counters-after-seed96.patch** (lab/evolve/README.md, lab/evolve/countfit.py, lab/evolve/evolve.py,
lab/evolve/loadtest.py, tools/cputime.c, tools/run-tests.sh) - the PMU's counts kept beside the time: cputime reads
branches mispredicted and last-level misses too (each absent where the PMU lacks it, as cycles and instructions were);
evolve.py keeps each run's counters, their medians per workload and side (measure(): LAST_CNT) and a record's "cnt"
([instructions, cycles, mispredictions, misses] a workload, beside "raw"); loadtest.py's line per design - chain B's -
carries "cnt", the first idle measure's, the design's and s6's; lab/evolve/countfit.py fits the time to them per
workload, held out by design, and reports the error and the speed's ranking (--self-test in run-tests). Why: Architect
Labs' Frostbite searched with Arcmodel, a function over counters fitted to RTL within 5 % (results/drafts/frostbite-711.md);
a model of our time from one run's counts would be a screen without rounds - chain B's ~60 designs at 10 rounds on
three machines are the data to fit and judge it (707's "INSTR beside time", set up). Nothing is selected or scored on
the counts; the timing is unchanged (two more events opened at exec). Tested: here, without a PMU, the lines are absent
and nothing changes; with a cputime that adds them, measure() keeps the medians per workload and side, through the
one-round-first state too, and a record's "cnt" comes out [instr, cycles, brmiss, llcmiss]; countfit.py reads both line
forms (records, loadtest's) and its self-test finds a known model (1.5 % median error, 19 % with instructions alone).
