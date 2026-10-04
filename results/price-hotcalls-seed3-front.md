# One-byte calls through a table of hot words - priced on seed 3's front

Iteration 13, development VM (1 CPU, GCC 13.3). Seed 3's database from the
Ryzen (1,310 designs, sha256 1d65de87b537a3d5...). Everything below is
measured on the image or counted by the engine's profiler unless marked
**modelled**; times on this VM are noise and are labelled so.

    lab/evolve/callsites.py 8dd8a7a146 60753a0eb0 f4a6dd9a13 550df563ee --db DB
    lab/evolve/image-ab.py  8dd8a7a146 60753a0eb0 f4a6dd9a13 550df563ee --env SOD16_OLD_BODYCHECK=1 --db DB
    lab/evolve/scan-bodycheck.py --db DB [--old]

## The framing (prompts/01)

| | |
|---|---|
| question | how many bytes of a front design's image would a band of one-byte calls save, net of their table, per opcode they take - and what would taking the opcodes cost? |
| cost model | image file bytes (the size objective): the image converted again with the top K targets as one-byte calls - exact, alignment and byte-header links included; **modelled**: the table, K entries at 2 bytes, charged to the image; the engine's handlers are not counted (the size measure never counts the engine - pairs and format-10 opcodes are not charged either) |
| degenerate answer | the table in the engine as a per-design constant: free in the size measure, a false saving - so the table is charged to the image; and every called word in the table: 122-155 targets, most called once - a byte saved for a 2-byte entry, a loss |
| budget | calls are 412-661 static sites, 432-681 bytes if every one shrank to a byte; dynamically 3.9-9.3% of dispatches; fib's and loop's calls are in code compiled at run time (99.7-99.9%), which no converter reaches |
| what would change it | the slots: all 34 free opcodes are taken (format-10 and pairs); byte headers (without them, bodies are padded to 8 and most single bytes vanish); calls before an inline operand (their alignment decides) |
| abandon if | the best K saves under 1% net, or only by taking slots that carry dispatches |

## The price (prompts/10)

Measured by the converter laying the image out again - the program is not
run, so nothing about its behaviour can move; the size is the converter's
own emission, the same code that emits every image. Net of the table:

| design | image | K = 4 | 8 | 16 | 32 | per slot at 32 |
|---|---|---|---|---|---|---|
| 8dd8a7a146 (no byte headers) | 13,352 | 24 | 40 | 96 | 136 (1.0%) | 4.2 |
| 60753a0eb0 | 9,686 | 104 | 129 | 156 | 221 (2.3%) | 6.9 |
| f4a6dd9a13 | 9,662 | 120 | 184 | 249 | 320 (3.3%) | 10.0 |
| 550df563ee | 9,646 | 104 | 168 | 225 | 304 (3.2%) | 9.5 |

**Where the opcodes would come from decides it.** Taking the pairs' slots
loses: the pairs with the fewest static sites are among the hottest
(`R@ ROT`, one site, a million dispatches on parse) - four of them carry
3-8% of the dispatches, for 24-120 bytes net. The band the price assumes
is the top of the far-call prefixes (0xE0-0xFF: 32 opcodes), which costs
no slot and no dispatch, and shrinks the far reach at scale 0 from 4 MB to
2 MB - which cv8.4's compiler does not check. The calls through a table of
32: 21-27% of kernel's, 43-46% of parse's and 40-45% of corpus's calls, still
one dispatch each: speed is not the case for it.

## The audit (prompts/03)

- Calibration: converted as the database's converter was
  (`SOD16_OLD_BODYCHECK=1`), the four images are 13,464, 9,785, 9,761 and
  9,745 bytes - exactly the sizes the Ryzen recorded; 8dd8a7a146's pair
  total on kernel was 6,934,908, exactly what price.py recorded in
  Iteration 11.
- Checks, each stops the tool: every site's bytes decode to its target;
  every dispatched address in the image whose byte is a call is a census
  site; per-address counts sum to the pair counts less the profiler's two
  non-dispatches; in each priced image exactly the hot targets' sites
  became one byte, holding their opcodes.
- Found by those checks: the profiler counts an escaped primitive twice
  (0.03%) and, with the 256-entry dispatch, every call twice (8% of
  kernel's dispatches) - so price.py's seed 3 table overstated
  60753a0eb0's dispatches by its calls and doubled its call share (14.8% of
  kernel, really 8.0%; parse 11.8%, really 6.2%). Both tools corrected.
- Direction of error: the raw count (a byte a site) overstated by 1.2-2.7
  times without byte headers and understated with them (links shorten);
  greedy top-K by static bytes is not the best K set - it understates;
  the reach the band takes is not priced in bytes - it flatters.
- Agreed with the expectation (mostly size, no speed) - which is why the
  calibrations above were run on known figures first.

## Found on the way: four format-10 opcodes dead on every front design

The converter gives a kernel word its opcode only where the word's body is
exactly the definition the engine implements. The check read the bodies
after the pairs, the short branches (Phase 3d) and the fused tests
(Iterations 8-12) had rewritten them: `?DUP` read `DUP ?BRANCH8 ...`,
`(LOOP)` read `... =?BRANCH8 ...` - no match, a printed line, and the
design lived without the opcode. **1,032 of seed 3's 1,145 living CV8
designs lost at least one word**; all four front designs lost `(LOOP)`,
`(+LOOP)`, `(?DO)`, `?DUP` (two also `(DO)`, to their pairs). Fixed
(tools/sod16.py: every rewrite off while checking); 0 of 1,145 now; the
evolver kills a design the check fails.

