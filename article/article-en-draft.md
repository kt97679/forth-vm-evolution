# Making a Forth virtual machine smaller: seven attempts by hand, then a genetic algorithm

I have always liked L.C. Benschop's SOD32 - the Stack Oriented Design, a
32-bit virtual machine with a Forth on top - for how lean, minimal and
simple it is. But its performance is fairly low, and in 2004 I started
wondering whether that could be improved. That is how RelF, for Relative
Forth, came about: I threw away SOD32's packed instruction format and
replaced it with one relative offset per cell. (A cell is the machine
word a Forth is built on: four bytes on a 32-bit host, eight on a 64-bit
one.) The speed-up turned out to be fairly modest, and for a long time I
lost interest in the project.

Recently I came back to it and built it for 64 bits. The same Forth, the
same words, in an image that had gone from 13,380 bytes to 24,320 - one
relative offset per cell means one *cell* per operation, and the cell
had just doubled. I wanted those bytes back, so I started trying other
ways of encoding the system. The first half of this article is those
attempts, in the order I tried them. The second half is what happened
when I stopped choosing by hand and let a genetic algorithm choose
instead.

Everything here regenerates from [the repository](https://github.com/kt97679/forth-vm-evolution):
every engine and image, every measurement, and every table below.
Part one's numbers come from the tree as the ladder left it, commit
a105e59 (`git checkout a105e59 && bash tools/build-stages.sh`); the
kernel took fixes and the search's changes after that, and at master
the same images are 6-12% larger.

Some vocabulary. **Threading** is how a compiled word records what it
calls: a list of references, walked at run time, rather than machine
code. The **engine** is the C program that fetches operations and runs
them; the **image** is the compiled Forth system it runs - the
dictionary, every word body, the whole language. Every system here
builds, boots and passes the same test corpus, the CORE word set of ANS
Forth, the 1994 American National Standard for Forth: 616 cases when
the ladder ended, 661 now.

One short word, compiled three ways - as RelF's cells, as 16-bit tokens
(section 4) and as CV8, the byte code of section 6:

```
: COUNT   DUP 1 + SWAP C@ ;        4-byte cells, from the real images

cell     25  0  0  0 |  9  0  0  0 |  1  0  0  0 | 93  0  0  0 | ...
         '-- DUP --'   '-- LIT --'   '--- 1 ---'   '--- + ---'
         7 cells x 4 bytes ....................................  28 bytes

token     6  0 |  2  0 |  1  0 | 23  0 |  7  0 | 10  0 |  1  0
          DUP     LIT      1       +      SWAP     C@     EXIT
         7 tokens x 2 bytes ...................................  14 bytes

CV8       6  | 120   1 |  7   |   79
         DUP     +1      SWAP   C@;EXIT ........................  5 bytes
```

---

# Part one: by hand

## 1. What 64-bit did

`COUNT` above compiles to seven consecutive cells, one per operation. A
cell holds a **call** - the distance from itself to the word called - or
a **primitive**, a small number saying which built-in operation it is;
the low bit tells the two apart. Nothing in the image is an absolute
address, so it loads anywhere, which was the point of the design.

Seven cells is 28 bytes on a 32-bit host and **56 on a 64-bit one**, for
a definition that has not changed. That is RelF's bargain: one host cell
per operation, whatever the host. The goal from here on was to stop
paying twice for the same program because the host got wider, without
giving back the speed RelF existed for.

## 2. Attempt one: pack operations into a cell, four bits each

SOD32 fits six operations into one cell, so the first thing I tried was
packing, PACK4: a tag byte, then four-bit opcodes - six in a 4-byte cell,
fourteen in an 8-byte one. Four bits name sixteen primitives, so the
other operations stay plain cells.

Each attempt gets two numbers against the cell engine: the size of its
image, and the time to compile the kernel's Forth source - 1.13 is 13%
slower.

    PACK4 image           21,296 bytes at 8-byte cells, 0.876x
    PACK4 kernel compile  1.13 at 8-byte cells, 1.14-1.18 at 4-byte

An eighth smaller and 13-18% slower. A primitive outside the sixteen
does not just fail to pack: it ends the run it sits in, and both halves
then need a tag of their own.

## 3. Attempt two: a byte each

So the opcode became a byte, and every primitive fits - PACK8:

    PACK8 image           20,848 bytes at 8-byte cells, 0.857x
    PACK8 kernel compile  1.09 at 8-byte cells, 1.08-1.18 at 4-byte

Still an eighth smaller and still slower. Measured on real kernel code,
the mean run of consecutive packable operations is about 1.3: this
kernel is mostly calls, and a call never packs. One tag byte to save one
opcode is not a saving. That was the end of packing.

## 4. Attempt three: a 16-bit token through a word table

If a cell is too wide, use a narrower unit: one 16-bit token per
operation, values below 256 primitives, 256+n "the body of the n'th
word", looked up in a table the engine builds at load. I called it
SOD16. The image halved, 24,320 to 12,864 bytes - and on kernel
compilation it was the worst system in the set, 1.378 on the laptop, an AMD
Ryzen 7 PRO 8840HS, and 1.364 on the Tegra, an NVIDIA board with four ARMv7 cores.

The table is enough to *run* a program and not enough to *compile* one.
A dictionary search hands the compiler an address, and the instruction
it must emit holds a number; the engine's table is indexed the wrong way
round and lives where Forth cannot read it. So the image kept an
inverted copy and binary-searched it on every call it compiled.

## 5. Attempt four: delete the table

CPT16, compressed-pointer threading, keeps the 16-bit unit and computes the call target instead of
looking it up: `base + (value << shift)`, so compiling a call is one
line, subtract, shift, add 256. The images are identical to SOD16's, to
the byte, and kernel compilation came level with the cell engine -
1.024 against 1.000 at 4-byte cells, with a standard error of 0.021 over five builds - about 34% ahead of
SOD16. That 34% is a sum: the lookup in the dispatch loop and the
compiler's reverse search went in the same step.

## 6. Attempt five: narrow the unit itself

What decides the size is how many bytes an operation takes, not how
cleverly a target is computed. CV8 - compressed-pointer, variable-length,
8-bit units - is the same idea in a byte stream: one byte for a
primitive, values under 0x80; a byte of 0x80 or more starts a call, two
or three bytes long. The compiler's side is one word of the kernel's
source, `CALL,` in forth/cv8.4:

```
: CALL, ( a-addr --- )
\ Append a call to the body at a-addr: a scaled offset from the image
\ base, near (2 bytes) if it fits in 14 bits, far (3 bytes) otherwise.
  0 LAST-OP !
  START @ - CV8-SHIFT RSHIFT
  DUP 16384 < IF
    DUP 8 RSHIFT 128 OR C, 255 AND C,
  ELSE
    DUP 16 RSHIFT 192 OR C, DUP 8 RSHIFT 255 AND C, 255 AND C,
  THEN ;
```

The engine's side is its dispatch in engine/vm-lab.c. Both are as they
were at a105e59; the engine is shown without its profiling hooks, and in only the
variant s6 builds:

```c
#define NEXT() do { \
        t = BYTE(ip); \
        if (t < 0x80) { ip += 1; goto *dispatch[t]; } \
        goto do_call; \
    } while (0)

do_call:
    if (t & 0x40) {                       /* 11xxxxxx: 22-bit target */
        t = ((t & 0x3F) << 16) | ((UNS64)BYTE(ip + 1) << 8) | BYTE(ip + 2);
        ip += 3;
    } else {                              /* 10xxxxxx: 14-bit target */
        t = ((t & 0x3F) << 8) | BYTE(ip + 1);
        ip += 2;
    }
    RPUSH(ip); ip = cbase + (t << SCALE);
    NEXT();
```

    CV8, image             11,416 bytes at 8-byte cells, 0.469x of cell threading

That is the `COUNT` of the figure: 28 bytes as cells, 14 as tokens, 5
as CV8.

## 7. Attempt six: give the common cases their own opcodes

Five bytes for six operations is two tricks. **Folding**: a primitive
followed by `EXIT` becomes one opcode, so `C@ EXIT` is one byte; I
added it to CPT16 first, the "CPT16 + folding" row below.
**Specialisation**: `1 +` is one opcode with its operand, and common
literals, variable fetches and short branches got opcodes of their own. On x86 that improved kernel
compilation three to four times as much as the whole move from cells to
CV8 before it; on the Tegra about as much. I never tried the two in the other
order.

## 8. Attempt seven: the last place cell width was still being paid

The token stream was now the same at both widths, but the 64-bit image
was still 2,980 bytes larger than the 32-bit one: 1,088 bytes of
dictionary link cells, 496 of padding to align names, 660 of padding at
the end of code bodies. None of that is code. The link became a distance
of one to three bytes, and names and bodies stopped being padded:

    image, 8-byte cells    11,088 -> 7,609     0.456x -> 0.313x
    image, 4-byte cells     8,108 -> 6,749     0.606x -> 0.504x

```
Forth image, 8-byte cells                              bytes  vs cell

cell (RelF)           ##############################  24,320  1.000
PACK4                 ##########################      21,296  0.876
PACK8                 ##########################      20,848  0.857
SOD16                 ################                12,864  0.529
CPT16                 ################                12,864  0.529
CPT16 + folding       ################                12,696  0.522
CV8                   ##############                  11,416  0.469
CV8 + specialised     ##############                  11,088  0.456
CV8 + byte headers    #########                        7,609  0.313
```

The ladder ended on CV8 with byte headers - in the repository, the stage
called s6: 0.31x the image and 0.73 the time on kernel compilation at
8-byte cells, still position-independent, at the price of 20% on text
interpretation. These numbers come from five builds of each engine on
the laptop and three on the Tegra, because a rebuild alone moved a
result by five or ten percent: where the compiler places code is worth
that much, and repeating a run cannot see it.

---

# Part two: by search

## 9. Why I stopped choosing by hand

While working on other projects I had noticed that some of the most
interesting findings came when I deliberately randomised the choices and
looked for solutions outside the usual patterns. Every attempt in part
one was the usual pattern: one decision taken on top of the last, of the
kind the literature already describes. I thought that a search which
randomises could find good designs no existing project or publication
covers.

There was also a practical reason. By s6 the open decisions were no
longer one big change each but dozens of small ones - which pairs to
fuse, which literals get their own opcode, whether the top of the stack
lives in a register, how the dictionary is chained, which compiler builds
the engine and with which flags - and their effects depend on each
other. So each of them became a gene, and a program breeds designs.
Whether what it found really is new is the question I end with.

## 10. A design is a genome

Every design is a genome of 84 genes, and a genome is all it takes to
build one: lab/evolve/evolve.py turns it into a C engine and a Forth
image. The genes are the kind of decision part one took by hand: the
encoding family (cell, SOD16, CPT16 or CV8), fused pairs, specialised
opcodes, the top of the stack in a register, a small JIT (a just-in-time
compiler) that turns hot words into machine code, the dictionary's layout, the compiler and its
flags. None of these techniques is mine. Byte-coded threading is old Forth
practice; superinstructions and stack caching are M. Anton Ertl and
David Gregg's, and so is a JIT that copies native code compiled from C
fragments, in a Forth, since 2004 - it is in Gforth; searching compiler
settings with a multi-objective genetic algorithm is COLE's (Compiler
Optimization Level Exploration; Hoste and Eeckhout, 2008). What the search adds is all of them in one genome.

