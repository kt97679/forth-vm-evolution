# hashk in the self-hosting compiler - applied at Iteration 731 (batch-check PASS on 1e245e71)

One patch, `hashk-cross.patch`, on 730's hashk: forth/cv8-hashk.4's word renamed HASH8 (tools/layout.py's X8 rule skips
it - its own swap, with --hashk only, as before); lab/evolve/export-genes.py writes G-HASHK (the K, 0 off) and names
cv8-hashk.4 among a hashk design's overlays where HASH is no engine op (ops10.json's [name, op] pairs), --hashk out of
G-NOT-YET; forth/cross-cv8.4's THASH multiplies by G-HASHK when it is not 0 - the self-built image's HASH8 swapped into
HASH by the cross compiler's own X8 rule; stages/s6-genes.4 written again (G-HASHK 0); GENES.md's row.

Checked on a scratch clone (results/drafts/hashk-cross-731.sh): smallest (the Forth HASH), portable-fastest (HASH an
op, klookup, the cached top) and small-jit (the JIT) with hashk on, exported and shipped by tools/selfhost-ship.sh
STRICT=1 - each self-built at 8- and 4-byte cells, A = B and the evolver's gate, `make selfhost selfhost32` byte for
byte, small-jit's JIT layout too; validate after s6's genes. Then batch-check, `git apply`, the stages rebuilt.

Apply, from the top of the tree:

    git apply results/applied-hashk-cross-731/hashk-cross.patch
