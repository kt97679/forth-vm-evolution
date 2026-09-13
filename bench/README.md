# The benchmarks

Four workloads, because no one of them answers the question on its own,
and the differences between them turned out to be the most interesting
result in the project.

| script | what it runs | who can take part |
|---|---|---|
| `kernel-compile.sh` | cross-compile `kernel.4` into a new image | the RelF-descended ladder |
| `corpus-run.sh` | the shared 616-case ANS CORE corpus | everything, including SOD32 |
| `loop-bench.sh` | `loop.fth`, nested counted loops over stack arithmetic | everything, including SOD32 |
| `parse-bench.sh` | `parse.fth`, 4000 lines of interpreted arithmetic | everything, including SOD32 |

Every one of them gates on correctness before it times anything.
`kernel-compile.sh` requires the produced image to be byte-identical to
the reference, so a stage that is fast because it is quietly wrong is
excluded by the same run that measures it. The others require the
end-of-run sentinel and zero failing cases.

All of them report the **minimum** of several interleaved repetitions,
not the mean. Every source of noise on a shared machine adds time, so
the fastest run is the least contaminated one; a mean would mostly
measure the neighbours. Repetitions are interleaved across stages rather
than run back to back, so a machine that drifts perturbs every stage
alike instead of penalising whichever went last.

## Why SOD32 is not in the kernel-compile table

SOD32 does cross-compile itself, in about 39 ms. But it compiles its own
`kernel.4th`, which is a different word set from `kernel.4`, so the two
numbers measure different amounts of work. Putting them in one column
would be a straightforward misrepresentation. The corpus and the two
micro-benchmarks are the workloads where the source text is identical
byte for byte, and that is where the cross-family comparison belongs.

## The result that reframes the others

Measured at 4-byte cells, against SOD32:

- **corpus** (compile several hundred definitions and run them): SOD32
  is about **2x faster** than every stage in the ladder.
- **loop** (almost pure inner interpreter): the ladder is **1.3 to 1.9x
  faster** than SOD32.
- **parse** (interpret 4000 lines; no compiling, no loops): SOD32 is
  about **2.9x faster**.

So the two families win different benchmarks, and the reason is not the
encoding. SOD32's advantage is in the OUTER interpreter - parsing,
dictionary search, number conversion - and it is large enough to decide
any whole-system workload. The encodings in this repository made the
INNER interpreter faster, which the loop benchmark shows and which the
corpus result completely hides.

The practical lesson for the article is that "the VM got faster" and
"the system got faster" are different claims, and a whole-system
benchmark cannot distinguish them. It is the same mistake as quoting the
shell workloads: a number that is real, and about something other than
what it is being used to argue.

## Does the choice of benchmark change the answer?

Mostly no, and that is worth knowing before arguing about which workload
is the right one. All four, at 4-byte cells, relative to the cell engine:

| stage | kernel | corpus | parse | loop | spread |
|---|---|---|---|---|---|
| s0-cell | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| s1-sod16 | 1.134 | 1.229 | 1.253 | 1.098 | 0.155 |
| s2-cpt16 | 1.111 | 1.116 | 1.178 | 1.161 | 0.067 |
| s3-cpt16f | 1.043 | 1.076 | 1.089 | 0.950 | 0.139 |
| s4-cv8 | 0.983 | 1.025 | 1.015 | 0.957 | 0.068 |
| s5-cv8spec | 0.817 | 0.772 | 0.721 | 0.807 | 0.096 |

The ordering is the same in every column with one exception - the loop
benchmark puts SOD16 ahead of CPT16, where the other three reverse them -
and the spread across four very different workloads never exceeds 0.16.
Every column says SOD16 is a speed regression on the cell engine, that
CV8 roughly breaks even, and that the specialisations are the only
change worth more than a few percent.

The reason the columns agree is that every one of these workloads is
Forth code running on the VM. The parser, the dictionary search and the
compiler are all compiled Forth, so a faster inner interpreter speeds
them up too. Within one family - one kernel.4, one word set - there is
no such thing as a workload that avoids the encoding.

The corollary is that the earlier SOD32 result is not a benchmark-choice
problem either. SOD32 wins the corpus because kernel.4th finds words
faster than kernel.4 does, and no choice of workload will separate that
from the encoding, because the two systems do not share a kernel. Only a
same-kernel comparison can isolate an encoding, and SOD32 cannot be part
of one.