The hand-made stages are points in the same space, and that is
checked rather than assumed:

    python3 lab/evolve/evolve.py --validate

rebuilds each of them from its genome and requires the images byte for
byte identical to the ones the ladder's build makes.

## 11. What a design is judged on

Four objectives, all minimised:

- **speed** - CPU time against s6 built from the same commit, on seven
  workloads (kernel compilation, fib, the CORE corpus, loop, bubble,
  ackermann, and a set of small applications), the design and s6
  measured in turn; the geometric mean;
- **speed at 32 bits** - the same, with every design built for 4-byte
  cells too;
- **size** - the stripped engine plus the image, in bytes;
- **memory** - peak resident, in KB.

A design that computes anything wrong dies: every workload's output is
compared with the expected one, at both widths. Two more workloads,
sieve and parse, are never used for selection; they are measured
afterwards, to see whether the speed carries over (Spearman's rank
correlation between sieve and the selection speed is 0.94-0.98 run by
run, where 1 is the same order).

## 12. The search

NSGA-II (the Non-dominated Sorting Genetic Algorithm II; Deb and
others, 2002), a standard multi-objective genetic algorithm. The result
of a run is not one design but a front: every design no other beats on
all four objectives at once. A population of 32; parents by tournament:
the lower Pareto rank wins (the front is rank 1, what only it beats is
rank 2, and so on), then the larger crowding distance (the one further
from its neighbours); children by crossover, by genes borrowed from a
third design and by mutation. A design already measured is never
measured again.

