# The demoscene's and the IOCCC's techniques against the register (Iteration 727)

The owner (727): "please check demoscene and ioccc implementations, sometime they do really interesting optimizations".
Done as 713 and 717 did the early games and the esoteric languages: each technique found, where the lab already has it
(GOALS.md's register, the genes), and what is new - priced when it is. **One new candidate came out of it, priced and
proposed as a gene: a hash seed searched per image (`hashk`, below)** - crinkler's way of finding imports by hash and
brute-forcing its parameters per program, applied to the dictionary's chains. Everything else is in the lab already or
does not fit an interpreter measured by dispatches, bytes and pages.

## The sources

The demoscene: sizecoding.org (its Linux page: tiny ELF binaries, self-compiling droppers -
https://www.sizecoding.org/wiki/Linux), the in4k wiki (crinkler's techniques - https://in4k.github.io/wiki/crinkler; the
Linux tools smol, vondehi, dnload, oneKpaq - https://in4k.github.io/wiki/linux), Brian Raiter's "Teensy ELF" tutorial,
tmp.out's ARM32 ELF sizecoding (https://tmpout.sh/3/08.html). The IOCCC's winners that are interpreters, compilers,
virtual machines or emulators (https://ioccc.org/years.html): 1989 jar.2 (a compressed Lisp), 1990 and 1991 dds (a
compressed BASIC), 1992 buzzard.2 (FIRST and THIRD, almost Forth), 1996 august (a C subset compiler and its byte-code
interpreter, the byte code LZ-compressed), 2001 bellard (OTCC), 2006 toledo2 (8080), 2011 richards (a JIT for dc), 2012
tromp (binary lambda calculus), 2013 cable3 (IBM PC), 2018 mills (PDP-7/11), 2019 adamovsky (Unlambda), 2024 mills (the
Z-machine v3), kurdyukov3 (a gaming VM running Doom), macke (OpenRISC), carlini (4004), 2025 cable (SUBLEQ in 366 bytes of
C), ncw1 (GameBoy), ncw3 (Forth in Unicode and the C preprocessor). Read at the depth of their pages; the emulators'
sources were not read - nothing is claimed of their internals here.

## Each technique

| technique | where | here |
|---|---|---|
| A compressed executable or byte code, a tiny decompressor (crinkler, vondehi, oneKpaq; IOCCC 1989 jar.2, 1990-91 dds; 1996 august's LZ with a 255-byte window) | the register: compressed image and engine (236), the echo instruction - LZ77 executed (260) | covered: priced, not built - disk bytes, not the bytes that run; the owner's question whether the size counts them stays open |
| ELF headers: overlays, unused fields, one segment (Teensy ELF, smol, tmp.out's 84-byte ARM32 header) | the register: PT_GNU_STACK (251, 712), header overlays (712) | covered: one segment -48 B on every 8-byte engine, a constant; overlays 8 B, fragile |
| Relative calls and jumps made absolute (crinkler) | - | only for a compressor's model: with 236 |
| Sections ordered so like data sits together (crinkler) | the fixed data layout (713, open) | for compression no; for pages faulted it is the open item 3 |
| Tables made at start-up, not stored (sizecoding) | vm-lab.c's dispatch as offsets, the addresses made at the first entry (237) | covered; 16-bit offsets refused (the owner: no limit a developer could hit) |
| The start-up state used (registers and BSS zero) | the libc-free runtimes, BSS | nothing to measure |
| **Import by hash: names stored as hashes** (crinkler) | - | **rejected on paper**: a Forth's FIND must be exact - with 16-bit hashes a miss (a literal, a new name) matches one of the smallest's 314 names about once in 200 (314/65,536) and resolves to the wrong word; 32-bit hashes save little over 5-6-character names and lose WORDS' and SEE's names. Packed names (222-233) are the exact form, deferred |
| **Hash parameters brute-forced per program** (crinkler searches its model's parameters per intro) | - | **new - the gene `hashk`, priced below** |
| One instruction (2025 cable: SUBLEQ with an indirect bit, 366 bytes of C) | the register: minimal primitive sets (sectorforth, milliForth - 717) | the opposite of the dispatch count; rejected |
| A language bootstrapped from a few primitives in one memory array (1992 buzzard.2, FIRST to THIRD) | kernel.4 on the engine's primitives; sectorforth (717); the self-hosting compiler (666-722) | covered |
| Forth words as C functions, IMMEDIATE as macros, the preprocessor evaluating (2025 ncw3) | the tail gene's function tables; the JIT | nothing for an interpreter's image |
| One-pass code generation (2001 bellard) | the compilers' control-flow stack | nothing for the image or the engine |
| A JIT for a stack language (2011 richards) | engine/jit.c from compiled stencils | not read in detail |
| The Z-machine (2024 mills) | 713's early games | covered |

## hashk - the chain hash's seed searched per image

The kernel's chain hash is `v = len ^ b0<<1 ^ b1<<2`, masked to the chain count (tools/layout.py's `_wl_hash`; the same
in the engine's HASH and the Forth walkers). An XOR seed only permutes the chains, so the tunable form is multiplicative:
`((v * K) & 0xFFFF) >> (16 - log2 chains)`, K odd - one constant the converter would choose for the image's own names.
K was searched over every odd value below 65,536 on the held-out programs' lookups only (wordfreq, minif, brainless -
the project's rule), then priced on the workloads' token streams by chain-order-707.py's simulation - entries visited a
lookup, definitions going in front as they come (results/drafts/hashseed-727.py; reads only).

| design | chains | workload | today | chainorder (707) | K | K and chainorder |
|---|---:|---|---:|---:|---:|---:|
| smallest 219878ec89 (the lookup in Forth; threads 3 - 128 chains) | 128 | corpus | 3.40 | -6 % | -11 % | -16 % |
| | 128 | parse | 2.63 | -43 % | -19 % | -52 % |
| | 128 | the five programs | 3.26 | -26 % | -17 % | -35 % |
| | 32 | corpus | 12.30 | -7 % | -15 % | -34 % |
| | 32 | parse | 12.62 | -45 % | -38 % | -61 % |
| | 32 | the five programs | 10.55 | -34 % | -18 % | -39 % |
| portable-fastest d727605472 (FIND in C; threads 0 - 16 chains) | 16 | corpus | 24.37 | -8 % | -5 % | -25 % |
| | 16 | parse | 23.75 | -47 % | -35 % | -59 % |
| | 16 | the five programs | 20.92 | -36 % | -14 % | -40 % |
| | 64 | corpus | 6.55 | -7 % | -8 % | -7 % |
| | 64 | parse | 6.12 | -45 % | -47 % | -51 % |
| | 64 | the five programs | 5.67 | -30 % | -14 % | -32 % |

Every chain count of both designs: results/drafts/hashseed-727.txt (the script's output, both runs).

**Read**: a searched K alone shortens the walk by 5-15 % on the corpus (most of whose walk is misses - literals - which
chainorder cannot shorten and a better spread can) and 4-47 % on parse, with no link changed; with chainorder the two
compound - a third to three fifths of the walk at most chain counts. Out of sample: K is chosen on programs the
selection never runs. One case does not compound (portable-fastest's 64 chains on the corpus, -7 % either way): the
search's objective is the held-out three's, not the corpus's.

**Its price, before a build**: the engine's HASH (and the k genes' C lookups) a multiply and a shift - a few bytes; the
Forth walkers' hash word a literal, `*` and a shift; K in the image's header (two bytes) or compiled in; layout.py, the
cross compiler and the run-time HEADER hash the same way, so a user definition lands where FIND looks. Visits are not
time: in a C walk a visit is a few instructions, in a Forth walk several dispatches - the prototype counts instructions
(callgrind) and dispatches (VMPROF), as chainorder's is to. Proposed as a gene, 0/1, beside chainorder; built in the
reopened search's preparation (HANDOFF.md, 727), chainorder's prototype and this one together - both change how a name
is placed in a chain.
