# Programs past 4 MB (Iterations 415-416, the owner)

Every design has the same 16 MB of memory (MEMSIZE); what differed is how far its code reaches within it. Two programs
that grow the dictionary past 4 MB (results/drafts/bigprog-gen-416.py): big1 - calls across 4.9 MB of dictionary (100
words, each followed by 48 KB of ALLOT), a DOES> child far from its defining word, variables, EXECUTE (answer 209); big2 -
a DOES> defining word past 4 MB (answer 5). Run by results/drafts/bigprog-416.py.

**Before** (master): on the two-bit tag both right - its calls, header links and DOES> calls all reach 1 GB. On plain CV8
(s6, seed 58's 09de03f091, s6 at 4-byte cells) both refused. At byte headers (scale 0) three reaches: a call 2 MB (21
bits - the one-byte hot calls hold the top first bytes; the 4 MB I first told the owner was wrong), a header link 4 MB
(22 bits) - a gap like `CREATE BUF 5000000 ALLOT` broke it - and a DOES> call 2 MB.

**The fix** (results/pending/bigprog-after-seed62.patch, the batch's twelfth). Calls: past reach, the body's address as a
literal and EXECUTE (cv8.4's FAR,; CALL1, the forms in reach) - any distance. A first try compiled EXECUTE as a
primitive's opcode; in this kernel it is a colon word, and what followed a far call went missing - FAR, compiles it as
COMPILE,8 would. Links: a fourth form, tags 0xE0-0xFF, four bytes, 29 bits (512 MB); the three-byte form keeps
0xC0-0xDF and 21 bits, so every link an image holds is as before (cv8b.4's LINK-LEN, LINK, and NEXT-NFA8; the engine's
PREVNFA and bfind's bf_prev; the converter's linklen and linkbytes). DOES>: the far DOES> call counts cells, its tail
being aligned - 22 bits reach 32 MB at 8-byte cells, 16 at 4 (cv8.4's !CALL and (;CODE)8; the engine's and SPN's
DODOES; the converter's DOES> code field). Another try forgot that this kernel has no NIP: the overlay failed to
compile, and build-stages.sh built on, a crashing s6 - open: it should stop there.

**After**: big1 209 and big2 5 on s6, on seed 58's 09de03f091, on seed 60's 4ac602c8bd and 5ee5c38165 (the tag, the
JIT) and on s6 at 4-byte cells. engines-check runs the two on s6, on the tag and at 4-byte cells - on master they fail.
batch-check, the twelve: PASS - 12 patches on a fresh clone of 911e26a: run-tests PASS (engines-check 89 paths, the programs past 4 MB among them), validate 7 of 7 IDENTICAL, jail PASS.

**The cost**: the overlays' new code in every plain-CV8 image - s6's 9,161 bytes to 9,345 (+184) at 8-byte cells, 8,257
to 8,441 at 4. Tag-2 images unchanged. **Limits left**: memory 16 MB by default (RELF_MEMSIZE raises it, to 256 MB);
on plain CV8 a DOES> word's code within 32 MB (16 at 4-byte cells); a link 512 MB; a call, any distance.
