# Chain D processed - the smallest JIT design stays 15eda54ebd; three JIT roles ship translator-built by the gate; the rage check failed on its own fault (Iteration 725)

Chain D (Iterations 717-720; the archive d85635c9-forth-vm-evolution-chain-be190a273-fury-20261122-035840-done-some-failed.tar.gz,
at be190a273, 23:10-03:58 on the laptop): rage-designs.py, pool-sizes.py over every database's JIT designs below 35,980 B
(its best 30 written to the list), measure-ids.py on the list (58: the 23 of results/followup-seed96-jitband.md, the role's
5 anchors, the 30), selfhost-speed.py (the self-hosting gate's speed half, 720), then loadtest.py; dream the 28 fixed at
the chain's start at both widths. Processed by `HANDOFF=results/handoff-relf-657.md PRED=717 sh lab/evolve/process-followup.sh
96-jitband 725 smalljit=15eda54ebd`: the readings results/chain-followup96-jitband, the pick results/followup-pick-seed96-jitband.md
(.json), the list results/followup-seed96-jitband.md (the 30 appended by written-list.py, the 58 records the laptop's).
Beyond it: results/drafts/chainD-725.py (the role on the laptop alone, `--roles`; dream at 4-byte cells by compiler; the
gate's spread), results/selfhost-speed-725.md and results/rage-designs-725.md (the two steps' outputs as the pack had them).

## The chain

- **The laptop: 10 of 11 steps** - rage-designs.py FAILED (below), the rest done: pool-sizes.py 40 minutes, measure-ids.py
  58 of 58 alive (3 rounds), selfhost-speed.py 15 minutes, **7 loadtest sessions** (1,848-1,934 s each; repeat-fits ran
  all seven), 58 of 58 measured in each. The ticker during them: load 2.6-7.6 (mean 4.1 - loadtest's own load on three
  cores among it), on AC, the 4 GB swap full throughout.
- **dream: 10 sessions a width** (324-327 s at 4-byte cells, 266-274 s at 8), 28 of 28 every session (xcheck 34 of 34 with
  the 6 front designs it draws). The 8-byte .md lists 13 "asked for by id" - its xcheck.log and out.json measure all 28,
  and chain-sessions.py takes them (the completeness line: 28 of 28): the mark only. Load 1.2-1.8 at 4 bytes; at 8 bytes
  sessions 6, 7, 9 above 2.0 on average (4.0, 2.5, 2.2).
- **The PMU's counts, the first chain with them (719)**: every loadtest line carries "cnt" (58 a session);
  kernel.perf_event_paranoid 2 only while loadtest.py measured, 4 after each session and at the pack (perf.txt: 4).
  `python3 lab/evolve/countfit.py` on the 406 lines: the held-out error per (design, workload) median 4.1 % (instructions
  alone) and 3.8 % (with mispredictions and last-level misses), the worst 26-50 % (loop); the designs' speed Spearman 0.30
  and 0.44, median error 3.1 % and 2.8 % - **not a screen at the roles' 2 %** (711's question), here at least, where the 58
  lie within about 20 % of each other.
- No design died on any line.

## The smallest JIT design - 15eda54ebd stays

pool-sizes.py: 5,662 of 26,249 JIT records within the in-run ceilings (0.2116 / 0.2354) up to 39,100 B; 1,048 built in its
40 minutes (2,402 s; up to 37,653 B before the batch), none failed, **1,000 below 35,980 B**; the best 30 written.
**None of the 54 JIT designs smaller than 15eda54ebd beats it by the rule** (1 % smaller, no class 2 % slower, memory
within 8 KB). dream measured only the 28 named at the chain's start, so followup-roles.py's pooled classes left the 30 new
finds "no class in common"; on the laptop alone (`results/drafts/chainD-725.py --roles`: followup-roles.py itself, its
classes the laptop's) every one is at least 4 % slower on x86-64. The nearest:

| design | total | bytes | x86-64 (laptop) | x86-32 (laptop) | memory |
|---|---|---|---|---|---|
| 458fe81373 | 35,951 | -1.08 % | +4.18 % +/- 1.04 % | +4.17 % +/- 0.35 % | +52 KB |
| 893d4cb050 | 35,789 | -1.53 % | +5.87 % +/- 0.70 % | -0.49 % +/- 0.52 % | +8 KB |
| 456bd9c43e | 35,621 | -1.99 % | +6.14 % +/- 0.82 % | +1.88 % +/- 0.50 % | +16 KB |
| aba773be87 | 35,621 | -1.99 % | +6.51 % +/- 1.03 % | +1.28 % +/- 0.43 % | +20 KB |
| 08578f5e3d (chain C's) | 36,030 | -0.86 % | +3.97 % +/- 0.51 % | +0.07 % +/- 0.76 % | +16 KB |

The 28 dream measured, pooled as followup-roles.py pools them (results/followup-pick-seed96-jitband.md and process-followup's
roles block): the same verdict. In-run the list lay within 10 % of 15eda54ebd (the ceilings); measured again, all 4-20 %
behind on x86-64 - the in-run fast end's optimism once more. Of pool-sizes.py's 1,000 the other 970 rank below the 30 in
in-run speed (the written list's order: the worse width against the ceilings). It built in size order to 37,653 B before
the batch - about 36,000 after it (the batch takes 1,600-1,670 B from these), at the 1 % threshold: the band's larger rest
(to ~38,600 B before, chain C's) could hardly be 1 % smaller than 15eda54ebd.

## The self-hosting gate's speed half - 6 of 9 pass; fastest-x86-32, fastest-x86-64 and small-jit ship translator-built

selfhost-speed.py (720; results/selfhost-speed-725.md): each role's self-built image on its own engine against the lab's
build of its record, 5 alternations of 10 rounds, both widths; portable-fastest not timed (translator-built in the
laptop's tree at be190a273 - since 722 self-built; its reading is the next laptop run's). The rule: at most 1.02 at both
widths keeps it self-built.

| design | 8-byte: median (mean +/- SE) | 4-byte: median (mean +/- SE) | gate |
|---|---|---|---|
| best-all-round df097ba2e2 | 0.975 (0.976 +/- 0.016) | 0.956 (0.963 +/- 0.009) | pass |
| fastest-x86-32 11f956db93 | 0.994 (0.996 +/- 0.011) | **1.021** (1.010 +/- 0.015) | FAIL |
| fastest-x86-64 9b15ba26f7 | **1.046** (1.031 +/- 0.028) | 0.992 (1.003 +/- 0.020) | FAIL |
| least-memory fb0d57c8a2 | 1.000 (0.999 +/- 0.003) | 1.004 (1.005 +/- 0.007) | pass |
| portable-arm a8d35bdccc | 0.996 (0.997 +/- 0.005) | 0.994 (1.004 +/- 0.013) | pass |
| portable-knee 48a012411a | 1.008 (1.008 +/- 0.005) | 0.996 (0.994 +/- 0.012) | pass |
| portable-small ae99617f06 | 1.004 (1.003 +/- 0.003) | 1.006 (1.002 +/- 0.004) | pass |
| small-jit 15eda54ebd | 0.989 (0.986 +/- 0.010) | **1.036** (1.026 +/- 0.017) | FAIL |
| smallest 219878ec89 | 0.996 (0.997 +/- 0.003) | 1.004 (1.003 +/- 0.004) | pass |

The six without the JIT within 1 % at both widths; the JIT designs swing about 5 % either way (best-all-round's self-built
image 4 % faster at 4 bytes) - their engines differ too (a JIT engine compiles its image's layout lines), and 721's
instruction counts found self / translator 0.998-0.999 for small-jit at both widths: a code-placement effect, not more
work. fastest-x86-64's 8-byte ackermann 1.24, bubble and fib 1.11; fastest-x86-32's 1.021 is within its own spread (two of
five alternations below 1). **The owner (725): the rule as written - all three ship translator-built**, named in
designs/TRANSLATOR-BUILT with the ratio (`TRANSLATOR='NAME:REASON|...'` through results/drafts/roles-build-718.sh's two
phases for the three; no ARM build, so no cross GCC).

## The rage check - FAILED on the check's own fault; fixed

results/rage-designs-725.md: the Tegra took least-memory, portable-arm and portable-small (GCC, no JIT) and stopped at the
first: `export-arm: fb0d57c8a2 - the ARM image is not image32.img`. lab/evolve/export-arm.py required image32.img to be the
lab's translator-built image (tools/selfhost-ship.sh's header says so), but tools/rage-designs-check.sh copies designs/,
which ships self-built images since 676 (least-memory's image.img 9,278 B, its record's translator image 9,566); the
build-outs run export-arm.py before selfhost-ship.sh, so it had never met one (the last rage check, 654, came before 676).
It stopped after the Tegra's GCC built the engine, before `make forth-arm` was compared or run: the GCC designs' bytes
**untested, not wrong**. **Fixed (725)**: a design whose Makefile has the `selfhost32` rule ships a self-built image32.img
- export-arm.py then skips the image's identity (the engine's bytes still checked) and runs forth-arm on the shipped
image; tested here on the clang three (below, the PROGRESS entry). The Tegra's run again: lab/evolve/NEXT-RUN.

## dream at 4-byte cells - the GCC JIT designs about 3 times slower

11 of the 28 read 0.736-0.755 on dream at 4-byte cells, the other 17 0.256-0.281 - per session 0.743-0.744, every one of the
10. The split is exact by compiler: the 11 are every GCC (`-O2`) JIT design of the 28, the 17 every clang (`-Os`) one; the
same prebuilt binaries run normally on dream at 8-byte cells and on the laptop at both widths. dream / the laptop at 32
bits: the GCC JIT designs 3.22 (3.06-3.31), the clang JIT designs 1.17 (1.13-1.25). Against 15eda54ebd's ratio to s6 on
dream, workload by workload: fib 5.9-6.5 times, the far calls 5.8-6.3, ackermann 4.9-5.0, sieve 4.2-4.4, loop 3.7-4.0,
bubble 3.4-3.5, apps 2.0-2.1, kernel 1.7, corpus 1.3-1.4, parse 1.1-1.2 (on fib slower than s6 itself).
Every earlier chain has it as a tail (results/drafts/chainD-725.py: GCC JIT max 3.21 in chain-followup89, 2.86 in chain A),
never more than 9 GCC JIT designs a chain. **Nothing shipped is touched** (the four JIT roles are clang) and the verdict
above stands without dream (those 11 are 9-14 % behind on the laptop's x86-64); but the roles' x86-32 class pools dream's
reading, so a GCC JIT design is judged 3 times slower there than it runs on the laptop. Cause not found: a host effect on
an Intel Skylake (the i7-6700) with a 32-bit GCC JIT engine - one candidate, writes landing near the JIT's code
(self-modifying-code machine clears), unconfirmed; `perf stat` on dream would tell.

## Predictions (results/predictions.md, Iterations 717, 719, 720) - 4 of 7 right, one void

(1) right - the laptop 7 loadtest sessions, dream 10 a width, every line whole. (2) right - 1,000 below 35,980 B. (3)
wrong - no design beats 15eda54ebd. (4) void - none beat it. (5) right - none died. (6) right - "cnt" on every line, the
value restored (4). (7) wrong - rage-designs.py FAILED, the check's own fault, the bytes not reached. (8) wrong - 6 of 9
within 1.02.

## Next

lab/evolve/NEXT-RUN: the rage check again with the fix, and portable-fastest's selfhost-speed reading (722) - the
laptop's two steps, no remote line, about 40 minutes. Then the relf handoff final (results/drafts/handoff-relf-draft-721.md:
small-jit 15eda54ebd, the gate's three, the Tegra's check) and the package; then the plan's rest (the card).
