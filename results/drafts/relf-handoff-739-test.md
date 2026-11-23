# Notes for results/drafts/relf-handoff-739.py - the test: 726's prose (Iteration 739)

The generator's notes file for its test: the 726 roles against the 657 handoff, with what results/handoff-relf-726.md
said by hand. The final handoff's notes take this form - three sections, bullets (or one paragraph for the history).
Run, as the build user from the repository's top:

    python3 results/drafts/relf-handoff-739.py --iter 726 --records results/relf-designs-718.md \
        --previous results/handoff-relf-657.md --package forth-vm-evolution-designs-iter726.tar.gz \
        --notes results/drafts/relf-handoff-739-test.md --sha results/drafts/designs-sha256-718.txt

## Changed

- **The measure** (676-686): the size is the engine, the image and the code the five selection programs lay (sim16, gc16,
  scan, evo, shellmix - relf's shellmix.fth the fifth, 686), at 8-byte cells - so the bytes below are not comparable
  with 657's (which were the engine and the image only).
- **The search reopened** (677-704): seeds 92-96 with the run-time genes rtvar (a data word's @ and ! as one operation,
  relf's VAR@ and VAR!), rtconst (a constant compiled as its value - relf's rule), rtinline (a body of at most 3
  instructions in 6 bytes copied for its call - relf's inlining rule), DOES> @ in rtvar; the unaligned strings and VALUE
  without its kind cell taken for everyone (680-681). The series stopped at seed 96 by its rule.
- **The roles chosen again** (705-725): chains A-D on the laptop, dream and the Tegra - A a screen of 944, B a shortlist
  of 99, C the 66 it could not settle, D the smallest JIT design's band (results/followup-roles-seed96-roles.md, -b.md,
  -c.md, followup-roles-seed96-jitband.md); the ten by the rule - 1 % smaller, no machine class 2 % slower, memory within
  8 KB; a speed role's challenger 2 % faster at 2 SE - results/new-roles-718.md, with every near design kept on record
  there.
- **The self-hosting gate** (721-726): lab/evolve/selfhost-speed.py on the laptop - 5 alternations of 10 rounds, both
  widths; a self-built image more than 2 % slower than the translator's ships the translator's. The instructions the
  same (721): code placement. portable-fastest, self-built since 722, passed at 726 (0.997 at 8-byte cells, 0.987 at 4).

## For relf

- **New: relf's own mechanisms measured in the lab** - rtvar, rtconst and rtinline (relf's VAR@/VAR!, constant rule and
  inlining rule; results/mech-prices-684.md, relf-reply-685.md): which of the ten carry them is in their genes above;
  shellmix.fth (relf's) is in the size and the speed.
- The GCC three on the Tegra: engines of 16,782, 13,014 and 11,158 B, running their self-built images
  (results/rage-designs-726.md).

## History

601-657: results/handoff-relf-657.md, "The history". 718: the new roles chosen (results/new-roles-718.md; the records
results/relf-designs-718.md). 721: this document drafted. 725: small-jit confirmed (chain D) and the gate's three
shipped translator-built. 726: the rage check passed on the self-built images, portable-fastest passed the gate - this
document.
