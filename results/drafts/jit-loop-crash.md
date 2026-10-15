# A JIT fault seed 52 found: two designs die in the corpus's loop tests (Iteration 310)

Seed 52's database holds two designs that died on the corpus - the first such deaths in
these runs: b21c6f6763 and 171214ba65, both with the JIT. The evolution's correctness
check discarded them, as it should; no design on a front has been seen to fail. But the
fault is the JIT's, and a design whose corpus run misses the trigger could meet it in
another program.

## What is known

- **Reproduced here, deterministically**: built from these genomes on master, both die on
  the corpus (evolve.alive: "died: corpus").
- **The JIT is necessary**: with jit 0 both live. opinline and opbody are not: off, both
  still die.
- **Reverting any one of four genes to s6's value makes each live**: folds, ops10, rtloop,
  tag2 - the same four for both designs (one at a time; every other gene that differs from
  s6 - 28 for one, 26 for the other - reverted alone, both still die).
- **Where**: the corpus output matches s6's through line 15, "TESTING DO LOOP +LOOP I J
  UNLOOP LEAVE EXIT", and then ends - 16 lines against 788. The engine stops inside the
  loop tests: loops compiled at run time as opcodes (rtloop), translated by the JIT, with
  folded operand sequences (folds), in tag2's encoding, and some words of the design's
  format-10 list.
- All four genes are older than the batches applied since seed 47: most likely a latent
  fault that evolution reached now, not one a recent batch made.

## Narrowed (Iteration 310, later)

- **How it stops**: a segmentation fault - the engine's fault handler says
  "relf: segmentation fault", exit status 70.
- **The test**: the loop section's first - `{ 4 1 GD1 -> 1 2 3 }` with
  `: GD1 DO I LOOP ;`. A micro-program reproduces it in milliseconds:

      : GD1 DO I LOOP ;
      4 1 GD1 . . . CR
      BYE

- **The format-10 words it needs**: (DO), I and (LOOP) - dropping any one of the three
  from the first design's list stops the crash; dropping any of its other ten expressed
  words (SWAP+I THREAD-FIND ?BRANCH8 BRANCH8 (+LOOP) +! SKIP UNLOOP (LEAVE) PLACE) does not.
- So: the JIT translating a DO I LOOP compiled at run time (rtloop) as the three loop
  words' format-10 opcodes, with folds, in tag2's encoding. The likeliest fault: (LOOP)'s
  branch operand decoded by the JIT in a form the run-time compiler did not write it in -
  a jump to a wrong address on the first iteration. Unconfirmed.
- **Not an escape pair**: in the crashing design all three are one-byte opcodes - (DO) 95,
  I 88, (LOOP) 87 (vm-ops10-table.h) - so an operand misread after a two-byte opcode is
  ruled out. And folds' part is indirect: reverted, the loop words are not format-10
  opcodes at all, and the faulty path is never taken -
  as recorded     folds=['@', 'XOR', 'LSHIFT', 'C@', 'AND', 'DROP', '!', 'U<', 'SWAP', '+', 'C!', 'LIT']: the loop words expressed in format-10: ['(LOOP)', 'I', '(DO)'] (of 13 words)
  folds reverted  folds=['+', '=', '!', '@', 'LSHIFT', 'RSHIFT', 'C@', 'C!', 'AND', 'OR', 'XOR', 'LIT', '<', 'U<', 'OVER', 'DROP', 'DUP', 'SWAP', 'ROT', '>R', 'R>', 'R@', 'NEGATE']: the loop words expressed in format-10: none (of 2 words)
- So the fault is in the JIT's translation of a run-time-compiled DO I LOOP whose loop
  words are one-byte format-10 opcodes - (LOOP)'s branch operand (the JIT's operand kind
  7) or the loop's frame on the return stack. Next: dump GD1's compiled bytes and the
  JIT's translation of it, against the same loop compiled with the loop words as calls.

## The condition (Iteration 311)

- **The compiled code is right.** GD1's bytes, dumped without running it (a BEGIN WHILE
  loop, no DO): (DO), I, (LOOP) and the operand 254 255 - a 16-bit -2 from the operand's
  own address, pointing back at I - then EXIT. The JIT's kind 7 is exactly that: the
  operand is not the fault.
- **The JIT's loop support decides it**: with jitloop on, the micro-program prints 3 2 1;
  with the cached top of stack off (tos 0), 3 2 1. The crash needs jit, the loop words as
  one-byte format-10 opcodes in code compiled at run time (rtloop; folds only decides
  whether they are opcodes), **jitloop off and tos on**.
- On seed 52's front, 88 of the 89 JIT designs have jitloop: the evolution had kept out
  of this region because designs in it die - the two deaths are where it went back in.
- So the fault is in the JIT's translation of a loop without jitloop's support, with the
  top of the stack cached - the likeliest mechanism, a cached top not kept consistent
  across the loop's operations. Next: jit.c and the converter's table - what (DO), I and
  (LOOP) translate to without --jitloop, and how the cached top is passed across them.

## Next

1. (done) Which test; 2. (done) which format-10 words.
3. jit.c's translation of that loop opcode with a folded operand; a fix, the two
   designs alive, and an engines-check path with jit, rtloop, folds, tag2 and the words
   found - which today's 57 paths lack.

## The two genomes

