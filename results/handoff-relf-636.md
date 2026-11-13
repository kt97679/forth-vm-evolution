# The relf handoff after seed 90's follow-up - the knee changes (Iteration 636)

> Replaced: the relf handoff is results/handoff-relf-657.md (Iteration 657) - the final one, all ten roles in one document.

results/handoff-relf-611.md stands - the roles, how to build, run and check a design, what relf takes - with 628's three
(results/handoff-relf-628.md), 631's small and fast on ARMv7 (results/handoff-relf-631.md) and now the knee to 11a56ff9e4
(the owner, 636: by the rule fixed before seed 87 - the evidence results/followup-roles-seed90.md). The ten, by role:
results/relf-designs-636.md; the package: forth-vm-evolution-designs-iter636.tar.gz (lab/evolve/pack-designs.py on it,
each design at both widths - 20 of 20 builds 9 of 9 right against s6); `make` builds them from designs/ (export-designs.py: portable-knee made again, the
lab's bytes at both widths; make test 10 of 10).

| role | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | bytes, 4-byte | memory KB | JIT | checks (8 / 4) |
|---|---|---|---|---|---|---|---|---|---|
| the knee: fast portable on x86, small | 11a56ff9e4 (was c2ef9488ff) | 0.363 | 0.377 | 0.477 | 19,761 | 19,369 | 140 | no - portable | 9/9 / 9/9 |

Speeds as 611's table: the classes of final-pick.py step 5, re-measured in seed 90's follow-up
(results/followup-pick-seed90.md; c2ef9488ff there 0.357, 0.391, 0.476). Against the holder it replaces, paired by
session: 5.45% smaller (1,140 B; at 4-byte cells 19,369 against 20,829, 7.0%), x86-32 -3.59% +/- 0.43% (faster on both x86
machines), x86-64 +1.54% +/- 0.25%, ARMv7 +0.35%, the same memory. At 8-byte cells the two x86 machines split - the
owner's laptop (Ryzen 7 PRO 8840HS) 4.4% slower, the i7-6700 1.2% faster - so for a build at 8-byte cells on a Zen-class
CPU c2ef9488ff is the faster of the two; it stays in the final set. The other nine unchanged: c7c35f9c97, ee34931cd7,
06b188f45b, c6f1c1331b, 782f3ad7ff, 3eb59b271d, ae99617f06, fb0d57c8a2, 64a7345393.
