# The plain design's dump with hashk, chainorder or numfirst - applied at Iteration 735 (batch-check PASS on ca87c108)

One patch, `plain-dump.patch`, lab/evolve/evolve.py: found by the rehearsal's short run (results/rehearsal-735.md) - a
design of no other part (cv8 and byte headers alone: tools/build-stages.sh's k64-b.txt and k32-b.txt, cv8.4 and cv8b.4
only) with hashk on did not convert (no HASH8 in the dump); chainorder or numfirst would have died the same way. Such
a design with any of the three on takes a dump of its own, KW-bg.txt, made by the lab with their files (boot_files
reads no part from the name); prebuild_dumps makes it at each width. Off, the old dump still: the lab's own plain dump
differs from build-stages' in INCLUDE-BUFFER's leftover text, so not byte for byte.

Checked on a scratch clone (results/drafts/plain-genes-735.py, plain-genes-735.json): off, the image and engine the
same bytes as master's at both widths; hashk, chainorder, numfirst and all three on, the kernel, corpus, parse and apps
outputs the same as off at both widths. Then batch-check (run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS),
`git apply`, the stages rebuilt.

Apply, from the top of the tree:

    git apply results/applied-plain-dump-735/plain-dump.patch
