# The after-seed-56 batch - applied (Iteration 354)

| # | patch | what it does |
|---|---|---|
| 1 | two-widths-after-seed56.patch | **Selecting at both widths** (the owner, Iterations 336-338; results/drafts/two-width-selection.md). evolve.py --widths 8,4: setup at 4-byte cells first (setup_widths: its own reference, kernel reference and k32 variants under width-suffixed paths), then as always; each design passing screening also measured as a 32-bit x86 engine at 4-byte cells (eval32: its JIT off, its call scale at most 2, a round fewer, the selection's workloads) - speed32, a fourth objective in dominates() and crowding(); none, with why32, if it does not build or live so. NEXT-RUN's word: widths. The report's 32-bit column and seed-facts' two-width lines from the data. **The converter's call alignment** (tools/layout.py): bodies aligned to max(cell, 2^scale) - the cell at 8-byte cells; SKIPPAD's shortcut only where a scaled call reaches it - seed 54's converter death (a2c8d50d0a) converts and lives. **The cell family's image** by width (and --validate's). No gene; ids unchanged. compare-fronts still judges at 64 bits. |
| 2 | jit-genes-after-seed56.patch | **Two JIT genes** (Iterations 339-343; results/drafts/next-genes.md): **jitimg** (0/1) - the image's words JIT candidates: the converter gives the outer interpreter's plain code words (INTERPRET, PARSE-WORD, WORD, ...; no inline aligned data, nothing landing inside them) the header run-time words get - [the JIT opcode][length \| 2^31] - translated on their first call or left bytecode; (2, every plain word, killed on the corpus: not offered). **jitvar** - vf and vs (getstatic, putstatic) given the JIT as a literal of the slot's address then @ or !: two operand kinds in jit.c's decoder under JITVAR, no new stencil. jitleft.py --set=gene=value. On top of patch 1 (tools/layout.py's CALIGN). |
| 3 | compare-widths-after-seed56.patch | **The comparison at both widths** (Iteration 352): compare-fronts.py --widths 8,4 sets up both widths and, after its rounds, measures each design's interpreter as a 32-bit engine at 4-byte cells (eval32, half the rounds); a section "At 32 bits": each run's fastest there against all the others', and its 64-bit fastest at 32 bits - so a two-width run is judged at 32 bits too. Without the flag, setup() itself: unchanged. On top of patch 1 (eval32, setup_widths). |

    git apply results/pending/two-widths-after-seed56.patch
    git apply results/pending/jit-genes-after-seed56.patch
    git apply results/pending/compare-widths-after-seed56.patch

Tested on master at Iteration 338 (results/drafts/two-width-selection.md, "Built so far", "Built"):
- **64 bits unchanged**: six recorded designs of seed 55's front - engines and images byte-identical
  against a clean clone; gene-equiv.py: PASS - 4,096 recorded genomes, every operator draw; run-tests
  PASS; validate 7 of 7 IDENTICAL; the gate: alive: 248 of 248 (the run's front 168, the joint front 133, 53 in both).
- **Two widths**: scratch runs (population 4, one generation, seed 99) - the first 12 of 20 designs
  with speed32; after the alignment fixes, the scale cap and the cell family's image, **20 of 20**
  (results/drafts/two-width-scratch-db.jsonl is the second run's). The report shows the 32-bit
  column from the data alone (no flag); seed-facts' lines: 7 of 7 of the front with speed32,
  Spearman 0.643 between the widths there.
- On a fresh clone of master after Iteration 338 it applies and reproduces the tested files.

To use it: NEXT-RUN "seed N tag2 Hh widths ..." - each design costs about one more build and
measurement, so fewer designs an hour.

Patch 2 tested on master with patch 1 (Iteration 343): off, six designs of seed 55's front -
engines and images byte-identical to patch 1's; gene-equiv.py: ids and expressions of all 4,096
recorded genomes unchanged (the operators' draws differ, as a new gene makes them); run-tests PASS,
**66 engine paths** - three new: jitimg with jitvar, jitvar at varslot 0 and 1; validate 7 of 7;
**forced: 16 of 16 JIT designs of seed 55's front alive with jitimg 1 and jitvar**; the gate 248 of
248. jitleft --why on c549c0677c with both: INTERPRET tried (refused for PLACE), PARSE-WORD and WORD
refused for (PARSE) - the next step is helper calls (results/drafts/next-genes.md). On a fresh clone
the two patches apply in order and reproduce the tested files.

**Patch 2 corrected (Iteration 345)**: jit.c filled a literal hole from the decoded operand only for
operand kinds 1-5, and jitvar's slot kinds are 8 and 9 - a translated vf would have pushed k (0) and
fetched from address 0: latent, no word with vf being translated yet; found reading the emitter for
the helper calls. JIT_LITOPND(o): with JITVAR the slot kinds too; without, the original tokens
exactly. Re-verified: six designs byte-identical to patch 1's (a first, parenthesized form changed
three JIT engines - GCC built `a && b && (c && d)` differently from the flat chain; builds proved
deterministic); run-tests 66 paths, validate 7 of 7, forced 16 of 16, the gate 248 of 248.

Patch 3 tested (Iteration 352): two small databases (the two-width scratch run's, halved) compared
with --rounds 2 --widths 8,4 - s6 at 32 bits against itself 1.005; each run's fastest at 32 bits and
its gain against the other; status 0. Without --widths the setup is setup() itself (setup_widths()
calls only it). To use it, NEXT-RUN's comparison: experiment compare-fronts.py --rounds 6 --widths 8,4
--frontier --cpus 2,8 - about half again its time (each design built and measured at 32 bits too).

**Applied on master at Iteration 354**, the three patches in order: build-stages; run-tests PASS, 66
engine paths; validate 7 of 7 IDENTICAL; the gate 268 of 268 alive (seed 56's front 187, the joint
front 136, 55 in both) - a front none of the three was developed against.

