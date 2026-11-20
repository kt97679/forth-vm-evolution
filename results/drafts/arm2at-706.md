# 2@ and 2! at any address on ARMv7 - the patch's tests (Iteration 706)

The after-seed-96 batch's arm2at (results/applied-after-seed96/ORDER.md). The cause, from the ARMv7 pre-flight (results/drafts/
arm-preflight-705.md): a tos=1 design's 2@ is `tos = CELL(a + CELL_BYTES); PUSHT(CELL(a))` (tools/gen-tos.py) - two
adjacent loads through UNS64*, which GCC joins into LDRD; ARMv7 traps LDRD and STRD at an address not word aligned (single
LDR and STR it allows). At tos=0 the store of the first value between the loads keeps them apart - every tos=0 design
lived under qemu. The fix: a one-byte-aligned UNS64 (CELLU) for 2@'s and 2!'s cell pair only.

## x86 - no byte changed

results/drafts/arm2at-bytes-706.py on results/followup-seed96-roles.md: 24 designs expressing 2@ - 4 of each of tos=0
GCC, tos=0 clang, tos=1 GCC, tos=1 clang, tos=1 clang with the JIT, tos=1 GCC with the JIT - each built by master's
evolve.py and by the patched tree's:

| width | designs | engine and image the same |
|---|---:|---:|
| 8-byte cells | 24 | 24 |
| 4-byte cells | 24 | 24 |

## ARMv7 under qemu-arm (tools/arm-cross-check.py, `CROSS=1 sh tools/setup-sandbox.sh`; the cross GCC 13 for --gcc,
gcc-multilib back after)

| build | designs | before (master) | after (patched) |
|---|---|---|---|
| GCC | d3496fcc6c, 2f5fa8daee, 2c841d55e3, 5d1597283e (tos=1), f8b7363885, 1e95d6638f, and 7fb40ff7ba, 58479dda0a (the final check's, measured on the Tegra) | 2 alive of 6 (705), 0 of 2 | 8 of 8 alive, fib and apps identical; engines +0 to +4 bytes |
| GCC | 14 spread by speed, the hand-made stages among them (--n 14) | - | 14 of 14 alive; s0-cell's apps DIFFERED by two "Redefining:" warnings - master the same; armcheck drops them, as evolve.py does: IDENTICAL |
| clang | 10 spread by speed (--n 10) | 8 of 8 (705) | 10 of 10 alive and identical |

The Tegra's readings are not in question: its kernel fixes the misaligned LDRD up (88 tos=1 GCC designs with 2@
measured there in the final check). What the patch buys: an ARM host whose kernel signals instead, and a qemu pre-flight
that no longer reports false deaths.