Most children are worse than what the run already has, and each one
costs a build and seven workloads at two widths. Two shortcuts spend
less on them, and each has an audit:

- **a screen**: a model fitted on the run's own designs predicts a
  child's speed and size, and a child predicted far behind is not
  measured; one in ten of those is measured anyway. Over seven runs, 2
  of the 421 audited children that ran in full reached the front - the
  screen loses a few, about twenty designs over seven runs against
  180-370 on each run's front;
- **one round first**: a child 30% behind after its first round stops
  there; one in ten runs in full anyway. Of 6,934 audited, none reached
  the front.

A run is one command on the laptop, `sh lab/evolve/next-run.sh`: the
tests and the byte-identical rebuild, the evolution for a set number of
hours, then the front measured again. Each run selects at both cell
widths and starts from the hand-made designs, carrying nothing in from
earlier runs, so the runs are replicates rather than one long run; each
is named by its random seed.

## 13. When to stop

A genetic algorithm can always be run once more, so the rule for
stopping was fixed before the runs it judged. Each run's front gets one
number - its hypervolume, the share of a fixed box of the four
objectives that the front dominates - and four extremes: the fastest,
the smallest, the least memory, the fastest at 32 bits. A run gains
when its hypervolume beats the best earlier run's by 1%, or an extreme
by its threshold: speed 2%, size 1%, memory 4 KB, the 32-bit speed 2%.
The runs stop when, after at least three on an unchanged method, the
last two gain nothing. With three runs no significance test can decide
anything, so the rule uses effect sizes decided in advance.

