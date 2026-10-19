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
| 5 | tail32-after-seed62.patch | Iteration 400 (results/fail32-400.md): no tail design had ever built at 4-byte cells (seed 58: 401 of 401 "engine did not compile"). build_tail preprocessed with CC(g), EVOLVE_CC's -m32 left out - an x86-64 engine (8-byte cells, __int128) for gcc -m32 - now CCV(g), and each of its failures keeps the tool's first error (why(r), as build's); behind it, the i386/ARM SYSCALL's local label sysc_done, which gen-tail.py took for a handler, gone (the same branches without it - no 64-bit change). engines-check: the tail variants at 4-byte cells too - but clang's without preserve_none, which then builds and dies on the corpus at 32 bits (open, results/fail32-400.md). |

    git apply results/pending/fastgate-after-seed62.patch
    git apply results/pending/jithelp-after-seed62.patch
    git apply results/pending/jitre-after-seed62.patch
    git apply results/pending/bfind32-after-seed62.patch
    git apply results/pending/tail32-after-seed62.patch

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
