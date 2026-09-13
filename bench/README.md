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

All of them unset `LD_PRELOAD` before running anything. A desktop
session that preloads a library into every process would otherwise have
it loaded into every engine being timed, which is work inside the
subject rather than around it. It showed up as noise first: on a machine
with `libgtk3-nocsd.so.0` preloaded, the 32-bit engines could not load
the 64-bit library and `ld.so` wrote a complaint per process.

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

Mostly, and with one loud exception. All four, at 4-byte cells, relative
to the cell engine, measured AFTER the hashed word list was restored -
see FINDINGS-OUTER-INTERPRETER.md, and do not mix these with any number
taken before it:

| stage | kernel | corpus | loop | parse | spread |
|---|---|---|---|---|---|
| s0-cell | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| p4-pack4 | 1.057 | 1.161 | 1.148 | 1.174 | 0.116 |
| p8-pack8 | 1.100 | 1.142 | 1.271 | 1.206 | 0.171 |
| s1-sod16 | 1.238 | 1.303 | 1.658 | 1.054 | **0.604** |
| s2-cpt16 | 1.032 | 1.026 | 1.106 | 1.022 | 0.084 |
| s3-cpt16f | 0.962 | 0.913 | 0.926 | 0.920 | 0.050 |
| s4-cv8 | 0.962 | 0.920 | 1.037 | 0.933 | 0.117 |
| s5-cv8spec | 0.802 | 0.719 | 0.863 | 0.679 | 0.184 |

Seven of the eight rows agree to within 0.18 across four unrelated
workloads, and every column puts the stages in the same order. The
conclusion does not depend on which benchmark is chosen.

**SOD16 is the exception, and the reason is instructive.** Its spread is
0.604: worst of all stages on the loop benchmark at 1.658, nearly level
with the cell engine on parsing at 1.054. Nothing else comes close to
that inconsistency.

It is the only stage whose RUNTIME-COMPILED code differs systematically
from its translated code. A SOD16 call names a word NUMBER, the table is
fixed at load, and a word defined afterwards has no number - so every
call to newly compiled code goes through the three-token FARCALL escape
instead of a one-token table call. `loop.fth` is almost entirely
runtime-compiled definitions calling each other, which is the worst case
for that. `parse.fth` spends its time inside the kernel's own words,
which were translated and do use table calls, and there SOD16's denser
image starts paying for itself in cache.

So the disagreement is not noise and it is not a benchmark artifact: it
is the escape hatch, showing up exactly where the design predicts. It is
also a cost no size model would ever have found, because it is not paid
by the image - it is paid by whatever the image compiles later.

## The two rejected designs, built
`p4-pack4` and `p8-pack8` are the tagged-nibble and tagged-byte schemes
that Iteration 157 measured in a synthetic loop and rejected without
building. Built and measured in a real engine, at 4-byte cells:

| | predicted dispatch | measured, kernel compile | measured, loop |
|---|---|---|---|
| tagged nibble | 2.05x | 1.19x | 1.15x |
| tagged byte | 1.90x | 1.17x | 1.22x |

| | modelled size | measured cells folded away |
|---|---|---|
| tagged nibble | 0.76x | 0.89x (347 of 931 primitive cells) |
| tagged byte | 0.76x | 0.86x (409 of 930) |

Three things follow, and only the first was known.

**The decision was right.** Both packed schemes are slower than the cell
engine they would replace and far behind CV8, which is 1.07 on the same
workload while being less than half the size. Nothing here reopens it.

**The reason recorded for it was wrong by about four times.** The
synthetic benchmark predicted a 90-105% penalty; the real penalty is
15-22%. `pack-bench.c`'s own header says why - its streams were sized to
stay hot, so density earned no credit, and it calls that the pessimistic
case. It was, by a factor nobody estimated.

**The nibble scheme is worse than the byte scheme on SIZE, which the
census said it was level on.** The census had them at 0.76x each. Built,
the nibble scheme folds away FEWER cells - 347 against 409 - because a
four-bit opcode only reaches sixteen primitives, and a primitive outside
that alphabet does not merely fail to pack: it ENDS the run it sits in.
With a mean run length near one, breaking runs costs more than the
narrower field saves. The nibble scheme is the denser encoding of a
sequence and the sparser encoding of this program.

That is not a subtlety a size model was ever going to catch, because the
model priced the fields and the program pays for the joins.
