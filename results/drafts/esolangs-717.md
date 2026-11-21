# What the esoteric languages lend the search (Iteration 717)

The owner: "do a deep dive and check esoteric languages like befunge and see if you can get some reusable ideas from
there". Read here: FALSE (Wouter van Oortmerssen, 1993: a Forth-like language whose compiler is 1,024 bytes of 68000 code -
the language Brainfuck and Befunge came from), Brainfuck (Urban Müller's 240-byte Amiga compiler; the optimising
compilers - Mats Linander's 2015 survey, Wilfred Hughes's bfc, esotope - and the self-compilers, awib and Daniel
Cristofani's), Befunge-93 and Funge-98 (Chris Pressey; Adrian Toncean's befunjit, Heikki Kallasjoki's ff3, the reference
bef2c, the fingerprints), the golfing languages (05AB1E's dictionary-compressed strings; golfing as LZ with a fixed
dictionary), Joy and Unlambda (quotations and combinators), and the size-coders beside them - sectorforth (512 bytes,
eight primitives) and milliForth (336 bytes). Each technique was set against the genes and GOALS.md's register first.
Most are here. One is not, and it is the text interpreter's: **a Forth looks every token up before it tries it as a
number, so every literal walks a whole chain and misses - FALSE and Brainfuck decide by the first character. A plain
decimal literal converted before the lookup (while no name is one) takes out about half of the corpus's and parse's
dictionary walk, for a few tens of bytes.** Priced by count (results/drafts/esolangs-717.py); proposed as a gene for the
reopened search.

## The one that pays: literals before the lookup (FALSE's first-character dispatch)

FALSE's compiler acts on a character: a digit starts a number, a letter is one of 26 variables, the rest are operators -
no dictionary to search. Brainfuck has eight commands and no names. A Forth must look a token up first, because a
definition named like a number takes precedence; so a literal is a lookup that fails - its chain walked to the end - and
then >NUMBER.

**What the misses cost** (measured before, on seed 43's smallest design at 16 chains - the chains today's small end still
takes: threads=3 on 3456fc28b2, 219878ec89 and 90273721a1, the lookup in byte code, klookup=0): the lookup - NEXT-NFA8,
SEARCH-WORDLIST, NAME=?, FIND, NAME>BUF, HASH - is 66.3 % of the corpus's dispatches, 69.0 % of parse's and 35.6 % of the
kernel's (results/price-stencils-bloom.md); names not found are 57 % of the corpus's walk and 49 % of parse's, "numbers and
names being defined" (results/price-lookup-cache.md).

**How many of the misses are literals** (results/drafts/esolangs-717.py: the token stream as 221's model made it, comments
and strings out - its counts give 221's lookups, 6,643 x 5 passes = 33,215 against 33,150 and 32,004 x 3 = 96,012
against 96,009):

| source | tokens | plain decimal literals (-?[0-9]+) | names defined |
|---|---:|---:|---:|
| the kernel workload (extend.4, cross.4, kernel.4) | 4,126 | 305 (7.4 %) | - |
| the corpus (tests/corpus/core.fth) | 6,643 | 1,901 (28.6 %) | 147 |
| parse (held out; bench/parse.fth) | 32,004 | 16,000 (50.0 %) | 0 |
| the apps (lab/evolve/apps) | 4,572 | 496 (10.8 %) | - |

On the corpus 93 % of the misses are literals (1,901 against 147 names defined), on parse all of them. A number-first path
takes out about 53 % of the corpus's walk and 49 % of parse's, and the hash and name buffer of every literal's lookup
besides - **on the order of a third of the corpus's and parse's dispatches** on an interpreted 16-chain design, less where
the lookup is C (klookup=1) or the chains more. The kernel workload's literals are 7.4 % of its tokens (a share of its
35.6 %), the apps' 10.8 %. 238's Bloom filter would have done about as much for ~350 bytes and lost to the threads gene
(64 chains: three quarters of the walk for 384 bytes more than 16, a trade evolution declines at the small end); this is
perhaps a tenth of either's bytes.

**The rule that keeps it a standard Forth**: a token of the form -?[0-9]+ is converted first only while no name in the
dictionary has that form. The converter checks the image's names (none today: forth/*.4 define none - the script's four
hits are `CREATE 0 ,` inside definitions); the header-making word sets a flag when a program defines one, and from then
the lookup comes first again. Every base stays right: below base 10 a digit may not convert and the token falls back to
the lookup (and its error); prefixes ($ # % 'c'), doubles (a trailing dot) and digit-led names (2DUP, 1+, 0= - 126 and
197 of them in the kernel's and the corpus's tokens) keep the lookup, a failed >NUMBER on one or two characters their only
cost. Output and the kernel workload's image do not change.

