# The final batch rehearsed on plain CV8 (Iteration 417)

The after-seed-62 batch's thirteen patches in a scratch clone - patch 12 leaner (the far call by (FAR), below), patch 13
new (the stage build's overlay check) - built, then as the earlier rehearsal (results/rehearsal-405.md), aimed at what
seed 63's free run leans on: plain-CV8 designs, whose calls, links and DOES> forms patch 12 changed.

**The test programs on s6, at 8- and 4-byte cells** (results/drafts/farcall-tests-417.py): the two past 4 MB (209, 5) and
three around a far call - an operation, a literal and SWAP after it (the cases that had found 416's first try wrong):
`s6                   big1 ok; big2 ok; plus3 ok; two ok; swap ok`  
`s6 at 4-byte cells   big1 ok; big2 ok; plus3 ok; two ok; swap ok`  

**Seed 58's front - all plain CV8 - sampled by size**, each evaluated as a run does, at both widths
(results/drafts/rehearsal-417.py): 8 of 8 alive at both widths.

**A short free run** (pop 16, one round, both widths, no tag-2 requirement), stopped at generation 7 (results/drafts/
rehearsal-db-417.py): designs 127 | by encoding {'cell': 1, 'sod16': 1, 'cpt16': 4, 'cv8': 112, 'tag2': 9} | status {'ok': 127} | 32-bit failures none | off a frozen value 0.

**The cost, now**: (FAR) - the target's address to the return stack, then EXIT goes there, so the callee sees its
caller's return address as from a call - in place of 416's EXECUTE looked up by name: s6's image 9,265 bytes at 8-byte
cells (9,161 on master; 9,345 with 416's version), 8,357 at 4 - 104 bytes, not 184.

**Patch 13**: tools/build-stages.sh checks each dump's load messages for evolve.py's DUMP_ERRORS. A clean build passes it;
cv8b.4 given `: ZZX 1 NIP ;` stops it - "k64-b.txt - an overlay did not load: Undefined word NIP".

batch-check, the thirteen: PASS - 13 patches on a fresh clone of 1a37de3: run-tests PASS (engines-check 89 paths), validate 7 of 7 IDENTICAL, jail PASS.
