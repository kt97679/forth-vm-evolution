# The new roles' shortlist - chain B processed: seven roles settle or lead clearly, three wait for chain C (Iteration 714)

Chain B (results/drafts/new-roles-plan-705.md, step 3; the archive
forth-vm-evolution-chain-eccab9505-fury-20261121-142903.tar.gz, at eccab9505 - master with the after-seed-96 batch): the 99
of results/followup-seed96-roles-b.md at 10 rounds - measure-ids.py first (the lean 14 five times), pool-sizes.py, then
loadtest.py alone and loaded at both widths; dream the 99 at both widths, the Tegra the 61 of the -arm list. Processed by
`HANDOFF=results/handoff-relf-657.md PRED=713 sh lab/evolve/process-followup.sh 96-roles-b 714 ROLES` (ROLES as at 713:
fastest=782f3ad7ff,arm=3eb59b271d,knee=11a56ff9e4,smallarm=ae99617f06,memory=fb0d57c8a2,smallest=d180351903,
fast64=c7c35f9c97,fast32=ee34931cd7,allround=06b188f45b,smalljit=c6f1c1331b). The readings by session:
results/chain-followup96-roles-b (pool-sizes.md beside them); the pooled pick: results/followup-pick-seed96-roles-b.md
(.json); beyond followup-roles.py - each role's near-ties, the smallest's contenders, the stalls, the ticker:
results/drafts/chainB-714.py.

## The chain

- **The laptop: 18 whole sessions** (57 minutes each, 21:11-14:28 UTC; repeat-fits.sh skipped the last 6 of 24, 29
  minutes past the remote deadline), after the five measure-ids packs and pool-sizes.py (33 minutes). The ticker (new in
  chain B): the load 2.9-4.5 on average in every session but the sixth (02:05-02:55: one tick at 21.7, free memory 4.5 ->
  13.2 GB - another job on the laptop ending); 82-96 C, on AC, the 4 GB swap full throughout. Its readings pass the stall
  test below. **No PMU counts** - kernel.perf_event_paranoid was not set to 2, so loadtest.py's lines carry no "cnt" and
  countfit.py has nothing to fit.
- **dream: 34 sessions a width** (895-904 s each), **the Tegra: 5** (11,106-11,135 s); every listed design measured in
  every session on every line; none died (xcheck 105 of 105 and 65 of 65 each session). Load: dream 1.3-2.2, the Tegra
  1.4-1.5.
- **Noise** (a design's session-to-session SD, the median; a paired difference's SE): the laptop 0.94 % / 0.27 % at
  8-byte cells, 1.26 % / 0.39 % at 4; dream 0.48 % / 0.12 % and 0.59 % / 0.14 %; the Tegra 0.59 % / 0.38 %. Ten rounds and
  more sessions cut chain A's SE 2-7 times.
- **Stalls** (a reading more than 10 % off its design's median after its session's common shift): 1 of 1,782 at 8-byte
  cells and 3 at 4 on the laptop (session 3), 2 of 3,366 on dream at 4 (the worst 1.143), none elsewhere.
- **Memory reads 4 KB higher than chain A's** at the lean end on the laptop: fb0d57c8a2 108 -> 112 KB (five reads 112-116),
  each of the lean 14 112-120 KB - a common shift, so the 8 KB rule's comparisons stand; its cause not measured here.

## The roles (followup-roles.py's rule: speed 2 % at 2 SE, binary + image + code 1 %, memory 8 KB)

