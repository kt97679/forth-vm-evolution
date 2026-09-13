# Who this is for, and what that changes

The English version goes to ForthHub's discussion forum; the Russian
version to Habr. Reading the forum first changed several decisions, so
the reasons are written down rather than left implicit.

## Who is actually there

The regulars include Mitch Bradley (Open Firmware, and therefore FCode),
Bernd Paysan (Gforth), Anton Ertl by reference, ruv, alexshpilkin,
alextangent, Anthony Howe. Discussion #187, "An elevator description for
Forth's threaded code models?", is 28 comments of exactly the material
this article is about.

These are people who have implemented the thing being described. That
is a gift and a hazard: they will find any claim that does not hold.

## What the forum tells us to do

**Use the community's taxonomy, and map our names onto it in the first
few paragraphs.** The thread settles on direct / indirect / subroutine /
token threading and byte-coded, with Bradley noting the "token threaded
variant where the pointers are not full addresses, but instead some
extra-compact representation like indices into an array, or
variable-length identifiers". That sentence describes SOD16, CPT16 and
the varint experiments precisely. Our names - CPT16, CV8, PACK4, PACK8 -
are local inventions and must be introduced as such, against the
standard terms, or the article reads as if it were unaware of the field.

**Do not skip literals and control flow.** ruv's immediate response to
Bradley's summary was "what about literals and control-flow? ... The
devil is in the details." Every encoding here had to answer that
question, the answers are in the overlay sources, and they are the
interesting part rather than an appendix. Same for `DOES>`, which is
where three of the bugs were.

**Be precise with terms.** In the same thread ruv rejects "closure" as
inappropriate for an indirect-threaded code field. Loose analogies will
be corrected in public.

**Cite the canon.** Brad Rodriguez, *Moving Forth* - referenced three
separate times in one thread, and the standard shared reference.
Loeliger, *Threaded Interpretive Languages* (1981). Ertl on dispatch.
Not citing these signals that the work was done in isolation.

**Tradeoffs, plural, named.** Bradley's fuller answer lists "size,
speed, ease of implementation, relocation, cross-platform portability,
and interactions with machine architecture details like memory models
and caching". Four of those are axes we measured and two are ones we
did not - relocation and portability - and RelF's relative addressing
has something to say about both.

**They will run it.** This is a forum where people build Forth systems.
One command to build, one to test, byte-identical verification, and
SOD32 vendored at a pinned revision. That is worth more here than any
prose.

## One thing to fix before publishing

`CV8-REFERENCE.md` credits Open Firmware's FCode for the byte-token
format with an escape for two-byte codes, and the parent project's own
notes flag it: the general shape is remembered, the exact ranges are
not, and it should be checked against IEEE 1275. Mitch Bradley wrote
Open Firmware and reads this forum. Either the claim gets verified
against the standard or it gets softened to "the same general idea,
from memory, not checked" - but it does not get published as it stands.

## Tone

The forum is technical, unhurried and allergic to salesmanship. The
strongest material here is the part where the work was wrong: two
designs rejected on a benchmark that was four times too harsh, a
regression inherited by omission and not noticed for two hundred
iterations, a test suite that passed while the compiler was broken.
That should be the spine, not a footnote at the end.