It stopped after seven runs, seeds 77 to 83: 9 or 12 hours each, 126-178
generations, 32,394-45,696 designs, about 3,400-3,800 an hour.

| | median of the seven | range |
|---|---|---|
| designs on the front | 246 | 180-370 |
| hypervolume | 0.340 | 0.332-0.352 |
| fastest, against s6 | 0.141 | 0.138-0.148 |
| fastest at 32 bits | 0.170 | 0.164-0.182 |
| smallest, engine + image | 14,055 bytes | 13,989-14,210 |
| least memory | 108 KB | 108-112 |

Two confirmation runs followed, started from the pooled fronts of all
the earlier runs. Neither found anything the search had bred: one
run's gain at the fast end turned out to be the laptop's (on an Intel
i7 it was -0.6% at 64 bits and +0.2% at 32), and the other's came from
designs carried in.

## 14. Did the search do anything?

A random search answers that. One more run, ten hours, in which every
child was a fresh random genome, measured exactly as the search's
children were - nothing learned, nothing bred: seed 85.

Its 35,760 random designs left a front of 30, against 180-370 in the
search's runs. Its hypervolume was 0.55 of the search's median; its
fastest 0.320 against 0.138-0.148, its smallest 16,446 bytes against
13,989-14,210, its least memory 116 KB against 108-112. The design space
alone is not where the result comes from.

Every run's front, as one number:

