# DOES> @ as a variable's fetch, in the gene rtvar (Iteration 695; step 3, mechanism 3)

relf's VAR@ takes DOES> @ too: a call to a DOES> child whose tail is `R> @` and EXIT - a VALUE (coreext.4's
`CREATE , DOES> @`), relfsh's and shellmix's buffers - is laid as vf of the child's parameter field. Part of rtvar
(forth/cv8-fuse-var.4's DOES-@): no gene of its own, no new dumps; no run has had rtvar yet. TO and >BODY ! store in
the field, and vf reads it at each use.

- **The tail** from the call (;CODE) stored after the child's DODOES (DOES-TAIL): the byte header's far form, 22 bits
  counting cells, and the tag's 4-byte form, 30 bits of bytes - the engine's DODOES decoding; the near form (doesfar 0,
  retired at 593) left a call.
- **`R> @` and EXIT** in any of the forms the compilers lay (TAIL-@?): three bytes; R> and @ with its EXIT folded in
  (the byte header's ;8, and the translator's folds); the pair R> @ and EXIT. tools/layout.py's VAR-OPS grows to 12
  bytes: the family, and those codes in the design's final one-byte codes, with which of them it has.
  SOD16_NO_DOESAT=1 writes them as absent, to measure.

## Checked (lab/evolve/rtvar-check.py): PASS on portable-knee, portable-fastest, fastest-x86-64

A DOES> @ child (V4) compiles to vf - on the byte header its first byte; under the tag, where T1's vf is - and reads
its body stored between two uses (5, then 9); a DOES> @ 1+ child (V6) stays a call (7).

## What it buys - shellmix alone (medians of 9, the full run less the load), and the apps workload (21, interleaved)

| design | shellmix: rtvar without DOES> @ | with it | DOES> @ itself | the apps workload, rtvar with DOES> @ |
|---|---|---|---|---|
| portable-fastest | 0.810 | 0.783 | 0.967 | 0.923 |
| fastest-x86-64 (JIT) | 0.925 | **0.606** | **0.655** | 0.948 |

On the JIT design a call to a DOES> child was refused by the JIT and took its callers down with it (results/
jit-shellmix-692.md: the hooks and buffers); as vf it is translated, and so are they. (rtvar-check's own five-round
measure of the apps workload read 0.991 and 1.140 on the same code - the interleaved 21 above are the figure.)
