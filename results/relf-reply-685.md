# relf's answers to 684, and shellmix measured (Iteration 685)

relf's reply (its Iteration 953) is kept as results/drafts/relf-reply-953.md; its program, port/measure/shellmix.fth,
as lab/evolve/apps/shellmix.fth (the run line in genapps.py's call; held out, an eighth program in genapps.py and
mech-census.py). What the reply settles, and what shellmix measures on the lab's systems.

## What relf's answers settle

- **Mechanism 8 (address literals in 5 bytes): drop.** relf's real code (relfsh, 46,096 tokens; rill3) has no TO,
  VALUE or `[']`; its hooks are set at load time. The only program here it pays on is brainless (1,220 B), which is
  not relf's use; with VAR@ built, a variable reference is no address literal either.
- **DOES> is relf's, in two hot shapes**: DEFER (`CREATE 0 , DOES> DUP @ 0= IF DROP EXIT THEN @XT EXECUTE`, 58 in
  relfsh) and BUFFER: (`CREATE ... DOES> @`, 118). So mechanism 3 (DOES> @ as VAR@) and the JIT's DODOES stencil have
  real code to count on - but not in the four.
- **Mechanism 2's bytes were overstated (684).** relf's VAR@ is opcode + a self-relative slot operand, big-endian,
  2 bytes within +-16 KB or 3 to +-4 MB (relfsh: 2.21 operand bytes on average): 3.2 bytes against a call (2 or 3) and
  @ - **it saves dispatches, not bytes**, in relf too. 684's 188-359 B came from 674's per-construct averages (2.5):
  read those as about 0. One dispatch replaces three (call, DOVAR, @); 2VAR@ six; VAR@'s superinstructions fold the
  next operation (VAR@+ VAR@< VAR@C@ VAR@1+ VAR@0= VAR@SWAP). The rewrite is a peephole: `var @` / `var !` right after
  a call to a word whose body starts with DOVAR - the call rewound, the slot op laid; a `DOES> @ ;` word's call gets
  VAR@ on its data field.
- **Constants (1)**: relf always compiles the literal, whatever its width (few are wide: 4 of relfsh's 122); a
  constant is any word whose body is one literal and EXIT (`: X 5 ;` too, CONST-WORD?) - a constant-time test of the
  callee's first bytes, 0.35 % of building relfsh's image. 59's rtlit lost to a check on every compiled word: the test
  must be relf's kind, reading the callee, not searching.
- **Inlining (4)**: a colon word's body copied for its call if straight-line and at most 3 instructions and 6 bytes
  (relf 701's sweep: 3/6 against 4/12, 4/6, 6/16, 3/5); no branch, no return-stack word, no locals, no data word;
  calls inside allowed but to a word starting with R> or R@ ((S"), (POSTPONE)); slot ops re-aimed when copied.
- **What 684's list missed** - relf does these in its run-time compiler, where the lab's translator does some of them
  for the kernel image only: folded returns (23 op;EXIT codes), VAR@ superinstructions and 2VAR@, compare-and-branch
  (0= AND < U< EQI > = DUP fused with ?BRANCH), pairs (CELLS+ CELL+@ DUPC@ DUP1- OVER+ DUP>R, (LOOP)BRANCH8), one-byte
  branches, the narrowest literal (push0/1/-1, LIT8; `n -` as ADDI -n), two-byte calls to the first 16 KB, and the
  rule that makes it safe: every branch target clears the peephole state. No tail calls, no dead-code removal.
- **Compatibility**: nothing of relf's depends on the unpadded strings (681) or VALUE's kind cell (680).
- **relf will measure the new roles** (relfsh built on each: bytes on disk, bench-vm's five and the start, RSS,
  shellmix, its suite) against relfsh64, relfshasm64 and the current roles - "faster, smaller and more RAM efficient",
  no role losing on any of the three to both CV8 engines. It asks to be told when the roles exist and how to fetch them.

## shellmix on the lab's systems (8-byte cells; genapps.py, one round)

The same line on all fourteen systems. Its code (bytes, HERE's advance less its data): s6 1,657 · smallest 1,741 · least-memory 1,629 · portable-small 1,621 · portable-knee 1,621 · portable-arm 1,613 · portable-fastest 1,653 · best-all-round 1,773 · small-jit 1,773 · fastest-x86-64 1,805 · fastest-x86-32 1,773 · relf64 1,480 · relfasm64 1,480 · gforth-fast 8,360.

Its run against relf64's (0.104 s): s6 3.63 · smallest 5.51 · least-memory 3.27 · portable-small 2.31 · portable-knee 1.51 · portable-arm 2.06 · portable-fastest 1.47 · best-all-round 1.18 · small-jit 1.35 · fastest-x86-64 1.49 · fastest-x86-32 1.11 · relf64 1.00 · relfasm64 1.08 · gforth-fast 0.98.

**The JIT designs run it at 1.11-1.49 of relf64's time** - on 674's six smaller programs they ran at 0.35 of it. The
selection's four have no DOES> word, no DEFER-style hook: what shellmix exercises, the selection does not see.

On portable-knee (lab/evolve/mech-dispatch.py, the profiler): 216 M dispatches (relf64: 118 M); DODOES 1.68 % of them;
a data word's @ and ! as one op would take out 22.3 %, DOES> @ as VAR@ at least 3.0 % (the call and DODOES of each
BUFFER: use), constants 0.2 %, small-word inlining 0.6-0.8 %. Bytes (lab/evolve/mech-price.py): the JIT header 130 B
on the JIT designs, the data-word ops 37-70 B by 674's averages (about 0 by relf's 3.2), constants 7-14 B, address
literals 0.

## For the owner

1. **shellmix into the selection** as a fifth program? It is relf's real mix (VAR@-heavy, DOES> hooks and buffers),
   small (1.6-1.8 KB of code, about 0.2 s on the knee), and it shows what the four hide: the JIT designs slower than
   relf64. Without it, mechanism 3 and the DODOES stencil cannot be selected for.
2. **Drop mechanism 8** (relf does not use what it shortens).
Step 3's batch, by relf's numbers: VAR@/VAR! (with 2VAR@ and the superinstructions later), constants by relf's
test, inlining at 3/6, the JIT header; DOES> @ and the DODOES stencil if shellmix joins.
