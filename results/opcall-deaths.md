# Five wrong answers: the gene opcall (Iteration 173)

Seed 40's five corpus deaths are in its db with their genomes (status 'died:
corpus'): ee0eff671a, 8dff2a3647, 8587e5a5c1, 9586059a75, f7dc8437ff - all
JIT designs with opcall (X;CALL: an operation and the call after it, one
opcode). Reproduced (results/drafts/opcall-repro.py, seed 40's code):
f7dc8437ff (opcall 1+) is right with the JIT off or opcall empty, wrong with
tracer or jitinl off; 9586059a75 (opcall DROP) is right only with opcall empty
- the JIT off does not help. Both restart: "Welcome to Forth" again mid-corpus,
while the corpus defines EMPTY-STACK (lines 11-12) and } (32-34) - the
run-time compiler's fusion, or the JIT's X;CALL. The gate kills them (5 of
~35,000); next: trace a restart with the tracer.

## Two bugs, not one (Iteration 178)

Each expressed gene of two of the dead designs turned off in turn: the corpus
comes right again with
- 9586059a75 (opcall DROP): escape, rtfuse or supers off - the run-time pair
  fusion (cv8t-fuse.4's table) under the escape's numbering, with DROP;CALL;
- f7dc8437ff (opcall 1+): jit, spec, t2wide or tos off - the JIT, with 1+;CALL.
Tested and not it: a call written as a one-byte hot call after X;CALL (no
effect on any of the five; reverted). 25 of seed 40's front designs combine
opcall and tos and are right. Next: one bug at a time, a design each.

## Narrowed (Iteration 179)

**Bug 1, 9586059a75 (opcall DROP).** Its 17 pairs removed one at a time: right
without `DUP C@` alone, wrong with `DUP C@` the only pair - the trigger is that
pair fused at run time (cv8t-fuse.4), with DROP;CALL, under escape 2. DROP;CALL
sits in the fuser's own code (`... R> DROP THEN HERE`). Excluded: a hot call
after X;CALL (no effect, reverted); a numbering collision (opcall ops are
logical 0xFE00+k, pairs below 128); the wrong engine for the bodies (a TOS
design's gen-opcall copies vm-lab-tos.c); preprocessor lines spliced (L_drop
and L_onep have none). Next: what the fuser writes for `: T DUP C@ ;` there.

**Bug 2, f7dc8437ff (opcall 1+).** Right with the tiny specialisation off -
var, small, imm do not matter; nor tracer, jitinl, supers, hotinl, hotcalls.
*Corrected the same day:* that says nothing about tiny. tiny is what makes 1+
an opcode (sod16 tiny_at: a call to the colon word becomes the operation);
without it 1+ is a call and is never fused - tiny off is opcall off by another
road. What is left: 1+;CALL itself goes wrong with the JIT, t2wide and tos
together. Next: what the JIT does around an X;CALL in such a design.
