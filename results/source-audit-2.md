# The Forth sources audited again - missed speed and size (Iteration 281)

Searched, not recalled (prompts/02): every word's largest share of the selection
workloads' dispatches over five reference designs, the JIT off
(lab/evolve/hotwords-v1.json); each hot word checked against what a gene can reach
- the ops10 pool, the tiny family, opbody, the k-overlays, the JIT; exact
per-workload counts for what none reaches (lab/evolve/word-cost.py); the smallest
design's image by body size against the same profile. Read first: word-audit.md
(Iterations 131, 144), loop-audit.md (203), forth-sources.md (116).

## Found: 2@, 2! and DEPTH - hot, and no gene reaches them

Iteration 131 listed 2@ and 2! among the heavy words "whose cost is the dispatch,
which the opcode genes (ops10, opbody) and the JIT answer" - but neither is in the
ops10 pool, the tiny family or opbody, so no design can choose that answer. (1-,
listed with them, is in the tiny family; so are > and 0=.) The calls come from
code compiled at run time: bubble's inner loop (bench/bubble.fth: 2@ three times,
2! once) and tester.fr's DEPTH in the corpus (ten uses), calling the kernel's
colon words - 2@ `DUP CELL+ @ SWAP @ ;` and 2! `SWAP OVER ! CELL+ ! ;`, six
dispatches a call each; DEPTH `SP@ S0 @ SWAP - CELLSHIFT-TOK RSHIFT ;`, seven.
The dispatches inside them, exact (word-cost.py; c9369657e4 is seed 47's fastest
design without the JIT):

| design | workload | dispatches | in 2@ | in 2! | in DEPTH | all of them |
|---|---|---|---|---|---|---|
| s6 | kernel | 5710023 | 0 (0.0%) | 0 (0.0%) | 6786 (0.1%) | 0.1% |
| s6 | fib | 59275129 | 0 (0.0%) | 0 (0.0%) | 192 (0.0%) | 0.0% |
| s6 | corpus | 30862167 | 50 (0.0%) | 25 (0.0%) | 236790 (0.8%) | 0.8% |
| s6 | loop | 92149651 | 0 (0.0%) | 0 (0.0%) | 210 (0.0%) | 0.0% |
| s6 | bubble | 32503250 | 4010220 (12.3%) | 1301280 (4.0%) | 396 (0.0%) | 16.3% |
| s6 | ackermann | 12738411 | 0 (0.0%) | 0 (0.0%) | 318 (0.0%) | 0.0% |
| 7535695a36 | kernel | 8544130 | 0 (0.0%) | 0 (0.0%) | 7917 (0.1%) | 0.1% |
| 7535695a36 | fib | 59315341 | 0 (0.0%) | 0 (0.0%) | 224 (0.0%) | 0.0% |
| 7535695a36 | corpus | 58778470 | 50 (0.0%) | 25 (0.0%) | 276255 (0.5%) | 0.5% |
| 7535695a36 | loop | 92180046 | 0 (0.0%) | 0 (0.0%) | 245 (0.0%) | 0.0% |
| 7535695a36 | bubble | 33092362 | 4010220 (12.1%) | 1301280 (3.9%) | 462 (0.0%) | 16.1% |
| 7535695a36 | ackermann | 12792558 | 0 (0.0%) | 0 (0.0%) | 371 (0.0%) | 0.0% |
| c9369657e4 | kernel | 1998614 | 0 (0.0%) | 0 (0.0%) | 6786 (0.3%) | 0.3% |
| c9369657e4 | fib | 45782217 | 0 (0.0%) | 0 (0.0%) | 192 (0.0%) | 0.0% |
| c9369657e4 | corpus | 4529779 | 50 (0.0%) | 25 (0.0%) | 236790 (5.2%) | 5.2% |
| c9369657e4 | loop | 20032723 | 0 (0.0%) | 0 (0.0%) | 210 (0.0%) | 0.0% |
| c9369657e4 | bubble | 12759474 | 4010220 (31.4%) | 1301280 (10.2%) | 396 (0.0%) | 41.6% |
| c9369657e4 | ackermann | 12693978 | 0 (0.0%) | 0 (0.0%) | 318 (0.0%) | 0.0% |

