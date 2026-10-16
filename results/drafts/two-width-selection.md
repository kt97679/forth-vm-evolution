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
