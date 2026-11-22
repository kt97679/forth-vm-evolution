# Forth designs for relf - the new roles (Iteration 726)

(forth-vm-evolution, Iteration 726: results/drafts/handoff-relf-draft-721.md made final - chain D decided the smallest
  JIT
design and the self-hosting gate (725, results/followup-roles-seed96-jitband.md), the rage check's second run and
portable-fastest's gate the rest (726, results/rage-designs-726.md). It replaces results/handoff-relf-657.md, which
  stays
as the history. Written by results/drafts/relf-handoff-726.py from designs/, the records and those documents.)

## What changed since the 657 handoff

- **The measure** (676-686): the size is the engine, the image and the code the five selection programs lay (sim16,
  gc16,
  scan, evo, shellmix - relf's shellmix.fth the fifth, 686), at 8-byte cells - so the bytes below are not comparable
  with 657's (which were the engine and the image only).
- **The search reopened** (677-704): seeds 92-96 with the run-time genes rtvar (a data word's @ and ! as one operation,
  relf's VAR@ and VAR!), rtconst (a constant compiled as its value - relf's rule), rtinline (a body of at most 3
  instructions in 6 bytes copied for its call - relf's inlining rule), DOES> @ in rtvar; the unaligned strings and VALUE
  without its kind cell taken for everyone (680-681). The series stopped at seed 96 by its rule.
- **The roles chosen again** (705-725): chains A-D on the laptop, dream and the Tegra - A a screen of 944, B a shortlist
  of 99, C the 66 it could not settle, D the smallest JIT design's band (results/followup-roles-seed96-roles.md, -b.md,
  -c.md, followup-roles-seed96-jitband.md); the ten by the rule - 1 % smaller, no machine class 2 % slower, memory
  within
  8 KB; a speed role's challenger 2 % faster at 2 SE - results/new-roles-718.md, with every near design kept on record
  there. 8 of the ten changed: `fastest-x86-64` 9b15ba26f7 (was c7c35f9c97), `fastest-x86-32` 11f956db93 (was
  ee34931cd7), `best-all-round` df097ba2e2 (was 06b188f45b), `small-jit` 15eda54ebd (was c6f1c1331b), `portable-fastest`
  d727605472 (was 782f3ad7ff), `portable-arm` a8d35bdccc (was 3eb59b271d), `portable-knee` 48a012411a (was 11a56ff9e4),
  `smallest` 219878ec89 (was d180351903); `portable-small` ae99617f06 and `least-memory` fb0d57c8a2 kept.
- **The images are self-built** (666-726, relf's way): forth/cross-cv8.4, a CV8 cross compiler in Forth run by each
  design's own engine, writes the design's image from source - designs/forth/ (kernel.4, extend.4, cross-cv8.4 and the
  overlays its genes name) and designs/NAME/genes.4; `make selfhost` in a design rebuilds its image byte for byte. Every
  role self-hosts at both widths (722). The gate's speed half (lab/evolve/selfhost-speed.py on the laptop: 5
  alternations of 10 rounds, both widths; a self-built image more than 2 %% slower than the translator's ships the
  translator's): 7 self-built; `fastest-x86-32`, `fastest-x86-64`, `small-jit` translator-built - their self-built
  images 2.1-4.6 % slower at one width
  (designs/TRANSLATOR-BUILT gives each), the instructions the same (721): code placement. portable-fastest, self-built
  since 722, passed at 726 (0.997 at 8-byte cells, 0.987 at 4).

## The designs

| `make` target | design | what it wins | x86-64 | x86-32 | ARMv7 | bytes | memory | JIT | image |
|---|---|---|---|---|---|---|---|---|---|
| `fastest-x86-64` | 9b15ba26f7 | fastest on x86-64 | 0.161 | 0.186 | - | 53,503 | 292 KB | yes | translator-built |
| `fastest-x86-32` | 11f956db93 | fastest on x86-32 | 0.175 | 0.180 | - | 49,925 | 264 KB | yes | translator-built |
| `best-all-round` | df097ba2e2 | best mean of x86-64, x86-32 and ARMv7 | 0.162 | 0.187 | 0.432* | 54,695 | 288 KB | yes | self-built |
| `small-jit` | 15eda54ebd | smallest of the JIT designs | 0.219 | 0.234 | - | 36,344 | 208 KB | yes | translator-built |
| `portable-fastest` | d727605472 | fastest without the JIT, by the mean | 0.318 | 0.317 | 0.324 | 35,539 | 148 KB | no | self-built |
| `portable-arm` | a8d35bdccc | fastest on ARMv7 | 0.339 | 0.431 | 0.302 | 45,274 | 140 KB | no | self-built |
| `portable-knee` | 48a012411a | fast without the JIT; small | 0.385 | 0.373 | 0.408 | 26,957 | 144 KB | no | self-built |
| `portable-small` | ae99617f06 | small, fast on ARMv7 | 0.451 | 0.443 | 0.324 | 26,261 | 124 KB | no | self-built |
| `least-memory` | fb0d57c8a2 | least memory | 0.849 | 0.880 | 0.477 | 25,569 | 112 KB | no | self-built |
| `smallest` | 219878ec89 | smallest | 1.483 | 1.285 | 1.234 | 21,673 | 116 KB | no | self-built |

Speed: CPU time against the hand-made s6-cv8b, the geometric mean over the selection workloads - lower is faster;
each class the geometric mean of its machines over a chain's sessions (chain B's, or chain C's where B lacks a class -
results/drafts/designs-table-718.py): x86-64 the laptop (AMD Ryzen 7 PRO 8840HS) and dream (Intel i7-6700) at 8-byte
cells, x86-32 the same at 4-byte cells, ARMv7 rage (an NVIDIA Tegra). \* best-all-round on ARMv7 without its JIT; - not
measured there. Bytes: the engine, the image and the five programs' code, 8-byte cells (the records, results/relf-
designs-718.md). Memory: peak resident, the laptop. Image: what designs/ ships at both widths. The same table:
designs/README.md. Of the seven measured in all three classes, none comes within 25 % of the best in each.

