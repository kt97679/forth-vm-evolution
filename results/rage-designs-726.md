# The rage check again - designs/' forth-arm on the Tegra (Iteration 726)

**PASS.** The chain at b0801d04e (Iteration 725's commit; NEXT-RUN `experiment rage-designs.py then experiment
selfhost-speed.py --rounds 10 --pairs 5 portable-fastest`), on fury 2026-11-22 05:28:49-05:38:35 UTC, 586 s; its archive
402c6eb5-forth-vm-evolution-chain-b0801d04e-fury-20261122-053836.tar.gz (the packs forth-vm-evolution-rage-designs-b0801d04e-fury-20261122-053647.tar.gz
and forth-vm-evolution-selfhost-speed-b0801d04e-fury-20261122-053836.tar.gz). On the Tegra the three GCC designs without
the JIT were built by its own cc as the lab's build() builds them, and each designs/NAME's `make forth-arm` gave the same
bytes and ran ': SQ DUP * ; 7 SQ .' to 49 on its shipped self-built image32.img - 725's fix to export-arm.py (a
`selfhost32` design's image not asked to be the translator's), whose absence stopped chain D's run before the bytes.
Every figure below: results/drafts/chain-pack-726.py on the archive, unpacked nowhere (exit 0).

## The chain

The laptop: run-tests PASS (253 s), validate 7 of 7 IDENTICAL, the jail PASS; both packs' trees the commit's (4,883 of
4,883 tracked files at its sizes, `git status --porcelain --ignored` 27 lines, all ignored); kernel.perf_event_paranoid 4
at the pack, no perf hold taken (neither step counts). rage-designs.py 206 s (05:33:20-05:36:46): HEAD copied to the
Tegra, a fresh clone there (rage-check.sh removes the last one first - chain D's kept clone not reused), its stages
built, then tools/rage-designs-check.sh. 654's took about 12 minutes by the same scripts (unchanged since 646); the pack
times nothing on the Tegra's side, so the difference is not explained - the PASS rests on the byte comparisons and the
runs, not the time. Then selfhost-speed.py 98 s (results/selfhost-speed-726.md). NEXT-RUN's "about 40 minutes" was
654's whole chain (17) and the gate (~2) with a margin: the chain ended early by design, not by a fault.

## The choice

export-arm.py --list classed each design by its exported Makefile at b0801d04e (`CC =`, src/jit.c in SRC) - checked
against each Makefile there: least-memory, portable-arm and portable-small (GCC, no JIT) taken; the clang three and the
four JIT designs not this host's.

## The three

| design | id | srcarm files | make's forth-arm | tightened = build()'s engine | image32.img | the check |
|---|---|---|---|---|---|---|
| least-memory | fb0d57c8a2 | 6 | 14,280 B | 11,158 B | self-built | the lab's bytes, runs (7 SQ . -> 49) |
| portable-small | ae99617f06 | 8 | 16,760 B | 13,014 B | self-built | the lab's bytes, runs (7 SQ . -> 49) |
| portable-arm | a8d35bdccc | 10 | 20,624 B | 16,782 B | self-built | the lab's bytes, runs (7 SQ . -> 49) |

portable-arm is a8d35bdccc's first check there (718's role; 654 checked 3eb59b271d). least-memory and portable-small,
the same designs as at 654, are 426 B smaller each (11,584 and 13,440 B then): the engine code both share changed since
(681-713, the after-seed-96 batch among it) - not traced byte by byte; the check compares the Tegra's build() with the
Makefile at one commit, so the sizes are today's. With the clang three's forth-arm the lab's bytes under qemu-arm (725),
every design without the JIT has its ARM build checked again on the self-built images.

## The predictions (results/predictions.md, 725)

(1) rage-designs.py PASS - 80/20: right. (2) portable-fastest within 1.02 at both widths - 80/20: right (0.9974, 0.9867).
(3) the chain ends with both packs and nothing failed - 85/15: right. 3 of 3. The pack names no compiler; 655's 16.2.1 is
the last on record.

## rage-designs.md, as it came

# designs/' forth-arm on the Tegra (lab/evolve/rage-designs.py, Iteration 647)

rage-check: rage.lan, b0801d04e Iteration 725: chain D processed - small-jit stays, evolve-amd-ryzen-7-pro-8840hs-seed96.md
rage-check: building the stages there
best-all-round (df097ba2e2): clang, the JIT - not this host's
fastest-x86-32 (11f956db93): clang, the JIT - not this host's
fastest-x86-64 (9b15ba26f7): clang, the JIT - not this host's
least-memory (fb0d57c8a2): GCC, no JIT - taken here
portable-arm (a8d35bdccc): GCC, no JIT - taken here
portable-fastest (d727605472): clang, no JIT - not this host's
portable-knee (48a012411a): clang, no JIT - not this host's
portable-small (ae99617f06): GCC, no JIT - taken here
smallest (219878ec89): clang, no JIT - not this host's
small-jit (15eda54ebd): clang, the JIT - not this host's
pinned to cpu 1 (it and its sibling 13% busy; BENCH_CPU=N to choose)
least-memory (fb0d57c8a2, GCC): srcarm 6 files, the engine 11158 bytes, image32.img self-built (its identity not asked)
portable-arm (a8d35bdccc, GCC): srcarm 10 files, the engine 16782 bytes, image32.img self-built (its identity not asked)
portable-small (ae99617f06, GCC): srcarm 8 files, the engine 13014 bytes, image32.img self-built (its identity not asked)
/tmp/export-arm-check-aql9fov7/least-memory/forth-arm.tight: 14280 -> 11158 bytes
  least-memory forth-arm: the lab's bytes, runs (7 SQ . -> 49)
/tmp/export-arm-check-aql9fov7/portable-arm/forth-arm.tight: 20624 -> 16782 bytes
  portable-arm forth-arm: the lab's bytes, runs (7 SQ . -> 49)
/tmp/export-arm-check-aql9fov7/portable-small/forth-arm.tight: 16760 -> 13014 bytes
  portable-small forth-arm: the lab's bytes, runs (7 SQ . -> 49)
export-arm: 3 designs, all the lab's bytes and running
rage-check: exit 0
rage-check: PASS

rage-designs: PASS
