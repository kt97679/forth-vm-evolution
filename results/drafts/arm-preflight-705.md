# The ARMv7 pre-flight for the new roles' screen (Iteration 705)

No design with step 3's genes (rtvar, rtconst, rtinline - 687-695) had been built for ARMv7 before the screen sends 437 to
the Tegra (results/followup-seed96-roles-arm.md). Here, `CROSS=1 sh tools/setup-sandbox.sh`, then tools/arm-cross-check.py
on that list: each design built by evolve.py at 4-byte cells for ARMv7, without the C library, alive (the corpus, the
kernel, far, full) and fib and apps as s6 gives them, under qemu-arm.

- **clang** (the laptop cross-builds these for the Tegra): 8 of 8 alive and identical - one design for each combination
  of the three genes (a9e72d295d rtinline, 64f3b1f920 rtconst, 3ca1b5bef2 both, 2179425c60 rtvar, b3fb4dde32 rtvar and
  rtinline, cab831cce8 rtvar and rtconst, 661541e0cb all three) and 9f1a569f91 none; ARM engines 6,472-19,548 bytes.
- **GCC** (the Tegra builds these with its own GCC 16; here arm-linux-gnueabihf-gcc 13, which removes gcc-multilib -
  put back after): 2 of 6 alive. All 6 identical on fib and apps; the 4 dead (d3496fcc6c, 2f5fa8daee, 2c841d55e3,
  5d1597283e) stop at the same corpus test - `HERE 1 ALLOT` then `HERE 1 ,` and `1ST 2@`: a cell at an odd address -
  with a segmentation fault or SIGBUS. What separates them: tos=1 (the cached top of stack) in all 4, in none of the 5
  alive (with the old holders 3eb59b271d, ae99617f06, fb0d57c8a2, all alive here). GCC compiles a cached-TOS 2@ as one
  doubleword load, which ARMv7 traps at a misaligned address; Linux on the Tegra fixes the access up, qemu-user does not.
  **A qemu artifact, not the genes**: 7fb40ff7ba and 58479dda0a (GCC, tos=1, 2@ a primitive), both measured on the
  Tegra in the final check (results/chain-followup91-final/, 0.306 and 0.480), die here the same way; 88 such designs
  ran there. d3496fcc6c, one of the 4, has none of the new genes.

So the screen's Tegra line builds as tested. One thing for relf and the article: on an ARM host whose kernel signals
misaligned accesses (/proc/cpu/alignment set to signal) a tos=1 GCC design dies where the corpus stores a cell at an odd
address - an ambiguous condition in Forth 2012 (`,` with the data-space pointer unaligned), which the Hayes test exercises.
