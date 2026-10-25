# Why the search ignored three JIT genes, and what the cpt16 designs do with larger programs (Iteration 517)

The owner asked for both while seed 72 runs.

## The JIT genes (seed 71: jitmul on 72 of 130 JIT designs; jitcfa 9, jitexec 2, jitdoes none)

Seed 71's fastest, f83a64a706 (it has jitmul and jitcfa), each gene added - instructions (cachegrind) on the seven
workloads, and the engine's bytes:

| | apps | kernel | corpus | the seven | bytes |
|---|---|---|---|---|---|
| + jitexec | -13.7% | -0.1% | +0.8% | -1.7% | **+586,544** |
| + jitdoes | 0.0% | +0.2% | +0.1% | +0.1% | +436 |
| + jitcfa (has it) | - | - | - | - | - |

- **jitexec cost 586 KB - a bug.** Its three extra rows in the JIT table sat after the highest name the converter knew,
  T2_JIT at 0xFE00: jit_ops ran to 65,029 rows (585,261 bytes of read-only data, nm). With the rows after the real
  operations: 2,752 bytes. **No search could keep a gene that made a 37 KB engine 623 KB**; fixed in the after-seed-72
  batch, its gain now to be weighed fairly (and its votes, rule 12, count from seed 72 - one run with the bug).
- **jitdoes buys nothing on the selection's workloads** - no DOES> child in their hot paths (the applications', at
  full size, held more): a fair outcome under rule 11; a freeze candidate if its votes say so.
- **jitcfa is on the fastest already** and costs nothing - it drifts, as it should.

## The cpt16 designs and larger programs (seed 71: 791 failed the applications; 7fabd817ed differed on toolstest.fth)

- **The applications: refused out loud, as the far rule allows.** A cpt16 design's calls are 16-bit tokens (2^16 bytes
  times 2^scale of reach - 908baebc14 scale 0, 7fabd817ed scale 1). gc16 allots 320 KB of cells before defining words;
  the words after it are beyond reach: "call out of reach ROOTS", and every later use "Undefined word". The far test
  (Iteration 158, the owner) accepts exactly this - every answer right, or refused out loud. No silent fault; the
  loophole was only that measure() did not look (fixed at 516: a wrong output kills the design).
- **toolstest.fth: a false difference.** Without blank lines and the prompt's OKs both outputs are the same 121 lines,
  no test failing in either; the design echoed 29 fewer OKs. ans-check.py now compares without them, as alive() does
  (on master: a tool).
