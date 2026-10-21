# The pending batch - one patch, proposed for before seed 64 (Iteration 441)

Found at seed 63's processing (results/evolve-amd-ryzen-7-pro-8840hs-seed63.md). **The owner's call: applied now, before
seed 64 starts - recommended, or at seed 64's processing.** Without it a free run with no evolved founders has no
working JIT, as seed 63 had none - its fast end -55% against seeds 59-62.

| # | patch | what it does |
|---|---|---|
| 1 | jitfix-after-seed63.patch | Two JIT faults. **The founder**: the hand-made founder carrying the JIT (s6-cv8b with jit, jitx, jitloop, jitinl, Iteration 155) gets tag2 - the JIT needs the two-bit tag (jit_on), and without it the founder's JIT never expressed; seeds 59-62 required the tag and seed 58 had evolved founders, so it showed first in seed 63. **jit_ends** (engine/jit.c) moves out of jitx's block: jitre (Iteration 346) calls it without jitx - three of seed 63's designs did not compile (jit.c:598, `jit_ends` undeclared). |

    git apply results/pending/jitfix-after-seed63.patch

## How it was tested

In a clone of master after the after-seed-63 batch (6f4e631), its stages built: the three designs that failed to compile
in seed 63 (11326e5c19, aa67bd896b, 8de6dc5781 - jitre without jitx) build and live; the founder with the tag expresses
the JIT, jitx, jitloop and jitinl, builds and lives. The JIT itself is not slower after the batch: seed 62's fastest JIT
designs measure 0.163 and 0.153 on seed 62's code and 0.153 and 0.155 on today's, here.
