# Inlining at the hottest call sites, and the bodies opcodes replaced (Iteration 92)

The first two of Iteration 91's ranked candidates (lab/evolve/GENES.md,
"Ranked (Iteration 91)", 1 and 2), built behind genes and counted on the VM:
dispatches by the profiler, every variant through the gate (the corpus and
the kernel workload byte for byte). Time is for the laptop's seed run.

## The genes

- **hotinl** (0, 10, 20, 40; designs in the tag): the converter inlines the
  first K safe sites of `lab/evolve/hotsites-v1.json` - the image's call
  sites ranked by the profile of the fastest design of all runs
  (2cbcf427f6; `lab/evolve/hotsites.py` writes it), named by caller, callee
  and which call it is, so the list carries over to designs from the same
  sources. A site is inlined before every rewrite (tools/sod16.py,
  hot_inline), so specialisations, folds, pairs and fused tests see the
  copied code in place. Safe means: the callee straight-line (no branch, no
  inline operand, no DOES> entry), one EXIT and that last, its return stack
  balanced within it, calling only words that do not read their caller's
  return address (or that become opcodes which do not), and not a body the
  converter rewrites after reading it.
- **opbody** (0, 1): the words an opcode replaced - (FIND), (>NUMBER),
  THREAD-FIND, +!, ?DUP - get the body [opcode EXIT], as FILL, CMOVE and
  the input side's did in Iterations 50 and 54. Their Forth bodies never ran
  in any workload (Iteration 91); code compiled at run time that calls them
  now takes the opcode too.

## The counts

Image bytes against the design as recorded, and each workload's dispatches
as a fraction of the design's own (with the JIT, fib and loop dispatch a few
thousand times: their fractions there are of almost nothing).

| design | variant | image | kernel | parse | corpus | sieve (held out) |
|---|---|---|---|---|---|---|
| 2cbcf427f6 (fastest) | hotinl=10 | +40 | 0.970 | 0.916 | 0.921 | 1.000 |
| | hotinl=40 | +112 | 0.959 | 0.896 | 0.907 | 1.000 |
| | opbody | -128 | 0.993 | 1.000 | 1.000 | 1.000 |
| | hotinl=40, opbody | **-16** | **0.952** | **0.896** | **0.907** | 1.000 |
| e83972af52 (middle) | hotinl=10 | +48 | 0.972 | 0.927 | 0.933 | 1.000 |
| | hotinl=40 | +160 | 0.961 | 0.908 | 0.919 | 1.000 |
| | opbody | -144 | 0.990 | 1.000 | 0.998 | 1.000 |
| | hotinl=40, opbody | **+16** | **0.950** | **0.908** | **0.918** | 1.000 |
| faf72cef8e (smallest) | hotinl=40 | +136 | 0.994 | 0.997 | 0.994 | 1.000 |
| | opbody | -8 | 0.998 | 1.000 | 1.000 | 1.000 |

On the fast designs the two together are about size-neutral and take 9-10%
of parse's and corpus's dispatches and 5% of the kernel workload's. On the
smallest design the list barely applies - its hot paths are other words -
so evolution chooses per design. With the genes off, all 35 designs of the
front of all runs build to their recorded sizes and ids; the hand-made
stages are identical; the tests pass.

## Three faults on the way - the gate caught each

1. **The compiler's swap.** An X8 word's body becomes X's after reading
   (tools/layout.py, the CV8 compiler overlay): the hottest callers (PARSE,
   WORD, INTERPRET, FIND) carry X8 names when read, and a callee's body read
   before the swap is the wrong one - LITERAL inlined as the cell format's
   compiler crashed the system at the first literal compiled. Now callers
   and callees are known by their final names and run their final bodies.
2. **Bodies patched after reading.** LIT8-OP, an opcode constant of the
   run-time compiler, is rewritten to the design's tag-2 code after the
   bodies are read; a copy kept the old code and code compiled at run time
   broke. The constants are never copied, and the tag-2 section asserts the
   list cannot drift (T2_CONSTS).
3. **Data told from code** by the first call's target, as the classifier
   does - a first test treated every body starting with a call as data,
   refusing SOURCE, HERE, WORD and FIND, and taking unchecked words as safe.
