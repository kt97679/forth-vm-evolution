# numfirst and chainorder in the self-hosting compiler, and the processing rehearsal's fix - applied at Iteration 736 (batch-check PASS on 66aeb911)

Two patches, in this order (the owner, 735: "start with 1 and 2" - the processing rehearsed while seed 97 runs, and the
self-hosting parts the converter-only genes lacked):

1. `selfhost-genes.patch` - forth/cross-cv8.4, lab/evolve/export-genes.py, stages/s6-genes.4, lab/evolve/GENES.md:
   numfirst (733) and chainorder (732) in the self-hosting compiler; export-genes.py no longer refuses either
   (G-NOT-YET). numfirst: its file last in G-OVERLAYS (as evolve.py's dumps load it), DIGITS? and NF-FLAG in
   G-HEADERLESS, a new list G-SKIP - the definitions the translator drops (the marker; INTERPRET8 in the C form) -
   skipped by cross's scan and its `:`. chainorder: G-CHAINORDER and G-CO-HOT (chainorder-use.txt's names at least
   --chainorder-min, and their counts); every pass logs its headers, the second's give each chain's walk (the hot
   names by count, the rest newest first - layout.py's), the third lays each link to its walk's next: back sized as
   NAME,-T sizes one, forward three bytes in their own form (F0-FF; E0-FF under the tag), patched when the headers are
   down, the thread heads the walks' firsts. The link words: the chainorder file before cv8b.4 (cv8bt.4), G-TRIM8
   (LINK-LEN8, NEXT-NFA88 read as LINK-LEN, NEXT-NFA8 - the name shortened in the source as read) and G-ONCE (cv8b.4's
   later definitions skipped) - what the translator's swap gives. ITEM-START reads a forward link as three bytes (the
   JIT's layout; small-jit's first self-built image crashed on it). stages/s6-genes.4 regenerated (the new lists,
   empty). With both genes off, s6's fixed point the same bytes (8,926).
2. `curse-guard.patch` - lab/evolve/review-checks.py: `curse` printed a slice of no designs by indexing it (a front
   under ten - the rehearsal's stand-in run of 8 a generation); now "0 designs". A real run's front of hundreds never
   reached it.

Checked on scratch clones: results/drafts/numfirst-cross-736.sh (.txt) - smallest (the Forth form), portable-fastest
(the C form), small-jit (the C form under the tag, the JIT) with numfirst, each exported, shipped self-built by
selfhost-ship.sh STRICT=1 at both widths (the fixed point, the evolver's gate, `make selfhost` byte for byte), numfirst's
probe the same; results/drafts/chainorder-cross-736.sh (.txt) - the same three with chainorder, and smallest and small-jit
with chainorder, numfirst and hashk together: all shipped, the probes the translator's, parse's instructions within 1 %
of the translator's images and 0.789 / 0.943 of the self-built ones without; small-jit with hashk alone as at 731
(8,090 B). The processing rehearsal (results/drafts/process-rehearsal-736.md). Then batch-check (run-tests PASS, validate 7 of 7
IDENTICAL, the jail PASS), `git apply`, the stages rebuilt.

Apply, from the top of the tree:

    git apply results/applied-selfhost-736/selfhost-genes.patch
    git apply results/applied-selfhost-736/curse-guard.patch