```
hypervolume of each run's front (higher is better)

seed 77                  ##########################################     0.350
seed 78                  #########################################      0.340
seed 79                  ###########################################    0.352
seed 80                  #########################################      0.336
seed 81                  ##########################################     0.347
seed 82                  ########################################       0.332
seed 83                  #########################################      0.336
seed 84, confirming      ############################################   0.366
seed 85, random          #######################                        0.188
seed 86, confirming      #############################################  0.369
```

## 15. No design is best at everything

Drawn as speed against size, the pooled front shows the trade before
any table does:

```
the pooled front: speed against s6 (log scale) and size

45 KB |    J               r
      |                        r
      |
39 KB |                       r
      | JJ                oo   r
      |  JJJ
32 KB |  JJJ
      |   JJJJJJ          o
      |       JJJJJJJJJJ o         r
26 KB |           JJJJJJJJ
      |                 oo      r r
      |                  ooo       rrr r    rr  S
19 KB |                  ooooo          r r r    r
      |                     oooooo         r   rrr  rrr
      |                          ooooooooooooo     r rr       r
13 KB |                                    ooooooooooooooooo
      +------------------------------------------------------------
          0.15      0.25          0.5           1             2
       faster <- speed (CPU time against s6) -> slower

J  a design with the JIT (x86 only)        o  a design without it
r  the random search's front               S  s6, where the ladder ended
444 designs on the pooled front (165 with the JIT); the random search's 30
```

The designs with the JIT own the fast corner and pay for it in bytes;
the designs without it run along the bottom, from fast at about 20 KB to
small and slow; the random search's front lies right of the search's or
above it everywhere.

The pooled fronts held 444 designs. The candidates were re-measured -
alone and under load, at both widths - on the laptop, then the forty
best of them again on two other machines: the i7 at both widths and the
Tegra. 31 sessions on the laptop, 42 on the i7,
6 on the Tegra; a session measures every candidate once. Speeds below are CPU time against s6, so 0.185 is 5.4 times s6's
speed:

| what it wins | x86-64 | x86-32 | ARMv7 | bytes | memory | JIT |
|---|---|---|---|---|---|---|
| fastest on x86-64 | 0.185 | 0.207 | 0.540 | 38,898 | 244 KB | yes |
| fastest on x86-32 | 0.195 | 0.199 | 0.510 | 39,778 | 228 KB | yes |
| best mean of the three | 0.193 | 0.201 | 0.464 | 38,102 | 236 KB | yes |
| fastest without the JIT, and on ARMv7 | 0.414 | 0.455 | **0.327** | 23,164 | 136 KB | no |
| fastest without the JIT on x86 | 0.359 | 0.394 | 0.476 | 20,901 | 140 KB | no |
| least memory | 0.916 | 0.881 | 0.520 | 17,830 | **104 KB** | no |
| smallest | 1.994 | 1.934 | 1.982 | **13,939** | 116 KB | no |
| s6, where the ladder ended | 1 | 1 | 1 | 22,265 | | no |

Later runs changed four of these rows and added two roles; the final
table closes section 17.

The JIT is x86 only; on the Tegra a JIT design runs without it, which is
why the fastest designs on x86 are slower there than the best without
it. No design comes within 25% of the best on all three machines at once, so there is
no single answer: the set kept then was 21 designs, chosen so that each
criterion's winner on each machine is in it.

The fast end is a band, not a design. The machines agree with
themselves - a rank correlation of 0.96-0.99 between their own sessions - and not with each
other: on the forty, the i7's order matches the laptop's at 0.92 at 32
bits and 0.47 at 64, and the Tegra's at 0.08. The laptop's fastest is
6-7% behind the i7's own best.

## 16. What the search removed

The aim was never the fastest Forth at any price; it was the smallest,
simplest system that does the job, with speed where it costs little. A
mechanism stays only if some design on the pooled front uses it. So the
search's last step was to take out what no good design used: the older
header and call formats that only the hand-made stages needed, two
file-system levels, a headerless form of the loop words. 358 lines out, 219 in. The stages
that needed them - s2 to s5 - are kept as built files, checked by hash,
so the ladder still runs. Every design in the final set builds to the
same engine and image bytes after the removal as before.

