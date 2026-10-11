# The gene pgo - a draft (Iteration 200)

results/drafts/pgo-draft.patch, on the two after-seed-42 patches: at the end
of build(), the engine compiled again - instrumented and hosted (libgcov
writes the profile through the C library), trained on the corpus with the
design's image in a work directory of its own, then freestanding with
-fprofile-use under the same output name. The I/O functions (t_fgetc,
full_read) differ hosted and freestanding, so their profiles mismatch:
-Wno-error=coverage-mismatch leaves them out, the interpreter keeps its.

Measured on the development VM (2 rounds; sizes exact):

| design | pgo=0 | pgo=1 | corpus | fib | bubble | sieve (held out) |
|---|---|---|---|---|---|---|
| 0ceb043115, the smallest | 1.352 | 1.413 | 1.47 -> 1.32 | 1.41 -> 1.56 | 1.32 -> 1.51 | 1.26 -> 1.33 |
| d99e3d9ed9, the knee (JIT) | 1.032 | 1.075 | 0.51 -> 0.53 | 1.51 -> 1.50 | 1.17 -> 1.49 | 1.38 -> 1.31 |
| d9247d19b0, the fastest | 0.202 | died: training SIGSEGV | | | | |

The profile fits its input: the corpus 10% faster, the loops and calls 11-27%
slower - the corpus marks their handlers cold, and GCC lays the one big
interpreter function out by it. Worse in all, so not in the batch.

Next, if pursued: train on a mix of the selection workloads, shortened (the
objective is theirs; the held-out workloads say whether it generalises); build
the training engine -no-pie (and -static) - the JIT design's crash is likely
its code placed where the hosted, position-independent build put it.

## The second attempt (Iteration 201, the owner) - four variants, all slower

The draft now trains on every selection workload (the first attempt: the
corpus alone), builds the training engine -static -no-pie like the real one,
and leaves out a workload the hosted training engine cannot run (the fastest
JIT design's kernel: SIGSEGV), three trained at least. Speed (VM, 2 rounds,
pgo=0 -> pgo=1, each pair in one session):

| variant | 0ceb043115 (smallest) | d99e3d9ed9 (knee, JIT) | d9247d19b0 (fastest, JIT) |
|---|---|---|---|
| A. the corpus (first attempt) | 1.352 -> 1.413 | 1.032 -> 1.075 | training crashed |
| B. each workload once (single) | 1.368 -> 1.433 | 1.070 -> 1.078 | training crashed (kernel) |
| C. each as measured (long); -fno-vpt, no hot/cold split | 1.352 -> 1.499 | 1.076 -> 1.172 | 0.204 -> 0.204, +768 bytes |
| D. C, block order kept, no tail duplication | 1.365 -> 1.522 | 1.062 -> 1.169 | 0.206 -> 0.213, +768 bytes |

B gained fib on the knee (1.46 -> 1.35) and lost bubble on both (13-20%); C
and D lost on every workload, held-out ones too. A profile closer to the
measurement made it worse, and keeping GCC's block layout did not help: the
cost is in how GCC compiles the 10 KB computed-goto function from a profile -
its register allocation, or the dispatch jumps merged, which the genes
nocrossjump and nogcse exist to prevent - not in the training set.

Not a gene, not in the batch. The draft keeps variant D's code. If ever tried
again: on the laptop's GCC and Zen 4 (an A/B over a dozen front designs, 6
rounds), or with Clang, whose profile use differs.
