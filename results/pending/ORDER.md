# The after-seed-50 batch - apply in this order (against master after Iteration 290)

| # | patch | what it does |
|---|---|---|
| 1 | twocell-after-seed50.patch | 2@ and 2! as opcodes: in the ops10 pool and opbody's list - their handlers in engine/vm-lab.c, tools/gen-tos.py and tools/gen-msc.py (gen-tail.py takes them as it finds them; the JIT leaves a word with an opcode it does not translate to the interpreter), their kernel bodies in tools/sod16.py's table as the converter reads them (SOD16_SHOW), evolve.py's OPS10_POOL, OPS10_LABEL and OPBODY, layout.py's _OPB; five more engines-check paths (s6, the cached top off, multi-state, tail calls, the JIT, each with the two opcodes). bubble's inner loop and the corpus's tester call these words at run time (results/source-audit-2.md). Measured on c9369657e4, seed 47's fastest design without the JIT: bubble 12,759,474 -> 9,572,364 dispatches (-25.0%), the corpus -0.3%: about -4.7% on the selection's geometric mean. DEPTH left out: its handler would have to agree with the kernel's S0 exactly. No kernel change: no reseed. |

    git apply results/pending/twocell-after-seed50.patch

Patch 1, tested on master at Iteration 289, in a scratch tree: the build; engines-check
PASS, 36 paths; run-tests PASS (the generators 36 paths); gene-equiv.py against HEAD -
every recorded design's id and expression the same (3,048), and, as a longer pool must,
243 of 1,000 random genomes and 4 of 3,000 mutations different; word-cost.py as above.