## 17. A search without the JIT

The designs without the JIT in that table were found on the way: in
those runs the JIT took the fast end. Would a search for portable
designs alone - those without the JIT, which run on any host - do
better? Before it ran, I fixed what better would mean:
its front against the 282 portable designs found before, by the
stopping rule's own effect sizes - 1% of hypervolume, or an extreme by
its threshold: 2% of speed at either width, 1% of size, 4 KB of memory.

The run, seed 87, kept every design without the JIT and started from
the earlier fronts built without it: 21 hours on the laptop. The laptop
crashed ten and a half hours in, and the restart did not continue the
first search but began a second one from the same designs. The shorter
search found the fastest designs at both widths, the longer one ended
below it, and together they beat either. By the rule the run was
better: hypervolume +2.4%, its fastest 0.285 against 0.298.

Numbers from inside a run are optimistic at the fast end, so the run's
30 best and the 15 best found before were measured again side by side
for 13 hours - the laptop 28 sessions, the i7 45 at 8-byte cells and 41
at 4, the Tegra 5, every design in every session. Three of the portable
roles above changed hands:

| what it wins | x86-64 | x86-32 | ARMv7 | bytes | memory |
|---|---|---|---|---|---|
| fastest without the JIT, on x86 and on average (new) | **0.343** | **0.339** | 0.372 | 26,242 | 148 KB |
| fastest on ARMv7 (unchanged) | 0.416 | 0.456 | **0.330** | 23,164 | 136 KB |
| small and fast on ARMv7 (new) | 0.452 | 0.443 | 0.359 | 18,607 | 124 KB |
| smallest (new) | 1.933 | 1.866 | 1.834 | **13,891** | 116 KB |

Against the best portable design found before, the new fastest is 4%
better on the mean of the three machines - 1.3% on x86-64, 5% at 32
bits - and 13% slower on the Tegra, where the old one keeps its place.
The new smallest is 48 bytes smaller than the old one and 3-7% faster
on every machine. The new small one fast on the Tegra is 1.7% smaller
and 1% faster than the one before it, for 4 KB more memory. Least
memory did not move.

So a search for portable designs alone does beat what came before, but
by a few percent, not by a step.

A second such run, seed 88, went another 21 hours. Inside the run it
found a design 2.9% faster at 32 bits than anything before; measured
again side by side with the best earlier designs, the same design was
2.1% slower. Nothing else among its best thirty passed a threshold, and
by the rule fixed in advance the portable search stopped.

It did not stay stopped, and not because of a portable run. While each
later run went, the other two machines took a quick measurement of the
designs the run before had bred but nobody had yet measured side by
side. The next run, seed 89, had the JIT back, and among the designs it
bred was 3eb59b271d: without the JIT, and 2.8% faster on ARMv7 than the
design holding that role - something neither portable run had managed.
The quick pass over seed 88's rest turned up ae99617f06, which took
small and fast on ARMv7, though only after six Tegra sessions pooled:
2.3% faster with a standard error of 0.42%, just past the 2% bar. Seed
90, the other JIT run, gained nothing, but the quick pass over seed 89's
rest found 11a56ff9e4. It took the place of section 15's fastest design
without the JIT on x86 (20,901 bytes), kept by then as the small one
fast on x86: 5.45% smaller, 3.6% faster at 32 bits and 1.5% slower at
64 - inside the threshold.

A role changing hands counts as a gain, so a third portable run
followed, seed 91. Against the short list it was compared with, it
gained twice. Against everything measured before - for speed, bridged
through the designs both measurements shared - its fastest at 4-byte
cells was 0.7% ahead, where 2% was needed, and its smallest 0.13%
smaller, where 1% was. The portable search stopped for good.

