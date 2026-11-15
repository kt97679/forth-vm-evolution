# The gene rtinline - a short colon definition copied for its call at run time (Iteration 694; step 3, mechanism 2)

forth/cv8-fuse-inline.4: a call, in code compiled at run time, to a word whose body is at most three instructions in
six bytes (relf's limits) becomes a copy of those bytes - one dispatch less for the call and one for the EXIT. Copied
as they are, so only operations that cannot tell where they sit: tools/layout.py's INL-OPS, a whitelist in the design's
own one-byte codes (two bits a code, its length with its operand; either family): the stack, arithmetic, logic and
memory operations, the short literals and immediate forms, pairs of them - no call, branch, loop operation, return
stack or locals operation, no EXECUTE (a callee would see one frame less). A body whose last operation folded its EXIT
in is copied with the plain code (the table's pairs); under the tag with the JIT a word's header is stepped over.
Loaded after rtvar's overlay and before rtconst's, so a constant still becomes a literal rtimm can fuse. The gene
rtinline (it needs the run-time fusers) and its -inl dumps.

## Checked (lab/evolve/rtinline-check.py): PASS on portable-knee, least-memory, portable-fastest, fastest-x86-64

Alive with rtinline 0 and 1; the same and right values for words it copies (two operations, a literal and an
operation, three, a 16-bit literal, an empty body, an EXIT within: copied to the first EXIT) and words it must not
(four operations, the return stack, calls, a DOES> child, a variable); `1+ 1+` compiled as its two ADDI 1 on the knee;
`>R 1+ R>` left a call.

## What it buys (medians: the apps workload of 15, each program's benchmark alone of 7; the sandbox, a few % noise)

| design | apps workload | sim16 | gc16 | scan | evo | shellmix |
|---|---|---|---|---|---|---|
| least-memory | 0.971 | 0.953 | 0.893 | 0.932 | 0.930 | 0.916 |
| portable-knee | 1.000 (0.989) | 0.917 (0.913) | 0.939 (0.856) | 0.992 (0.905) | 0.986 (0.954) | 0.905 (0.939) |
| portable-fastest | 0.976 | 0.986 | 0.919 | 0.919 | 0.980 | 0.958 |
| fastest-x86-64 (JIT) | 1.036 | 0.885 | 0.825 | 0.861 | 0.940 | 0.853 |

(the knee twice: the spread is the noise.) The programs' run time gains 5-15 %; the short apps workload, mostly
compiling, about even. The JIT design gains most: its own inlining (jitinl) takes one-operation words; this takes the
two- and three-operation ones, and a copied body stays native where the call had been translated alone.

## And the dumps, made when first asked for (evolve.py's dump_file)

setup() made every kernel dump up front - 2,699, 63 s at every start of a run or a check tool, and each run-time gene
doubled the fused ones (rtinline would have made it about 2 minutes). Now each is made the first time a design asks
for it, in build/dumps-HASH (HASH of the overlays, the cell engine and its kernel image: a change makes new ones, none
deleted under a reader; written under a name of its own and renamed, for the pool's workers); setup 1.6 s. boot_files()
is the one list of a dump's files - export-genes.py's own copy had missed 687's -var and 691's -const, so a design
exported with rtvar or rtconst would have lost its overlay. The 5,400 old dumps in build/ removed.
