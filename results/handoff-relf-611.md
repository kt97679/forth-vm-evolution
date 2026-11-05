# Forth designs for relf - the winners of forth-vm-evolution's search (Iteration 611)

(forth-vm-evolution, Iteration 611, the smallest 612: it replaces results/handoff-relf-601.md - the portable run's
782f3ad7ff the fastest portable design, 690981ca5b kept as the fastest on ARMv7, a627b954c6 for 22420b3b61 as small and
fast on ARMv7, and 64a7345393 for cea114f47e as the smallest - smaller at both widths, 3-7% faster in each class
(results/followup-roles-seed87.md); the other six unchanged, their engine and image bytes 601's at both widths; built
and checked with lab/evolve/pack-designs.py.)

Ten designs - the lab's final set's (21 designs, results/final-set-chainsBCD-seed86.md) and the portable run's
(seed 87, results/followup-pick-seed87.md) - chosen so that every
criterion's winner is here: no design is best at everything - none comes within 25% of the best on all three machine
classes, and the fast designs are large while the small ones are slow. Every one is the CV8 byte-coded family, built
at both cell widths and checked against the lab's hand-made s6-cv8b on the nine workloads it measures.

## The designs

Speed: CPU time against the hand-made s6-cv8b, the geometric mean over the selection workloads (kernel, fib, corpus,
loop, bubble, ackermann, apps) - lower is faster, 0.185 is 5.4 times s6's speed. Each class the geometric mean of its
machines, every session pooled: x86-64 - the laptop (AMD Ryzen 7 PRO 8840HS) and dream (Intel i7-6700) at 8-byte
cells; x86-32 - the same at 4-byte cells; ARMv7 - rage (an NVIDIA Tegra), where a JIT design runs without its JIT (*).
The six portable designs read side by side in the follow-up chain (Iteration 611: the laptop 28 sessions, dream 45 at
8-byte cells and 41 at 4-byte, the Tegra 5); the four JIT designs in seed 86's chains B-D (the laptop 31, dream 42,
the Tegra 6). Size: the stripped engine plus the image, exact. Memory: peak resident, the
laptop at 8-byte cells.

| role | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | bytes, 4-byte | memory KB | JIT | checks (8 / 4) |
|---|---|---|---|---|---|---|---|---|---|
| fastest on x86-64 | c7c35f9c97 | 0.185 | 0.207 | 0.540* | 38,898 | 34,262 | 244 | x86-64 and x86-32 | 9/9 / 9/9 |
| fastest on x86-32 | 4ef851fd8e | 0.195 | 0.199 | 0.510* | 39,778 | 38,326 | 228 | x86-64 and x86-32 | 9/9 / 9/9 |
| best all-round (the best mean of the three classes) | 06b188f45b | 0.193 | 0.201 | 0.464* | 38,102 | 33,718 | 236 | x86-64 and x86-32 | 9/9 / 9/9 |
| smallest of the JIT designs | bac37f35a2 | 0.230 | 0.238 | 0.543* | 30,121 | 29,945 | 208 | x86-64 and x86-32 | 9/9 / 9/9 |
| fastest portable; fastest portable on x86 | 782f3ad7ff | 0.343 | 0.339 | 0.372 | 26,242 | 25,406 | 148 | no - portable | 9/9 / 9/9 |
| fastest on ARMv7 | 690981ca5b | 0.416 | 0.456 | 0.330 | 23,164 | 24,239 | 136 | no - portable | 9/9 / 9/9 |
| the knee: fast portable on x86, small | c2ef9488ff | 0.360 | 0.396 | 0.478 | 20,901 | 20,829 | 140 | no - portable | 9/9 / 9/9 |
| small, fast on ARMv7 | a627b954c6 | 0.452 | 0.443 | 0.359 | 18,607 | 18,135 | 124 | no - portable | 9/9 / 9/9 |
| least memory | fb0d57c8a2 | 0.916 | 0.884 | 0.521 | 17,830 | 17,462 | 104 | no - portable | 9/9 / 9/9 |
| smallest | 64a7345393 | 1.933 | 1.866 | 1.834 | 13,891 | 13,675 | 116 | no - portable | 9/9 / 9/9 |

