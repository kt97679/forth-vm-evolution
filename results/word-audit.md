# Every word, audited - the sources and the weights (Iteration 131)

The first step of results/word-audit-plan.md: the other Forths' sources, newer online where they
exist (the owner: check online; else the collection), their licences; and every kernel word weighed
by what it costs under the selection, so the comparison starts where the cost is.

## The sources

Fetched to the VM, not into the repository (their licences differ; the commits are the record).

| Forth | where | commit, date | licence | use here | in the collection |
|---|---|---|---|---|---|
| pForth | github.com/philburk/pforth | e561763 2026-07-28 | 0BSD-style | code | PFTHPC19 (v19, 1990s) |
| FICL | github.com/jwsadler58/ficl (its author) | 50c54d6 2026-06-12 | BSD-3-Clause | code | ficl202 (2.02) |
| ueForth / ESP32forth | github.com/flagxor/ueforth (eForth's successor) | d8376db 2026-09-26 | Apache-2.0 | code | eForth 1.0 (1990), lx-eforth, e4a |
| jonesforth | github.com/nornagon/jonesforth | d97a25b 2022-03-10 | public domain | code | - |
| zForth | github.com/zevv/zForth | 41db72d 2025-08-15 | MIT | code | - |
| Retro | github.com/crcx/retroforth | 7d23972 2026-09-11 | ISC | code (not a standard Forth) | - |
| lbForth | github.com/larsbrinkhoff/lbForth | 912433b 2023-02-11 | GPL-3 | ideas only | - |
| the Forth 2012 standard | github.com/Forth-Standard/forth-standard | 79bd531 2026-09-05 | none stated | ideas (reference implementations) | - |
| F83 (Laxen, Perry) | the owner's collection | - | public domain | code | Open Source - 8086 Forth 83 2.1.0 (no newer) |
| cmFORTH, FIRST/THIRD, Itsy, 3ins4th | the owner's collection | - | not stated | ideas | - |
| gforth, SP-Forth, bigFORTH, ciforth, SOD32 | the owner's collection | - | GPL | ideas only | - |
| RelF | github.com/kt97679/relf, the collection | - | the owner's | code | RelF 0.1-0.3, relf_dev |

Newer online: pForth, FICL (4.x from its author, against 2.02), eForth (ueForth), and three
not in the collection - jonesforth, zForth, Retro. Nothing newer for F83; the rest from the collection.

## The weights

Profiling builds (VMPROF, exact) of hand-made s6, the front's fastest (38446e6c09, seed 37, the JIT)
and its smallest (cd6c94b30d), on the six selected workloads; each dispatch counted to the kernel
word whose bytes hold it (the converter's map), a word's weight the mean of its shares of the six -
the equal weighting of the speed score. Kernel words carry 60% of s6's dispatches (the rest is code
compiled at run time), 60% of the smallest's, 70% of what the fastest still interprets (its JIT runs
fib, loop and its translated words natively - not counted, so its weights are the interpreter's).
**17 words carry 90% of the kernel words' share on s6 and on the smallest, 41 on the fastest; the
three sets together are 51 words** - the audit's order:

| word | bytes | s6 | fastest | smallest |
|---|---|---|---|---|
| INTERPRET | 93 |  | 11.36% |  |
| FILL | 24 | 10.42% |  | 10.00% |
| (LOOP) | 23 | 9.50% |  | 9.10% |
| (+LOOP) | 36 | 7.54% |  | 7.42% |
| PARSE-WORD | 47 | 0.91% | 7.10% | 1.00% |
| 2@ | 5 | 2.03% | 6.04% | 2.00% |
| NEXT-NFA8 | 65 | 3.41% |  | 5.34% |
| I | 4 | 5.08% |  | 4.93% |
| ?STACK | 33 |  | 3.72% |  |
| REFILL | 105 | 1.77% | 3.58% | 1.90% |
| SEARCH-WORDLIST | 71 | 3.35% |  | 3.30% |
| CMOVE | 30 | 2.50% |  |  |
| NUMBER? | 115 |  | 2.25% |  |
| 2! | 6 | 0.79% | 1.96% | 0.78% |
| HERE | 4 |  | 1.96% |  |
| COLD | 85 |  | 1.87% |  |
| SCAN | 27 | 1.42% |  | 1.48% |
| NAME=? | 32 | 1.45% |  | 1.48% |
| CMOVE> | 32 |  | 1.47% |  |
| 0= | 2 | 1.29% | 1.36% | 1.29% |
| > | 2 |  | 1.36% | 0.81% |
| WORD | 30 |  | 1.34% |  |
| >NAME | 8 |  | 1.31% |  |
| 1- | 2 | 1.27% | 1.29% | 1.27% |
| COMPILE, | 66 |  | 1.14% |  |
| FIND | 63 | 0.86% |  | 0.94% |
| HEADER | 169 |  | 0.92% |  |
| 1+ | 2 | 0.68% | 0.92% | 0.69% |
| COMPILE,8 | 73 |  | 0.86% |  |
| SUPER-OP | 51 |  | 0.76% |  |
| C, | 9 |  | 0.74% |  |
| INCLUDE-FILE | 64 |  | 0.72% |  |
| CALL, | 62 |  | 0.69% |  |
| SMALL-LIT? | 84 |  | 0.65% |  |
| * | 2 |  | 0.63% |  |
| >IN | 16 |  | 0.62% |  |
| ; | 55 |  | 0.61% |  |
| ALLOT | 4 |  | 0.60% |  |
| BL | 2 |  | 0.55% |  |
| IMM+ | 102 |  | 0.49% |  |
| OP, | 7 |  | 0.49% |  |
| PARSE | 29 |  | 0.42% |  |
| PICK | 7 |  | 0.41% |  |
| LITERAL | 35 |  | 0.40% |  |
| W, | 23 |  | 0.40% |  |
| CONTEXT | 48 |  | 0.40% |  |
| W@ | 9 |  | 0.40% |  |
| NAMEBUF | 48 |  | 0.39% |  |
| (POSTPONE) | 23 |  | 0.34% |  |
| LIT, | 90 |  | 0.33% |  |
| DP | 16 |  | 0.33% |  |

## Seen already

- **FILL through NAME>BUF.** `NAMEBUF 32 0 FILL 32 MIN NAMEBUF PLACE`: every dictionary lookup
  zero-fills 32 bytes, a byte at a time in a Forth loop - on s6, FILL is 35% of the kernel workload's
  dispatches and 27% of the corpus's (cross.4 also clears its 64 KB target image with it, once a
  run). kfast replaces this path, which is why the fastest design does not show it - 240 of seed
  37's 242 front designs have kfast - but s6, the yardstick, and every design without it pay it.
  pForth, FICL and F83 have FILL in C or assembler; eForth's is a FOR NEXT byte loop.
