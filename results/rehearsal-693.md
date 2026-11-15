# Step 4's rehearsal for rtvar and rtconst (Iteration 693)

HANDOFF-REFERENCE.md's lesson (405): before the laptop runs a batch, the front evaluated with its genes on and a short
run, in a scratch clone (/tmp, the tree at 692). results/drafts/search-reopen-plan-677.md step 4.

## The front with the genes on: 10 of 10 alive, at both widths

evolve.evaluate() at 2 rounds, two widths, the ten roles with rtvar=1 rtconst=1 asked: every one status ok, its record
carrying the five programs' code (app, appby). What each can express: rtvar portable-fastest and fastest-x86-64 (it
needs spec var and varslot); rtconst those and least-memory, portable-small, portable-knee, portable-arm (it needs the
run-time fusers); neither smallest, best-all-round, small-jit, fastest-x86-32.

## The search's own score, the genes off against on (3 rounds, two interleaved pairs each; the sandbox)

| role | genes | speed (the gate's workloads) | the apps' code | image |
|---|---|---|---|---|
| least-memory | rtconst | 0.8231 -> 0.8225 (0.999) | 8,429 -> 8,531 | 9,566 -> 9,822 |
| portable-small | rtconst | 0.4692 -> 0.4655 (0.992) | 8,320 -> 8,422 | 9,135 -> 9,399 |
| portable-knee | rtconst | 0.3568 -> 0.3476 (0.974) | 8,365 -> 8,457 | 8,953 -> 9,169 |
| portable-arm | rtconst | 0.4068 -> 0.3923 (0.964) | 8,340 -> 8,433 | 9,098 -> 9,322 |
| portable-fastest | rtvar + rtconst | 0.3343 -> 0.3207 (0.960) | 8,392 -> 8,515 | 9,642 -> 10,274 |
| fastest-x86-64 | rtvar + rtconst | 0.1700 -> 0.1696 (0.998) | 9,988 -> 9,972 | 9,734 -> 10,398 |

The compile layer costs the kernel and corpus workloads nothing measurable; the gain grows from the size end to the
knee. The cost is bytes: each overlay's code in the image (rtconst about 220-260, rtvar about 380), and rtconst's apps'
code about 100 more - relf's rule lays a constant as its literal whatever its width, and a 16- or 32-bit literal is
longer than a 2-byte call. The size-end roles would pay about 350 bytes for nothing; the search weighs it. A narrower
value (fold only a literal no longer than the call) is a candidate, if a run shows the size end wanting the speed.

## The short run: --pop 8 --gens 2 --rounds 1 --seed 692

33 records, 29 alive. The deaths: two genomes with retired genes (varcall 0, doesfar 0 - their stages frozen; as
always), and two hand-made founders on the apps workload:

- **s2-cpt16** - calls out of reach within gc16 (dead on apps since Iteration 574's run);
- **s1-sod16 - new since 686**: it runs the four programs clean, and shellmix's DOES> buffers take its dictionary past
  sod16's DOES> reach - forth/sod16.4's DODOESF holds a 16-bit offset in half-words, 128 KB for the whole family. enc is
  not a mutated gene (sod16 and cpt16 enter only as hand-made founders), so the search loses a reference point, no
  candidate. Recorded, not changed: sod16 is a hand-made stage, not a role.

No live design in so short a run expressed either gene. Mutation reaches them rarely, but it does: of 4,000 mutations
of the front's roles, rtvar on 0.4 %, rtconst on 1.3 % - a laptop run's ~14,000 designs try each many times; and the
front's own evaluation above exercised both through the search's build.
