# The new roles' last chain - chain C processed: the smallest JIT design to 15eda54ebd, three choices for the owner (Iteration 716)

Chain C (results/drafts/new-roles-plan-705.md, step 3's last chain; the archive
forth-vm-evolution-chain-71fc8dd42-fury-20261121-203512.tar.gz, at 71fc8dd42): the 66 of results/followup-seed96-roles-c.md
at 10 rounds - measure-ids.py first, pool-sizes.py over seed 96's database's JIT designs, then loadtest.py alone and loaded
at both widths; dream the 66 at both widths, the Tegra the 34 of the -c-arm list. Processed by
`HANDOFF=results/handoff-relf-657.md PRED=714 sh lab/evolve/process-followup.sh 96-roles-c 716 ROLES` (ROLES chain B's
leaders: fastest=d727605472,smallarm=ae99617f06,smallest=219878ec89,fast64=9b15ba26f7,fast32=ea782c6094,smalljit=c6f1c1331b).
The readings by session: results/chain-followup96-roles-c (pool-sizes.md beside them, trimmed); the pooled pick:
results/followup-pick-seed96-roles-c.md (.json); beyond followup-roles.py: results/drafts/chainB-714.py on chain C's
readings (the near-ties, the smallest's contenders, the stalls, the ticker), results/drafts/chainC-716.py (the open pairs
in chain B, in chain C and pooled), results/drafts/jitmiddle-716.py (pool-sizes.py's JIT finds in in-run terms).

## The chain

- **The laptop: 6 whole sessions** (2,686-2,769 s each, 16:00-20:27 UTC; repeat-fits.sh skipped the last 4 of 10, the
  seventh 14 minutes past the remote deadline), after measure-ids.py and pool-sizes.py (15:02-15:54). The ticker: the load
  3.1-5.0 on average a session, 85-96 C, on AC, the 4 GB swap full. **No PMU counts** again (kernel.perf_event_paranoid
  not set to 2).
- **dream: 11 sessions a width** (871-928 s each), **the Tegra: 2** (9,425 and 9,215 s); every listed design measured in
  every session on every line; **none died** (xcheck 72 of 72 on dream, 38 of 38 on the Tegra, each session). Load: dream
  1.3-1.7 (2.5 in its 4-byte session 10), the Tegra 1.4-1.9.
- **Why fewer sessions than planned** (16 on dream, 3 on the Tegra, about 8 on the laptop): a session's length does not
  follow the list's - dream's took the same ~900 s with 66 designs as with chain B's 99; the Tegra's about 7,100-7,300 s
  plus 62-67 s a design (chain B 11,106-11,135 s for 61, chain C 9,215-9,425 s for 34); the laptop's about 1,300 s plus
  21 s a design (chain B 57 minutes for 99, chain C 45 for 66). The
  plan scaled chain B's sessions by the list (results/predictions.md, chain C's (1)).
- **Noise** (a design's session-to-session SD, the median; a paired difference's SE): the laptop 0.59 % / 0.24 % at
  8-byte cells, 0.63 % / 0.35 % at 4; dream 0.66 % / 0.27 % and 0.80 % / 0.34 %; the Tegra 0.36 % / 0.33 %.
- **Stalls**: none - no reading more than 10 % off its design's median after its session's common shift (2,312 readings;
  the worst 1.074, dream at 8-byte cells).

## The roles (followup-roles.py's rule: speed 2 % at 2 SE, binary + image + code 1 %, memory 8 KB)

Chain B settled five (results/followup-roles-seed96-roles-b.md): the fastest on ARMv7 a8d35bdccc, the knee 48a012411a, the
fastest on x86-64 9b15ba26f7, best all-round df097ba2e2, least memory the holder fb0d57c8a2. Chain C's readings agree
where they overlap (the x86-64 pair below). The other five:

| role | before chain C | chain C | verdict |
|---|---|---|---|
| small, fast on ARMv7 | ae99617f06 (holder) | e51c01ba10 +70 %, 4acee9a48e +38 % on ARMv7 | **settled: the holder kept** |
| the smallest JIT design | c6f1c1331b 36,805 B | three beat it by the rule: 15eda54ebd 36,344 B (-1.25 %; x86-64 -0.69 % +/- 0.50 %, x86-32 +0.27 % +/- 0.71 %, -4 KB), fa38596098 36,360 B (-1.21 %; -0.25 %, +0.27 %, +0 KB), 13a2b38e1b 36,408 B (-1.08 %; -1.56 %, -0.46 %, +4 KB); 08578f5e3d 36,030 B a trade (+12 KB, +1.6 %) | **settled: 15eda54ebd**, the smallest that beats it; 13a2b38e1b 64 B larger, -0.88 % +/- 0.15 % x86-64 and -0.73 % x86-32 against it, +8 KB |
| fastest portable (the best mean) | d727605472, tied with 5f7e66b12d | 5f7e66b12d +0.14 % +/- 0.30 %; chains B and C pooled +0.21 % +/- 0.14 % (1.5 SE) | **tied - the owner's**: 5f7e66b12d 4.2 % smaller (34,056 B against 35,539), the same 148 KB; x86-64 -1.45 %, x86-32 +2.68 %, ARMv7 -0.82 % (pooled) |
| fastest on x86-32 | ea782c6094, five within 2 SE | 69cebcaed9 leads by 0.15 %; ea782c6094, 11f956db93, 163935642a, b525180392 within 2 SE (pooled: +0.05 % to +0.64 %, each within 2 SE) | **tied - 714's assumption breaks it by size: 11f956db93** (49,925 B, 264 KB; against ea782c6094 -3.8 %, -16 KB); 163935642a smaller (49,105 B) but +40 KB against 11f956db93, x86-64 +5.2 % against ea782c6094 |
| smallest | 219878ec89 21,673 B | none of the 23 beats it - each 3-7 B smaller and 3.7-6.3 % slower in its slowest class | **the owner's trade** - below |

