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

## Phase 2c: the hang, and two more mapping bugs

The hang was not what it looked like. On s6 the trigger is `bytehdr=0`
ALONE; no caching and `-fno-crossjumping` only changed how it failed (a
stack error instead of a hang). Interpreted, `SOURCE TYPE` worked;
compiled into a definition it failed - so the fault was in code compiled
at RUN time.

cv8.4 and cv8b.4 set the in-image compiler's call shift and DOES> form
as a pair - shift 3, near DOES> calls, 2 bytes reserved; or shift 0, far
calls, 3 bytes - but the genome chooses `scale`, `bytehdr` and `doesfar`
independently. s6 without byte headers got cv8.4's shift 3 with its own
byte-granular calls, so every call compiled at run time went to the
wrong address. The converter now writes all three variables from the
design's own genes (`--set-compiler-vars`, `--does-far`); the hand-made
stages come out unchanged.

The second: variable-length calls are decoded only on the engine's
shared call path (`do_call`), so `varcall` without `sharedcall` misread
every three-byte call - in every earlier run. `sharedcall` is now dormant,
built in, when `varcall` is set; decoding both forms on the unshared path
would reopen that combination.

What dies now is real. A byte-granular design with near DOES> calls, or
without the three-byte call form, reaches 16 KB, and the kernel
workload's dictionary is larger: a DOES> word past 20,000 bytes of padding
hangs with near calls and works with far ones. They die by timing out
because cv8.4's near forms do not check their reach.

The same 12 x 4 run, before and after each fix: alive 45 -> 51 -> 53 of
60; corpus deaths 7 -> 3 -> 0; the remaining 7 deaths all that reach
limit. The fastest design was s6 without byte headers, with d256 and one
pair, at 0.806 of s6 - the combination that used to hang.

All three bugs (with the fold list) are one kind: a setting of the
compiler INSIDE the image that the genome treated as free, but the dump
fixed. So the earlier runs' verdicts on fold lists, on byte headers
against call granularity, and on the shared call path were artefacts.

## Phase 2d: a scan of every single change, and a flawed check

`lab/evolve/scan.py` checks every single-gene change of every hand-made
design for correctness only - 125 changes; `SCAN.md` has the result.

It exposed a flaw in the survival check itself. The kernel workload runs
in a directory that starts with a copy of the reference kernel, and the
check compared that file afterwards - so a design that died quietly
before saving passed. Every earlier run has that flaw: designs counted
alive may never have finished the kernel workload, and their kernel
times, cut short, would look fast. The check now removes the file first;
the hand-made stages all still pass.

With the strict check, every death has a real cause. Two-byte-only forms
(calls without `varcall`, near DOES> calls) reach 2^14 units - 16 KB at
scale 0, 32 KB at scale 1 - and the kernel workload's dictionary is
larger; with both far forms the same designs live. And the scan found a
fourth mapping bug: DODOES decodes the far form only under VARCALL, so
`doesfar` is now dormant, built off, without `varcall`.

A broken design executes arbitrary code, and the engine's primitives
include fork and execve. Leftover processes held pipes open past every
timeout, and probably crashed the container once; every engine run now
has a process group of its own, killed whole on timeout, and a CPU cap.

## Phase 3a: relf's format-10 opcodes

`ops10`: seven kernel colon words - `EXECUTE`, `I`, `(DO)`, `+!`, `?DUP`,
`UNLOOP`, `J` - as one-byte opcodes, in the free slots before the pairs
take theirs, so the three compete. The converter substitutes a call only
where the word's compiled body is exactly the definition the engine
implements (the same check as the tiny family; `SOD16_SHOW=NAME,...`
prints how a word reads). As opcodes the return-stack words have no
return address of their own: `I` is the top cell, `J` two below.

Development VM, against the parent: s4 with all seven, 0.964 of the time
and 32 bytes smaller; with 20 pairs as well, 0.843 and 96 smaller; s6 with
the two its free slots hold, `EXECUTE` and `I`, 0.981 and 16 smaller.
Parse and corpus gain most: the outer interpreter runs every word it
interprets through `EXECUTE`. Each word alone passes the strict check in
s4, s5 and s6, and the scan now tries each one.

That check found a hazard in the engine's macros: in the top-of-stack
build, `PUSH(x)` lowers dsp BEFORE it evaluates x, so `PUSH(DS0)` copies
the new, empty slot onto itself. `?DUP` failed in s5 and s6 only; it now
takes the value first.

## Next

`GENES.md` lists what other VMs could add - load-time translation to
direct threading, tail-call threading, the rest of relf's format 10, indirect threading, multi-state stack caching, SPN's
genes, a register machine - each needing engine work before evolution can
use it.