```
{"abortif": 0, "align1": 1, "alignfn": 0, "alignhot": 2, "bss": 1, "bytehdr": 1, "compiler": 0, "d256": 0, "doesfar": 1, "dskew": 1, "enc": "cv8", "escape": 0, "factor": 3, "fbuf": 0, "fold": 1, "folds": ["@", "XOR", "LSHIFT", "C@", "AND", "DROP", "!", "U<", "SWAP", "+", "C!", "LIT"], "fsys": 2, "gotodup": 0, "guard": 0, "hotcalls": 32, "hotinl": 10, "ipaclone": 1, "jit": 1, "jitinl": 1, "jitk": 0, "jitloop": 0, "jitos": 0, "jittail": 0, "jitx": 1, "kfast": 1, "kinput": 0, "klookup": 0, "knumber": 0, "kstack": 0, "lean": 1, "lto": 1, "msc": 0, "nocet": 1, "nocrossjump": 0, "nogcse": 0, "noinls": 0, "noreorder": 0, "opbody": 1, "opcall": ["0="], "opinline": 1, "ops10": ["?BRANCH8", "BRANCH8", "(LOOP)", "I", "(+LOOP)", "TABS>BL", "+!", "SKIP", "UNLOOP", "(LEAVE)", "(>NUMBER)", "PLACE", "(DO)", "THREAD-FIND", ">?BRANCH8", "J", "?NBRANCH8", "<>?BRANCH8", "0<?BRANCH", "OVER?BRANCH", "=?BRANCH8", ">?BRANCH", "(?DO)", "EXECUTE", "SCAN", "HASH", "<>?BRANCH", "SWAP+I", "DUP?BRANCH", "0<?BRANCH8"], "opt": "Os", "peel": 1, "regpin": 0, "rtempty": 0, "rtfuse": 1, "rtimm": 1, "rtiplus": 0, "rtloop": 2, "rtloopall": 1, "scale": 0, "sharedcall": 0, "skippad": 0, "spec": ["loc", "var", "tiny", "small", "imm"], "supers": [["R@", "@"], ["C@", "@"], ["<", ">R"], ["+", "R>"], ["R>", "DUP"], ["NEGATE", "NEGATE"], ["ROT", "ROT"], ["DUP", "R@"], ["U<", "+"], ["<", "+"], ["@", ">R"], ["SWAP", "R>"], ["C!", "DROP"], ["DUP", ">R"], ["C@", "OR"], ["C@", "="], ["DUP", "C@"]], "swapi": 1, "sysc": 0, "t2hot": 1, "t2wide": 1, "tag2": 1, "tail": 0, "tailpn": 1, "tfind": 1, "thinhdr": 1, "threads": 3, "tos": 1, "tracer": 0, "varcall": 1, "varslot": 0}
{"abortif": 0, "align1": 0, "alignfn": 1, "alignhot": 2, "bss": 1, "bytehdr": 1, "compiler": 0, "d256": 0, "doesfar": 1, "dskew": 1, "enc": "cv8", "escape": 0, "factor": 3, "fbuf": 0, "fold": 1, "folds": ["@", "SWAP", "+", "AND", "DROP", "OR", "LIT", "!", "LSHIFT", "RSHIFT"], "fsys": 2, "gotodup": 0, "guard": 0, "hotcalls": 8, "hotinl": 0, "ipaclone": 0, "jit": 1, "jitinl": 0, "jitk": 0, "jitloop": 0, "jitos": 0, "jittail": 0, "jitx": 1, "kfast": 1, "kinput": 1, "klookup": 0, "knumber": 0, "kstack": 0, "lean": 1, "lto": 0, "msc": 0, "nocet": 1, "nocrossjump": 0, "nogcse": 0, "noinls": 0, "noreorder": 0, "opbody": 1, "opcall": ["@"], "opinline": 1, "ops10": ["?BRANCH8", "(LOOP)", "I", "(+LOOP)", "(DO)", "(LEAVE)", "+!", ">?BRANCH8", "<?BRANCH", "=?BRANCH8", "?NBRANCH8", ">?BRANCH", "0<?BRANCH8", "DUP?BRANCH8", "PLACE", "?DUP", "<?BRANCH8", "OVER?BRANCH8", "(?DO)", "?NBRANCH", "<>?BRANCH8", "<>?BRANCH", "=I?BRANCH", "EXECUTE", "FILL", "BRANCH8", "SCAN", "HASH", "(>NUMBER)", "TABS>BL", "=I?BRANCH8"], "opt": "Os", "peel": 1, "regpin": 0, "rtempty": 0, "rtfuse": 0, "rtimm": 1, "rtiplus": 0, "rtloop": 2, "rtloopall": 0, "scale": 0, "sharedcall": 1, "skippad": 0, "spec": ["loc", "tiny", "small", "imm"], "supers": [["DUP", ">R"], ["C@", "@"], ["C@", "OR"], ["DROP", "UM*"], ["NEGATE", "NEGATE"], ["RSHIFT", "@"], ["DUP", "R@"], ["R>", "="], ["ROT", "ROT"], ["@", "RSHIFT"], ["C@", "DUP"], ["+", "DROP"], ["DUP", "C@"], ["<", "+"], ["XOR", "C!"], ["R>", "U<"], ["C@", ">R"], ["@", ">R"]], "swapi": 1, "sysc": 0, "t2hot": 1, "t2wide": 1, "tag2": 1, "tail": 0, "tailpn": 0, "tfind": 1, "thinhdr": 1, "threads": 3, "tos": 1, "tracer": 0, "varcall": 1, "varslot": 0}
```
