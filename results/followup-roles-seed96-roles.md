# The new roles' screen - chain A processed: seven of the ten holders beaten by the rule on the screen; chain B, 76 designs (Iteration 713)

Chain A (results/drafts/new-roles-plan-705.md; the archive forth-vm-evolution-chain-517d6310-fury-20261120-150552.tar.gz,
at 517d6310): the ten holders measured on the laptop first (measure-ids.py), then the 944 of results/followup-seed96-roles.md
alone and loaded at both widths, 3 rounds a session; dream the 944 at both widths, the Tegra the 437 of the -arm list.
Processed by `HANDOFF=results/handoff-relf-657.md sh lab/evolve/process-followup.sh 96-roles 713 ROLES` (the ten roles,
the plan's step 1: ROLES = fastest=782f3ad7ff,arm=3eb59b271d,knee=11a56ff9e4,smallarm=ae99617f06,memory=fb0d57c8a2,
smallest=d180351903,fast64=c7c35f9c97,fast32=ee34931cd7,allround=06b188f45b,smalljit=c6f1c1331b; followup-roles.py again
with --predictions 705 after the fix below), the holders' records first replaced by the measure-ids pack's (results/drafts/holders-laptop-713.py:
the binary, image and programs' code the same bytes; the laptop's memory 4-16 KB below the sandbox's). The readings by
session: results/chain-followup96-roles; the pooled pick: results/followup-pick-seed96-roles.md (.json).

## The chain

- **The laptop: 5 whole sessions** (3.4-3.5 hours each, 20:07-13:25 UTC); a sixth, started at 13:25 because repeat-fits.sh
  said it would end 9 minutes inside the remote lines' deadline, was ended by hand at 15:05 UTC, about 100 of its ~207
  minutes in - its readings not packed (ended.txt). The steps file's "skipped" line names the fourth session's start
  (06:30:53) - wrong: sessions 4 and 5 are in the archive, whole. At the end the laptop had 480 MB free (5.6 GB available) and its 4 GB
  of swap full (ended.txt); chain A had no ticker (the batch's ticker patch gives chain B one), so earlier sessions' load is
  unknown - the noise below shows no session apart (the shift's range 0.8-1.4 %; the loaded line drifts +1.05 % from the
  first third to the last).
- **dream: 8 sessions a width; the Tegra: 3** - every listed design built and measured on every line (944 a
  session, the Tegra 437); none died anywhere. Load: dream's 8-byte session 6 averaged 2.2 (its others 1.4-1.8), the Tegra 1.4.
- **Noise** (a design's session-to-session SD, the median; a paired difference's SE over the sessions): the laptop 0.98 %
  / 0.56 % at 8-byte cells, 1.33 % / 0.81 % at 4; loaded 1.24 % / 0.72 % and 1.41 % / 0.87 %; dream 1.76-1.80 % / 0.89-0.90 %;
  the Tegra 1.12 % / 0.91 %. Rank agreement with the laptop alone (Spearman): dream 0.85 (8-byte) and 0.92 (4-byte), the
  Tegra 0.58-0.61.
- **The fast end's optimism**: the in-run fastest tenth (94, holders out) re-measured alone on the laptop / in-run, the
  median 1.113 at 8-byte cells (quartiles 1.104-1.122), 1.074 at 4 - seed 96's in-run curse was 1.056
  (results/drafts/chainA-713.py).

## Found and fixed - the portable roles took JIT designs

followup-roles.py takes a design for JIT from its record's "jit" mark (622: portable-followup.py --jit writes it);
new-roles-705.py's list carries none, so process-followup.sh's first pass took the six portable roles over all 944 - the
fastest portable came out 923951e8ab, a JIT design, and "the smallest JIT design" found none smaller than c6f1c1331b. Now,
without a mark, followup-roles.py expresses the genome (the screen's test, 630): 526 of the 944 are JIT designs. The
roles below are the second pass. Checked: results/drafts/followup-rehearsal-615.sh's roles output the same before and
after the fix, byte for byte; both follow-up rehearsals FAIL at 3a04c66 already - 615's roles on 708's memory rule (its
heading 8 KB, 611's 4), jit-rehearsal-622.py's (5) portable-followup.py --jit 0 records - stale, not this change; left.

## The after-seed-96 batch, applied (7081f96) - and the sizes it moves

Before chain B's lists, on master: batch-check PASS (8 patches on 3a04c66 - run-tests PASS, validate 7 of 7 IDENTICAL,
the jail PASS); results/applied-after-seed96/. Chain A's readings are from before it. The sizes at master, every design
the size roles and the shortlist touch (206, results/drafts/sizes-713.py -> results/drafts/sizes-713.json, 8-byte cells):
only the engines change - JIT-free clang -676 to -936 bytes, GCC -482 to -650; JIT designs with jitx -1,784 to -2,224
(clang) and -1,608 (GCC; wends16), the rest -488 to -760; every image and the programs' code unchanged. The small end's
order stands (the 40 smallest JIT-free designs the same 40 before and after, each -730 to -746; the holder
d180351903 -730, 38th both times); the smallest JIT designs move
past one another (the jitx ones lose the table).

## The roles - the screen (followup-roles.py's rule: speed 2 %, binary + image + code 1 %, memory 8 KB)

| role | holder | the screen's leader | against the holder |
|---|---|---|---|
| fastest portable (the best mean) | 782f3ad7ff 0.3471 | d7fb9683c2 0.3295 | -5.07 % +/- 0.33 % (x86-64 -8.2 %, x86-32 +4.1 %, ARMv7 -10.4 %) |
| fastest on ARMv7 | 3eb59b271d | a8d35bdccc 0.3055 | -3.37 % +/- 0.27 %; 60d1484673 -2.00 %, a2fdd505b0 -1.90 % |
| the knee | 11a56ff9e4 | 48a012411a | x86-64 +1.0 %, x86-32 -3.2 %, bytes -1.4 % (after the batch: 26,957 B against 27,334), memory +4 KB |
| small, fast on ARMv7 | ae99617f06 | none by the rule | - |
| least memory | fb0d57c8a2 108 KB | five more at 108 KB | a tie by the 8 KB rule; d3496fcc6c 25,201 B (holder 25,569) and 0.61 against 0.82 - the five reads decide |
| smallest | d180351903 22,107 B | six at 21,679 B (21768033b7 ...) | -1.94 % bytes after the batch; each 24.6-25.2 % faster on x86-64, 26.8-27.9 % on x86-32, 28.4-29.4 % on ARMv7 - trade-free |
| fastest on x86-64 | c7c35f9c97 | df097ba2e2 0.1639 | -10.9 % +/- 1.2 % (laptop and dream pooled); 9b15ba26f7 -10.6 % |
| fastest on x86-32 | ee34931cd7 | 2236e26656 0.1802 | -7.9 % +/- 0.8 % |
| best all-round | 06b188f45b | 923951e8ab 0.2446 | -5.9 % +/- 0.4 % |
| the smallest JIT design | c6f1c1331b 36,805 B | 1f7a2646cd 32,044 B (-12.9 %) | x86-64 +69 % - trades only: the nearest, 5ff17f9000 35,720 B (-2.9 %) at +7.2 %, 4ba25fac6c / a6e8c448f0 35,830 B at +5.6-6.7 % - the owner's call |

The roles are not chosen here: the plan's chain B measures the shortlist at 10 rounds on the three machines, and its
processing picks them - the owner's trades, as at 611 and 649. On the screen, seven of the ten holders are beaten by the
rule (the least memory tied at the floor, small and fast on ARMv7 kept, the smallest JIT design's contenders all trades); the smallest changes whichever of the six wins.
The smallest JIT design is a size role with no trade-free contender: the strict reading takes 1f7a2646cd (-4,761 B, 1.7x
the time), a 1 % rule none.

## Chain B - the shortlist (results/followup-seed96-roles-b.md: 76; -arm: 42; -lean: 13)

results/drafts/shortlist-713.py: final-pick.py's shortlist (--n 40: the set alone and loaded, the additions across machines,
each width's 5 fastest alone and loaded, then by hypervolume), the ten holders, and each role's leaders by the pooled
classes - the 5 best JIT-free means, the 5 fastest JIT-free on ARMv7, the 5 fastest on x86-64 and x86-32 and the 5 best
means over every design, the knee's and small-and-fast's contenders by the rule (sizes after the batch) and the pool's
knee bee5d0daa2, the 5 fastest JIT-free at 108 KB, the 5 best means within 0.1 % of the smallest after the batch, the 3
smallest JIT designs and those smaller than c6f1c1331b within 10 % of its x86-64. 35 JIT-free, 41 JIT. Each record carries
master's sizes (bin, total; before_batch the chain's). The -arm list: the JIT-free designs and the JIT designs leading
across machines with the all-round holder (their JIT-off builds). The -lean list: the 13 within 8 KB of 108 KB.

ARMv7 pre-flight (tools/arm-cross-check.py, qemu-arm, the batch applied): the -arm list's 21 clang JIT-free designs 21
built, alive and identical on fib and apps (engines 6,012-18,596 bytes); its GCC ones are built by the Tegra.

NEXT-RUN (the owner: 19 hours): measure-ids.py on the 76 (the laptop's size and memory beside the batch), measure-ids.py
on the lean 13 four times more (five reads of the memory), then loadtest.py at 10 rounds, about 56 minutes a session,
repeated while another ends by the remote lines' deadline (about 19). REMOTES: the Tegra the 42, 8 sessions in 1,110
minutes (about 2.2 hours each); dream the 76 at both widths, 40 sessions a width, 555 + 555 minutes. Its processing:
`process-followup.sh 96-roles-b` - the shortlist named so for it (its holders' and candidates'
records from the measure-ids pack, the lean end's memory the median of its five), then the roles.

**Found: the counts need the perf hold on the laptop.** The batch's counters patch (711) has cputime read four counts
and loadtest.py's lines carry them - but cputime opens them only at kernel.perf_event_paranoid 2 or below, the laptop's
is Ubuntu's 4 (seed 75's clock test), and next-run.sh takes the chain's perf hold for counters.py, missmap.py and
clockcheck.py only. So chain B carries counts only if the owner sets 2 by hand before the start (`sudo sysctl
kernel.perf_event_paranoid=2`, 4 after - Iteration 544's way); xcheck.py's remote lines record none in any case. The
timing is CPU time either way (EVOLVE_METRIC unset). The fix for later chains: loadtest.py taking the hold as
clockcheck.py does (counters.PerfHold, the time alone when refused) and next-run.sh asking for it - not built here.

## Predictions (Iteration 705) - 6 of 6

(1) right - the laptop 5, dream 8 a width, the Tegra 3; none failed. (2) right - 1.113. (3) right - 9b15ba26f7 -12.4 % +/-
1.4 % on the laptop alone at 8-byte cells (5 sessions). (4) right - 89988b4c1f, JIT-free, -8.1 % +/- 0.3 % against
782f3ad7ff there. (5) right - 108 KB. (6) right - none died.