The last measurement before the designs were frozen put 435 of them
side by side on all three machines for 26 hours: the 72 on the final
front that nobody had measured across machines, the rest of seed 91,
the role holders and the best of the earlier re-measurements. No
extreme gained - the run's fastest came out 0.7-2.8% behind the best
found before, the fast end optimistic once more. Every design smaller
than the smallest holder but one paid for it in speed; the smallest of
them, 1.4% smaller, by 18-19% at 32 bits. The one that did not,
d180351903, is 8 bytes smaller at 8-byte cells and 48 at 4, with no
speed traded, and it became the smallest.

So: three portable runs, the first better than what came before by a
few percent, the second only through a design outside its best thirty,
the third not at all - and the fastest design on ARMv7 came from a run
with the JIT in it. The search ended with these ten, one design
to a role:

| what it wins | `make` | x86-64 | x86-32 | ARMv7 | bytes | memory | JIT |
|---|---|---|---|---|---|---|---|
| fastest on x86-64 | `fastest-x86-64` | **0.185** | 0.207 | 0.540 | 38,898 | 244 KB | yes |
| fastest on x86-32 | `fastest-x86-32` | 0.189 | **0.193** | 0.476 | 41,990 | 224 KB | yes |
| best mean of the three | `best-all-round` | 0.193 | 0.201 | 0.464 | 38,102 | 236 KB | yes |
| smallest with the JIT | `small-jit` | 0.225 | 0.235 | 0.577 | 29,306 | 208 KB | yes |
| fastest without the JIT, on x86 and on average | `portable-fastest` | 0.343 | 0.339 | 0.372 | 26,242 | 148 KB | no |
| fastest on ARMv7 | `portable-arm` | 0.378 | 0.443 | **0.320** | 22,522 | 132 KB | no |
| fast on x86 and small | `portable-knee` | 0.363 | 0.377 | 0.477 | 19,761 | 140 KB | no |
| small and fast on ARMv7 | `portable-small` | 0.450 | 0.444 | 0.351 | 18,599 | 124 KB | no |
| least memory | `least-memory` | 0.916 | 0.884 | 0.521 | 17,830 | **104 KB** | no |
| smallest | `smallest` | 1.926 | 1.784 | 1.717 | **13,883** | 116 KB | no |
| s6, where the ladder ended |  | 1 | 1 | 1 | 22,265 | | no |

On ARMv7 the designs with the JIT run without it: the JIT is written
for x86 only. Bytes are the engine and the image at 8-byte cells.

Each design is a directory under designs/ in the repository - its C
source, its image and a Makefile - and the `make` column is its name
there. To get one and run it on x86-64 Linux (gcc or clang needed):

```
git clone https://github.com/kt97679/forth-vm-evolution
cd forth-vm-evolution
make portable-knee        # one design; plain `make` builds all ten
designs/portable-knee/forth designs/portable-knee/image.img
```

