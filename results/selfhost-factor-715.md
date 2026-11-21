# The gene factor in the cross compiler (Iteration 715)

Self-hosting phase 6, the third part (after 714's VAR-OPS / INL-OPS and --guard-abort). The owner (715): "start
--factor now". forth/cross-cv8.4 now does what the translator's `--factor` does (tools/layout.py, Iteration 267):
repeated straight-line code in cold words moved into headerless bodies `[run][EXIT]` after the last word, each use a
call. It finds and chooses the runs itself, as it finds the dead words and fills VAR-OPS; only the profile-derived
word list comes through the genes, as G-HOT-INLINE does.

## How

- **The genes** (lab/evolve/export-genes.py): `G-FACTOR` (-1 under `--factor` with the tag and byte headers; layout.py
  ignores it elsewhere, and so does the cross compiler), `G-FACTOR-ANY` (`--factor-share` above 1: every word),
  `G-FACTOR-COLD` (the reference profile's words below the share; a word missing from it is kept, as there),
  `G-FACTOR-NOT` (layout.py's T2_CONSTS and DUMPTOOL, read from its source). `--factor` is out of G-NOT-YET. Genes
  written before 715 lack the four: read as 0 and empty (the ten shipped designs').
- **Pass 2** keeps every operation of the words it may factor (by final name), after the rewrites, and for every word
  whether it may be called from anywhere (sod16.py's ra_safe: its own return-stack walk before the rewrites, not strict).
- **Between passes 2 and 3** the search, layout.py's rules: a stretch of safe operations nothing lands on but its first
  (a mark, a branch's target, a loop's start); safe - no EXIT or folded EXIT form, no I, J, EXECUTE, UNLOOP or loop
  word, no pair holding one, no branch, inline cell, string or address literal, no call to a word that reads its
  caller's return address; runs of 2 to 16 operations, more than 2 bytes, balanced on the return stack (rs_walk,
  strict), recurring; taken greedily by net bytes k(len-2)-(len+1), a use never overlapping another (_free). The
  positions are merge-sorted by their runs and each run's uses read off at each length - the same set as layout.py's
  enumeration, in N log N.
- **Pass 3**: each use in a word a call (the new operation O-FB, chained - the bodies come last), checked to be what
  pass 2 kept (an abort if not); the bodies laid after the last word from the first use's operations as pass 3 has
  them, the EXIT folded as fold_exit does.
- **Compared by what both passes see**: a call or a slot by its word's ordinal; a FORWARD's or a rebound name's call
  as the word it reached (the translator compares addresses - the same); nothing host-dependent orders anything, so the
  64-bit build makes the same 32-bit image.
- Two small changes on the way, no byte of any image moved: `[']` marks its literal an address (ALIT+, b = 1 - the
  translator's relocated literals, never in a run); SPECIALISE's VF/VS keep the data word's shadow (compared by
  ordinal).

## Checked

Test designs (results/drafts/factor-variants-715.py): d727605472 and 5f7e66b12d, the fastest portable's pair, without
the fused =I?BRANCH / DUP?NBRANCH the cross compiler does not do yet (fac0000001 "va", fac0000002 "vb"), and va at
factor=3 (every word, "vc"). Run by results/drafts/selfhost-ids-714.sh (the export, the genes, tools/selfhost-check.sh,
fusetab-714.py); the translator's lines by results/drafts/factor-translator-715.py.

| design | translator: bodies, uses, runs; code smaller - bodies = net | cross compiler: the same | self-built A, 8 / 4-byte cells |
|---|---|---|---|
| va (factor=1) | 18, 66, 136; 165 - 102 = 63 B | 17, 64, 136; 159 - 95 = 64 B | 9,977 / 9,341 B |
| vb (factor=1) | 20, 72, 147; 186 - 115 = 71 B | 19, 70, 147; 180 - 108 = 72 B | 10,062 / 9,414 B |
| vc (factor=3) | 39, 158, 395; 436 - 239 = 197 B | 36, 147, 373; 399 - 217 = 182 B | 9,843 B (8-byte) |

Each: A = B on its own engine, the gate passed, VAR-OPS and INL-OPS the translator's to the byte, the probes the same;
at 4-byte cells the 64-bit build makes the same image. The runs considered are the translator's exactly where the
profile decides (136, 147); every word (vc) gives 22 fewer - words the translator reads that the cross compiler never
compiles as such (an X8 before the last, an op-body word's body). The choice is one body and two uses short of the
translator's at factor=1 (ties broken differently: the translator's heap by Python's tuple order, here the first of
equals), the net bytes within 1. run-tests PASS (the ten shipped designs and s6 self-build byte for byte).

## Left

- **The fused =I?BRANCH / DUP?NBRANCH** (and =I?BRANCH8): the fastest portable's pair's last G-NOT-YET - until then the
  gate ships portable-fastest translator-built (tools/selfhost-ship.sh, 714).
- The JIT designs with factor: none in chain C's lists expresses it with the JIT; not tried.
- The gate's speed half (the laptop, after the roles) times the self-built images against the translator's.