The same image of each front design, old check against the fix, on one
engine (lab/evolve/image-ab.py, B / A; times: this VM, noise):

| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| 8dd8a7a146 | 13464 | 13352 | -112 | 1.000, 1.000, 1.000, 0.999, 1.000 | 1.093, 0.997, 1.005, 1.041, 1.057 | 1.033 |
| 60753a0eb0 | 9785 | 9686 | -99 | 1.000, 1.000, 1.000, 1.000, 1.142 | 1.042, 1.060, 1.025, 1.000, 1.136 | 1.031 |
| f4a6dd9a13 | 9761 | 9662 | -99 | 1.000, 1.000, 1.000, 0.999, 1.135 | 1.039, 1.042, 0.993, 1.070, 1.201 | 1.036 |
| 550df563ee | 9745 | 9646 | -99 | 1.000, 1.000, 1.000, 0.999, 1.135 | 0.942, 0.987, 1.101, 0.992, 1.112 | 1.004 |

Smaller by 99-112 bytes; on the selection workloads the dispatches do not
move - the restored words are cold there. The held-out loop's +14% is not
the fix: loop.fth is compiled at run time, and before a call with an
inline operand - `(LOOP)` - the compiler pads with NOOPs to align the
operand, on every pass. Where HERE lands decides how many: 60753a0eb0's
image shrank by 99 bytes (3 mod 8) and its NOOPs went from 400,833 to
1,600,833 - three more on each of 400,000 passes; 8dd8a7a146 shrank by
112 (0 mod 8) and did not move. **Any two designs whose images differ in
size mod 8 differ on loop by up to seven NOOPs a pass (about 4% each), for
no reason of design.**

## The census, by design

## 8dd8a7a146 - 13352 bytes (13464 as recorded, before the body-check fix); 412 call sites in code to 122 targets

Sites by length: 2 bytes 392, 3 bytes 20; 20 of them before an inline operand (always long); 44 targets called from one site only.

| workload | dispatches | calls | share | calls from the image's code | of all calls |
|---|---|---|---|---|---|
| kernel | 6929465 | 521124 | 7.5% | 230336 | 44.2% |
| fib | 29670318 | 2695085 | 9.1% | 2548 | 0.1% |
| parse | 27734198 | 1076544 | 3.9% | 1076544 | 100.0% |
| corpus | 5040455 | 237753 | 4.7% | 222243 | 93.5% |
| loop | 8855124 | 803339 | 9.1% | 2138 | 0.3% |

The top 32 targets by bytes a one-byte call would save (sites before an inline operand last: their saving depends on alignment), and each one's share of the workload's calls:

