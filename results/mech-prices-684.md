# relf's mechanisms priced on application code (Iteration 684; step 2 of results/drafts/search-reopen-plan-677.md)

Each mechanism of relf's run-time compiler, priced on the selection's four applications (sim16, gc16, scan, evo) with
the held-out three beside (wordfreq, minif, brainless). Bytes: lab/evolve/mech-census.py counts what each mechanism
acts on in the programs' source; lab/evolve/mech-price.py multiplies by 674's per-construct costs at 8-byte cells
(results/generic-apps-674.md, genapps-constructs.py) against what relf reaches. Dispatches: lab/evolve/mech-dispatch.py
on portable-knee's profiling engine, each word's executions placed by the profiler (genapps.py's benchmarks, the
full run less the load).

## The census (static: what is compiled)

The four: 58 constant references, 236 variable references (79 followed by @, 77 by !), 16 `n + - =`, 1 `[']`, no
TO, **no DOES> word and no VALUE**, 149 definitions, 117 calls of a small straight word (at most 4 words). brainless:
812 constant references (with minif and wordfreq), 500 VALUE fetches, 250 TO, 179 uses of DOES> children - none of
them a `DOES> @` word - 683 definitions.

## Bytes saved (8-byte cells; the four / the held-out three)

| mechanism | s6: four / held-out | smallest: four / held-out | portable-knee: four / held-out | small-jit: four / held-out | fastest-x86-64: four / held-out |
|---|---:|---:|---:|---:|---:|
| 1 constants as literals, where not longer | 34 / 597 | 34 / 597 | 34 / 597 | 34 / 597 | 75 / 1251 |
| 2 a data word's @ and ! as one op | 188 / 106 | 188 / 106 | 196 / 111 | 203 / 114 | 359 / 199 |
| 3 DOES> @ as VAR@ | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| 5 n + - = as one op | 14 / 45 | 14 / 45 | 0 / 0 | 16 / 50 | 16 / 50 |
| 8 address literals in 5 bytes ([']; TO) | 4 / 1220 | 4 / 1220 | 4 / 1220 | 4 / 1245 | 4 / 1245 |
| 9 no JIT header (5 bytes a definition) | 0 / 0 | 0 / 0 | 0 / 0 | 745 / 3415 | 745 / 3415 |
| the instances, the four / held-out | const 58/812; var@ 79/52; var! 77/33; imm 16/50; tick 1/55; to 0/250; defs 149/683; small4 117/410; does 0/179 |

Small-word inlining (4) is not in the table: it trades bytes for dispatches (a 2-byte call becomes the body).

## Dispatches saved on portable-knee (share of each benchmark's dispatches)

| program | dispatches | 1 constants as literals | 2 data word @ ! fused | 4 small words (<= 4) inlined | 4 (<= 8) inlined | 680's VALUE (taken) |
|---|---:|---:|---:|---:|---:|---:|
| sim16 | 1,077,352,424 | 0.0 % | 13.8 % | 0.0 % | 1.9 % | 0.0 % |
| gc16 | 772,338,148 | 2.5 % | 7.1 % | 8.4 % | 9.4 % | 0.0 % |
| scan | 781,447,798 | 2.1 % | 24.9 % | 0.1 % | 0.1 % | 0.0 % |
| evo | 644,194,778 | 0.3 % | 3.5 % | 1.8 % | 1.8 % | 0.0 % |
| wordfreq | 634,026,226 | 0.4 % | 5.0 % | 1.3 % | 1.3 % | 0.0 % |
| minif | 414,056,038 | 5.7 % | 8.3 % | 0.0 % | 0.0 % | 0.0 % |
| brainless | 1,244,990,353 | 5.2 % | 0.2 % | 2.2 % | 4.3 % | 3.9 % |

## What pays - each mechanism's verdict for step 3

| # | mechanism | the four | held-out | verdict |
|---|---|---|---|---|
| 2 | a data word's @ and ! as one operation | 188-359 B (at relf's 2.5-byte form), 3.5-24.9 % of dispatches | 106-199 B, 0.2-8.3 % | **pays most: the first gene**. Its form decides the bytes - the engine's VARSLOT slot operands are 2-3 bytes, so a slot form costs about what a call and @ do; relf's is 2.5 |
| 1 | a constant compiled as its value, where not longer | 34 B (75 on the JIT designs), 0-2.5 % | 597-1,251 B, 0.4-5.7 % | **pays**: a gene, priced again on the compiling workloads - 59's rtlit lost there to a check on every compiled word (kernel 0.984, corpus 1.016) |
| 4 | small straight words inlined | bytes up (the body for the call); 0.1-9.4 % (gc16) | 1.3-4.3 % | **a trade: a gene with a size limit** (4 or 8 words) |
| 9 | the JIT designs: no 5-byte header a definition; a DODOES stencil | 745 B; DODOES 0 % of the four's dispatches | 3,415 B; DODOES 3.5-4.1 % on brainless | the header **pays** on the four; the DODOES stencil only on brainless |
| 5 | `n +`, `-`, `=` as one operation | 0 B on the knee (rtimm has `n +`), 14-16 B elsewhere | 45-50 B | small: rtimm's `-` and `=` forms, low priority |
| 8 | address literals in 5 bytes (8-byte cells) | 4 B (one `[']`) | 1,220-1,245 B (brainless's TO) | **invisible to the selection**: the owner's choice (the plan's first risk) - drop it, or a fifth program with brainless's mix |
| 3 | a `DOES> @` word's fetch as one VAR@ | 0 - no DOES> word | 0 - no `DOES> @` word in any of the seven | **does not pay on this code**: GOALS.md's register |

**Corrected at 685** (relf's answers, results/relf-reply-685.md): mechanism 2's bytes are about 0, not 188-359 - relf's own
VAR@ averages 3.2 bytes (a 2- or 3-byte self-relative slot operand), what a call and @ cost; it saves dispatches. And
mechanism 8: relf's code has no TO, VALUE or ['] - to drop. shellmix.fth (relf's mix) prices 3 and the DODOES stencil.

680's VALUE change, the count owed: 3.9 % of brainless's dispatches (500 VALUE fetches, each one CELL+ fewer); 0 on
the other six. Caveats: the variables' fused share is their references' static share (per variable); inlining counts
the call and the EXIT only; one interpreted design (the JIT designs' native code dispatches nothing); bytes from
674's per-construct averages - exact counts come with each gene built (step 3).
