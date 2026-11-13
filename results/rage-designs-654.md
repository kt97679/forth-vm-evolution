# The rage check - designs/' forth-arm on the Tegra (Iteration 654)

**PASS.** The chain at c8c423671f (Iteration 652's commit; NEXT-RUN `experiment rage-designs.py`, set at 647), on fury
2026-11-12 22:53-23:10, 17 minutes; its archive forth-vm-evolution-chain-c8c423671f-fury-20261112-231020_tar.gz, the
pack forth-vm-evolution-rage-designs-c8c423671f-fury-20261112-231020.tar.gz. On the Tegra the three GCC designs without
the JIT were built by its own cc as the lab's build() builds them, and each designs/NAME's `make forth-arm`, in a fresh
directory holding only that design, gave the same bytes and ran ': SQ DUP * ; 7 SQ .' to 49. Every figure below:
results/drafts/rage-pack-654.py on the archive, unpacked nowhere (exit 0; a copy with one design's line made DIFFERS
fails on that design).

## The chain

The laptop: run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS. Its tree the commit's: 3,882 of 3,882 tracked
files at the commit's sizes, `git status --porcelain --ignored` 7 lines, all ignored. rage-designs.py 22:58-23:10, about
12 minutes - HEAD copied to the Tegra, its stages built there, then tools/rage-designs-check.sh (the first run's chain,
2e9343d91f, failed at 16 minutes - 652).

## The choice - 652's fix on the Tegra

export-arm.py --list classed each design by its exported Makefile (`CC =`, src/jit.c in SRC), each as designs/ at
c8c423671f has it: least-memory, portable-arm and portable-small (GCC, no JIT) taken; the clang three (portable-fastest,
portable-knee, smallest) and the four JIT designs (best-all-round, fastest-x86-64, fastest-x86-32, small-jit) not this
host's. The first run failed at this step: the Tegra's express() made best-all-round a GCC design without the JIT.

## The three

| design | id | srcarm files | make's forth-arm | tightened = build()'s engine | the check |
|---|---|---|---|---|---|
| least-memory | fb0d57c8a2 | 6 | 14564 B | 11584 B | the lab's bytes, runs (7 SQ . -> 49) |
| portable-small | ae99617f06 | 8 | 17104 B | 13440 B | the lab's bytes, runs (7 SQ . -> 49) |
| portable-arm | 3eb59b271d | 10 | 19712 B | 15968 B | the lab's bytes, runs (7 SQ . -> 49) |

None of the three engine sizes was in the repository before (designs/*/record.json hold no ARM figures). With the clang
three's forth-arm the lab's bytes, cross-built and running under qemu-arm (646; smallest d180351903 at 649), every
design without the JIT has its ARM build checked; the four JIT designs have none (the JIT is x86 code).

## What the PASS covers, and what is left on rage

- It proves the Makefile reproduces build() with the cc rage had on 2026-11-12. The pack names no compiler; the records
  have GCC 16.2.1 from seed 78 through the final check (results/followup-roles-seed91-final.md, "The Tegra between
  chains": the kernel moved 7.3.1 -> 7.3.3 on 2026-11-10, the compiler stayed).
- One /tmp/export-arm-check-* on rage (elf_tight.py only): 652's --list made it and exited - fixed in 653, after this
  run's commit. fve-ragecheck/build.log and check.log stay there by design (rage-check.sh keeps the log on a pass).
- The pack's rage-designs.log is empty by design: rage-designs.py folds stderr into rage-designs.md.

The owner's, once - the compiler named for the relf handoff, the directory removed:
`ssh rage.lan 'cc --version | head -1; rm -rf /tmp/export-arm-check-*'`

## The prediction (results/predictions.md, 648)

(1) rage-designs.md says PASS, all three byte for byte - 75/25: right. The rage check's: 1 of 1 (the run at 2e9343d91f
not scored - 652).

## rage-designs.md, as it came

```
# designs/' forth-arm on the Tegra (lab/evolve/rage-designs.py, Iteration 647)

rage-check: rage.lan, c8c423671f Iteration 652: the rage check's first run failed , evolve-amd-ryzen-7-pro-8840hs-seed91.md
rage-check: building the stages there
best-all-round (06b188f45b): clang, the JIT - not this host's
fastest-x86-32 (ee34931cd7): clang, the JIT - not this host's
fastest-x86-64 (c7c35f9c97): clang, the JIT - not this host's
least-memory (fb0d57c8a2): GCC, no JIT - taken here
portable-arm (3eb59b271d): GCC, no JIT - taken here
portable-fastest (782f3ad7ff): clang, no JIT - not this host's
portable-knee (11a56ff9e4): clang, no JIT - not this host's
portable-small (ae99617f06): GCC, no JIT - taken here
smallest (d180351903): clang, no JIT - not this host's
small-jit (c6f1c1331b): clang, the JIT - not this host's
pinned to cpu 1 (it and its sibling 7% busy; BENCH_CPU=N to choose)
least-memory (fb0d57c8a2, GCC): srcarm 6 files, the engine 11584 bytes
portable-arm (3eb59b271d, GCC): srcarm 10 files, the engine 15968 bytes
portable-small (ae99617f06, GCC): srcarm 8 files, the engine 13440 bytes
/tmp/export-arm-check-fohq14g7/least-memory/forth-arm.tight: 14564 -> 11584 bytes
  least-memory forth-arm: the lab's bytes, runs (7 SQ . -> 49)
/tmp/export-arm-check-fohq14g7/portable-arm/forth-arm.tight: 19712 -> 15968 bytes
  portable-arm forth-arm: the lab's bytes, runs (7 SQ . -> 49)
/tmp/export-arm-check-fohq14g7/portable-small/forth-arm.tight: 17104 -> 13440 bytes
  portable-small forth-arm: the lab's bytes, runs (7 SQ . -> 49)
export-arm: 3 designs, all the lab's bytes and running
rage-check: exit 0
rage-check: PASS

rage-designs: PASS
```
