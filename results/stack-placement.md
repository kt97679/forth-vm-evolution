# The stacks' place - the owner's question (Iteration 183)

"Keep the stack in the same memory chunk as the dictionary, or in a separate
one?" Where they are now (engine/vm-lab.c): one block of MEMSIZE (16 MB); the
image at its bottom and the dictionary growing up; the return stack its top 64
KB, from the very top down; the data stack from just below that, 256 KB room.
Stacks and dictionary are already 16 MB apart: separate pages, separate TLB
entries, the same pages touched either way - a separate block would change
neither speed nor peak memory, and would need the kernel's "dictionary full"
check (ALLOT: S0 minus a margin) to take its limit from elsewhere. Its one
gain, guard pages, the gene guard already gives.

What placement can change is how the two stacks' top cells sit within their
pages. A load can be held up by an earlier store whose address agrees in its
low 12 bits (4K aliasing - Intel's cores most of all). Without guard: the data
stack's cells at page offsets 4080, 4072, ...; the return stack's at 4088,
4080, ... - the same offset whenever the return stack is one cell deeper, and
both are touched on nearly every operation. With guard, at 66 cells deeper.

Priced on the development VM (one Intel Xeon core): seed 40's smallest, the
data stack started 0 or 2,048 bytes lower, timed against s6 by the evolver's
own measure(), alternating, twice: the same build's two rounds differ by up to
9% (bubble 1.19 against 1.29) - more than any difference between the builds
(+9.7% to -3.4%, no direction). Not measurable here; the laptop measures to
about 1%.

**The gene dskew** (0, 1): 1 starts the data stack 2 KB lower - no kernel
change (COLD takes S0 from where the stack starts), a late gene (every
recorded id kept: 218 of 218), mutation reaches it. Pending after seed 41:
results/pending/dskew-after-seed41.patch. Found on the way: a hand-made
genome reached the engine flags without the late gene's default - eff[k] a
KeyError, three stages failing validate; eff.get(k) now.
