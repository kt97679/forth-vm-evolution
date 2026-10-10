# The gene opcall: an operation and the call after it in one opcode (Iteration 121)

From the owner's documents (results/docs-reuse.md): Koopman's Table 6.3 - on
the RTX 32P, an operation sharing its instruction with the call after it was
11% of instructions; the one combination of his no gene had.

**What it does.** `X;CALL` is an opcode of its own for an operation X that
comes before a call: X's handler, copied (tools/gen-opcall.py), with its
NEXT() made CALLNEXT() - the call's first byte read, a compare, a direct jump
into the call's code for its width (vm-lab.c) - where NEXT would have gone
through the table. The call itself stays as it was after it, so a branch to
the call still finds a call. The converter (tools/sod16.py opcall_rewrite)
makes the change last, on the operation as it ends up. Only operations
without an operand and with one exit: the pool is DROP AND @ >R C@ SWAP DUP
ROT OVER R> + OR, 0= and 1+ (the tiny specialisation's), (PARSE) and PLACE
(format-10 words) - each offered only where the design has it.

**Codes of their own.** The two designs it was meant for had no slot left in
the 128-entry table (the fastest: 39 format-10 words and 11 pairs). So the
fused operations are logical 0xFE00 + k, with their own small table, as the
JIT's opcode is: they compete only for the tag's one-byte codes, by rank.

**Measured** (the VM; bytecode dispatches, every available operation fused):

| design | fused | image | engine | kernel | parse | corpus |
|---|---|---|---|---|---|---|
| fastest, e5193642ef | 16 | +24 bytes | +768 bytes | -1.6% | -3.8% | -3.4% |
| smallest, 585376cf49 | 14 | +0 | +656 bytes | -1.6% | -2.5% | -2.5% |

Under the 2.7-6.6% priced: the two operations before calls most often, LIT8
and ?BRANCH8, carry an operand or two exits and are not fused. Each fused
operation costs ~45 bytes of engine; mutation adds or removes one at a time.
On JIT designs a kernel word holding a fused operation stays bytecode (the
translator knows no stencil for it) - correct, a little less native.

**Checks**: the gate on both; the held-out ANS suite on both - all ten files
as s6; tests; hand-made stages; all 945 recorded designs keep their ids; the
converter's format-10 body checks run with it off (they failed with it on).
