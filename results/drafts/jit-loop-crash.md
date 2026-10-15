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

## Next

1. Which test: run the loop section's tests one at a time; the engine's exit status
   (signal, or a Forth abort).
2. Which format-10 words: drop them one at a time from the design's list.
3. Then jit.c's translation of that loop opcode with a folded operand; a fix, the two
   designs alive, and an engines-check path with jit, rtloop, folds, tag2 and the words
   found - which today's 57 paths lack.

## The two genomes

```
{"abortif": 0, "align1": 1, "alignfn": 0, "alignhot": 2, "bss": 1, "bytehdr": 1, "compiler": 0, "d256": 0, "doesfar": 1, "dskew": 1, "enc": "cv8", "escape": 0, "factor": 3, "fbuf": 0, "fold": 1, "folds": ["@", "XOR", "LSHIFT", "C@", "AND", "DROP", "!", "U<", "SWAP", "+", "C!", "LIT"], "fsys": 2, "gotodup": 0, "guard": 0, "hotcalls": 32, "hotinl": 10, "ipaclone": 1, "jit": 1, "jitinl": 1, "jitk": 0, "jitloop": 0, "jitos": 0, "jittail": 0, "jitx": 1, "kfast": 1, "kinput": 0, "klookup": 0, "knumber": 0, "kstack": 0, "lean": 1, "lto": 1, "msc": 0, "nocet": 1, "nocrossjump": 0, "nogcse": 0, "noinls": 0, "noreorder": 0, "opbody": 1, "opcall": ["0="], "opinline": 1, "ops10": ["?BRANCH8", "BRANCH8", "(LOOP)", "I", "(+LOOP)", "TABS>BL", "+!", "SKIP", "UNLOOP", "(LEAVE)", "(>NUMBER)", "PLACE", "(DO)", "THREAD-FIND", ">?BRANCH8", "J", "?NBRANCH8", "<>?BRANCH8", "0<?BRANCH", "OVER?BRANCH", "=?BRANCH8", ">?BRANCH", "(?DO)", "EXECUTE", "SCAN", "HASH", "<>?BRANCH", "SWAP+I", "DUP?BRANCH", "0<?BRANCH8"], "opt": "Os", "peel": 1, "regpin": 0, "rtempty": 0, "rtfuse": 1, "rtimm": 1, "rtiplus": 0, "rtloop": 2, "rtloopall": 1, "scale": 0, "sharedcall": 0, "skippad": 0, "spec": ["loc", "var", "tiny", "small", "imm"], "supers": [["R@", "@"], ["C@", "@"], ["<", ">R"], ["+", "R>"], ["R>", "DUP"], ["NEGATE", "NEGATE"], ["ROT", "ROT"], ["DUP", "R@"], ["U<", "+"], ["<", "+"], ["@", ">R"], ["SWAP", "R>"], ["C!", "DROP"], ["DUP", ">R"], ["C@", "OR"], ["C@", "="], ["DUP", "C@"]], "swapi": 1, "sysc": 0, "t2hot": 1, "t2wide": 1, "tag2": 1, "tail": 0, "tailpn": 1, "tfind": 1, "thinhdr": 1, "threads": 3, "tos": 1, "tracer": 0, "varcall": 1, "varslot": 0}
{"abortif": 0, "align1": 0, "alignfn": 1, "alignhot": 2, "bss": 1, "bytehdr": 1, "compiler": 0, "d256": 0, "doesfar": 1, "dskew": 1, "enc": "cv8", "escape": 0, "factor": 3, "fbuf": 0, "fold": 1, "folds": ["@", "SWAP", "+", "AND", "DROP", "OR", "LIT", "!", "LSHIFT", "RSHIFT"], "fsys": 2, "gotodup": 0, "guard": 0, "hotcalls": 8, "hotinl": 0, "ipaclone": 0, "jit": 1, "jitinl": 0, "jitk": 0, "jitloop": 0, "jitos": 0, "jittail": 0, "jitx": 1, "kfast": 1, "kinput": 1, "klookup": 0, "knumber": 0, "kstack": 0, "lean": 1, "lto": 0, "msc": 0, "nocet": 1, "nocrossjump": 0, "nogcse": 0, "noinls": 0, "noreorder": 0, "opbody": 1, "opcall": ["@"], "opinline": 1, "ops10": ["?BRANCH8", "(LOOP)", "I", "(+LOOP)", "(DO)", "(LEAVE)", "+!", ">?BRANCH8", "<?BRANCH", "=?BRANCH8", "?NBRANCH8", ">?BRANCH", "0<?BRANCH8", "DUP?BRANCH8", "PLACE", "?DUP", "<?BRANCH8", "OVER?BRANCH8", "(?DO)", "?NBRANCH", "<>?BRANCH8", "<>?BRANCH", "=I?BRANCH", "EXECUTE", "FILL", "BRANCH8", "SCAN", "HASH", "(>NUMBER)", "TABS>BL", "=I?BRANCH8"], "opt": "Os", "peel": 1, "regpin": 0, "rtempty": 0, "rtfuse": 0, "rtimm": 1, "rtiplus": 0, "rtloop": 2, "rtloopall": 0, "scale": 0, "sharedcall": 1, "skippad": 0, "spec": ["loc", "tiny", "small", "imm"], "supers": [["DUP", ">R"], ["C@", "@"], ["C@", "OR"], ["DROP", "UM*"], ["NEGATE", "NEGATE"], ["RSHIFT", "@"], ["DUP", "R@"], ["R>", "="], ["ROT", "ROT"], ["@", "RSHIFT"], ["C@", "DUP"], ["+", "DROP"], ["DUP", "C@"], ["<", "+"], ["XOR", "C!"], ["R>", "U<"], ["C@", ">R"], ["@", ">R"]], "swapi": 1, "sysc": 0, "t2hot": 1, "t2wide": 1, "tag2": 1, "tail": 0, "tailpn": 0, "tfind": 1, "thinhdr": 1, "threads": 3, "tos": 1, "tracer": 0, "varcall": 1, "varslot": 0}
```
