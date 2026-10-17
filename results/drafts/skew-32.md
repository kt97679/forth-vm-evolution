# Why designs lose at 32 bits - the skew, taken apart (Iteration 352)

Seed 55's checks measured the skew (dream.lan, 32-bit x86: Spearman 0.694 against the laptop). Here,
on the VM (it runs -m32 natively), each design's **interpreter** (its JIT off) measured at both widths
- r = its speed at 32 bits / its speed at 64, each relative to hand-made s6 at that width: r = 1 keeps
its place, r > 1 loses ground. (The 32-bit build caps the call scale at 2.) Scratch: master with the
pending two-width batch, evolve.py's evaluate() with --widths' eval32.

## Thirty designs of seed 55's front (results/drafts/skew-32-front.jsonl)

r: median **1.30**, from 0.98 to 2.44. Two groups: the fastest interpreters (0.39-0.45 at 64 bits) lose
most among the fast (r 1.3-1.55; the middle, 0.6-0.78, r 1.0-1.1); and the slow small end of the
front (non-JIT, 0.56-1.32) collapses - r 1.6-2.4, twice s6's time at 32 bits. By gene value (a
correlation, the slow end being one lineage): opt O2 r 1.69 against Os 1.17; without kfast, t2wide or
rtloop 1.62-1.70 against 1.23-1.26 with; without an opcall 1.46 against 1.05.

## Knockouts - each gene where a design differs from s6, set to s6's, one at a time
(results/drafts/skew-32-knockouts.jsonl; one measurement each on the VM: effects under 10% are noise)

**c549c0677c, the fastest** (0.392 at 64, 0.590 at 32 - r 1.51):
- **compiler**: r 1.01 - 64-bit 0.602, 32-bit 0.607. Its compiler choice is worth 35% at 64 bits and
  nothing at 32.
- **tag2**: r 0.99 - 64-bit 0.464, 32-bit **0.461**: the two-bit tag helps at 64 bits and **hurts at
  32** - without it the design is 22% faster there.
- ops10: r 1.10 - the C primitives help at both widths, more at 64 (0.39 vs 0.74) than at 32 (0.59
  vs 0.81). escape r 1.20, opt r 1.26, supers r 1.30: each helps at 64 and costs at 32.

**4c908aedb2, the slow end** (1.308 at 64, 2.220 at 32 - r 1.70):
- **fsys**: r 1.02 - 64-bit 1.114, 32-bit **1.138**: the Forth file layer over SYSCALL is the whole of
  the 32-bit loss (2x), and costs at 64 too. tag2 r 1.42 again.

## What it says

The skew has a few causes with names, and two look like **the engine's inefficiencies at 32 bits**,
not trade-offs: the two-bit tag's decoding and the Forth file layer are far slower at 4-byte cells
than their work needs - worth reading as engine bugs (the tag's call decode, cbase arithmetic; the file
layer's 64-bit arithmetic, the system call's mapping) before leaving them to the selection. The
compiler's 64-bit-only gain is the selection's to weigh - speed32 makes it visible to it. Selecting at
both widths (the pending batch) will push against tag2, fsys 3, escape and supers at 32 bits.
