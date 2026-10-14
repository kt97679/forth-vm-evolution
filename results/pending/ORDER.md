# The after-seed-50 batch - apply in this order (against master after Iteration 293)

| # | patch | what it does |
|---|---|---|
| 1 | twocell-after-seed50.patch | 2@ and 2! as opcodes: in the ops10 pool and opbody's list - their handlers in engine/vm-lab.c, tools/gen-tos.py and tools/gen-msc.py (gen-tail.py takes them as it finds them; the JIT leaves a word with an opcode it does not translate to the interpreter), their kernel bodies in tools/sod16.py's table as the converter reads them (SOD16_SHOW), evolve.py's OPS10_POOL, OPS10_LABEL and OPBODY, layout.py's _OPB, and for the JIT their SPN stencils in layout.py's table - five each, CELL+'s ADDI the one constant (without them a JIT design that took the opcodes would leave every word holding one to the interpreter: jit.c's all or nothing); five more engines-check paths (s6, the cached top off, multi-state, tail calls, the JIT, each with the two opcodes). bubble's inner loop and the corpus's tester call these words at run time (results/source-audit-2.md). Measured on c9369657e4, seed 47's fastest design without the JIT: bubble 12,759,474 -> 9,572,364 dispatches (-25.0%), the corpus -0.3%: about -4.7% on the selection's geometric mean. DEPTH left out: its handler would have to agree with the kernel's S0 exactly. No kernel change: no reseed. |
| 2 | opinline-after-seed50.patch | The gene opinline (late, 0 and 1; Iteration 292): the [opcode EXIT] words - layout.py's base list, and opbody's - placed among the primitives, before (PRIMITIVES-END), where PRIMITIVE? asks by address, so every run-time COMPILE, copies their opcode in place of a call. A word defined once only. Expressed only where a design has such a word. Measured on c9369657e4 with patch 1's opcodes and opbody: bubble 9,572,364 -> 7,448,901 dispatches (-22.2%; -41.6% from the 12,759,474 before patch 1), the corpus -0.2% - with patch 1 about -8.6% on the selection's geometric mean. For a JIT design it can cost (an inlined opcode without a stencil leaves its word to the interpreter): evolution judges. |
| 3 | tailpn-after-seed50.patch | The gene tailpn (late, 0 and 1; Iteration 293): the tail-call engine (tools/gen-tail.py) with clang 19+'s preserve_none on every handler - no register callee-saved, the machine state kept in registers through the chain - and musttail on every handler-to-handler call: CPython 3.14's tail-call interpreter. Built with clang_pn(), the newest clang here that takes them (clang-20 on the laptop, clang-19 on the VM); expressed only on a clang tail engine, only where such a clang is installed. evolve.py also counts a versioned clang a build tool: jailed as an engine (no new process), its driver could not start the linker - the first try's 'did not compile'. s6's engine 14,232 bytes against 14,680 without; its speed is the laptop's to judge - seed 49's front had no tail engine at all. |

    git apply results/pending/twocell-after-seed50.patch
    git apply results/pending/opinline-after-seed50.patch
    git apply results/pending/tailpn-after-seed50.patch

Patch 1, tested on master at Iteration 289, in a scratch tree: the build; engines-check
PASS, 36 paths; run-tests PASS (the generators 36 paths); gene-equiv.py against HEAD -
every recorded design's id and expression the same (3,048), and, as a longer pool must,
243 of 1,000 random genomes and 4 of 3,000 mutations different; word-cost.py as above;
the gate with the two opcodes put first in every design's list and opbody on, seed 49's
front: 172 of 172 alive, every one expressing them. Then (Iteration 291) the JIT's stencils
added and tested again: engines-check PASS, the JIT path with the opcodes among the 36;
the fastest JIT design 927064f127 with them translatable - 70 of its 129 operations, 69
without; the gate on seed 49's front again 172 of 172 (99 JIT designs); run-tests PASS.
The patch applies on a fresh clone of master after Iteration 291 and reproduces the tested
files.

Patch 2, tested on patch 1 in a scratch tree (Iteration 292): the build; engines-check
PASS, 41 paths - five more, patch 1's five with opinline on; run-tests PASS; gene-equiv.py
against patch 1 - every recorded design's id and expression the same (3,048), every made
genome different, as a new gene's key must make them; word-cost.py as above; the gate with
2@ and 2! first, opbody and opinline on, seed 49's front: 172 of 172 alive, every one
expressing it. Patches 1 and 2 apply in turn on a fresh clone of master after Iteration
292 and reproduce the tested files.

Patch 3, tested on patches 1 and 2 in a scratch tree (Iteration 293): engines-check PASS,
42 paths - one more, clang-19's tail engine with preserve_none (225 handlers and
declarations so marked, 223 tail calls musttail); run-tests PASS (the generators 42 paths);
gene-equiv.py against patch 2 - every recorded design's id and expression the same, every
made genome different (a new gene's key); the gate with tail, clang and tailpn forced on 20
of seed 49's front: 19 of 19 alive, the 20th not able to express a tail engine. A rough
timing on the VM was not made: its script ran the engines wrongly, and the VM's noise would
not judge it anyway. All three patches apply in turn on a fresh clone of master after
Iteration 293 and reproduce the tested files.
