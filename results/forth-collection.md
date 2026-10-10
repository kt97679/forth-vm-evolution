# The owner's Forth collection (Iteration 118)

~138 MB unpacked, 3,106 files, ~1,100 of them source: the owner's RelF history,
SOD32 and its descendants, eForth, FIRST/THIRD (IOCCC buzzard.2), Itsy,
3-instruction Forth, gforth 0.6.2, SP-Forth 3 and 4, bigForth, colorForth,
DSSP, the ANS test suite, benchmarks, and books (Koopman's Stack Computers,
Moving Forth, Thinking Forth, the ANS standard ...). Examined in /tmp, not
committed - except the ANS tests (freely distributable, tests/ans). Code may
be taken only from public-domain or permissive sources and from the owner's
own RelF; from GPL ones (SOD32 - GPL v2, gforth, bigForth) ideas only.

## What it holds for this project

**RelF's own history** (RelF/, relf_dev/). relf-0.2's readme tells the
origin: SOD32 by L.C. Benschop, too slow, sped up - and threaded code that
refers to a definition by its RELATIVE offset, hence the name. `opchaines.
sorted` is an early superinstruction count (vmlit vmdolist, vmdup vm0branch,
vmlit vmplus vmexit ...); RelF/stat word and pair statistics; vmll.4 and
vmhl.4 the virtual machine written in Forth. The owner's todo (CP866): make
`=` a primitive instead of `0=` (done), consider `-` and DOVAR as primitives,
implement D+ in Forth (with its definition) - primitive-set decisions, the
floor of results/deep-dive-2.md section 3, twenty years before.

**Minimal cores**, for "SOD32 from nothing": eForth's 31 primitives (RelF/
eforth/eforth.prims - arithmetic only UM+, no + ROT = or shifts); FIRST, the
language under the IOCCC's buzzard.2, from which THIRD (almost Forth) is
built; Itsy; 3ins4th; cmForth and colorForth.

**Optimizers and research** (ideas): gforth 0.6.2's peeprules.vmg and
super2.i (vmgen's superinstructions), SP-Forth's macroopt.f and spf_inline.f
(a peephole optimizer and an inliner for native code), CamelForth (Moving
Forth), Koopman's Stack Computers, Optimal Code Generation for Stack Machines.

**Benchmarks**: RelF/bench - ackermann (deep recursion), bubble (memory and
loops), sieve, fib - and bench.txt, the gforth versions of the old Great
Computer Language Shootout (heapsort, matrix, nested loops ...): execution-
heavy candidates for the selected workloads, where parse is over-weighted.

## The ANS test suite, run (tests/ans)

Gerry Jackson's 0.3 around Hayes's core.fr: lowercase, so tools/ans-upper.py
converts it; prelude.fth adds TRUE, FALSE and `.(`. A first run looked
perfect - every file to its end, nothing failing - and was vacuous: core.fr's
ACCEPT test read the next input line, the next file's INCLUDED, so none of the
nine other files ran (prompts/15: a check that cannot fail). With an empty
line for ACCEPT, on hand-made s6 and the fastest design: coreplus (18 cases)
and memorytest (13) pass whole; coreexttest stops at :NONAME, doubletest at
D-, exceptiontest at CATCH, filetest at COMPARE, searchordertest at ONLY,
stringtest at a helper, toolstest at AHEAD - word sets the kernel lacks; and
INTERPRET reads double literals (`1.`) as singles: `1. D.` prints 2^64.

**It found a divergence the gate cannot see**: with the stack-guard gene on,
an underflow kills the engine - "relf: return stack overflow" (for a DATA
stack UNDERFLOW), exit code 1, every buffered byte of output lost - where s6
and the same design without the gene print "Stack error DROP" and go on. ANS
leaves underflow to the implementation, but the message is wrong and the
output lost; neither the corpus nor the kernel workload ever underflows. 10 of
the 22 knocked-out front designs carry the gene.

## Next, from it

1. The guard gene's fault: flush the output, name the stack and the
   direction (the fault address against the guard pages) - or recover as the
   software check does.
2. The ANS suite as a held-out check (tests/ans): every design must give s6's
   output on the files that run - for genetic improvement first.
3. Execution-heavy workloads from the benchmarks (with parse held out).
4. eForth's and FIRST's cores as floors for the instruction-set search.

## Iteration 119: the guard fixed, the held-out check, the catalog

**The stack guard** (engine/vm-lab.c, rt-linux-x86_64.c): 64 cells of slack
above the data stack, so a shallow underflow is ?STACK's, as without the
guard ("Stack error DROP", and on); a stack meets its guard at the page's
near edge, so the handler names the stack and the way - data stack
underflow, return stack overflow, data stack overflow, dictionary full - and
a fault below main's frame is the C stack (the JIT's native recursion,
which before killed the engine with a bare SIGSEGV); the handler runs on its
own stack (sigaltstack), flushes the output and exits 70, as stack_fault.
Two guard designs with the JIT: all four faults reported, the gate passed.

**The held-out check** (lab/evolve/ans-check.py): each design's output on the
ten ANS files against s6's, byte for byte. Twelve front designs, six with the
guard: all ten files as s6.

**The catalog**: results/forth-collection-catalog.md - every item, what it is,
its licence, how useful.
