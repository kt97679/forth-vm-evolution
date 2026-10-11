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

## The stacks apart, so the dictionary can grow (Iteration 184)

The owner's reason: with the stacks at the end of the dictionary's block, the
block cannot be grown; apart, it can. Right - with one constraint: addresses
are absolute everywhere (both stacks, the dictionary's links and heads, a
program's stored pointers), so the dictionary must never move - a realloc
that relocates the block would leave all of them pointing at freed memory.
Growth in place, then: a range reserved once, committed only where touched.

engine/vm-lab.c, the cv8 family (ENC 3: s6 and every evolved design): the
stacks in a page-aligned chunk of their own (guard pages included); the
dictionary an mmap reservation of MEMMAX, 256 MB (MAP_NORESERVE, MAP_32BIT
with 4-byte cells) - within the jail's 1 GB of address space and tag 2's 1 GB
call reach. The kernel: DICT-MAX (written by the converter) and DICT-LIMIT -
ALLOT's limit the reservation's end, or S0 less a margin where DICT-MAX is 0
(the other engines, unchanged); UNUSED takes it too.

Three faults found on the way:
1. sod16 and cpt16 (s1-s3) crashed with their stacks moved out of reach -
   those encodings keep the old layout.
2. ALLOT checked HERE + n against the limit: a 32-bit process placed the
   reservation at 0xE7FB6000, HERE + 2,000,000,000 wrapped under the limit,
   and full.fth's request was granted - the old layout's low block only hid
   it. Now n is compared with the room left.
3. That compare, unsigned, refused a negative ALLOT - giving room back - as
   "dictionary full": 35 of seed 40's 218 front designs wrong on the corpus.
   Now only n > 0 is checked.

Then: reseeded, run-tests PASS (32-bit stages and full.fth included), 7 of 7
IDENTICAL, the jail; all 218 front designs alive. Grown past the old 16 MB:
both evolved designs tried took 32 MB and ran a word defined there (HERE 33.5
MB above START) and refused 300 MB more; s6 refused to link a word across the
32 MB gap ("link out of reach" - its byte headers' links are short, Iteration
158), cleanly. results/pending/stacksep-after-seed41.patch. Made the default
for the cv8 family, not a gene: no workload outgrows 16 MB, so evolution
could not see what it is for.
