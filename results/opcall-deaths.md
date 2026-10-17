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

## One pattern, contained (Iteration 180)

Probing bug 1's design step by step (each step its own process - a restart
loses the buffered output): `: U DUP @ ;` alone restarts it; `DUP C@` (a pair)
is right. The X;CALLs in all five dead designs: 9586059a75's eleven DROP;CALLs
escaped (first byte 0x3F); the other four's in t2wide's band (144, 157, 177,
178, 179 - 0x80-0xBF). The engine's tables send both bands to the X;CALL
handlers, and the JIT decodes the wide band right - the mechanism is still not
found. But the pattern holds: every gene whose removal fixed a design changes
how many operations compete for the 63 base codes, moving the X;CALL in.

**Contained:** X;CALL only where its code is in the base band; elsewhere the
plain operation (tools/layout.py, results/applied-after-seed41/opcall-band-after-seed41.patch).
All five dead designs right; all 48 of seed 40's front designs with opcall
alive; 7 of 7 stages identical. The root cause stays open.

## The cause (Iteration 191)

Bisected on 9586059a75 with the band containment off: eleven X;CALLs, each
built alone - only one breaks it, the DROP;CALL in SUPER-OP (the run-time
pair fuser's lookup), whose call goes to (LOOP) - a colon word taking an
inline operand. Not the branch targets (fused only where a branch targets
the call: right; only elsewhere: wrong). The bytes: `3f 00` (DROP;CALL,
escaped, selector 0), then `00 00 00 00`, then the 4-byte call `c0 00 03 2a`,
then the operand. The four zeros are pad_before's alignment for the operand -
in FRONT of the call, so BETWEEN X;CALL and its call. CALLNEXT reads the byte
after X;CALL as the call's first: 0x00, a 2-byte call to offset 0 - the
image's start - and the system restarts.

So the band was a coincidence: escaping moved that one site to a padded
position. Any X;CALL before a call with an inline operand is exposed wherever
the padding is not zero (7 positions of 8); the base-band designs that
survived had none padded. The "two bugs" of Iteration 178 were genes moving
code positions. The fix (tools/sod16.py opcall_rewrite): no X;CALL in front of
a call whose operand follows it - padding goes only there, so an X;CALL is
always followed by its call. The containment is out: every band open again.

Checked: all five dead designs right with every band (corpus); all 25 opcall
designs of seed 40's front and the five alive through the full gate (30 of 30);
run-tests PASS. results/applied-after-seed41/opcall-fix-after-seed41.patch, the fifteenth.
