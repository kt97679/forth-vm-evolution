# The relf handoff after seed 90 - small and fast on ARMv7 changes (Iteration 631)

results/handoff-relf-611.md stands - the roles, how to build, run and check a design, what relf takes - with 628's three
(results/handoff-relf-628.md) and now small and fast on ARMv7 to ae99617f06 (the owner, 631: the rule fixed at 629; the
evidence: results/xcheck-seed90.md and results/followup-roles-seed89.md, "The re-measure's verdict"). The ten, by role:
results/relf-designs-631.md; the package: forth-vm-evolution-designs-iter631.tar.gz (lab/evolve/pack-designs.py on it,
each design at both widths - 20 of 20 builds 9 of 9 right against s6); `make` builds them from designs/
(export-designs.py: portable-small made again).

| role | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | bytes, 4-byte | memory KB | JIT | checks (8 / 4) |
|---|---|---|---|---|---|---|---|---|---|
| small, fast on ARMv7 | ae99617f06 (was a627b954c6) | 0.450 | 0.444 | 0.351 | 18,599 | 18,131 | 124 | no - portable | 9/9 / 9/9 |

Speeds as 611's table: the classes of final-pick.py step 5, re-measured in seed 89's follow-up
(results/drafts/smallarm-classes-631.py; a627b954c6 there 0.453, 0.444, 0.359). Against the holder it replaces, every
Tegra session pooled - the follow-up's three at 10 rounds and seed 90's three at 3: -2.30% +/- 0.42% on ARMv7, all six
faster; 8 bytes smaller, the same memory. The other nine unchanged: c7c35f9c97, ee34931cd7, 06b188f45b, c6f1c1331b,
782f3ad7ff, 3eb59b271d, c2ef9488ff, fb0d57c8a2, 64a7345393 - the knee's c2ef9488ff with its challenger 11a56ff9e4
re-measured in seed 90's follow-up (results/followup-seed90.md).
