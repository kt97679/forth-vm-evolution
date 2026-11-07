# The jump-alignment test - dream's GCC slowdown at 32 bits (Iteration 623)

`python3 results/drafts/jcc-count-623.py` (seed 88's follow-up's 46) and `... results/candidates-dream32-612.md results/chain-seed88` (614's dream 32-bit experiment, its 20). Every engine built here as the laptop builds it - the 46's 8-byte engines all the laptop's size exactly (bin); the jumps from objdump of engine.full.

## Across the 46

| cells | compiler | designs | dispatch jumps a design | on a boundary | branch units on a boundary | dream/laptop (median) |
|---|---|---|---|---|---|---|
| 4-byte | GCC | 18 | 61.8 | 15.1% | 14.8% | 1.516 |
| 4-byte | clang | 28 | 89.2 | 14.6% | 14.1% | 1.163 |
| 4-byte | Spearman with dream/laptop | 46 | | dispatch +0.09 | branches +0.19 | |
| 4-byte | Spearman, the dispatch jumps' count with dream/laptop | all -0.41 | GCC +0.43 | clang -0.66 | | |
| 8-byte | GCC | 18 | 47.4 | 13.9% | 16.9% | 1.300 |
| 8-byte | clang | 28 | 87.5 | 34.1% | 13.6% | 1.212 |
| 8-byte | Spearman with dream/laptop | 46 | | dispatch +0.39 | branches +0.62 | |
| 8-byte | Spearman, the dispatch jumps' count with dream/laptop | all -0.72 | GCC -0.03 | clang -0.59 | | |

## Across 614's variants (4-byte cells; the 8-byte Spearman last)

| cells | compiler | designs | dispatch jumps a design | on a boundary | branch units on a boundary | dream/laptop (median) |
|---|---|---|---|---|---|---|
| 4-byte | GCC | 17 | 140.9 | 17.2% | 13.1% | 1.880 |
| 4-byte | clang | 3 | 146.0 | 8.1% | 14.2% | 1.166 |
| 4-byte | Spearman with dream/laptop | 20 | | dispatch +0.79 | branches -0.66 | |
| 4-byte | Spearman, the dispatch jumps' count with dream/laptop | all -0.43 | GCC -0.59 | clang -1.00 | | |
|   4 | 782f3ad7ff clang | | 156 | 6.4% | 10.9% | 1.105 |
|   4 | 8d0543a069 clang | | 147 | 6.1% | 17.1% | 1.166 |
|   4 | 0701dd4670 clang | | 135 | 11.9% | 14.5% | 1.167 |
|   4 | a91930f793 GCC | | 148 | 14.2% | 16.3% | 1.588 |
|   4 | 969d4ff708 GCC | | 136 | 19.1% | 16.8% | 1.625 |
|   4 | 8e8d3b5f88 GCC | | 148 | 16.2% | 16.1% | 1.632 |
|   4 | 2ac7d6b132 GCC | | 136 | 15.4% | 15.4% | 1.645 |
|   4 | 04ab053102 GCC | | 148 | 18.9% | 17.7% | 1.809 |
|   4 | 690981ca5b GCC | | 148 | 13.5% | 16.4% | 1.824 |
|   4 | 41afedb8d0 GCC | | 148 | 13.5% | 16.4% | 1.830 |
|   4 | 64c534c502 GCC | | 148 | 13.5% | 16.4% | 1.856 |
|   4 | 5b415caff7 GCC | | 148 | 13.5% | 16.4% | 1.880 |
|   4 | 49859ccf95 GCC | | 136 | 15.4% | 9.3% | 2.002 |
|   4 | b0042fce56 GCC | | 136 | 19.9% | 9.2% | 2.094 |
|   4 | 1d73264c94 GCC | | 136 | 19.9% | 9.2% | 2.126 |
|   4 | 22aa39921b GCC | | 136 | 19.9% | 9.6% | 2.128 |
|   4 | 9f8811f7f4 GCC | | 136 | 19.9% | 9.2% | 2.130 |
|   4 | 6835b2e3d5 GCC | | 136 | 20.6% | 9.6% | 2.138 |
|   4 | 3965a85446 GCC | | 136 | 19.9% | 9.2% | 2.147 |
|   4 | f8b8fed677 GCC | | 136 | 19.9% | 9.2% | 2.213 |
| 8-byte | Spearman with dream/laptop | 20 | | dispatch +0.80 | branches -0.37 | |
| 8-byte | Spearman, the dispatch jumps' count with dream/laptop | all -0.37 | GCC -0.66 | clang +0.50 | | |
|   8 | 8d0543a069 clang | | 146 | 5.5% | 13.7% | 1.193 |
|   8 | 04ab053102 GCC | | 147 | 19.7% | 19.0% | 1.219 |
|   8 | 0701dd4670 clang | | 134 | 6.7% | 13.4% | 1.222 |
|   8 | a91930f793 GCC | | 147 | 21.8% | 19.5% | 1.239 |
|   8 | 64c534c502 GCC | | 147 | 17.0% | 18.4% | 1.241 |
|   8 | 2ac7d6b132 GCC | | 135 | 21.5% | 19.5% | 1.260 |
|   8 | 969d4ff708 GCC | | 135 | 19.3% | 18.0% | 1.277 |
|   8 | 5b415caff7 GCC | | 147 | 21.8% | 18.6% | 1.277 |
|   8 | 690981ca5b GCC | | 147 | 21.8% | 18.6% | 1.277 |
|   8 | 8e8d3b5f88 GCC | | 147 | 19.0% | 19.6% | 1.284 |
|   8 | 41afedb8d0 GCC | | 147 | 21.8% | 18.6% | 1.285 |
|   8 | 782f3ad7ff clang | | 156 | 10.9% | 15.9% | 1.285 |
|   8 | 1d73264c94 GCC | | 135 | 24.4% | 16.6% | 1.374 |
|   8 | b0042fce56 GCC | | 135 | 24.4% | 16.6% | 1.384 |
|   8 | 49859ccf95 GCC | | 135 | 24.4% | 16.2% | 1.399 |
|   8 | 6835b2e3d5 GCC | | 135 | 24.4% | 17.1% | 1.408 |
|   8 | 9f8811f7f4 GCC | | 135 | 24.4% | 16.6% | 1.414 |
|   8 | 3965a85446 GCC | | 135 | 24.4% | 16.6% | 1.426 |
|   8 | f8b8fed677 GCC | | 135 | 23.7% | 13.2% | 1.446 |
|   8 | 22aa39921b GCC | | 135 | 24.4% | 16.5% | 1.448 |

## Intel's mitigation, built here - the two GCC bases at 4-byte cells (dispatch jumps and branch units on a boundary)

| build | 9f8811f7f4 | 690981ca5b |
|---|---|---|
| plain | 34,352 B; 27 of 136, 108 of 1,168 | 16,720 B; 20 of 148, 153 of 931 |
| -Wa,-mbranches-within-32B-boundaries | 34,480 B; 26 of 136, 59 of 1,169 | 17,456 B; 22 of 148, 52 of 931 |
| -Wa,-malign-branch=jcc+fused+jmp+indirect+call+ret (boundary 32) | 34,480 B (+0.4%); 0 of 136, 23 of 1,168 | 17,584 B (+5.2%); 0 of 148, 3 of 931 |

## The reading

- Across the 46 the static share on a boundary does not separate the compilers at 4-byte cells (GCC 15.1%, clang 14.6%;
  Spearman with dream/laptop +0.09): 614's compiler effect is no general property of GCC's layout. At 8-byte cells clang's
  dispatch jumps sit on boundaries more (34.1%) and run relatively better - a static count cannot weigh what runs hot.
- In 614's controlled variants the dispatch jumps' share ranks with dream's slowdown (Spearman +0.79): clang 6-12% at
  1.1-1.17, 690981ca5b's family 13.5% at 1.59-1.88, 9f8811f7f4's 19.9% at about 2.1 - and genes that only move code
  (align1, alignhot; in 690981ca5b's family noinls and lto) move dream's ratio 10-24%, design by design: a placement
  effect on dream's front end, the signature of Intel's JCC erratum on its Skylake (i7-6700).
- The standard mitigation misses an interpreter: -mbranches-within-32B-boundaries pads conditional and direct jumps, not
  indirect ones - every dispatch jump. With indirect jumps, calls and returns added, none is left on a boundary, at +128 B
  for 9f8811f7f4 and +864 B for 690981ca5b.
- Not confirmed - timing needs dream: the two bases' all-padded builds beside their plain ones on dream at 4-byte cells (a
  line of four); if the erratum is the cause their ratio falls toward clang's 1.1-1.2. Not a gene - an assembler flag the
  laptop's selection would only pay for in bytes (Zen 4 has no such erratum) - so an Intel build option, the owner's call.
  Either way, for 32-bit x86 on Intel: clang (614), or GCC with this padding.
