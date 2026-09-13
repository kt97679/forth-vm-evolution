# Making a Forth VM smaller: four attempts, two of which failed

In 2004 I forked L.C. Benschop's SOD32, threw away its packed instruction
format, and replaced it with one relative offset per cell. I called the
result RelF and used it for twenty years. The point was speed: a cell
you can jump through directly beats six 5-bit subinstructions you have
to unpack.

Then I built it for 64-bit, and the deal changed.

What follows is what I tried, in the order I tried it, including the two
attempts that did not work and why. Every system named here builds,
boots, compiles its own encoding and passes the same 616-case ANS CORE
corpus; the tables come out of the repository, not out of a model.

    tools/build-stages.sh      # every engine and image, both cell widths
    tools/run-tests.sh         # the corpus on all of them
    tools/collect-results.sh   # every table below

Ratios are against the cell engine, so smaller is better. They carry one
standard error, measured across several differently-laid-out builds of
each engine - see the last section, which is about measurement and is
the part I would keep if I had to cut the rest.

---

## 1. What 64-bit did

Cell threading pays one host cell per *operation*. Move to a 64-bit host
and every operation costs eight bytes instead of four, while the program
it encodes has not changed at all. The kernel image went from 13,380
bytes to 24,320 for the same word set.

That is the whole motivation. Not "make it smaller" in the abstract, but
"stop paying twice for the same program because the host got wider" -
and, since RelF existed to be fast, without giving the speed back.

The obvious first thought is that this is SOD32's problem, and SOD32
already solved it by packing. So that is where I started.

## 2. Attempt one: pack several operations into a cell

Put several small opcodes in one cell behind a tag byte. Two variants:
4-bit opcodes, sixteen of them, and 8-bit opcodes. I had costed both in
2018 and rejected them on a synthetic dispatch benchmark that put them
at 1.90x and 2.05x. This time I built them.

Measured on kernel compilation, across three machines:

| | predicted | 8-byte cells | 4-byte cells |
|---|---|---|---|
| tagged nibble | 2.05x | 1.13 | 1.14-1.18 |
| tagged byte | 1.90x | 1.09 | 1.08-1.18 |

So the rejection was right and the reason was wrong by a factor of four.
The old benchmark's own header said why, in advance: its streams were
sized to run hot, so it measured decode cost with memory free, which it
called the pessimistic case. Pessimistic by four times, as it turned
out. The baseline it lost to was wrong too - token threading had been
recorded at 0.985, faster than cell dispatch, from a benchmark running a
32 MB stream against a 2 MB L2. That was measuring memory traffic.

The interesting failure is the other one, and only building it showed
it. On a size census the nibble and byte schemes were level, both at
0.76x. Built, the nibble scheme folds away *fewer* cells - 377 against
433 - and produces the **larger** image, 21,296 bytes against 20,848.

A four-bit opcode reaches only sixteen primitives. A primitive outside
that alphabet does not merely fail to pack: it **ends the run it is
sitting in**, and both halves then need their own tag byte. Measured on
real kernel code, the mean run of consecutive packable primitives is
about 1.3.

That is the finding. **Packing needs long runs of packable operations,
and Forth code has not got them.** Forth is calls. A size model prices
the fields and gets 0.76x; the program pays for the joins and gets 0.86x
while running 10-18% slower.

Packing was out.

## 3. Attempt two: a 16-bit token through a word table

If a cell is too wide, use a narrower unit. One 16-bit token per
operation, values below 256 are primitives, values at or above index a
table of word addresses built when the image loads. This is textbook
token threading, and the table is the obvious way to turn a number into
an address.

The image halved, 24,320 to 12,864 at 8-byte cells. And it was the
slowest system in the whole set:

    SOD16, kernel compile     1.37 (AMD)    1.36 (ARM)

Worse than the cell engine it was meant to improve on, on every machine
and every workload, by a wider margin than anything else I built.

It cost more than the table lookup, too. A SOD16 call names a word
*number*, but a compiler has an *address*, and the engine's table runs
the other way and lives in memory Forth cannot reach. So the image has
to build its own sorted copy on the heap and binary-search it on every
call it compiles. The table is also sized at load and never grows, so a
word defined afterwards has no number at all - which needed a far-call
escape opcode, and a second one for `DOES>`, whose runtime pushes a
mid-word address that no word number can name.

Compare the whole of CPT16's call compiler, below, with a page of that.

## 4. Delete the table

If the table is the problem, compute the address instead of looking it
up. Lay the words out so that a target is `base + (value << shift)` -
compressed pointers, as HotSpot does for object references. No table, no
second dependent load, and the compiler's job becomes one line:

```forth
: CALL, ( a-addr --- )
  START @ - CPT-SHIFT RSHIFT 256 + OP, ;
```

Subtract the base, shift, add the opcode band. That is the entire call
mechanism.

    CPT16, kernel compile    1.024 ±0.021 (AMD)    1.007 ±0.016 (ARM)

