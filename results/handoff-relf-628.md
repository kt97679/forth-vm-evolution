# The relf handoff after seed 89's follow-up - three roles change (Iteration 628)

results/handoff-relf-611.md stands - the roles, how to build, run and check a design, what relf takes - with three of
its ten designs replaced by seed 89's (the owner, 628; the evidence: results/followup-roles-seed89.md). The ten, by role:
results/relf-designs-628.md; the package: forth-vm-evolution-designs-iter628.tar.gz (lab/evolve/pack-designs.py on it,
each design at both widths - 20 of 20 builds 9 of 9 right against s6); `make` builds them from designs/
(export-designs.py: fastest-x86-32, portable-arm and small-jit made again).

| role | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | bytes, 4-byte | memory KB | JIT | checks (8 / 4) |
|---|---|---|---|---|---|---|---|---|---|
| fastest on x86-32 | ee34931cd7 (was 4ef851fd8e) | 0.189 | 0.193 | 0.476 | 41,990 | 40,162 | 224 | x86-64 and x86-32 | 9/9 / 9/9 |
| smallest of the JIT designs | c6f1c1331b (was bac37f35a2) | 0.225 | 0.235 | 0.577 | 29,306 | 28,930 | 208 | x86-64 and x86-32 | 9/9 / 9/9 |
| fastest on ARMv7 | 3eb59b271d (was 690981ca5b) | 0.378 | 0.443 | 0.320 | 22,522 | 23,246 | 132 | no - portable | 9/9 / 9/9 |

Speeds as 611's table: the classes of final-pick.py step 5, re-measured in seed 89's follow-up (lower is faster; a JIT
design's ARMv7 its JIT-off build). Against the holders they replace, in the same sessions: ee34931cd7 -3.15% +/- 0.42%
on x86-32 (5.6% larger); c6f1c1331b 2.71% smaller, x86-64 -2.30%, x86-32 -1.53%; 3eb59b271d -2.84% +/- 0.62% on
ARMv7, 2.77% smaller, 4 KB less memory. The other seven unchanged: c7c35f9c97, 06b188f45b, 782f3ad7ff, c2ef9488ff,
a627b954c6 (its challenger 8164d3858f re-measured on the Tegra during seed 90), fb0d57c8a2, 64a7345393.