## What each is built from

The genes where a design's expression differs from s6-cv8b's, by today's evolver (lab/evolve/evolve.py; long lists as
their length; GENE=- one s6 has and the design does not). tag2: relf's two-bit tag format; compiler 1: clang, else GCC;
opt: the optimisation level, -O2 if absent. designs/NAME/genes.4 has the same as Forth (lab/evolve/export-genes.py).

- **9b15ba26f7** (`fastest-x86-64`): abortif=1, align1=-, alignfn=1, bfind=1, bss=1, compiler=1, dskew=1,
  folds=+,U<,DROP, fsys=1, hotinl=40, jit=1, jitcfa=1, jitdoes=1, jitexec=1, jitfuse=1, jitimg=1, jitinl=1, jitk=3,
  jitloop=1, jitmul=1, jittail=1, jitvar=1, jitx=1, kfast=1, kinput=1, klookup=1, knumber=1, nocet=1, nocrossjump=-,
  nogcse=-, noreorder=-, opbody=1, ops10=22 ops, opt=O3, rtinline=1, rtiplus=1, rtloop=1, rtloopall=1, swapi=1, t2hot=1,
  t2wide=1, tag2=1, tfind=1, thinhdr=1, threads=2, varslot=0.
- **11f956db93** (`fastest-x86-32`): align1=-, alignfn=1, bss=1, compiler=1, dskew=1, folds=C!,U<,LIT, hotinl=10, jit=1,
  jitcfa=1, jitexec=1, jitfuse=1, jitimg=1, jitinl=1, jitloop=1, jitmul=1, jittail=1, jitvar=1, jitx=1, kfast=1,
  kinput=1, klookup=1, knumber=1, nocet=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, ops10=21 ops, opt=O3,
  rtfuse=1, rtinline=1, rtloop=1, rtloopall=1, spec=4 ops, supers=++C!, swapi=1, t2hot=1, t2wide=1, tag2=1, thinhdr=1,
  threads=2, varslot=0.
- **df097ba2e2** (`best-all-round`): abortif=1, align1=-, bfind=1, bss=1, compiler=1, dskew=1, folds=+,U<,DROP, fsys=2,
  guard=1, hotinl=40, jit=1, jitcfa=1, jitdoes=1, jitexec=1, jitfuse=1, jitimg=1, jitinl=1, jitk=3, jitloop=1, jitmul=1,
  jittail=1, jitvar=1, jitx=1, kfast=1, kinput=1, klookup=1, knumber=1, nocet=1, nocrossjump=-, nogcse=-, noreorder=-,
  opbody=1, ops10=22 ops, opt=O3, rtinline=1, rtiplus=1, rtloop=1, rtloopall=1, swapi=1, t2hot=1, t2wide=1, tag2=1,
  tfind=1, thinhdr=1, threads=2, varslot=0.
