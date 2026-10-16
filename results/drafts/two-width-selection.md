# Selecting at both widths - the skew in the evolution itself (Iteration 335, a draft)

Seed 55's checks measured the skew the owner feared: dream.lan ranks the laptop's designs at 64 bits
much as the laptop does (Spearman 0.940), but its 32-bit x86 build at 4-byte cells far less (0.694)
- the laptop's six fastest interpreted designs 8th to 13th there, their lead over s6 about halved.
The evolution selects on the laptop at 64 bits alone, so it is free to win there by what does not
carry. The owner: select at both widths. The laptop runs 32-bit x86 itself, natively (it builds the
-m32 engines the checks ship), so a 32-bit measurement costs no other machine.

## The decisions

1. **The JIT designs** - the speed frontier (0.13 of s6's time; the best interpreted 0.34) - cannot
   run at 32 bits: the JIT is x86-64's. Requiring a 32-bit measurement would drop them; ignoring it
   leaves the skew where the speed is. The proposal: a design's 32-bit measurement is **its
   interpreter's** - the design built with the JIT off (jit and its family unexpressed), at 4-byte
   cells - which is what runs on any host the JIT does not: a JIT design is judged at 64 bits by its
   JIT, and at 32 by the interpreter under it.
2. **How the two combine**: a **second speed objective** on the front (speed32 beside speed, size,
   memory), not one score - a combined score lets a design hide a weakness at one width behind a
   strength at the other, which is the skew again. A design good at both dominates one good at one.
3. **The cost**: a second build and measurement for each design that passes the 64-bit screening (a
   quarter are screened out first) - about 1.5x the evaluation time, a third fewer designs an hour.
   A cheaper 32-bit pass (fewer rounds, the four selection workloads) would bring it near 1.2x.
4. **The records**: speed32 in the database beside speed; old records without it - compare-fronts
   measures each front again every session, and would measure speed32 there too; the progress table
   and seed-facts report it.
5. **Correctness**: a design that does not build or live at 32 bits (as xcheck's --cell 4 finds)
   gets no speed32 - dominated on that objective, kept for the others.

## Next

Settle 1 and 2 with the owner; then evolve.py's evaluation (the 32-bit build and measurement after
screening), the front with four objectives, compare-fronts, seed-facts, the progress table; tests -
gene-equiv (no id changes), an evolution of a few generations at both widths, compare-fronts on it.

## Built so far (Iteration 336 - results/drafts/two-width-wip.patch; master without it)

The owner agreed: the JIT designs judged at 32 bits by their interpreter; speed32 a fourth objective.
In evolve.py: --widths 8,4; setup_widths() runs setup at 4-byte cells first (its reference, kernel
reference and k32 variants, under width-suffixed paths) and keeps REF, KREF, REF_CORPUS, KERNEL_IN
in WIDTH4, then setup as always; at_width() swaps those and the build's environment in and out;
eval32() measures the design with jit=0 as a 32-bit x86 engine, over the selection's workloads, a
round fewer, after the 64-bit measurement - speed32, or none and why32; dominates() and crowding()
take speed32 with --widths (none the worst: 1e9); CCV() gives clang -m32 too. Off, nothing changes.

**The first run** (a scratch clone, population 4, one generation, one round): it ran through; 20
designs, all alive at 64 bits; 12 with speed32, 8 without, and why: four "call target ... not
8-aligned" in the converter (and "v8 call target ... not a[ligned]") - the assertion that killed one
of seed 54's designs at 8-byte cells, at 4 far more often (code aligned to 4 there, and a call
encoding counting targets in 8-byte units); one corpus death at 4-byte cells. Both are faults to fix
before speed32 is selected on - else the selection pushes away from those encodings for a
converter's limit, not the design's. Then: compare-fronts (speed32 on its fronts too), seed-facts,
the report, next-run.sh's word for it (NEXT-RUN "widths"), the gate at both widths.

## The converter's alignment (Iteration 337 - in the draft patch)

Two faults, both "call target ... not aligned", both scaled calls (--cpt S reaches multiples of 2^S):
- **Word starts at 4-byte cells**: bodies aligned to CELL (4), S = 3 needs 8 - now CALIGN = max(CELL,
  2^S): at 8-byte cells (S 0-3) the cell, as before. The second scratch run: those gone.
- **SKIPPAD's shortcut** (the CPT16 family: a call to a data word lands past its NOOP pad at body +
  CELL - 2) is unreachable for S >= 2 - **seed 54's converter death** (1390 = 6 mod 8); now only where
  reachable, else the body itself. a2c8d50d0a (results/drafts/convert-align-death.md) converts and
  lives. Only designs that died change.
- **Left**: mid-word targets - DOES> tails, ALIGN_TAILS = 2^S only for S > 1 (layout.py:99); the second
  scratch run (population 4, seed 99: results/drafts/two-width-scratch-db.jsonl) still had 5 "v8 call
  target ... not aligned" and 1 CPT16 one, and 1 corpus death, at 4-byte cells. The designs:

    a9a65d6057 enc cell scale None tag2 None - died: corpus
    d113518703 enc cpt16 scale 3 tag2 None - died: image did not convert (AssertionError: call target 9780 not 8-al
    18a2c3e300 enc cv8 scale 3 tag2 None - died: image did not convert (AssertionError: v8 call target 8492 not a
    31f61139fa enc cv8 scale 3 tag2 None - died: image did not convert (AssertionError: v8 call target 8076 not a
    8f9272d24b enc cv8 scale 3 tag2 None - died: image did not convert (AssertionError: v8 call target 8452 not a
    b0aa079d67 enc cv8 scale 3 tag2 None - died: image did not convert (AssertionError: v8 call target 916 not al
    3cfd650b67 enc cv8 scale 3 tag2 None - died: image did not convert (AssertionError: v8 call target 8492 not a

  **Checked: every one is scale 3, not 1** - my tail hypothesis was wrong. Their targets are 4 mod 8
  (8492, 9780): word starts at 4-byte cells. The two align_up(off, CALIGN) changed are the HL and the
  byte-header paths; the third - ordinary headers (link cell, name padded to a cell, body after) -
  aligns a body only implicitly, to CELL. Next: pad that path's name so the body lands on CALIGN (at
  8-byte cells CALIGN is the cell: unchanged); then bisect the corpus death (a9a65d6057, enc cell).

## Built (Iteration 338)

- **The call scale at 4-byte cells**: the header padding of Iteration 337 let the images convert,
  but 7 designs then died on the corpus - run-time definitions align to the cell, and scale 3's
  8-byte units missed them. Taken back out; instead the 32-bit build of a design caps its scale at
  2 - nothing is 8-aligned at 4-byte cells; cell-aligned calls are its 32-bit form, as no JIT is.
- **The cell family's image**: build_other copied s0-cell-s64.img at any width - a 4-byte engine
  refused it, nothing printed (a9a65d6057); now the image of its width (and --validate's likewise).
- The scratch two-width run (population 4, one generation): **20 of 20 designs with speed32**.
- next-run.sh's word `widths`; the report's 32-bit column and seed-facts' lines, from the data;
  compare-fronts unchanged (64 bits: comparable with every earlier session) - a 32-bit section for
  it later.

