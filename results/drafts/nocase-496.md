# The case-insensitive gene - where it hooks in, planned (Iteration 496)

The owner (468): a case-insensitive gene, with a concern for real programs that might rely on case. Appbench's lexex and
benchgc stop on lower-case names made or read at run time (results/drafts/appbench-467.md) - no folding of their source
reaches those; the systems they were written for (Gforth, SwiftForth, VFX) fold case.

**The concern, weighed**: a program defining two words that differ only in case would break - rare, and by Forth 2012
non-portable (a program that depends on a system's case sensitivity has an environmental dependency). As a gene it
breaks nothing: off by default, a design without it as today. Only ASCII letters folded, so UTF-8 names are untouched.

**Where it hooks in** (read here, 496):
- Every lookup copies its key into NAMEBUF first - NAME>BUF in kernel.4, NAME>BUF8 in the kfast overlay - and every
  search compares NAMEBUF against the stored names: SEARCH-WORDLIST (cells), cv8b.4's SEARCH-WORDLIST8 (count and
  bytes), the (FIND) primitive (vm-lab.c's L_x_find, klookup's), THREAD-FIND. So **folding NAMEBUF after the copy**
  folds every search, the C ones included, with no change to them.
- Every definition's name is stored by HEADER (kernel.4) - **folding the stored name** there makes the dictionary upper
  case; REVEAL's HASH then hashes the folded name, as a search's HASH must hash the folded key (to check: that the
  search hashes NAMEBUF, not the caller's string).
- The mechanism: an overlay, forth/cv8b-nocase.4, loaded for the gene as cv8b-kfast.4 is - each X8 word in it gives the
  kernel's X its body, so every caller gets it (evolve.py's overlay()). It must compose with kfast (which has its own
  NAME>BUF8) and klookup/kinput: one NAME>BUF8 per combination, or the folding as its own word called from both.
- The kernel's own names must all be upper case already (a lower-case one would become unfindable) - to check over
  kernel.4 and the overlays; the converter could assert it.

**The test**: lexex and benchgc unshimmed (appbench.py with the folding of their source off) on a design with the gene;
the corpus and the Forth 2012 suite (ans-check) with lower-case test files; every engine path (engines-check).
