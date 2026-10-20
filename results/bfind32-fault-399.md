# The 32-bit corpus deaths of seed 59: bfind's signature in the cell type (Iteration 399)

HANDOFF open item 0f. Seed 59's front: 34 of 171 "died: corpus" as 32-bit engines (eval32: the design, its JIT
off, at 4-byte cells), all jit=1, scale=0, tos=0; 2,057 such in its database.

**The separator: bfind without tos.** The 34 all express bfind. Of the 44 alive with jit=1, scale=0, tos=0, 43
have bfind 0, and the one with bfind 1 (505aec3d29) does not express it - neither THREAD-FIND nor (FIND) among its
opcodes. The 42 alive with bfind 1 and tos 1 take no bfind walk at all: a TOS engine's THREAD-FIND and (FIND) are
tools/gen-tos.py's own bodies, the plain walk, written before the gene (Iteration 316).

**The cause.** bf_walk (engine/vm-lab.c) compares a candidate's count byte and first seven characters as one
masked 64-bit word, and the rest of a longer name, from the eighth character, only on a match. The word, its mask
and bf_ld64's result were declared UNS64 - the VM's cell type, uint32_t at 4-byte cells. There the signature held
the count and three characters: a name of 4 to 7 characters matched the newest word of its length and first
three, and a longer one went unchecked in its 4th to 7th. The hash (the first two characters and the length) puts
every such pair in one thread. At 8-byte cells UNS64 is uint64_t: the 64-bit engines were right, and the fix
leaves them as they were.

**The corpus case.** Both seed-59 designs rebuilt here as eval32 builds them (708757c03f, 686ae7cd5f) fail at
the corpus's line 254, `{ 1 2 2DUP -> 1 2 1 2 }`: INCORRECT RESULT (line 259 of the 1,217 the reference prints).
The tester's `->` and `}` index ACTUAL-RESULTS by `I CELLS +`, and CELLS shares its length and first three
characters with CELL+, CELL- and CELL, - so another of them answered for it. A single result is stored and read
back at the same wrong place and passes; 2DUP's is the corpus's first test with more than one result (none of the
253 lines before it has two), and its four overlap.

**The fix** (results/applied-after-seed62/bfind32-after-seed62.patch): the signature, the mask and bf_ld64's result uint64_t at
either width. With it both designs live at 32 bits - the corpus and the kernel workload, as eval32 runs them
(results/drafts/bfind32-repro-399.py).

**The check that missed it, and the one that catches it.** engines-check.py's four bfind variants (Iteration 316)
were set on s6, a TOS design, so they built no bf_walk at either width - and passed (here too: all four alive at
4-byte cells on the faulty engine). In the patch they set tos 0, and run again at 4-byte cells as eval32 builds a
design. On the faulty engine all four die at 2DUP's test, as the seed-59 designs did. With the fix they live: the batch's run-tests (engines-check: 70 paths, each built and its corpus right; tools/batch-check.sh: PASS - 4 patches on a fresh clone of 0165837: run-tests PASS, validate 7 of 7 IDENTICAL, jail PASS.).

**What it did to the runs.** Since selection at both widths (seed 57), a design expressing bfind without tos
counted at 32 bits as the slowest (Iteration 336): kept on fronts by its 64-bit objectives, out of the 32-bit
fast end whatever its speed there. Seeds 60-62 keep it - one evolver for the three; the fix applies with the
after-seed-62 batch, and seed 63 is the first run to measure those designs at 32 bits. The remote checks at 32
bits (dream, the Tegra) build the same source at 4-byte cells: the same designs die there.

**Not explained here: the 326 that did not compile at 32 bits** - seed 59's database is not in hand; the next
archive's can say whether they are another fault.

**A second finding: bfind is inert in every TOS design** - expressed (its need is only THREAD-FIND or (FIND) among
the opcodes) while nothing built differs: 42 of seed 59's front carry it so, and gene-usage counts read it as
used. Either the TOS bodies take the walk (gen-tos.py), or the gene needs tos 0 - an honest identity. Open: HANDOFF
item 4b, the simplicity review.

## Iteration 402: bfind built in TOS designs

The second finding fixed (results/applied-after-seed62/bfindtos-after-seed62.patch). A name's walk down a thread is one macro,
NAME_WALK (engine/vm-lab.c) - bf_walk's in a bfind design, else the plain loop - taken by THREAD-FIND and (FIND) and by
gen-tos.py's TOS bodies of them. On master, s6 with THREAD-FIND as an opcode builds the same engine, byte for byte,
with bfind and without it. With the patch the two differ, at 8- and 4-byte cells, for THREAD-FIND on CV8 and (FIND) on
the two-bit tag alike, and all live; the same design built twice without bfind is identical, so the difference is the
gene's (results/drafts/bfindtos-402.py). engines-check: those two variants on s6 itself, each checked built - its engine
not the same without bfind - which fails on master. batch-check, the seven: PASS - 7 patches on a fresh clone of befd1b6: run-tests PASS (engines-check 83 paths), validate 7 of 7 IDENTICAL, jail PASS.
