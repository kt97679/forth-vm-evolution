# The dream 32-bit experiment, read (Iteration 614): the compiler

Seed 88's chain (results/chain-seed88: the laptop one session of 20 rounds, dream 30 sessions a width, the Tegra 12) on
results/candidates-dream32-612.md. **The compiler is the cause**: built with clang, 9f8811f7f4's dream/laptop ratio at
4-byte cells falls 2.130 -> 1.167 and 690981ca5b's 1.824 -> 1.166, the control 782f3ad7ff 1.105 (the bar 1.271) - dream
37.6% and 24.6% faster, the laptop 13.9% and 18.0% slower at 32 bits (18.9% and 9.7% at 64): the laptop prefers GCC and
dream clang, so a search selected on the laptop keeps GCC at 32 bits. No other gene reverted on both bases restores
either (regpin, rtimm, nogcse, gotodup, lto, noinls: -6% to +4% on the ratio). Alignment moves dream too: 9f8811f7f4's
alignhot=0 or align1=1 each 9.9% faster on dream, 17-18% slower on the laptop; lto=0 and noinls=0 lower 690981ca5b's
ratio only by slowing the laptop (dream unchanged) - the ratio alone misleads there. At 8-byte cells dream moves 2-3%,
the Tegra 1-3%. Dream paired by session: +/- 0.1%; the laptop one session, no error.
Across both chains (results/drafts/gcc-clang-614.py): GCC's 32-bit penalty on dream is general, not one lineage's -
seed 87's follow-up's 18 GCC designs 1.10-2.09 (median 1.57), its 27 clang ones 1.06-1.47 (1.13). Dream is an Intel
i7-6700 (Skylake) running the laptop's own builds, the same bytes: a front-end effect is the candidate (Skylake's
jump-alignment erratum - a jump crossing or ending on a 32-byte boundary leaves the decoded-instruction cache), with the
alignment genes' effect. Not tested; a count of the engines' dispatch jumps on such boundaries would test it here.

- dream.lan-prebuilt32 (x32): 30 session(s); 20 of 20 designs measured
- dream.lan-prebuilt64 (x64): 30 session(s); 20 of 20 designs measured
- laptop32 (laptop): 1 session(s); 20 of 20 designs measured
- laptop64 (laptop): 1 session(s); 20 of 20 designs measured
- rage.lan-prebuiltarm (arm): 12 session(s); 20 of 20 designs measured