- **15eda54ebd** (`small-jit`): align1=-, bfind=1, bss=1, compiler=1, dskew=1, folds=DROP, fsys=2, hotinl=10, jit=1,
  jitimg=1, jitinl=1, jitloop=1, jitmul=1, jittail=1, jitx=1, kfast=1, kinput=1, klookup=1, nocrossjump=-, nogcse=-,
  noreorder=-, opbody=1, opinline=1, ops10=22 ops, opt=Os, rtloop=1, rtloopall=1, spec=tiny,small,imm, t2hot=3, tag2=1,
  tfind=1, thinhdr=1, threads=3, varslot=0.
- **d727605472** (`portable-fastest`): align1=-, bss=1, compiler=1, escape=2, factor=1, folds=22 ops, fsys=2, guard=1,
  hotinl=20, kfast=1, kinput=1, klookup=1, knumber=1, msc=-, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1,
  ops10=37 ops, rtfuse=0, rtimm=2, rtinline=1, rtiplus=1, rtloop=1, rtloopall=1, rtvar=1, swapi=1, t2wide=1, tag2=1,
  tail=-, tfind=1, thinhdr=1, tos=0.
- **a8d35bdccc** (`portable-arm`): alignhot=3, bss=1, escape=1, folds=22 ops, fsys=2, gotodup=2, guard=1, kfast=1,
  kinput=1, klookup=1, lto=1, msc=-, nocet=1, nocrossjump=1, nogcse=1, noinls=1, opbody=1, opinline=1, ops10=29 ops,
  peel=1, regpin=1, rtfuse=1, rtimm=1, rtiplus=1, rtloop=1, rtloopall=1, spec=4 ops, supers=@++,R>+DROP, swapi=1,
  tail=-, thinhdr=1, threads=2, tos=0, tracer=1, varslot=0.
- **48a012411a** (`portable-knee`): align1=-, alignfn=1, bss=1, compiler=1, d256=1, escape=1, folds=6 ops, fsys=2,
  guard=1, kfast=1, kinput=1, klookup=1, msc=-, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1, ops10=27
  ops, opt=Os, rtfuse=0, rtinline=1, rtiplus=1, rtloop=1, rtloopall=1, supers=DUP+@, tail=-, thinhdr=1, threads=3,
  tos=0, varslot=0.
- **ae99617f06** (`portable-small`): bss=1, dskew=1, fbuf=1, folds=22 ops, fsys=2, gotodup=1, guard=1, kfast=1,
  kinput=1, klookup=1, lto=1, msc=-, nocet=1, noinls=1, opbody=1, opinline=1, ops10=29 ops, rtfuse=1, rtiplus=1,
  rtloop=1, rtloopall=1, spec=, supers=++@,DUP+>R, tail=-, thinhdr=1, threads=3, tos=0, varslot=0.
- **fb0d57c8a2** (`least-memory`): alignfn=1, bss=1, fsys=3, gotodup=1, hotcalls=32, kfast=1, kinput=1, klookup=1,
  lto=1, msc=-, noinls=1, opbody=1, ops10=19 ops, regpin=3, rtfuse=0, rtiplus=1, rtloop=1, rtloopall=1, spec=, tail=-,
  tfind=1, thinhdr=1, tos=0.
- **219878ec89** (`smallest`): align1=-, bss=1, compiler=1, fbuf=2, folds=4 ops, fsys=3, hotcalls=32, kfast=1, msc=-,
  nocet=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1, ops10=12 ops, opt=Os, rtfuse=0, rtloop=1,
  rtloopall=1, spec=, supers=@++,R>+DROP, tail=-, thinhdr=1, threads=3, tos=0.

### The genes

- `abortif` - ABORT" guarded (`abortif`: 0, 1; Iteration 117): the converter puts every (ABORT") call behind ?BRANCH and
  -1, as gforth and lbForth compile ABORT"
- `align1` - the -falign-*=1 flags, GCC only (build.txt)
- `alignfn` - function alignment off (`alignfn`: 0, 1; Iteration 113): -falign-functions=1 -falign-loops=1
- `alignhot` - handler entries aligned (`alignhot`: off, 32:11, 32, 64; Iteration 298): GCC's -falign-jumps,
  -falign-labels and -falign-functions - a computed goto's target, or a tail engine's function, on a fetch window's
  start; 32:11 only where it costs at most 10 ...
