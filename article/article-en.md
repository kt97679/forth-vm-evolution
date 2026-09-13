# Nine Forth virtual machines, measured against each other

## Abstract

I built eight token- and byte-threaded encodings of the same Forth
kernel, each as a working system that compiles its own encoding, and
measured them against the cell-threaded original (RelF) and its ancestor
(SOD32). All nine pass the same 616-case ANS CORE corpus at 4- and 8-byte
cells; the eight RelF descendants cross-compile the kernel to
byte-identical images. Timings are from three machines, two
architectures, with a measured resolution floor per workload.

Findings. The densest encoding, a byte stream with specialised opcodes
for hot kernel words and small integers, gives an image 0.46x the size at
8-byte cells and runs kernel compilation at 0.78x the time. A 16-bit
token encoding with a word-number table is a regression (1.40x); deleting
the table recovers exactly that and no more (0.997x). Nearly all of the
speed gain comes from the specialisations, not the encoding.

Two packed-cell schemes I had rejected on a synthetic dispatch benchmark
at 1.90-2.05x were built and measured at 0.98-1.21x; the benchmark was
wrong by four times, for a reason its own header predicted. Of those
two, the 4-bit scheme is the larger image despite the narrower field,
because an unpackable primitive ends the run it sits in.

Making each encoding self-host exposed a design cost no size model
shows: a word-number table forces the compiler into a heap-side reverse
map and two escape opcodes, where a computed target makes the call one
line.

And running the descendant against its ancestor for the first time found
a 20-year-old regression worth 4x on text-heavy workloads - a dictionary
hash I had dropped in 2004. Every benchmark I had run in the meantime
compared the system to itself.

Everything regenerates from the repository:

    tools/build-stages.sh      # nine systems, both cell widths
    tools/run-tests.sh         # the corpus on all of them
    tools/collect-results.sh   # every table below

---

## 1. Names

