# The nine likely retire candidates - what retiring each would remove (Iteration 573)

Seeds 77-83's true fronts have nine of the ten re-enabled genes at their old values everywhere (confirm.py on their
results files; alignhot the exception). Retiring one (GOALS.md step 3, consolidation - the owner's decision) means
fixing it at its old value and removing the other value's code. Read here before seed 84 returned: the gene's hooks
(evolve.py), the code they reach, the hand-made stages that use the other value (evolve.py's HUMAN, as built), the
couplings. Line counts are a grep's, not an audit.

| gene | old value | the other value's code | a hand-made stage uses it | coupling | retiring it removes |
|---|---|---|---|---|---|
| bytehdr | 1 | full headers - the older formats | s4 (bytehdr 0) | scale > 0 only without byte headers | a gene; the code builds s4 |
| varcall | 1 | fixed call slots (-DVARCALL=0) | s4 (varcall 0) | implies sharedcall; doesfar and hotcalls need it | a gene; the code builds s4 |
| doesfar | 1 | near DOES> only | s5 (doesfar 0) | needs varcall | a gene; the code builds s5 |
| scale | 0 | scaled call targets (-DSCALE, --cpt N) | s2 1, s3-s5 3 | never with byte headers: every front design has them | a gene; the code builds s2-s5 |
| sharedcall | 0 | -DSHAREDCALL without varcall | none (s4: 0, s5-s6: implied) | varcall=1 implies it - no effect on any modern design | the gene only; the engine path stays (every varcall design builds it) |
| thinhdr | 1 | 32 thread heads (layout.py --thin-header off) | none | - | the switch: a few lines of tools/layout.py |
| bss | 1 | scratch buffers in the file (--bss off) | none | V8 and the CV8 compiler | the switch: a few lines of tools/layout.py |
| lean | 1 | the X8 copies and the dump tool kept | none (s5-s6 lean) | - | the switches: a few lines of layout.py, build-stages.sh's flags stay |
| msc | 0 | multi-state stack caching: tools/gen-msc.py (330 lines), evolve.py's hooks | none | excludes the JIT (jit_on needs msc 0), and t2wide with tos | the only real removal - about 350 lines |

**What it says.** Retired as genes, the nine shrink the search space, but little code goes - except msc - because the
old values' code builds the hand-made stages s2-s5, which validate rebuilds (7 of 7 IDENTICAL) and the article's story
of the stages uses. Suggestions, for the owner at consolidation:
1. bytehdr, varcall, doesfar, scale: the deciding question is the stages, not the fronts - kept while s2-s5 are built;
   retired only with a decision to freeze the stages as built artefacts.
2. sharedcall: the gene can go alone - it does nothing on any design with varcall 1, and s4 needs it at 0.
3. thinhdr, bss, lean: the transformations unconditional - a few lines each; the mechanisms stay.
4. msc: its evidence is x86's, where the JIT wins the fast end and excludes it; on the Tegra (no JIT) it was never
   measured, since no msc design reached a front. Before retiring it: a few msc=1 and msc=0 non-JIT designs of seed 84's
   database asked for by id on the Tegra (xcheck.py --also), so a design good there is not lost on x86's evidence.