| role | holder | chain B's leader | against the holder | settled? |
|---|---|---|---|---|
| fastest portable (the best mean) | 782f3ad7ff 0.3457 | d727605472 0.3199 | -7.46 % +/- 0.10 % (x86-64 -4.91 %, x86-32 -10.73 %, ARMv7 -6.63 %) | led, not settled: 5f7e66b12d +0.24 % +/- 0.16 % on the mean, 34,056 B against 35,539 (-4.2 %), x86-32 +2.6 %, +4 KB - both to chain C |
| fastest on ARMv7 | 3eb59b271d | a8d35bdccc 0.3023 | -2.63 % +/- 0.39 % | settled (the next, a2fdd505b0, -1.64 %) |
| the knee | 11a56ff9e4 | 48a012411a | bytes -1.38 % (26,957 B against 27,334), x86-64 +0.76 %, x86-32 +0.45 %, memory +0 | settled by the rule |
| small, fast on ARMv7 | ae99617f06 | none by the rule | - | chain C: e51c01ba10, 4acee9a48e |
| least memory | fb0d57c8a2 112 KB | three more at 112 KB | 71005d8a0d and 16560cb51f x86 -23 %, ARMv7 +7 %; 2c841d55e3 23,647 B, x86 -4 % / -19 %, ARMv7 +6 % - trades | the holder kept (the 8 KB rule; every contender gives up ARMv7) |
| smallest | d180351903 22,107 B | 219878ec89 21,673 B | -1.96 %; x86-64 -18.65 %, x86-32 -28.08 %, ARMv7 -28.08 %, -4 KB | not settled: the four at 21,679 B (+6 B) 11.2-11.3 % faster than 219878ec89 on x86-64, 1.7-2.2 % on x86-32, ARMv7 the same; 23 designs 3-7 B smaller never timed - chain C |
| fastest on x86-64 | c7c35f9c97 0.1806 | 9b15ba26f7 0.1614 | -10.65 % +/- 0.54 % | settled: 262a51bc6c (+0.31 % +/- 0.40 %) and df097ba2e2 (+0.55 % +/- 0.33 %) not separated, both larger (54,551 and 54,695 B against 53,503) and using more memory (292 and 288 KB against 284) |
| fastest on x86-32 | ee34931cd7 0.1930 | ea782c6094 0.1824 | -5.49 % +/- 0.26 % | led, not settled: five within 2 SE (+0.15 % to +0.64 %), 11f956db93 among them 3.8 % smaller (49,925 B) and 16 KB leaner (260 KB) - to chain C |
| best all-round | 06b188f45b | df097ba2e2 0.2359 | -7.53 % +/- 0.23 % | settled (2236e26656 -6.59 %, separated) |
| the smallest JIT design | c6f1c1331b 36,805 B | trades only | 5ff17f9000 35,720 B (-2.95 %) at x86-64 +8.3 %, 4ba25fac6c / a6e8c448f0 35,830 B at +7.2-7.3 %; 1f7a2646cd 32,044 B at +71 % | chain C: the JIT middle (13a2b38e1b and 3; seed 96's database's) |

The owner (714): "our goal is not to lose any potentially good designs" - so a tie keeps both: the fastest portable's
two and the x86-32 five go to chain C together, the leader by the mean the role's provisional holder. Two answers
assumed (the owner did not choose): the x86-32 tie the same way, broken after chain C by size if still within 2 SE; the
least memory the rule's (the holder), its trades kept in chain C's list.

## pool-sizes.py (chain B's, 40 minutes on the laptop)

Every database's small end built at eccab9505, smallest first: JIT-free 1,315 of 9,678 (up to 22,447 B before the batch,
past the 22,419 B a design needs to land below 21,673 after the batch's largest cut, -746 - so the small end is covered),
JIT 120 of 120 up to 34,286 B; 0 failed. **23 JIT-free designs below 219878ec89**: 4 at 21,666 B and 19 at 21,670 B (in-run
1.17-1.25 against its 1.18), none on the list and never timed; no JIT design below 32,044 B. They go to chain C.
ARMv7 pre-flight (tools/arm-cross-check.py, qemu-arm): chain C's 27 new clang JIT-free designs - the 23 and four of the
five candidates - 27 built, alive and identical on fib and apps (engines 6,080-10,276 bytes); 4acee9a48e is GCC's, built
by the Tegra.

## Predictions (results/predictions.md, Iteration 713) - 7 of 8 scored right; (7) not scored

(1) right - the laptop 18, dream 34 a width, the Tegra 5, none failed. (1b) wrong - 23 JIT-free designs below 21,673 B
(3-7 B); none JIT. (2) right - each of the four at 21,679 B beats d180351903 (-1.94 %; 27.7-29.7 % faster in every class).
(3) right - d727605472 -7.46 % +/- 0.10 %. (4) right - a8d35bdccc -2.63 % +/- 0.39 %. (5) right - none below fb0d57c8a2's
112 KB. (6) right - -10.65 %, -5.49 %, -7.53 %. (7) not scored - no counts recorded. (8) right - none died. 7 of 8.

## Chain C - NEXT-RUN and REMOTES (the owner: 6 hours)

results/followup-seed96-roles-c.md - 66 (results/drafts/chainC-list-714.py): the 23, chainC-candidates-713.md's 9, and
from chain B's list the ten holders, each speed role's leader with every design it does not separate from at 2 SE, the
smallest's four at 21,679 B and 219878ec89, the knee's 48a012411a, the least memory's three trades, the smallest JIT
design's three nearest trades; -c-arm 34 (the JIT-free designs a size or ARMv7 question needs). The laptop: measure-ids.py,
`pool-sizes.py --list LIST --free 0 --jit 39100 --below-jit 36805 --minutes 40` (seed 96's database's JIT middle), then
loadtest.py at 10 rounds (about 38 minutes a session: ~8). The Tegra 3 sessions in 350 minutes; dream 16 a width, 175 +
175. Its processing: `HANDOFF=results/handoff-relf-657.md PRED=714 sh lab/evolve/process-followup.sh 96-roles-c ITERATION
ROLES` (ROLES as above - the holders are in the list), then results/drafts/chainB-714.py on chain C's readings; a design
measured in both chains compared in its chain's terms against the anchors both carry; then the roles, the owner's trades.
