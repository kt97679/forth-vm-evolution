# The JIT's operation pairs - pricing super-stencils (Iteration 506)

The owner: count first (idea 2 of 505's answer - fused stencils for the commonest pairs, the JIT's superinstructions).
lab/evolve/jitpairs.py: seed 70's fastest JIT design, 77d42fd7da with the four JIT genes, built with the JIT off and the
profiler on - so every operation the JIT would copy is a dispatch, counted in pairs - over the seven selection
workloads, each weighted equally (the selection's geometric mean); names from the JIT build's table.

**41.2% of dispatched pairs are two operations in straight-line code** (no branch, loop step, EXIT or EXECUTE between):
by workload kernel 46.6%, fib 40.9%, corpus 49.7%, loop 59.9%, bubble 36.2%, ackermann 12.6%, apps 42.2%. The top 25
pairs cover 25.3% of all dispatched pairs; a long tail after them.

| pair | share | cumulative |
|---|---|---|
| I + | 2.98% | 3.0% |
| DUP I | 2.91% | 5.9% |
| + XOR | 2.85% | 8.7% |
| I 2@ | 1.40% | 10.1% |
| DUP LIT8 | 1.34% | 11.5% |
| LIT8 < | 1.30% | 12.8% |
| LIT32 + | 1.30% | 14.1% |
| DUP 0= | 1.25% | 15.3% |
| SWAP <;EXIT | 0.97% | 16.3% |
| DOVAR @ | 0.87% | 17.2% |
| + SWAP | 0.72% | 17.9% |
| DOVAR + | 0.66% | 18.5% |
| DROP LIT8 | 0.65% | 19.2% |
| DUP LIT32 | 0.65% | 19.8% |
| SWAP LIT32 | 0.65% | 20.5% |
| ADDIX OVER | 0.59% | 21.1% |
| ROT + | 0.50% | 21.6% |
| DUP @ | 0.48% | 22.1% |
| SWAP !;EXIT | 0.47% | 22.5% |
| @ ROT | 0.47% | 23.0% |
| SWAP OVER | 0.45% | 23.5% |
| + C! | 0.45% | 23.9% |
| OVER ! | 0.45% | 24.4% |
| ! CELL+ | 0.45% | 24.8% |
| CELL+ !;EXIT | 0.45% | 25.3% |

The single operations: DUP 8.3%, + 7.0%, ?BRANCH 6.3%, EXIT 6.1%, SWAP 5.4%, I 5.0%, LIT8 4.6%, (LOOP) 3.1%, XOR 3.0%,
DOVAR 2.8%, BRANCH 2.6%.

**What it prices.** Between two stencils a value goes through the stack in memory: the first pushes (a store and the
pointer moved), the second pops. A fused stencil keeps it in a register - for I + : the top plus the loop index, no
push or pop. Per pair that saves perhaps a third of the two stencils' instructions, less where jitk already keeps the
second item in a register. Fusing the top 25 (a quarter of the pairs; non-overlapping, perhaps a third of the
operations) at that rate: **a few percent of a JIT design's time, perhaps up to 8% without jitk** - the low end of the
estimate at 505. The leaders fall in three groups: the loop index (I +, DUP I, I 2@), literals into an operation (LIT8 <,
LIT32 +, DUP LIT8), and arithmetic between shuffles (+ XOR, + SWAP, ROT +, OVER !).

**Proposed** - smaller than a pair table: a JIT gene for the literal-into-operation group alone - LIT followed by +, -,
<, =, AND, OR, XOR as one stencil with the literal in a hole, as the interpreter's folds do - and the loop index into +
and 2@; measured on the fast design before a gene is made (rule 11: the selection pays for it, every workload runs JIT
code on a JIT design). Or none, if a few percent does not justify its stencils' bytes - a size cost the search weighs.
