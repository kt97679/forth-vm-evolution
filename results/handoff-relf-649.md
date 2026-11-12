# The relf handoff after the final check - the smallest changes (Iteration 649)

results/handoff-relf-611.md stands - the roles, how to build, run and check a design, what relf takes - with 628's three
(results/handoff-relf-628.md), 631's small and fast on ARMv7 (results/handoff-relf-631.md), 636's knee
(results/handoff-relf-636.md) and now the smallest to d180351903 (the owner, 649: the final check's one candidate without a
trade - the evidence results/followup-roles-seed91-final.md). The ten, by role: results/relf-designs-649.md; the package:
forth-vm-evolution-designs-iter649.tar.gz (lab/evolve/pack-designs.py on it, each design at both widths - 20 of 20
builds 9 of 9 right against s6); `make` builds them from designs/ (export-designs.py and export-arm.py: smallest made again,
the lab's bytes at both widths and for ARMv7, forth-arm running under qemu-arm; make test 10 of 10, make 32, make libc).

| role | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | bytes, 4-byte | memory KB | JIT | checks (8 / 4) |
|---|---|---|---|---|---|---|---|---|---|
| smallest | d180351903 (was 64a7345393) | 1.926 | 1.784 | 1.717 | 13,883 | 13,627 | 116 | no - portable | 9/9 / 9/9 |

Speeds as 611's table: the classes of final-pick.py step 5, re-measured in the final check
(results/followup-pick-seed91-final.md; 64a7345393 there 1.937, 1.855, 1.775). Against the holder it replaces, paired by
session: smaller at both widths (8 B at 8-byte cells, 48 B at 4-byte: 13,627 against 13,675), x86-32 -3.85% +/- 0.25%
(faster on both x86 machines), ARMv7 -3.30% +/- 0.68% (two Tegra sessions, one chain), x86-64 -0.59% +/- 0.29%, the same
memory. At 8-byte cells the two x86 machines split - the owner's laptop (Ryzen 7 PRO 8840HS) 3.4% slower, the i7-6700 4.4%
faster - so for a build at 8-byte cells on a Zen-class CPU 64a7345393 is the faster of the two; its record stays in
results/relf-designs-636.md. The engine is 48 B larger - four more primitives (0<?BRANCH, I, UNLOOP, FILL, CMOVE in,
=I?BRANCH out) - and the image 56 B smaller; the mechanisms the same. The other nine unchanged: c7c35f9c97, ee34931cd7,
06b188f45b, c6f1c1331b, 782f3ad7ff, 3eb59b271d, 11a56ff9e4, ae99617f06, fb0d57c8a2.

Reading the ARMv7 column (648, results/followup-roles-seed91-final.md, "The Tegra between chains"): on the Tegra, two
designs within a few percent of each other do not keep their order from one measuring chain to the next - a pair swung
4-5% (its kernel moved from 7.3.1 to 7.3.3 between chains). The ARMv7 roles were decided over every session pooled (629's
rule); take the column as a band of a few percent - portable-small (ae99617f06) and a627b954c6 are interchangeable there,
and so are portable-arm (3eb59b271d) and 7fb40ff7ba (-0.94% in the final check).
