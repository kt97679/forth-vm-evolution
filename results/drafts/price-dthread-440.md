# Translation to direct threading at load - priced (Iteration 440)

The one mechanism in lab/evolve/GENES.md's "Not yet" never priced (results/audit-genes-designs-439.md). The idea
(gforth's hybrid, Wasm3's M3): the image stays compact on disk; at start the engine expands it into handler addresses
with operands decoded, so a dispatch is `goto **ip++` - no byte fetched and looked up in a table (`t = *ip++; goto
*dtab256[t]`). Code compiled at run time would be expanded at `;`, or compiled as addresses from the start.

## Speed - the dispatch lab

lab/dispatch/README.md measures the same handlers dispatched both ways (the development VM, best of 5):

| | fib | loop | sieve |
|---|---|---|---|
| direct against token | -5.5% | **+8.9%** | -12.4% |
| with superinstructions | -13.1% | +6.3% | -15.4% |

About 3% faster on the geometric mean, mixed: the loop slower. What direct threading saves is one load from a table
that sits in the first-level cache; what dominates dispatch - the indirect jump's misprediction - is the same either
way (the interpreted designs are front-end bound on it, Iteration 301). In the same lab tail-call threading is the
fastest pure dispatch, and the tail engines now build at both widths (the after-seed-62 batch); the JIT removes
dispatch from translated code altogether.

## Memory - seed 62's front

Every code byte becomes an 8-byte address. Seed 62's front: the image's median 8,519 bytes, about **+58 KB in memory**
expanded - **+33% to +38% of the memory objective** (its median 152 KB; the fastest third's 176 KB). An upper bound -
headers and data would stay compact - but the order stands.

## Work

An expansion pass at load and at `;`; the run-time compiler and every overlay that writes or patches code (the fuser,
the immediates, both loop compilers, I+) taught the expanded form; every dispatch form (escapes, the tag's two-bit
calls, format-10 words) at both widths; the converter's tables. A new engine path the size of the tail engines.

## Verdict

**Not worth building now**: about 3% at best on interpreted designs, for a third more memory and a path as large as
the tail engines - where tail threading and the JIT already hold the fast end. Worth another look only if the memory
objective were dropped, or if the fast end turned decode-bound rather than bound on the jump's prediction.
