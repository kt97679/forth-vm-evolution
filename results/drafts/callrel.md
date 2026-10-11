# The gene callrel - a draft, not in the batch (Iteration 164)

The owner: tag-2 calls by their offset from the image base (today), by their
distance from the call site, or either - a bit saying which - all three as a
gene. results/drafts/callrel-draft.patch, against the eleven pending patches.

## Measured first (seed 37's smallest, 13 and 14 bits)

Executed calls, bytes each: from the base 2.00-2.10 on the eight workloads,
3.00 on far; from the call site 2.00-2.99 (bubble 2.82, sieve 2.99); either
2.00-2.10 and 2.00 on far. The kernel images' own calls (496 and 387 sites):
13 bits from the base cost +0 bytes (the images are under 8 KB), the call site
alone at 13 bits +35 and +41, either +0. A design whose image grows past 8 KB
would pay a byte per call to a word above 8 KB that the site form cannot take.

## Built

- vm-lab.c: CALLREL 0/1/2 - T2TARGET in the three decode labels and DODOES;
  at 0 the engines are byte for byte the same (12 stage engines checked).
- jit.c: the translator, its report and jit_repoint decode and re-encode by
  the mode (repoint keeps the call's own form).
- The converter: --call-rel 2 writes the kernel's calls in the base form with
  the low bit 0 (no positions needed); CV8-CALLREL-V and CV8-T2WIDE-V for the
  run-time compiler. 1 - by distance alone - refused: the converter would have
  to place the kernel's calls by distance.
- cv8t.4: CALL, and !CALL by the mode; T2CALL-REL picks the shortest form,
  never the 3-byte one under t2wide (140 of seed 38's 165 front designs).
- evolve.py: callrel 0/2 in the cv8 family, tag 2 only; off, it stays out of
  the id - every recorded design keeps its id.

## Tested

The smallest (t2wide), the JIT founder (t2wide, JIT) and a design without
t2wide, each with callrel 0 and 2: alive (the corpus, the kernel workload, far,
full), and the whole corpus compiled past a 4 MB ALLOT (the owner's trick: every
test word in long-call reach) gives the same output. run-tests PASS, 7 of 7
IDENTICAL at callrel 0.

## Why not in the batch yet

The run-time encoder lives in cv8t.4, so every tag-2 image carries it - the
smallest's image 6,990 -> 7,390 bytes, ~400 bytes, at callrel 0 too. It must go
to an overlay of its own, loaded for callrel designs only (one more dump
variant), CALL, reaching it through a cell the converter writes. Then the 167
designs swept at 0 and 2, the far benchmark timed at both, and 1 if the
converter learns to place calls by distance.

## Packaged (Iteration 167) - and why it is still a draft

CALL, reaches the encoder through CALLREL-XT, written by the converter; a
design without the gene leaves the encoder out: 56 bytes to the others, not
~400 (the smallest 7,062 -> 7,118; with the gene 7,406). But swept over seed
38's front with the gene forced on, 23 of 167 did not convert - "body size
drift" - every one with a kernel image past 8 KB: the converter writes the
kernel's calls in the base form only, so at 13 bits a call above 8 KB grows and
its sizing and emission passes disagree. The "+0 bytes" for either form assumed
the converter would choose the site form where shorter; it does not. Next: the
converter placing the kernel's calls by distance, sized to a fixed point - the
work the site form alone needs too. The draft: results/drafts/callrel-draft.patch,
against the fourteen pending patches.

## Rebased, and the drift fixed (Iteration 185) - results/drafts/callrel-draft-rebased.patch

Rebased onto the eleven after-seed-41 patches (a three-way merge; evolve.py's
two conflicts both sides' additions - the late genes, the cv8 family's
expressed genes). With the gene off, a design is alive and pays its 56 bytes
(note: the stacksep patch changes kernel.4 - a tree carrying it needs the
reseed, or ALLOT refuses everything; the batch's procedure does reseed).

The drift's cause, found: the converter encodes each word's tokens once,
before any offset exists - every tag-2 call sized 2 bytes - and emission
re-encodes each call against the true offset. At 13 bits a call to a word
past 8 KB came out longer than sized. Fixed without a fixed-point loop (which
would have to rerun the header links and all between placement and emission):
in hybrid mode a call is sized, at both passes, from an upper bound of its
target's offset - its old offset from the dump's lowest word, plus 1 KB for
the new header - and emitted at exactly that length, with an assertion that
the true offset fits. SEARCH-WORDLIST's drift is gone.

**Next blocker:** "short branch out of range" (-130 to -146) on part of the
front: the pass that chooses 8-bit branches estimates a loop body with 2-byte
calls; with calls sized by the bound the body grows past 128 bytes. That pass
must size calls by the same rule (sod16 shorten, or op_bytes' callers).

## The short branches, and why the bound will not do (Iteration 186)

Every design with the gene on now dies one way: "short branch out of range"
at emission. The converter's branch-shortening pass runs inside read_ops
(layout.py line 223, each word's operations read), long before the tag-2 map
is installed (line 511) - so it measures with the non-tag-2 sizes: every call
2 bytes, escaped opcodes 1. Base mode lives on the margins; the hybrid's
longer calls push loop bodies past 128 bytes.

And fixing that alone would not make the gene worth having: the bound of
Iteration 185 measures from the old, cell-sized dump (about 27 KB) where the
byte image is 7-11 KB - nearly every call to a kernel word past ~7 KB of old
offset is sized 3-4 bytes though its real offset is under 8 KB. Correct, and
larger than base mode: the gene's point lost.

**What it needs:** a real fixed point - place the image, take the true
offsets, size calls (and branches) from them, place again until nothing
changes (calls only grow, so it ends). layout.py places at module level
(placement, the header links, BSS, the tables between it and emission), so
that flow becomes a function rerun - a session's work. Or two converter runs,
the second sized from the first's CALLMAP offsets. To weigh with the owner as
well: the hybrid for run-time code only - but the engine has one call decoder,
so the image's calls would carry the flag bit too.

## Rebased onto the sixteen (Iteration 192); the fixed point, planned

results/drafts/callrel-draft-rebased16.patch: the draft on the after-seed-41
batch - two evolve.py hunks moved by rtloop=2's lines, mended; it parses.

The fixed point, as two converter runs rather than layout.py made a function:
pass 1 with every call long; its offsets are upper bounds for pass 2's, since
calls only shrink between them - so every word's offset, and every call's
distance (forward or backward: what lies between site and target only
shrinks), can only get smaller. Pass 2 sizes each call from pass 1's distance:
a call short there is short in the end. The short-branch pass needs the same:
measured in pass 2 with pass 1's tag-2 map installed, not the pre-tag-2 sizes
(the blocker of Iteration 186). Cost: one more converter run per design built.
Then the sweep of 186: the front with callrel=2 alive, and its bytes.

## The fixed point built, and measured (Iteration 193) - results/drafts/callrel-draft-twopass.patch

Two converter runs or more (lab/evolve/evolve.py): pass 1 sizes calls from the
loose bound and writes each word's call value (tools/layout.py --emit-offsets);
each pass after sizes from the one before (--call-bounds: upper bounds - calls
only shrink between passes); the first to convert after pass 1 is the image.
And the short-branch pass sizes a call as emission does (tools/sod16.py
op_bytes) - the blocker of Iteration 186 gone.

On the sixteen after-seed-41 patches, reseeded (27,120 bytes), stages rebuilt,
three rounds each - every one alive both ways:

| design | callrel=0 image / total | callrel=2 image / total | speed with callrel=2 |
|---|---|---|---|
| 0ceb043115, the smallest | 7,566 / 18,194 | 7,870 / 18,658 | sieve 1.20 -> 1.41, bubble 1.32 -> 1.50, corpus 1.34 -> 1.48 |
| d99e3d9ed9, the small knee | 7,358 / 18,402 | 7,678 / 18,818 | sieve 1.26 -> 1.42, bubble 1.22 -> 1.45 |
| 528c2523c3, the Q-best | 8,224 / 26,680 | 8,568 / 27,312 | fib 0.20 -> 0.22, bubble 0.15 -> 0.12 |
| d9247d19b0, the fastest | 8,384 / 31,000 | 8,776 / 31,776 | fib 0.22 -> 0.25 |

Worse on all four: +300-400 bytes of image, +400-800 in all - the flag bit
halves a 2-byte call's reach to 8 KB, and these images end just past it - and
the interpreted designs 10-17% slower on sieve, bubble and the corpus: every
call decoded tests the flag. The gain was to come from run-time code's
relative calls; these workloads do not have enough of them. Not in the batch:
the gene, there, would cost every tag-2 design ~48 bytes to be selected
against. Worth it, if ever, as calls relative only for code compiled at run
time, with the image's own calls left in the base form - an engine with two
call decoders, which is the owner's to weigh.
