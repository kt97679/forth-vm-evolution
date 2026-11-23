# The JIT designs' stack guard - queued until the series ends, after step 2 (Iteration 743)

The gap (results/drafts/data-layout2-738.txt, jit-guard-739.txt): on the JIT designs without the guard gene - today
small-jit, fastest-x86-32 and fastest-x86-64 - a runaway data-stack push in JIT code runs down through the whole engine
and native recursion leaves the fault handler no stack: status 139, nothing said, the output lost. The owner (742):
"for open questions - I don't have strong opinions, please continue as you think is most reasonable". Decided (743): no
shipped role dies that way - this fix for every JIT design without the gene, while the guard gene's variants
(results/candidates-guard-740.md) still compete for the roles by the rule in the follow-up.

The fix (results/drafts/jit-guard-slim-739.patch, rebased on step 2): for X_JIT designs without the gene, one unreadable
page at the data stack's floor (`STK_END - RSTACK_BYTES - STK_PAD - DSTACK_BYTES` - step 2's pad counted), the
interpreter's bound a page above it so it still names the overflow first, and the handler on a 16 KB stack of its own
(sigaltstack; SA_ONSTACK in the fault installers only when X_JIT is defined - every other design's engine byte for byte
as before). Measured in a scratch tree, step 2 against step 2 with this: small-jit +112 B, fastest-x86-32 +128,
fastest-x86-64 +112 at 8-byte cells (+176, +208, +208 at 4); their push loop, push recursion and native recursion 70
"segmentation fault" instead of a bare SIGSEGV, every other trap the same; best-all-round, smallest, least-memory,
portable-knee, portable-arm and portable-fastest the same bytes and traps. 739's measure: no instruction changes.

Apply it when the series ends, AFTER results/queued-layout2 (the same lines of main()):
`env BASE=results/queued-layout2 PENDING=results/queued-jitguard RECORD=1 sh tools/batch-check.sh`, then from the
repository's top:

    git apply results/queued-jitguard/jit-guard-after-layout2.patch

batch-check (743, on Iteration 742 with this batch committed, after results/queued-layout2 - 1 patch): PASS - run-tests PASS (the generators: 118
paths), validate 7 of 7 IDENTICAL, the jail PASS.

The JIT designs' engines grow by the figures above, so their records' sizes are the chain's measure-ids readings, as
for step 2's memory.
