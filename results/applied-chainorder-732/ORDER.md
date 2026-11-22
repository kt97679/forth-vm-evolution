# The gene chainorder - applied at Iteration 732 (batch-check PASS on aac73c5b)

One patch, `chainorder.patch`: the gene chainorder (results/drafts/demoscene-ioccc-727.md's hashk section,
chainorder-margin-731.txt) - each chain's names looked up at least 64 times in the held-out programs
(lab/evolve/chainorder-use.txt, written by results/drafts/chainorder-use-732.py) at its front, most first, the rest
newest first as before. A link to a word laid later is its own form: three bytes, tag F0-FF (tag 2: E0-FF), carved from
the four-byte form (28 and 29 bits back now); backward links as before, so a walk's common step costs what it did.
forth/cv8-chainorder.4 and cv8t-chainorder.4 in every dump with cv8b.4 or cv8bt.4: tools/layout.py --chainorder swaps
their LINK-LEN8 (the narrower reach) and NEXT-NFA88 (the forward form) in, drops them without; the engine's PREVNFA
(both header families) and bfind's bf_prev by -DCHAINORDER; lab/evolve/evolve.py's gene (CO_MIN 64), co_file, the dump
guard and setup's copies; export-genes.py lists --chainorder in G-NOT-YET (the owner, 732: the self-hosting part built
if a role takes the gene - its forward links fixed at three bytes, patched at the end); lab/evolve/test-resume.py's noise
1.0 (the gene moved the draws; at 0.6 the control no longer forked); GENES.md's row.

Checked on a scratch clone (results/drafts/chainorder-gene-732.py, chainorder-732.txt): off - run-tests, validate, the
ten roles' 40 engines and images byte for byte 718's; on - the ten roles' outputs the same at 8-byte cells, three at 4,
hashk with it on two. Then batch-check, `git apply`, the stages rebuilt.

Apply, from the top of the tree:

    git apply results/applied-chainorder-732/chainorder.patch