| # | target | sites | bytes | callers | kernel | fib | parse | corpus | loop |
|---|---|---|---|---|---|---|---|---|---|
| 1 | HERE | 35 | 35 | 27 | 6.4% | 0.0% | 10.0% | 10.8% | 0.0% |
| 2 | OP, | 28 | 28 | 18 | 0.2% | 0.0% | 0.0% | 0.2% | 0.0% |
| 3 | , | 12 | 12 | 12 | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| 4 | C, | 11 | 11 | 6 | 0.9% | 0.0% | 0.0% | 1.1% | 0.0% |
| 5 | ALIGN | 9 | 9 | 8 | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |
| 6 | TYPE | 9 | 9 | 5 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 7 | (ABORT") | 8 | 8 | 8 | 0.7% | 0.0% | 4.8% | 3.6% | 0.0% |
| 8 | WORD | 8 | 8 | 7 | 0.5% | 0.0% | 3.3% | 2.9% | 0.0% |
| 9 | ALLOT | 8 | 8 | 8 | 1.2% | 0.0% | 0.0% | 1.2% | 0.0% |
| 10 | CR | 8 | 8 | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 11 | OPERAND-ALIGN | 8 | 8 | 8 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 12 | . | 7 | 7 | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 13 | REVEAL | 6 | 6 | 6 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 14 | EXIT-OP | 6 | 6 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 15 | >RESOLVE | 6 | 6 | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 16 | CELLB | 6 | 6 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 17 | NAMEBUF | 5 | 5 | 2 | 5.6% | 0.0% | 11.9% | 10.9% | 0.0% |
| 18 | HEADER | 5 | 5 | 5 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 19 | W, | 5 | 5 | 4 | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| 20 | FORTH-WORDLIST | 5 | 5 | 3 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 21 | BRANCH-OP | 5 | 5 | 5 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 22 | <RESOLVE | 5 | 5 | 5 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 23 | CALL, | 4 | 4 | 4 | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| 24 | NAME> | 4 | 4 | 4 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 25 | LIT, | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% |
| 26 | >MARK | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 27 | 32, | 4 | 4 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 28 | 0BRANCH-OP | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 29 | RESOLVE-LEAVE | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 30 | PLACE | 3 | 3 | 3 | 2.7% | 0.0% | 6.3% | 5.4% | 0.0% |
| 31 | CONTEXT | 3 | 3 | 2 | 2.3% | 0.0% | 5.9% | 5.0% | 0.0% |
| 32 | SOURCE | 3 | 3 | 3 | 1.9% | 0.0% | 3.7% | 3.4% | 0.0% |

Cumulative, the raw count (a byte per near site, two per far): top 1 35, top 2 63, top 4 86, top 8 120, top 16 175, top 32 242, top 64 322, top 122 432 bytes.
The most-called targets, by mean share of calls over the selection workloads: NAMEBUF 7.1% (5 sites), HERE 6.8% (35 sites), CMOVE 3.6% (2 sites), PLACE 3.6% (3 sites), >IN 3.4% (2 sites), CONTEXT 3.3% (3 sites), (ABORT") 2.3% (8 sites), SOURCE 2.3% (3 sites)

The price, exact - the image converted again with the top K as one-byte calls (the slot question aside), the table at 2 bytes an entry:

| K | sites | raw bytes | image bytes saved | table | net | net per slot | calls through the table: kernel, fib, parse, corpus |
|---|---|---|---|---|---|---|---|
| 4 | 86 | 86 | 32 | 8 | 24 | 6.0 | 7.6%, 0.0%, 10.0%, 12.1% |
| 8 | 120 | 120 | 56 | 16 | 40 | 5.0 | 9.1%, 0.0%, 18.2%, 18.8% |
| 16 | 175 | 175 | 128 | 32 | 96 | 6.0 | 10.4%, 0.0%, 18.2%, 20.1% |
| 32 | 242 | 242 | 200 | 64 | 136 | 4.2 | 23.2%, 0.0%, 46.1%, 45.1% |

What holds the slots now: 34 slot users (21 format-10, 13 pairs), fewest static sites first - each site is about a byte saved:

| opcode | user | static sites | dispatches: kernel, fib, parse, corpus |
|---|---|---|---|
| 40 | J | 0 | 0, 0, 0, 0 |
| 42 | (?DO) | 0 | 0, 0, 0, 0 |
| 43 | (+LOOP) | 0 | 0, 0, 0, 0 |
| 44 | (LEAVE) | 0 | 0, 0, 0, 0 |
| 47 | ?NBRANCH | 0 | 0, 0, 0, 0 |
| 49 | <?BRANCH | 0 | 0, 0, 0, 0 |
| 51 | =?BRANCH | 0 | 0, 0, 0, 0 |
| 53 | U<?BRANCH | 0 | 0, 0, 0, 0 |
| 58 | >R C! | 0 | 0, 0, 0, 0 |
| 65 | C@ DUP | 0 | 0, 0, 0, 0 |
| 39 | UNLOOP | 1 | 24, 1, 0, 20 |
| 60 | R@ ROT | 1 | 259296, 1600, 1024352, 188452 |
| 67 | LSHIFT OVER | 1 | 7583, 54, 32011, 6117 |
| 64 | C@ = | 2 | 445, 17, 0, 179 |
| 57 | C! R> | 3 | 298827, 1934, 1128518, 217328 |
| 59 | ROT DUP | 3 | 33184, 303, 112108, 27793 |
| 126 | EXECUTE | 3 | 1523, 33, 16011, 3764 |
| 38 | ?DUP | 4 | 414, 35, 33, 147 |
| 52 | =?BRANCH8 | 4 | 54589, 557, 472155, 65451 |
| 54 | U<?BRANCH8 | 4 | 113, 9, 0, 195 |
| 56 | >R DUP | 4 | 7801, 50, 32011, 6868 |
| 50 | <?BRANCH8 | 5 | 554, 3, 0, 348 |
| 62 | >R OVER | 5 | 40767, 357, 144119, 33687 |
| 63 | OVER C@ | 6 | 39840, 349, 152166, 33739 |
| 66 | SWAP R> | 6 | 44471, 378, 120178, 33745 |
| 36 | (DO) | 7 | 25, 2, 1, 21 |
| 41 | (LOOP) | 7 | 162, 46, 32, 181 |
| 127 | I | 9 | 210, 48, 32, 221 |
| 37 | +! | 10 | 18844, 181, 64032, 15532 |
| 55 | DUP >R | 10 | 345285, 2324, 1280696, 253955 |
| 61 | DUP C@ | 11 | 83039, 1093, 116381, 37665 |
| 48 | ?NBRANCH8 | 15 | 300057, 1960, 1192520, 225213 |
| 46 | BRANCH8 | 45 | 114775, 1470, 260536, 70528 |
| 45 | ?BRANCH8 | 80 | 328762, 3935, 1417199, 262611 |

Taking the 4 fewest-site pairs' slots (>R C!, C@ DUP, R@ ROT, LSHIFT OVER): the image grows 0 bytes without them; with the 4 hottest targets in their place, net of the table, -24 bytes; the pairs removed 266879/1654/1056363/194569 dispatches on kernel/fib/parse/corpus.
Taking the 8 fewest-site pairs' slots (>R C!, C@ DUP, R@ ROT, LSHIFT OVER, C@ =, C! R>, ROT DUP, >R DUP): the image grows 16 bytes without them; with the 8 hottest targets in their place, net of the table, -24 bytes; the pairs removed 607136/3958/2329000/446737 dispatches on kernel/fib/parse/corpus.

(Dispatched in the image off the census's operation starts - padding and data bodies: corpus byte 0: 306, corpus byte 69: 53898, fib byte 69: 583, kernel byte 0: 135, kernel byte 69: 61985, loop byte 0: 16, loop byte 69: 496, parse byte 69: 256160.)

## 60753a0eb0 - 9686 bytes (9785 as recorded, before the body-check fix); 456 call sites in code to 127 targets

Sites by length: 2 bytes 436, 3 bytes 20; 20 of them before an inline operand (always long); 43 targets called from one site only.

| workload | dispatches | calls | share | calls from the image's code | of all calls |
|---|---|---|---|---|---|
| kernel | 7295465 | 582225 | 8.0% | 291437 | 50.1% |
| fib | 29674355 | 2695842 | 9.1% | 3305 | 0.1% |
| parse | 31723081 | 1980694 | 6.2% | 1980694 | 100.0% |
| corpus | 5545174 | 336416 | 6.1% | 320906 | 95.4% |
| loop | 9657513 | 803878 | 8.3% | 2677 | 0.3% |

The top 32 targets by bytes a one-byte call would save (sites before an inline operand last: their saving depends on alignment), and each one's share of the workload's calls:

| # | target | sites | bytes | callers | kernel | fib | parse | corpus | loop |
|---|---|---|---|---|---|---|---|---|---|
| 1 | HERE | 50 | 50 | 28 | 5.4% | 0.0% | 5.5% | 7.2% | 0.0% |
| 2 | OP, | 28 | 28 | 18 | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| 3 | C, | 17 | 17 | 7 | 0.7% | 0.0% | 0.0% | 0.5% | 0.0% |
| 4 | , | 11 | 11 | 11 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 5 | NAMEBUF | 10 | 10 | 3 | 10.7% | 0.0% | 29.9% | 23.2% | 0.1% |
| 6 | TYPE | 10 | 10 | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 7 | WORD | 9 | 9 | 8 | 0.5% | 0.0% | 1.8% | 2.1% | 0.0% |
| 8 | ALLOT | 9 | 9 | 9 | 0.8% | 0.0% | 0.0% | 0.6% | 0.0% |
| 9 | CR | 9 | 9 | 7 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 10 | (ABORT") | 8 | 8 | 8 | 0.7% | 0.0% | 2.6% | 2.5% | 0.0% |
| 11 | OPERAND-ALIGN | 8 | 8 | 8 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 12 | ALIGN | 7 | 7 | 7 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 13 | . | 7 | 7 | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 14 | REVEAL | 6 | 6 | 6 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 15 | EXIT-OP | 6 | 6 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 16 | >RESOLVE | 6 | 6 | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 17 | CELLB | 6 | 6 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 18 | HASH | 5 | 5 | 5 | 1.3% | 0.0% | 1.6% | 1.8% | 0.0% |
| 19 | HEADER | 5 | 5 | 5 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 20 | W, | 5 | 5 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 21 | FORTH-WORDLIST | 5 | 5 | 3 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 22 | BRANCH-OP | 5 | 5 | 5 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 23 | <RESOLVE | 5 | 5 | 5 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 24 | FIND | 4 | 4 | 4 | 0.3% | 0.0% | 1.6% | 1.7% | 0.0% |
| 25 | CALL, | 4 | 4 | 4 | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| 26 | CMOVE> | 4 | 4 | 4 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 27 | NAME> | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 28 | LIT, | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 29 | (.") | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 30 | >MARK | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 31 | 32, | 4 | 4 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 32 | 0BRANCH-OP | 4 | 4 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Cumulative, the raw count (a byte per near site, two per far): top 1 50, top 2 78, top 4 106, top 8 144, top 16 201, top 32 273, top 64 355, top 127 476 bytes.
The most-called targets, by mean share of calls over the selection workloads: NAMEBUF 16.0% (10 sites), NEXT-NFA8 8.3% (2 sites), HERE 4.5% (50 sites), CMOVE 2.4% (2 sites), PLACE 2.4% (3 sites), >IN 2.3% (2 sites), CONTEXT 2.2% (3 sites), NAME=? 1.8% (2 sites)

The price, exact - the image converted again with the top K as one-byte calls (the slot question aside), the table at 2 bytes an entry:

| K | sites | raw bytes | image bytes saved | table | net | net per slot | calls through the table: kernel, fib, parse, corpus |
|---|---|---|---|---|---|---|---|
| 4 | 106 | 106 | 112 | 8 | 104 | 26.0 | 6.2%, 0.0%, 5.5%, 7.9% |
| 8 | 144 | 144 | 145 | 16 | 129 | 16.1 | 18.2%, 0.0%, 37.2%, 33.8% |
| 16 | 201 | 201 | 188 | 32 | 156 | 9.8 | 19.1%, 0.0%, 39.8%, 36.4% |
| 32 | 273 | 273 | 285 | 64 | 221 | 6.9 | 21.0%, 0.1%, 43.0%, 40.2% |

What holds the slots now: 34 slot users (21 format-10, 13 pairs), fewest static sites first - each site is about a byte saved:

| opcode | user | static sites | dispatches: kernel, fib, parse, corpus |
|---|---|---|---|
| 40 | J | 0 | 0, 0, 0, 0 |
| 42 | (?DO) | 0 | 0, 0, 0, 0 |
| 43 | (+LOOP) | 0 | 0, 0, 0, 0 |
| 44 | (LEAVE) | 0 | 0, 0, 0, 0 |
| 47 | ?NBRANCH | 0 | 0, 0, 0, 0 |
| 49 | <?BRANCH | 0 | 0, 0, 0, 0 |
| 51 | =?BRANCH | 0 | 0, 0, 0, 0 |
| 53 | U<?BRANCH | 0 | 0, 0, 0, 0 |
| 58 | >R C! | 0 | 0, 0, 0, 0 |
| 39 | UNLOOP | 1 | 24, 1, 0, 20 |
| 60 | R@ ROT | 1 | 259296, 1600, 1024352, 188452 |
| 65 | C@ DUP | 1 | 21334, 277, 368048, 36555 |
| 52 | =?BRANCH8 | 2 | 25122, 219, 80093, 22038 |
| 38 | ?DUP | 3 | 33, 33, 33, 33 |
| 57 | C! R> | 3 | 301309, 1944, 1128518, 217959 |
| 59 | ROT DUP | 3 | 33184, 303, 112108, 27793 |
| 67 | LSHIFT OVER | 3 | 22698, 261, 284047, 31326 |
| 126 | EXECUTE | 3 | 1523, 33, 16011, 3764 |
| 56 | >R DUP | 4 | 7801, 50, 32011, 6868 |
| 64 | C@ = | 4 | 26194, 337, 384059, 40889 |
| 50 | <?BRANCH8 | 5 | 554, 3, 0, 348 |
| 62 | >R OVER | 6 | 58655, 501, 220153, 51646 |
| 66 | SWAP R> | 6 | 56333, 447, 140193, 42395 |
| 36 | (DO) | 7 | 25, 2, 1, 21 |
| 41 | (LOOP) | 7 | 162, 46, 32, 181 |
| 63 | OVER C@ | 7 | 60210, 503, 228200, 52329 |
| 54 | U<?BRANCH8 | 8 | 37141, 497, 620084, 62137 |
| 127 | I | 9 | 210, 48, 32, 221 |
| 37 | +! | 10 | 17457, 170, 64032, 14690 |
| 55 | DUP >R | 11 | 350249, 2344, 1280696, 255217 |
| 61 | DUP C@ | 13 | 101167, 1368, 500440, 76240 |
| 48 | ?NBRANCH8 | 16 | 320427, 2114, 1268554, 243803 |
| 46 | BRANCH8 | 55 | 153531, 1906, 764623, 128449 |
| 45 | ?BRANCH8 | 92 | 378367, 4523, 2057329, 340862 |

Taking the 4 fewest-site pairs' slots (>R C!, R@ ROT, C@ DUP, C! R>): the image grows 8 bytes without them; with the 4 hottest targets in their place, net of the table, -96 bytes; the pairs removed 581939/3821/2520918/442966 dispatches on kernel/fib/parse/corpus.
Taking the 8 fewest-site pairs' slots (>R C!, R@ ROT, C@ DUP, C! R>, ROT DUP, LSHIFT OVER, >R DUP, C@ =): the image grows 8 bytes without them; with the 8 hottest targets in their place, net of the table, -113 bytes; the pairs removed 671816/4772/3333143/549842 dispatches on kernel/fib/parse/corpus.

(Dispatched in the image off the census's operation starts - padding and data bodies: corpus byte 0: 810, corpus byte 69: 105024, fib byte 0: 6, fib byte 69: 974, kernel byte 0: 14914, kernel byte 69: 93731, loop byte 0: 32, loop byte 69: 769, parse byte 0: 6, parse byte 69: 720233.)

## f4a6dd9a13 - 9662 bytes (9761 as recorded, before the body-check fix); 661 call sites in code to 155 targets

Sites by length: 2 bytes 641, 3 bytes 20; 20 of them before an inline operand (always long); 44 targets called from one site only.

| workload | dispatches | calls | share | calls from the image's code | of all calls |
|---|---|---|---|---|---|
| kernel | 7414886 | 688712 | 9.3% | 397924 | 57.8% |
| fib | 29676132 | 2697200 | 9.1% | 4663 | 0.2% |
| parse | 32439486 | 2493017 | 7.7% | 2493017 | 100.0% |
| corpus | 5680279 | 439271 | 7.7% | 423761 | 96.5% |
| loop | 10058638 | 805033 | 8.0% | 3832 | 0.5% |

The top 32 targets by bytes a one-byte call would save (sites before an inline operand last: their saving depends on alignment), and each one's share of the workload's calls:

| # | target | sites | bytes | callers | kernel | fib | parse | corpus | loop |
|---|---|---|---|---|---|---|---|---|---|
| 1 | HERE | 50 | 50 | 28 | 4.6% | 0.0% | 4.3% | 5.6% | 0.0% |
| 2 | OP, | 28 | 28 | 18 | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| 3 | C, | 17 | 17 | 7 | 0.6% | 0.0% | 0.0% | 0.4% | 0.0% |
| 4 | 'LEAVE | 17 | 17 | 11 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 5 | LAST-OP | 13 | 13 | 9 | 0.2% | 0.0% | 0.0% | 0.2% | 0.0% |
| 6 | >IN | 12 | 12 | 5 | 4.5% | 0.0% | 5.6% | 6.2% | 0.0% |
| 7 | BASE | 12 | 12 | 6 | 0.2% | 0.0% | 3.2% | 2.3% | 0.0% |
| 8 | NFA | 12 | 12 | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 9 | , | 11 | 11 | 11 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 10 | NAMEBUF | 10 | 10 | 3 | 9.1% | 0.0% | 23.8% | 17.7% | 0.1% |
| 11 | #SRC | 10 | 10 | 4 | 2.1% | 0.0% | 1.9% | 2.3% | 0.0% |
| 12 | HDR-HEAD | 10 | 10 | 2 | 0.3% | 0.0% | 0.0% | 0.1% | 0.0% |
| 13 | TYPE | 10 | 10 | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 14 | ACC-W | 10 | 10 | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 15 | SRC | 9 | 9 | 5 | 1.8% | 0.0% | 1.8% | 2.1% | 0.0% |
| 16 | WORD | 9 | 9 | 8 | 0.4% | 0.0% | 1.4% | 1.6% | 0.0% |
| 17 | ALLOT | 9 | 9 | 9 | 0.7% | 0.0% | 0.0% | 0.5% | 0.0% |
| 18 | CR | 9 | 9 | 7 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 19 | (ABORT") | 8 | 8 | 8 | 0.6% | 0.0% | 2.1% | 1.9% | 0.0% |
| 20 | STATE | 8 | 8 | 7 | 0.3% | 0.0% | 1.3% | 1.4% | 0.0% |
| 21 | SID | 8 | 8 | 4 | 0.9% | 0.0% | 0.5% | 0.7% | 0.0% |
| 22 | HDR-LEN | 8 | 8 | 2 | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |
| 23 | LAST | 8 | 8 | 8 | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |
| 24 | OPERAND-ALIGN | 8 | 8 | 8 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 25 | CURRENT | 7 | 7 | 4 | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |
| 26 | ALIGN | 7 | 7 | 7 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 27 | FORTH-WORDLIST | 7 | 7 | 3 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 28 | . | 7 | 7 | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 29 | BP | 7 | 7 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 30 | START | 6 | 6 | 3 | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| 31 | REVEAL | 6 | 6 | 6 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 32 | EXIT-OP | 6 | 6 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Cumulative, the raw count (a byte per near site, two per far): top 1 50, top 2 78, top 4 112, top 8 161, top 16 240, top 32 359, top 64 494, top 155 681 bytes.
The most-called targets, by mean share of calls over the selection workloads: NAMEBUF 12.6% (10 sites), NEXT-NFA8 6.5% (2 sites), >IN 4.1% (12 sites), DP 3.9% (4 sites), HERE 3.6% (50 sites), CMOVE 1.9% (2 sites), PLACE 1.9% (3 sites), CONTEXT 1.7% (4 sites)

The price, exact - the image converted again with the top K as one-byte calls (the slot question aside), the table at 2 bytes an entry:

| K | sites | raw bytes | image bytes saved | table | net | net per slot | calls through the table: kernel, fib, parse, corpus |
|---|---|---|---|---|---|---|---|
| 4 | 112 | 112 | 128 | 8 | 120 | 30.0 | 5.3%, 0.0%, 4.3%, 6.1% |
| 8 | 161 | 161 | 200 | 16 | 184 | 23.0 | 10.1%, 0.0%, 13.2%, 14.7% |
| 16 | 240 | 240 | 281 | 32 | 249 | 15.6 | 23.6%, 0.1%, 42.1%, 38.6% |
| 32 | 359 | 359 | 384 | 64 | 320 | 10.0 | 26.9%, 0.1%, 45.9%, 43.4% |

What holds the slots now: 34 slot users (21 format-10, 13 pairs), fewest static sites first - each site is about a byte saved:

| opcode | user | static sites | dispatches: kernel, fib, parse, corpus |
|---|---|---|---|
| 39 | J | 0 | 0, 0, 0, 0 |
| 41 | (?DO) | 0 | 0, 0, 0, 0 |
| 42 | (+LOOP) | 0 | 0, 0, 0, 0 |
| 43 | (LEAVE) | 0 | 0, 0, 0, 0 |
| 46 | ?NBRANCH | 0 | 0, 0, 0, 0 |
| 48 | <?BRANCH | 0 | 0, 0, 0, 0 |
| 50 | =?BRANCH | 0 | 0, 0, 0, 0 |
| 52 | U<?BRANCH | 0 | 0, 0, 0, 0 |
| 57 | >R C! | 0 | 0, 0, 0, 0 |
| 38 | UNLOOP | 1 | 24, 1, 0, 20 |
| 59 | R@ ROT | 1 | 259296, 1600, 1024352, 188452 |
| 63 | C@ DUP | 1 | 21334, 277, 368048, 36555 |
| 66 | OVER R> | 2 | 7635, 85, 36019, 7228 |
| 54 | ?DUP | 3 | 33, 33, 33, 33 |
| 56 | C! R> | 3 | 301309, 1944, 1128518, 217959 |
| 58 | ROT DUP | 3 | 33184, 303, 112108, 27793 |
| 65 | LSHIFT OVER | 3 | 22698, 261, 284047, 31326 |
| 126 | EXECUTE | 3 | 1523, 33, 16011, 3764 |
| 49 | <?BRANCH8 | 5 | 554, 3, 0, 348 |
| 51 | =?BRANCH8 | 5 | 51008, 555, 464152, 62919 |
| 61 | >R OVER | 6 | 58655, 501, 220153, 51646 |
| 64 | SWAP R> | 6 | 56333, 447, 140193, 42395 |
| 36 | (DO) | 7 | 25, 2, 1, 21 |
| 40 | (LOOP) | 7 | 145, 47, 32, 183 |
| 62 | OVER C@ | 7 | 60210, 503, 228200, 52329 |
| 53 | U<?BRANCH8 | 8 | 37141, 497, 620084, 62137 |
| 67 | ROT ROT | 9 | 40222, 353, 144119, 34386 |
| 127 | I | 9 | 193, 49, 32, 223 |
| 37 | +! | 10 | 17457, 170, 64032, 14690 |
| 55 | DUP >R | 11 | 350249, 2344, 1280696, 255217 |
| 60 | DUP C@ | 13 | 101167, 1368, 500440, 76240 |
| 47 | ?NBRANCH8 | 16 | 320427, 2114, 1268554, 243803 |
| 45 | BRANCH8 | 55 | 153531, 1906, 764623, 128449 |
| 44 | ?BRANCH8 | 89 | 352464, 4188, 1673270, 299983 |

Taking the 4 fewest-site pairs' slots (>R C!, R@ ROT, C@ DUP, OVER R>): the image grows 0 bytes without them; with the 4 hottest targets in their place, net of the table, -120 bytes; the pairs removed 288265/1962/1428419/232235 dispatches on kernel/fib/parse/corpus.
Taking the 8 fewest-site pairs' slots (>R C!, R@ ROT, C@ DUP, OVER R>, C! R>, ROT DUP, LSHIFT OVER, >R OVER): the image grows 0 bytes without them; with the 8 hottest targets in their place, net of the table, -168 bytes; the pairs removed 704111/4971/3173245/560959 dispatches on kernel/fib/parse/corpus.

(Dispatched in the image off the census's operation starts - padding and data bodies: corpus byte 0: 995, corpus byte 69: 207879, fib byte 0: 7, fib byte 69: 2332, kernel byte 0: 9935, kernel byte 69: 200218, loop byte 0: 35, loop byte 69: 1924, parse byte 0: 7, parse byte 69: 1232556.)

## 550df563ee - 9646 bytes (9745 as recorded, before the body-check fix); 661 call sites in code to 155 targets

Sites by length: 2 bytes 641, 3 bytes 20; 20 of them before an inline operand (always long); 44 targets called from one site only.

| workload | dispatches | calls | share | calls from the image's code | of all calls |
|---|---|---|---|---|---|
| kernel | 7429769 | 688729 | 9.3% | 397941 | 57.8% |
| fib | 29676313 | 2697199 | 9.1% | 4662 | 0.2% |
| parse | 32735514 | 2493017 | 7.6% | 2493017 | 100.0% |
| corpus | 5709123 | 439269 | 7.7% | 423759 | 96.5% |
| loop | 10058771 | 805032 | 8.0% | 3831 | 0.5% |

The top 32 targets by bytes a one-byte call would save (sites before an inline operand last: their saving depends on alignment), and each one's share of the workload's calls:

| # | target | sites | bytes | callers | kernel | fib | parse | corpus | loop |
|---|---|---|---|---|---|---|---|---|---|
| 1 | HERE | 50 | 50 | 28 | 4.6% | 0.0% | 4.3% | 5.6% | 0.0% |
| 2 | OP, | 28 | 28 | 18 | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| 3 | C, | 17 | 17 | 7 | 0.6% | 0.0% | 0.0% | 0.4% | 0.0% |
| 4 | 'LEAVE | 17 | 17 | 11 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 5 | LAST-OP | 13 | 13 | 9 | 0.2% | 0.0% | 0.0% | 0.2% | 0.0% |
| 6 | >IN | 12 | 12 | 5 | 4.5% | 0.0% | 5.6% | 6.2% | 0.0% |
| 7 | BASE | 12 | 12 | 6 | 0.2% | 0.0% | 3.2% | 2.3% | 0.0% |
| 8 | NFA | 12 | 12 | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 9 | , | 11 | 11 | 11 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 10 | NAMEBUF | 10 | 10 | 3 | 9.1% | 0.0% | 23.8% | 17.7% | 0.1% |
| 11 | #SRC | 10 | 10 | 4 | 2.1% | 0.0% | 1.9% | 2.3% | 0.0% |
| 12 | HDR-HEAD | 10 | 10 | 2 | 0.3% | 0.0% | 0.0% | 0.1% | 0.0% |
| 13 | TYPE | 10 | 10 | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 14 | ACC-W | 10 | 10 | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 15 | SRC | 9 | 9 | 5 | 1.8% | 0.0% | 1.8% | 2.1% | 0.0% |
| 16 | WORD | 9 | 9 | 8 | 0.4% | 0.0% | 1.4% | 1.6% | 0.0% |
| 17 | ALLOT | 9 | 9 | 9 | 0.7% | 0.0% | 0.0% | 0.5% | 0.0% |
| 18 | CR | 9 | 9 | 7 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 19 | (ABORT") | 8 | 8 | 8 | 0.6% | 0.0% | 2.1% | 1.9% | 0.0% |
| 20 | STATE | 8 | 8 | 7 | 0.3% | 0.0% | 1.3% | 1.4% | 0.0% |
| 21 | SID | 8 | 8 | 4 | 0.9% | 0.0% | 0.5% | 0.7% | 0.0% |
| 22 | HDR-LEN | 8 | 8 | 2 | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |
| 23 | LAST | 8 | 8 | 8 | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |
| 24 | OPERAND-ALIGN | 8 | 8 | 8 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 25 | CURRENT | 7 | 7 | 4 | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |
| 26 | ALIGN | 7 | 7 | 7 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 27 | FORTH-WORDLIST | 7 | 7 | 3 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 28 | . | 7 | 7 | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 29 | BP | 7 | 7 | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| 30 | START | 6 | 6 | 3 | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| 31 | REVEAL | 6 | 6 | 6 | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| 32 | EXIT-OP | 6 | 6 | 4 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Cumulative, the raw count (a byte per near site, two per far): top 1 50, top 2 78, top 4 112, top 8 161, top 16 240, top 32 359, top 64 494, top 155 681 bytes.
The most-called targets, by mean share of calls over the selection workloads: NAMEBUF 12.6% (10 sites), NEXT-NFA8 6.5% (2 sites), >IN 4.1% (12 sites), DP 3.9% (4 sites), HERE 3.6% (50 sites), CMOVE 1.9% (2 sites), PLACE 1.9% (3 sites), CONTEXT 1.7% (4 sites)

The price, exact - the image converted again with the top K as one-byte calls (the slot question aside), the table at 2 bytes an entry:

| K | sites | raw bytes | image bytes saved | table | net | net per slot | calls through the table: kernel, fib, parse, corpus |
|---|---|---|---|---|---|---|---|
| 4 | 112 | 112 | 112 | 8 | 104 | 26.0 | 5.3%, 0.0%, 4.3%, 6.1% |
| 8 | 161 | 161 | 184 | 16 | 168 | 21.0 | 10.1%, 0.0%, 13.2%, 14.7% |
| 16 | 240 | 240 | 257 | 32 | 225 | 14.1 | 23.6%, 0.1%, 42.1%, 38.6% |
| 32 | 359 | 359 | 368 | 64 | 304 | 9.5 | 26.9%, 0.1%, 45.9%, 43.4% |

What holds the slots now: 34 slot users (21 format-10, 13 pairs), fewest static sites first - each site is about a byte saved:

| opcode | user | static sites | dispatches: kernel, fib, parse, corpus |
|---|---|---|---|
| 38 | (+LOOP) | 0 | 0, 0, 0, 0 |
| 39 | (LEAVE) | 0 | 0, 0, 0, 0 |
| 42 | ?NBRANCH | 0 | 0, 0, 0, 0 |
| 44 | <?BRANCH | 0 | 0, 0, 0, 0 |
| 46 | =?BRANCH | 0 | 0, 0, 0, 0 |
| 48 | U<?BRANCH | 0 | 0, 0, 0, 0 |
| 50 | J | 0 | 0, 0, 0, 0 |
| 54 | (?DO) | 0 | 0, 0, 0, 0 |
| 57 | >R C! | 0 | 0, 0, 0, 0 |
| 53 | UNLOOP | 1 | 24, 1, 0, 20 |
| 59 | R@ ROT | 1 | 259296, 1600, 1024352, 188452 |
| 63 | C@ DUP | 1 | 21334, 277, 368048, 36555 |
| 47 | =?BRANCH8 | 2 | 25122, 219, 80093, 22038 |
| 66 | C@ SWAP | 2 | 42013, 344, 104166, 29507 |
| 49 | ?DUP | 3 | 33, 33, 33, 33 |
| 56 | C! R> | 3 | 301309, 1944, 1128518, 217959 |
| 58 | ROT DUP | 3 | 33184, 303, 112108, 27793 |
| 126 | EXECUTE | 3 | 1523, 33, 16011, 3764 |
| 45 | <?BRANCH8 | 5 | 554, 3, 0, 348 |
| 62 | C@ = | 5 | 44082, 481, 460093, 58848 |
| 64 | SWAP R> | 5 | 56209, 447, 140193, 42375 |
| 67 | R> SWAP | 5 | 15394, 170, 72038, 14490 |
| 61 | >R OVER | 6 | 58655, 501, 220153, 51646 |
| 36 | (DO) | 7 | 25, 2, 1, 21 |
| 51 | (LOOP) | 7 | 162, 46, 32, 181 |
| 52 | U<?BRANCH8 | 8 | 37141, 497, 620084, 62137 |
| 65 | ROT ROT | 9 | 40222, 353, 144119, 34386 |
| 127 | I | 9 | 210, 48, 32, 221 |
| 37 | +! | 10 | 17457, 170, 64032, 14690 |
| 55 | DUP >R | 11 | 350249, 2344, 1280696, 255217 |
| 60 | DUP C@ | 13 | 101167, 1368, 500440, 76240 |
| 43 | ?NBRANCH8 | 16 | 320427, 2114, 1268554, 243803 |
| 41 | BRANCH8 | 55 | 153531, 1906, 764623, 128449 |
| 40 | ?BRANCH8 | 92 | 378367, 4523, 2057329, 340862 |

Taking the 4 fewest-site pairs' slots (>R C!, R@ ROT, C@ DUP, C@ SWAP): the image grows 8 bytes without them; with the 4 hottest targets in their place, net of the table, -96 bytes; the pairs removed 322643/2221/1496566/254514 dispatches on kernel/fib/parse/corpus.
Taking the 8 fewest-site pairs' slots (>R C!, R@ ROT, C@ DUP, C@ SWAP, C! R>, ROT DUP, C@ =, SWAP R>): the image grows 16 bytes without them; with the 8 hottest targets in their place, net of the table, -144 bytes; the pairs removed 757427/5396/3337478/601489 dispatches on kernel/fib/parse/corpus.

(Dispatched in the image off the census's operation starts - padding and data bodies: corpus byte 0: 918, corpus byte 69: 207877, fib byte 0: 7, fib byte 69: 2331, kernel byte 0: 9601, kernel byte 69: 200235, loop byte 0: 35, loop byte 69: 1923, parse byte 0: 7, parse byte 69: 1232556.)

