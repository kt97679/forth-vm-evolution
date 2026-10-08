# The gene jitx: the JIT reaches further (Iteration 108)

The first gene batch after the deep dive (lab/evolve/GENES.md, "Ranked
(Iteration 91)", the JIT's next steps; priced in results/jit-kernel-words.md).
One gene on top of `jit`, because the parts only pay together: kernel words
made native free nothing without data words as literals, and the sieve's one
word waited on FILL.

## What it does (engine/jit.c, under JITX)

- **Variables are literals.** A call to a word that begins with DOVAR becomes
  its parameter field's address, align8(body + 5) under the tag - the rule
  L_dovar pushes - fixed for the run.
- **Words without the JIT header are translated too** - kernel words in the
  image, CONSTANTs and the like made at run time - each once, kept by address
  in a 256-entry table; the end found as the converter finds a body's end:
  the first EXIT no branch reaches past. A call cycle stays bytecode.
- **>R, R> and R@ get stencils** (SPN's tor, fromr, rfetch; layout.py --jitx),
  in a word whose return stack balances in order: never below its entry,
  back to it at every EXIT. Native words return through the C stack, not
  the engine's return stack, so a word that reads its own return address
  (R> DROP, inline operands) must stay bytecode - and does.
- **FILL gets a stencil** (spn-stencils.c st_fill): rep stosb on x86-64, no
  call - a stencil may hold none. Call depth up to 8 (was 4).

## The counts (VM)

Bytecode dispatches with jitx against without, the same design (70bc3ae6b5;
679fdd08a1 the same to 0.1%):

| workload | jitx | why |
|---|---|---|
| kernel | **0.900** | the cross-compiler's words: kernel callees native, variables literal, >R/R> |
| corpus | 0.997 | |
| sieve (held out) | **0.001** | PRIMES native: FILL, 1+, 2DROP, the run-time FLAGS (a variable) and SIZE (a constant) |
| parse, fib, loop | 1.000 | parse runs no run-time code; fib and loop were native already |

On the VM the sieve runs **3.4x faster** (14.5 -> 4.2 ms); kernel and corpus
show nothing at this length through the VM's noise - the laptop will tell.

Correct where it was changed: the gate (corpus, kernel workload) on two JIT
designs; the sieve's output equal to hand-made s6's; FILL writing the right
bytes on the call that translates and the one after; a balanced >R R@ R> R>
word right. Tests pass, hand-made stages identical.

## The cost

Code +368 bytes and a 4 KB table in BSS (touched as used). The engine's FILE
grew 4,288 bytes: the page-padding step again (Iteration 95) - evolution will
see ~4 KB for ~400 bytes of code until that is fixed. With the gene off,
images are identical; the JIT engines' code is 48 bytes larger (the
translator split in two), their files the same size.
