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

## Phase 2a: superinstructions

`tools/gen-super.py` builds a pair's handler from the two primitives' own
bodies - the first jumps into the second where it would have dispatched -
and the converter fuses the pair wherever no branch lands between them
(`--supers-file`, the same guard as folding). The pairs take the opcodes
nothing else holds: 126 and 127, the fold band past the folds in use, and
the specialisation band when SPEC is off, so folds, specialisations and
pairs compete for slots. The 24 candidates are the primitive pairs the
CV8 interpreter dispatched most over the four selection workloads.

Every pair improves BOTH objectives. Development VM, against the parent:
s6 with the two it has room for, 0.944 of the time and 16 bytes smaller;
s4, which has thirty free slots, with all 24, 0.849 and 96 bytes smaller -
and the held-out loop faster too, 0.983 and 0.892, so it is no artefact
of the selection workloads.

A 12 x 4 run, with two founders carrying pairs: 23 of 44 living designs
had them, and hand-made s6 fell off the front - its founder variant was
smaller and faster. The best design came from that founder, borrowed its
pairs from a third lineage and its call-target block from another, and
reached 0.85 of s6's time.

## Phase 2b: run-time fusion, and a correction about folds

Superinstructions in the image leave out code compiled at run time.
`forth/cv8-fuse.4` is an overlay on the CV8 compiler that fuses as it
compiles: COMPILE,8 rewrites the previous byte when it is a plain
primitive immediately before HERE and the pair is in SUPER-TABLE, which
the converter fills in per design (`--rtfuse`). BEGIN and DO now clear
LAST-OP, since they make HERE a branch target without emitting anything
there. Read back: `: T1 DUP >R C! R> ;` compiles to 126 127 EXIT, while
`DUP BEGIN >R` stays two bytes. Corpus identical, kernel reproduced.

It does not pay on these workloads, so it is a gene (`rtfuse`, with the
overlay only where it is set) and selection rejects it. The overlay costs
560-576 bytes and the designs get slower: s6 with two pairs 0.956 -> 0.970,
s4 with 24 pairs 0.855 -> 0.877. The hot pairs are in the image's code,
already fused; code compiled at run time here holds few of the 24 (FIB
none); and the compiler now scans the pair table for every primitive it
compiles. In a 12 x 4 run, 5 living designs fused at run time, none on
the front.

**A correction to phase 1.** cv8.4's FOLD-OPS, the compiler's fold list,
is fixed in its source. Every CV8 design whose fold list differed from
the default - shorter, or reordered - compiled run-time code with fold
opcodes its engine gives to other primitives, and died on the corpus:
with the converter before this change, s6 without `LIT` and s6 with 12
folds both die. So in every earlier run the fold genes could survive only
in their default form, and nothing said about folds was learned from
selection. The converter now writes each design's list into FOLD-OPS,
padded with 255, which no opcode matches; the default list writes back
the same bytes, so the hand-made stages are unchanged and it costs
nothing. Those designs now live: the reversed list at the same size and
speed, without `LIT` 16 bytes bigger, with 12 folds 40 bytes bigger and
3.5% slower. In the 12 x 4 run, 4 of 5 fold mutants survived, and the best
design has a removed fold and a borrowed fold list in its history.

**Found, not yet explained:** s6 with no top-of-stack caching, no byte
headers and `-fno-crossjumping` hangs (`died: timed out`), reproducibly,
also with the converter from before these changes. Either of the first
two alone is fine, and so is specialisation without caching.

## Next

`GENES.md` lists what other VMs could add - load-time translation to
direct threading, tail-call threading, relf's format-10 opcodes, indirect threading, multi-state stack caching, SPN's
genes, a register machine - each needing engine work before evolution can
use it.