- `bfind` - the dictionary walk branch-light (`bfind`; Iteration 316): THREAD-FIND's and (FIND)'s candidates compared as
  one masked 64-bit word - count and first seven characters - and the link read without a branch on its form; expressed
  when either is a format-10 ...
- `bss` - scratch buffers out of the file (`bss`: 0, 1; Iteration 44): TIB, POCKET and INCLUDE-BUFFER live past the
  image's end, DP after them
- `compiler` - the compiler (`compiler`: 0 GCC, 1 clang; Iteration 262; CV8 designs, offered only where clang is
  installed): every engine compile through clang - -Oz for -Os, only the flags clang knows; GCC's own genes (nogcse,
  nocrossjump, align1, noreorder, peel, ...
- `d256` - a 256-entry dispatch table (GENES.md's CV8 table)
- `dskew` - the data stack's start skewed (`dskew`: 0, 1; Iteration 183, the owner's question - the stacks' place): 2 KB
  lower, so its top cells and the return stack's stop sharing page offsets (4K aliasing: with both stacks at the block's
  top they met whenever the ...
- `escape` - the escape (`escape`): primitives 36-67 behind one byte (125 + selector), their 32 opcodes joining the free
  slots
- `factor` - repeated code in shared bodies (`factor`: 0, 1, 2, 3; Iteration 267; tag-2 designs): the converter moves
  runs of whole operations that recur in the image - no branch or branch target, inline operand, string, EXIT,
  return-stack or loop word, call to a word ...
- `fbuf` - the file read-ahead buffer (`fbuf`: 0, 1, 2 = 4096, 1024, 512 bytes; Iteration 115)
- `folds` - which of the 23 foldable primitives get prim;EXIT opcodes, in what order (GENES.md's table)
- `fsys` - the file words over single system calls, by level (results/drafts/fsys/single-syscall.md; levels 4-5 retired
  at 599)
- `gotodup` - GCC's computed-goto unfactoring (`gotodup`: 0, 1, 2 - its default 8, 32, 128 instructions; Iteration 260;
  CV8 designs): `--param max-goto-duplication-insns`. GCC factors computed gotos early and copies the dispatch back into
  handlers whose block ends in no ...
- `guard` - guard pages around the stacks (GENES.md's CV8 table)
- `hotcalls` - one-byte calls (`hotcalls`: 0, 8, 16, 32): the far-call prefixes 0xE0-0xFF call the image's own words
  with the most call sites, through a table in the image's header; chosen per design by the converter, no profile
- `hotinl` - inlined at the hottest call sites (`hotinl`: 0, 10, 20, 40; Iteration 92; in the tag): the converter
  splices the first K safe sites of lab/evolve/hotsites-v1.json - the image's call sites by the fastest design's
  profile, named by caller, callee and ordinal ...
- `jit` - the JIT: hot words translated to x86 machine code from compiled stencils (engine/jit.c, engine/spn-stencils.c;
  x86 only)
- `jitcfa` - the return-stack check along the paths (`jitcfa`: 0, 1; Iteration 482; JIT with jitx; enabled 483): a
  word's >R and R> balanced on every control-flow path, not in page order - fcp's evalLP. As jitmul for seed 70.
- `jitdoes` - DOES> children native (`jitdoes`: 0, 1; Iterations 473-485; JIT with jitx; enabled 475): the child's body
  pushed as a literal, decoding from the DOES> code, with or without a header, R> fused or separate. As jitmul: on no
  front of seed 70; apps from seed 71.
- `jitexec` - EXECUTE native (`jitexec`: 0, 1; Iterations 476-488; JIT with jitx; enabled 477): through a helper
  (jit_exec) with a cache of three cells at each site; S" and ." as literals; cold calls (CR, ABORT, THROW) through the
  helper; a callee it cannot translate ...
- `jitfuse` - pairs as one stencil on the JIT (`jitfuse`: 0, 1; Iteration 507; JIT with jitx; enabled for seed 72 by the
  owner, 508): a literal into +, <, >, =, XOR, AND or OR, and I into + or 2@, copied as one stencil, never where the
  second is a branch target ...
- `jitimg` - the image's own words JIT candidates (evolve.py, Iteration 341)
- `jitinl` - one-operation words inline on the JIT (`jitinl`: 0, 1; Iteration 137; JIT with jitx; **dormant** until seed
  39 has run): a call to a word of one operation and EXIT - 1+, 0=, 1- - is that operation in the caller (not one that
  branches, ends the word, or ...
- `jitk` - the JIT's stack cache (`jitk`: 0, 2, 3; Iteration 259; JIT designs): the top K cells stay in fixed registers
  across the copied code - tools/gen-jitk.py writes a variant of 16 hot data stencils (literal, DUP DROP SWAP OVER, +
  and immediate +, = > <, AND ...
- `jitloop` - (+LOOP) and (?DO) native (`jitloop`: 0, 1; Iteration 130; on the JIT; **dormant** - in LATE, not in
  EXPRESSED, until seed 39 has run): SPN's stencils for both, the scanner reading 160 bytes (its 64 cut both stencils:
  (+LOOP)'s 87 before either exit, ...
- `jitmul` - UM*, UM/MOD, SP@, ALIGNED and COUNT native, (ABORT") too with jitexec (`jitmul`: 0, 1; Iterations 472-488;
  JIT designs; enabled 474): stencils for the operations the applications' words stopped at (lab/evolve/jitapps.py) -
  PICK, CELLS, MOD chains; UM/MOD's ...
- `jittail` - tail calls as jumps on the JIT (`jittail`: 0, 1; Iteration 246; JIT designs): engine/jit.c - a call to a
  native word whose next operation is EXIT, or a BRANCH chain to one, is translated as a jump to it, so its ret returns
  to the caller and tail recursion ...
- `jitvar` - variable fetch and store given JIT stencils (evolve.py, Iteration 342)
- `jitx` - the JIT reaches further (`jitx`: 0, 1; Iteration 108; on the JIT): variables as literals, words without the
  JIT header translated once each, >R/R>/R@ in balanced words, a FILL stencil
- `kfast` - kernel words faster (`kfast`: 0, 1; Iteration 49; byte headers): NAME>BUF without its 32-byte zero fill,
  which the byte compare never reads (forth/cv8b-kfast.4)
- `kinput` - the input side (`kinput`: 0, 1; Iterations 54-55; with kfast): forth/cv8b-kinput.4 (REFILL's tab loop as
  TABS>BL; (PARSE) and PARSE8; ?STACK8) and SCAN, SKIP, TABS>BL, FILL, (PARSE), HASH, PLACE first among the format-10
  names
- `klookup` - the whole lookup and numbers (`klookup`: 0, 1; Iteration 57; with kinput): forth/cv8b-klookup.4 ((FIND)
  and FIND8, (>NUMBER) and >NUMBER8, WORD8) and (FIND), (>NUMBER) first among the format-10 names
- `knumber` - NUMBER? as one opcode (`knumber`: 0, 1; Iteration 295): forth/cv8b-knumber.4, after klookup's overlay -
  (NUMBER?), the kernel's NUMBER? with BASE @ and DPL given (its failures 0 0 0: only INTERPRET calls it, and aborts or
  throws), and NUMBER?8, whose body ...
- `lto` - link-time optimisation (`lto`: 0, 1; Iteration 260; CV8 designs): the engine and its runtime compiled as one
  (-flto), so GCC inlines and drops across them; the JIT's stencils are compiled outside it - LTO changed their code and
  the JIT stopped translating ...
- `msc` - multi-state stack caching (`msc`): 0, 1 or 2 top items in registers, a dispatch table per state, each handler
  variant dispatching by the table of the state it ends in; generated from stack effects for 72 operations, the rest
  normalised to the one-register ...
- `nocet` - -fcf-protection=none (build.txt)
- `nocrossjump` - -fno-crossjumping, GCC only (build.txt)
- `nogcse` - -fno-gcse, GCC only (the compile line in build.txt)
- `noinls` - no inlining of small functions (`noinls`: 0, 1; Iteration 113): -fno-inline-small-functions
- `noreorder` - -fno-reorder-blocks, GCC only (build.txt)
- `opbody` - words an opcode replaced, [opcode EXIT] (`opbody`: 0, 1; Iteration 92): (FIND), (>NUMBER), THREAD-FIND, +!,
  ?DUP, as FILL and CMOVE (Iterations 50, 54)
- `opinline` - the [opcode EXIT] words among the primitives (`opinline`: 0, 1; Iteration 292): placed before
  (PRIMITIVES-END), where PRIMITIVE? asks by address, so the run-time compiler copies their opcode in place of a call -
  code compiled at run time (bubble's 2@ and ...
- `ops10` - format-10 opcodes (`ops10`): `EXECUTE`, `I`, `(DO)`, `+!`, `?DUP`, `UNLOOP`, `J`, and the loop words with an
  operand, `(LOOP)`, `(?DO)`, `(+LOOP)`, `(LEAVE)` - kernel colon words - and the short branches `?BRANCH8`, `BRANCH8`
  as opcodes, from the free ...
- `opt` - the optimisation level: O2 (absent), O3 or Os (clang: -Oz)
- `peel` - -fpeel-loops, GCC only (build.txt)
- `regpin` - the VM's registers pinned to machine registers (RELF.md, Iteration 364)
- `rtfuse` - run-time fusion: the compiler the image carries fuses pairs as the converter does
- `rtimm` - run-time immediates (`rtimm`: 0, 1, 2; Iteration 37; 2 - Iteration 175: without pairs, the overlay alone):
  with run-time fusion and spec imm, the compiler the image carries makes `n +` an ADDI and `SWAP n +` a SWAP+I in the
  code it writes ...
- `rtinline` - a body of at most 3 instructions in 6 bytes copied for its call at run time - relf's inlining rule
  (forth/cv8-fuse-inline.4; results/rtinline-694.md)
- `rtiplus` - I + fused in run-time code (`rtiplus`: 0, 1; Iteration 60; with rtloopall): a format-10 opcode I+,
  SUPER-TABLE's (I, +) -> I+, and forth/cv8-fuse-iplus.4 pointing LAST-OP at I's byte
- `rtloop` - run-time loops (`rtloop`: 0, 1; Iteration 41): the compiler the image carries emits the design's loop
  opcodes - (DO) (LOOP) (+LOOP) (?DO) (LEAVE), I J UNLOOP - each where it has one, 16-bit operands, no padding
  (forth/cv8-fuse-loop.4 - this partial form ...
- `rtloopall` - rtloop compact (`rtloopall`: 0, 1; Iteration 43; retired at 1, 641 - rtloop means all eight since): with
  rtloop and all eight loop opcodes, a run-time loop compiler without fallbacks - one chain, one 12-byte table
  (forth/cv8-fuse-loopall.4)
- `rtvar` - a data word's @ and ! compiled as one operation (vf, vs) at run time - relf's VAR@ and VAR!, DOES> @ among
  them (forth/cv8-fuse-var.4; results/rtvar-688.md, does-at-695.md)
- `spec` - specialised opcode families - var, tiny, small, imm, loc: variables, small literals and immediates as their
  own opcodes (GENES.md's CV8 table, "specialisation families")
- `supers` - superinstructions - the pairs listed, each one opcode (tools/gen-super.py)
- `swapi` - SWAP+I sure of a slot (`swapi`: 0, 1; Iteration 61; with 'imm'): SWAP+I first among the format-10 names
- `t2hot` - the two-bit tag's ranking: its hot threshold - 0.02 by default, 0, 0.05 or static (Iteration 71; with the
  tag)
- `t2wide` - the tag without its 3-byte call (`t2wide`: 0, 1; Iteration 95; in the tag, not multi-state): `10xxxxxx` 64
  more one-byte codes (127), calls of 2 bytes (16 KB) and 4 (1 GB)
- `tag2` - the two-bit tag image format, relf's (FORMAT-TAG2.md)
- `tail` - **Retired at Iteration 456** - frozen off since Iteration 450 (12 of 12 removal votes over seeds 63-65, no
  loss in seed 66), its code removed; the gene kept in the genome, off, so identities hold. Was: tail-call threading
  (`tail`): every handler a function ...
- `tfind` - THREAD-FIND first (`tfind`: 0, 1; Iteration 52; with kfast): THREAD-FIND first among the format-10 names -
  seed 11 drew it from the pool 7 times in 1,425 designs
- `thinhdr` - one thread head in the header (`thinhdr`: 0, 1; Iteration 58; CV8): the header's 32 thread heads - read by
  the CV8 loader and never used, only SOD16 numbers calls - as a count of 1 and a zero head
- `threads` - the dictionary in 16, 32, 64 or 128 chains (evolve.py, Iteration 204)
- `tos` - the top of the data stack in a register (GENES.md's CV8 table; engine/vm-lab-tos.c)
- `tracer` - -ftracer, GCC only (build.txt)
- `varslot` - slot operands (VAR@ and VAR!, the locals opcodes) of variable length - a 15-bit payload in two bytes, 23
  bits in three; at 0 a fixed 16 bits (engine/vm-lab.c, VARSLOT)

## For relf (RELF.md's adoption criteria) - what still holds from 657, and what is new

- **The JIT is x86 only**, as before; the six without it are relf's candidates as they stand.
- **New: the images are built relf's way** - by a cross compiler in Forth, from source, on the design's own engine - so
  what relf takes can now be the source as well as the mechanisms: designs/forth/ and a design's genes.4 rebuild its
  image (`make selfhost`); the genes as Forth name each translator rewrite the design uses.
- **New: relf's own mechanisms measured in the lab** - rtvar, rtconst and rtinline (relf's VAR@/VAR!, constant rule and
  inlining rule; results/mech-prices-684.md, relf-reply-685.md): which of the ten carry them is in their genes above;
  shellmix.fth (relf's) is in the size and the speed.
- **The two-bit tag** (relf's format, tag2=1): `fastest-x86-64`, `fastest-x86-32`, `best-all-round`, `small-jit`,
  `portable-fastest`; the rest CV8 without the tag.
- **Without the C library and on ARMv7**, as before: `make libc`, `make arm` for the six without the JIT; the clang
  three
  (portable-fastest, portable-knee, smallest) cross-built, the lab's bytes, under qemu-arm (725); the GCC three
  (portable-arm, portable-small, least-memory) built on the Tegra by its own GCC, the lab's bytes and running on their
  self-built images (726: results/rage-designs-726.md - engines of 16,782, 13,014 and 11,158 B).
- **Not measured here**, as before: relf's shell workloads beyond shellmix, AArch64, RISC-V.

## The files and how to fetch them

- **designs/** in the repository (the bundle the owner hands over) - what to build from: each design's engine source,
  its Makefile, its images (the "image" column) and their source; `make`, `make test`, `make selfhost`, `make 32`, `make
  libc`, `make arm` from the top.
- **The package** forth-vm-evolution-designs-iter726.tar.gz (lab/evolve/pack-designs.py, as 657's; the owner's copy, not
  the repository): for
  each design `ID/record.json` and, at each width, `ID/cell8/`, `ID/cell4/` - `engine`, `image.img` (`./engine image.img
  < program.fth`; names upper case, `BYE` ends it), `src/`, `build.txt` (each command the lab's build ran), `check.txt`
  (the nine workloads against s6-cv8b at the same width); `SHA256SUMS`. It is the lab's measured build: its images are
  the converter's (tools/layout.py), so for the seven self-built roles designs/' images differ from it (smaller; the
  same speed by the gate). Rebuilt byte for byte from the repository, in a built tree:
  `python3 lab/evolve/pack-designs.py OUT results/relf-designs-718.md
  9b15ba26f7,11f956db93,df097ba2e2,15eda54ebd,d727605472,a8d35bdccc,48a012411a,ae99617f06,fb0d57c8a2,219878ec89` -
  its 40 engines and images the checksums of results/drafts/designs-sha256-718.txt (718, and again at 726).
- **The build-out**: `sh results/drafts/roles-build-718.sh 1 . results/relf-designs-718.md NAMES`, the cross GCC's
  export-arm.py --gcc, then `... 2 . results/relf-designs-718.md NAMES` (the script's header; NAMES
`fastest-x86-64=9b15ba26f7,fastest-x86-32=11f956db93,best-all-round=df097ba2e2,small-jit=15eda54ebd,portable-fastest=d727605472,portable-arm=a8d35bdccc,portable-knee=48a012411a,portable-small=ae99617f06,least-memory=fb0d57c8a2,smallest=219878ec89`);
  a gate FAIL ships
  translator-built by `TRANSLATOR='NAME:REASON'` in phase 2 (725). A role changed later goes the same way, alone.

## The history

Each document stays as it was written. 601-657: results/handoff-relf-657.md, "The history". 718: the new roles chosen
(results/new-roles-718.md; the records results/relf-designs-718.md). 721: this document drafted. 725: small-jit
confirmed (chain D) and the gate's three shipped translator-built. 726: the rage check passed on the self-built images,
portable-fastest passed the gate - this document.