| design | what | dream.lan-prebuilt32 | dream.lan-prebuilt64 | laptop32 | laptop64 | rage.lan-prebuiltarm | dream.lan-prebuilt32 / laptop | dream.lan-prebuilt64 / laptop | rage.lan-prebuiltarm / laptop |
|---|---|---|---|---|---|---||---|---|---||
| 9f8811f7f4 | a base | 0.6546 | 0.4239 | 0.3073 | 0.2998 | 0.3344 | 2.130 | 1.414 | 1.088 |
| 690981ca5b | a base | 0.6138 | 0.4680 | 0.3365 | 0.3664 | 0.3286 | 1.824 | 1.277 | 0.977 |
| 782f3ad7ff | the control | 0.3508 | 0.3833 | 0.3173 | 0.2983 | 0.3713 | 1.105 | 1.285 | 1.170 |
| f8b8fed677 | 9f8811f7f4 with regpin=0 | 0.6568 | 0.4275 | 0.2968 | 0.2955 | 0.3335 | 2.213 | 1.446 | 1.124 |
| 1d73264c94 | 9f8811f7f4 with rtimm=0 | 0.6653 | 0.4325 | 0.3129 | 0.3148 | 0.3399 | 2.126 | 1.374 | 1.086 |
| 49859ccf95 | 9f8811f7f4 with nogcse=0 | 0.6327 | 0.4227 | 0.3160 | 0.3021 | 0.3434 | 2.002 | 1.399 | 1.087 |
| 2ac7d6b132 | 9f8811f7f4 with alignhot=0 | 0.5895 | 0.4341 | 0.3582 | 0.3447 | 0.3334 | 1.645 | 1.260 | 0.931 |
| 969d4ff708 | 9f8811f7f4 with align1=1 | 0.5897 | 0.4308 | 0.3629 | 0.3373 | 0.3344 | 1.625 | 1.277 | 0.921 |
| 3965a85446 | 9f8811f7f4 with noreorder=0 | 0.6543 | 0.4236 | 0.3048 | 0.2970 | 0.3376 | 2.147 | 1.426 | 1.107 |
| b0042fce56 | 9f8811f7f4 with gotodup=0 | 0.6554 | 0.4243 | 0.3130 | 0.3066 | 0.3345 | 2.094 | 1.384 | 1.069 |
| 22aa39921b | 9f8811f7f4 with lto=0 | 0.6501 | 0.4341 | 0.3055 | 0.2998 | 0.3306 | 2.128 | 1.448 | 1.082 |
| 6835b2e3d5 | 9f8811f7f4 with noinls=0 | 0.6489 | 0.4225 | 0.3036 | 0.3000 | 0.3290 | 2.138 | 1.408 | 1.084 |
| 0701dd4670 | 9f8811f7f4 with compiler=1 | 0.4085 | 0.4355 | 0.3501 | 0.3563 | 0.3318 | 1.167 | 1.222 | 0.948 |
| 64c534c502 | 690981ca5b with regpin=0 | 0.6141 | 0.4688 | 0.3308 | 0.3778 | 0.3292 | 1.856 | 1.241 | 0.995 |
| 5b415caff7 | 690981ca5b with rtimm=0 | 0.6216 | 0.4727 | 0.3306 | 0.3702 | 0.3317 | 1.880 | 1.277 | 1.003 |
| 04ab053102 | 690981ca5b with nogcse=0 | 0.6052 | 0.4621 | 0.3346 | 0.3790 | 0.3461 | 1.809 | 1.219 | 1.034 |
| 41afedb8d0 | 690981ca5b with gotodup=0 | 0.6127 | 0.4683 | 0.3347 | 0.3644 | 0.3299 | 1.830 | 1.285 | 0.986 |
| 8e8d3b5f88 | 690981ca5b with lto=0 | 0.6159 | 0.4705 | 0.3774 | 0.3665 | 0.3313 | 1.632 | 1.284 | 0.878 |
| a91930f793 | 690981ca5b with noinls=0 | 0.6215 | 0.4662 | 0.3915 | 0.3764 | 0.3323 | 1.588 | 1.239 | 0.849 |
| 8d0543a069 | 690981ca5b with compiler=1 | 0.4628 | 0.4794 | 0.3970 | 0.4018 | 0.3388 | 1.166 | 1.193 | 0.853 |

dream.lan-prebuilt32 / laptop at 4 bytes: the control 782f3ad7ff 1.105 - a variant RESTORES at 1.271 or below.

