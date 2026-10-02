# Evolving VM designs

`evolve.py` breeds CV8-family designs: engines and images built from a
genome, kept alive only if they pass the CORE corpus byte for byte and
cross-compile the kernel exactly, and selected on two counts at once -
speed, and image size - as a Pareto front. Its docstring has the genome,
the operators and the fitness; this is how to use it and what it found.

    lab/evolve/evolve.py --validate     s4, s5, s6 rebuilt from their genomes
    lab/evolve/evolve.py --pop 32 --gens 40 --rounds 5
    lab/evolve/evolve.py --report       build/evolve/report.md

It needs a finished `tools/build-stages.sh`. Everything it learns goes to
`build/evolve/db.jsonl`, one line per design - genome, parents, how it was
made, how it lived or died - so a run can stop and resume, and no design
is measured twice.

**Trusting it.** `--validate` rebuilds the three hand-made CV8 stages from
their genomes; their images must be byte-identical to the build's, or the
genome means something other than it says. They are.

**Running it for real.** Selection on CPU time in a VM is noise-bound; on
the Ryzen, cycles repeat to 0.3%. With the counters readable, it measures
cycles by itself:

    sudo sysctl kernel.perf_event_paranoid=2
    BENCH_CPU=9 lab/evolve/evolve.py --pop 32 --gens 40 --rounds 5
    sudo sysctl kernel.perf_event_paranoid=4

A design takes a second or two to build and test; 32 x 40 is about an
hour, less what the database already knows.

## Phase 1, development VM, CPU time - a first run, 8 x 3

- **It rediscovered the 256-entry dispatch table.** The best design was s6
  with `d256=1`: the same 9,969-byte image, about 8% faster, and 7% faster
  on the held-out loop - strictly better than the hand-made s6. It got
  there by BORROWING the dispatch block from another lineage.
- **The held-out workload caught overfitting.** The fastest design on the
  four selection workloads (0.849 of s6) was slower than s6 on loop.
- **Most of what mutation tries is lethal**: designs that do not convert,
  fail the corpus, or hang. Each cause is recorded; one, byte headers with
  scaled call targets, is now a constraint rather than a death.
- **The fold gene is small.** Only the 23 hand-picked primitives can be
  folded at all - the other candidates make engines that do not compile -
  so the opcode map's real combinatorial space waits for phase 2.

## Phase 1b: four families and the compiler

The genome now spans the whole ladder - the cell engine, SOD16, CPT16 and
CV8 - with genes a family does not use carried dormant, and the compiler
flags gforth and CPython rely on as genes of their own (`GENES.md`).
`--validate` rebuilds all seven hand-made stages, s0 to s6, with
byte-identical images. Each family keeps its best member, so a family
survives as a species even when CV8 dominates the front.

A first 12 x 3 run in the VM: 48 designs, 37 alive. CV8 took the front;
the other families held their niches. Compiler genes spread on their own
- `-fno-crossjumping` in 9 of the living, `-fcf-protection=none` in 7,
`-fno-gcse` in 6. The fastest design descended from the PLAIN s4 by
crossover, borrowed another lineage's call path and dispatch, and took
`-fno-crossjumping`: 0.83 of s6's time, 0.98 on the held-out loop.

## Next

`GENES.md` lists what other VMs could add - load-time translation to
direct threading, tail-call threading, static superinstructions, relf's
format-10 opcodes, indirect threading, multi-state stack caching, SPN's
genes, a register machine - each needing engine work before evolution can
use it.