Exactly back to the cell engine. Not faster - *exactly* back. Deleting
the table recovers precisely what the table cost and nothing more, at
half the image size.

Two things follow. The first is the one I would tell anyone starting
this work: **logic you add to the dispatcher costs about what it looks
like it costs.** That reads as obvious now. It did not read as obvious
when the table seemed like free indirection and the measurement had not
been taken.

The second is a caveat. `s2` removes the table's dispatch cost and the
compiler's inverse-map complexity in the same step, so the 37% cannot be
split between them by these measurements. Only their sum is measured.

## 5. Attempt three: narrow the unit itself

Two lessons now point the same way. Packing fails because Forth code has
no long runs. Dispatcher logic fails because it costs what it costs. The
remaining lever is the size of the unit - not how many operations share
a cell, and not how cleverly the target is computed, but how many bytes
one operation takes.

So: a byte stream. Values under 0x80 are opcodes; 0x80 and above begin a
call whose remaining bits are an offset. No alignment, no tag bytes, no
runs required, nothing in the dispatch path but a compare and a shift.
Two bytes for a near call, three for a far one, exactly as FCode and the
JVM encode theirs.

    CV8, kernel compile    0.919 ±0.026 (AMD)    0.896 ±0.011 (ARM)
    CV8, image             11,416 bytes - 0.469x of cell threading

The first thing in the sequence that was better on both axes at once.
Here is the same definition in each encoding, dumped from the real
images at 4-byte cells by `tools/show-word.sh`:

```
: COUNT   DUP 1 + SWAP C@ ;

cell     25 9 1 93 29 41 5      7 cells x 4  = 28 bytes
token    6 2 1 23 7 10 1        7 tokens x 2 = 14 bytes
CV8      6 120 1 7 79                          5 bytes
```

In the CV8 line, `120` is an add-immediate opcode into which `LIT 1 +`
collapsed, and `79` is a folded "`C@` then return".

## 6. Then it compounds

Folding is the first of those: a primitive followed by `EXIT` becomes one
opcode, which removes a dispatch from the end of a great many
definitions. Then specialisation - the CPython 3.11 idea of giving the
common case its own opcode. Small integers, the hottest kernel words,
and immediate operands each get one.

| stage | kernel compile (AMD, 8-byte) | image | vs cell |
|---|---|---|---|
| cell | 1.000 ±0.037 | 24,320 | 1.000 |
| CPT16 | 1.035 ±0.033 | 12,864 | 0.529 |
| + folding | 0.897 ±0.027 | 12,696 | 0.522 |
| CV8 | 0.919 ±0.026 | 11,416 | 0.469 |
| + specialisation | 0.688 ±0.019 | 11,088 | 0.456 |

Worth saying plainly, because it is not the result I expected: **the
specialisations are worth more than every encoding change put
together.** CV8 alone is 0.92; the opcodes take it to 0.69. Measured by
bytes saved in the image, the three that do anything are small integers
(190), hot words (194) and immediate operands (111).

## 7. The last place cell width was still being paid

At this point the token stream is the same size at both cell widths -
the same program either way. But the 64-bit image was still 2,980 bytes
larger than the 32-bit one. Measured, that was: 1,088 bytes of
dictionary link cells, 496 of padding to align names, 660 of padding to
align the end of each code body, and the rest data.

None of that is code. It is the dictionary *header*, which the whole
encoding exercise had never touched.

So the link became a distance rather than an address, 1 to 3 bytes, with
its tag byte last so that it decodes read backwards from the name the
same way a call decodes read forwards. Names stopped being padded, code
bodies stopped being padded, and the call scale dropped to 0.

    image, 8-byte cells    11,088 -> 7,609     0.456x -> 0.313x
    image, 4-byte cells     8,108 -> 6,749     0.606x -> 0.504x

The largest single size result in the sequence, and it came from the
part of the system that is not the instruction encoding at all.

`FINDINGS-CELL-WIDTH.md` accounts for every one of the 860 bytes still
separating the two widths. 408 are data fields, which are cells because
a `VARIABLE` holds a cell. 156 are a wordlist table. The remaining 273
are seventeen inline operands that are still cell-sized and force their
bodies to align - the only part worth chasing.

## 8. What it costs

The byte-granular header is not free. The cost lands where the design
says it should: on dictionary search, because a variable-length link is
more work to walk than a cell.

| workload | AMD | ARMv7 |
|---|---|---|
| kernel compile | +0.056 | +0.047 |
| corpus | +0.086 | +0.071 |
| parse | +0.119 | +0.099 |

Reproduced across three separate builds on the AMD machine and two on
the ARM board; the corpus figure repeats to a thousandth. It is a size
optimisation that costs time, on both architectures, and anyone adopting
it should know which of the two they are buying.

So the sequence ends on a trade rather than a win. 0.31x the image, 0.73
the time on kernel compilation, and a measurably slower dictionary.

## 9. The premise I never checked

