# Five wrong answers: the gene opcall (Iteration 173)

Seed 40's five corpus deaths are in its db with their genomes (status 'died:
corpus'): ee0eff671a, 8dff2a3647, 8587e5a5c1, 9586059a75, f7dc8437ff - all
JIT designs with opcall (X;CALL: an operation and the call after it, one
opcode). Reproduced (results/drafts/opcall-repro.py, seed 40's code):
f7dc8437ff (opcall 1+) is right with the JIT off or opcall empty, wrong with
tracer or jitinl off; 9586059a75 (opcall DROP) is right only with opcall empty
- the JIT off does not help. Both restart: "Welcome to Forth" again mid-corpus,
while the corpus defines EMPTY-STACK (lines 11-12) and } (32-34) - the
run-time compiler's fusion, or the JIT's X;CALL. The gate kills them (5 of
~35,000); next: trace a restart with the tracer.
