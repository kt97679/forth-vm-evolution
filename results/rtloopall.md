# rtloop for a design with all eight loop opcodes: the gene `rtloopall`

Iteration 43. Seed 8's front jumped from 0.661 at 8,171 bytes to 0.550 at
8,525: the jump was rtloop's overlay. Priced first - the words a design
gains with it, from the converter's symbol map, be02a4c0cf with rtloop and
without (+467 bytes):

| part | bytes |
|---|---|
| the words it defers to, kept alive: COMPILE,8 DO8 ?DO8 LEAVE8 | about 150-190 |
| three tables: LOOP-OPS X10-XTS X10-OPS - headers, padding, cells | about 127 |
| X10-OP, the chain mode (CHAIN16? RESOLVE-LEAVES), RESOLVE-LEAVE16, W@ | about 170 |

cv8-fuse-loop.4 serves any subset of the loop opcodes, so every word keeps
a fallback. Seven of the ten rtloop designs on seed 8's front have all
eight - (DO) (LOOP) (+LOOP) (?DO) (LEAVE) I J UNLOOP - and for them the
fallbacks are dead. **`forth/cv8-fuse-loopall.4`**, loaded in its place
for a design with rtloop, all eight opcodes and the gene `rtloopall`: no
fallbacks (the replaced words go, with lean), one chain (16 bits), one
12-byte table (I's offset in 16 bits, J's and UNLOOP's distance past it in
a byte - neighbours in the kernel; the converter asserts it). Only the
COMPILE,8 before it stays: which one that is depends on the other
overlays.

## Checks

Without the gene nothing moves: hand-made stages IDENTICAL, eight of seed
8's front designs (the rtloop ones among them) byte for byte, all 1,309
ids kept (rtloopall is in LATE); 20 overlay dumps load cleanly. With it,
on five of seed 8's front designs: alive, and the loop tests (nested I J,
-2 +LOOP, a ?DO of no passes, LEAVE, UNLOOP EXIT, LEAVE in a nested ?DO)
answer as with rtloop. INNER compiles to `(DO) DUP I + XOR (LOOP)` - five
one-byte dispatches a pass.

## Measured

| design | rtloop | rtloopall | saved |
|---|---|---|---|
| 85cac726b5 | 8,614 | 8,234 | 380 |
| 1b602bc9bd | 8,671 | 8,276 | 395 |
| 72ca2cf497 | 8,990 | 8,588 | 402 |
| 577c999e62 | 9,278 | 8,876 | 402 |
| 9bb527944a | 13,073 | 12,585 | 488 |

Dispatches, rtloopall over rtloop, counted on profiling engines: kernel
1.0005-1.0010, fib 1.0000, parse 0.9946-0.9973, corpus 1.0023-1.0026, loop
and sieve 1.0000 - the same speed for 380-488 bytes. 85cac726b5 would be
0.505 at 8,234 - where seed 8's front had 0.661 at 8,171.