- **(LOOP), (+LOOP), I** - 22% of s6's share: user loops on designs without the loop opcodes
  (ops10); evolved designs mostly have them; s6 does not.
- **The dictionary search** - NEXT-NFA8, SEARCH-WORDLIST, NAME=?, FIND: ~9% on s6 and the smallest.
- **The interpreter** - INTERPRET, PARSE-WORD, ?STACK, REFILL, NUMBER?, WORD, HERE: the fastest
  design's bytecode. **COLD**, 1.9% of the fastest's: start-up, in every timed run.

A kernel change moves s6, the yardstick, and every design without the matching k-gene; as an overlay
gene, s6 and the recorded designs stay as they are - the plan's rule (4).

## Batch 1 - NAME>BUF (Iteration 132): a waste, not a dispatch cost

**Ours.** `NAMEBUF 32 0 FILL 32 MIN NAMEBUF PLACE` - 32 bytes zeroed a byte at a time, for every
lookup. The search compares names a cell at a time, so the buffer needs zeros only where the
stored names have padding (the name's last cell) and in the cell after (where the compare finds
the name's end - the first cell that differs must be that one).

**Theirs.** eForth's PACK$, used for every name it parses: the count, then one zero cell at the
string's end, then the string - `2DUP C! 1 + 2DUP + 0 SWAP ! SWAP CMOVE` (the collection's
EFORTH.SRC). The same idea; its compare counts cells, so it needs no cell after. pForth and FICL
compare bytes and need no padding; kfast (Iteration 51) went that way here (NAME>BUF8, "no
padding: nothing reads past it").

**The candidate** - two cells zeroed, then the name:

    : NAME>BUF ( c-addr u ---)
      32 MIN DUP 1+ ALIGNED NAMEBUF +  0 OVER !  0 SWAP 1 CELLS - !  NAMEBUF PLACE ;

and NAMEBUF one cell larger (`32 ALLOT-T`, not 28): the cell after a 31-character name lies at
bytes 32 to 32+cell, past the old buffer at both widths - the old code *read* it there (harmless);
the candidate writes it, and without the larger buffer the 4-byte build broke (it zeroed what
followed NAMEBUF while the shell loaded).

**The price** - exact, s6 built from a scratch clone with both changes (reseeded, both widths;
run-tests PASS, 7 of 7 IDENTICAL):

| workload | dispatches before | after | after/before |
|---|---|---|---|
| kernel | 9,252,139 | 6,625,636 | **0.716** |
| corpus | 47,357,767 | 34,713,117 | **0.733** |
| fib, loop | | | 1.000 |
| bubble, ackermann | | | 0.998 |

s6's image +8 bytes. **The owner's decision**: (a) in the kernel - s6, the yardstick, does 27-28%
fewer dispatches on two of the six workloads, so every design's ratio to it shifts (a
measurement-like change: alone, between runs, after seed 39); or (b) an overlay gene - s6 and the
recorded designs unchanged, but it would reach almost none of them (kfast has 240 of seed 37's 242
front designs past this path). The recommendation is (a): an equivalent, shorter path, one latent
read past a buffer fixed, and the shared kernel better for everything built from it.