Then type Forth - names in upper case, `BYE` to leave. `make test`
builds all ten and runs a definition in each. The six without the JIT
also build for ARMv7 (`make forth-arm` in a design's directory) and,
with the C library, for any host with a C compiler (`make forth-libc`);
designs/README.md lists every build.

What they are made of, from their genomes (designs/ holds each one's):
all ten are CV8 and fold a primitive into the `EXIT` after it - the
search could still pick cells, SOD16 or CPT16, and no winner did. Byte
headers are in all ten too, but those I fixed for every CV8 design; the
search did not choose them. The rest divides them. The four with the
JIT and the small fast one on x86 keep the top of the stack in a
register; the other five keep the whole stack in memory. The fast
designs without the JIT have every kind of specialised opcode, the JIT
designs four of the five kinds, the three smallest none at all. Fused
pairs hardly figure: nine of the ten carry one or none, the fastest on
ARMv7 six. And seven of the ten are built by clang, five with -Os.

## 18. What carries over

For anyone building a small Forth, this is what the measurements say,
in order of what each step bought. Size comes from the encoding: the
byte code took the image to 0.469 of the cells', the byte headers to
0.313 (sections 6 and 8), and every one of the ten winners is that byte
code. Speed without a JIT comes from specialisation: on x86 it bought
three to four times what the move to the byte code did (section 7), and
the fastest designs without the JIT have every kind of it. The JIT buys
nearly twice the speed on x86 - 0.185 against 0.343 at 64 bits - for
38,898 bytes against 26,242, and nothing on a machine it does not
support: on ARMv7 that design is at 0.540 and the best portable one at
0.320. The top of the stack in a register, the usual first step, is in
all four JIT designs and in one of the six without.

## What still bothers me

**Whether any of this is new.** Technique by technique, nothing in the
winners is: see the credits in section 10. Even the two details I
thought were mine turned out to have relatives once I looked properly.
Calls relative to a base, for relocation and for shorter references,
and a dictionary link that is a relative offset in a hashed chain are
both in Anthony Rose's ART-FORTH, at the Rochester Forth Conference in
1986; a token whose top bit marks a call is in uxForth (2016); Enforth
makes its calls offsets from the start of the dictionary. What I still
have not found is the variable-length forms - a call of two or three
bytes, a link of one to three read backwards from the name - and any
winner's whole combination. Forth's folklore lives on comp.lang.forth
more than in papers, so not finding them proves little. If you know a
Forth that does either, please tell me in the comments.

**Selection ran on one machine.** The Tegra disagrees with the laptop
almost completely - as Huang, Marr and Ugawa found for interpreter
handler orders evolved for one machine - and one gene shows what that
costs: multi-state stack caching made its designs 18% faster on ARMv7, and the search never kept
it, because on the laptop those designs were slower and twice the size.
How much else of that kind there is, I cannot tell from here.

**The 34%** from part one is still two effects I could not separate,
and the search did not separate them either: the table and the
compiler's inverted copy went in one step and stayed gone.

The repository is at [github.com/kt97679/forth-vm-evolution](https://github.com/kt97679/forth-vm-evolution);
every number above comes out of it, and `make` at its top builds the
ten designs of the table at the end of section 17 from source. I would rather be
corrected in the comments than be wrong quietly.

## References

- This project: [github.com/kt97679/forth-vm-evolution](https://github.com/kt97679/forth-vm-evolution)
- Brad Rodriguez, [*Moving Forth*, part 1](https://www.bradrodriguez.com/papers/moving1.htm)
- R.G. Loeliger, *Threaded Interpretive Languages*, Byte Books, 1981
- L.C. Benschop, [SOD32](https://github.com/lennart-benschop/sod32), vendored here at a pinned revision, GPLv2
- K. Deb, A. Pratap, S. Agarwal, T. Meyarivan, "A fast and elitist multiobjective genetic algorithm: NSGA-II", *IEEE
  Transactions on Evolutionary Computation* 6(2), 2002
- ForthHub discussion #187, ["An elevator description for Forth's threaded code models?"](https://github.com/ForthHub/discussion/discussions/187), whose vocabulary this article uses
- IEEE 1275-1994, the Open Firmware standard, whose FCode is a byte-coded Forth
- M.A. Ertl, "Stack caching for interpreters", PLDI 1995; M.A. Ertl, D. Gregg, "Combining stack caching with dynamic
  superinstructions", IVME 2004
- M.A. Ertl, D. Gregg, "Retargeting JIT compilers by using C-compiler generated executable code", PACT 2004; D. Gregg,
  M.A. Ertl, "Optimizing code-copying JIT compilers for virtual stack machines", Concurrency and Computation 18(11), 2006
- H. Xu, F. Kjolstad, "Copy-and-patch compilation", OOPSLA 2021
- A. Rose, "Design of a fast 68000-based subroutine threaded FORTH with inline code & an optimiser", Proceedings of the
  1986 Rochester Forth Conference (JFAR 4(2), 285-288)
- [uxForth](http://oneweekwonder.blogspot.com/2016/11/uxforth-unexpanded-forth-for-standard_6.html), 2016;
  [Enforth](https://github.com/malyn/Enforth)
- K. Hoste, L. Eeckhout, "COLE: compiler optimization level exploration", CGO 2008
- W. Huang, S. Marr, T. Ugawa, "Optimizing the order of bytecode handlers in interpreters using a genetic algorithm",
  ACM SAC 2023
