# The after-seed-67 batch - apply in this order (at seed 67's processing)

The owner (454-455): "yes, lets remove" - the gene rule's last step for the first freeze, which showed no loss in seed
66 (against seed 65 at their common generation: fastest 0.1286 against 0.1288, smallest +0.1%). After seed 67, so seed 67
is not mixed with it.

| # | patch | what it does |
|---|---|---|
| 1 | retire-after-seed67.patch | **tail, tailpn and kstack retired**: their code removed - tools/gen-tail.py, build_tail() and tail_offenders() (lab/evolve/evolve.py), the preserve_none compiler choice, the engines-check paths that built tail engines (89 paths to 69), forth/kstack.4 and its dump variants. The genes stay in the genome, frozen off (FROZEN), so every design keeps its identity; lab/evolve/GENES.md marks them retired. **sharedcall's path stays**: CV8's base genome sets it, so the hand-made s5 and s6 - the reference - use it; only its gene is retired (frozen off since 450). |

    git apply results/applied-after-seed67/retire-after-seed67.patch

## How it was tested

In a clone of master (e1285e3), its stages built: run-tests PASS (engines-check: 69 paths, each built and its corpus
right), validate 7 of 7 IDENTICAL, a short evolution (16 designs, 3 generations) - 78 of 78 alive. **batch-check on
c69752e: run-tests PASS, validate 7 of 7 IDENTICAL, jail PASS.**