**The rest of the heavy words, seen in this pass**: (LOOP), (+LOOP), I, 2@, 2!, 0=, 1-, 1+, >
are already minimal colon definitions (or single operations) - their cost is the dispatch, which
the opcode genes (ops10, opbody) and the JIT answer, not a better definition. The dictionary search
(NEXT-NFA8, SEARCH-WORDLIST, NAME=?, FIND) has kfast's and klookup's alternatives. Next to read
closely: CMOVE and CMOVE> (byte loops), REFILL's tab loop, the interpreter's ?STACK, NUMBER?, and
COLD (1.9% of the fastest's interpreted dispatches - start-up, in every timed run).

## Core or extension (Iteration 138)

The owner: the kernel holds core words only, the base everything else extends;
the size objective is the kernel's. A source-level census of kernel.4 - every
word it defines, its standard word set (the standard's own sources), and who
names it: the kernel itself, the kernel workload (extend.4, cross.4), the
workloads (the CORE corpus, bench/), the shell, the other extensions.

269 words: 180 standard (CORE and CORE EXT 151, FILE 17, DOUBLE 4, MEMORY 3,
STRING 2, SEARCH 2, TOOLS 1), 89 not. **24 non-standard words are named
nowhere in the kernel or the workloads**; four of them - LIT, BRANCH, ?BRANCH,
NOOP - are primitives the compiler lays down by opcode, not by name, and stay.
The other 20 are extension words in the kernel:

| words | used by | |
|---|---|---|
| FORK EXECVE WAITPID PIPE DUP2 GETENV SETENV UNSETENV SYS-EXIT CHDIR GETCWD SYS-ARGC SYS-ARG GETPID GETPWHOME GETFSIZE SETFSIZE | shell.4 only | the shell's seventeen - sysc's |
| SYSTEM | nothing | a primitive and its handler (214 bytes) nobody calls |
| A/O | shell.4, once (`>>`) | an access mode only the shell's append uses |
| CHAR- | nothing | |

Their headers are some 300-400 bytes of every kernel image. Moving them out
meets sysc being a gene: an engine without it keeps the seventeen handlers,
and the shell finds them by the names the kernel declares. The principle's
own end is one model - every engine with SYSCALL, the kernel declaring it
alone, the shell always loading forth/shell-sysc.4 - which reaches all six
engines, the cell stage's relf.c among them. The owner's decision.

## Batch 2 - the last heavy words (Iteration 144)

**SKIP and SCAN - built, a pending patch.** Every word the interpreter parses
goes through them, and they moved on a character with `1+ ROT ROT SWAP 1- SWAP`
- about 17 dispatches a character. Now the delimiter waits on the return stack
and `1 -1 D+` - the owner's own idiom, from his ackermann - moves the address
up and the length down in one double add (it cannot carry: that would need an
address at the top of memory):

    : SCAN ( c-addr u c -- c-addr' u' )
      >R BEGIN DUP WHILE OVER C@ R@ = 0= WHILE 1 -1 D+ REPEAT THEN R> DROP ;

On s6, after NAME>BUF (a scratch clone; reseeded, both widths, run-tests PASS,
7 of 7 IDENTICAL): the kernel workload -2.3%, the corpus -1.7%, parse (held
out) -1.4%, the rest unchanged; s6's image 8 bytes smaller.
results/pending/skipscan-after-seed39.patch, with NAME>BUF's or alone.

**Not worth a kernel change**, read and counted:
- **CMOVE, CMOVE>** - 20 dispatches a byte, 17 at best in this Forth; -15% of
  a 2.5% share is 0.4%, and the k-genes give evolved designs CMOVE as an
  operation already.
- **?STACK** - a few dispatches cheaper against precomputed bounds; it
  matters only on the JIT designs, at 3.7% of what they still interpret.
- **NUMBER?, DIGIT?** - ~20 dispatches a digit; a lookup table would be
  faster and cost 256 bytes of every kernel image, against the size objective.

**REFILL's tab pass - a decision, not built.** A full pass over every source
line turns tabs into spaces - 7.3% of s6's kernel workload. Only parsing that
treats any control character as a space delimiter (the standard allows it)
removes the pass, and that changes behaviour: a tab inside a string literal
would stay a tab. kinput's TABS>BL operation already serves evolved designs.

## Batch 2, revised - tab-free parsing (Iteration 145)

The owner: a tab is a space to the parser, as the standard allows - no need to
make it one. And nothing in this repository's sources holds a single tab: the
pass REFILL made over every line (7.3% of s6's kernel workload) never changed
a byte here. **results/pending/parsing-after-seed39.patch replaces the SKIP/SCAN
patch**, eight files:

- the kernel: SKIP and SCAN by `1 -1 D+`, a space delimiter taking every
  control character (a separate loop - other delimiters, control characters
  among them, `0 WORD` style, still match exactly); REFILL without its pass;
- kinput's REFILL8 without TABS>BL (TABS>BL stays defined: genomes name it);
- the C operations for SCAN, SKIP and (PARSE) - and they are in three places:
  vm-lab.c, and gen-tos.py's and gen-msc.py's own copies for their engines;
- tools/sod16.py's expected bodies for SCAN and SKIP;
- tests/core/tabs.fth and its section in run-tests.sh.

**Two catches.** The converter makes a word its C operation only if its body
is exactly the expected one, and the evolver kills a design whose isn't - the
SKIP/SCAN patch alone would have killed every kinput design, most of the front
(found building seed 37's fastest; validate's stages carry no kinput). And with
vm-lab.c's operations changed, half of a front sample still read a tab as part
of a word: the register-cached and msc engines take gen-tos.py's and
gen-msc.py's copies. All three agree now.

**Proved**: the tab test - tabs between words and leading, in a definition,
kept in a string (9, not 32), in an EVALUATEd string, before CHAR and a
comment - right on all 22 hand-made stages at both widths and 20 front designs
(kinput 19, opbody 20, the JIT 8), every one through the gate; its negative
control, the file with X for tab, does not give the answers; run-tests PASS,
7 of 7 IDENTICAL. **Priced** on s6 after NAME>BUF: the kernel workload -11.3%,
the corpus -5.4%, parse -3.7%; the image 8 bytes larger. With NAME>BUF, s6's
kernel workload -36%, its corpus -31%.

## Batch 3 - the size review of the long tail (Iteration 150)

The owner: the rarely-run kernel words, for bytes - compact definitions from
the permissive Forths where they help. Measured on the after-seed-39 batch
(all seven pending patches, reseeded): every word's bytes in s6's image and
the front's smallest's (cd6c94b30d), and its runs over all eight workloads.

**The definitions have little left to give.** The smallest image is 6,982
bytes: word bodies 4,356 (code 3,476, data 880) and headers - links, counts,
names, alignment - 2,626 (38%; the names alone 1,516). Code never run by any
workload: 151 bytes over 45 words - `lean` already leaves out the dump tool and
the compiler's copies. The kernel's rarely-run words are 20-60 bytes each
(ACCEPT 50, QUIT 46, INCLUDED 39) in an encoding averaging 24 bytes a word: a
fifth off the twenty largest would be ~120 bytes. The biggest rarely-run items
in s6 - INCLUDE-BUFFER, TIB, POCKET, 1,072 bytes of zeros - are layout, not
definitions: the bss gene already leaves them out of evolved images.

**The headers are where the bytes are, and nearly all are needed.** Of 293
words, 21 are named by no source that loads on top of the kernel (48 files:
the extensions, the cross-compiler, the overlays, the shell, the workloads and
tests) and are not standard - ~211 bytes of headers at most, ~150 in truth
(\, INTERPRET, the stack-pointer primitives are named by people if not by
files); headerless words would cost the converter and the dump real work. The
data: FORTH-WORDLIST's 32 threads are 272 bytes - 4-byte entries would save
~128, fewer threads would slow every lookup; the rest is state, ~20 variables
at 16 bytes.

**Priced, not built.** Headerless internals ~150 bytes (2%), half-width thread
entries ~128 bytes (2%) - each with work in the converter or FIND. For scale,
the batch already takes the smallest design from 20,630 bytes to 17,610 (-14.6%:
the image -192 by the kernel census, the engine -2,828 by the single SYSCALL
model and the tight ELF) and the fastest from 33,512 to 29,976 (-10.6%).
