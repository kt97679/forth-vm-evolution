# The after-seed-62 batch - apply in this order (against master after Iteration 393)

Prepared at Iteration 391 while seed 59 ran: re-measuring designs before they enter the fast end (the owner,
Iteration 391; results/review-methodology-386.md, 2a). Waits for seed 62's processing (Iteration 393: renamed
from after-seed-60) so that seed 60 - the anchoring test - and seeds 61-62, its replicates, all run on the
evolver of seeds 53-59: a change of evolver between them would be read as run-to-run spread.

| # | patch | what it does |
|---|---|---|
| 1 | fastgate-after-seed62.patch | evolve.py: a child whose speed is under the fast gate - 5% above the 20th fastest design alive so far - is measured again, the same rounds on the engine as built, and its speed is the geometric mean of the two (speed1 and speed2 kept in its record; memory and size the first measurement's). The fast end's in-run speeds were ~10% optimistic, designs admitted on lucky draws (a 3% noise, the best of thousands); twice the rounds where admission is decided. `--fastgate N` sets the 20; 0 turns it off. |
| 2 | jithelp-after-seed62.patch | The gene jithelp (Iteration 344's draft, results/drafts/jithelp-wip.patch, unchanged): the C primitives the outer interpreter stops at, called from native code (st_call). The owner, Iteration 397: try it - out again if the fronts show it useless. |
| 3 | jitre-after-seed62.patch | The gene jitre (Iteration 346's draft, results/drafts/jitre-wip.patch, unchanged; needs jithelp): a callee the JIT cannot translate run by the interpreter from native code, not refused. The same decision. |
| 4 | bfind32-after-seed62.patch | Open item 0f (Iteration 399, results/bfind32-fault-399.md): bf_walk's signature and its mask 64 bits at either width - they were UNS64, the cell, 4 bytes at 4-byte cells, so a name of 4 to 7 characters matched the newest of its length and first three (seed 59: 34 of its front dead on the corpus at 32 bits). engines-check.py: the four bfind variants at tos 0 - on s6's TOS engine they had built no bf_walk - and at 4-byte cells too. No 64-bit engine changes: UNS64 is uint64_t there. |
| 5 | tail32-after-seed62.patch | Iteration 400 (results/fail32-400.md): no tail design had ever built at 4-byte cells (seed 58: 401 of 401 "engine did not compile"). build_tail preprocessed with CC(g), EVOLVE_CC's -m32 left out - an x86-64 engine (8-byte cells, __int128) for gcc -m32 - now CCV(g), and each of its failures keeps the tool's first error (why(r), as build's); behind it, the i386/ARM SYSCALL's local label sysc_done, which gen-tail.py took for a handler, gone (the same branches without it - no 64-bit change). tail_offenders reads i386's call forms too: it read only x86-64's, so clang's calls went unseen and its engine grew the C stack and died on the corpus - now it fails as it is, 'tail calls not jumps', clang making i386's dispatches jumps only under musttail (tailpn). engines-check: the tail variants at 4-byte cells too, but that one. |
| 6 | musttail-after-seed62.patch | Iteration 401 (results/fail32-400.md): musttail on every clang tail engine, not only with preserve_none (tailpn) - gen-tail.py --musttail. A tail engine is right only if every dispatch is a jump: at 8-byte cells clang's optimizer made them, at 4-byte cells (the five on the stack) none - seeds 58 and 59's 160 clang tail designs without tailpn failed there. tailpn is preserve_none alone now, the trade-off; musttail is the guarantee. GCC's left to its optimizer, which makes them at both widths (its musttail needs GCC 15). engines-check: clang's tail variant at 4-byte cells too. |
| 7 | bfindtos-after-seed62.patch | Iteration 402: bfind built in TOS designs. A name's walk down a thread is one macro, NAME_WALK (engine/vm-lab.c) - bf_walk's in a bfind design, else the plain loop - taken by THREAD-FIND and (FIND) and by tools/gen-tos.py's TOS bodies of them, which, written before the gene, had the plain walk: bfind was inert in every TOS design (42 of seed 59's front carry it so). engines-check: two bfind variants on s6 itself (tos), each checked built - its engine not the same without bfind - at 8 bytes, and alive at both widths. |
| 8 | jitret-after-seed62.patch | Iteration 404 (the owner: try it): the gene jitret - the JIT's EXIT leaves a native word by pop %rcx; jmp *%rcx, not ret (engine/jit.c, EXIT's stencil copied with its ret so made). ret is predicted by the return predictor, the last 32 or so calls; the JIT's ackermann nests past 250. An indirect jmp is predicted by its targets' history. A gene: the search weighs it on every workload. engines-check: the JIT with jitret. |
| 9 | tailipa-after-seed62.patch | Iteration 405, found by the batch's rehearsal: at 32-bit x86 GCC gave the two-bit tag's shared call path, t2call - a static function reached only by direct calls - a convention of its own, arguments in registers, so its incoming stack was too small for the five a dispatch passes and its tail call stayed a call: every GCC tail design with tag2 "tail calls not jumps (t2call)" at 32 bits (GCC 13.3, the laptop's). gen-tail.py: every handler noipa there (TC_NOIPA, empty for clang and off i386 - no other engine changes). engines-check: tail calls on the two-bit tag, at both widths. |
| 10 | frozen-after-seed62.patch | Iteration 409 (the owner: the simplicity review, results/drafts/simplicity-proposal-408.md): genes the search no longer varies - bytehdr, doesfar, thinhdr, varcall, bss and lean held on, msc and scale at 0, in every design the search makes (evolve.py's FROZEN, applied by require() at get(), now always; mutation no longer picks them). Hand-made designs keep their own, so s6 and the stages are unchanged; with varcall and doesfar on, no reach-limit deaths. tail not frozen: judged after seed 63. |
| 11 | iplustag-after-seed62.patch | Iteration 412: rtiplus fires on the two-bit tag. Its (I, +) -> I+ entry in the run-time fuser's SUPER-TABLE holds one-byte codes on the tag, as the loop tables do; I+, never used by the image's own code, ranked low and was escaped, so the converter dropped the entry and the fusion never fired (seed 60's 4ac602c8bd: loop's I, a fifth of its dispatches, unfused with rtiplus on). tools/layout.py pins I+ where the table carries it - as Iteration 176 pinned IMM-OPS's keeping forms. Only designs with rtiplus change. |
| 12 | bigprog-after-seed62.patch | Iteration 416 (the owner: programs past 4 MB supported): plain CV8 at byte headers reached 2 MB with a call, 4 MB with a header link and 2 MB with a DOES> word (the two-bit tag reaches 1 GB with all three). Now: a call past reach compiles as the body's address and (FAR), which puts it on the return stack and returns there - the callee sees its caller's return address (cv8.4; Iteration 417, in place of 416's EXECUTE, 80 bytes less); a fourth link form, 29 bits (cv8b.4, the engine's PREVNFA and bf_prev, the converter); the far DOES> call counts cells - its tail is aligned - so 22 bits reach 32 MB, 16 at 4-byte cells (cv8.4, the engine's and SPN's DODOES, the converter). Within the old reaches every form and byte is as before; the overlays' new code costs a plain-CV8 image 104 bytes (s6 9,161 to 9,265). engines-check: two programs past 4 MB on s6, on the tag and at 4-byte cells. |
| 13 | dumpcheck-after-seed62.patch | Iteration 417: tools/build-stages.sh stops when an overlay does not load - the load messages before each dump checked for evolve.py's DUMP_ERRORS, as its dump_guard checks a design's kernel variants. An undefined word (NIP, Iteration 416) had left a dump, then an s6 that crashed, and the build went on; with this, a cv8b.4 given `: ZZX 1 NIP ;` stops the build: "k64-b.txt - an overlay did not load: Undefined word NIP". |

    git apply results/applied-after-seed62/fastgate-after-seed62.patch
    git apply results/applied-after-seed62/jithelp-after-seed62.patch
    git apply results/applied-after-seed62/jitre-after-seed62.patch
    git apply results/applied-after-seed62/bfind32-after-seed62.patch
    git apply results/applied-after-seed62/tail32-after-seed62.patch
    git apply results/applied-after-seed62/musttail-after-seed62.patch
    git apply results/applied-after-seed62/bfindtos-after-seed62.patch
    git apply results/applied-after-seed62/jitret-after-seed62.patch
    git apply results/applied-after-seed62/tailipa-after-seed62.patch
    git apply results/applied-after-seed62/frozen-after-seed62.patch
    git apply results/applied-after-seed62/iplustag-after-seed62.patch
    git apply results/applied-after-seed62/bigprog-after-seed62.patch
    git apply results/applied-after-seed62/dumpcheck-after-seed62.patch

Its cost, from seed 58's evaluations replayed through the gate: 1,121 of 24,885 measured children (4.5%) under
it, their evaluations 4.4% of the evaluation time - an upper bound on the added time, the second measurement
having no build and no 32-bit pass. The 32-bit fast end is not gated: a later step, if the first run with this
shows it worth it. What to look for in that run: `review-checks.py curse` on its report - the fastest tenth's
re-measured / in-run ratio down from seed 58's 1.112.

Tested at Iteration 391, in a scratch clone of master: fast_gate() over 30 alive designs gives 1.05 x the 20th
fastest, None with fewer alive and with --fastgate 0; a miniature run (--pop 6 --gens 2 --rounds 1 --fastgate
3) measured 3 of its 28 designs twice - 524fef96b3 0.2264 then 0.2547, 12.5% apart - each record's speed exactly
the geometric mean of its two and of its workloads' figures, its memory the first measurement's, generation 0
(no gate yet) once; exit 0.

With it applied: run-tests.sh PASS - no regressions; evolve.py --validate 7 of 7 IDENTICAL; test-jail.py PASS. On a fresh clone of
master it applies, and lab/evolve/evolve.py is then byte for byte the tested file.

The second and third, at Iteration 397: applied in order after the first on a fresh clone, cleanly. Seed 58's
fastest, 1b5ac698ce, built with jithelp, jitre, jitimg and jitvar on: both expressed, alive, 40,565 bytes against
its recorded 36,021 (the design as recorded rebuilt to exactly that). What they buy, by jitleft.py's deterministic
counts - the dispatches the JIT leaves to the interpreter, without and with: kernel 989,120 / 987,090 (53.7% /
53.6%), corpus 4,057,836 / 4,054,591, bubble 151,968 / 129,788 (2.0% / 1.7%), fib, loop and ackermann unchanged
or nearly. Little, as Iteration 346 had found (INTERPRET stops at (FIND), PARSE-WORD at +!); a 1-round timing
here (0.2369 / 0.2044) is inside this VM's noise. The search weighs them; the fronts after seed 62 decide.

All three, tools/batch-check.sh at Iteration 397: PASS - 3 patch(es) applied to a fresh clone of 6268b51 Iteration 397: the owner's decisions - foo; run-tests: PASS - no regressions (exit 0); validate: 7 of 7 IDENTICAL (exit 0); jail: PASS (exit 0)

The fourth, tested at Iteration 399 (results/bfind32-fault-399.md): seed 59's 708757c03f and 686ae7cd5f, built as
eval32 builds them, died on the corpus at 2DUP's test on master's engine and live with the fix; engines-check's four
bfind variants at tos 0 and 4-byte cells died the same way on master's engine. With all four applied: PASS - 4 patches on a fresh clone of 0165837: run-tests PASS, validate 7 of 7 IDENTICAL, jail PASS.

The fifth, tested at Iteration 400 (results/fail32-400.md): on master, seed 58's tail designs 9483791a8e, 4bdb2d8bb3
and 272c47406f died at 4-byte cells on `'__int128' is not supported`; with the preprocessing by CCV(g), on undeclared
H_sysc_done (clang) or a link failure (GCC); with the label gone, all three live, as do engines-check's GCC tail
variants and clang's with preserve_none - clang's without it died on the corpus, unseen calls; with i386's call forms
read, it fails as "tail calls not jumps". With all five applied: PASS - 5 patches on a fresh clone of 0092bee: run-tests PASS (engines-check 78 paths), validate 7 of 7 IDENTICAL, jail PASS.

The sixth, tested at Iteration 401: with patches 1-6, seed 59's clang tail designs a973c305bc and 0136e7294a (no
tailpn) and its GCC one f510231b27 live at 4-byte cells, and engines-check's clang tail variant without preserve_none
builds and lives at both widths. With all six applied: PASS - 6 patches on a fresh clone of de0b64f: run-tests PASS (engines-check 79 paths), validate 7 of 7 IDENTICAL, jail PASS.

The seventh, tested at Iteration 402: on master s6 with THREAD-FIND builds the same engine with bfind as without it; with
patches 1-7 the engines differ at 8- and 4-byte cells (THREAD-FIND on CV8, (FIND) on the two-bit tag), all alive, and
the same design built twice without bfind is identical. With all seven applied: PASS - 7 patches on a fresh clone of befd1b6: run-tests PASS (engines-check 83 paths), validate 7 of 7 IDENTICAL, jail PASS.

The eighth, tested at Iteration 404: the JIT design with jitret built, alive, its engine not the one without; measured
here against s6 on the six workloads, ackermann -26%, fib 0, bubble +9%, loop +6% (results/jitret-404.md). With all
eight applied: PASS - 8 patches on a fresh clone of c397f25: run-tests PASS (engines-check 84 paths), validate 7 of 7 IDENTICAL, jail PASS.

The ninth, found and tested at Iteration 405 by the batch's rehearsal (results/rehearsal-405.md): seed 59's cd9d470f51
with a GCC tail engine on the two-bit tag died at 32 bits as "tail calls not jumps (t2call)" with patches 1-8; with
patch 9 it and two more live at both widths. With all nine applied: PASS - 9 patches on a fresh clone of 789364b: run-tests PASS (engines-check 86 paths), validate 7 of 7 IDENTICAL, jail PASS.

The tenth, tested at Iteration 409: a short free run here with patches 1-10 (pop 16, one round, both widths, noevolved, no tag-2 requirement), to generation 13: 222 designs, 7 hand-made; status {'ok': 222}; 32-bit failures none; designs the search made off a frozen value: 0. With all ten applied: PASS - 10 patches on a fresh clone of 50942b8: run-tests PASS (engines-check 86 paths), validate 7 of 7 IDENTICAL, jail PASS.

The eleventh, tested at Iteration 412: 4ac602c8bd with rtiplus on - the loop's dispatches 20,031,683 to 16,032,016, I's 4,000,036 to 37; built and alive with and without it. With all eleven applied: PASS - 11 patches on a fresh clone of ba83322: run-tests PASS (engines-check 86 paths), validate 7 of 7 IDENTICAL, jail PASS.

The twelfth, tested at Iteration 416 (results/bigprog-416.md): big1 and big2 refused on plain CV8 on master, right on all five builds with patches 1-12. With all twelve applied: PASS - 12 patches on a fresh clone of 911e26a: run-tests PASS (engines-check 89 paths, the programs past 4 MB among them), validate 7 of 7 IDENTICAL, jail PASS.

The twelfth revised and the thirteenth, tested at Iteration 417 (results/rehearsal-417.md): the far-call tests and the programs past 4 MB on s6 at both widths; seed 58's front sampled, 8 of 8 alive at both widths; a short free run, designs 127 | by encoding {'cell': 1, 'sod16': 1, 'cpt16': 4, 'cv8': 112, 'tag2': 9} | status {'ok': 127} | 32-bit failures none | off a frozen value 0. With all thirteen applied: PASS - 13 patches on a fresh clone of 1a37de3: run-tests PASS (engines-check 89 paths), validate 7 of 7 IDENTICAL, jail PASS.
