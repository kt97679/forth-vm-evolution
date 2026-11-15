# Reopening the search - application code in the size score (Iteration 677; step 2 of results/generic-apps-674.md)

## The owner's decisions (677)

- **The search reopens** (step 2 after relf's report): the size score counts application code, and relf's run-time
  compiler mechanisms become genes, each priced on that code first.
- **The size**: one total - the engine, the kernel image, and the code the selection's four applications lay (sim16,
  gc16, scan, evo: lab/evolve/apps/, the `apps` workload's programs), bytes counted equal. Still three objectives, no
  weights. For application code this replaces Iteration 138's "the size is the kernel's"; an extension's own code
  (relf's shell, its OS words) stays outside the measure.
- **Held out, never objectives**: wordfreq, minif and brainless (lab/evolve/genapps.py), then relf's shell and rill3
  (step 3). Each processing reports them beside the selection.

## What the four lay now (674's table, 8-byte cells, bytes)

The knee 6,988, portable-small 6,948, smallest 7,524, s6 7,572, small-jit 7,860, fastest-x86-64 8,368; relf64 6,627,
relfasm64 6,543. A spread of 1,420 bytes across the ten - as large as their engines' differences - with the JIT
designs 0.9-1.4 KB behind the knee (the 5-byte JIT header per definition, the wide calls). The portable designs' gap to relf64 is
+5-6 % on the four against +9-10 % on brainless: the four use fewer VALUEs, DOES> words and strings, so a mechanism
for those may be nearly invisible to the selection (the risk below).

## The measure (step 0)

- evaluate() already runs the four in the `apps` workload. Each app's code bytes - HERE across its source, less its
  own data, as genapps.py counts them - measured in a deterministic run of its own (no timing; like the gate), once
  per design and width: `rec['app']`, and `rec['total'] = bin + size + app`. s6 the same (the yardstick's own).
- Checked against genapps.py on the ten designs and s6 at both widths, byte for byte; a planted change (one
  definition more in an app) must move it (prompts/15).
- Records before 677 have no `app`: compare-fronts, stopping.py and final-pick re-measure, never mix the two sizes.
  The stopping rule's ledger starts afresh (a new measure, new genes: GOALS.md, "Judging a run").

## The mechanisms - each priced on the four first (bytes exact, dispatches by the profiler; the held-out three beside)

| # | mechanism (relf's iteration) | what the lab has | the price to take |
|---|---|---|---|
| 1 | a constant compiled as its value at run time (681) | **rtlit, built and rejected at 59**: the COMPILE,8 check on every compiled word cost compiling workloads more than it saved (kernel 0.984, corpus 1.016, +132 bytes) - GOALS.md's register | again, now that the code it shrinks counts; relf's form (the CONSTANT's code field known at compile time) against 59's |
| 2 | a data word's fetch or store as one operation - VAR@, VAR!, 2VAR@, fused with the next (940) | the translator's vf/vs (VARSLOT) for kernel code, the JIT's jitvar - not used by the run-time compiler | the run-time compiler laying the opcodes the engine already has |
| 3 | a DOES> `@ ;` word's fetch as one VAR@ (260) | jitdoes (DOES> children native under jitx) | bytes and dispatches; for the JIT it also leaves no DODOES to refuse (674, item 6) |
| 4 | small straight words inlined at run time (683) | hotinl / hot-inline at image build, tag-2 designs only | a bytes-for-dispatches trade: a gene with a size limit |
| 5 | `LIT n +`, `-`, `=` as one operation (935) | rtimm (`n +` at run time, with spec imm) | rtimm's forms widened |
| 6 | inline strings not cell-aligned | kernel.4's (S") and (.") step past with ALIGNED | a pure saving: taken, not a gene (the standing rule), once measured to cost no speed |
| 7 | VALUE without its kind cell (8 bytes a VALUE, a CELL+ a fetch) | coreext.4's VALUE | a pure saving, as 6 - TO must still tell a VALUE (relf's way) |
| 8 | 8-byte cells: the dictionary at a low address, address literals 5 bytes not 9 (relfasm64) | - | the layout and the engine's load address |
| 9 | the JIT: a DODOES stencil, or 3's rewrite; the 5-byte header per definition and the 4-byte wide calls, on application code | - | priced on the JIT designs |

A mechanism that does not pay goes to GOALS.md's register with its numbers.

## The order - each step leaves a working, checked state

0. **The measure** (above): evolve.py counts the four apps' code; checked; run-tests, validate. **Done (678)**:
   results/app-size-measure-678.md; the cross-run tools refuse to pool the two sizes (679).
1. **The pure savings** (6, 7): kernel and library changes - every image and s6 move, so measured on the ten and s6
   before and after, speed by dispatches. **680**: 7 taken (coreext.4; the four do not see it), 6 priced and mapped -
   results/pure-savings-680.md; 6 built (681): results/unaligned-strings-681.md.
2. **The prices** of 1-5, 8, 9 on the four (and the held-out three) - a results file, a row each. **Done (684)**:
   results/mech-prices-684.md - 2, 1, 4 and 9's header pay on the four; 8 and 9's DODOES only on brainless; 3 nowhere.
   relf's answers (685, results/relf-reply-685.md): 8 is not relf's use (drop); 3 and the DODOES stencil pay on relf's
   shellmix.fth - a fifth selection program, the owner's choice; step 3 builds to relf's forms and rules.
   **686, the owner**: shellmix is the fifth (results/shellmix-686.md); 8 deferred - nothing dropped or limited.
3. **The genes** that pay, as a batch (results/pending/, ORDER.md, tools/batch-check.sh). The gene rules
   (results/seed63-rules.md): rule 11 - a gene leaves FROZEN only when a selection workload can see its benefit; the
   four apps' code is now one.
4. **The rehearsal** (HANDOFF-REFERENCE.md's lesson, 405): the front evaluated with the genes on, a short run, in a
   scratch clone; engines-check builds each gene's code.
5. **The laptop**: a seed per lab/evolve/NEXT-RUN, its hours the owner's; processed as usual; the stopping rule
   counts from it - its processing opens the new series (`NEXT_METHOD='...'`: stopping.py refuses the old one).
6. **After the search**: self-hosting phase 6 on the new roles (results/drafts/selfhost-plan-666.md) - the cross
   compiler learns any new way of laying the kernel; step 3's held-out checks; the article.

## What stays

- The translator (tools/layout.py) builds the search's images - the records' measure; the self-built images ship
  at the end. A run-time mechanism lives in the overlays, which both share; one that changes how the kernel is laid
  is made in both, and tools/selfhost-check.sh checks the cross compiler's form.
- Speed: the `apps` workload is in the speed score already. relf's shell is not an objective (RELF.md, 365).

## Risks

- **The four may not see a mechanism** (3, 7: few VALUEs and DOES> words in them). Step 2 says which; if one pays on
  brainless and not on the four, the owner chooses: drop it, or add a fifth selection program with brainless's mix
  (the option he did not take at 677).
- **Overfitting**: a gene chosen for the four's constructs. The held-out three at every processing are the check.
- **rtlit's lesson**: a check in COMPILE, costs every compiling workload (kernel, corpus); price speed as well as
  bytes.
- **Comparability**: the records and the article's figures before 677 measure the old size; the article says so.