The trade in two sentences: the JIT designs are 4.3-5.4 times s6's speed on x86-64 (4.2-5.0 at 32 bits) in 30-40 KB and 208-244 KB of
memory; without the JIT the three fastest portable designs are 2.1-3.0 times s6's speed on ARMv7 and 2.4-2.9 on x86-64 in 20-27 KB,
and the smallest and the leanest give up speed for 14 KB of engine and image, or 104 KB of memory.

## What each is built from

The genes where a design's expression differs from s6-cv8b's (lab/evolve/evolve.py; long lists as their length; GENE=-
one s6 has and the design does not). tag2: relf's two-bit tag format; compiler 1: clang, else GCC; opt: the
optimisation level, -O2 if absent.

- **c7c35f9c97** (fastest on x86-64): align1=-, bfind=1, bss=1, compiler=1, dskew=1, escape=1, folds=22 ops, fsys=2, hotinl=20, jit=1, jitexec=1, jitfuse=1, jitimg=1, jitinl=1, jitk=3, jitloop=1, jitmul=1, jittail=1, jitvar=1, jitx=1, kfast=1, kinput=1, klookup=1, knumber=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, ops10=21 ops, opt=Os, rtiplus=1, rtloop=1, rtloopall=1, spec=4 ops, swapi=1, t2hot=2, t2wide=1, tag2=1, thinhdr=1, threads=2.
- **4ef851fd8e** (fastest on x86-32): align1=-, bfind=1, bss=1, compiler=1, escape=2, fsys=2, hotinl=40, jit=1, jitfuse=1, jitimg=1, jitinl=1, jitloop=1, jitmul=1, jittail=1, jitx=1, kfast=1, kinput=1, klookup=1, knumber=1, nocet=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1, ops10=20 ops, opt=O3, rtloop=1, rtloopall=1, swapi=1, t2hot=1, t2wide=1, tag2=1, thinhdr=1, threads=1, varslot=0.
- **06b188f45b** (best all-round (the best mean of the three classes)): align1=-, bss=1, compiler=1, dskew=1, escape=1, folds=22 ops, fsys=2, guard=1, hotinl=10, jit=1, jitexec=1, jitfuse=1, jitinl=1, jitk=3, jitloop=1, jitmul=1, jittail=1, jitx=1, kfast=1, kinput=1, klookup=1, knumber=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1, ops10=28 ops, opt=Os, rtfuse=0, rtloop=1, rtloopall=1, spec=4 ops, supers=OVER+C@, t2hot=1, t2wide=1, tag2=1, thinhdr=1.
- **bac37f35a2** (smallest of the JIT designs): align1=-, alignfn=1, bfind=1, bss=1, compiler=1, dskew=1, escape=1, folds=22 ops, fsys=2, hotinl=10, jit=1, jitimg=1, jitinl=1, jitloop=1, jitmul=1, jittail=1, jitx=1, kfast=1, kinput=1, klookup=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1, ops10=18 ops, opt=Os, rtloop=1, rtloopall=1, spec=4 ops, t2wide=1, tag2=1, thinhdr=1, threads=3, varslot=0.
- **782f3ad7ff** (fastest portable; fastest portable on x86): align1=-, bss=1, compiler=1, d256=1, escape=1, folds=22 ops, fsys=2, guard=1, kfast=1, kinput=1, klookup=1, knumber=1, msc=-, nocet=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1, ops10=33 ops, opt=O3, rtfuse=0, rtimm=1, rtiplus=1, rtloop=1, rtloopall=1, supers=++C@, swapi=1, tail=-, thinhdr=1, threads=2, tos=0.
- **690981ca5b** (fastest on ARMv7): align1=1, alignfn=1, bss=1, dskew=1, escape=1, gotodup=2, guard=1, kfast=1, kinput=1, klookup=1, lto=1, msc=-, nocet=1, nocrossjump=1, nogcse=1, noinls=1, opbody=1, opinline=1, ops10=34 ops, regpin=3, rtfuse=0, rtimm=2, rtiplus=1, rtloop=1, rtloopall=1, spec=4 ops, tail=-, thinhdr=1, tos=0, varslot=0.
- **c2ef9488ff** (the knee: fast portable on x86, small): abortif=1, align1=-, bfind=1, bss=1, compiler=1, d256=1, escape=2, folds=22 ops, fsys=2, guard=1, kfast=1, kinput=1, klookup=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1, ops10=42 ops, opt=Os, rtfuse=0, rtiplus=1, rtloop=1, rtloopall=1, spec=4 ops, swapi=1, tfind=1, thinhdr=1, threads=1, varslot=0.
- **a627b954c6** (small, fast on ARMv7): bss=1, dskew=1, fbuf=1, folds=22 ops, fsys=2, gotodup=2, guard=1, kfast=1, kinput=1, klookup=1, lto=1, msc=-, nocet=1, noinls=1, opbody=1, opinline=1, ops10=29 ops, rtfuse=0, rtiplus=1, rtloop=1, rtloopall=1, spec=, supers=++@,DUP+>R, tail=-, thinhdr=1, threads=3, tos=0.
- **fb0d57c8a2** (least memory): alignfn=1, bss=1, fsys=3, gotodup=1, hotcalls=32, kfast=1, kinput=1, klookup=1, lto=1, msc=-, noinls=1, opbody=1, ops10=19 ops, regpin=3, rtfuse=0, rtiplus=1, rtloop=1, rtloopall=1, spec=, tail=-, tfind=1, thinhdr=1, tos=0.
- **64a7345393** (smallest): align1=-, bss=1, compiler=1, dskew=1, fbuf=2, folds=11 ops, fsys=3, hotcalls=32, kfast=1, msc=-, nocet=1, nocrossjump=-, nogcse=-, noreorder=-, opbody=1, opinline=1, ops10=6 ops, opt=Os, rtfuse=0, spec=, supers=++C@, tail=-, thinhdr=1, threads=3, tos=0.

