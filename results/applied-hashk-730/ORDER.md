# hashk - applied at Iteration 730 (results/pending until then; batch-check PASS on b9f60491)

One patch, `hashk.patch`: the gene hashk (results/drafts/demoscene-ioccc-727.md, after the demoscene's crinkler) - a
name's chain ((v * 18835) >> 8) & (chains - 1), v kernel.4's HASH; one constant for every design and chain count
(results/drafts/hashk-table-728.py). forth/cv8-hashk.4's HASHK in every dump (evolve.py: the dump's boot, the base dump,
setup's copies; the dump guard not counting it twice); tools/layout.py --hashk K makes HASHK's body HASH's and threads
the image by it, and drops HASHK always; the engine's hashes by -DHASHK=K - vm-lab.c's CHAIN in L_x_hash and (FIND),
tools/gen-msc.py's and tools/gen-tos.py's copies; export-genes.py lists --hashk in G-NOT-YET (cross-cv8.4's THASH is the
next patch); lab/evolve/GENES.md's row.

Checked on a scratch clone of 0a73200f's successor (results/drafts/hashk-gene-729.py, the Iteration 729 PROGRESS entry):
the gene off - run-tests PASS, validate, engines-check 113 of 113, the 68 stage images and the ten roles' 40 engines and
images byte for byte (pack-designs.py against results/drafts/designs-sha256-718.txt); the gene on - the ten roles at
8-byte cells, every workload's output the same, the corpus's instructions 0.914-0.994 of off, parse's 0.833-1.000; three
at 4-byte cells likewise. Then batch-check on master, `git apply`, the stages rebuilt.

Apply, from the top of the tree:

    git apply results/applied-hashk-730/hashk.patch
