# The drafts read as a ForthHub member would (Iteration 661)

The owner asked for the ASCII diagrams aligned, every abbreviation explained before its use, and the article read from
an average ForthHub member's side. Done in both drafts (article/article-en-draft.md, article/article-ru-draft.md):

- The introduction's figure: the cell labels now span their cells (they drifted a column per cell), the CV8 row's
  labels sit under their bytes, the three totals end in one column. The Russian bar chart's label column widened for
  its longest label; the English chart's "CV8 + spec" is "CV8 + specialised". The other two figures were aligned.
- Before use: the vocabulary paragraph and a sentence naming the figure's three rows now come before it (CV8 had no
  introduction before section 6); PACK4 and PACK8 named where they are introduced; "kernel compile" said once, in
  section 2; folding and specialisation named in section 7 (the chart's rows had no text); JIT, ANS Forth, COLE and
  NSGA-II expanded at first use; the front defined before Pareto rank, the rank and crowding distance said in words; a
  run named by its seed, a session, a rank correlation, portable (no JIT), the laptop and the ARM board at first use.
- Facts: the corpus is 616 cases at the ladder's commit and 661 now (the drafts said 616 for every system); section
  15's "final set is 21 designs" is the set kept then - section 17 ends with the ten roles.

For the owner - changes a ForthHub reader would want, not made:

1. (Done, Iteration 662: the paragraph under the final table.) What the winners are made of: under the final table, a few lines on each kind of design - its encoding, the top of
   the stack in a register, the fused pairs, the JIT (designs/README.md has every design's genes). That is what a Forth
   implementer takes home, and the article now gives only roles and numbers.
2. (Done, Iteration 662: section 18.) A closing paragraph on what would carry into another Forth, from the measured steps: the size came from the byte
   code and the byte headers, the speed from specialisation and the JIT.
3. (Done, 664: plain words instead of the run file's line; section 14's raw line too.) Section 12's plumbing - the NEXT-RUN line, "experiment review-checks.py spread" - is the workflow, not the result;
   the one command is enough.
4. (Done, 663: one standard error of the ratio over the five builds - tools/collect-results.sh.) Section 5's "error 0.021" does not say what kind (the spread of the five builds?).
5. (Done, 663: CV8 is compressed-pointer, variable-length, 8-bit units - forth/cv8.4; CPT16 compressed-pointer
   threading - engine/vm-lab.c.) CV8 and CPT16 are explained by what they do; if the names stand for something, say it once.
6. (Done, 663 - one board, the owner: "the Tegra" throughout, named in section 4.) Part one's ARM board (a 4-core ARMv7) and part two's NVIDIA Tegra: if they are one board, say so once.
7. (Done, 663: `CALL,` from forth/cv8.4 and the CV8 dispatch from engine/vm-lab.c, both at a105e59, in section 6.)
   Some code: the CV8 dispatch loop or its opcode table, a dozen lines - ForthHub readers read code.
8. Length: about 5,000 words - one ForthHub post can carry it; for Habr, the split at the part boundary.

Also done, 663 (the owner: make getting each winner's code absolutely clear): a `make` column in the final table and,
under it, the clone, build and run commands, and the other builds' names.