| variant | dream.lan-prebuilt32 / laptop: base -> variant | change (dream.lan-prebuilt32 paired SE) | dream.lan-prebuilt32 speed | dream.lan-prebuilt64 speed | laptop32 speed | laptop64 speed | rage.lan-prebuiltarm speed |
|---|---|---|---|---|---|---|---|
| 9f8811f7f4 regpin=0 | 2.130 -> 2.213 | +3.9% (dream.lan-prebuilt32 +/- 0.1%) | +0.3% | +0.8% | -3.4% | -1.4% | -0.3% |
| 9f8811f7f4 rtimm=0 | 2.130 -> 2.126 | -0.2% (dream.lan-prebuilt32 +/- 0.1%) | +1.6% | +2.0% | +1.8% | +5.0% | +1.6% |
| 9f8811f7f4 nogcse=0 | 2.130 -> 2.002 | -6.0% (dream.lan-prebuilt32 +/- 0.1%) | -3.3% | -0.3% | +2.8% | +0.8% | +2.7% |
| 9f8811f7f4 alignhot=0 | 2.130 -> 1.645 | -22.7% (dream.lan-prebuilt32 +/- 0.1%) | -9.9% | +2.4% | +16.6% | +15.0% | -0.3% |
| 9f8811f7f4 align1=1 | 2.130 -> 1.625 | -23.7% (dream.lan-prebuilt32 +/- 0.1%) | -9.9% | +1.6% | +18.1% | +12.5% | -0.0% |
| 9f8811f7f4 noreorder=0 | 2.130 -> 2.147 | +0.8% (dream.lan-prebuilt32 +/- 0.2%) | -0.0% | -0.1% | -0.8% | -1.0% | +0.9% |
| 9f8811f7f4 gotodup=0 | 2.130 -> 2.094 | -1.7% (dream.lan-prebuilt32 +/- 0.1%) | +0.1% | +0.1% | +1.8% | +2.3% | +0.0% |
| 9f8811f7f4 lto=0 | 2.130 -> 2.128 | -0.1% (dream.lan-prebuilt32 +/- 0.1%) | -0.7% | +2.4% | -0.6% | -0.0% | -1.1% |
| 9f8811f7f4 noinls=0 | 2.130 -> 2.138 | +0.4% (dream.lan-prebuilt32 +/- 0.1%) | -0.9% | -0.3% | -1.2% | +0.1% | -1.6% |
| 9f8811f7f4 compiler=1 | 2.130 -> 1.167 RESTORES | -45.2% (dream.lan-prebuilt32 +/- 0.1%) | -37.6% | +2.7% | +13.9% | +18.9% | -0.8% |
| 690981ca5b regpin=0 | 1.824 -> 1.856 | +1.8% (dream.lan-prebuilt32 +/- 0.1%) | +0.0% | +0.2% | -1.7% | +3.1% | +0.2% |
| 690981ca5b rtimm=0 | 1.824 -> 1.880 | +3.1% (dream.lan-prebuilt32 +/- 0.1%) | +1.3% | +1.0% | -1.7% | +1.0% | +1.0% |
| 690981ca5b nogcse=0 | 1.824 -> 1.809 | -0.9% (dream.lan-prebuilt32 +/- 0.1%) | -1.4% | -1.2% | -0.5% | +3.4% | +5.3% |
| 690981ca5b gotodup=0 | 1.824 -> 1.830 | +0.3% (dream.lan-prebuilt32 +/- 0.1%) | -0.2% | +0.1% | -0.5% | -0.5% | +0.4% |
| 690981ca5b lto=0 | 1.824 -> 1.632 | -10.5% (dream.lan-prebuilt32 +/- 0.1%) | +0.3% | +0.5% | +12.2% | +0.0% | +0.8% |
| 690981ca5b noinls=0 | 1.824 -> 1.588 | -13.0% (dream.lan-prebuilt32 +/- 0.1%) | +1.3% | -0.4% | +16.3% | +2.7% | +1.1% |
| 690981ca5b compiler=1 | 1.824 -> 1.166 RESTORES | -36.1% (dream.lan-prebuilt32 +/- 0.1%) | -24.6% | +2.4% | +18.0% | +9.7% | +3.1% |

(3) the clang build restores both bases: RIGHT
(4) one other gene, reverted on both, restores both: WRONG - none of gotodup=0, lto=0, nogcse=0, noinls=0, regpin=0, rtimm=0

## GCC and clang across both chains (results/drafts/gcc-clang-614.py)

```
follow-up 87 GCC: 18 designs, dream/laptop at 4 bytes 1.10-2.09 (median 1.57); at 8 bytes median 1.28
follow-up 87 clang: 27 designs, dream/laptop at 4 bytes 1.06-1.47 (median 1.13); at 8 bytes median 1.21
seed 88 chain GCC: 17 designs, dream/laptop at 4 bytes 1.59-2.21 (median 1.88); at 8 bytes median 1.28
seed 88 chain clang: 3 designs, dream/laptop at 4 bytes 1.11-1.17 (median 1.17); at 8 bytes median 1.22
```