**The price**: the digit test (a short loop, or in knumber=1 designs the C NUMBER's own scan returning early) and the flag in
the header word - a few tens of bytes. **Proposed: a gene `numfirst`** for the reopened search, beside chainorder and the
queued genes (jitdead, fixenv, jitfew) - the owner's call; its first measure the profiler's dispatches on 219878ec89 and
d727605472 over the corpus, kernel and parse, then the held-out programs (the corpus is the CORE tests, literal-heavy; the
apps' share is a third of it). Not before the roles ship: no gene changes under chain C's readings.

## Checked - here already

| technique | from | here |
|---|---|---|
| contraction (`+++` as Add 3) | the Brainfuck optimisers (Linander; bfc; esotope) | the literal folds, rtimm's immediate forms, the specialisations |
| clear, copy and multiply loops as one operation | the same | idioms of a byte tape; a Forth's are words already (ERASE, FILL, MOVE, `n *`) |
| scan loops by memchr (dbfi.b over 3 times faster) | Linander | the text interpreter's scan is not its cost - the walk is (above); kinput puts the input words in C |
| operation offsets (pointer moves deferred to a block's end) | the Brainfuck optimisers | IP and stack-pointer updates combined in superinstructions (Ertl and Paysan's, deferred; GCC combines within one), stack state in the JIT's translator (deferred) |
| speculative execution - the program run at compile time to its first input | bfc | the image is that snapshot already; the workloads compile their source each run by design |
| static paths compiled, `p` invalidating the paths through its cell | befunjit (lazy and eager runtimes) | the JIT's trigger byte translates a word at its first call; a Forth writes code only while compiling - load-time threading with invalidation, deferred (register) |
| four handler pointers a cell, one a direction: the state in the dispatch | ff3 | multi-state caching - built, lost (register) |
| each cell as a C snippet, control through them as the interpreter's | bef2c | the engine's own threaded code |
| fingerprints: instruction sets loaded on demand | Funge-98 | the converter drops dead words; a generic Forth carries its wordsets |
| 26 one-letter variables, one-byte access | FALSE | rtvar's slots (VAR-OPS: a data word's @ and ! as one operation) |
| a compiler that compiles itself (awib; Cristofani's 904 bytes) | Brainfuck | self-hosting, phase 6 (cross-cv8.4) |
| ELF header tricks (Brian Raiter's 199-byte Linux compiler) | Brainfuck | ELF header overlays checked, nothing for us (712) |
| a fixed dictionary of built-ins - golfing as LZ with a pre-defined dictionary; 05AB1E's words from a dictionary | the golfing languages | one-byte codes by use (ops10, the tag's ranking - 713's Mesa); names packed 6 bits a character (priced, deferred); the LZSS'd image and the echo instruction (priced, the owner's) |
| eight primitives and the rest in Forth | sectorforth, milliForth | ops10 and the escape gene choose per word which are opcodes - the trade sectorforth makes by hand is the evolver's |
| quotations and combinators instead of branches; a rewriting system | Joy, Unlambda | branches are cheaper in a byte-code VM; the rewriting superoptimizer measured at 707 (11 bytes) |
| a Brainfuck interpreter as a workload | dbfi | brainless, held out (674) |

## Priced, not proposed

- **A one-byte conditional skip** (Befunge's `#`; PDP-8's SKP, PIC's BTFSC) for an IF whose body is one word: kernel.4 13 of
  84 IFs, coreext.4 6 of 90, the five programs 4 of 59 (ELSE x THEN 6, 9, 10); 2 bytes each where the word is a one-byte
  opcode (a call's length would need the skip to decode it) - at most ~50 bytes, a third of 713's short branches (about
  150 bytes, priced, not proposed), which cover it.
- **The kernel's messages as codes** (FALSE: "there are no error messages"): 211 bytes of text in kernel.4 (155 in 11
  ABORT"s, 56 in 6 ."s) and 50 in coreext.4; as THROW codes at most ~200 bytes, 0.9 % of the smallest - user-visible and
  in the workloads' reference outputs (OK, Redefining:): the owner's call, as 709's imagemsg was.

## Closed

Malbolge, INTERCAL's COME FROM, Whitespace, Piet, Thue, FRACTRAN: nothing a byte-coded Forth can use.

Sources: van Oortmerssen, the FALSE manual (strlen.com/files/lang/false/false.txt); esolangs.org's FALSE, Befunge and
Funge-98 pages; Linander, "Optimizing Brainfuck" (calmerthanyouare.org, 2015); bfc's optimisations (docs.rs/crate/bfc);
Müller's original distribution (gist rdebath/0ca09ec0fdcf3f82478f); Toncean, befunjit (github.com/adrianton3/befunjit);
Kallasjoki, ff3 (gist fis/6898996); catseye/Befunge-93 (bef2c); Pressey, the Funge-98 specification; O'Dwyer's Funge-98
notes; sectorforth (github.com/cesarblum/sectorforth); milliForth (github.com/fuzzballcat/milliForth); esolangs.org's
05AB1E page; iczelia, "jcram golf"; von Thun's Joy papers.