Using the vocabulary of ForthHub discussion #187
(<https://github.com/ForthHub/discussion/discussions/187>), where Mitch
Bradley describes token threading as pointers replaced by "some
extra-compact representation like indices into an array, or
variable-length identifiers":

| name here | what it is |
|---|---|
| SOD32 | six 5-bit subinstructions packed per 32-bit cell, plus a return flag |
| cell | one host cell per operation; the cell IS a relative offset |
| PACK4 | tagged nibble: a tag byte then 4-bit opcodes, 16-opcode alphabet |
| PACK8 | tagged byte: a tag byte then 8-bit opcodes |
| SOD16 | token threading, word numbers through a table built at load |
| CPT16 | token threading, table deleted; target = base + (v << S) |
| CV8 | the same, narrowed to a byte stream |
| +spec | CV8 with specialised opcodes for hot words, small ints and immediate operands |

All nine separate engine from image, and the image is machine
independent - the ARM board runs byte-for-byte the same files as the x86
machines. The eight RelF descendants are also position independent:
every reference in the image is relative. SOD32 uses absolute addresses
in its own simulated memory.

## 2. One word, four encodings

`: COUNT DUP 1 + SWAP C@ ;` as bytes, dumped from the images at 4-byte
cells by `tools/show-word.sh`:

    cell    25 9 1 93 29 41 5      7 cells x 4  = 28 bytes
    token   6 2 1 23 7 10 1        7 tokens x 2 = 14 bytes
    CV8     6 120 1 7 79                          5 bytes

A cell value is `1 + index*CELL`, the low bit marking a primitive rather
than a call. A token is the index. In CV8, `120` is `ADDI` - an add with
an immediate operand, into which `LIT 1 +` collapses - and `79` is the
folded `C@ EXIT`.

## 3. Results

### Size, Forth image, bytes

| stage | 8-byte | 4-byte |
|---|---|---|
| SOD32 | -- | 13,292 |
| cell | 24,320 | 13,380 |
| PACK4 | 21,296 | 11,900 |
| PACK8 | 20,848 | 11,844 |
| SOD16 | 12,864 | 10,000 |
| CPT16 | 12,864 | 10,000 |
| CPT16+fold | 12,696 | 9,772 |
| CV8 | 11,416 | 8,456 |
| CV8+spec | **11,088** | **8,108** |

The packed figures are arithmetic: those schemes rewrite in place and
skip the folded cells, and since packing is cell-granular and every
reference is relative, compaction removes exactly (cells folded) x (cell
size) and nothing else.

### Speed, ARMv7, 4-byte cells, ratio to the cell engine

Floors 1.1% (kernel) and 1.4% (parse); a second sweep agreed within 2%.
The ordering is identical on all three machines.

| stage | kernel compile | parse |
|---|---|---|
| SOD32 | -- | 1.397 |
| cell | 1.000 | 1.000 |
| PACK4 | 1.130 | 1.106 |
| PACK8 | 1.066 | 1.045 |
| SOD16 | 1.400 | 1.017 |
| CPT16 | 0.997 | 0.964 |
| CPT16+fold | 0.913 | 0.885 |
| CV8 | 0.890 | 0.890 |
| CV8+spec | **0.782** | **0.765** |

At 8-byte cells the laptop puts CV8+spec at 0.64-0.67 on kernel
compilation - the density argument is about twice as strong where cells
are twice as wide.

## 4. What self-hosting costs

A translated image runs what was compiled into it and compiles nothing.
To make each encoding compile itself I wrote a Forth overlay per
encoding, replacing `;`, `IF`, `LITERAL`, `CREATE`, `DOES>` and the rest.
The overlays are the honest measure of each design's complexity.

CPT16's call is one line - subtract the base, shift, add the opcode
band:

    : CALL, ( a-addr --- )  START @ - CPT-SHIFT RSHIFT 256 + OP, ;

SOD16's is a page. A SOD16 call names a word *number*; the compiler has
an address; the engine's number-to-address table lives in `malloc`ed
memory unreachable from Forth. So the image builds its own sorted copy
on the heap and binary-searches it per call compiled. And the table is
sized at load and never grows, so a word defined afterwards has no
number at all - which needed a far-call escape opcode, and a second for
`DOES>`, whose runtime pushes a mid-word address no number can name.

Deleting the table is usually argued for on dispatch cost. This is the
argument that convinced me, and it is invisible until the system has to
compile for itself.

For the questions ruv asked in that thread: CV8 picks the narrowest of
five literal forms (0/1/-1 as opcodes, then 8-, 16-, 32-bit, full cell);
branches are signed 16-bit offsets from the operand, in tokens or bytes;
`(LOOP)` keeps a cell-aligned inline operand, so the compiler pads with
NOOPs that execute once per loop; and `DOES>` overwrites the one cell
`CREATE` reserved, which is why SOD16's far form is a halved 16-bit
offset - 32 bits does not fit at 4-byte cells.

## 5. Two designs rejected on the wrong number

Before SOD16 I timed two packed-cell schemes in a synthetic dispatch loop
- 1.65x/1.60x on x86-64, 2.05x/1.90x on i386 - and did not build them.
Built, on kernel compilation across three machines:

| | predicted | 8-byte | 4-byte |
|---|---|---|---|
| tagged nibble | 2.05x | 0.99-1.13 | 1.11-1.21 |
| tagged byte | 1.90x | 0.98-1.03 | 1.04-1.19 |

The benchmark's header said, in advance, that its streams were sized to
run hot and so "deliberately ignore the advantage density would bring
... the pessimistic case for the packed schemes". It was, by four times.
The baseline they lost to was also wrong: token threading had been
recorded at 0.985 from a 32 MB stream against a 2 MB L2.

CV8 still beats both on both axes at both widths, so the decision holds.
The reason recorded for it does not.

The census had nibble and byte level on size at 0.76x each. Built, the
nibble scheme folds fewer cells - 377 against 433 - and is the larger
image. A 4-bit opcode reaches sixteen primitives; one outside that
alphabet does not merely fail to pack, it ends the run, and the mean
run of packable primitives is about 1.3. A size model prices the fields;
the program pays for the joins.

## 6. Measurement

**The floor is per workload.** Building the same engine five times with
flags that only move code, verifying all five still produce a
byte-identical kernel, and timing them gives 1.1% on kernel compilation
and 6% on a small recursive benchmark, on the same board.

**The fastest machine is the worst instrument.** The 16-core laptop's
floor reads 5.3% in one run and 13.1% in the next; between two full
sweeps its kernel-compile ratios move by 8.1%. The 4-core ARM board with
nothing else running moves 2.0%. Magnitudes above are from the board.

**Two microbenchmarks were discarded** - a counted loop and recursive
Fibonacci - for swinging 15-23% between runs of the same binary on the
same machine. Both surviving workloads run a lot of varied code.

**And the 4x.** Run side by side for the first time, SOD32 was twice as
fast as RelF on everything text-heavy while slower on pure execution.
Counting: 44.5M VM operations against 266.6M for the same input, with
8.05M dictionary entries visited against SOD32's 0.4M. SOD32's
`FORTH-WORDLIST` is 32 hashed chains; RelF's was one chain, because I
dropped the hash in 2004 while changing the link fields from absolute to
relative and never went back. Restored: 288K entries visited, 3.7-4.4x
on parsing. Nothing about the fix is interesting. What is interesting is
that twenty years of benchmarks never compared the system to anything
but its own previous build.

## 7. Not measured

Three machines, two architectures, no RISC-V, no big-endian. No reliable
pure-execution workload, since both microbenchmarks failed
reproducibility. Relocation and portability cost, which RelF's relative
addressing bears on, untested. Thread count of 32 inherited from SOD32,
not chosen. And with token threading, `DOES>` is the only extension
point - a new behaviour type cannot be added from Forth. That is the
strongest criticism this design has had and I do not have an answer.

## References

- Brad Rodriguez, *Moving Forth*, part 1 -
  <https://www.bradrodriguez.com/papers/moving1.htm>
- R.G. Loeliger, *Threaded Interpretive Languages*, Byte Books, 1981
- L.C. Benschop, SOD32 - <https://github.com/lennart-benschop/sod32>,
  vendored at a pinned revision, GPLv2
- ForthHub discussion #187, "An elevator description for Forth's
  threaded code models?"
- IEEE 1275-1994 (FCode): one-byte codes `0x10`-`0xFE`, escape band
  `0x01`-`0x0F` for two-byte codes. CV8 took the idea of a byte stream
  with an escape, not the layout: it splits on the top bit and has a
  single escape opcode. Oracle, *Writing FCode 3.x Programs*;
  openbios/fcode-utils.
- Named in the source where borrowed: HotSpot compressed oops for
  `base + (v << shift)`; JVM `iload`, CPython `LOAD_FAST`, Smalltalk-80
  bytecodes 16-31 for locals as opcodes; PEP 659 for specialisation;
  Lua 5.4 for immediate operands; Titzer's in-place Wasm interpreter.