One thing remained, and it is the part of this exercise I would most
like other people to avoid repeating.

RelF existed to be faster than SOD32. That was the entire reason for the
2004 fork. So at the end I ran the two side by side - which, in twenty
years, I had never once done.

SOD32 was twice as fast as RelF on the test corpus and 2.9 times as fast
at interpreting text.

The cause took an afternoon. SOD32's dictionary is 32 hashed chains,
selected on the first two characters of a name. RelF's was a single
chain walked from the top. I had dropped the hash while changing the
link fields from absolute to relative in 2004 and never went back to see
what it cost. It costs most on *numbers*, which are never found and so
pay a complete traversal before the interpreter gives up and converts
them - and about half the tokens in a program's text are numbers.

Restored, with SOD32's hash function unchanged:

    dictionary entries visited, same input     before  8,052,823
                                                after    288,037
                                                SOD32    397,720

Those are counts, not timings, so they are the same on every machine. In
time it was 3.7x on parsing at 4-byte cells and 4.4x at 8-byte. The
whole encoding sequence in this article is worth about 0.69. One
omission, restored, was worth more than all of it.

There is nothing clever here. Hashing a dictionary is the obvious thing
and SOD32 already did it. What is worth reporting is *why it survived
twenty years*: every benchmark I ever ran compared the system against
itself - against last week's build, against the previous stage, never
against the thing it was forked from to beat. The ancestor sat in a
tarball the whole time.

If you have a project with a parent, go and run the parent.

## 10. How this was measured

Three machines: a single-vCPU x86-64 VM, a 16-core x86-64 laptop, and a
4-core ARMv7 board. Every stage cross-compiles the kernel and the output
image must be byte-identical to the reference *before* the timing is
recorded, so correctness and speed are the same run: a stage that is
fast because it is quietly wrong fails the comparison that times it.

Three things about the numbers are worth more than the numbers.

**The variation is per-build, not per-run.** Repeated runs of the same
binaries agree to 1-2%. Rebuild the tree and a stage moves by five or
ten percent, because where the compiler places code is worth that much
and is fixed for a given binary. Taking the minimum over more
repetitions measures that bias more precisely rather than removing it.
So every engine is built five ways with flags that only move code, all
five are timed, and the figure is the mean with a standard error. The
widest spread of any stage was the *baseline* at 12.6% - the number that
divides every ratio in every table.

**The fastest machine was the worst instrument.** The 16-core laptop's
resolution floor read 5.3% in one run and 13.1% in the next. The ARM
board, four slow cores with nothing else running, resolves to about 1%.

**Two benchmarks had to be thrown away.** A counted-loop microbenchmark
swung 21% between runs of the same binary on the same machine; a
recursive Fibonacci swung 15-23%. Both are the short, narrow ones. Both
surviving workloads run a lot of varied code. A tight interpreter loop
over a handful of opcodes is dominated by indirect-branch prediction and
code placement, which is exactly what varies between builds - so it
measures the build, not the encoding.

Every conclusion above survived being measured twice on at least two
machines. Several earlier ones did not, and are not above.

## 11. Not measured

- Three machines is not a study. Two x86-64 and one ARMv7; no RISC-V, no
  big-endian, no bare metal.
- Nothing here measures pure execution reliably, since both
  microbenchmarks failed reproducibility.
- The locals and variable specialisations are inert in these images:
  `locals.4` is loaded only into the shell image, so the kernel that
  every benchmark runs has no locals to specialise.
- With token threading, `DOES>` is the only extension point - a new
  behaviour type cannot be added from Forth. That is the strongest
  architectural criticism this design has had and I have no answer.

## References

- Brad Rodriguez, *Moving Forth*, part 1 -
  <https://www.bradrodriguez.com/papers/moving1.htm>
- R.G. Loeliger, *Threaded Interpretive Languages*, Byte Books, 1981
- L.C. Benschop, SOD32 - <https://github.com/lennart-benschop/sod32>,
  vendored here at a pinned revision, GPLv2
- ForthHub discussion #187, "An elevator description for Forth's
  threaded code models?", whose vocabulary this article uses -
  <https://github.com/ForthHub/discussion/discussions/187>
- IEEE 1275-1994 (FCode): one-byte codes `0x10`-`0xFE`, escape band
  `0x01`-`0x0F` for two-byte codes. CV8 took the idea of a byte stream
  with an escape, not the layout - it splits on the top bit and has a
  single escape opcode, and FCode has no call band because an FCode
  token *is* a dictionary reference.
- Named in the source where borrowed: HotSpot compressed oops for
  `base + (v << shift)`; CPython 3.11 / PEP 659 for specialising the
  common case; Lua 5.4 for immediate operands; JVM `iload`, CPython
  `LOAD_FAST` and Smalltalk-80's bytecodes 16-31 for locals as opcodes;
  Titzer's in-place Wasm interpreter for interpreting the compact form
  rather than expanding it at load.
