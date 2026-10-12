# Stack state in the JIT's translator, priced (Iteration 218)

Item 1 of results/drafts/jit-vm-survey.md: the translator tracks which of the
top stack cells are in registers and which are known constants, instead of
every stencil entering and leaving with `(sp, tos)` - the top in a register,
everything below it in memory. Searched first (prompts/12): FINDINGS-SPN.md
named this SPN's next step ("register allocation as table lookup", SUMTO's
loop 5x C with the top alone cached); never attempted. Priced here before
anything is built (prompts/10).

## Method

- **A counting-only build, `JIT_PRICE`** (engine/vm-lab.c, engine/jit.c;
  profiling builds only, `JIT_PRICE=1` in the environment of a profiling
  build in lab/evolve/evolve.py). The JIT translates every word exactly as
  it would - a translated word keeps its header, so the translations after
  it see what they would have seen - but native code never runs: the
  translated words' byte code is dispatched, so the profiler counts every
  operation where it is, and the translator's dump lists, for each
  translated word, its operations, the stencils each becomes, and every
  branch's target. Same program, same translations; only where it runs
  changes.
- **lab/evolve/jitstack.py**: each stencil's cost read from the engine with
  objdump as the JIT copies it - instructions, those there only for the stack
  in memory (writing `%rdi`, moving a cell to or from `(%rdi)`), and the
  data-stack memory accesses. Then the translator's proposed state
  simulated over each translated word with K cached registers: a shuffle or
  a literal costs nothing while its cells are cached (a register may hold
  several slots, as Liftoff's does); an operation keeps its instructions
  less its stack moves; a cell fetched from memory is one load, one sent
  there one store; at every branch, branch target, loop, call and EXIT the
  state goes back to `(sp, tos)` - each cached cell below the top stored, a
  constant top loaded, the stack pointer moved once.
- **Two bounds.** Words compiled at run time run native wherever they are
  called (their header); kernel words translated under jitx run native only
  when native code calls them - the second figure counts all their
  executions (an upper bound), the first none.

**Checked:** the switch changes no normal build - four designs (28677d13b1,
cc6d168e0a, fc09f6373d, add5ec8937) built from this tree and from the
Iteration 217 tree: engines and images byte for byte; 7 of 7 stages
identical. The simulation audited by hand on the loop workload's hot word
(`jitstack.py --show 2` lists every operation's cost in both models): per
iteration DUP I + XOR LOOP is 22 instructions and 4 data-stack accesses
today; with three registers 16 and none - the I and LOOP stencils keep their
return-stack work.

## The prize, counted

The fastest design of all runs, 28677d13b1 (seed 42); share of all operations
dispatched that are in translated words (run-time words / with kernel words);
native instructions and data-stack memory accesses removed, at K = 2 / 3:

| workload | translated | instructions removed | stack accesses removed |
|---|---|---|---|
| fib | 90.5% | 27.4% / 27.4% | 75.0% / 75.0% |
| loop | 99.9% | 13.7% / 27.3% | 50.1% / 100% |
| bubble | 34.4% / 90.7% | 17.4-20.0% / 17.4-20.9% | 55.6-56.3% / 55.8-61.1% |
| ackermann | 75.0% / 92.7% | 11.6-14.2% | 18.0-33.6% |
| kernel | 36.1% / 42.5% | 17.3-20.4% / 21.4-25.2% | 28.3-29.3% / 46.1-47.9% |
| corpus | 1.0% / 2.4% | (12-24% of almost nothing) | |
| sieve (held out) | 80.1% / 81.9% | 44.5-45.4% / 43.0-43.9% | 87.1-88.2% / 81.9-83.0% |
| parse (held out) | 0.0% | - | - |

Seed 43's fastest (cc6d168e0a) gives the same to the tenth; the Q-best of all
runs (fc09f6373d) fib 38.2%, loop 13.1% / 26.1%, kernel 18.0-20.5% /
22.2-25.3%, sieve 45.3-46.8%. The corpus and parse barely run translated
code - nothing to gain there until more of them is translated.

Three registers do slightly worse than two on the sieve: storing every
cached cell at each boundary costs more than the third register saves - a
lazier policy (store only what the boundary needs) would keep both gains.
Every call still sends its cells to memory, which caps fib. And the loop's
own index lives in memory: the LOOP stencil's load-add-store of it is a
second chain the cache does not touch.

## The count turned into time (prompts/10: once)

lab/evolve/jitstack-inner.S: the loop workload's hot word, `DUP I + XOR`
inside `DO ... LOOP`, as the JIT copies it today (the stencils' instructions
verbatim), with three cells cached, and with the loop's index and limit in
registers too; 200 million iterations, best of 7, three runs, on the
development VM (Intel Xeon @ 2.1 GHz):

| | ns per iteration | of today's |
|---|---|---|
| today (22 instructions, 4 stack accesses) | 1.01-1.03 | 1.00 |
| three cells cached (16, none) | 0.72-0.76 | 0.70-0.75 |
| and the loop's index and limit in registers | 0.62-0.65 | 0.61-0.63 |

Here the instructions removed (27%) came out as the time removed (25-30%).
Not yet measured on the laptop's Zen 4.

**What it could be worth:** if the time removed follows the instructions
removed on the translated share, the selection's geometric mean improves
by about 15% on the JIT designs (fib and loop ~25%, bubble ~15%, ackermann
~12%, kernel ~8%, corpus nothing), the held-out sieve ~40%. An estimate, not
a measurement.

## Not yet priced: what it displaces

The binary objective counts every engine byte, and stencils have their
registers fixed in their machine code: the state needs stencil variants, or
a small instruction emitter in the translator. The JIT costs about 3.4 KB of
engine today (JIT.md, Iteration 82).
