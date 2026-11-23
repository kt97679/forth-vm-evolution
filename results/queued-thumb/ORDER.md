# The thumb gene - queued until the series ends (Iteration 742)

The owner (742: "continue" - other sources for ideas; this one from embedded toolchains' size practice): the 32-bit ARM
engines are built A32 - clang's cross build by its default, and the Tegra's GCC 16 too (its engines' sizes: 16,782,
13,014 and 11,158 B at 726 are this sandbox's A32 builds' 16,862, 13,070, 11,186, not Thumb-2's 12,506, 9,754, 8,410) -
so every ARM design was measured in one instruction set, and Thumb-2 makes every ARM engine 25-31 % smaller
(results/drafts/thumb-742.txt). Its Tegra speed is unknown. The gene `thumb` (evolve.py, GENES.md) adds -mthumb to an ARM
build alone: x86 builds byte for byte the parent's, every recorded design's id the same (thumb=0 adds nothing), HELD -
never mutated or drawn. Queued, not applied: evolve.py changes, and seeds 98 on run on the method from seed 97.

Apply it when the series ends, with results/queued-layout2 (either order - other files), before the roles' follow-up:
`env PENDING=results/queued-thumb RECORD=1 sh tools/batch-check.sh`, then from the repository's top:

    git apply results/queued-thumb/thumb-gene-after-series.patch

batch-check (742, on Iteration 741 with this batch committed - 1 patch): PASS - run-tests PASS (the generators: 118 paths), validate 7 of 7
IDENTICAL, the jail PASS.

then `git mv results/queued-thumb/candidates-thumb-742.md results/candidates-thumb-742.md` (the remote lines find the
variants' genomes there; before the gene a master's canon() drops `thumb` and would build the parents under the
variants' ids), and `git mv results/queued-thumb results/applied-thumb-ITER`.

In the follow-up: the screen with `--also-arm results/candidates-thumb-742.md` (results/drafts/roles-screen-741.py - the
Tegra's list alone: on x86 the variants are their parents' twins); after the chain, `python3 results/drafts/thumb-pairs-742.py
results/chain-followupNN-... results/candidates-thumb-742.md` - each variant against its parent, paired by session, the
roles' 2 % rule. **[owner]** then: ship Thumb-2 (the six ARM roles' records become their thumb variants - new ids, the same
x86 bytes, the ARM engines 25-31 % smaller), or not.

Tested (742, results/drafts/thumb-742.txt): ids of 6,330 recorded designs the same with and without the gene; mutate()
4,000 times and random_genome() 2,000 times never set it; the six variants' x86 builds at both widths byte for byte their
parents'; the clang three's ARM builds Thumb-2 (4,440, 8,848, 12,728 B), alive and fib and apps the reference's under
qemu-arm (tools/arm-cross-check.py); the GCC three's with Ubuntu's cross GCC (Thumb-2 by default, so the variants
its parents' bytes; with -marm the parents A32, 25-26 % larger), alive and the reference's; the Tegra line's sample (xcheck.py --arm --bundle)
carrying the variants' Thumb-2 engines; export-arm.py's `make forth-arm` the lab's bytes for two variants.