The price. An opcode saves at most a word's own dispatches - bubble -16% (s6, the
smallest) to -42% (c9369657e4), the corpus up to -5%. But run-time code CALLS the
words; it meets an opcode only through the word's body, opbody's [opcode EXIT] -
two dispatches of six, so two thirds of those counts (bubble -11% to -28%) -
unless the run-time compiler learns to emit the opcode for the call, as rtloop
does for the loop words. On the selection's geometric mean, c9369657e4 at
opbody's two thirds: about -5% of dispatches - dispatches, not time; JIT designs
translate that code, and gain less: the laptop's to say.

The cost: three handlers in vm-lab.c and through every generator (tens of bytes
each), three entries in OPS10_POOL and OPS10_LABEL, the bodies' patterns in
sod16's ops10_at, opbody's list (evolve.py OPBODY, layout.py _OPB) - offered as
genes, evolution weighing the handlers' bytes against the speed. A patch for after
seed 48, checked as the others: engines-check, the gate, gene-equiv.py for ids.

## Rechecked, standing

- The lookup (NEXT-NFA8, SEARCH-WORDLIST, FIND, NAME=?: up to 19% of what the
  interpreter dispatches) - threads (204), klookup, THREAD-FIND and (FIND) as
  opcodes; a cache priced (221).
- (LOOP), (+LOOP), I, SCAN, CMOVE, FILL, ?DUP, HASH, SKIP - in the ops10 pool;
  >, 0=, 1+, 1- - the tiny family.
- NUMBER? (2.1%; at 185 bytes the largest code body): ~20 dispatches a digit. A
  table was rejected for its 256 bytes in Iteration 144, before "trade-offs as
  genes" was the standing rule - it could be offered as one; (>NUMBER) as an
  opcode covers designs with klookup already.
- INTERPRET (4.8%), PARSE-WORD, WORD, ?STACK (1.5%) - kinput's opcodes ((PARSE),
  SKIP, SCAN) take their loops; what is left is control flow.

## Size: nothing new

The smallest image (7535695a36): 8,696 bytes - code bodies 4,867, data 1,064,
headers and padding 2,765 (32%). The largest bodies are words the system needs
(NUMBER? 185, READ-LINE 168, HEADER 153, INTERPRET 109, THROW 104). 42 words run
in no workload of the five designs (672 bytes, 14% of the code) - error paths and
file words, required; factor's level 1 already shares their repeated code. The
headers stay the largest lever, and they are in GOALS.md's register, the
owner's: packed names, hidden internal names.

## Recalled against searched (prompts/02)

| recalled from memory | here |
|---|---|
| superinstructions | supers |
| stack caching, multi-state | tos, msc |
| threading variants | tail, d256, sharedcall |
| inlining | hotinl, jitinl |
| tail calls | jittail; Forth tail calls priced (89) |
| specialised opcodes | spec, ops10, tiny, opcall |
| literal folding, immediates | fold, folds, rtimm |
| dispatch replication | gotodup |
| native code | the JIT and its genes, SPN |
| dictionary hashing | threads |
| a lookup cache | priced (221) |
| packed and hidden names | the register (the owner's) |
| factoring repeated code | factor |
| short branches | BRANCH8 and the tests' short forms |
| profile-guided order | t2hot, the tag's ranking |

Fifteen recalled, fifteen built, priced or in the register: none new. The search
found three: 2@, 2! and DEPTH uncovered (new); NUMBER?'s table, an old rejection the
standing rule reopens; the headers' 32% (the register).

## Built (Iteration 290): the after-seed-50 batch, patch 1

2@ and 2! as opcodes, in the ops10 pool and opbody's list (results/pending/ORDER.md);
DEPTH left out - its handler would have to agree with the kernel's S0 exactly, through
ABORT and saved images. Measured with word-cost.py on c9369657e4, the opcodes added:
bubble 12,759,474 -> 9,572,364 dispatches (-25.0%), the corpus 4,529,779 -> 4,516,324
(-0.3%) - about -4.7% on the selection's geometric mean, through opbody's [opcode
EXIT] bodies. The rest of bubble's - 2.1 million of the dispatches still inside the
two words - would go if the run-time compiler emitted the opcode for a call to them.
A design gets the opcodes only where its slots reach them: ops10_in hands the free
opcode slots out in its list's order, and evolution places the words.
