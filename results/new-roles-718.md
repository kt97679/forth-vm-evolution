# The new roles - the ten chosen, every near one kept on record (Iteration 718)

The owner (718), on the three choices chain C left (results/followup-roles-seed96-roles-c.md): "I don't have strong
opinions, please proceed in the most reasonable way ensuring we are not losing any good designs". So each is decided by
the rule the chains already judge by - a design replaces the leader when it is 1 % smaller (binary + image + code), no
class (x86-64, x86-32, ARMv7) 2 % slower, memory within 8 KB; a speed role's challenger must be 2 % faster at 2 SE - the
same for all three, and with 649's precedent for the smallest (d180351903 taken at -8 B because it lost nowhere). Every
design the rule does not ship but that is on a front of the trade is listed below with its numbers: none is lost, and
any can be shipped later with the same build-out (results/drafts/roles-build-718.sh, a role at a time).

## The three choices

1. **The smallest: 219878ec89 stays** (21,673 B). The 23 smaller designs are 3-7 B smaller (0.01-0.03 %) and each 3.7-6.3 % slower
   in a class - trades, not wins, as 649's rule reads it. Kept on record: **3456fc28b2** (21,666 B, the fewest bytes:
   x86-64 -11.33 %, x86-32 +5.54 %, ARMv7 +3.63 % against 219878ec89) and **90273721a1** (21,679 B, +6 B: x86-64 -11.32 %,
   x86-32 -2.06 %, ARMv7 -0.18 %, pooled over chains B and C - faster in every class), with the other three at 21,679 B.
2. **The fastest portable: d727605472** (35,539 B, 148 KB). 5f7e66b12d ties it on the mean (+0.21 % +/- 0.14 %, pooled)
   and is 4.2 % smaller, but x86-32 +2.68 % +/- 0.14 % - a class 2 % slower, so it does not replace it. Kept on record:
   5f7e66b12d (34,056 B; x86-64 -1.45 %, ARMv7 -0.82 %).
3. **The fastest on x86-32: 11f956db93** (49,925 B, 264 KB). Within 2 SE of ea782c6094 (+0.24 % +/- 0.32 % pooled) and 3.8 %
   smaller, 16 KB leaner, x86-64 +0.37 % - it replaces it by the rule. 69cebcaed9 (50,172 B, 260 KB) leads by 0.15 % in chain C
   and is within 1 % and 8 KB of 11f956db93 - the same by the rule; 11f956db93 is the smaller. 163935642a (49,105 B) is
   smaller still but 40 KB more memory and x86-64 +5.2 %. Kept on record: 69cebcaed9, ea782c6094, b525180392, 163935642a.

## The ten

| role (designs/) | design | bytes (8-byte cells) | memory | against the 649 holder | decided |
|---|---|---:|---:|---|---|
| fastest-x86-64 | 9b15ba26f7 | 53,503 | 292 KB | c7c35f9c97: x86-64 -10.65 % +/- 0.54 % | chain B |
| fastest-x86-32 | 11f956db93 | 49,925 | 264 KB | ee34931cd7: x86-32 about -6.4 % (chain C; ea782c6094's -5.49 % in chain B, tied) | 718, the rule |
| best-all-round | df097ba2e2 | 54,695 | 288 KB | 06b188f45b: the mean -7.53 % +/- 0.23 % | chain B |
| small-jit | 15eda54ebd | 36,344 | 208 KB | c6f1c1331b: -1.25 % bytes, x86-64 -0.69 %, x86-32 +0.27 %, -4 KB | chain C; **provisional - chain D** |
| portable-fastest | d727605472 | 35,539 | 148 KB | 782f3ad7ff: the mean -7.46 % +/- 0.10 % | chain B, 718 |
| portable-arm | a8d35bdccc | 45,274 | - | 3eb59b271d: ARMv7 -2.63 % +/- 0.39 % | chain B |
| portable-knee | 48a012411a | 26,957 | - | 11a56ff9e4: bytes -1.38 %, speed within 1 % | chain B |
| portable-small | ae99617f06 | 26,261 | 124 KB | kept (e51c01ba10 +70 %, 4acee9a48e +38 % on ARMv7) | chain C |
| least-memory | fb0d57c8a2 | 25,569 | 112 KB | kept (the 8 KB rule; every contender an ARMv7 trade) | chain B |
| smallest | 219878ec89 | 21,673 | 116 KB | d180351903: -1.96 % bytes, 18.7-28.1 % faster in every class | chain B, 718 |

The records: results/relf-designs-718.md (chain C's list's - master's sizes, the laptop's memory).

## Kept on record - the near ones the rule does not ship

| role | design | why it is not shipped | where its numbers are |
|---|---|---|---|
| smallest | 3456fc28b2 (21,666 B) | 7 B smaller, x86-32 +5.5 %, ARMv7 +3.6 % - a trade | results/followup-roles-seed96-roles-c.md |
| smallest | 90273721a1 and the three others at 21,679 B | 6 B larger; faster in every class (x86-64 -11.3 %) | the same; results/followup-roles-seed96-roles-b.md |
| portable-fastest | 5f7e66b12d (34,056 B) | the mean tied, 4.2 % smaller, x86-32 +2.7 % | the same; results/drafts/chainC-716.py |
| fastest-x86-32 | 69cebcaed9, ea782c6094, b525180392, 163935642a | tied on x86-32; larger or (163935642a) 40 KB more memory | results/drafts/chainC-716.py |
| fastest-x86-64 | 262a51bc6c (54,551 B) | -0.38 % +/- 0.31 % pooled, under the 2 % rule; 2.0 % larger | results/drafts/chainC-716.py |
| small-jit | fa38596098, 13a2b38e1b | beat c6f1c1331b too; 13a2b38e1b 64 B larger than 15eda54ebd, x86-64 -0.88 %, +8 KB | results/followup-roles-seed96-roles-c.md |
| small-jit | chain D's band (results/followup-seed96-jitband.md and the laptop's finds) | not yet measured | chain D |
| least-memory | 71005d8a0d, 16560cb51f, 2c841d55e3 (112 KB) | x86 4-23 % faster, ARMv7 6-7 % slower - trades | results/followup-roles-seed96-roles-b.md |

## Next

The build-out (results/drafts/roles-build-718.sh: designs/ made again, the GCC designs' ARM rule by the cross GCC,
self-hosting phase 6 by tools/selfhost-ship.sh - a design the cross compiler cannot build ships translator-built, named
in designs/TRANSLATOR-BUILT; the package by pack-designs.py); the Tegra's own GCC confirms the GCC designs' bytes
(RAGECHECK_CMD='sh tools/rage-designs-check.sh' sh tools/rage-check.sh, the owner, beside chain D); chain D decides
small-jit; then relf told how to fetch the ten (one message, after chain D).