**The smallest - three designs within 13 bytes** (chain C; 90273721a1 against 219878ec89 pooled over chains B and C):

| design | bytes | memory | x86-64 | x86-32 | ARMv7 |
|---|---|---|---|---|---|
| 3456fc28b2 (the fewest bytes; the best of the four at 21,666) | 21,666 | 116 KB | 1.3171 | 1.3515 | 1.2814 |
| 219878ec89 (the rule's holder) | 21,673 | 116 KB | 1.4854 | 1.2806 | 1.2365 |
| 90273721a1 (the four at 21,679 B's fastest) | 21,679 | 116 KB | 1.3161 | 1.2576 | 1.2336 |

3456fc28b2 against 219878ec89: x86-64 -11.33 % +/- 0.22 %, x86-32 +5.54 % +/- 0.14 %, ARMv7 +3.63 % +/- 0.16 % - a trade.
90273721a1 against 219878ec89: x86-64 -11.32 % +/- 0.09 %, x86-32 -2.06 % +/- 0.13 %, ARMv7 -0.18 % +/- 0.11 % (pooled) -
faster in two classes, the same in the third, for 6 bytes. 90273721a1 against 3456fc28b2: x86-64 -0.07 % +/- 0.15 %, x86-32
-6.95 %, ARMv7 -3.73 % - for 13 bytes. The 19 at 21,670 B are 2.9-4.7 % slower than 219878ec89 in every class. So:
strict bytes is 3456fc28b2; the rule (1 % is 217 B) keeps 219878ec89; 90273721a1 is faster than both, 0.03-0.06 % larger.

**The fastest on x86-64 re-read**: 262a51bc6c against 9b15ba26f7 -1.52 % +/- 0.51 % in chain C (+0.31 % in chain B) -
the laptop's swing (+1.12 % +/- 0.79 % in B, -2.38 % +/- 1.00 % in C); dream -0.50 % and -0.64 % in both; pooled -0.38 %
+/- 0.31 %. Below the 2 % rule: 9b15ba26f7 stays (262a51bc6c 2.0 % larger).

## pool-sizes.py - seed 96's database's JIT middle (40 minutes on the laptop)

`--free 0 --jit 39100 --below-jit 36805`: 26,269 JIT designs up to 39,100 B before the batch; built smallest first, 1,054 in
the 40 minutes (up to 35,365 B before the batch, 32,044-34,714 B after), 0 failed, every one below c6f1c1331b's 36,805 B.
**In in-run terms none is within 20 % of c6f1c1331b at both widths** (results/drafts/jitmiddle-716.py: c6f1c1331b's
in-run reading its chain C laptop reading times the list's JIT designs' in-run / alone, the median 1.012 at both widths,
quartiles -4.1 % / +1.6 % at 8-byte cells): the best by the slower width 84dd23b61b (33,693 B, -8.5 %) at +33.8 % / +32.9 %;
the smallest five +64 % to +149 %. All trades. Not built: the band from 35,365 B before the batch to where a design lands
below 36,805 after it (the after-seed-96 batch took 456-1,832 B off these 1,054: up to about 38,600 B before it) -
unscreened, the 40 minutes spent below it; their in-run readings are in the database, so a screen by in-run speed
before building would cover it in minutes.

## Predictions (results/predictions.md, Iteration 714) - 4 of 8 right

(1) wrong - every line returned whole sessions and none failed, but the laptop 6, dream 11 a width, the Tegra 2 (the
session lengths above). (2) wrong - each of the 23 is 3.7-6.3 % slower than 219878ec89 in its slowest class. (3) wrong (the 35 %
side) - the four at 21,666 B within 0.07-1.2 % of 90273721a1 on x86-64. (4) right, the coin - +0.14 % +/- 0.30 %.
(5) right - e51c01ba10 and 4acee9a48e 70 % and 38 % slower on ARMv7. (6) right - 1,054. (7) wrong (the 30 % side) -
15eda54ebd, fa38596098 and 13a2b38e1b beat c6f1c1331b. (8) right - none died.

## Next - the roles (results/drafts/new-roles-plan-705.md, step 6)

The owner's answers first: the smallest (3456fc28b2, 219878ec89 or 90273721a1); the fastest portable's tie (d727605472
or 5f7e66b12d); the x86-32 tie by size (11f956db93) confirmed; whether the JIT band pool-sizes.py did not reach is
screened first. Then designs/ and the package made again (`sh results/drafts/freeze-build-645.sh . RECORDS NAME=ID,...`),
self-hosting phase 6 on them (the gate: a design the cross compiler cannot build ships translator-built, named - so far
d727605472 and 5f7e66b12d need the fused =I?BRANCH / DUP?NBRANCH), relf told how to fetch them.
