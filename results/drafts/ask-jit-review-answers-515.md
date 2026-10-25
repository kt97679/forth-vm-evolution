# The answers to the bug hunt, checked - one real bug found and fixed (Iteration 515)

Four answers to results/drafts/ask-jit-review-511.md (three documents and one in the owner's message, 515), every claim
read against the code and, where it could be, run - on s6 interpreted and on JIT designs, at both widths.

## The real one: a word made after MARKER ran an older word's native code

**Reproduced**: `MARKER M1 5 CONSTANT K : USE K ; USE .` then `M1` and the same with 7 - the new K sits at the old K's
address (the program prints both addresses: equal). Interpreted: `5 7`. On a JIT design without jitinl: **`5 5`**.
**The cause**: words without the JIT header (kernel words, and CONSTANTs made at run time) are translated once and kept
in jit_k keyed by their address alone; MARKER (coreext.4) rolls the dictionary back, and the new word got the old
word's code - through a call from translated code and through EXECUTE's helper alike. With jitinl the CONSTANT is folded
into its caller and the cache is not consulted, which hid it from every test.

Answer 1 pointed here (its Bug 2: stale native code when a word reuses an address), though it blamed the EXECUTE cache's
key - that key (the four bytes after the token) does catch a changed body; the stale code came from jit_k behind it.

**The fix** (results/applied-after-seed71/jit-ksig-after-seed71.patch, the after-seed-71 batch's fifth): each jit_k entry also keeps
a hash of the bytes its translation read - to the word's end, found as the translator finds it; a different hash is a
different word, translated again. The reproduction gives `5 7` on every JIT design. tests/jit/jit-marker.fth (MARKER
three times, through calls and EXECUTE; and a user word shaped like EXECUTE) runs after extend.4 and coreext.4 on every
JIT variant at both widths in engines-check, which gains a variant without jitinl, so calls of headerless words go
through jit_k. engines-check PASS, 101 paths.

## The other claims

| Claim | Answer | Verdict |
|---|---|---|
| A user word `>R EXIT` (`: MY >R ;`) is translated as EXECUTE - diverges | 1 (Bug 4, "high") | **Not a bug**: in this interpreter `>R` then EXIT runs the token - it is how EXECUTE is defined (`: EXECUTE >R ;`); `5 ['] DUP MY-TOR +` gives 10 interpreted and native; now in jit-marker.fth |
| jitk's state forced to canonical after a fused pair | 1 (Bug 5, "low-medium") | **Correct by design**: base stencils take and leave the canonical state, as the unfused path sets it; the jitfuse-with-jitk variant passes at both widths |
| st_pick off by one (`0 PICK` should be the top) | 3 ("high") | **Wrong**: PICK consumes its count, so `0 PICK` is the item below it - sp[0]; jit-ops.fth runs PICK at both widths |
| 32-bit immediate holes (`imm32`) found but never patched | 4 ("high") | **True in the code, unreachable**: no operation maps to st_addi32 or st_dup_gti_br (its trigger `: T 42 + ;` is S_LIT/S_PLUS, or st_addi under jitfuse). **Hardened**: jit_usable refuses a stencil with a 32-bit hole |
| (ABORT")'s resume helper wired under JITMUL, its hole scanned under JITEXEC | 2 ("medium", conditional) | **Unreachable** - (ABORT") is decoded to its stencil under JITMUL too; consistent, but by two guards that must agree |
| No per-stencil check that every hole it needs was found | 2, 4 | **Fair** - a literal without its hole would copy the marker; the stencil checker vouches for the stencils, not the JIT. Proposed: a check build that scans copied code for any marker left |

## The answers, ranked

1 found the one real bug (by its effect, not quite its mechanism) and withdrew most of its own false starts in the open;
its two other claims were wrong. 2 claimed nothing it could not support and named the right missing invariants. 4 found
a real defect in the code, unreachable today. 3's one claim was wrong.