### The genes, as lab/evolve/GENES.md describes them

- `abortif` - ABORT" guarded (`abortif`: 0, 1; Iteration 117): the converter puts every (ABORT") call behind ?BRANCH and -1, as gforth and lbForth compile ABORT"
- `align1` - the -falign-*=1 flags, GCC only (build.txt)
- `alignfn` - function alignment off (`alignfn`: 0, 1; Iteration 113): -falign-functions=1 -falign-loops=1
- `bfind` - the dictionary walk branch-light (`bfind`; Iteration 316): THREAD-FIND's and (FIND)'s candidates compared as one masked 64-bit word - count and first seven characters - and the link read without a branch on its form; expressed when either is a format-10 ...
- `bss` - scratch buffers out of the file (`bss`: 0, 1; Iteration 44): TIB, POCKET and INCLUDE-BUFFER live past the image's end, DP after them
- `compiler` - the compiler (`compiler`: 0 GCC, 1 clang; Iteration 262; CV8 designs, offered only where clang is installed): every engine compile through clang - -Oz for -Os, only the flags clang knows; GCC's own genes (nogcse, nocrossjump, align1, noreorder, peel, ...
- `d256` - a 256-entry dispatch table (GENES.md's CV8 table)
- `dskew` - the data stack's start skewed (`dskew`: 0, 1; Iteration 183, the owner's question - the stacks' place): 2 KB lower, so its top cells and the return stack's stop sharing page offsets (4K aliasing: with both stacks at the block's top they met whenever the ...
- `escape` - the escape (`escape`): primitives 36-67 behind one byte (125 + selector), their 32 opcodes joining the free slots
- `fbuf` - the file read-ahead buffer (`fbuf`: 0, 1, 2 = 4096, 1024, 512 bytes; Iteration 115)
- `folds` - see lab/evolve/evolve.py, `grep -n "gene('folds'" lab/evolve/evolve.py`
- `fsys` - the file words over single system calls, by level (results/drafts/fsys/single-syscall.md; levels 4-5 retired at 599)
- `gotodup` - GCC's computed-goto unfactoring (`gotodup`: 0, 1, 2 - its default 8, 32, 128 instructions; Iteration 260; CV8 designs): `--param max-goto-duplication-insns`. GCC factors computed gotos early and copies the dispatch back into handlers whose block ends in no ...
- `guard` - guard pages around the stacks (GENES.md's CV8 table)
- `hotcalls` - one-byte calls (`hotcalls`: 0, 8, 16, 32): the far-call prefixes 0xE0-0xFF call the image's own words with the most call sites, through a table in the image's header; chosen per design by the converter, no profile
- `hotinl` - inlined at the hottest call sites (`hotinl`: 0, 10, 20, 40; Iteration 92; in the tag): the converter splices the first K safe sites of lab/evolve/hotsites-v1.json - the image's call sites by the fastest design's profile, named by caller, callee and ordinal ...
- `jit` - the JIT: hot words translated to x86 machine code from compiled stencils (engine/jit.c, engine/spn-stencils.c; x86 only)
- `jitexec` - EXECUTE native (`jitexec`: 0, 1; Iterations 476-488; JIT with jitx; enabled 477): through a helper (jit_exec) with a cache of three cells at each site; S" and ." as literals; cold calls (CR, ABORT, THROW) through the helper; a callee it cannot translate ...
- `jitfuse` - pairs as one stencil on the JIT (`jitfuse`: 0, 1; Iteration 507; JIT with jitx; enabled for seed 72 by the owner, 508): a literal into +, <, >, =, XOR, AND or OR, and I into + or 2@, copied as one stencil, never where the second is a branch target ...
- `jitimg` - the image's own words JIT candidates (evolve.py, Iteration 341)
- `jitinl` - one-operation words inline on the JIT (`jitinl`: 0, 1; Iteration 137; JIT with jitx; **dormant** until seed 39 has run): a call to a word of one operation and EXIT - 1+, 0=, 1- - is that operation in the caller (not one that branches, ends the word, or ...
- `jitk` - the JIT's stack cache (`jitk`: 0, 2, 3; Iteration 259; JIT designs): the top K cells stay in fixed registers across the copied code - tools/gen-jitk.py writes a variant of 16 hot data stencils (literal, DUP DROP SWAP OVER, + and immediate +, = > <, AND ...
- `jitloop` - (+LOOP) and (?DO) native (`jitloop`: 0, 1; Iteration 130; on the JIT; **dormant** - in LATE, not in EXPRESSED, until seed 39 has run): SPN's stencils for both, the scanner reading 160 bytes (its 64 cut both stencils: (+LOOP)'s 87 before either exit, ...
- `jitmul` - UM*, UM/MOD, SP@, ALIGNED and COUNT native, (ABORT") too with jitexec (`jitmul`: 0, 1; Iterations 472-488; JIT designs; enabled 474): stencils for the operations the applications' words stopped at (lab/evolve/jitapps.py) - PICK, CELLS, MOD chains; UM/MOD's ...
- `jittail` - tail calls as jumps on the JIT (`jittail`: 0, 1; Iteration 246; JIT designs): engine/jit.c - a call to a native word whose next operation is EXIT, or a BRANCH chain to one, is translated as a jump to it, so its ret returns to the caller and tail recursion ...
- `jitvar` - variable fetch and store given JIT stencils (evolve.py, Iteration 342)
- `jitx` - the JIT reaches further (`jitx`: 0, 1; Iteration 108; on the JIT): variables as literals, words without the JIT header translated once each, >R/R>/R@ in balanced words, a FILL stencil
- `kfast` - kernel words faster (`kfast`: 0, 1; Iteration 49; byte headers): NAME>BUF without its 32-byte zero fill, which the byte compare never reads (forth/cv8b-kfast.4)
- `kinput` - the input side (`kinput`: 0, 1; Iterations 54-55; with kfast): forth/cv8b-kinput.4 (REFILL's tab loop as TABS>BL; (PARSE) and PARSE8; ?STACK8) and SCAN, SKIP, TABS>BL, FILL, (PARSE), HASH, PLACE first among the format-10 names
- `klookup` - the whole lookup and numbers (`klookup`: 0, 1; Iteration 57; with kinput): forth/cv8b-klookup.4 ((FIND) and FIND8, (>NUMBER) and >NUMBER8, WORD8) and (FIND), (>NUMBER) first among the format-10 names
- `knumber` - NUMBER? as one opcode (`knumber`: 0, 1; Iteration 295): forth/cv8b-knumber.4, after klookup's overlay - (NUMBER?), the kernel's NUMBER? with BASE @ and DPL given (its failures 0 0 0: only INTERPRET calls it, and aborts or throws), and NUMBER?8, whose body ...
- `lto` - link-time optimisation (`lto`: 0, 1; Iteration 260; CV8 designs): the engine and its runtime compiled as one (-flto), so GCC inlines and drops across them; the JIT's stencils are compiled outside it - LTO changed their code and the JIT stopped translating ...
- `msc` - multi-state stack caching (`msc`): 0, 1 or 2 top items in registers, a dispatch table per state, each handler variant dispatching by the table of the state it ends in; generated from stack effects for 72 operations, the rest normalised to the one-register ...
- `nocet` - -fcf-protection=none (build.txt)
- `nocrossjump` - -fno-crossjumping, GCC only (build.txt)
- `nogcse` - -fno-gcse, GCC only (the compile line in build.txt)
- `noinls` - no inlining of small functions (`noinls`: 0, 1; Iteration 113): -fno-inline-small-functions
- `noreorder` - see lab/evolve/evolve.py, `grep -n "gene('noreorder'" lab/evolve/evolve.py`
- `opbody` - words an opcode replaced, [opcode EXIT] (`opbody`: 0, 1; Iteration 92): (FIND), (>NUMBER), THREAD-FIND, +!, ?DUP, as FILL and CMOVE (Iterations 50, 54)
- `opinline` - the [opcode EXIT] words among the primitives (`opinline`: 0, 1; Iteration 292): placed before (PRIMITIVES-END), where PRIMITIVE? asks by address, so the run-time compiler copies their opcode in place of a call - code compiled at run time (bubble's 2@ and ...
- `ops10` - format-10 opcodes (`ops10`): `EXECUTE`, `I`, `(DO)`, `+!`, `?DUP`, `UNLOOP`, `J`, and the loop words with an operand, `(LOOP)`, `(?DO)`, `(+LOOP)`, `(LEAVE)` - kernel colon words - and the short branches `?BRANCH8`, `BRANCH8` as opcodes, from the free ...
- `opt` - the optimisation level: O2 (absent), O3 or Os (clang: -Oz)
- `regpin` - the VM's registers pinned to machine registers (RELF.md, Iteration 364)
- `rtfuse` - run-time fusion: the compiler the image carries fuses pairs as the converter does
- `rtimm` - run-time immediates (`rtimm`: 0, 1, 2; Iteration 37; 2 - Iteration 175: without pairs, the overlay alone): with run-time fusion and spec imm, the compiler the image carries makes `n +` an ADDI and `SWAP n +` a SWAP+I in the code it writes ...
- `rtiplus` - I + fused in run-time code (`rtiplus`: 0, 1; Iteration 60; with rtloopall): a format-10 opcode I+, SUPER-TABLE's (I, +) -> I+, and forth/cv8-fuse-iplus.4 pointing LAST-OP at I's byte
- `rtloop` - run-time loops (`rtloop`: 0, 1; Iteration 41): the compiler the image carries emits the design's loop opcodes - (DO) (LOOP) (+LOOP) (?DO) (LEAVE), I J UNLOOP - each where it has one, 16-bit operands, no padding (forth/cv8-fuse-loop.4)
- `rtloopall` - rtloop compact (`rtloopall`: 0, 1; Iteration 43): with rtloop and all eight loop opcodes, a run-time loop compiler without fallbacks - one chain, one 12-byte table (forth/cv8-fuse-loopall.4)
- `spec` - specialised opcode families - var, tiny, small, imm, loc: variables, small literals and immediates as their own opcodes (GENES.md's CV8 table, "specialisation families")
- `supers` - superinstructions - the pairs listed, each one opcode (tools/gen-super.py)
- `swapi` - SWAP+I sure of a slot (`swapi`: 0, 1; Iteration 61; with 'imm'): SWAP+I first among the format-10 names
- `t2hot` - see lab/evolve/evolve.py, `grep -n "gene('t2hot'" lab/evolve/evolve.py`
- `t2wide` - the tag without its 3-byte call (`t2wide`: 0, 1; Iteration 95; in the tag, not multi-state): `10xxxxxx` 64 more one-byte codes (127), calls of 2 bytes (16 KB) and 4 (1 GB)
- `tag2` - the two-bit tag image format, relf's (FORMAT-TAG2.md)
- `tail` - **Retired at Iteration 456** - frozen off since Iteration 450 (12 of 12 removal votes over seeds 63-65, no loss in seed 66), its code removed; the gene kept in the genome, off, so identities hold. Was: tail-call threading (`tail`): every handler a function ...
- `tfind` - THREAD-FIND first (`tfind`: 0, 1; Iteration 52; with kfast): THREAD-FIND first among the format-10 names - seed 11 drew it from the pool 7 times in 1,425 designs
- `thinhdr` - one thread head in the header (`thinhdr`: 0, 1; Iteration 58; CV8): the header's 32 thread heads - read by the CV8 loader and never used, only SOD16 numbers calls - as a count of 1 and a zero head
- `threads` - the dictionary in 16, 32, 64 or 128 chains (evolve.py, Iteration 204)
- `tos` - the top of the data stack in a register (GENES.md's CV8 table; engine/vm-lab-tos.c)
- `varslot` - see lab/evolve/evolve.py, `grep -n "gene('varslot'" lab/evolve/evolve.py`

## For relf (RELF.md's adoption criteria)

- **The JIT is x86 only** (x86-64 and x86-32); relf's CV8 stays portable, so the four JIT designs show what x86 reaches
  and the six without it are relf's candidates as they stand. The JIT designs' ARMv7 figures are their JIT-off builds.
- **The images come from the lab's converter** (tools/layout.py), not relf's cross.4: what relf can take is mechanisms -
  opcodes, fused and specialised forms, the dictionary's chains, engine flags - each rebuilt in relf and measured on
  relf's own workloads with its tools (tools/relf-ab.sh, relf's bench-vm.py), as RELF.md requires. At Iteration 364 the
  C-engine-only flags (clang, -Os, pinned registers) did not transfer to relf's cv8.c; the instruction level is the offer.
- **The two-bit tag**: the JIT designs use it (tag2=1), the portable ones do not - their format is CV8 without the tag.
- **Not measured here**: relf's shell workloads, AArch64 and RISC-V. The lab's selection is generic Forth by design (RELF.md,
  the order of the work: phase 2 is seeing how these fit relf).

## The files

For each design, `ID/record.json` (its genome and the lab's record) and, at each width, `ID/cell8/` and `ID/cell4/`:
`engine` and `image.img` (statically linked; run `./engine image.img < program.fth` - names are upper case, `BYE`
ends it), `src/` (the engine's C source as compiled: vm.c and every file generated beside it), `build.txt` (each command
the lab's build ran, in order - the compiler line gives every -D), `check.txt` (the nine workloads against s6-cv8b at the
same width). `SHA256SUMS` covers every engine and image.

Rebuilt byte for byte from the repository at the commit named in the bundle: `python3 lab/evolve/pack-designs.py OUT
results/relf-designs-611.md c7c35f9c97,4ef851fd8e,06b188f45b,bac37f35a2,782f3ad7ff,690981ca5b,c2ef9488ff,a627b954c6,fb0d57c8a2,64a7345393` (in a built tree). The rest of the final set
and every reading behind these numbers: results/final-pick-chainCD-seed86.md and results/followup-pick-seed87.md.
